"""
Módulo 6: Optimización y Costos
Ejemplo 7: Real Time Monitor - Monitoreo en tiempo real de tokens y costos
"""

from datetime import datetime
from collections import defaultdict


class RealTimeTokenMonitor:
    """Monitoreo en tiempo real de tokens, costos y presupuesto"""

    def __init__(self, budget_limit=100.0):
        self.budget_limit = budget_limit
        self.transactions = []
        self.usage_by_agent = defaultdict(lambda: {"tokens": 0, "cost": 0, "calls": 0})
        self.hourly_stats = defaultdict(lambda: {"tokens": 0, "cost": 0, "calls": 0})
        self.start_time = datetime.now()

    def log_transaction(self, agent_name, tokens, cost, task_type="general"):
        """Registrar transacción de tokens"""
        timestamp = datetime.now()
        hour_key = timestamp.strftime("%Y-%m-%d %H:00")

        # Registrar transacción
        self.transactions.append({
            "agent": agent_name,
            "tokens": tokens,
            "cost": cost,
            "timestamp": timestamp,
            "task_type": task_type
        })

        # Actualizar estadísticas por agente
        self.usage_by_agent[agent_name]["tokens"] += tokens
        self.usage_by_agent[agent_name]["cost"] += cost
        self.usage_by_agent[agent_name]["calls"] += 1

        # Actualizar estadísticas por hora
        self.hourly_stats[hour_key]["tokens"] += tokens
        self.hourly_stats[hour_key]["cost"] += cost
        self.hourly_stats[hour_key]["calls"] += 1

    def get_budget_status(self):
        """Estado del presupuesto"""
        total_cost = sum(u["cost"] for u in self.usage_by_agent.values())
        remaining = self.budget_limit - total_cost
        percentage = (total_cost / self.budget_limit) * 100 if self.budget_limit > 0 else 0

        return {
            "budget_limit": self.budget_limit,
            "spent": total_cost,
            "remaining": remaining,
            "percentage_used": percentage,
            "within_budget": remaining >= 0,
            "status": "✓ OK" if remaining >= 0 else "⚠️  EXCEDIDO"
        }

    def get_agent_ranking(self):
        """Ranking de agentes por consumo"""
        return sorted(
            self.usage_by_agent.items(),
            key=lambda x: x[1]["cost"],
            reverse=True
        )

    def get_hourly_stats(self):
        """Estadísticas por hora"""
        return dict(sorted(self.hourly_stats.items()))

    def get_task_breakdown(self):
        """Desglose por tipo de tarea"""
        task_stats = defaultdict(lambda: {"tokens": 0, "cost": 0, "calls": 0})

        for transaction in self.transactions:
            task_type = transaction.get("task_type", "general")
            task_stats[task_type]["tokens"] += transaction["tokens"]
            task_stats[task_type]["cost"] += transaction["cost"]
            task_stats[task_type]["calls"] += 1

        return dict(task_stats)

    def get_total_stats(self):
        """Estadísticas totales"""
        total_tokens = sum(u["tokens"] for u in self.usage_by_agent.values())
        total_cost = sum(u["cost"] for u in self.usage_by_agent.values())
        total_calls = sum(u["calls"] for u in self.usage_by_agent.values())
        avg_tokens_per_call = total_tokens / total_calls if total_calls > 0 else 0
        avg_cost_per_call = total_cost / total_calls if total_calls > 0 else 0

        return {
            "total_tokens": total_tokens,
            "total_cost": total_cost,
            "total_calls": total_calls,
            "avg_tokens_per_call": avg_tokens_per_call,
            "avg_cost_per_call": avg_cost_per_call,
            "uptime": datetime.now() - self.start_time
        }

    def check_budget_alerts(self):
        """Verificar alertas de presupuesto"""
        status = self.get_budget_status()
        alerts = []

        if status["percentage_used"] > 80:
            alerts.append(f"⚠️  Presupuesto al {status['percentage_used']:.1f}%")

        if status["percentage_used"] > 100:
            alerts.append("🔴 PRESUPUESTO EXCEDIDO")

        return alerts

    def print_comprehensive_report(self):
        """Imprimir reporte completo"""
        print("\n" + "="*70)
        print("REPORTE DE MONITOREO EN TIEMPO REAL")
        print("="*70)

        # Resumen general
        total_stats = self.get_total_stats()
        print("\n📊 RESUMEN GENERAL")
        print("-"*70)
        print(f"Total de tokens: {total_stats['total_tokens']}")
        print(f"Total de costo: ${total_stats['total_cost']:.4f}")
        print(f"Total de llamadas: {total_stats['total_calls']}")
        print(f"Promedio tokens/llamada: {total_stats['avg_tokens_per_call']:.1f}")
        print(f"Promedio costo/llamada: ${total_stats['avg_cost_per_call']:.6f}")
        print(f"Tiempo de ejecución: {total_stats['uptime']}")

        # Estado del presupuesto
        budget = self.get_budget_status()
        print("\n💰 ESTADO DEL PRESUPUESTO")
        print("-"*70)
        print(f"Límite: ${budget['budget_limit']:.2f}")
        print(f"Gastado: ${budget['spent']:.4f}")
        print(f"Restante: ${budget['remaining']:.4f}")
        print(f"Porcentaje usado: {budget['percentage_used']:.1f}%")
        print(f"Estado: {budget['status']}")

        # Alertas
        alerts = self.check_budget_alerts()
        if alerts:
            print("\n🔔 ALERTAS")
            print("-"*70)
            for alert in alerts:
                print(f"  {alert}")

        # Ranking de agentes
        ranking = self.get_agent_ranking()
        if ranking:
            print("\n🤖 RANKING DE AGENTES (por costo)")
            print("-"*70)
            for i, (agent_name, stats) in enumerate(ranking, 1):
                print(f"{i}. {agent_name}")
                print(f"   Llamadas: {stats['calls']}, Tokens: {stats['tokens']}, Costo: ${stats['cost']:.6f}")

        # Desglose por tarea
        task_breakdown = self.get_task_breakdown()
        if task_breakdown:
            print("\n📋 DESGLOSE POR TIPO DE TAREA")
            print("-"*70)
            for task_type, stats in task_breakdown.items():
                print(f"{task_type}: {stats['calls']} llamadas, {stats['tokens']} tokens, ${stats['cost']:.6f}")

        print("\n" + "="*70 + "\n")


