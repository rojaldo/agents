"""
MÓDULO 1: Fundamentos de Sistemas Multi-Agente
Ejemplo 2: Arquitecturas Multi-Agente

Demuestra tres arquitecturas fundamentales:
1. CENTRALIZADA: Un coordinador maestro controla todo
2. DESCENTRALIZADA: Agentes autónomos sin coordinador
3. JERÁRQUICA: Múltiples niveles de control
"""

import sys
sys.path.insert(0, '../utilidades')

from agent_base import Agent
from ollama_client import OllamaClient
from typing import Any, List
from datetime import datetime


class AgenteCoordinador(Agent):
    """Agente coordinador (arquitectura centralizada)"""

    def __init__(self):
        super().__init__(name="Coordinador-Central", role="coordinator")
        self.model = OllamaClient(model="mistral")
        self.agentes_supervizados = []
        self.objective = "Coordinar y supervisar a todos los agentes"

    def registrar_agente(self, agente: Agent):
        """Registra un agente bajo supervisión"""
        self.agentes_supervizados.append(agente)
        print(f"✓ {agente.name} registrado bajo supervisión del coordinador")

    def asignar_tarea(self, agente_name: str, tarea: str):
        """Asigna una tarea a un agente específico"""
        print(f"[Coordinador] Asignando a {agente_name}: {tarea}")

    def _execute_action(self, action: str) -> Any:
        return {
            "coordinador_accion": action,
            "agentes_supervizados": len(self.agentes_supervizados)
        }


class AgenteDescentralizado(Agent):
    """Agente que funciona de forma autónoma sin coordinador"""

    def __init__(self, name: str):
        super().__init__(name=name, role="autonomous")
        self.model = OllamaClient(model="mistral")
        self.vecinos = []  # Conexiones peer-to-peer con otros agentes
        self.objective = f"Lograr objetivo independientemente"

    def conectar_vecino(self, otro_agente: Agent):
        """Conecta con otro agente de forma peer-to-peer"""
        self.vecinos.append(otro_agente)

    def coordinar_localmente(self, vecinos_estados: List[dict]):
        """Coordina con agentes vecinos solo localmente"""
        # En sistemas descentralizados, la coordinación emerge
        # de interacciones locales
        print(f"[{self.name}] Coordinando con {len(vecinos_estados)} vecinos")

    def _execute_action(self, action: str) -> Any:
        return {
            "agente": self.name,
            "accion": action,
            "conexiones_peer": len(self.vecinos)
        }


class AgenteJerarquico(Agent):
    """Agente en arquitectura jerárquica (tiene supervisor y subordinados)"""

    def __init__(self, name: str, nivel: int = 0):
        super().__init__(name=name, role="hierarchical")
        self.model = OllamaClient(model="mistral")
        self.nivel = nivel
        self.supervisor = None
        self.subordinados = []
        self.objective = f"Cumplir objetivos del nivel {nivel}"

    def establecer_supervisor(self, supervisor: Agent):
        """Establece quién es el supervisor"""
        self.supervisor = supervisor
        print(f"[{self.name}] Asignado supervisor: {supervisor.name}")

    def agregar_subordinado(self, subordinado: Agent):
        """Agrega un agente subordinado"""
        self.subordinados.append(subordinado)
        subordinado.establecer_supervisor(self)

    def escalar_problema(self, problema: str):
        """Escala un problema al nivel superior"""
        if self.supervisor:
            print(f"[{self.name}] Escalando problema: {problema}")

    def delegar_tarea(self, subordinado: Agent, tarea: str):
        """Delega una tarea a un agente subordinado"""
        print(f"[{self.name}] Delegando a {subordinado.name}: {tarea}")

    def _execute_action(self, action: str) -> Any:
        return {
            "agente": self.name,
            "nivel": self.nivel,
            "subordinados": len(self.subordinados),
            "accion": action
        }


def demostrar_arquitectura_centralizada():
    """
    ARQUITECTURA CENTRALIZADA
    - Un coordinador maestro controla todo
    - Ventajas: Control simple, decisiones óptimas globales
    - Desventajas: Punto único de fallo, escalabilidad limitada
    """
    print("\n" + "=" * 70)
    print("ARQUITECTURA CENTRALIZADA")
    print("=" * 70)

    coordinador = AgenteCoordinador()

    # Crear agentes trabajadores
    trabajadores = [
        AgenteDescentralizado(f"Trabajador-{i}") for i in range(1, 4)
    ]

    # Registrar bajo supervisión del coordinador
    for trabajador in trabajadores:
        coordinador.registrar_agente(trabajador)

    # Coordinador asigna tareas
    print("\nEl coordinador asigna tareas:")
    coordinador.asignar_tarea("Trabajador-1", "Procesar datos")
    coordinador.asignar_tarea("Trabajador-2", "Validar resultados")
    coordinador.asignar_tarea("Trabajador-3", "Guardar en BD")

    print(f"\n✓ Coordinador tiene {len(coordinador.agentes_supervizados)} agentes bajo control")

    return coordinador


