"""
Clase base para todos los agentes multi-agente.
Proporciona funcionalidades comunes: percepción, decisión, acción.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
from datetime import datetime
import json
from .ollama_client import OllamaClient


class Agent(ABC):
    """
    Clase base para todos los agentes en el sistema.

    Un agente es una entidad autónoma que:
    1. Percibe su ambiente
    2. Razona sobre lo percibido
    3. Actúa en el ambiente
    """

    def __init__(self, name: str, role: str = "generic", model_client: OllamaClient = None):
        """
        Inicializa un agente

        Args:
            name: Nombre único del agente
            role: Rol/especialidad del agente
            model_client: Cliente Ollama para IA (si es None, crea uno)
        """
        self.name = name
        self.role = role
        self.model = model_client or OllamaClient()

        # Estado interno del agente
        self.state = {}

        # Historial de acciones
        self.history = []

        # Mensajes recibidos
        self.inbox = []

        # Objetivo del agente
        self.objective = None

    def perceive(self, environment: Dict[str, Any]) -> Dict[str, Any]:
        """
        El agente percibe el ambiente

        Args:
            environment: Información disponible del ambiente

        Returns:
            Percepción procesada del agente
        """
        percepts = {
            "timestamp": datetime.now().isoformat(),
            "agent": self.name,
            "environment": environment,
            "own_state": self.state.copy(),
            "pending_messages": len(self.inbox)
        }
        return percepts

    def reason(self, percepts: Dict[str, Any]) -> str:
        """
        El agente razona usando IA

        Args:
            percepts: Percepciones del ambiente

        Returns:
            Decisión tomada
        """
        # Construir prompt para la IA
        prompt = self._build_reasoning_prompt(percepts)

        # Usar el modelo para razonar
        reasoning = self.model.generate(prompt, temperature=0.7)

        return reasoning

    def decide(self, reasoning: str) -> Dict[str, Any]:
        """
        El agente decide qué acción tomar basado en su razonamiento

        Args:
            reasoning: Salida del proceso de razonamiento

        Returns:
            Acción a ejecutar
        """
        decision = {
            "timestamp": datetime.now().isoformat(),
            "agent": self.name,
            "reasoning": reasoning,
            "action": self._extract_action(reasoning)
        }
        return decision

    def act(self, decision: Dict[str, Any]) -> Any:
        """
        El agente ejecuta la acción decidida

        Args:
            decision: Decisión del agente

        Returns:
            Resultado de la acción
        """
        action = decision["action"]

        # Registrar en historial
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "reasoning": decision["reasoning"]
        })

        # Ejecutar la acción específica del agente
        result = self._execute_action(action)

        return result

    def step(self, environment: Dict[str, Any]):
        """
        Un paso completo del ciclo percepto-acción

        Args:
            environment: Estado actual del ambiente
        """
        # Ciclo: percibir -> razonar -> decidir -> actuar
        percepts = self.perceive(environment)
        reasoning = self.reason(percepts)
        decision = self.decide(reasoning)
        result = self.act(decision)

        print(f"\n[{self.name}] Acción ejecutada: {decision['action']}")
        print(f"[{self.name}] Resultado: {result}")

    def receive_message(self, sender: str, content: str):
        """
        El agente recibe un mensaje de otro agente

        Args:
            sender: Nombre del agente remitente
            content: Contenido del mensaje
        """
        message = {
            "timestamp": datetime.now().isoformat(),
            "sender": sender,
            "content": content
        }
        self.inbox.append(message)
        print(f"[{self.name}] Mensaje recibido de {sender}: {content}")

    def send_message(self, recipient: str, content: str) -> Dict[str, Any]:
        """
        El agente envía un mensaje a otro agente

        Args:
            recipient: Nombre del agente receptor
            content: Contenido del mensaje

        Returns:
            Confirmación del envío
        """
        message = {
            "timestamp": datetime.now().isoformat(),
            "sender": self.name,
            "recipient": recipient,
            "content": content
        }
        print(f"[{self.name}] Mensaje enviado a {recipient}: {content}")
        return message

    def get_state(self) -> Dict[str, Any]:
        """Obtiene el estado actual del agente"""
        return {
            "name": self.name,
            "role": self.role,
            "state": self.state.copy(),
            "inbox_size": len(self.inbox),
            "history_length": len(self.history)
        }

    def _build_reasoning_prompt(self, percepts: Dict[str, Any]) -> str:
        """
        Construye el prompt para el razonamiento del agente

        Args:
            percepts: Percepciones del agente

        Returns:
            Prompt para pasar al modelo de IA
        """
        env_str = json.dumps(percepts["environment"], indent=2)
        prompt = f"""Eres un agente llamado {self.name} con rol {self.role}.
Tu objetivo es: {self.objective or 'No especificado'}

Estado actual:
{json.dumps(percepts['own_state'], indent=2)}

Información del ambiente:
{env_str}

Basándote en esto, ¿cuál es tu siguiente acción? Sé conciso y directo."""
        return prompt

    def _extract_action(self, reasoning: str) -> str:
        """
        Extrae la acción del razonamiento

        Args:
            reasoning: Texto del razonamiento del IA

        Returns:
            Acción identificada
        """
        # En implementaciones reales, podrías usar técnicas de NLP
        # Para ahora, devolvemos el razonamiento como acción
        return reasoning[:100] + "..." if len(reasoning) > 100 else reasoning

    @abstractmethod
    def _execute_action(self, action: str) -> Any:
        """
        Ejecuta la acción específica (implementar en subclases)

        Args:
            action: Acción a ejecutar

        Returns:
            Resultado de la acción
        """
        pass

    def __str__(self) -> str:
        return f"Agent({self.name}, {self.role})"

    def __repr__(self) -> str:
        return self.__str__()
