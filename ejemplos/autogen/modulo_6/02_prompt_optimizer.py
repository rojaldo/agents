"""
Módulo 6: Optimización y Costos
Ejemplo 2: Prompt Optimizer - Optimización de prompts para reducir tokens
"""


class PromptOptimizer:
    """Optimizador de prompts para reducir tokens"""

    def __init__(self):
        """Inicializar optimizer"""
        self.original_prompts = []
        self.optimized_prompts = []

    def estimate_tokens(self, text):
        """Estimar tokens (1 token ≈ 4 caracteres)"""
        return max(1, len(text) // 4)

    def count_tokens(self, text):
        """Contar tokens de un texto"""
        return self.estimate_tokens(text)

    def remove_redundancy(self, prompt):
        """Eliminar palabras redundantes"""
        redundant_words = [
            "por favor", "porfavor", "gracias", "thank you",
            "muy", "realmente", "verdaderamente", "bastante"
        ]

        optimized = prompt
        for word in redundant_words:
            optimized = optimized.replace(word + " ", "").replace(" " + word, "")

        return optimized

    def compress_prompt(self, prompt, target_reduction=20):
        """Comprimir prompt manteniendo semántica"""
        # Paso 1: Remover redundancias
        compressed = self.remove_redundancy(prompt)

        # Paso 2: Convertir a minúsculas cuando sea posible
        compressed = compressed.strip()

        # Paso 3: Eliminar espacios múltiples
        compressed = " ".join(compressed.split())

        # Paso 4: Si aún es muy largo, tomar solo las primeras oraciones
        sentences = compressed.split(".")
        original_tokens = self.count_tokens(prompt)
        target_tokens = original_tokens - (original_tokens * target_reduction // 100)

        result = []
        for sentence in sentences:
            result.append(sentence.strip())
            if self.count_tokens(". ".join(result)) >= target_tokens:
                result.pop()
                break

        if result:
            compressed = ". ".join(result) + "."
        else:
            compressed = sentences[0] + "."

        return compressed

    def suggest_improvements(self, prompt):
        """Sugerir mejoras para reducir tokens"""
        suggestions = []
        token_count = self.count_tokens(prompt)
        word_count = len(prompt.split())

        if word_count > 100:
            suggestions.append("✓ El prompt es muy largo. Intente ser más conciso.")

        if prompt.count("\n\n") > 3:
            suggestions.append("✓ Demasiados saltos de línea. Considere agrupar párrafos.")

        if "por favor" in prompt.lower() or "gracias" in prompt.lower():
            suggestions.append("✓ Palabras de cortesía innecesarias. Pueden ser eliminadas.")

        if prompt.count(" a ") > 5 or prompt.count(" el ") > 5:
            suggestions.append("✓ Artículos repetidos. Intente escribir de forma más directa.")

        return {
            "tokens": token_count,
            "words": word_count,
            "character_count": len(prompt),
            "suggestions": suggestions
        }


def main():
    """Demostración del Prompt Optimizer"""
    print("Demostración: Prompt Optimizer")
    print("-" * 60)

    optimizer = PromptOptimizer()

    # Ejemplo 1: Prompt largo
    prompt1 = """
    Por favor, necesito que analices este código Python muy cuidadosamente.
    Gracias de antemano. Quiero que revises si hay errores, y realmente
    espero que puedas ayudarme a mejorar la calidad del código.
    El código es bastante importante para mi proyecto.
    """

    print("\n📝 EJEMPLO 1: Prompt Largo")
    print("Original:")
    print(prompt1)
    print(f"Tokens originales: {optimizer.count_tokens(prompt1)}")

    compressed = optimizer.compress_prompt(prompt1)
    print("\nOptimizado:")
    print(compressed)
    print(f"Tokens optimizados: {optimizer.count_tokens(compressed)}")

    original_tokens = optimizer.count_tokens(prompt1)
    optimized_tokens = optimizer.count_tokens(compressed)
    reduction = ((original_tokens - optimized_tokens) / original_tokens) * 100
    print(f"Reducción: {reduction:.1f}%")

    # Ejemplo 2: Análisis de mejoras
    print("\n" + "="*60)
    print("📋 ANÁLISIS DE MEJORAS")
    print("="*60)

    suggestions = optimizer.suggest_improvements(prompt1)
    print(f"\nTokens: {suggestions['tokens']}")
    print(f"Palabras: {suggestions['words']}")
    print(f"Caracteres: {suggestions['character_count']}")
    print("\nSugerencias:")
    for suggestion in suggestions['suggestions']:
        print(f"  {suggestion}")

    # Ejemplo 3: Comparación múltiple
    print("\n" + "="*60)
    print("📊 COMPARACIÓN DE PROMPTS")
    print("="*60)

    prompts = [
        "¿Qué es Python?",
        "Por favor, dime qué es Python. Gracias.",
        "Necesito que me expliques, con mucho detalle, qué es el lenguaje de programación Python.",
    ]

    for i, p in enumerate(prompts, 1):
        tokens = optimizer.count_tokens(p)
        compressed = optimizer.compress_prompt(p, target_reduction=15)
        compressed_tokens = optimizer.count_tokens(compressed)
        print(f"\nPrompt {i}:")
        print(f"  Original ({tokens} tokens): {p}")
        print(f"  Optimizado ({compressed_tokens} tokens): {compressed}")


if __name__ == "__main__":
    main()
