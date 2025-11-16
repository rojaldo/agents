"""
SECCION 1.3 - EJEMPLO 01: Cooperación vs Colaboración
======================================================

Objetivo Educativo:
    Demostrar la diferencia entre:
    
    1. COOPERACIÓN (Implícita):
       - Agentes siguen reglas simples locales
       - Sin comunicación explícita
       - Comportamiento coordinado emerge
       - Ejemplo: Peces en cardumen
    
    2. COLABORACIÓN (Explícita):
       - Agentes comunican activamente
       - Negocian acuerdos
       - Plan común coordinado
       - Ejemplo: Equipo de desarrollo

Usando LangChain + Ollama:
    - COOPERACIÓN: Agentes siguen reglas, LLM valida
    - COLABORACIÓN: Agentes intercambian mensajes con LLM
"""

import sys
from typing import List, Tuple
from dataclasses import dataclass
from enum import Enum

try:
    from config_ollama import obtener_llm
except ImportError:
    print("❌ Error: No se puede importar config_ollama")
    sys.exit(1)


@dataclass
class Posicion:
    """Coordenada 2D."""
    x: float
    y: float
    
    def distancia_a(self, otra: 'Posicion') -> float:
        """Calcula distancia euclidiana."""
        return ((self.x - otra.x)**2 + (self.y - otra.y)**2)**0.5
    
    def __repr__(self) -> str:
        return f"({self.x:.1f},{self.y:.1f})"


class TipoAgente(Enum):
    """Tipos de agentes."""
    DEPREDADOR = "🦅 Depredador"
    PRESA = "🐟 Presa"


# ============================================================================
# COOPERACIÓN: Comportamiento Emergente (Implícito)
# ============================================================================

