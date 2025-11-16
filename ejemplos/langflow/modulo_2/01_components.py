"""
Módulo 2: Conceptos Fundamentales
Ejemplo 1: Tipos de componentes y conexiones
"""

from datetime import datetime
from typing import Dict, List, Any


class ComponentLibrary:
    """Librería de componentes disponibles en Langflow"""

    def __init__(self):
        self.components = {
            "LLM": {
                "ChatOpenAI": "OpenAI chat models",
                "Claude": "Anthropic Claude",
                "Llama": "Meta Llama models",
                "Mistral": "Mistral models"
            },
            "Tools": {
                "GoogleSearch": "Search on Google",
                "Wikipedia": "Wikipedia lookup",
                "Calculator": "Math operations",
                "HTTPRequest": "Make HTTP calls"
            },
            "Data": {
                "CSVLoader": "Load CSV files",
                "TextSplitter": "Split documents",
                "Embeddings": "Generate embeddings",
                "JSONParser": "Parse JSON"
            },
            "Memory": {
                "ConversationMemory": "Chat history",
                "ConversationSummaryMemory": "Summarized history",
                "VectorStoreMemory": "Vector based memory"
            },
            "Output": {
                "ChatOutput": "Chat interface",
                "FileOutput": "Save to file",
                "WebhookOutput": "Send to webhook",
                "DatabaseOutput": "Save to DB"
            }
        }

    def list_by_category(self, category: str) -> Dict:
        """Listar componentes por categoría"""
        return self.components.get(category, {})

    def get_all_categories(self) -> List[str]:
        """Obtener todas las categorías"""
        return list(self.components.keys())

    def print_library(self):
        """Imprimir librería completa"""
        print("\n📚 LIBRERÍA DE COMPONENTES LANGFLOW\n")

        for category, components in self.components.items():
            print(f"📦 {category}:")
            for comp_name, description in components.items():
                print(f"   • {comp_name}: {description}")
            print()


class Connection:
    """Representa una conexión entre componentes"""

    def __init__(self, source: str, source_output: str, target: str, target_input: str):
        self.source = source
        self.source_output = source_output
        self.target = target
        self.target_input = target_input
        self.created_at = datetime.now()

    def __str__(self):
        return f"{self.source}.{self.source_output} → {self.target}.{self.target_input}"


class FlowValidator:
    """Valida la estructura de un flujo"""

    @staticmethod
    def validate_connection(source_type: str, target_type: str) -> tuple:
        """Validar si una conexión es válida"""

        valid_connections = {
            "ChatOpenAI": ["ChatOutput", "TextSplitter", "Calculator"],
            "GoogleSearch": ["ChatOpenAI", "ChatOutput", "TextSplitter"],
            "TextSplitter": ["Embeddings", "ChatOpenAI"],
            "Embeddings": ["VectorStoreMemory", "DatabaseOutput"]
        }

        if source_type in valid_connections:
            if target_type in valid_connections[source_type]:
                return True, "Conexión válida"
            else:
                return False, f"{source_type} no puede conectar a {target_type}"
        else:
            return False, f"{source_type} no tiene outputs definidos"

    @staticmethod
    def validate_flow(components: List[str], connections: List[Connection]) -> tuple:
        """Validar un flujo completo"""

        # Verificar que hay al menos entrada y salida
        has_input = any("Input" in comp for comp in components)
        has_output = any("Output" in comp for comp in components)

        if not has_input:
            return False, "Falta componente de entrada"
        if not has_output:
            return False, "Falta componente de salida"

        # Verificar conexiones
        if len(connections) < len(components) - 1:
            return False, "No hay suficientes conexiones"

        return True, "Flujo válido"


class FlowAnalyzer:
    """Analiza propiedades de un flujo"""

    def __init__(self, components: List[str], connections: List[Connection]):
        self.components = components
        self.connections = connections

    def get_flow_depth(self) -> int:
        """Calcular profundidad del flujo"""
        return len(set(c.source for c in self.connections)) + 1

    def get_branches(self) -> int:
        """Contar ramificaciones del flujo"""
        source_counts = {}
        for conn in self.connections:
            source_counts[conn.source] = source_counts.get(conn.source, 0) + 1

        return sum(1 for count in source_counts.values() if count > 1)

    def get_complexity(self) -> str:
        """Evaluar complejidad del flujo"""
        depth = self.get_flow_depth()
        branches = self.get_branches()

        complexity_score = depth + (branches * 2)

        if complexity_score <= 3:
            return "Baja"
        elif complexity_score <= 6:
            return "Media"
        else:
            return "Alta"

    def print_analysis(self):
        """Imprimir análisis del flujo"""
        print("\n📊 ANÁLISIS DEL FLUJO\n")
        print(f"  Componentes: {len(self.components)}")
        print(f"  Conexiones: {len(self.connections)}")
        print(f"  Profundidad: {self.get_flow_depth()}")
        print(f"  Ramificaciones: {self.get_branches()}")
        print(f"  Complejidad: {self.get_complexity()}")


def main():
    """Demostración de componentes fundamentales"""
    print("="*70)
    print(" MÓDULO 2: CONCEPTOS FUNDAMENTALES")
    print("="*70)

    # Mostrar librería de componentes
    library = ComponentLibrary()
    library.print_library()

    # Crear un flujo de ejemplo
    print("\n🔗 CREANDO FLUJO CON CONEXIONES\n")

    components = [
        "User Input",
        "ChatOpenAI",
        "TextSplitter",
        "Embeddings",
        "VectorStoreMemory",
        "Chat Output"
    ]

    print("Componentes del flujo:")
    for i, comp in enumerate(components, 1):
        print(f"  {i}. {comp}")

    # Crear conexiones
    connections = [
        Connection("User Input", "message", "ChatOpenAI", "prompt"),
        Connection("ChatOpenAI", "response", "TextSplitter", "text"),
        Connection("TextSplitter", "chunks", "Embeddings", "texts"),
        Connection("Embeddings", "vectors", "VectorStoreMemory", "embeddings"),
        Connection("VectorStoreMemory", "context", "Chat Output", "message")
    ]

    print("\nConexiones:")
    for conn in connections:
        print(f"  → {conn}")

    # Validar flujo
    print("\n✓ VALIDACIÓN DEL FLUJO\n")

    validator = FlowValidator()
    is_valid, message = validator.validate_flow(components, connections)

    print(f"  Estado: {'✓ Válido' if is_valid else '✗ Inválido'}")
    print(f"  Mensaje: {message}")

    # Analizar flujo
    analyzer = FlowAnalyzer(components, connections)
    analyzer.print_analysis()

    # Validar conexión individual
    print("\n🔍 VALIDACIÓN DE CONEXIÓN INDIVIDUAL\n")

    test_connections = [
        ("ChatOpenAI", "TextSplitter"),
        ("TextSplitter", "Embeddings"),
        ("GoogleSearch", "ChatOpenAI")
    ]

    for source, target in test_connections:
        is_valid, msg = validator.validate_connection(source, target)
        status = "✓" if is_valid else "✗"
        print(f"  {status} {source} → {target}: {msg}")

    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
