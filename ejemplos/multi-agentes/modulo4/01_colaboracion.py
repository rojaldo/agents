"""
MÓDULO 4: Colaboración y Trabajo en Equipo
Ejemplo 1: Agentes Colaborativos y Consenso

Demuestra:
1. Formación de equipos colaborativos
2. Alcance de consenso mediante votación
3. Delegación y supervisión de tareas
4. Resolución de conflictos en equipo
"""

import sys
sys.path.insert(0, '../utilidades')

from agent_base import Agent
from ollama_client import OllamaClient
from typing import Any, List, Dict, Optional
from datetime import datetime
from enum import Enum
import json


class VotoEnum(Enum):
    """Opciones de voto"""
    A_FAVOR = "a_favor"
    EN_CONTRA = "en_contra"
    ABSTENCION = "abstencion"


class EquipoColaborativo:
    """
    Un equipo donde múltiples agentes trabajan juntos
    para alcanzar un objetivo común
    """

    def __init__(self, nombre: str, objetivo: str):
        self.nombre = nombre
        self.objetivo = objetivo
        self.miembros: List[Agent] = []
        self.tareas_completadas = []
        self.tareas_en_progreso = []
        self.decisiones_tomadas = []

    def agregar_miembro(self, agente: Agent):
        """Agrega un agente al equipo"""
        self.miembros.append(agente)
        print(f"✓ {agente.name} se unió al equipo {self.nombre}")

    def remover_miembro(self, agente: Agent):
        """Remueve un agente del equipo"""
        if agente in self.miembros:
            self.miembros.remove(agente)
            print(f"✗ {agente.name} se fue del equipo {self.nombre}")

    def delegar_tarea(self, responsable: str, tarea: str, descripcion: str):
        """Delega una tarea a un miembro"""
        tarea_obj = {
            "timestamp": datetime.now().isoformat(),
            "responsable": responsable,
            "tarea": tarea,
            "descripcion": descripcion,
            "estado": "asignada"
        }
        self.tareas_en_progreso.append(tarea_obj)
        print(f"  [{self.nombre}] Tarea '{tarea}' delegada a {responsable}")
        return tarea_obj

    def completar_tarea(self, tarea_name: str):
        """Marca una tarea como completada"""
        for tarea in self.tareas_en_progreso[:]:
            if tarea["tarea"] == tarea_name:
                tarea["estado"] = "completada"
                tarea["finalizado"] = datetime.now().isoformat()
                self.tareas_en_progreso.remove(tarea)
                self.tareas_completadas.append(tarea)
                print(f"  ✓ Tarea '{tarea_name}' completada")
                return True
        return False

    def votacion(self, tema: str, opciones: List[str]) -> dict:
        """
        Realiza una votación democrática en el equipo
        """
        print(f"\n  [VOTACIÓN] {tema}")
        print(f"  Opciones: {', '.join(opciones)}")
        print(f"  Votantes: {[m.name for m in self.miembros]}")

        votos = {opt: [] for opt in opciones}
        for i, miembro in enumerate(self.miembros):
            # Simular voto
            voto = opciones[i % len(opciones)]
            votos[voto].append(miembro.name)
            print(f"    {miembro.name} vota por: {voto}")

        # Determinar ganador
        ganador = max(votos.items(), key=lambda x: len(x[1]))[0]

        decision = {
            "timestamp": datetime.now().isoformat(),
            "tema": tema,
            "votos": votos,
            "ganador": ganador,
            "participacion": len(self.miembros)
        }
        self.decisiones_tomadas.append(decision)

        print(f"  ✓ RESULTADO: {ganador} (con {len(votos[ganador])} votos)")

        return decision

    def obtener_estado(self) -> dict:
        """Retorna estado del equipo"""
        return {
            "equipo": self.nombre,
            "objetivo": self.objetivo,
            "miembros": len(self.miembros),
            "tareas_en_progreso": len(self.tareas_en_progreso),
            "tareas_completadas": len(self.tareas_completadas),
            "decisiones_tomadas": len(self.decisiones_tomadas)
        }


