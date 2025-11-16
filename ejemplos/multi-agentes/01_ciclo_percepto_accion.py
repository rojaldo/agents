"""
SECCION 1.1 - EJEMPLO 01: Ciclo Percepto-Acción Básico
========================================================

Objetivo Educativo:
    Entender el ciclo fundamental de un agente:
    1. PERCIBIR: Obtener información del ambiente
    2. RAZONAR: Procesar y tomar decisión
    3. ACTUAR: Ejecutar acción
    4. Repetir

Usando LangChain + Ollama Local:
    - Agente que percibe números
    - LLM razona sobre qué hacer
    - Agente actúa (ejecuta operación)
    - Ciclo completo

Pre-requisitos:
    - Ollama corriendo: ollama serve
    - Modelo descargado: ollama pull mistral
    - LangChain instalado: pip install langchain langchain-ollama
"""

import sys
from datetime import datetime
from typing import Dict, Any

# Importar configuración centralizada
try:
    from config_ollama import obtener_llm, MODELO_DEFECTO
except ImportError:
    print("❌ Error: No se puede importar config_ollama")
    print("   Asegúrate de estar en el directorio 'ejemplos'")
    sys.exit(1)


class AgenteNumerico:
    """
    Agente simple que razona sobre números usando LLM.
    
    El ciclo:
    1. PERCIBIR: Lee número del ambiente
    2. RAZONAR: Pide a LLM que decida acción
    3. ACTUAR: Ejecuta acción (suma, resta, etc.)
    4. Registra en histórico
    """
    
    def __init__(self, nombre: str, modelo: str = MODELO_DEFECTO):
        """
        Inicializa el agente.
        
        Args:
            nombre: identificador del agente
            modelo: modelo Ollama a usar
        """
        self.nombre = nombre
        self.llm = obtener_llm(modelo)
        self.modelo = modelo
        self.historico = []  # Registro de ciclos
        self.valor_actual = 0  # Estado interno
        self.ciclo_num = 0
        
        print(f"🤖 Agente '{self.nombre}' inicializado")
        print(f"   Modelo: {self.modelo}")
        print(f"   Fecha: {datetime.now().strftime('%H:%M:%S')}\n")
    
    def percibir(self, numero: int) -> Dict[str, Any]:
        """
        FASE 1: PERCEPCIÓN
        
        Lee el número del ambiente y lo procesa.
        """
        percepcion = {
            "timestamp": datetime.now().isoformat(),
            "numero_percibido": numero,
            "valor_actual": self.valor_actual,
            "diferencia": numero - self.valor_actual,
        }
        
        print(f"📊 [{self.nombre}] PERCEPCIÓN")
        print(f"   Número percibido: {numero}")
        print(f"   Valor actual interno: {self.valor_actual}")
        print(f"   Diferencia: {percepcion['diferencia']}\n")
        
        return percepcion
    
    def razonar(self, percepcion: Dict[str, Any]) -> str:
        """
        FASE 2: RAZONAMIENTO
        
        Usa LLM para decidir qué acción tomar basado en la percepción.
        """
        numero = percepcion["numero_percibido"]
        actual = percepcion["valor_actual"]
        diferencia = percepcion["diferencia"]
        
        # Construir prompt para que LLM razone
        prompt = f"""Eres un agente automático que debe decidir una acción.

CONTEXTO:
- Número observado: {numero}
- Valor actual del agente: {actual}
- Diferencia: {diferencia}

ACCIONES POSIBLES:
1. 'SUMAR' - Aumentar valor actual
2. 'RESTAR' - Disminuir valor actual
3. 'MULTIPLICAR' - Multiplicar por el número observado
4. 'DIVIDIR' - Dividir entre el número observado (si es posible)
5. 'MANTENER' - No cambiar valor

CRITERIO DE DECISIÓN:
- Si diferencia es positiva y > 5: SUMAR
- Si diferencia es negativa y < -5: RESTAR
- Si valor actual es 0: MULTIPLICAR
- Si diferencia es pequeña (abs < 3): MANTENER
- Otro caso: DIVIDIR si es posible

Decide la acción más apropiada en UNA PALABRA (solo la acción, nada más).
"""
        
        print(f"🧠 [{self.nombre}] RAZONAMIENTO")
        print("   Consultando LLM...")
        
        # Invocar LLM
        decision = self.llm.invoke(prompt).strip().upper()
        
        # Validar que sea una acción válida
        acciones_validas = ["SUMAR", "RESTAR", "MULTIPLICAR", "DIVIDIR", "MANTENER"]
        if decision not in acciones_validas:
            # Si LLM devuelve algo inválido, parsear
            decision_encontrada = None
            for accion in acciones_validas:
                if accion in decision:
                    decision_encontrada = accion
                    break
            decision = decision_encontrada or "MANTENER"
        
        print(f"   Decisión LLM: {decision}\n")
        
        return decision
    
    def actuar(self, accion: str, numero: int) -> int:
        """
        FASE 3: ACCIÓN
        
        Ejecuta la acción y actualiza estado interno.
        """
        print(f"⚡ [{self.nombre}] ACCIÓN")
        print(f"   Acción ejecutada: {accion}")
        
        valor_anterior = self.valor_actual
        
        try:
            if accion == "SUMAR":
                self.valor_actual += numero
                print(f"   Operación: {valor_anterior} + {numero} = {self.valor_actual}")
            
            elif accion == "RESTAR":
                self.valor_actual -= numero
                print(f"   Operación: {valor_anterior} - {numero} = {self.valor_actual}")
            
            elif accion == "MULTIPLICAR":
                if numero != 0:
                    self.valor_actual *= numero
                    print(f"   Operación: {valor_anterior} × {numero} = {self.valor_actual}")
                else:
                    print("   Operación: IMPOSIBLE (número = 0)")
            
            elif accion == "DIVIDIR":
                if numero != 0:
                    self.valor_actual = int(self.valor_actual / numero)
                    print(f"   Operación: {valor_anterior} ÷ {numero} = {self.valor_actual}")
                else:
                    print("   Operación: IMPOSIBLE (división por cero)")
            
            elif accion == "MANTENER":
                print(f"   Operación: Mantener valor = {self.valor_actual}")
        
        except Exception as e:
            print(f"   ❌ Error en operación: {e}")
        
        print(f"   Nuevo valor: {self.valor_actual}\n")
        
        return self.valor_actual
    
    def ejecutar_ciclo(self, numero_entrada: int) -> Dict[str, Any]:
        """
        Ejecuta un ciclo completo percepto-acción.
        
        Returns:
            Información del ciclo ejecutado
        """
        self.ciclo_num += 1
        
        print("=" * 70)
        print(f"🔄 CICLO #{self.ciclo_num}")
        print("=" * 70 + "\n")
        
        # 1. PERCIBIR
        percepcion = self.percibir(numero_entrada)
        
        # 2. RAZONAR
        accion = self.razonar(percepcion)
        
        # 3. ACTUAR
        nuevo_valor = self.actuar(accion, numero_entrada)
        
        # 4. Registrar ciclo
        ciclo_data = {
            "ciclo": self.ciclo_num,
            "timestamp": datetime.now().isoformat(),
            "entrada": numero_entrada,
            "accion": accion,
            "valor_anterior": percepcion["valor_actual"],
            "valor_nuevo": nuevo_valor,
        }
        
        self.historico.append(ciclo_data)
        
        print("✅ Ciclo completado\n")
        
        return ciclo_data
    
    def mostrar_historico(self) -> None:
        """Muestra resumen del histórico de ciclos."""
        print("\n" + "=" * 70)
        print(f"📈 HISTÓRICO DE CICLOS - {self.nombre}")
        print("=" * 70)
        print(f"{'Ciclo':<6} {'Entrada':<8} {'Acción':<12} {'Ant.':<6} {'Nuevo':<6}")
        print("-" * 70)
        
        for registro in self.historico:
            print(
                f"{registro['ciclo']:<6} "
                f"{registro['entrada']:<8} "
                f"{registro['accion']:<12} "
                f"{registro['valor_anterior']:<6} "
                f"{registro['valor_nuevo']:<6}"
            )
        
        print("-" * 70)
        print(f"Total ciclos: {len(self.historico)}")
        print(f"Valor final: {self.valor_actual}\n")


