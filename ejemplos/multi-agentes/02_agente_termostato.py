"""
SECCION 1.1 - EJEMPLO 02: Agente Termostato Inteligente
=========================================================

Objetivo Educativo:
    Implementar un termostato autónomo que:
    - Percibe temperatura
    - Razona sobre acciones de calefacción/refrigeración
    - Actúa para mantener rango de confort
    - Usa histéresis para evitar oscilación

Conceptos Clave:
    - Estado interno del agente
    - Histéresis: banda de histeresia para eficiencia
    - Autonomía: decide automáticamente
    - Racionalidad acotada: reglas simples pero efectivas

Usando LangChain + Ollama:
    - LLM explica sus decisiones
    - Razonamiento natural del modelo
"""

import sys
from typing import Dict, List, Any

try:
    from config_ollama import obtener_llm, MODELO_DEFECTO
except ImportError:
    print("❌ Error: No se puede importar config_ollama")
    sys.exit(1)


class TermostatoInteligente:
    """
    Termostato autónomo con razonamiento LLM.
    
    Características:
    - Histéresis: rango de confort para evitar oscilación
    - Estadísticas: monitoreo de eficiencia
    - Razonamiento transparente: LLM explica decisiones
    """
    
    def __init__(
        self,
        nombre: str,
        temperatura_objetivo: float = 20.0,
        margen_confort: float = 1.0,
        modelo: str = MODELO_DEFECTO,
    ):
        """
        Inicializa el termostato.
        
        Args:
            nombre: identificador
            temperatura_objetivo: temperatura deseada
            margen_confort: rango aceptable (±)
            modelo: modelo Ollama a usar
        """
        self.nombre = nombre
        self.objetivo = temperatura_objetivo
        self.margen = margen_confort
        self.llm = obtener_llm(modelo)
        self.modelo = modelo
        
        # Estado
        self.estado = "APAGADO"  # APAGADO, CALENTANDO, REFRIGERANDO
        self.temperatura_actual = temperatura_objetivo
        self.ciclos = 0
        
        # Histórico
        self.historico = []
        self.ciclos_calentando = 0
        self.ciclos_refrigerando = 0
        self.ciclos_mantener = 0
        
        print(f"🌡️  Termostato '{self.nombre}' inicializado")
        print(f"   Objetivo: {self.objetivo}°C")
        print(f"   Confort: ±{self.margen}°C ({self.objetivo-self.margen}°C a {self.objetivo+self.margen}°C)")
        print(f"   Modelo: {self.modelo}\n")
    
    def percibir(self, temperatura_ambiente: float) -> Dict[str, Any]:
        """PERCEPCIÓN: Lee sensores de temperatura."""
        self.temperatura_actual = temperatura_ambiente
        
        # Calcular métricas
        diferencia = temperatura_ambiente - self.objetivo
        en_rango = abs(diferencia) <= self.margen
        
        percepcion = {
            "temperatura": temperatura_ambiente,
            "objetivo": self.objetivo,
            "diferencia": diferencia,
            "en_rango": en_rango,
            "muy_frio": temperatura_ambiente < (self.objetivo - self.margen),
            "muy_calido": temperatura_ambiente > (self.objetivo + self.margen),
            "estado_actual": self.estado,
        }
        
        return percepcion
    
    def razonar_con_llm(self, percepcion: Dict[str, Any]) -> tuple:
        """
        RAZONAMIENTO: Usa LLM para explicar decisión.
        
        Returns:
            (accion, explicacion)
        """
        temp = percepcion["temperatura"]
        obj = percepcion["objetivo"]
        diff = percepcion["diferencia"]
        estado = percepcion["estado_actual"]
        
        prompt = f"""Eres un termostato autónomo inteligente.

SITUACIÓN ACTUAL:
- Temperatura ambiente: {temp}°C
- Temperatura objetivo: {obj}°C
- Diferencia: {diff:+.1f}°C
- Estado actual: {estado}
- Rango de confort: {obj-self.margen}°C a {obj+self.margen}°C

REGLAS DE DECISIÓN (histéresis):
- Si estado = APAGADO y temp < (objetivo - margen): ACTIVAR CALEFACCIÓN
- Si estado = CALENTANDO y temp > (objetivo + margen): DESACTIVAR
- Si estado = REFRIGERANDO y temp < (objetivo - margen): DESACTIVAR
- Si temp está en rango de confort: MANTENER estado actual
- Si estado = APAGADO y temp > (objetivo + margen): ACTIVAR REFRIGERACIÓN

RESPONDE COMO AGENTE AUTÓNOMO:
1. Primera línea: DECISIÓN (una palabra: CALENTAR, ENFRIAR, MANTENER)
2. Segunda línea: EXPLICACIÓN (breve, máximo 2 frases)
"""
        
        respuesta = self.llm.invoke(prompt).strip()
        lineas = respuesta.split("\n")
        
        accion = lineas[0].upper() if lineas else "MANTENER"
        explicacion = lineas[1] if len(lineas) > 1 else "Sin explicación"
        
        # Validar acciones
        acciones_validas = ["CALENTAR", "ENFRIAR", "MANTENER"]
        accion_limpia = None
        for acc in acciones_validas:
            if acc in accion:
                accion_limpia = acc
                break
        
        accion = accion_limpia or "MANTENER"
        
        return accion, explicacion
    
    def actuar(self, accion: str) -> str:
        """ACCIÓN: Ejecuta cambio de estado."""
        if accion == "CALENTAR":
            self.estado = "CALENTANDO"
            self.ciclos_calentando += 1
            resultado = "Calefacción encendida"
        
        elif accion == "ENFRIAR":
            self.estado = "REFRIGERANDO"
            self.ciclos_refrigerando += 1
            resultado = "Refrigeración encendida"
        
        elif accion == "MANTENER":
            if self.estado == "CALENTANDO":
                resultado = "Calefacción en espera"
            elif self.estado == "REFRIGERANDO":
                resultado = "Refrigeración en espera"
            else:
                resultado = "Sistema en espera"
            self.ciclos_mantener += 1
        
        return resultado
    
    def ejecutar_ciclo(self, temperatura_ambiente: float) -> Dict[str, Any]:
        """Ejecuta ciclo completo percepto-acción."""
        self.ciclos += 1
        
        # 1. PERCIBIR
        percepcion = self.percibir(temperatura_ambiente)
        
        # 2. RAZONAR
        accion, explicacion = self.razonar_con_llm(percepcion)
        
        # 3. ACTUAR
        resultado = self.actuar(accion)
        
        # 4. Registrar
        ciclo_data = {
            "ciclo": self.ciclos,
            "temperatura": temperatura_ambiente,
            "accion": accion,
            "estado": self.estado,
            "diferencia": percepcion["diferencia"],
            "en_rango": percepcion["en_rango"],
            "explicacion": explicacion,
            "resultado": resultado,
        }
        
        self.historico.append(ciclo_data)
        
        # Mostrar
        print(f"Ciclo {self.ciclos:2d}: {temperatura_ambiente:5.1f}°C → "
              f"{accion:8s} [{self.estado:11s}] - {resultado}")
        
        return ciclo_data
    
    def simular_periodo(self, temperaturas: List[float]) -> None:
        """Simula múltiples ciclos con variación de temperatura."""
        print(f"\n{'SIMULACIÓN DEL TERMOSTATO':^70}")
        print("=" * 70)
        print("Cicl  Temp     Acción   Estado       Resultado")
        print("-" * 70)
        
        for temp in temperaturas:
            self.ejecutar_ciclo(temp)
        
        print("-" * 70)
    
    def mostrar_estadisticas(self) -> None:
        """Muestra análisis de eficiencia."""
        print("\n" + "=" * 70)
        print(f"📊 ESTADÍSTICAS - {self.nombre}")
        print("=" * 70)
        
        total_ciclos = len(self.historico)
        ciclos_en_rango = sum(1 for c in self.historico if c["en_rango"])
        diferencia_promedio = sum(abs(c["diferencia"]) for c in self.historico) / total_ciclos
        
        print("\nRESUMEN:")
        print(f"  Total ciclos: {total_ciclos}")
        print(f"  Ciclos en rango: {ciclos_en_rango} ({100*ciclos_en_rango//total_ciclos}%)")
        print(f"  Diferencia promedio: {diferencia_promedio:.2f}°C")
        
        print("\nACTIVIDAD:")
        print(f"  Ciclos calentando: {self.ciclos_calentando}")
        print(f"  Ciclos refrigerando: {self.ciclos_refrigerando}")
        print(f"  Ciclos en mantener: {self.ciclos_mantener}")
        
        print("\nEFICIENCIA:")
        print(f"  Factor de utilización: {(self.ciclos_calentando + self.ciclos_refrigerando) / total_ciclos:.1%}")
        print(f"  Oscilación promedio: {diferencia_promedio:.2f}°C")
        
        if diferencia_promedio < 0.5:
            print("  ✅ Excelente estabilidad")
        elif diferencia_promedio < 1.0:
            print("  ✓ Buena estabilidad")
        else:
            print("  ⚠️  Oscilación moderada")
        
        print()