class CardumenPeces:
    """
    Cardumen de peces cooperativo.
    
    COOPERACIÓN IMPLÍCITA: Cada pez sigue 3 reglas simples:
    1. Mantener distancia mínima (no chocar)
    2. Moverse hacia centro de vecinos (cohesión)
    3. Alinearse con dirección promedio (alineación)
    
    Resultado: Movimiento coordinado perfecto SIN comunicación
    """
    
    def __init__(self, nombre: str, cantidad: int = 10, radio_vecindad: float = 3.0):
        self.nombre = nombre
        self.radio_vecindad = radio_vecindad
        self.llm = obtener_llm()
        
        # Crear peces en posiciones aleatorias
        import random
        random.seed(42)  # Para reproducibilidad
        
        self.peces = []
        for i in range(cantidad):
            self.peces.append({
                "id": i,
                "pos": Posicion(random.uniform(0, 10), random.uniform(0, 10)),
                "vel": (random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)),
            })
        
        self.ciclo = 0
    
    def obtener_vecinos(self, pez_id: int) -> List[dict]:
        """Obtiene peces cercanos (dentro de radio_vecindad)."""
        vecinos = []
        pez = self.peces[pez_id]
        
        for otro in self.peces:
            if otro["id"] != pez_id:
                dist = pez["pos"].distancia_a(otro["pos"])
                if dist < self.radio_vecindad:
                    vecinos.append(otro)
        
        return vecinos
    
    def regla_1_separacion(self, pez_id: int) -> Tuple[float, float]:
        """Mantener distancia mínima (no chocar)."""
        pez = self.peces[pez_id]
        vecinos = self.obtener_vecinos(pez_id)
        
        dx, dy = 0, 0
        for vecino in vecinos:
            diff_x = pez["pos"].x - vecino["pos"].x
            diff_y = pez["pos"].y - vecino["pos"].y
            dist = pez["pos"].distancia_a(vecino["pos"])
            
            if dist > 0.1:
                dx += (diff_x / dist) * 0.2
                dy += (diff_y / dist) * 0.2
        
        return dx, dy
    
    def regla_2_alineacion(self, pez_id: int) -> Tuple[float, float]:
        """Alinearse con dirección promedio de vecinos."""
        vecinos = self.obtener_vecinos(pez_id)
        
        if not vecinos:
            return 0, 0
        
        vel_x = sum(v["vel"][0] for v in vecinos) / len(vecinos)
        vel_y = sum(v["vel"][1] for v in vecinos) / len(vecinos)
        
        pez = self.peces[pez_id]
        return (vel_x - pez["vel"][0]) * 0.01, (vel_y - pez["vel"][1]) * 0.01
    
    def regla_3_cohesion(self, pez_id: int) -> Tuple[float, float]:
        """Moverse hacia centro de masa de vecinos."""
        pez = self.peces[pez_id]
        vecinos = self.obtener_vecinos(pez_id)
        
        if not vecinos:
            return 0, 0
        
        centro_x = sum(v["pos"].x for v in vecinos) / len(vecinos)
        centro_y = sum(v["pos"].y for v in vecinos) / len(vecinos)
        
        return (centro_x - pez["pos"].x) * 0.01, (centro_y - pez["pos"].y) * 0.01
    
    def iterar(self) -> None:
        """Un ciclo de simulación."""
        self.ciclo += 1
        
        # Aplicar reglas a cada pez
        for pez in self.peces:
            # Aplicar 3 reglas (COOPERACIÓN IMPLÍCITA)
            sep = self.regla_1_separacion(pez["id"])
            ali = self.regla_2_alineacion(pez["id"])
            coh = self.regla_3_cohesion(pez["id"])
            
            # Combinar fuerzas
            vel_x = pez["vel"][0] + sep[0] + ali[0] + coh[0]
            vel_y = pez["vel"][1] + sep[1] + ali[1] + coh[1]
            
            # Limitar velocidad máxima
            import math
            vel_mag = math.sqrt(vel_x**2 + vel_y**2)
            if vel_mag > 0.5:
                vel_x = (vel_x / vel_mag) * 0.5
                vel_y = (vel_y / vel_mag) * 0.5
            
            pez["vel"] = (vel_x, vel_y)
            
            # Actualizar posición (con wrapping)
            pez["pos"].x = (pez["pos"].x + vel_x) % 10
            pez["pos"].y = (pez["pos"].y + vel_y) % 10
    
    def mostrar_estado(self) -> None:
        """Visualiza estado del cardumen."""
        # Crear grid visual
        grid = [['.' for _ in range(20)] for _ in range(10)]
        
        for pez in self.peces:
            x = int(pez["pos"].x * 2)
            y = int(pez["pos"].y)
            if 0 <= x < 20 and 0 <= y < 10:
                grid[9-y][x] = '*'
        
        print(f"\nCiclo {self.ciclo:3d}:")
        for fila in grid:
            print(''.join(fila))
    
    def analizar_coordinacion(self) -> dict:
        """Calcula métricas de coordinación."""
        # Distancia promedio
        distancias = []
        for i, pez in enumerate(self.peces):
            vecinos = self.obtener_vecinos(i)
            for vecino in vecinos:
                dist = pez["pos"].distancia_a(vecino["pos"])
                distancias.append(dist)
        
        distancia_prom = sum(distancias) / len(distancias) if distancias else 0
        
        # Velocidades promedio
        vel_x_prom = sum(abs(p["vel"][0]) for p in self.peces) / len(self.peces)
        vel_y_prom = sum(abs(p["vel"][1]) for p in self.peces) / len(self.peces)
        
        return {
            "distancia_promedio": distancia_prom,
            "velocidad_promedio": (vel_x_prom + vel_y_prom) / 2,
            "cohesion": 1 - min(distancia_prom / self.radio_vecindad, 1),  # 0-1
        }


# ============================================================================
# COLABORACIÓN: Negociación Explícita
# ============================================================================

class Especialista:
    """
    Especialista que colabora explícitamente con otros.
    
    COLABORACIÓN EXPLÍCITA: Agentes comunican y negocian.
    """
    
    def __init__(self, nombre: str, especialidad: str, experiencia: int = 5):
        self.nombre = nombre
        self.especialidad = especialidad  # "diseño", "backend", "frontend"
        self.experiencia = experiencia
        self.tareas_asignadas = []
        self.llm = obtener_llm()
    
    def proponer_solucion(self, problema: str) -> str:
        """Propone solución basada en especialidad."""
        prompt = f"""Eres un especialista en {self.especialidad}.
Experiencia: {self.experiencia} años
Propón una solución breve (máximo 1 línea) para:

{problema}

Incluye por qué tu especialidad es relevante."""
        
        return self.llm.invoke(prompt).strip()
    
    def evaluar_propuesta_otros(self, propuesta: str) -> Tuple[bool, str]:
        """Evalúa propuesta de otro especialista."""
        prompt = f"""Eres un especialista en {self.especialidad}.

Evalúa esta propuesta desde tu perspectiva:
"{propuesta}"

RESPONDE:
1. Primera línea: APRUEBO o RECHAZO
2. Explicación: Por qué (máximo 1 frase)"""
        
        respuesta = self.llm.invoke(prompt).strip().split("\n")
        aprobacion = "APRUEBO" in respuesta[0].upper()
        explicacion = respuesta[1] if len(respuesta) > 1 else ""
        
        return aprobacion, explicacion


