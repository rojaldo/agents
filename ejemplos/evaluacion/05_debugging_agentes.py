"""
MÓDULO 5: Debugging de Agentes
===============================

Este módulo demuestra técnicas de debugging para agentes.

Conceptos clave:
- Logging estratégico (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Trazas de ejecución
- Inspección de estado
- Replay de ejecuciones
- Profiling (qué funciones tardan más)
- Post-mortem analysis

Ejemplo práctico: Debuggear un agente con comportamiento inesperado
"""

import logging
import time
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import traceback


# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

def configurar_logging(nivel: str = "DEBUG") -> logging.Logger:
    """Configura logging con nivel específico"""

    logger = logging.getLogger("AgentDebug")
    logger.setLevel(getattr(logging, nivel))

    # Handler para consola
    handler = logging.StreamHandler()
    handler.setLevel(getattr(logging, nivel))

    # Formato detallado
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


# ============================================================================
# TIPOS Y ESTRUCTURAS
# ============================================================================

@dataclass
class EventoEjecucion:
    """Registra un evento en ejecución del agente"""
    timestamp: float
    tipo: str  # 'entrada', 'salida', 'decision', 'error'
    funcion: str
    mensaje: str
    variables: Dict[str, Any] = None
    nivel: str = "INFO"

    def a_dict(self) -> Dict:
        return asdict(self)


@dataclass
class SnapshotEstado:
    """Captura estado del agente en un punto específico"""
    timestamp: float
    paso: int
    creencias: Dict[str, Any]
    objetivos: List[str]
    ultima_accion: Optional[str]
    historico_reciente: List[str]


# ============================================================================
# AGENTE CON CAPACIDADES DE DEBUG
# ============================================================================

class AgenteDebugeable:
    """Agente con capacidades de logging y debugging"""

    def __init__(self, nombre: str, debug: bool = True):
        self.nombre = nombre
        self.debug = debug
        self.logger = configurar_logging("DEBUG" if debug else "INFO")

        # Estado del agente
        self.creencias = {}
        self.objetivos = []
        self.ultima_accion = None
        self.historial_acciones = []
        self.contador_pasos = 0

        # Para debugging
        self.eventos_ejecucion: List[EventoEjecucion] = []
        self.snapshots_estado: List[SnapshotEstado] = []

    def log(self, nivel: str, mensaje: str, **variables):
        """Registra evento de logging"""
        getattr(self.logger, nivel.lower())(f"[{self.nombre}] {mensaje}")

        # Guardar para replay
        evento = EventoEjecucion(
            timestamp=time.time(),
            tipo=nivel.lower(),
            funcion="log",
            mensaje=mensaje,
            variables=variables if variables else None,
            nivel=nivel
        )
        self.eventos_ejecucion.append(evento)

    def percibir(self, entorno_estado: Dict[str, Any]) -> Dict[str, Any]:
        """Percibe el entorno"""
        self.log("DEBUG", f"Percibiendo... estado entorno: {entorno_estado}")

        # Actualizar creencias
        self.creencias.update(entorno_estado)
        self.log("DEBUG", f"Creencias actualizadas: {self.creencias}")

        return self.creencias

    def decidir(self, percepts: Dict[str, Any]) -> str:
        """Decide qué acción tomar"""
        self.log("DEBUG", f"Decidiendo basado en percepts: {percepts}")

        self.contador_pasos += 1

        # Lógica de decisión
        if percepts.get("amenaza"):
            self.log("WARNING", "¡Amenaza detectada!")
            accion = "huir"
        elif percepts.get("oportunidad"):
            self.log("INFO", "Oportunidad encontrada")
            accion = "avanzar"
        else:
            self.log("DEBUG", "Sin estimulos especiales, accion neutral")
            accion = "esperar"

        self.log("INFO", f"Acción decidida: {accion}")
        return accion

    def actuar(self, accion: str) -> bool:
        """Ejecuta la acción"""
        self.log("DEBUG", f"Ejecutando acción: {accion}")

        try:
            # Simular ejecución
            if accion == "huir":
                self.log("INFO", "Huyendo...")
                exito = True
            elif accion == "avanzar":
                self.log("INFO", "Avanzando...")
                exito = True
            else:
                self.log("DEBUG", "Esperando...")
                exito = True

            self.ultima_accion = accion
            self.historial_acciones.append(accion)
            self.log("DEBUG", f"Acción ejecutada exitosamente")

            return exito

        except Exception as e:
            self.log("ERROR", f"Error ejecutando acción: {str(e)}")
            return False

    def capturar_snapshot_estado(self) -> SnapshotEstado:
        """Captura snapshot del estado actual"""
        snapshot = SnapshotEstado(
            timestamp=time.time(),
            paso=self.contador_pasos,
            creencias=self.creencias.copy(),
            objetivos=self.objetivos.copy(),
            ultima_accion=self.ultima_accion,
            historico_reciente=self.historial_acciones[-5:] if self.historial_acciones else []
        )
        self.snapshots_estado.append(snapshot)
        return snapshot

    def imprimir_estado_actual(self):
        """Imprime estado actual para debugging"""
        print(f"\n{'='*60}")
        print(f"ESTADO DEL AGENTE: {self.nombre}")
        print(f"{'='*60}")
        print(f"Paso: {self.contador_pasos}")
        print(f"Creencias: {self.creencias}")
        print(f"Objetivos: {self.objetivos}")
        print(f"Última acción: {self.ultima_accion}")
        print(f"Últimas {min(5, len(self.historial_acciones))} acciones: {self.historial_acciones[-5:]}")
        print(f"{'='*60}\n")

    def generar_reporte_debug(self) -> Dict[str, Any]:
        """Genera reporte de debugging"""
        return {
            "nombre_agente": self.nombre,
            "pasos_totales": self.contador_pasos,
            "total_eventos": len(self.eventos_ejecucion),
            "total_snapshots": len(self.snapshots_estado),
            "acciones_ejecutadas": len(self.historial_acciones),
            "estado_actual": {
                "creencias": self.creencias,
                "objetivos": self.objetivos,
                "ultima_accion": self.ultima_accion
            }
        }