def main():
    """Simulación educativa del termostato."""
    
    print("\n" + "🎓 " * 35)
    print("EJEMPLO 1.1.2: TERMOSTATO INTELIGENTE CON LANGCHAIN + OLLAMA")
    print("🎓 " * 35 + "\n")
    
    print("""DESCRIPCIÓN:
    Termostato autónomo que usa LLM local para razonar sobre:
    - Decisiones de calefacción/refrigeración
    - Histéresis para evitar oscilación
    - Explicaciones transparentes de cada decisión
    """)
    
    # Crear termostato
    termostato = TermostatoInteligente(
        nombre="SmartThermo v1",
        temperatura_objetivo=20.0,
        margen_confort=1.0,
    )
    
    # Simular variación de temperatura a lo largo del día
    # Simulamos: mañana fría → día cálido → noche fría nuevamente
    temperaturas_simuladas = [
        # Mañana: frío
        15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 19.5,
        # Día: calor
        20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 22.5, 22.0, 21.5,
        # Tarde: normalización
        21.0, 20.5, 20.0, 19.8, 19.5,
        # Noche: frío
        19.0, 18.5, 18.0, 17.5, 17.0,
    ]
    
    print(f"Simulando {len(temperaturas_simuladas)} ciclos con variación de temperatura...\n")
    
    termostato.simular_periodo(temperaturas_simuladas)
    
    termostato.mostrar_estadisticas()
    
    # Análisis educativo
    print("\n" + "=" * 70)
    print("📚 ANÁLISIS EDUCATIVO")
    print("=" * 70)
    print("""
1. AUTONOMÍA:
   ✓ El termostato decide automáticamente
   ✓ Basado en percepción (temperatura actual)
   ✓ Sin intervención externa (salvo parámetros iniciales)

2. RACIONALIDAD ACOTADA:
   ✓ Reglas simples y locales
   ✓ Razonamiento del LLM sobre contexto
   ✓ Decisión rápida (sin búsqueda exhaustiva)

3. HISTÉRESIS (BAJA OSCILACIÓN):
   ✓ Rango de confort previene oscilación
   ✓ Cambios de estado menos frecuentes
   ✓ Mayor eficiencia energética

4. CICLO PERCEPTO-ACCIÓN:
   ✓ Percepto (temperatura)
   ✓ Razonamiento (LLM explica)
   ✓ Acción (cambio de estado)
   ✓ Retroalimentación (ciclo se repite)

5. RAZONAMIENTO NATURAL CON LLM:
   ✓ El LLM explica decisiones en lenguaje natural
   ✓ No solo ejecuta código ciego
   ✓ Puede adaptarse a reglas más complejas

COMPARACIÓN CON TERMOSTATO SIMPLE:
┌────────────────────────────────────────────┐
│ Termostato Simple                          │
│ if temp < objetivo: calentar               │
│ if temp > objetivo: enfriar                │
│ → Oscila mucho (entra/sale frecuente)     │
└────────────────────────────────────────────┘
          vs
┌────────────────────────────────────────────┐
│ Termostato Inteligente (este)             │
│ Histéresis + LLM razonamiento              │
│ → Más estable, eficiente, explicable      │
└────────────────────────────────────────────┘
""")
    
    print("\n✨ " * 35)
    print("Simulación completada")
    print("✨ " * 35 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Simulación interrumpida")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        print("\nVerifica que Ollama está corriendo:")
        print("  ollama serve")