class EquipoColaborativo:
    """
    Equipo colaborativo que negocia soluciones.
    """
    
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.especialistas = []
        self.decisiones_tomadas = []
    
    def agregar_especialista(self, especialista: Especialista) -> None:
        """Agrega especialista al equipo."""
        self.especialistas.append(especialista)
    
    def resolver_problema_colaborativo(self, problema: str) -> dict:
        """
        Proceso COLABORATIVO:
        1. Cada especialista propone
        2. Equipo evalúa todas
        3. Consenso de aceptación
        """
        print(f"\n📋 PROBLEMA: {problema}")
        print("-" * 70)
        
        propuestas = {}
        
        # Fase 1: Cada uno propone
        print("\n1️⃣  PROPUESTAS INICIALES:")
        for esp in self.especialistas:
            prop = esp.proponer_solucion(problema)
            propuestas[esp.nombre] = prop
            print(f"   {esp.nombre} ({esp.especialidad}): {prop}")
        
        # Fase 2: Evaluación cruzada
        print("\n2️⃣  EVALUACIÓN COLABORATIVA:")
        evaluaciones = {}
        
        for nombre_prop, propuesta in propuestas.items():
            evaluaciones[nombre_prop] = {"aprobaciones": 0, "comentarios": []}
            
            for esp in self.especialistas:
                if esp.nombre != nombre_prop:
                    aprobacion, comentario = esp.evaluar_propuesta_otros(propuesta)
                    if aprobacion:
                        evaluaciones[nombre_prop]["aprobaciones"] += 1
                        print(f"   ✓ {esp.nombre} aprueba propuesta de {nombre_prop}")
                    else:
                        print(f"   ✗ {esp.nombre} rechaza propuesta de {nombre_prop}")
                    
                    if comentario:
                        evaluaciones[nombre_prop]["comentarios"].append(comentario)
        
        # Fase 3: Consenso
        print("\n3️⃣  CONSENSO:")
        mejor_propuesta = max(
            evaluaciones.items(),
            key=lambda x: x[1]["aprobaciones"]
        )
        
        print(f"   ✅ DECISIÓN: {mejor_propuesta[0]}")
        print(f"   Aprobaciones: {mejor_propuesta[1]['aprobaciones']}/{len(self.especialistas)-1}")
        
        resultado = {
            "propuesta_ganadora": mejor_propuesta[0],
            "aprobaciones": mejor_propuesta[1]["aprobaciones"],
            "todas_propuestas": propuestas,
        }
        
        self.decisiones_tomadas.append(resultado)
        return resultado


