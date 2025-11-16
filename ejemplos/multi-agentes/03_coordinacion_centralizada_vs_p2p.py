"""
SECCION 1.2 - EJEMPLO 01: Coordinación Centralizada vs Descentralizada
========================================================================

Objetivo Educativo:
    Comparar dos arquitecturas multi-agente:
    
    1. CENTRALIZADA:
       - Un coordinador central (manager)
       - Workers envían tareas al manager
       - Manager asigna recursos
       - Ventaja: decisiones óptimas
       - Desventaja: cuello de botella
    
    2. DESCENTRALIZADA (P2P):
       - Agentes negocian directamente
       - Sin autoridad central
       - Emergencia de acuerdos
       - Ventaja: robustez, escalabilidad
       - Desventaja: complejidad

Usando LangChain + Ollama:
    - LLM decide si acepta/rechaza tareas
    - Coordinador usa LLM para elegir mejor worker
    - Workers razonan sobre carga de trabajo
"""

import sys
from typing import List
from dataclasses import dataclass
from enum import Enum

try:
    from config_ollama import obtener_llm
except ImportError:
    print("❌ Error: No se puede importar config_ollama")
    sys.exit(1)


@dataclass
class Tarea:
    """Representa una tarea en el sistema."""
    id: str
    complejidad: int  # 1-10
    tiempo_estimado: int  # segundos
    descripcion: str


class EstadoWorker(Enum):
    """Estados posibles de un worker."""
    DISPONIBLE = "DISPONIBLE"
    OCUPADO = "OCUPADO"
    SATURADO = "SATURADO"


class WorkerDescentralizado:
    """
    Worker autónomo que decide si acepta tareas.
    Razona con LLM.
    """
    
    def __init__(self, nombre: str, capacidad_maxima: int = 100):
        """
        Args:
            nombre: identificador
            capacidad_maxima: carga máxima que puede tomar
        """
        self.nombre = nombre
        self.capacidad_maxima = capacidad_maxima
        self.carga_actual = 0
        self.tareas_asignadas = []
        self.llm = obtener_llm()
    
    def calcular_estado(self) -> EstadoWorker:
        """Calcula estado basado en carga."""
        porcentaje = self.carga_actual / self.capacidad_maxima
        
        if porcentaje < 0.3:
            return EstadoWorker.DISPONIBLE
        elif porcentaje < 0.7:
            return EstadoWorker.OCUPADO
        else:
            return EstadoWorker.SATURADO
    
    def decidir_aceptar_tarea(self, tarea: Tarea) -> bool:
        """
        DESCENTRALIZADO: Worker decide autonomamente si acepta tarea.
        Usa LLM para razonar.
        """
        estado = self.calcular_estado()
        carga_nueva = self.carga_actual + tarea.complejidad
        
        prompt = f"""Eres un worker autónomo en un sistema distribuido.

INFORMACIÓN ACTUAL:
- Mi nombre: {self.nombre}
- Mi estado: {estado.value}
- Carga actual: {self.carga_actual}/{self.capacidad_maxima}
- Carga si acepto: {carga_nueva}/{self.capacidad_maxima}

TAREA PROPUESTA:
- ID: {tarea.id}
- Complejidad: {tarea.complejidad}/10
- Tiempo: {tarea.tiempo_estimado}s
- Descripción: {tarea.descripcion}

CRITERIOS DE DECISIÓN:
- Si estado es SATURADO: rechazar (demasiado ocupado)
- Si carga_nueva > capacidad_maxima: rechazar (overflow)
- Si complejidad > 7 pero yo soy especialista: aceptar
- Si estado es DISPONIBLE: aceptar (capacidad)
- Si complejidad <= 3: aceptar (rápido)

RESPONDE (solo una palabra):
- "ACEPTAR" si tomaré la tarea
- "RECHAZAR" si no puedo tomarla
"""
        
        respuesta = self.llm.invoke(prompt).strip().upper()
        decision = "ACEPTAR" in respuesta
        
        return decision
    
    def ejecutar_tarea(self, tarea: Tarea) -> None:
        """Simula ejecución de tarea."""
        self.carga_actual += tarea.complejidad
        self.tareas_asignadas.append(tarea)
        
        print(f"    ✓ {self.nombre} ejecutando: {tarea.id} "
              f"(carga: {self.carga_actual}/{self.capacidad_maxima})")
    
    def liberar_capacidad(self, cantidad: int) -> None:
        """Simula finalización de tareas."""
        self.carga_actual = max(0, self.carga_actual - cantidad)


