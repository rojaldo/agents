"""
Módulo 4: Integraciones y Herramientas
Ejemplo 1: Integración con APIs y herramientas externas
"""

from datetime import datetime
from typing import Dict, List, Any


class APIComponent:
    """Componente para llamadas a APIs"""

    def __init__(self, name: str, base_url: str):
        self.name = name
        self.base_url = base_url
        self.calls_made = 0
        self.results = []

    def call(self, endpoint: str, params: Dict = None) -> Dict:
        """Realizar llamada a API"""
        self.calls_made += 1

        # Simular respuesta
        result = {
            "endpoint": endpoint,
            "url": f"{self.base_url}/{endpoint}",
            "params": params,
            "status": 200,
            "timestamp": datetime.now().isoformat()
        }

        self.results.append(result)
        return result


class SearchTool:
    """Herramienta de búsqueda web"""

    def __init__(self):
        self.name = "WebSearch"
        self.searches = 0

    def search(self, query: str) -> List[Dict]:
        """Buscar en web"""
        self.searches += 1

        # Simular resultados de búsqueda
        results = [
            {
                "title": f"Resultado 1 sobre {query}",
                "url": "https://example1.com",
                "snippet": f"Información relevante sobre {query}..."
            },
            {
                "title": f"Resultado 2 sobre {query}",
                "url": "https://example2.com",
                "snippet": f"Más información sobre {query}..."
            },
            {
                "title": f"Resultado 3 sobre {query}",
                "url": "https://example3.com",
                "snippet": f"Artículo relacionado con {query}..."
            }
        ]

        return results


class DatabaseComponent:
    """Componente de conexión a base de datos"""

    def __init__(self, db_type: str):
        self.db_type = db_type
        self.connected = False
        self.queries_executed = 0
        self.data_store = {
            "users": ["Alice", "Bob", "Charlie"],
            "products": ["Producto A", "Producto B", "Producto C"]
        }

    def connect(self) -> bool:
        """Conectar a BD"""
        self.connected = True
        return True

    def query(self, sql: str) -> List[Dict]:
        """Ejecutar query"""
        if not self.connected:
            return {"error": "No conectado"}

        self.queries_executed += 1

        # Simular resultados
        table = "users" if "user" in sql.lower() else "products"
        return [{"id": i, "name": item} for i, item in enumerate(self.data_store.get(table, []))]

    def insert(self, table: str, data: Dict) -> bool:
        """Insertar datos"""
        if table not in self.data_store:
            self.data_store[table] = []

        self.data_store[table].append(data)
        return True


class ToolIntegrationFlow:
    """Flujo que integra múltiples herramientas"""

    def __init__(self):
        self.tools = {}
        self.integrations = []

    def add_tool(self, tool_name: str, tool):
        """Agregar herramienta"""
        self.tools[tool_name] = tool

    def integrate(self, source: str, target: str):
        """Integrar dos componentes"""
        self.integrations.append((source, target))

    def execute_search_flow(self, query: str) -> Dict:
        """Ejecutar flujo: busca en web y guarda en BD"""

        print(f"\n🔄 EJECUTANDO FLUJO DE BÚSQUEDA Y ALMACENAMIENTO\n")

        # Paso 1: Búsqueda
        print("[1] BÚSQUEDA WEB")
        search_tool = self.tools.get("search")
        results = search_tool.search(query)
        print(f"    Resultados encontrados: {len(results)}")

        # Paso 2: Almacenar en BD
        print("\n[2] ALMACENAMIENTO EN BD")
        db = self.tools.get("database")
        db.connect()

        for i, result in enumerate(results, 1):
            db.insert("search_results", {
                "id": i,
                "title": result["title"],
                "url": result["url"]
            })
            print(f"    ✓ Guardado resultado {i}")

        # Paso 3: Recuperar de BD
        print("\n[3] RECUPERACIÓN DE BD")
        stored = db.query("SELECT * FROM search_results")
        print(f"    Total de resultados almacenados: {len(stored)}")

        return {
            "query": query,
            "search_results": len(results),
            "stored_results": len(stored),
            "flow_status": "completed"
        }

    def execute_api_flow(self, endpoint: str) -> Dict:
        """Ejecutar flujo: llamada a API"""

        print(f"\n🔄 EJECUTANDO FLUJO DE API\n")

        api = self.tools.get("api")
        response = api.call(endpoint, {"query": "test"})

        print(f"[1] LLAMADA A API")
        print(f"    Endpoint: {response['endpoint']}")
        print(f"    Status: {response['status']}")
        print(f"    Total de llamadas: {api.calls_made}")

        return response

    def print_integration_report(self):
        """Imprimir reporte de integraciones"""
        print("\n" + "="*70)
        print("REPORTE DE INTEGRACIONES")
        print("="*70 + "\n")

        print("🔧 Herramientas Integradas:\n")
        for tool_name, tool in self.tools.items():
            print(f"  • {tool_name.upper()}")
            if hasattr(tool, "calls_made"):
                print(f"    Llamadas: {tool.calls_made}")
            if hasattr(tool, "searches"):
                print(f"    Búsquedas: {tool.searches}")
            if hasattr(tool, "queries_executed"):
                print(f"    Queries: {tool.queries_executed}")
            print()


def main():
    """Demostración de integraciones"""
    print("="*70)
    print(" MÓDULO 4: INTEGRACIONES Y HERRAMIENTAS")
    print("="*70)

    # Crear flujo
    flow = ToolIntegrationFlow()

    # Agregar herramientas
    print("\n🔧 AGREGANDO HERRAMIENTAS\n")

    search = SearchTool()
    flow.add_tool("search", search)
    print("  ✓ WebSearch agregado")

    api = APIComponent("OpenWeatherAPI", "https://api.openweathermap.org")
    flow.add_tool("api", api)
    print("  ✓ API agregado")

    db = DatabaseComponent("PostgreSQL")
    flow.add_tool("database", db)
    print("  ✓ Database agregado")

    # Integrar componentes
    print("\n🔗 INTEGRANDO COMPONENTES\n")

    flow.integrate("SearchTool", "DatabaseComponent")
    flow.integrate("APIComponent", "DatabaseComponent")
    print("  ✓ Integraciones establecidas")

    # Ejecutar flujos
    print("\n" + "="*70)
    search_result = flow.execute_search_flow("Inteligencia Artificial")

    print("\n" + "="*70)
    api_result = flow.execute_api_flow("weather")

    # Reporte
    flow.print_integration_report()

    print("="*70 + "\n")


if __name__ == "__main__":
    main()
