"""
MÓDULO 3: Coordinación y Orquestación
Ejemplo 1: Estrategias de Coordinación

Demuestra tres estrategias de coordinación:
1. CENTRALIZADA: Un coordinador maestro
2. JERÁRQUICA: Múltiples niveles
3. DISTRIBUIDA: Consenso emergente
"""

import sys
sys.path.insert(0, '../utilidades')

from agent_base import Agent
from ollama_client import OllamaClient
from typing import Any, List, Dict
from datetime import datetime
from enum import Enum
import time


class EstadoRecurso(Enum):
    """Estados posibles de un recurso compartido"""
    LIBRE = "libre"
    OCUPADO = "ocupado"
    RESERVADO = "reservado"


class RecursoCompartido:
    """Simula un recurso que múltiples agentes quieren usar"""

    def __init__(self, nombre: str):
        self.nombre = nombre
        self.estado = EstadoRecurso.LIBRE
        self.propietario = None
        self.historial_acceso = []

    def adquirir(self, agente_name: str, timeout: int = 10) -> bool:
        """Intenta adquirir el recurso"""
        if self.estado == EstadoRecurso.LIBRE:
            self.estado = EstadoRecurso.OCUPADO
            self.propietario = agente_name
            self.historial_acceso.append({
                "timestamp": datetime.now().isoformat(),
                "agente": agente_name,
                "accion": "adquirió"
            })
            print(f"  ✓ {agente_name} adquirió {self.nombre}")
            return True
        else:
            print(f"  ✗ {agente_name} no pudo adquirir {self.nombre} (ocupado por {self.propietario})")
            return False

    def liberar(self, agente_name: str) -> bool:
        """Libera el recurso"""
        if self.propietario == agente_name:
            self.estado = EstadoRecurso.LIBRE
            self.propietario = None
            self.historial_acceso.append({
                "timestamp": datetime.now().isoformat(),
                "agente": agente_name,
                "accion": "liberó"
            })
            print(f"  ✓ {agente_name} liberó {self.nombre}")
            return True
        return False

    def obtener_estado(self) -> dict:
        return {
            "nombre": self.nombre,
            "estado": self.estado.value,
            "propietario": self.propietario or "ninguno",
            "accesos_totales": len(self.historial_acceso)
        }


class CoordinadorCentralizado:
    """Coordinador que asigna recursos centralizadamente"""

    def __init__(self, nombre: str):
        self.nombre = nombre
        self.agentes_registrados = {}
        self.cola_solicitudes = []
        self.decisiones_tomadas = []

    def registrar_agente(self, agente_name: str):
        self.agentes_registrados[agente_name] = {
            "estado": "listo",
            "tareas_asignadas": 0
        }
        print(f"✓ {agente_name} registrado con coordinador {self.nombre}")

    def solicitar_recurso(self, agente_name: str, recurso_name: str):
        """Un agente solicita acceso a un recurso"""
        solicitud = {
            "timestamp": datetime.now().isoformat(),
            "agente": agente_name,
            "recurso": recurso_name
        }
        self.cola_solicitudes.append(solicitud)
        print(f"  {agente_name} solicitó {recurso_name}")

    def otorgar_acceso(self, agente_name: str, recurso: RecursoCompartido) -> bool:
        """El coordinador otorga acceso al recurso"""
        success = recurso.adquirir(agente_name)
        if success:
            self.decisiones_tomadas.append({
                "timestamp": datetime.now().isoformat(),
                "decision": f"Otorgado {recurso.nombre} a {agente_name}"
            })
        return success

    def obtener_estadisticas(self) -> dict:
        return {
            "agentes_registrados": len(self.agentes_registrados),
            "solicitudes_pendientes": len(self.cola_solicitudes),
            "decisiones_tomadas": len(self.decisiones_tomadas)
        }


