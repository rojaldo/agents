"""
Módulo 8: Optimización y Performance
Ejemplo 1: Caching, batch processing y escalabilidad
"""

from datetime import datetime
from typing import Dict, List
import hashlib


class RequestCache:
    """Cache simple para optimizar requests"""

    def __init__(self, max_size: int = 100):
        self.cache = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0

    def get_key(self, **kwargs) -> str:
        """Generar clave de cache"""
        key_str = str(sorted(kwargs.items()))
        return hashlib.md5(key_str.encode()).hexdigest()

    def get(self, **kwargs):
        """Obtener del cache"""
        key = self.get_key(**kwargs)

        if key in self.cache:
            self.hits += 1
            return self.cache[key]

        self.misses += 1
        return None

    def set(self, result, **kwargs):
        """Guardar en cache"""
        if len(self.cache) >= self.max_size:
            # Eliminar entrada más antigua
            oldest_key = min(self.cache.keys())
            del self.cache[oldest_key]

        key = self.get_key(**kwargs)
        self.cache[key] = result

    def get_stats(self) -> Dict:
        """Obtener estadísticas de cache"""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0

        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate:.1f}%",
            "size": len(self.cache),
            "max_size": self.max_size
        }


class BatchProcessor:
    """Procesador de batch para optimizar throughput"""

    def __init__(self, batch_size: int = 10):
        self.batch_size = batch_size
        self.queue = []
        self.processed = 0

    def add_item(self, item):
        """Agregar item a la cola"""
        self.queue.append(item)

    def process_batch(self) -> List:
        """Procesar batch completo"""
        if len(self.queue) < self.batch_size:
            return []

        batch = self.queue[:self.batch_size]
        self.queue = self.queue[self.batch_size:]
        self.processed += len(batch)

        return batch

    def get_stats(self) -> Dict:
        """Obtener estadísticas"""
        return {
            "processed": self.processed,
            "queue_size": len(self.queue),
            "batch_size": self.batch_size
        }


class TokenOptimizer:
    """Optimiza uso de tokens en llamadas a LLM"""

    def __init__(self):
        self.token_usage = 0
        self.cost_per_1k = 0.015  # Costo por 1000 tokens

    def estimate_tokens(self, text: str) -> int:
        """Estimar tokens en texto"""
        # Aproximación: 4 caracteres = 1 token
        return len(text) // 4

    def optimize_prompt(self, prompt: str) -> str:
        """Optimizar prompt para reducir tokens"""
        # Eliminar espacios innecesarios
        optimized = " ".join(prompt.split())
        return optimized

    def calculate_cost(self, tokens: int) -> float:
        """Calcular costo de tokens"""
        return (tokens / 1000) * self.cost_per_1k

    def get_stats(self) -> Dict:
        """Obtener estadísticas de tokens"""
        return {
            "total_tokens": self.token_usage,
            "cost": f"${self.calculate_cost(self.token_usage):.2f}",
            "cost_per_1k": self.cost_per_1k
        }


class PerformanceMonitor:
    """Monitorea performance del sistema"""

    def __init__(self):
        self.metrics = []
        self.start_time = datetime.now()

    def record_metric(self, name: str, value: float, unit: str = "ms"):
        """Registrar métrica"""
        metric = {
            "name": name,
            "value": value,
            "unit": unit,
            "timestamp": datetime.now().isoformat()
        }
        self.metrics.append(metric)

    def get_average(self, metric_name: str) -> float:
        """Calcular promedio de métrica"""
        matching = [m["value"] for m in self.metrics if m["name"] == metric_name]
        if not matching:
            return 0
        return sum(matching) / len(matching)

    def print_report(self):
        """Imprimir reporte de performance"""
        print("\n📊 REPORTE DE PERFORMANCE\n")

        metric_names = set(m["name"] for m in self.metrics)

        for name in metric_names:
            avg = self.get_average(name)
            print(f"  {name}: {avg:.2f} ms")

        # Uptime
        uptime = (datetime.now() - self.start_time).total_seconds()
        print(f"  Uptime: {uptime:.1f}s")


def main():
    """Demostración de optimización y performance"""
    print("="*70)
    print(" MÓDULO 8: OPTIMIZACIÓN Y PERFORMANCE")
    print("="*70)

    # Cache
    print("\n💾 SISTEMA DE CACHE\n")

    cache = RequestCache(max_size=20)

    # Simular requests
    queries = ["IA", "machine learning", "IA", "python", "IA"]

    for query in queries:
        result = cache.get(query=query)
        if result is None:
            result = f"Resultado para {query}"
            cache.set(result, query=query)
            print(f"  MISS: {query}")
        else:
            print(f"  HIT: {query}")

    cache_stats = cache.get_stats()
    print(f"\n  Estadísticas: {cache_stats['hit_rate']} hit rate")

    # Batch processing
    print("\n📦 BATCH PROCESSING\n")

    batch = BatchProcessor(batch_size=5)

    items = [f"item_{i}" for i in range(12)]
    for item in items:
        batch.add_item(item)

    processed = batch.process_batch()
    print(f"  Batch procesado: {len(processed)} items")
    print(f"  Queue remaining: {len(batch.queue)} items")

    batch_stats = batch.get_stats()
    print(f"  Total procesado: {batch_stats['processed']}")

    # Token optimization
    print("\n🔤 OPTIMIZACIÓN DE TOKENS\n")

    optimizer = TokenOptimizer()

    original_prompt = "Este es un prompt muy largo con   espacios    innecesarios"
    optimized_prompt = optimizer.optimize_prompt(original_prompt)

    original_tokens = optimizer.estimate_tokens(original_prompt)
    optimized_tokens = optimizer.estimate_tokens(optimized_prompt)

    print(f"  Original: {original_tokens} tokens (${optimizer.calculate_cost(original_tokens):.4f})")
    print(f"  Optimizado: {optimized_tokens} tokens (${optimizer.calculate_cost(optimized_tokens):.4f})")
    print(f"  Ahorro: {original_tokens - optimized_tokens} tokens")

    # Performance monitoring
    print("\n⚡ MONITOREO DE PERFORMANCE\n")

    monitor = PerformanceMonitor()

    # Simular métricas
    monitor.record_metric("LLM Response Time", 245.5)
    monitor.record_metric("Cache Lookup", 0.5)
    monitor.record_metric("LLM Response Time", 250.2)
    monitor.record_metric("Database Query", 45.3)
    monitor.record_metric("LLM Response Time", 248.1)

    monitor.print_report()

    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
