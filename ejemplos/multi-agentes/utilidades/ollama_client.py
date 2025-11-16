"""
Cliente Ollama para interactuar con modelos locales.
Simplifica la comunicación con el servidor Ollama.
"""

import requests
import json
from typing import Optional
import time


class OllamaClient:
    """Cliente para conectar con Ollama localmente"""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "mistral"):
        """
        Inicializa el cliente Ollama

        Args:
            base_url: URL donde corre Ollama (default: localhost:11434)
            model: Modelo a usar (default: mistral)
        """
        self.base_url = base_url
        self.model = model
        self._verify_connection()

    def _verify_connection(self) -> bool:
        """Verifica que Ollama esté disponible"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                print(f"✓ Ollama disponible en {self.base_url}")
                return True
        except Exception as e:
            print(f"✗ Error conectando a Ollama: {e}")
            print(f"  Asegúrate de que Ollama esté corriendo: ollama serve")
            return False

    def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """
        Genera una respuesta del modelo

        Args:
            prompt: Texto de entrada
            temperature: Control de creatividad (0-1)

        Returns:
            Respuesta del modelo
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "temperature": temperature,
                    "stream": False
                },
                timeout=300  # 5 minutos timeout
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("response", "").strip()
            else:
                return f"Error: {response.status_code}"

        except requests.exceptions.Timeout:
            return "Error: Timeout - la respuesta tomó demasiado tiempo"
        except Exception as e:
            return f"Error en generación: {str(e)}"

    def chat(self, messages: list, temperature: float = 0.7) -> str:
        """
        Conversación estilo chat

        Args:
            messages: Lista de mensajes {'role': 'user'/'assistant', 'content': '...'}
            temperature: Control de creatividad

        Returns:
            Respuesta del modelo
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": temperature,
                    "stream": False
                },
                timeout=300
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("message", {}).get("content", "").strip()
            else:
                return f"Error: {response.status_code}"

        except Exception as e:
            return f"Error en chat: {str(e)}"

    def list_models(self) -> list:
        """Lista los modelos disponibles en Ollama"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get("models", [])
            return []
        except Exception as e:
            print(f"Error listando modelos: {e}")
            return []

    def set_model(self, model_name: str):
        """Cambia el modelo activo"""
        self.model = model_name
        print(f"Modelo cambiado a: {model_name}")


def crear_cliente_local(modelo: str = "mistral") -> OllamaClient:
    """
    Función auxiliar para crear un cliente Ollama rápidamente

    Args:
        modelo: Nombre del modelo

    Returns:
        Instancia de OllamaClient lista para usar
    """
    return OllamaClient(model=modelo)
