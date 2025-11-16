"""
Módulo 6: Optimización y Costos
Ejemplo 8: Cost Optimizer - Estrategia de caché con preferencia de modelos
"""

import hashlib
from datetime import datetime


class SimpleCacheStrategy:
    """Estrategia de caché simple sin dependencias externas"""

    def __init__(self):
        self.cache = {}
        self.hits = 0
        self.misses = 0

    def _hash_key(self, prompt):
        """Generar clave del prompt"""
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
        key = self._hash_key(prompt)
        self.cache[key] = response

    def get_stats(self):
        """Estadísticas"""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate
        }


class MultiModelCostOptimizer:
    """Optimizador de costos con estrategia de caché y modelos locales"""

    def __init__(self):
        self.cache = SimpleCacheStrategy()
        self.model_preferences = {
            "code": {
                "local": "mistral",
                "weight": 0.8,
                "local_cost": 0.0,
                "api_cost": 0.002
            },
            "analysis": {
                "local": "llama2",
                "weight": 0.7,
                "local_cost": 0.0,
                "api_cost": 0.001
            },
            "general": {
                "local": "neural-chat",
                "weight": 0.75,
                "local_cost": 0.0,
                "api_cost": 0.001
            }
        }
        self.total_cost_saved = 0.0
        self.usage_log = []

    def estimate_api_cost(self, prompt):
        """Estimar costo en API"""
        # Aproximación: 1 token ≈ 4 caracteres, $0.001 por 1000 tokens
        tokens = len(prompt) // 4
        return (tokens / 1000) * 0.001

    def get_or_generate(self, prompt, task_type="general"):
        """Obtener del caché o marcar para generar localmente"""
        # Buscar en caché
        cached = self.cache.get(prompt)
        if cached:
            # Calcular ahorro
            api_cost = self.estimate_api_cost(prompt)
            self.total_cost_saved += api_cost
            self.usage_log.append({
                "prompt": prompt[:50] + "...",
                "source": "cache",
                "cost_saved": api_cost,
                "timestamp": datetime.now()
            })
            return cached, "cache", api_cost

        # Seleccionar modelo local
        model_config = self.model_preferences.get(task_type, self.model_preferences["general"])
        model = model_config["local"]
        local_cost = model_config["local_cost"]
        api_cost = self.estimate_api_cost(prompt)
        cost_savings = api_cost - local_cost

        self.usage_log.append({
            "prompt": prompt[:50] + "...",
            "source": "local_model",
            "model": model,
            "cost_saved": cost_savings,
            "timestamp": datetime.now()
        })

        self.total_cost_saved += cost_savings

        return None, model, cost_savings

    def get_cost_comparison(self, prompt, task_type="general"):
        """Comparar costos: API vs Local vs Cache"""
        api_cost = self.estimate_api_cost(prompt)
        cache_hit = self.cache.get(prompt)

        model_config = self.model_preferences.get(task_type, self.model_preferences["general"])
        local_cost = model_config["local_cost"]
        local_model = model_config["local"]

        comparison = {
            "prompt": prompt[:50] + "...",
            "api_cost": api_cost,
            "local_cost": local_cost,
            "cache_available": cache_hit is not None,
            "best_option": "cache" if cache_hit else "local",
            "potential_savings": api_cost - local_cost if not cache_hit else api_cost
        }

        return comparison

    def optimize_query_batch(self, queries, task_type="general"):
        """Optimizar un lote de consultas"""
        results = []
        total_api_cost = 0.0
        total_local_cost = 0.0
        cache_hits = 0

        for query in queries:
            comparison = self.get_cost_comparison(query, task_type)
            results.append(comparison)

            api_cost = comparison["api_cost"]
            local_cost = comparison["local_cost"]

            total_api_cost += api_cost
            total_local_cost += local_cost

            if comparison["cache_available"]:
                cache_hits += 1

        return {
            "queries_processed": len(queries),
            "cache_hits": cache_hits,
            "total_api_cost": total_api_cost,
            "total_local_cost": total_local_cost,
            "potential_savings": total_api_cost - total_local_cost,
            "results": results
        }

    def print_optimization_report(self):
        """Imprimir reporte de optimización"""
        cache_stats = self.cache.get_stats()

        print("\n" + "="*70)
        print("REPORTE DE OPTIMIZACIÓN DE COSTOS")
        print("="*70)

        print("\n📊 ESTADÍSTICAS DE CACHÉ")
        print("-"*70)
        print(f"Aciertos (Hits): {cache_stats['hits']}")
        print(f"Fallos (Misses): {cache_stats['misses']}")
        print(f"Tasa de acierto: {cache_stats['hit_rate']:.1f}%")

        print("\n💰 AHORROS TOTALES")
        print("-"*70)
        print(f"Costo total ahorrado: ${self.total_cost_saved:.4f}")
        print(f"Transacciones registradas: {len(self.usage_log)}")

        if self.usage_log:
            print("\n📋 ÚLTIMAS TRANSACCIONES")
            print("-"*70)
            for i, log in enumerate(self.usage_log[-5:], 1):
                print(f"{i}. {log['prompt']}")
                print(f"   Fuente: {log['source']}, Ahorro: ${log['cost_saved']:.6f}")

        print("\n✅ RECOMENDACIONES")
        print("-"*70)
        if cache_stats['hit_rate'] < 30:
            print("• Aumentar tamaño de caché - tasa de acierto baja")
        else:
            print("• Caché funcionando bien")

        print("• Usar modelos locales para reducir costos en APIs")
        print("• Reutilizar prompts comunes para maximizar caché")

        print("\n" + "="*70 + "\n")


def main():
    """Demostración del Cost Optimizer"""
    print("Demostración: Multi-Model Cost Optimizer")
    print("-" * 60)

    optimizer = MultiModelCostOptimizer()

    # Simular consultas
    queries = [
        ("¿Qué es Python?", "general"),
        ("Escribe un programa en Python", "code"),
        ("Analiza estos datos", "analysis"),
        ("¿Qué es Python?", "general"),  # Repetido
        ("Dame 3 best practices", "code"),
        ("Explica la estadística", "analysis"),
        ("¿Qué es Python?", "general"),  # Repetido de nuevo
    ]

    print("\n📝 Procesando consultas...\n")

    for i, (query, task_type) in enumerate(queries, 1):
        result, source, savings = optimizer.get_or_generate(query, task_type)

        if source == "cache":
            print(f"[{i}] ✓ CACHÉ: {query[:40]}")
            print(f"     Ahorro: ${savings:.6f}")
        else:
            print(f"[{i}] 🔄 LOCAL: {query[:40]}")
            print(f"     Modelo: {source}, Ahorro: ${savings:.6f}")

        # Guardar en caché si no está
        optimizer.cache.set(query, f"Respuesta a: {query}")

    # Optimizar lote
    print("\n" + "="*60)
    print("Analizando lote de optimización...")

    batch_queries = [
        "¿Qué es machine learning?",
        "¿Cómo funcionan las redes neuronales?",
        "¿Qué es deep learning?",
    ]

    batch_result = optimizer.optimize_query_batch(batch_queries, "analysis")
    print(f"\nConsultas procesadas: {batch_result['queries_processed']}")
    print(f"Costo total con API: ${batch_result['total_api_cost']:.4f}")
    print(f"Costo total con local: ${batch_result['total_local_cost']:.4f}")
    print(f"Ahorro potencial: ${batch_result['potential_savings']:.4f}")

    # Reporte
    optimizer.print_optimization_report()


if __name__ == "__main__":
    main()
