"""
MÓDULO 1: Fundamentos de Sistemas Multi-Agente
Ejemplo 1: Agente Básico Autónomo

Este ejemplo muestra los conceptos fundamentales:
- Definición de agente: entidad que percibe, razona y actúa
- Ciclo percepto-acción básico
- Autonomía en toma de decisiones
"""

import sys
sys.path.insert(0, '../utilidades')

from agent_base import Agent
from ollama_client import OllamaClient
from typing import Any


class AgenteAutonomo(Agent):
    """
    Un agente autónomo simple que:
    1. Percibe el ambiente
    2. Razona sobre la situación
    3. Toma decisiones
    4. Ejecuta acciones
    """

    def __init__(self, name: str, objetivo: str):
        """
        Args:
            name: Nombre del agente
            objetivo: Qué quiere lograr el agente
        """
        # Inicializar cliente Ollama
        model_client = OllamaClient(model="mistral")

        # Llamar al inicializador de la clase base
        super().__init__(name=name, role="autonomous", model_client=model_client)

        # Objetivo específico del agente
        self.objective = objetivo

        # Variables de estado específicas
        self.energia = 100
        self.tareas_completadas = 0

    def _execute_action(self, action: str) -> Any:
        """
        Ejecuta la acción decidida por el agente

        Args:
            action: Descripción de la acción

        Returns:
            Resultado de ejecutar la acción
        """
        # Simular gasto de energía
        self.energia = max(0, self.energia - 10)

        # Simular completar una tarea
        self.tareas_completadas += 1

        return {
            "accion_ejecutada": action,
            "energia_restante": self.energia,
            "tareas_completadas": self.tareas_completadas,
            "exito": True
        }


def demostrar_ciclo_percepto_accion():
    """
    Demuestra el ciclo fundamental de un agente autónomo
    """
    print("=" * 60)
    print("AGENTE AUTÓNOMO - Ciclo Percepto-Acción")
    print("=" * 60)

    # Crear un agente
    agente = AgenteAutonomo(
        name="Agente-Explorador-1",
        objetivo="Explorar y mapear el ambiente"
    )

    print(f"\nAgente creado: {agente.name}")
    print(f"Objetivo: {agente.objective}")
    print(f"Rol: {agente.role}")

    # Simular el ambiente
    ambiente = {
        "temperatura": 25,
        "humedad": 60,
        "obstaculos": 3,
        "zona_segura": True,
        "energia_disponible": agente.energia
    }

    print(f"\nAmbiente inicial:")
    for key, value in ambiente.items():
        print(f"  {key}: {value}")

    # Ejecutar varios pasos
    print("\n" + "=" * 60)
    print("Ejecutando 3 ciclos de percepto-acción...")
    print("=" * 60)

    for i in range(3):
        print(f"\n--- CICLO {i+1} ---")
        agente.step(ambiente)

        # Actualizar ambiente basado en acciones del agente
        if agente.energia <= 0:
            print("⚠ Energía agotada. El agente se detiene.")
            break

    # Mostrar estado final
    print("\n" + "=" * 60)
    print("ESTADO FINAL DEL AGENTE")
    print("=" * 60)
    estado_final = agente.get_state()
    for key, value in estado_final.items():
        print(f"{key}: {value}")

    # Mostrar historial
    print("\n" + "=" * 60)
    print("HISTORIAL DE ACCIONES")
    print("=" * 60)
    for i, accion in enumerate(agente.history, 1):
        print(f"\n{i}. Timestamp: {accion['timestamp']}")
        print(f"   Razonamiento: {accion['reasoning'][:100]}...")


if __name__ == "__main__":
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║       CONCEPTO: Agentes Autónomos                         ║")
    print("║                                                            ║")
    print("║  Un agente es una entidad que:                            ║")
    print("║  • PERCIBE su ambiente (sensors/inputs)                   ║")
    print("║  • RAZONA sobre la situación (cognición)                  ║")
    print("║  • ACTÚA en el mundo (actuadores/outputs)                 ║")
    print("║                                                            ║")
    print("║  Ciclo: Percepción → Razonamiento → Acción → Repetir      ║")
    print("╚════════════════════════════════════════════════════════════╝\n")

    try:
        demostrar_ciclo_percepto_accion()
    except Exception as e:
        print(f"\nError: {e}")
        print("Asegúrate de que Ollama está corriendo con: ollama serve")
