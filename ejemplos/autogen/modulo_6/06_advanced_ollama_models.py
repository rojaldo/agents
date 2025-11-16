"""
Módulo 6: Optimización y Costos
Ejemplo 6: Advanced Ollama Models - Gestor de modelos multi-proveedor
"""

import requests
from enum import Enum
from datetime import datetime


class LLMProvider(Enum):
    """Proveedores de LLM disponibles"""
    OLLAMA = "ollama"
    LOCAL = "local"
    HUGGINGFACE = "huggingface"


class OllamaModelManager:
    """Gestor de modelos Ollama con selección automática según tarea"""

    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
        self.available_models = []
        self.model_characteristics = {
            "mistral": {"speed": "fast", "quality": "high", "specialty": ["code", "analysis"]},
            "neural-chat": {"speed": "very_fast", "quality": "medium", "specialty": ["general", "fast"]},
            "llama2": {"speed": "medium", "quality": "high", "specialty": ["analysis", "reasoning"]},
            "orca-mini": {"speed": "very_fast", "quality": "low", "specialty": ["fast", "summary"]},
        }
        self.task_preferences = {
            "code": ["mistral", "llama2", "neural-chat"],
            "analysis": ["mistral", "llama2", "orca-mini"],
            "creative": ["neural-chat", "mistral"],
            "fast": ["orca-mini", "neural-chat"],
            "reasoning": ["llama2", "mistral"],
            "general": ["mistral", "neural-chat"]
        }
        self.usage_stats = {}
        self.refresh_models()

    def refresh_models(self):
        """Actualizar lista de modelos disponibles"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.available_models = [m['name'].split(':')[0] for m in data.get('models', [])]
                print(f"✓ Modelos disponibles: {', '.join(self.available_models) if self.available_models else 'Ninguno'}")
            else:
                print(f"✗ Error al obtener modelos: {response.status_code}")
                self.available_models = []
        except requests.exceptions.ConnectionError:
            print("✗ Error: No se puede conectar a Ollama")
            print("✗ Asegúrate de ejecutar: ollama serve")
            self.available_models = []
        except Exception as e:
            print(f"✗ Error: {e}")
            self.available_models = []

    def select_best_model(self, task_type="general"):
        """Seleccionar mejor modelo según tarea"""
        preferred = self.task_preferences.get(task_type, ["mistral"])

        for model in preferred:
            if any(m.startswith(model) for m in self.available_models):
                return model

        return self.available_models[0] if self.available_models else None

    def get_model_characteristics(self, model):
        """Obtener características del modelo"""
        return self.model_characteristics.get(model, {})

    def generate_with_fallback(self, prompt, task_type="general", temperature=0.7):
        """Generar con fallback automático a otro modelo si falla"""
        model = self.select_best_model(task_type)

        if not model:
            return "Error: No hay modelos disponibles"

        try:
            response = self.generate(prompt, model, temperature)
            self._record_usage(model, task_type, True)
            return response
        except Exception as e:
            print(f"⚠️  Fallback: Modelo {model} falló, intentando otro...")
            # Intentar con otro modelo
            for alt_model in self.available_models:
                if alt_model != model:
                    try:
                        response = self.generate(prompt, alt_model, temperature)
                        self._record_usage(alt_model, task_type, True)
                        return response
                    except:
                        continue

            return f"Error: Todos los modelos fallaron"

    def generate(self, prompt, model=None, temperature=0.7):
        """Generar respuesta con modelo específico"""
        if model is None:
            model = self.select_best_model()

        payload = {
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            else:
                return f"Error del servidor: {response.status_code}"

        except requests.exceptions.ConnectionError:
            return "Error: No se puede conectar a Ollama. ¿Está ejecutándose 'ollama serve'?"
        except requests.exceptions.Timeout:
            return "Error: Timeout esperando respuesta de Ollama"
        except Exception as e:
            return f"Error: {str(e)}"

    def _record_usage(self, model, task_type, success):
        """Registrar uso del modelo"""
        if model not in self.usage_stats:
            self.usage_stats[model] = {"calls": 0, "failures": 0}

        self.usage_stats[model]["calls"] += 1
        if not success:
            self.usage_stats[model]["failures"] += 1

    def get_usage_stats(self):
        """Obtener estadísticas de uso"""
        return self.usage_stats

    def print_stats(self):
        """Imprimir estadísticas"""
        print("\n" + "="*60)
        print("ESTADÍSTICAS DE MODELOS")
        print("="*60)
        print(f"Modelos disponibles: {len(self.available_models)}")

        for model in self.available_models:
            chars = self.get_model_characteristics(model)
            print(f"\n{model}:")
            if chars:
                print(f"  Velocidad: {chars.get('speed', 'N/A')}")
                print(f"  Calidad: {chars.get('quality', 'N/A')}")
                print(f"  Especialidades: {', '.join(chars.get('specialty', []))}")

            if model in self.usage_stats:
                stats = self.usage_stats[model]
                success_rate = ((stats['calls'] - stats['failures']) / stats['calls'] * 100) if stats['calls'] > 0 else 0
                print(f"  Llamadas: {stats['calls']}, Éxito: {success_rate:.1f}%")

        print("="*60 + "\n")


def main():
    """Demostración del Gestor de Modelos"""
    print("Demostración: Advanced Ollama Models Manager")
    print("-" * 60)

    # Crear gestor
    manager = OllamaModelManager()

    # Verificar disponibilidad
    if not manager.available_models:
        print("\n⚠️  Ollama no está disponible.")
        print("Para usar este ejemplo:")
        print("1. Instala Ollama: https://ollama.ai")
        print("2. Ejecuta: ollama serve")
        print("3. Descarga un modelo: ollama pull mistral")
        return

    # Pruebas de generación
    test_cases = [
        ("code", "def fibonacci(n):\n    # Tu código aquí"),
        ("analysis", "Analiza el impacto de la IA"),
        ("creative", "Escribe un haiku sobre la naturaleza"),
        ("fast", "¿Qué es Python?"),
    ]

    print(f"\n📝 Usando gestor de modelos...")
    print(f"Modelos disponibles: {manager.available_models}\n")

    for task_type, prompt in test_cases:
        print(f"[Tarea: {task_type}]")
        print(f"Prompt: {prompt}")

        best_model = manager.select_best_model(task_type)
        print(f"Modelo seleccionado: {best_model}")

        response = manager.generate_with_fallback(prompt, task_type)

        if response.startswith("Error"):
            print(f"❌ {response}")
        else:
            print(f"✓ Respuesta: {response[:80]}...")

        print()

    # Mostrar estadísticas
    manager.print_stats()


if __name__ == "__main__":
    main()
