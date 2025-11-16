"""
Módulo 6: Optimización y Costos
Ejemplo 5: Semantic Cache - Búsqueda de similitud para caché inteligente
"""

import hashlib
from datetime import datetime


class SemanticCacheSimulator:
    """
    Caché inteligente que simula búsqueda semántica sin dependencias externas.
    En producción, usaría SentenceTransformers para embeddings reales.
    """

    def __init__(self, similarity_threshold=0.8):
        self.cache = []
        self.similarity_threshold = similarity_threshold
        self.hits = 0
        self.total_queries = 0

    def _simple_similarity(self, text1, text2):
        """
        Similitud simple basada en palabras comunes (sin librerías externas).
        En producción, usar SentenceTransformers.
        """
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = len(words1 & words2)
        union = len(words1 | words2)

        # Jaccard similarity
        return intersection / union if union > 0 else 0.0

    def get(self, prompt):
        """Buscar respuesta para prompt similar"""
        self.total_queries += 1

        if not self.cache:
            return None

        best_match = None
        best_similarity = 0
        best_prompt = None

        for cached_prompt, cached_response in self.cache:
            similarity = self._simple_similarity(prompt, cached_prompt)

            if similarity > best_similarity:
                best_similarity = similarity
                best_match = cached_response
                best_prompt = cached_prompt

        if best_similarity >= self.similarity_threshold:
            self.hits += 1
            return best_match

        return None

    def set(self, prompt, response):
        """Guardar en caché"""
        self.cache.append((prompt, response))

    def get_similar_prompts(self, prompt, top_k=3):
        """Obtener prompts similares"""
        similarities = []

        for cached_prompt, _ in self.cache:
            similarity = self._simple_similarity(prompt, cached_prompt)
            similarities.append((cached_prompt, similarity))

        return sorted(
            similarities,
            key=lambda x: x[1],
            reverse=True
        )[:top_k]

    def get_stats(self):
        """Estadísticas"""
        hit_rate = (self.hits / self.total_queries * 100) if self.total_queries > 0 else 0
        return {
            "hits": self.hits,
            "total_queries": self.total_queries,
            "hit_rate": hit_rate,
            "cached_items": len(self.cache),
            "threshold": self.similarity_threshold
        }

    def print_stats(self):
        """Imprimir estadísticas"""
        stats = self.get_stats()
        print("\n" + "="*60)
        print("ESTADÍSTICAS DE CACHÉ SEMÁNTICO")
        print("="*60)
        print(f"Aciertos: {stats['hits']}")
        print(f"Total de consultas: {stats['total_queries']}")
        print(f"Tasa de acierto: {stats['hit_rate']:.1f}%")
        print(f"Elementos en caché: {stats['cached_items']}")
        print(f"Umbral de similitud: {stats['threshold']}")
        print("="*60 + "\n")


def main():
    """Demostración del Semantic Cache"""
    print("Demostración: Semantic Cache Simulator")
    print("-" * 60)

    cache = SemanticCacheSimulator(similarity_threshold=0.6)

    # Base de datos de conocimiento
    knowledge_base = {
        "¿Qué es Python?": "Python es un lenguaje de programación de alto nivel, interpretado y dinámico.",
        "¿Cuál es la sintaxis de Python?": "Python usa indentación para definir bloques de código.",
        "¿Cómo instalar librerías en Python?": "Usa: pip install nombre_libreria",
    }

    # Cargar base de conocimiento en caché
    print("\n📚 Cargando base de conocimiento en caché...")
    for prompt, response in knowledge_base.items():
        cache.set(prompt, response)
    print(f"✓ {len(knowledge_base)} elementos cargados")

    # Consultas de prueba
    test_queries = [
        ("¿Qué es Python?", True),  # Exacto
        ("Cuéntame sobre Python", True),  # Similar
        ("¿Cómo se instala una librería?", True),  # Parecido
        ("¿Cuál es la capital de Francia?", False),  # Diferente
        ("Explica la sintaxis de Python", True),  # Similar
        ("¿Cómo defino bloques en Python?", True),  # Similar
    ]

    print("\n🔍 Realizando consultas...\n")
    for i, (query, expected_match) in enumerate(test_queries, 1):
        result = cache.get(query)
        status = "✓ HIT" if result else "✗ MISS"

        print(f"[{i}] {status}: {query}")
        if result:
            print(f"    Respuesta: {result[:60]}...")
        else:
            print(f"    Sin coincidencia en caché")

        # Mostrar similares
        similar = cache.get_similar_prompts(query, top_k=2)
        if similar:
            print(f"    Prompts similares:")
            for sim_prompt, sim_score in similar:
                if sim_score > 0:
                    print(f"      - {sim_prompt[:40]}... (similitud: {sim_score:.2f})")

    # Mostrar estadísticas
    cache.print_stats()


if __name__ == "__main__":
    main()