def main():
    """Demostración del Monitor de Tiempo Real"""
    print("Demostración: Real Time Token Monitor")
    print("-" * 60)

    # Crear monitor con presupuesto
    monitor = RealTimeTokenMonitor(budget_limit=10.0)

    print(f"\n💼 Monitor iniciado con presupuesto de $10.00\n")

    # Simular algunas transacciones
    transactions = [
        ("CodeReviewAgent", 150, 0.0015, "code"),
        ("CodeReviewAgent", 200, 0.0020, "code"),
        ("AnalysisAgent", 300, 0.0030, "analysis"),
        ("DataAgent", 250, 0.0025, "analysis"),
        ("CodeReviewAgent", 180, 0.0018, "code"),
        ("GeneralAgent", 120, 0.0012, "general"),
        ("DataAgent", 400, 0.0040, "analysis"),
    ]

    print("📝 Registrando transacciones...\n")
    for i, (agent, tokens, cost, task_type) in enumerate(transactions, 1):
        monitor.log_transaction(agent, tokens, cost, task_type)
        budget = monitor.get_budget_status()
        print(f"[{i}] {agent:20s} | Tokens: {tokens:3d} | Costo: ${cost:.6f} | Presupuesto: {budget['percentage_used']:.1f}%")

    # Mostrar reporte completo
    monitor.print_comprehensive_report()


if __name__ == "__main__":
    main()