class CoordinadorCentralizado:
    """
    ARQUITECTURA CENTRALIZADA: Un coordinador decide todo.
    """
    
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.workers = []
        self.llm = obtener_llm()
        self.tareas_procesadas = 0
    
    def registrar_worker(self, worker: WorkerDescentralizado) -> None:
        """Registra worker en el sistema centralizado."""
        self.workers.append(worker)
    
    def elegir_mejor_worker(self, tarea: Tarea) -> WorkerDescentralizado:
        """
        CENTRALIZADO: Coordinador elige el mejor worker.
        Usa LLM para razonar.
        """
        if not self.workers:
            return None
        
        # Información de workers
        info_workers = "\n".join([
            f"- {w.nombre}: carga={w.carga_actual}/{w.capacidad_maxima}, "
            f"estado={w.calcular_estado().value}"
            for w in self.workers
        ])
        
        prompt = f"""Eres un coordinador centralizado en un sistema multi-agente.

TAREA A ASIGNAR:
- ID: {tarea.id}
- Complejidad: {tarea.complejidad}
- Descripción: {tarea.descripcion}

WORKERS DISPONIBLES:
{info_workers}

ESTRATEGIA DE COORDINACIÓN:
- Elige worker con menor carga
- Considera si puede manejar complejidad
- Evita saturar un worker
- Balance de carga

RESPONDE solo el nombre del worker más adecuado:
"""
        
        respuesta = self.llm.invoke(prompt).strip()
        
        # Encontrar worker más mencionado en respuesta
        for worker in self.workers:
            if worker.nombre in respuesta:
                return worker
        
        # Fallback: worker con menor carga
        return min(self.workers, key=lambda w: w.carga_actual)
    
    def asignar_tarea(self, tarea: Tarea) -> bool:
        """Asigna tarea a mejor worker."""
        worker = self.elegir_mejor_worker(tarea)
        
        if worker and worker.carga_actual + tarea.complejidad <= worker.capacidad_maxima:
            worker.ejecutar_tarea(tarea)
            self.tareas_procesadas += 1
            return True
        else:
            print(f"    ✗ No se pudo asignar {tarea.id} (sin capacidad)")
            return False


def simulacion_centralizada(tareas: List[Tarea]) -> None:
    """Simula arquitectura centralizada."""
    print("\n" + "=" * 70)
    print("🎯 SIMULACIÓN CENTRALIZADA")
    print("=" * 70)
    print("Arquitectura: 1 Coordinador Central + 3 Workers")
    print("Estrategia: El coordinador decide TODO\n")
    
    # Crear sistema centralizado
    coordinador = CoordinadorCentralizado("Coordinador-Central")
    
    workers = [
        WorkerDescentralizado("Worker-A", capacidad_maxima=100),
        WorkerDescentralizado("Worker-B", capacidad_maxima=100),
        WorkerDescentralizado("Worker-C", capacidad_maxima=100),
    ]
    
    for w in workers:
        coordinador.registrar_worker(w)
    
    # Asignar tareas
    print(f"{'Tarea':<10} {'Complj':<6} {'Asignado a':<15}")
    print("-" * 70)
    
    for tarea in tareas:
        # El coordinador decide
        worker = coordinador.elegir_mejor_worker(tarea)
        puede_asignar = (worker and 
                        worker.carga_actual + tarea.complejidad <= worker.capacidad_maxima)
        
        if puede_asignar:
            worker.ejecutar_tarea(tarea)
            print(f"{tarea.id:<10} {tarea.complejidad:<6} {worker.nombre:<15} ✓")
        else:
            print(f"{tarea.id:<10} {tarea.complejidad:<6} {'(Rechazada)':<15} ✗")
    
    # Estadísticas
    print("\n" + "-" * 70)
    print("ESTADÍSTICAS CENTRALIZADO:")
    for w in workers:
        print(f"  {w.nombre}: {w.carga_actual}/{w.capacidad_maxima} "
              f"({100*w.carga_actual//w.capacidad_maxima}%)")
    print(f"  Tareas procesadas: {coordinador.tareas_procesadas}/{len(tareas)}")