def demostrar_arquitectura_descentralizada():
    """
    ARQUITECTURA DESCENTRALIZADA
    - Agentes autónomos sin autoridad central
    - Ventajas: Robustez, escalabilidad, resiliencia
    - Desventajas: Complejidad de coordinación, posibles conflictos
    """
    print("\n" + "=" * 70)
    print("ARQUITECTURA DESCENTRALIZADA (Peer-to-Peer)")
    print("=" * 70)

    # Crear red peer-to-peer
    agentes = [
        AgenteDescentralizado(f"Peer-{i}") for i in range(1, 5)
    ]

    # Conectar entre pares
    print("\nConectando agentes en red P2P:")
    for i, agente in enumerate(agentes):
        # Conectar con siguientes agentes (topología de anillo)
        siguiente = agentes[(i + 1) % len(agentes)]
        agente.conectar_vecino(siguiente)
        print(f"  {agente.name} ←→ {siguiente.name}")

    print(f"\n✓ Red P2P formada con {len(agentes)} agentes")
    print("  Cada agente toma decisiones autonomamente")
    print("  La coordinación emerge de interacciones locales")

    return agentes


def demostrar_arquitectura_jerarquica():
    """
    ARQUITECTURA JERÁRQUICA
    - Múltiples niveles de coordinadores
    - Ventajas: Balance entre centralización y distribución
    - Desventajas: Complejidad intermedia
    """
    print("\n" + "=" * 70)
    print("ARQUITECTURA JERÁRQUICA")
    print("=" * 70)

    # Nivel 0: Director general
    director = AgenteJerarquico("Director-General", nivel=0)

    # Nivel 1: Managers
    manager1 = AgenteJerarquico("Manager-Operaciones", nivel=1)
    manager2 = AgenteJerarquico("Manager-Datos", nivel=1)

    director.agregar_subordinado(manager1)
    director.agregar_subordinado(manager2)

    # Nivel 2: Trabajadores
    empleados1 = [
        AgenteJerarquico(f"Trabajador-Op-{i}", nivel=2) for i in range(1, 3)
    ]
    empleados2 = [
        AgenteJerarquico(f"Trabajador-Datos-{i}", nivel=2) for i in range(1, 3)
    ]

    for emp in empleados1:
        manager1.agregar_subordinado(emp)

    for emp in empleados2:
        manager2.agregar_subordinado(emp)

    # Mostrar la jerarquía
    print("\nJerarquía establecida:")
    print(f"  {director.name} (nivel 0)")
    print(f"  ├─ {manager1.name} (nivel 1)")
    for emp in empleados1:
        print(f"  │  └─ {emp.name} (nivel 2)")
    print(f"  └─ {manager2.name} (nivel 1)")
    for emp in empleados2:
        print(f"     └─ {emp.name} (nivel 2)")

    # Delegar tareas bajando la jerarquía
    print("\nDelegación de tareas:")
    manager1.delegar_tarea(empleados1[0], "Procesar lote A")
    manager2.delegar_tarea(empleados2[0], "Indexar datos")

    return director


def comparar_arquitecturas():
    """Compara las tres arquitecturas"""
    print("\n" + "=" * 70)
    print("COMPARACIÓN DE ARQUITECTURAS")
    print("=" * 70)

    comparacion = {
        "CENTRALIZADA": {
            "Control": "⭐⭐⭐⭐⭐",
            "Escalabilidad": "⭐",
            "Robustez": "⭐",
            "Complejidad": "⭐",
            "Casos de uso": "Pequeños sistemas, control crítico"
        },
        "DESCENTRALIZADA": {
            "Control": "⭐⭐",
            "Escalabilidad": "⭐⭐⭐⭐⭐",
            "Robustez": "⭐⭐⭐⭐⭐",
            "Complejidad": "⭐⭐⭐⭐⭐",
            "Casos de uso": "Redes P2P, IoT distribuido, blockchain"
        },
        "JERÁRQUICA": {
            "Control": "⭐⭐⭐⭐",
            "Escalabilidad": "⭐⭐⭐",
            "Robustez": "⭐⭐⭐",
            "Complejidad": "⭐⭐⭐",
            "Casos de uso": "Empresas, organizaciones complejas"
        }
    }

    for arch, props in comparacion.items():
        print(f"\n{arch}:")
        for prop, valor in props.items():
            print(f"  {prop:15} {valor}")


if __name__ == "__main__":
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║    ARQUITECTURAS MULTI-AGENTE                             ║")
    print("║                                                            ║")
    print("║  1. CENTRALIZADA: Coordinador maestro                     ║")
    print("║  2. DESCENTRALIZADA: Agentes autónomos (P2P)              ║")
    print("║  3. JERÁRQUICA: Múltiples niveles                         ║")
    print("╚════════════════════════════════════════════════════════════╝\n")

    try:
        # Demostrar las tres arquitecturas
        demostrar_arquitectura_centralizada()
        demostrar_arquitectura_descentralizada()
        demostrar_arquitectura_jerarquica()

        # Comparación
        comparar_arquitecturas()

    except Exception as e:
        print(f"\nError: {e}")
        print("Nota: Asegúrate de que Ollama está corriendo")