# ============================================================================
# PROFILING
# ============================================================================

class Profiler:
    """Profiler simple para medir performance de funciones"""

    def __init__(self):
        self.medidas: Dict[str, List[float]] = {}

    def registrar_tiempo(self, funcion_nombre: str, tiempo_ms: float):
        """Registra tiempo de ejecución"""
        if funcion_nombre not in self.medidas:
            self.medidas[funcion_nombre] = []
        self.medidas[funcion_nombre].append(tiempo_ms)

    def obtener_estadisticas(self) -> Dict[str, Dict[str, float]]:
        """Obtiene estadísticas de tiempo"""
        stats = {}
        for funcion, tiempos in self.medidas.items():
            stats[funcion] = {
                "total_ms": sum(tiempos),
                "promedio_ms": sum(tiempos) / len(tiempos) if tiempos else 0,
                "min_ms": min(tiempos) if tiempos else 0,
                "max_ms": max(tiempos) if tiempos else 0,
                "llamadas": len(tiempos)
            }
        return stats

    def imprimir_reporte(self):
        """Imprime reporte de profiling"""
        print("\n" + "=" * 80)
        print("REPORTE DE PROFILING")
        print("=" * 80)

        stats = self.obtener_estadisticas()

        # Ordenar por tiempo total descendente
        ordenado = sorted(stats.items(), key=lambda x: x[1]["total_ms"], reverse=True)

        print(f"{'Función':<30} {'Total (ms)':<12} {'Promedio':<12} {'Llamadas':<10}")
        print("-" * 80)

        for funcion, datos in ordenado:
            print(f"{funcion:<30} {datos['total_ms']:<12.2f} {datos['promedio_ms']:<12.2f} {datos['llamadas']:<10}")


# ============================================================================
# REPRODUCTOR DE EJECUCIÓN
# ============================================================================