class AgenteColaborador(Agent):
    """Agente especializado en trabajo colaborativo"""

    def __init__(self, name: str, especialidad: str):
        super().__init__(name=name, role="collaborative")
        self.model = OllamaClient(model="mistral")
        self.especialidad = especialidad
        self.equipo: Optional[EquipoColaborativo] = None
        self.tareas_asignadas = []
        self.objetivo = f"Colaborar en equipo como {especialidad}"

    def unirse_equipo(self, equipo: EquipoColaborativo):
        """Se une a un equipo"""
        self.equipo = equipo
        equipo.agregar_miembro(self)

    def aceptar_tarea(self, tarea: str, descripcion: str):
        """Acepta una tarea delegada"""
        self.tareas_asignadas.append({
            "timestamp": datetime.now().isoformat(),
            "tarea": tarea,
            "descripcion": descripcion,
            "estado": "en_progreso"
        })
        print(f"    {self.name} aceptó tarea: {tarea}")

    def reportar_resultado(self, tarea: str, resultado: str):
        """Reporta el resultado de una tarea"""
        print(f"    {self.name} reporta: {resultado}")
        if self.equipo:
            self.equipo.completar_tarea(tarea)

    def votar(self, tema: str, opcion: str):
        """Participa en una votación"""
        print(f"    {self.name} vota: {opcion}")
        return opcion

    def _execute_action(self, action: str) -> Any:
        return {
            "agente": self.name,
            "especialidad": self.especialidad,
            "accion": action
        }


def demostrar_equipo_colaborativo():
    """
    Demuestra un equipo de agentes trabajando colaborativamente
    """
    print("\n" + "=" * 70)
    print("EQUIPO COLABORATIVO - Proyecto Común")
    print("=" * 70)
    print("\nCaracterísticas:")
    print("• Múltiples agentes con roles especializados")
    print("• Objetivo común para todo el equipo")
    print("• Delegación de tareas")
    print("• Comunicación abierta")

    # Crear equipo
    equipo = EquipoColaborativo(
        nombre="Equipo-Desarrollo",
        objetivo="Desarrollar un sistema de recomendación"
    )

    print(f"\nObjetivo del equipo: {equipo.objetivo}")

    # Crear agentes especializados
    agentes = [
        AgenteColaborador("Alice", "Data Scientist"),
        AgenteColaborador("Bob", "Ingeniero ML"),
        AgenteColaborador("Charlie", "Ingeniero Backend"),
        AgenteColaborador("Diana", "DevOps Engineer")
    ]

    print("\nMiembros del equipo:")
    for agente in agentes:
        agente.unirse_equipo(equipo)

    # Fase 1: Planificación y delegación
    print("\n" + "─" * 70)
    print("FASE 1: Delegación de Tareas")
    print("─" * 70)

    tareas = [
        ("Data Processing", "Limpiar y preparar datos"),
        ("Feature Engineering", "Crear características del modelo"),
        ("Model Training", "Entrenar el modelo de ML"),
        ("API Development", "Desarrollar API REST"),
        ("Deployment", "Desplegar en producción")
    ]

    for tarea, desc in tareas:
        responsable = agentes[len(equipo.tareas_en_progreso) % len(agentes)]
        equipo.delegar_tarea(responsable.name, tarea, desc)
        responsable.aceptar_tarea(tarea, desc)

    # Fase 2: Ejecución
    print("\n" + "─" * 70)
    print("FASE 2: Ejecución de Tareas")
    print("─" * 70)

    for agente in agentes:
        if agente.tareas_asignadas:
            tarea = agente.tareas_asignadas[0]
            print(f"\n{agente.name} ejecutando: {tarea['tarea']}")
            agente.reportar_resultado(
                tarea['tarea'],
                f"✓ Completado con éxito"
            )

    # Fase 3: Votación sobre decisión crítica
    print("\n" + "─" * 70)
    print("FASE 3: Decisión del Equipo (Votación)")
    print("─" * 70)

    decision = equipo.votacion(
        tema="¿Usar Tensorflow o PyTorch para el modelo?",
        opciones=["Tensorflow", "PyTorch", "Ambas (ensemble)"]
    )

    # Mostrar estado final
    print("\n" + "=" * 70)
    print("ESTADO FINAL DEL EQUIPO")
    print("=" * 70)
    estado = equipo.obtener_estado()
    for key, value in estado.items():
        print(f"{key:25} {value}")

    return equipo, agentes