def main():
    """Simulación educativa de Cooperación vs Colaboración."""
    
    print("\n" + "🎓 " * 35)
    print("EJEMPLO 1.3.1: COOPERACIÓN vs COLABORACIÓN")
    print("🎓 " * 35 + "\n")
    
    print("""DESCRIPCIÓN:
    Compara dos modelos de coordinación:
    
    A) COOPERACIÓN (Implícita):
       - Agentes siguen reglas locales simples
       - Sin comunicación entre agentes
       - Coordinación EMERGE globalmente
       - Ejemplo: Cardumen de peces, hormigas
    
    B) COLABORACIÓN (Explícita):
       - Agentes comunican activamente
       - Negocian y llegan a acuerdos
       - Coordinación PLANIFICADA
       - Ejemplo: Equipo de proyecto
    """)
    
    # =====================================================================
    # PARTE 1: COOPERACIÓN
    # =====================================================================
    
    print("\n" + "=" * 70)
    print("🐟 PARTE 1: COOPERACIÓN IMPLÍCITA - CARDUMEN DE PECES")
    print("=" * 70)
    print("""
    3 REGLAS LOCALES (cada pez sigue):
    1. SEPARACIÓN: Mantener distancia de vecinos
    2. ALINEACIÓN: Moverse en dirección promedio
    3. COHESIÓN: Ir hacia centro de masa
    
    RESULTADO: Movimiento coordinado emerge SIN comunicación
    """)
    
    cardumen = CardumenPeces("Cardumen-1", cantidad=15)
    
    print("Iterando simulación (10 ciclos):\n")
    for _ in range(10):
        cardumen.iterar()
        if cardumen.ciclo % 2 == 0:
            cardumen.mostrar_estado()
    
    # Análisis de coordinación
    metricas = cardumen.analizar_coordinacion()
    print("\n" + "-" * 70)
    print("📊 MÉTRICAS DE COORDINACIÓN EMERGENTE:")
    print(f"   Distancia promedio: {metricas['distancia_promedio']:.2f}")
    print(f"   Cohesión: {metricas['cohesion']:.2%}")
    print(f"   Velocidad promedio: {metricas['velocidad_promedio']:.3f}")
    print("""
    OBSERVACIONES:
    ✓ Los peces se coordinan perfectamente sin comunicarse
    ✓ Comportamiento emergente es robusto
    ✓ Sistema escala bien (funciona con miles de peces)
    """)
    
    # =====================================================================
    # PARTE 2: COLABORACIÓN
    # =====================================================================
    
    print("\n" + "=" * 70)
    print("👥 PARTE 2: COLABORACIÓN EXPLÍCITA - EQUIPO DE PROYECTO")
    print("=" * 70)
    print("""
    PROCESO COLABORATIVO:
    1. Cada especialista propone solución
    2. Todos evalúan todas las propuestas
    3. Consenso selecciona mejor opción
    """)
    
    equipo = EquipoColaborativo("Equipo-Dev")
    
    # Crear especialistas
    especialistas = [
        Especialista("Alice", "diseño", experiencia=7),
        Especialista("Bob", "backend", experiencia=8),
        Especialista("Charlie", "frontend", experiencia=5),
    ]
    
    for esp in especialistas:
        equipo.agregar_especialista(esp)
    
    # Resolver problemas colaborativamente
    problemas = [
        "¿Cómo mejorar velocidad de carga de la web?",
        "¿Qué arquitectura es mejor para escalar?",
    ]
    
    for problema in problemas:
        equipo.resolver_problema_colaborativo(problema)
    
    # Análisis de colaboración
    print("\n" + "=" * 70)
    print("📊 ANÁLISIS DE COLABORACIÓN")
    print("=" * 70)
    print(f"""
    Problemas resueltos: {len(equipo.decisiones_tomadas)}
    
    VENTAJAS DE COLABORACIÓN:
    ✓ Decisiones bien fundamentadas (consenso)
    ✓ Conocimiento colectivo
    ✓ Responsabilidad compartida
    ✓ Auditable y transparente
    
    DESVENTAJAS:
    ✗ Más lento (requiere comunicación)
    ✗ Overhead de coordinación
    ✗ Puntos de desacuerdo
    """)
    
    # =====================================================================
    # COMPARACIÓN FINAL
    # =====================================================================
    
    print("\n" + "=" * 70)
    print("🔄 COMPARATIVA: COOPERACIÓN vs COLABORACIÓN")
    print("=" * 70)
    print("""
┌──────────────────────────────────────────────────────────────┐
│                      COOPERACIÓN                            │
├──────────────────────────────────────────────────────────────┤
│ Comunicación: MÍNIMA                                         │
│ Coordinación: EMERGENTE (local rules → global behavior)    │
│ Velocidad: RÁPIDA                                          │
│ Escalabilidad: EXCELENTE (1000+ agentes)                   │
│ Robustez: ALTA (sin punto único de fallo)                  │
│ Ejemplo: Colonias de hormigas, cardúmenes                  │
│                                                              │
│ ✓ Funciona con agentes simples                            │
│ ✗ Impredecibilidad (emerge, no se programa)               │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                     COLABORACIÓN                            │
├──────────────────────────────────────────────────────────────┤
│ Comunicación: ACTIVA                                         │
│ Coordinación: PLANIFICADA (acuerdos explícitos)            │
│ Velocidad: LENTA (mucha negociación)                       │
│ Escalabilidad: MODERADA (10-100 agentes)                   │
│ Robustez: MEDIA (depende de acuerdos)                      │
│ Ejemplo: Equipos humanos, empresas                          │
│                                                              │
│ ✓ Previsible y auditrable                                 │
│ ✗ Más lento, más overhead                                 │
└──────────────────────────────────────────────────────────────┘

CUÁNDO USAR CADA UNO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COOPERACIÓN es mejor para:
• Sistemas con muchos agentes simples
• Entornos dinámicos (agentes entran/salen)
• Máxima resilencia requerida
• Decisiones locales viables

COLABORACIÓN es mejor para:
• Sistemas con pocos agentes complejos
• Decisiones críticas que requieren consenso
• Requisitos de auditoria/trazabilidad
• Control y previsibilidad importantes
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
        import traceback
        traceback.print_exc()