def simulacion_descentralizada(tareas: List[Tarea]) -> None:
    """Simula arquitectura descentralizada (P2P)."""
    print("\n" + "=" * 70)
    print("🌐 SIMULACIÓN DESCENTRALIZADA (P2P)")
    print("=" * 70)
    print("Arquitectura: 3 Workers autónomos (sin coordinador)")
    print("Estrategia: Cada worker decide si acepta\n")
    
    # Crear workers descentralizados
    workers = [
        WorkerDescentralizado("Worker-X", capacidad_maxima=100),
        WorkerDescentralizado("Worker-Y", capacidad_maxima=100),
        WorkerDescentralizado("Worker-Z", capacidad_maxima=100),
    ]
    
    tareas_asignadas = 0
    
    print(f"{'Tarea':<10} {'Complj':<6} {'Decisión':<15} {'Worker':<12}")
    print("-" * 70)
    
    for tarea in tareas:
        # Cada worker decide autónomamente
        asignada = False
        
        for worker in workers:
            # Worker razona si acepta
            acepta = worker.decidir_aceptar_tarea(tarea)
            
            if acepta and (worker.carga_actual + tarea.complejidad <= worker.capacidad_maxima):
                worker.ejecutar_tarea(tarea)
                print(f"{tarea.id:<10} {tarea.complejidad:<6} {'ACEPTO':<15} {worker.nombre:<12} ✓")
                asignada = True
                tareas_asignadas += 1
                break
        
        if not asignada:
            print(f"{tarea.id:<10} {tarea.complejidad:<6} {'TODOS RECHAZARON':<15} {'-':<12} ✗")
    
    # Estadísticas
    print("\n" + "-" * 70)
    print("ESTADÍSTICAS DESCENTRALIZADO:")
    for w in workers:
        print(f"  {w.nombre}: {w.carga_actual}/{w.capacidad_maxima} "
              f"({100*w.carga_actual//w.capacidad_maxima}%)")
    print(f"  Tareas procesadas: {tareas_asignadas}/{len(tareas)}")


def main():
    """Comparativa educativa entre arquitecturas."""
    
    print("\n" + "🎓 " * 35)
    print("EJEMPLO 1.2.1: CENTRALIZADO vs DESCENTRALIZADO")
    print("🎓 " * 35 + "\n")
    
    print("""DESCRIPCIÓN:
    Compara dos formas de coordinación multi-agente:
    
    A) CENTRALIZADA: Un coordinador maestro decide TODO
       - Ventaja: Decisiones globales óptimas
       - Desventaja: Punto único de fallo, cuello de botella
       - Caso de uso: Sistemas críticos con pocas tareas
    
    B) DESCENTRALIZADA (P2P): Agentes deciden autónomamente
       - Ventaja: Robustez, escalabilidad, autonomía
       - Desventaja: Posibles decisiones subóptimas, complejidad
       - Caso de uso: Sistemas grandes, dinámicos
    """)
    
    # Crear tareas de prueba
    tareas = [
        Tarea("T1", complejidad=3, tiempo_estimado=5, descripcion="Procesar datos"),
        Tarea("T2", complejidad=5, tiempo_estimado=10, descripcion="Análisis complejo"),
        Tarea("T3", complejidad=2, tiempo_estimado=3, descripcion="Validar entrada"),
        Tarea("T4", complejidad=7, tiempo_estimado=15, descripcion="ML training"),
        Tarea("T5", complejidad=4, tiempo_estimado=8, descripcion="Integración"),
        Tarea("T6", complejidad=6, tiempo_estimado=12, descripcion="Reportes"),
        Tarea("T7", complejidad=3, tiempo_estimado=5, descripcion="Backup"),
        Tarea("T8", complejidad=5, tiempo_estimado=10, descripcion="Sincronización"),
    ]
    
    print(f"Tareas de entrada: {len(tareas)}")
    print(f"Carga total: {sum(t.complejidad for t in tareas)}\n")
    
    # Simulaciones
    simulacion_centralizada(tareas)
    simulacion_descentralizada(tareas)
    
    # Análisis comparativo
    print("\n" + "=" * 70)
    print("📊 ANÁLISIS COMPARATIVO")
    print("=" * 70)
    print("""
CENTRALIZADO:
✓ Decisión única y consistente
✓ Optimización global posible
✓ Auditoría fácil (una fuente de verdad)
✗ Cuello de botella: coordinador sobrecargado
✗ Falla crítica si coordinador cae
✗ Comunicación constante hacia coordinador

DESCENTRALIZADO:
✓ Robustez: sin punto único de fallo
✓ Escalabilidad: agrega workers sin límite
✓ Autonomía: cada agente decide
✓ Resilencia: continúa si algunos fallan
✗ Suboptimalidad: decisiones locales ≠ globales
✗ Debugging: comportamiento emergente complejo
✗ Consistencia: acuerdos posibles

CUÁNDO USAR CADA UNO:
┌─────────────────────────────────────────────┐
│ CENTRALIZADO es mejor cuando:               │
│  • Pocas tareas                            │
│  • Optimización crítica                    │
│  • Control estricto necesario              │
│  • Arquitectura simple importante          │
│  Ejemplo: Sistema de misión crítica        │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ DESCENTRALIZADO es mejor cuando:            │
│  • Muchas tareas heterogéneas              │
│  • Alta disponibilidad requerida           │
│  • Escalabilidad horizontal                │
│  • Dinamismo: agentes entran/salen        │
│  Ejemplo: Sistema de cloud computing      │
└─────────────────────────────────────────────┘
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
        print("\nVerifica que Ollama está corriendo")
