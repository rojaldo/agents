"""
Módulo 10: Integraciones
Ejemplo 1: Framework Integration - Integración con frameworks populares
"""

import requests
from abc import ABC, abstractmethod


class LLMFramework(ABC):
    """Clase base para frameworks de LLM"""

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def query(self, prompt):
        pass


class OllamaFramework(LLMFramework):
    """Integración con Ollama"""

    def __init__(self, base_url="http://localhost:11434", model="mistral"):
        self.base_url = base_url
        self.model = model
        self.connected = False

    def setup(self):
        """Configurar conexión"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            self.connected = response.status_code == 200
            if self.connected:
                print("✓ Ollama conectado correctamente")
            else:
                print("✗ No se pudo conectar a Ollama")
        except:
            print("✗ Error conectando a Ollama")
            self.connected = False

    def query(self, prompt, temperature=0.7):
        """Realizar consulta"""
        if not self.connected:
            return "Error: Ollama no conectado"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                return response.json().get('response', '')
            else:
                return f"Error: {response.status_code}"

        except requests.exceptions.Timeout:
            return "Error: Timeout"
        except Exception as e:
            return f"Error: {str(e)}"

    def get_models(self):
        """Obtener modelos disponibles"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [m['name'] for m in data.get('models', [])]
            return []
        except:
            return []


class LangChainIntegration:
    """Integración simulada con LangChain"""

    def __init__(self, llm_framework):
        self.llm = llm_framework
        self.memory = []

    def setup_chain(self):
        """Configurar cadena de prompts"""
        self.llm.setup()
        return self.llm.connected

    def execute_chain(self, initial_prompt):
        """Ejecutar cadena de prompts"""
        results = []

        # Primer prompt
        response1 = self.llm.query(initial_prompt)
        results.append(("Initial", response1[:100]))

        # Segundo prompt basado en resultado
        follow_up = f"Basándote en: {response1[:50]}, expande este concepto"
        response2 = self.llm.query(follow_up)
        results.append(("Follow-up", response2[:100]))

        return results

    def add_memory(self, context):
        """Agregar contexto a memoria"""
        self.memory.append(context)

    def get_context(self):
        """Obtener contexto actual"""
        return "\n".join(self.memory) if self.memory else "No hay contexto"


class APIGateway:
    """Gateway para exponer agentes como API"""

    def __init__(self, framework):
        self.framework = framework
        self.endpoints = {}
        self.request_count = 0

    def register_endpoint(self, name, handler):
        """Registrar un endpoint"""
        self.endpoints[name] = handler

    def handle_request(self, endpoint_name, data):
        """Manejar solicitud"""
        self.request_count += 1

        if endpoint_name not in self.endpoints:
            return {"error": "Endpoint no encontrado"}

        handler = self.endpoints[endpoint_name]
        return handler(data)

    def get_stats(self):
        """Obtener estadísticas"""
        return {
            "total_requests": self.request_count,
            "endpoints_registered": len(self.endpoints),
            "endpoints": list(self.endpoints.keys())
        }

    def print_stats(self):
        """Imprimir estadísticas"""
        stats = self.get_stats()
        print("\n" + "="*60)
        print("API GATEWAY STATISTICS")
        print("="*60)
        print(f"Total de solicitudes: {stats['total_requests']}")
        print(f"Endpoints registrados: {stats['endpoints_registered']}")
        if stats['endpoints']:
            print(f"Endpoints disponibles:")
            for ep in stats['endpoints']:
                print(f"  - {ep}")
        print("="*60 + "\n")


def main():
    """Demostración de integraciones"""
    print("Demostración: Framework Integration")
    print("-" * 60)

    # Integración con Ollama
    print("\n🔗 INTEGRACIÓN CON OLLAMA")
    print("="*60)

    ollama = OllamaFramework()
    ollama.setup()

    if ollama.connected:
        print(f"✓ Framework Ollama listo")
        print(f"  Modelo: {ollama.model}")

        models = ollama.get_models()
        if models:
            print(f"  Modelos disponibles: {', '.join(models)}")
        else:
            print(f"  No se pudieron obtener modelos")

        # Consulta de prueba
        print(f"\n  Realizando consulta de prueba...")
        result = ollama.query("¿Qué es AutoGen?", temperature=0.5)

        if result.startswith("Error"):
            print(f"  ❌ {result}")
        else:
            print(f"  ✓ Respuesta: {result[:150]}...")
    else:
        print("❌ No se pudo conectar a Ollama")
        print("\nPara usar este ejemplo:")
        print("1. Instala Ollama: https://ollama.ai")
        print("2. Ejecuta: ollama serve")
        print("3. Descarga un modelo: ollama pull mistral")
        return

    # Integración con LangChain (simulada)
    print("\n\n🔗 INTEGRACIÓN CON LANGCHAIN (SIMULADA)")
    print("="*60)

    langchain = LangChainIntegration(ollama)
    if langchain.setup_chain():
        print("✓ LangChain chain configurada")

        # Agregar contexto
        langchain.add_memory("Contexto: AutoGen es un framework de Microsoft")

        # Ejecutar cadena
        print(f"\n  Ejecutando cadena de prompts...")
        results = langchain.execute_chain("¿Qué es AutoGen?")

        for stage, response in results:
            print(f"  [{stage}] {response}...")

    # API Gateway
    print("\n\n🔗 API GATEWAY")
    print("="*60)

    gateway = APIGateway(ollama)

    # Registrar endpoints
    gateway.register_endpoint("generate", lambda data: {"result": "Generated content"})
    gateway.register_endpoint("analyze", lambda data: {"result": "Analysis complete"})
    gateway.register_endpoint("summarize", lambda data: {"result": "Summary generated"})

    # Simular solicitudes
    print(f"✓ Gateway con 3 endpoints registrados")
    print(f"\n  Simulando solicitudes...")

    for _ in range(5):
        gateway.handle_request("generate", {})

    gateway.print_stats()


if __name__ == "__main__":
    main()