class AgenteConCoordinacion(Agent):
    """Agente que respeta coordinación"""

    def __init__(self, name: str, coordinador: CoordinadorCentralizado = None):
        super().__init__(name=name, role="coordinated")
        self.model = OllamaClient(model="mistral")
        self.coordinador = coordinador
        self.recursos_asignados = []
        self.objetivo = "Completar tareas usando recursos compartidos"

        if coordinador:
            coordinador.registrar_agente(name)

    def solicitar_recurso(self, recurso: RecursoCompartido) -> bool:
        """Solicita un recurso al coordinador"""
        if self.coordinador:
            self.coordinador.solicitar_recurso(self.name, recurso.nombre)
            success = self.coordinador.otorgar_acceso(self.name, recurso)
            if success:
                self.recursos_asignados.append(recurso.nombre)
            return success
        else:
            # Sin coordinador, intenta adquirir directamente
            return recurso.adquirir(self.name)

    def liberar_recurso(self, recurso: RecursoCompartido):
        """Libera un recurso"""
        if recurso.liberar(self.name):
            if recurso.nombre in self.recursos_asignados:
                self.recursos_asignados.remove(recurso.nombre)

    def procesar_tarea(self, descripcion: str, duracion: float = 1.0):
        """Simula procesamiento de una tarea"""
        print(f"    [{self.name}] Procesando: {descripcion}")
        time.sleep(duracion)

    def _execute_action(self, action: str) -> Any:
        return {"agente": self.name, "accion": action}


def demostrar_coordinacion_centralizada():
    """
    COORDINACIÓN CENTRALIZADA
    - Un coordinador maestro asigna recursos
    - Ventajas: Óptimo global, evita conflictos
    - Desventajas: Punto único de fallo, escalabilidad limitada
    """
    print("\n" + "=" * 70)
    print("COORDINACIÓN CENTRALIZADA")
    print("=" * 70)
    print("\nCaracterísticas:")
    print("• Un coordinador central asigna todos los recursos")
    print("• Decisiones óptimas globales")
    print("• Evita condiciones de carrera")
    print("• Desventaja: Punto único de fallo")

    # Crear coordinador
    coordinador = CoordinadorCentralizado("Coordinador-Principal")

    # Crear recurso compartido
    servidor_bd = RecursoCompartido("Servidor-BD")

    # Crear agentes
    agentes = [
        AgenteConCoordinacion(f"Worker-{i}", coordinador)
        for i in range(1, 4)
    ]

    print("\nSecuencia de acceso al recurso:")
    print("─" * 50)

    # Simular acceso coordinado
    for agente in agentes:
        print(f"\n{agente.name} intenta acceder a Servidor-BD...")
        if agente.solicitar_recurso(servidor_bd):
            agente.procesar_tarea(f"Leyendo datos", 0.5)
            agente.liberar_recurso(servidor_bd)
        time.sleep(0.3)

    # Estadísticas
    print("\n" + "=" * 50)
    print("Estadísticas del Coordinador:")
    stats = coordinador.obtener_estadisticas()
    for key, value in stats.items():
        print(f"  {key:25} {value}")

    return coordinador, servidor_bd


def demostrar_coordinacion_jerarquica():
    """
    COORDINACIÓN JERÁRQUICA
    - Múltiples niveles de coordinadores
    - Balance entre centralización y distribución
    - Escalabilidad mejorada
    """
    print("\n" + "=" * 70)
    print("COORDINACIÓN JERÁRQUICA")
    print("=" * 70)
    print("\nCaracterísticas:")
    print("• Múltiples niveles de coordinadores")
    print("• Cada coordinador supervisa un grupo")
    print("• Mejor escalabilidad que centralizada")
    print("• Menos puntos únicos de fallo")

    # Crear jerarquía de coordinadores
    coordinador_central = CoordinadorCentralizado("Coordinador-Central")
    coordinador_region1 = CoordinadorCentralizado("Coordinador-Región-1")
    coordinador_region2 = CoordinadorCentralizado("Coordinador-Región-2")

    # Crear recursos por región
    recurso_r1 = RecursoCompartido("Base-Datos-Región1")
    recurso_r2 = RecursoCompartido("Base-Datos-Región2")

    print("\nHierarquía de coordinadores:")
    print("─" * 50)
    print("  Coordinador-Central")
    print("  ├─ Coordinador-Región-1 → BD-R1")
    print("  └─ Coordinador-Región-2 → BD-R2")

    # Crear agentes para cada región
    agentes_r1 = [
        AgenteConCoordinacion(f"Worker-R1-{i}", coordinador_region1)
        for i in range(1, 3)
    ]
    agentes_r2 = [
        AgenteConCoordinacion(f"Worker-R2-{i}", coordinador_region2)
        for i in range(1, 3)
    ]

    print("\nAcceso a recursos por región:")
    print("─" * 50)

    # Región 1
    print("\nRegión 1:")
    for agente in agentes_r1:
        if agente.solicitar_recurso(recurso_r1):
            agente.procesar_tarea(f"Procesando en Región 1", 0.3)
            agente.liberar_recurso(recurso_r1)
        time.sleep(0.2)

    # Región 2
    print("\nRegión 2:")
    for agente in agentes_r2:
        if agente.solicitar_recurso(recurso_r2):
            agente.procesar_tarea(f"Procesando en Región 2", 0.3)
            agente.liberar_recurso(recurso_r2)
        time.sleep(0.2)

    return [coordinador_region1, coordinador_region2]


