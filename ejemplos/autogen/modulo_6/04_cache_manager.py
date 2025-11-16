"""
Módulo 6: Optimización y Costos
Ejemplo 4: Cache Manager - Caché en memoria con estadísticas
"""

import hashlib
from datetime import datetime


class SimpleMemoryCache:
    """Caché en memoria con TTL básico"""

    def __init__(self, max_size=1000):
        self.cache = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
        self.creation_times = {}

    def _hash_key(self, prompt):
        """Generar clave hash del prompt"""
        return hashlib.md5(prompt.encode()).hexdigest()

    def get(self, prompt):
        """Obtener del caché"""
        key = self._hash_key(prompt)
        if key in self.cache:
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        return None

    def set(self, prompt, response):
        """Guardar en caché"""
        if len(self.cache) >= self.max_size:
            # Eliminar entrada más antigua
            oldest_key = min(self.creation_times, key=self.creation_times.get)
            del self.cache[oldest_key]
            del self.creation_times[oldest_key]

        key = self._hash_key(prompt)
        self.cache[key] = response
        self.creation_times[key] = datetime.now()

    def get_stats(self):
        """Estadísticas de caché"""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate,
            "size": len(self.cache),
            "total_requests": total
        }

    def clear(self):
        """Limpiar caché"""
        self.cache.clear()
        self.creation_times.clear()
        self.hits = 0
        self.misses = 0

    def print_stats(self):
        """Imprimir estadísticas"""
        stats = self.get_stats()
        print("\n" + "="*50)
        print("ESTADÍSTICAS DE CACHÉ")
        print("="*50)
        print(f"Aciertos (Hits): {stats['hits']}")
        print(f"Fallos (Misses): {stats['misses']}")
        print(f"Tasa de acierto: {stats['hit_rate']:.1f}%")
        print(f"Elementos en caché: {stats['size']}/{self.max_size}")
        print(f"Total de solicitudes: {stats['total_requests']}")
        print("="*50 + "\n")


def main():
    """Demostración del Cache Manager"""
    print("Demostración: Simple Memory Cache")
    print("-" * 60)

    cache = SimpleMemoryCache(max_size=100)

    # Simular algunas consultas
    prompts = [
        "¿Qué es Python?",
        "Explica machine learning",
        "¿Qué es Python?",  # Repetido
        "¿Qué es Python?",  # Repetido
        "Dame 5 best practices",
        "Explica machine learning",  # Repetido
    ]

    responses = {
        "¿Qué es Python?": "Python es un lenguaje de programación de alto nivel, interpretado y dinámico.",
        "Explica machine learning": "Machine learning es una rama de la inteligencia artificial que permite a las máquinas aprender de datos.",
        "Dame 5 best practices": "1. Type hints\n2. Docstrings\n3. Funciones pequeñas\n4. Context managers\n5. Tests",
    }

    print("\n📝 Procesando consultas...\n")
    for i, prompt in enumerate(prompts, 1):
        # Intentar obtener del caché
        cached = cache.get(prompt)
        if cached:
            print(f"[{i}] ✓ CACHÉ: {prompt}")
            print(f"    Respuesta: {cached[:50]}...")
        else:
            # Generar respuesta
            response = responses.get(prompt, "Respuesta desconocida")
            cache.set(prompt, response)
            print(f"[{i}] ✗ MISS:  {prompt}")
            print(f"    Respuesta: {response[:50]}...")

    # Mostrar estadísticas
    cache.print_stats()


if __name__ == "__main__":
    main()
