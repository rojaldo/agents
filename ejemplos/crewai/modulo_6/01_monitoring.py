"""
Módulo 6: Monitoreo y Debugging
Ejemplo 1: Logging y observabilidad en CrewAI
"""

from datetime import datetime
import json


class CrewLogger:
    """Logger para monitorear ejecución de crews"""

    def __init__(self, verbose=True):
        self.verbose = verbose
        self.logs = []
        self.execution_trace = []

    def log_task_start(self, task_name, agent_name):
        """Registrar inicio de tarea"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "task_start",
            "task": task_name,
            "agent": agent_name
        }
        self.logs.append(log_entry)
        self.execution_trace.append(log_entry)

        if self.verbose:
            print(f"[TASK START] {task_name} - {agent_name}")

    def log_task_end(self, task_name, status, output_length=0):
        """Registrar fin de tarea"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "task_end",
            "task": task_name,
            "status": status,
            "output_length": output_length
        }
        self.logs.append(log_entry)
        self.execution_trace.append(log_entry)

        if self.verbose:
            print(f"[TASK END] {task_name} - Status: {status}")

    def log_agent_thinking(self, agent_name, thought):
        """Registrar pensamiento del agente"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "agent_thinking",
            "agent": agent_name,
            "thought": thought
        }
        self.logs.append(log_entry)

        if self.verbose:
            print(f"[AGENT THINKING] {agent_name}: {thought[:50]}...")

    def log_tool_usage(self, tool_name, tool_input, tool_output):
        """Registrar uso de herramienta"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "tool_usage",
            "tool": tool_name,
            "input": str(tool_input)[:100],
            "output": str(tool_output)[:100]
        }
        self.logs.append(log_entry)

        if self.verbose:
            print(f"[TOOL] {tool_name} - Input: {str(tool_input)[:50]}...")

    def log_error(self, error_message, context=""):
        """Registrar error"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "error",
            "message": error_message,
            "context": context
        }
        self.logs.append(log_entry)
        self.execution_trace.append(log_entry)

        if self.verbose:
            print(f"[ERROR] {error_message}")

    def get_execution_summary(self):
        """Obtener resumen de ejecución"""
        task_starts = len([l for l in self.logs if l["event"] == "task_start"])
        task_ends = len([l for l in self.logs if l["event"] == "task_end"])
        tool_uses = len([l for l in self.logs if l["event"] == "tool_usage"])
        errors = len([l for l in self.logs if l["event"] == "error"])

        return {
            "total_logs": len(self.logs),
            "tasks_started": task_starts,
            "tasks_completed": task_ends,
            "tools_used": tool_uses,
            "errors": errors,
            "duration": "N/A"
        }

    def export_logs(self, filename):
        """Exportar logs a JSON"""
        with open(filename, 'w') as f:
            json.dump(self.logs, f, indent=2)

    def print_report(self):
        """Imprimir reporte de monitoreo"""
        summary = self.get_execution_summary()

        print("\n" + "="*70)
        print("REPORTE DE MONITOREO Y DEBUGGING")
        print("="*70)

        print(f"\n📊 Resumen de Ejecución:")
        print(f"   Total de logs: {summary['total_logs']}")
        print(f"   Tareas iniciadas: {summary['tasks_started']}")
        print(f"   Tareas completadas: {summary['tasks_completed']}")
        print(f"   Herramientas usadas: {summary['tools_used']}")
        print(f"   Errores: {summary['errors']}")

        print(f"\n📋 Últimos 5 eventos:")
        for i, log in enumerate(self.logs[-5:], 1):
            print(f"   {i}. [{log['event']}] {log.get('task', log.get('agent', 'N/A'))}")

        print("\n" + "="*70 + "\n")


def main():
    """Demostración de monitoreo y debugging"""
    print("="*70)
    print(" MÓDULO 6: MONITOREO Y DEBUGGING")
    print("="*70)

    # Crear logger
    logger = CrewLogger(verbose=True)

    print("\n🔍 Simulando ejecución de crew...\n")

    # Simular ejecución
    logger.log_task_start("research_task", "Investigador")
    logger.log_agent_thinking("Investigador", "Necesito buscar información sobre IA")
    logger.log_tool_usage("search_tool", {"query": "IA 2024"}, {"results": 50})
    logger.log_task_end("research_task", "completed", 1500)

    logger.log_task_start("analysis_task", "Analista")
    logger.log_agent_thinking("Analista", "Analizaré los hallazgos")
    logger.log_tool_usage("data_analyzer", {"data": "[1,2,3...]"}, {"mean": 2.5})
    logger.log_task_end("analysis_task", "completed", 800)

    logger.log_task_start("reporting_task", "Reportero")
    logger.log_agent_thinking("Reportero", "Sintetizaré los resultados")
    logger.log_task_end("reporting_task", "completed", 2000)

    # Mostrar reporte
    logger.print_report()

    # Exportar logs
    logger.export_logs("crew_execution.json")
    print("✓ Logs exportados a: crew_execution.json\n")


if __name__ == "__main__":
    main()
