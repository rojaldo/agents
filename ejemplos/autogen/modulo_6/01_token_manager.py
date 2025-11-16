"""
Módulo 6: Optimización y Costos
Ejemplo 1: Token Manager - Gestión básica de tokens y costos
"""

from datetime import datetime


class TokenManager:
    """Gestor básico de tokens y costos"""

    def __init__(self, model="mistral", pricing_per_1k=0.0):
        """
        Inicializar Token Manager

        Args:
            model: Modelo a usar
            pricing_per_1k: Precio por 1000 tokens (0 para modelos locales)
        """
        self.model = model
        self.pricing_per_1k = pricing_per_1k
        self.tokens_used = 0
        self.cost_accumulated = 0.0
        self.interactions = []

    def estimate_tokens(self, text):
        """Estimación aproximada de tokens (1 token ≈ 4 caracteres)"""
        return max(1, len(text) // 4)

    def calculate_cost(self, tokens):
        """Calcular costo basado en tokens"""
        cost = (tokens / 1000) * self.pricing_per_1k
        self.cost_accumulated += cost
        self.tokens_used += tokens
        return cost

    def record_interaction(self, prompt, response):
        """Registrar una interacción"""
        prompt_tokens = self.estimate_tokens(prompt)
        response_tokens = self.estimate_tokens(response)
        total_tokens = prompt_tokens + response_tokens
        cost = self.calculate_cost(total_tokens)

        self.interactions.append({
            "timestamp": datetime.now().isoformat(),
            "prompt_tokens": prompt_tokens,
            "response_tokens": response_tokens,
            "total_tokens": total_tokens,
            "cost": cost
        })

        return {
            "prompt_tokens": prompt_tokens,
            "response_tokens": response_tokens,
            "total_tokens": total_tokens,
            "cost": cost
        }

    def get_cost_summary(self):
        """Resumen de costos"""
        return {
            "total_tokens": self.tokens_used,
            "total_cost": self.cost_accumulated,
            "avg_token_cost": self.cost_accumulated / max(self.tokens_used, 1),
            "interactions": len(self.interactions),
            "model": self.model
        }

    def print_summary(self):
        """Imprimir resumen en consola"""
        summary = self.get_cost_summary()
        print("\n" + "="*50)
        print("RESUMEN DE TOKENS Y COSTOS")
        print("="*50)
        print(f"Modelo: {summary['model']}")
        print(f"Total de tokens usados: {summary['total_tokens']}")
        print(f"Total de costo: ${summary['total_cost']:.4f}")
        print(f"Costo promedio por token: ${summary['avg_token_cost']:.6f}")
        print(f"Total de interacciones: {summary['interactions']}")
        print("="*50 + "\n")


def main():
    """Demostración del Token Manager"""
    print("Demostración: Token Manager")
    print("-" * 50)

    # Crear gestor de tokens
    manager = TokenManager(model="mistral", pricing_per_1k=0.0)  # Ollama es gratis

    # Simular algunas interacciones
    interactions = [
        {
            "prompt": "¿Qué es Python?",
            "response": "Python es un lenguaje de programación de alto nivel, interpretado y dinámico."
        },
        {
            "prompt": "Explica qué es machine learning",
            "response": "Machine learning es una rama de la inteligencia artificial que permite a las máquinas aprender de los datos sin ser programadas explícitamente."
        },
        {
            "prompt": "Dame 5 mejores prácticas en Python",
            "response": "1. Usar type hints\n2. Escribir docstrings\n3. Mantener funciones pequeñas\n4. Usar context managers\n5. Escribir tests unitarios"
        }
    ]

    for interaction in interactions:
        print(f"\nPrompt: {interaction['prompt']}")
        print(f"Response: {interaction['response'][:50]}...")

        stats = manager.record_interaction(
            interaction['prompt'],
            interaction['response']
        )
        print(f"Tokens usados: {stats['total_tokens']}")
        print(f"Costo: ${stats['cost']:.6f}")

    # Mostrar resumen final
    manager.print_summary()


if __name__ == "__main__":
    main()