def demostrar_supervicion_y_delegacion():
    """
    Demuestra supervisión de tareas delegadas
    """
    print("\n" + "=" * 70)
    print("SUPERVISIÓN Y DELEGACIÓN")
    print("=" * 70)
    print("\nCaracterísticas:")
    print("• Manager delega tareas a workers")
    print("• Supervisor monitorea progreso")
    print("• Detección de fallos y reallocación")

    # Crear equipo
    equipo = EquipoColaborativo(
        nombre="Equipo-QA",
        objetivo="Garantizar calidad del software"
    )

    # Supervisor
    supervisor = AgenteColaborador("Eva-Manager", "Project Manager")
    supervisor.unirse_equipo(equipo)

    # Workers
    workers = [
        AgenteColaborador("Frank", "QA Tester 1"),
        AgenteColaborador("Grace", "QA Tester 2"),
    ]
    for worker in workers:
        worker.unirse_equipo(equipo)

    print(f"\nSupervisor: {supervisor.name}")
    print(f"Workers: {[w.name for w in workers]}")

    # Delegación
    print("\n" + "─" * 70)
    print("DELEGACIÓN DE PRUEBAS")
    print("─" * 70)

    test_cases = [
        ("Login Testing", "Probar flujo de login"),
        ("API Testing", "Verificar endpoints"),
        ("UI Testing", "Validar interfaz")
    ]

    for i, (test_name, desc) in enumerate(test_cases):
        worker = workers[i % len(workers)]
        equipo.delegar_tarea(worker.name, test_name, desc)
        worker.aceptar_tarea(test_name, desc)

    # Monitoreo
    print("\n" + "─" * 70)
    print("MONITOREO DE PROGRESO")
    print("─" * 70)

    for i, worker in enumerate(workers):
        if worker.tareas_asignadas:
            tarea = worker.tareas_asignadas[0]
            print(f"\n{supervisor.name} supervisa a {worker.name}")
            print(f"  Tarea: {tarea['tarea']}")
            print(f"  Progreso: En ejecución...")

            # Simular completación
            worker.reportar_resultado(tarea['tarea'], "Tests pasados ✓")

    return equipo


def demostrar_resolucion_conflictos():
    """
    Demuestra cómo un equipo resuelve conflictos
    """
    print("\n" + "=" * 70)
    print("RESOLUCIÓN DE CONFLICTOS EN EQUIPO")
    print("=" * 70)
    print("\nEscenario: El equipo debe elegir entre dos soluciones incompatibles")

    # Crear equipo
    equipo = EquipoColaborativo(
        nombre="Equipo-Arquitectura",
        objetivo="Definir arquitectura del sistema"
    )

    # Crear agentes con diferentes opiniones
    arquitectos = [
        AgenteColaborador("Héctor", "Arquitecto de Software"),
        AgenteColaborador("Iris", "Arquitecta de Datos"),
        AgenteColaborador("Jack", "Arquitecto de Seguridad"),
        AgenteColaborador("Karen", "DevOps Architect")
    ]

    for arq in arquitectos:
        arq.unirse_equipo(equipo)

    print("\n" + "─" * 70)
    print("DEBATIENDO: Arquitectura Monolítica vs Microservicios")
    print("─" * 70)

    # Presentar opciones
    print("\nOpción A: Monolítica")
    print("  ✓ Más simple de desplegar")
    print("  ✗ Difícil de escalar")

    print("\nOpción B: Microservicios")
    print("  ✓ Altamente escalable")
    print("  ✗ Más complejo de mantener")

    # Votación para resolver conflicto
    print("\n" + "─" * 70)
    print("VOTACIÓN PARA RESOLVER CONFLICTO")
    print("─" * 70)

    decision = equipo.votacion(
        tema="¿Qué arquitectura adoptamos?",
        opciones=["Monolítica", "Microservicios"]
    )

    print(f"\n✓ DECISIÓN TOMADA: {decision['ganador']}")
    print(f"  Participación: {decision['participacion']}/{len(arquitectos)} miembros")

    return equipo


if __name__ == "__main__":
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║    COLABORACIÓN Y TRABAJO EN EQUIPO                       ║")
    print("║                                                            ║")
    print("║  1. EQUIPO COLABORATIVO                                   ║")
    print("║  2. SUPERVISIÓN Y DELEGACIÓN                              ║")
    print("║  3. RESOLUCIÓN DE CONFLICTOS                              ║")
    print("╚════════════════════════════════════════════════════════════╝\n")

    try:
        demostrar_equipo_colaborativo()
        demostrar_supervicion_y_delegacion()
        demostrar_resolucion_conflictos()

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
