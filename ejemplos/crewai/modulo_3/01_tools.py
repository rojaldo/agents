"""
Módulo 3: Herramientas (Tools)
Ejemplo 1: Herramientas personalizadas
"""


class Tool:
    """Clase base para herramientas"""

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.usage_count = 0

    def execute(self, *args, **kwargs):
        """Ejecutar la herramienta"""
        self.usage_count += 1
        raise NotImplementedError

    def get_info(self):
        """Obtener información de la herramienta"""
        return {
            "name": self.name,
            "description": self.description,
            "usage_count": self.usage_count
        }


class CalculatorTool(Tool):
    """Herramienta para cálculos matemáticos"""

    def __init__(self):
        super().__init__(
            name="calculator",
            description="Realiza operaciones matemáticas básicas"
        )

    def execute(self, operation, a, b):
        """Ejecutar operación"""
        if operation == "add":
            return a + b
        elif operation == "subtract":
            return a - b
        elif operation == "multiply":
            return a * b
        elif operation == "divide":
            if b == 0:
                return "Error: División por cero"
            return a / b
        else:
            return "Operación no soportada"


class DataAnalyzerTool(Tool):
    """Herramienta para análisis de datos"""

    def __init__(self):
        super().__init__(
            name="data_analyzer",
            description="Analiza datos y calcula estadísticas"
        )

    def execute(self, numbers):
        """Analizar datos"""
        if not numbers:
            return {"error": "Lista vacía"}

        return {
            "count": len(numbers),
            "sum": sum(numbers),
            "average": sum(numbers) / len(numbers),
            "min": min(numbers),
            "max": max(numbers)
        }


class FileReaderTool(Tool):
    """Herramienta para leer archivos"""

    def __init__(self):
        super().__init__(
            name="file_reader",
            description="Lee y procesa archivos"
        )

    def execute(self, filename):
        """Leer archivo"""
        try:
            with open(filename, 'r') as f:
                content = f.read()
            return {
                "filename": filename,
                "lines": len(content.split('\n')),
                "characters": len(content),
                "preview": content[:100]
            }
        except FileNotFoundError:
            return {"error": f"Archivo no encontrado: {filename}"}


class ToolBox:
    """Caja de herramientas para un agente"""

    def __init__(self):
        self.tools = {}

    def add_tool(self, tool):
        """Agregar herramienta"""
        self.tools[tool.name] = tool

    def get_tool(self, name):
        """Obtener herramienta por nombre"""
        return self.tools.get(name)

    def list_tools(self):
        """Listar todas las herramientas"""
        return list(self.tools.values())

    def use_tool(self, tool_name, *args, **kwargs):
        """Usar una herramienta"""
        tool = self.get_tool(tool_name)
        if tool:
            return tool.execute(*args, **kwargs)
        return f"Herramienta no encontrada: {tool_name}"


def main():
    """Demostración de herramientas"""
    print("="*70)
    print(" MÓDULO 3: HERRAMIENTAS PERSONALIZADAS")
    print("="*70)

    # Crear toolbox
    print("\n🔧 Creando caja de herramientas...\n")

    toolbox = ToolBox()

    # Agregar herramientas
    calc_tool = CalculatorTool()
    toolbox.add_tool(calc_tool)
    print(f"  ✓ {calc_tool.name}: {calc_tool.description}")

    analyzer_tool = DataAnalyzerTool()
    toolbox.add_tool(analyzer_tool)
    print(f"  ✓ {analyzer_tool.name}: {analyzer_tool.description}")

    # Usar herramientas
    print("\n📊 Usando herramientas...\n")

    # Usar calculator
    print("[1] Calculator Tool")
    result1 = toolbox.use_tool("calculator", "add", 10, 5)
    print(f"  10 + 5 = {result1}")

    result2 = toolbox.use_tool("calculator", "multiply", 4, 7)
    print(f"  4 * 7 = {result2}")

    # Usar data analyzer
    print("\n[2] Data Analyzer Tool")
    data = [10, 20, 30, 40, 50]
    result3 = toolbox.use_tool("data_analyzer", data)
    print(f"  Análisis de {data}:")
    for key, value in result3.items():
        print(f"    {key}: {value}")

    # Mostrar estadísticas
    print("\n" + "="*70)
    print("ESTADÍSTICAS DE HERRAMIENTAS")
    print("="*70)

    for tool in toolbox.list_tools():
        info = tool.get_info()
        print(f"\n{tool.name}:")
        print(f"  Descripción: {info['description']}")
        print(f"  Usos: {info['usage_count']}")

    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
