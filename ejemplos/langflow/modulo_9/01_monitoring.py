"""
Módulo 9: Monitoreo y Debugging
Ejemplo 1: Logging, debugging y análisis de ejecución
"""

import json
from datetime import datetime
from typing import Dict, List


class FlowLogger:
    """Sistema de logging para flujos Langflow"""

    def __init__(self, flow_name: str):
        self.flow_name = flow_name
        self.logs = []
        self.execution_trace = []

    def log_component_start(self, component_name: str):
        """Registrar inicio de componente"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "component_start",
            "component": component_name
        }
        self.logs.append(log_entry)
        print(f"[START] {component_name}")

    def log_component_end(self, component_name: str, output: str):
        """Registrar fin de componente"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "component_end",
            "component": component_name,
            "output": output[:100]  # Limitar longitud
        }
        self.logs.append(log_entry)
        self.execution_trace.append(log_entry)
        print(f"[END] {component_name} → {output[:50]}...")

    def log_error(self, component_name: str, error_message: str):
        """Registrar error"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "error",
            "component": component_name,
            "error": error_message
        }
        self.logs.append(log_entry)
        print(f"[ERROR] {component_name}: {error_message}")

    def log_warning(self, message: str):
        """Registrar warning"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "warning",
            "message": message
        }
        self.logs.append(log_entry)
        print(f"[WARNING] {message}")

    def get_execution_summary(self) -> Dict:
        """Obtener resumen de ejecución"""
        starts = len([l for l in self.logs if l["event"] == "component_start"])
        ends = len([l for l in self.logs if l["event"] == "component_end"])
        errors = len([l for l in self.logs if l["event"] == "error"])

        return {
            "total_logs": len(self.logs),
            "components_started": starts,
            "components_completed": ends,
            "errors": errors,
            "warnings": len([l for l in self.logs if l["event"] == "warning"]),
            "success_rate": f"{(ends/starts*100):.1f}%" if starts > 0 else "N/A"
        }

    def export_logs(self, filename: str = "flow_logs.json"):
        """Exportar logs a JSON"""
        with open(filename, 'w') as f:
            json.dump(self.logs, f, indent=2)
        print(f"\nLogs exportados a: {filename}")

    def print_summary(self):
        """Imprimir resumen de ejecución"""
        summary = self.get_execution_summary()

        print("\n" + "="*70)
        print("RESUMEN DE EJECUCIÓN")
        print("="*70 + "\n")

        print(f"  Flow: {self.flow_name}")
        print(f"  Total de logs: {summary['total_logs']}")
        print(f"  Componentes iniciados: {summary['components_started']}")
        print(f"  Componentes completados: {summary['components_completed']}")
        print(f"  Errores: {summary['errors']}")
        print(f"  Warnings: {summary['warnings']}")
        print(f"  Tasa de éxito: {summary['success_rate']}")


class FlowDebugger:
    """Herramienta de debugging para flujos"""

    def __init__(self):
        self.breakpoints = []
        self.variables = {}
        self.call_stack = []

    def set_breakpoint(self, component_name: str):
        """Establecer breakpoint"""
        self.breakpoints.append(component_name)
        print(f"  Breakpoint establecido en: {component_name}")

    def inspect_variable(self, var_name: str, value):
        """Inspeccionar variable"""
        self.variables[var_name] = value
        print(f"  [{var_name}] = {value}")

    def push_stack(self, component_name: str):
        """Agregar a call stack"""
        self.call_stack.append({
            "component": component_name,
            "timestamp": datetime.now().isoformat()
        })

    def pop_stack(self):
        """Remover del call stack"""
        if self.call_stack:
            return self.call_stack.pop()

    def print_stack_trace(self):
        """Imprimir stack trace"""
        print("\n📍 CALL STACK\n")

        for i, frame in enumerate(self.call_stack, 1):
            print(f"  {i}. {frame['component']} @ {frame['timestamp']}")

    def print_variables(self):
        """Imprimir variables"""
        print("\n🔍 VARIABLES\n")

        for name, value in self.variables.items():
            print(f"  {name} = {value}")


class ExecutionAnalyzer:
    """Analiza ejecución de flujos"""

    def __init__(self, logs: List[Dict]):
        self.logs = logs

    def get_component_times(self) -> Dict[str, float]:
        """Calcular tiempo por componente"""
        times = {}

        for i, log in enumerate(self.logs):
            if log["event"] == "component_start":
                # Buscar fin correspondiente
                for j in range(i+1, len(self.logs)):
                    if (self.logs[j]["event"] == "component_end" and
                        self.logs[j]["component"] == log["component"]):
                        # Calcular tiempo (simulado)
                        times[log["component"]] = 0.5
                        break

        return times

    def identify_bottlenecks(self) -> List[str]:
        """Identificar cuellos de botella"""
        times = self.get_component_times()

        if not times:
            return []

        avg_time = sum(times.values()) / len(times)
        bottlenecks = [comp for comp, time in times.items() if time > avg_time * 1.5]

        return bottlenecks

    def print_analysis(self):
        """Imprimir análisis"""
        print("\n📊 ANÁLISIS DE EJECUCIÓN\n")

        times = self.get_component_times()
        print("  Tiempos por componente:")
        for comp, time in times.items():
            print(f"    {comp}: {time:.2f}ms")

        bottlenecks = self.identify_bottlenecks()
        if bottlenecks:
            print("\n  ⚠️  Cuellos de botella detectados:")
            for comp in bottlenecks:
                print(f"    • {comp}")


def main():
    """Demostración de monitoreo y debugging"""
    print("="*70)
    print(" MÓDULO 9: MONITOREO Y DEBUGGING")
    print("="*70)

    # Crear logger
    logger = FlowLogger("MiFlujoPrincipal")

    print("\n📝 EJECUTANDO FLUJO CON LOGGING\n")

    # Simular ejecución
    logger.log_component_start("ChatInput")
    logger.log_component_end("ChatInput", "¿Cuál es el significado de IA?")

    logger.log_component_start("ChatOpenAI")
    logger.log_component_end("ChatOpenAI", "La IA es inteligencia artificial...")

    logger.log_component_start("TextProcessing")
    logger.log_warning("Performance degradada")
    logger.log_component_end("TextProcessing", "Texto procesado")

    logger.log_component_start("ChatOutput")
    logger.log_component_end("ChatOutput", "Respuesta lista para enviar")

    # Resumen
    logger.print_summary()

    # Debugging
    print("\n" + "="*70)
    print("SESIÓN DE DEBUGGING")
    print("="*70 + "\n")

    debugger = FlowDebugger()

    # Establecer breakpoints
    print("🔴 ESTABLECIENDO BREAKPOINTS\n")
    debugger.set_breakpoint("ChatOpenAI")
    debugger.set_breakpoint("TextProcessing")

    # Inspeccionar variables
    print("\n🔍 INSPECCIONANDO VARIABLES\n")
    debugger.inspect_variable("user_input", "¿Cuál es el significado de IA?")
    debugger.inspect_variable("model_response", "La IA es inteligencia artificial...")
    debugger.inspect_variable("tokens_used", 125)

    # Stack trace
    debugger.push_stack("main")
    debugger.push_stack("ChatOpenAI")
    debugger.push_stack("TextProcessing")

    debugger.print_stack_trace()
    debugger.print_variables()

    # Análisis
    print("\n" + "="*70)
    analyzer = ExecutionAnalyzer(logger.logs)
    analyzer.print_analysis()

    # Exportar
    print("\n" + "="*70)
    print("EXPORTACIÓN")
    print("="*70)

    logger.export_logs()

    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
