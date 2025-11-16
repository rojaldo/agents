#!/usr/bin/env python3
"""
Utilidades para integración con Ollama
Proporciona funciones para conectar con Ollama como proveedor de LLM local
"""

import requests
import json
from typing import Optional, List, Dict, Any
import time


class OllamaClient:
    """Cliente para interactuar con Ollama"""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "mistral"):
        """
        Inicializar el cliente de Ollama

        Args:
            base_url: URL base de Ollama (default: http://localhost:11434)
            model: Modelo a usar (default: mistral)
        """
        self.base_url = base_url
        self.model = model
        self.api_endpoint = f"{base_url}/api/generate"
        self.chat_endpoint = f"{base_url}/api/chat"

    def is_available(self) -> bool:
        """Verificar si Ollama está disponible"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except (requests.ConnectionError, requests.Timeout):
            return False

    def get_available_models(self) -> List[str]:
        """Obtener lista de modelos disponibles"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
            return []
        except Exception as e:
            print(f"Error obteniendo modelos: {e}")
            return []

    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 500) -> str:
        """
        Generar texto usando Ollama

        Args:
            prompt: Texto de entrada
            temperature: Control de creatividad (0-1)
            max_tokens: Número máximo de tokens

        Returns:
            Texto generado
        """
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }

            response = requests.post(
                self.api_endpoint,
                json=payload,
                timeout=120
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("response", "").strip()
            else:
                return f"Error: {response.status_code}"

        except requests.Timeout:
            return "Error: Timeout - Ollama tardó demasiado en responder"
        except requests.ConnectionError:
            return "Error: No se puede conectar a Ollama en " + self.base_url
        except Exception as e:
            return f"Error: {str(e)}"

    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """
        Chat con Ollama usando formato de mensajes

        Args:
            messages: Lista de mensajes con formato [{"role": "user", "content": "..."}]
            temperature: Control de creatividad

        Returns:
            Respuesta del modelo
        """
        try:
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": temperature
                }
            }

            response = requests.post(
                self.chat_endpoint,
                json=payload,
                timeout=120
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("message", {}).get("content", "").strip()
            else:
                return f"Error: {response.status_code}"

        except requests.Timeout:
            return "Error: Timeout - Ollama tardó demasiado en responder"
        except requests.ConnectionError:
            return "Error: No se puede conectar a Ollama"
        except Exception as e:
            return f"Error: {str(e)}"


class MockOllamaClient:
    """Cliente simulado de Ollama para testing sin servidor real"""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "mistral"):
        """Inicializar el cliente simulado"""
        self.base_url = base_url
        self.model = model
        self.responses = {
            "hola": "¡Hola! Soy un asistente IA. ¿Cómo puedo ayudarte hoy?",
            "nombre": "Soy un asistente de IA ejecutándose en Ollama localmente.",
            "python": "Python es un lenguaje de programación interpretado, dinámico y de alto nivel.",
            "variable": "Una variable es un contenedor con nombre que almacena un valor en la memoria.",
            "función": "Una función es un bloque de código reutilizable que realiza una tarea específica.",
            "lista": "Una lista es una colección ordenada de elementos que pueden ser de diferentes tipos.",
            "diccionario": "Un diccionario es una colección de pares clave-valor.",
            "clase": "Una clase es un blueprint o plantilla para crear objetos.",
            "código": "Claro, puedo ayudarte con tu código. ¿Qué necesitas?",
            "generador": "Un generador es una función que utiliza yield para devolver valores uno a uno.",
            "decorador": "Un decorador es una función que modifica el comportamiento de otra función.",
            "módulo": "Un módulo es un archivo de Python que contiene código reutilizable.",
            "fibonacci": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
            "factorial": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)",
            "primo": "def is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True"
        }

    def is_available(self) -> bool:
        """Siempre disponible en modo mock"""
        return True

    def get_available_models(self) -> List[str]:
        """Retornar modelos simulados"""
        return ["mistral", "llama2", "neural-chat"]

    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 500) -> str:
        """Generar respuesta simulada"""
        prompt_lower = prompt.lower()

        # Respuestas para generación de código
        code_responses = {
            "fibonacci": '''def fibonacci(n):
    """Calcular los primeros n números de Fibonacci"""
    if n <= 0:
        return []
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[-1] + fib[-2])
    return fib

result = fibonacci(10)
print("Fibonacci(10):", result)''',

            "factorial": '''def factorial(n):
    """Calcular factorial"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

result = factorial(5)
print("5! =", result)''',

            "primo": '''def is_prime(n):
    """Verificar si es primo"""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

primes = [n for n in range(2, 30) if is_prime(n)]
print("Primos hasta 30:", primes)'''
        }

        # Buscar coincidencias de código
        for key, response in code_responses.items():
            if key in prompt_lower:
                return response

        # Buscar coincidencias en respuestas normales
        for key, response in self.responses.items():
            if key in prompt_lower:
                return response

        # Respuesta por defecto
        return "He entendido tu pregunta. Basándome en tu solicitud, aquí está mi respuesta sobre el tema que mencionaste."

    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """Chat simulado"""
        if not messages:
            return "No hay mensajes para procesar."

        # Usar el último mensaje del usuario
        last_message = messages[-1].get("content", "").lower()
        return self.generate(last_message, temperature)


def create_ollama_client(use_mock: bool = False, base_url: str = "http://localhost:11434",
                        model: str = "mistral") -> OllamaClient:
    """
    Crear un cliente de Ollama (real o simulado)

    Args:
        use_mock: Si True, usa el cliente simulado
        base_url: URL de Ollama
        model: Modelo a usar

    Returns:
        Cliente de Ollama
    """
    if use_mock:
        return MockOllamaClient(base_url, model)

    client = OllamaClient(base_url, model)

    # Verificar si Ollama está disponible
    if not client.is_available():
        print(f"⚠️  Advertencia: No se puede conectar a Ollama en {base_url}")
        print("   Usando cliente simulado (mock)...")
        return MockOllamaClient(base_url, model)

    return client


def test_ollama_connection(base_url: str = "http://localhost:11434") -> bool:
    """
    Probar conexión con Ollama

    Returns:
        True si está disponible, False en caso contrario
    """
    client = OllamaClient(base_url)
    is_available = client.is_available()

    if is_available:
        print(f"✓ Ollama disponible en {base_url}")
        models = client.get_available_models()
        if models:
            print(f"✓ Modelos disponibles: {', '.join(models[:3])}")
        return True
    else:
        print(f"✗ Ollama no disponible en {base_url}")
        print(f"  Asegúrate de ejecutar: ollama serve")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("Prueba de Conectividad con Ollama")
    print("=" * 70)

    # Probar conexión
    test_ollama_connection()

    print("\n" + "=" * 70)
    print("Prueba de Cliente Mock")
    print("=" * 70)

    # Probar cliente mock
    mock_client = MockOllamaClient()
    print(f"Mock disponible: {mock_client.is_available()}")
    print(f"Modelos simulados: {mock_client.get_available_models()}")

    response = mock_client.generate("¿Qué es una variable en Python?")
    print(f"\nRespuesta a '¿Qué es una variable?':\n{response}")
