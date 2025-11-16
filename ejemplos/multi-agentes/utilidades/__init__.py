"""
Utilidades para sistema multi-agentes con LangChain y Ollama
"""

from .ollama_client import OllamaClient, crear_cliente_local
from .agent_base import Agent

__all__ = [
    'OllamaClient',
    'crear_cliente_local',
    'Agent'
]