def demostrar_coordinacion_distribuida():
    """
    COORDINACIÓN DISTRIBUIDA
    - Negociación local entre agentes
    - Consenso emerge de interacciones
    - Máxima resiliencia pero más complejidad
    """
    print("\n" + "=" * 70)
    print("COORDINACIÓN DISTRIBUIDA")
    print("=" * 70)
    print("\nCaracterísticas:")
    print("• Agentes negocian directamente entre ellos")
    print("• Sin coordinador central")
    print("• Mayor resiliencia")
    print("• Más compleja de implementar")

    # Crear recurso
    servidor = RecursoCompartido("Servidor-Compartido")

    # Crear agentes sin coordinador
    agentes = [
        AgenteConCoordinacion(f"Peer-{i}")
        for i in range(1, 4)
    ]

    print("\nCordinación mediante turnos (basada en timestamps):")
    print("─" * 50)

    # Simular coordinación distribuida con turnos
    for i, agente in enumerate(agentes):
        timestamp_solicitud = datetime.now()
        print(f"\n{agente.name} solicita acceso (timestamp: {i+1})")

        # Simula que el agente con timestamp más antiguo consigue el recurso
        if servidor.estado == EstadoRecurso.LIBRE:
            if agente.solicitar_recurso(servidor):
                agente.procesar_tarea(f"Ejecutando tarea", 0.3)
                agente.liberar_recurso(servidor)
        time.sleep(0.2)

    print("\nResultado: Acceso ordenado sin coordinador central")
    print("           (basado en orden de llegada)")

    return agentes


def comparar_estrategias():
    """Compara las tres estrategias"""
    print("\n" + "=" * 70)
    print("COMPARACIÓN DE ESTRATEGIAS DE COORDINACIÓN")
    print("=" * 70)

    comparacion = {
        "CENTRALIZADA": {
            "Optimalidad": "⭐⭐⭐⭐⭐",
            "Escalabilidad": "⭐",
            "Resiliencia": "⭐",
            "Complejidad": "⭐",
            "Latencia": "Baja",
            "Mejor para": "Sistemas pequeños con control crítico"
        },
        "JERÁRQUICA": {
            "Optimalidad": "⭐⭐⭐⭐",
            "Escalabilidad": "⭐⭐⭐",
            "Resiliencia": "⭐⭐⭐",
            "Complejidad": "⭐⭐⭐",
            "Latencia": "Media",
            "Mejor para": "Organizaciones grandes, sistemas distribuidos"
        },
        "DISTRIBUIDA": {
            "Optimalidad": "⭐⭐",
            "Escalabilidad": "⭐⭐⭐⭐⭐",
            "Resiliencia": "⭐⭐⭐⭐⭐",
            "Complejidad": "⭐⭐⭐⭐⭐",
            "Latencia": "Alta",
            "Mejor para": "P2P, sistemas altamente distribuidos, blockchain"
        }
    }

    for estrategia, props in comparacion.items():
        print(f"\n{estrategia}:")
        for prop, valor in props.items():
            print(f"  {prop:15} {valor}")


if __name__ == "__main__":
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║    COORDINACIÓN Y ORQUESTACIÓN                            ║")
    print("║                                                            ║")
    print("║  1. CENTRALIZADA: Un coordinador maestro                  ║")
    print("║  2. JERÁRQUICA: Múltiples niveles                         ║")
    print("║  3. DISTRIBUIDA: Negociación entre pares                  ║")
    print("╚════════════════════════════════════════════════════════════╝\n")

    try:
        demostrar_coordinacion_centralizada()
        demostrar_coordinacion_jerarquica()
        demostrar_coordinacion_distribuida()
        comparar_estrategias()

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
