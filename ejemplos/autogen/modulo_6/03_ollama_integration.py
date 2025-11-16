"""
Módulo 6: Optimización y Costos
Ejemplo 3: Integración Ollama - Cliente avanzado para Ollama con optimización
"""

import requests
import json
from datetime import datetime


class AdvancedOllamaClient:
    """Cliente avanzado para Ollama con tracking de costos"""

    def __init__(self, base_url="http://localhost:11434", model="mistral"):
        """
        Inicializar cliente Ollama

        Args:
            base_url: URL base de Ollama
            model: Modelo a usar
        """
        self.base_url = base_url
        self.model = model
        self.available_models = []
        self.interactions = []
        self.tokens_used = 0

        # Intentar conectar y obtener modelos disponibles
        try:
            self.refresh_models()
            print(f"✓ Conectado a Ollama en {base_url}")
            print(f"✓ Modelo disponible: {model}")
        except Exception as e:
            print(f"✗ Error conectando a Ollama: {e}")
            print(f"✗ Asegúrate de ejecutar: ollama serve")

    def refresh_models(self):
        """Actualizar lista de modelos disponibles"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            data = response.json()
            self.available_models = [m['name'].split(':')[0] for m in data.get('models', [])]
        except Exception as e:
            self.available_models = []
            raise Exception(f"No se pudo conectar a Ollama: {e}")

    def select_best_model(self, task_type="general"):
        """Seleccionar mejor modelo según la tarea"""
        model_rankings = {
            "code": ["mistral", "neural-chat", "llama2"],
            "analysis": ["mistral", "llama2", "neural-chat"],
            "creative": ["mistral", "neural-chat"],
            "fast": ["neural-chat", "mistral"],
            "general": ["mistral"]
        }

        preferred = model_rankings.get(task_type, self.available_models)
        for model in preferred:
            if any(m.startswith(model) for m in self.available_models):
                return model

        return self.available_models[0] if self.available_models else self.model

    def generate(self, prompt, model=None, temperature=0.7, stream=False):
        """
        Generar respuesta con Ollama

        Args:
            prompt: Texto de entrada
            model: Modelo a usar (por defecto, el configurado)
            temperature: Temperatura (0-1)
            stream: Si es True, retorna streaming

        Returns:
            Respuesta del modelo
        """
        if model is None:
            model = self.model

        payload = {
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": stream
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                response_text = result.get('response', '')

                # Registrar interacción
                self._record_interaction(prompt, response_text)

                return response_text
            else:
                print(f"Error: {response.status_code}")
                return f"Error del servidor: {response.status_code}"

        except requests.exceptions.ConnectionError:
            return "Error: No se puede conectar a Ollama. ¿Está ejecutándose 'ollama serve'?"
        except requests.exceptions.Timeout:
            return "Error: Timeout esperando respuesta de Ollama"
        except Exception as e:
            return f"Error: {str(e)}"

    def generate_with_fallback(self, prompt, task_type="general", temperature=0.7):
        """
        Generar con fallback automático a otro modelo si falla

        Args:
            prompt: Texto de entrada
            task_type: Tipo de tarea
            temperature: Temperatura

        Returns:
            Respuesta del modelo
        """
        model = self.select_best_model(task_type)

        try:
            return self.generate(prompt, model, temperature)
        except Exception as e:
            print(f"Fallback: Modelo {model} falló, intentando otro...")
            # Intentar con otro modelo
            for alt_model in self.available_models:
                if alt_model != model:
                    try:
                        return self.generate(prompt, alt_model, temperature)
                    except:
                        continue

            return "Error: Todos los modelos fallaron"

    def _record_interaction(self, prompt, response):
        """Registrar una interacción"""
        # Estimación simple de tokens
        prompt_tokens = max(1, len(prompt) // 4)
        response_tokens = max(1, len(response) // 4)
        total_tokens = prompt_tokens + response_tokens

        self.interactions.append({
            "timestamp": datetime.now().isoformat(),
            "model": self.model,
            "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
            "response_length": len(response),
            "tokens": total_tokens
        })

        self.tokens_used += total_tokens

    def get_stats(self):
        """Obtener estadísticas de uso"""
        return {
            "total_interactions": len(self.interactions),
            "total_tokens_estimated": self.tokens_used,
            "avg_tokens_per_interaction": self.tokens_used / max(len(self.interactions), 1) if self.interactions else 0,
            "models_available": self.available_models,
            "current_model": self.model
        }

    def print_stats(self):
        """Imprimir estadísticas"""
        stats = self.get_stats()
        print("\n" + "="*50)
        print("ESTADÍSTICAS DE USO")
        print("="*50)
        print(f"Modelo actual: {stats['current_model']}")
        print(f"Modelos disponibles: {', '.join(stats['models_available']) if stats['models_available'] else 'Ninguno'}")
        print(f"Total de interacciones: {stats['total_interactions']}")
        print(f"Total de tokens estimados: {stats['total_tokens_estimated']}")
        print(f"Promedio tokens/interacción: {stats['avg_tokens_per_interaction']:.1f}")
        print("="*50 + "\n")


def main():
    """Demostración del cliente Ollama avanzado"""
    print("Demostración: Cliente Ollama Avanzado")
    print("-" * 60)

    # Crear cliente
    client = AdvancedOllamaClient()

    # Verificar si Ollama está disponible
    if not client.available_models:
        print("\n⚠️  Ollama no está disponible.")
        print("Para usar este ejemplo:")
        print("1. Instala Ollama: https://ollama.ai")
        print("2. Ejecuta: ollama serve")
        print("3. Descarga un modelo: ollama pull mistral")
        return

    # Realizar consultas
    prompts = [
        "¿Qué es Python? (Respuesta corta)",
        "Dame 3 mejores prácticas en programación",
        "Explica qué es machine learning en una línea"
    ]

    print(f"\n📝 Usando modelo: {client.model}")
    print("-" * 60)

    for i, prompt in enumerate(prompts, 1):
        print(f"\n[Consulta {i}]")
        print(f"Prompt: {prompt}")
        print("Generando respuesta...")

        response = client.generate(prompt)

        if response.startswith("Error"):
            print(f"❌ {response}")
        else:
            print(f"Respuesta: {response[:150]}...")

    # Mostrar estadísticas
    client.print_stats()


if __name__ == "__main__":
    main()