# ============================================================================
# SIMULACIÓN PRINCIPAL
# ============================================================================

def main():
    """Simulación educativa del ciclo percepto-acción."""
    
    print("\n" + "🎓 " * 35)
    print("EJEMPLO 1.1: CICLO PERCEPTO-ACCIÓN CON LANGCHAIN + OLLAMA")
    print("🎓 " * 35 + "\n")
    
    print("DESCRIPCIÓN:")
    print("-" * 70)
    print("Este ejemplo demuestra el ciclo fundamental de un agente:")
    print("  1. PERCEPCIÓN: El agente observa un número")
    print("  2. RAZONAMIENTO: Un LLM (ejecutando en Ollama local) decide qué hacer")
    print("  3. ACCIÓN: El agente modifica su estado interno")
    print("  4. ITERACIÓN: El ciclo se repite\n")
    
    # Crear agente
    agente = AgenteNumerico("AgenteMatemático")
    
    # Números de entrada para la simulación
    numeros_entrada = [3, -2, 5, 0, 10, 2]
    
    print(f"ENTRADA: {numeros_entrada}\n")
    print("Iniciando ciclos...\n")
    
    # Ejecutar ciclos
    for numero in numeros_entrada:
        agente.ejecutar_ciclo(numero)
    
    # Mostrar análisis final
    agente.mostrar_historico()
    
    # Análisis
    print("=" * 70)
    print("📊 ANÁLISIS")
    print("=" * 70)
    print("""
OBSERVACIONES EDUCATIVAS:

1. CICLO PERCEPTO-ACCIÓN:
   - Cada iteración sigue: Percibir → Razonar → Actuar
   - El LLM (en Ollama) razona sobre qué acción es mejor
   - El estado del agente (valor_actual) cambia continuamente

2. RACIONALIDAD DEL AGENTE:
   - El agente toma decisiones basadas en:
     * Su percepción actual
     * Su estado interno
     * La capacidad del LLM para razonar
   - Las decisiones emergen de un prompts simple

3. AUTONOMÍA:
   - El agente decide QUÉ HACER sin intervención externa
   - Solo recibe números de entrada (observaciones)
   - Las acciones son seleccionadas automáticamente

4. LIMITACIONES:
   - El LLM puede devolver respuestas inesperadas
   - No hay garantía de optimización global
   - La decisión es tan buena como el modelo y el prompt

CONCEPTOS RELACIONADOS (Sección 1.1):
✅ Definición de Agente (Percibe → Razona → Actúa)
✅ Autonomía relativa (decide dentro de restricciones)
✅ Racionalidad acotada (mejores decisiones con info disponible)
✅ Ciclo percepto-acción (feedback loop continuo)
""")
    
    print("\n" + "✨ " * 35)
    print("¡Simulación completada!")
    print("✨ " * 35 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Simulación interrumpida por usuario")
    except Exception as e:
        print(f"\n\n❌ Error durante simulación: {e}")
        print("\nVerifica que:")
        print("  1. Ollama está corriendo: ollama serve")
        print("  2. El modelo está descargado: ollama pull mistral")
        print("  3. LangChain está instalado: pip install langchain langchain-ollama")