class ReproductorEjecucion:
    """Reproduce ejecuciones del agente para debugging"""

    def __init__(self, agente: AgenteDebugeable):
        self.agente = agente

    def reproducir_hasta_paso(self, paso_objetivo: int):
        """Reproduce ejecución hasta paso específico"""
        print(f"\n{'='*80}")
        print(f"REPRODUCIENDO EJECUCIÓN HASTA PASO {paso_objetivo}")
        print(f"{'='*80}")

        snapshots_relevantes = [s for s in self.agente.snapshots_estado if s.paso <= paso_objetivo]

        if not snapshots_relevantes:
            print("No hay snapshots para reproducir")
            return

        ultimo_snapshot = snapshots_relevantes[-1]

        print(f"\nSnapshot en paso {ultimo_snapshot.paso}:")
        print(f"  Creencias: {ultimo_snapshot.creencias}")
        print(f"  Objetivos: {ultimo_snapshot.objetivos}")
        print(f"  Última acción: {ultimo_snapshot.ultima_accion}")
        print(f"  Historial reciente: {ultimo_snapshot.historico_reciente}")

    def analizar_evento_error(self, indice_evento: int = None):
        """Analiza evento de error"""
        eventos_error = [e for e in self.agente.eventos_ejecucion if e.nivel == "ERROR"]

        if not eventos_error:
            print("No hay eventos de error para analizar")
            return

        if indice_evento is None:
            evento = eventos_error[-1]  # Último error
        else:
            evento = eventos_error[indice_evento] if indice_evento < len(eventos_error) else eventos_error[-1]

        print(f"\n{'='*80}")
        print(f"ANÁLISIS DE ERROR")
        print(f"{'='*80}")
        print(f"Timestamp: {datetime.fromtimestamp(evento.timestamp)}")
        print(f"Función: {evento.funcion}")
        print(f"Mensaje: {evento.mensaje}")
        print(f"Variables: {evento.variables}")

        # Buscar eventos previos
        idx = self.agente.eventos_ejecucion.index(evento)
        eventos_previos = self.agente.eventos_ejecucion[max(0, idx-5):idx]

        print(f"\nÚltimos 5 eventos previos:")
        for e in eventos_previos:
            print(f"  - [{e.nivel}] {e.mensaje}")


# ============================================================================
# DEMOSTRACIÓN
# ============================================================================

def demo_debugging():
    """Demuestra debugging de agentes"""

    print("=" * 80)
    print("DEBUGGING DE AGENTES - TÉCNICAS Y HERRAMIENTAS")
    print("=" * 80)

    # Crear agente
    agente = AgenteDebugeable("AgenteDemostracion", debug=True)

    # Simular ejecución
    print("\n1. EJECUCIÓN CON LOGGING")
    print("-" * 80)

    profiler = Profiler()

    # Paso 1
    inicio = time.time()
    percepts = agente.percibir({"amenaza": False, "oportunidad": True})
    tiempo1 = (time.time() - inicio) * 1000
    profiler.registrar_tiempo("percibir", tiempo1)

    agente.capturar_snapshot_estado()

    # Paso 2
    inicio = time.time()
    accion = agente.decidir(percepts)
    tiempo2 = (time.time() - inicio) * 1000
    profiler.registrar_tiempo("decidir", tiempo2)

    # Paso 3
    inicio = time.time()
    exito = agente.actuar(accion)
    tiempo3 = (time.time() - inicio) * 1000
    profiler.registrar_tiempo("actuar", tiempo3)

    agente.capturar_snapshot_estado()

    print("\n✓ Ejecución completada")

    # Inspección de estado
    print("\n2. INSPECCIÓN DE ESTADO")
    print("-" * 80)

    agente.imprimir_estado_actual()

    # Profiling
    print("\n3. PROFILING")
    print("-" * 80)

    profiler.imprimir_reporte()

    # Reporte de debugging
    print("\n4. REPORTE DE DEBUGGING")
    print("-" * 80)

    reporte = agente.generar_reporte_debug()
    print(f"\nReporte de debugging:")
    print(json.dumps(reporte, indent=2))

    # Reproductor de ejecución
    print("\n5. REPRODUCTOR DE EJECUCIÓN")
    print("-" * 80)

    reproductor = ReproductorEjecucion(agente)
    reproductor.reproducir_hasta_paso(1)

    # Análisis de eventos
    print("\n6. ANÁLISIS DE EVENTOS")
    print("-" * 80)

    print(f"Total eventos registrados: {len(agente.eventos_ejecucion)}")
    print(f"Total snapshots: {len(agente.snapshots_estado)}")

    print("\nPrimeros 5 eventos:")
    for evento in agente.eventos_ejecucion[:5]:
        print(f"  [{evento.nivel}] {evento.mensaje}")

    # Resumen
    print("\n" + "=" * 80)
    print("RESUMEN DE HERRAMIENTAS DE DEBUGGING")
    print("=" * 80)
    print(f"""
✓ Logging estratégico (DEBUG, INFO, WARNING, ERROR)
✓ Captura de snapshots de estado
✓ Reproducción de ejecuciones
✓ Profiling de performance
✓ Análisis de eventos y errores
✓ Reporte de debugging

MEJORES PRÁCTICAS:
1. Log en puntos críticos (entrada/salida de funciones)
2. Captura estado regularmente
3. Registra timestamps para timeline reconstruction
4. Perfil funciones para encontrar cuellos de botella
5. Reproduce bugs con logs para debugging offline
    """)


if __name__ == "__main__":
    demo_debugging()
