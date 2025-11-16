"""
Módulo 6: Exportación y Deployment
Ejemplo 1: Exportar flows como APIs
"""

import json
from datetime import datetime
from typing import Dict, List


class FlowExporter:
    """Exporta flows Langflow a diferentes formatos"""

    def __init__(self, flow_name: str):
        self.flow_name = flow_name
        self.components = []
        self.connections = []
        self.metadata = {
            "name": flow_name,
            "created": datetime.now().isoformat(),
            "version": "1.0"
        }

    def add_component(self, comp_dict: Dict):
        """Agregar componente al flujo"""
        self.components.append(comp_dict)

    def add_connection(self, source: str, target: str):
        """Agregar conexión"""
        self.connections.append({"source": source, "target": target})

    def export_as_json(self) -> str:
        """Exportar como JSON"""
        export_data = {
            "metadata": self.metadata,
            "components": self.components,
            "connections": self.connections
        }
        return json.dumps(export_data, indent=2)

    def export_as_python_api(self) -> str:
        """Exportar como código Python FastAPI"""

        api_code = f'''
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="{self.flow_name}")

class InputData(BaseModel):
    input: str

class OutputData(BaseModel):
    output: str

@app.post("/run", response_model=OutputData)
async def run_flow(data: InputData):
    """Ejecutar flujo {self.flow_name}"""
    # Componente 1
    result = process_input(data.input)

    # Componente 2
    result = process_with_llm(result)

    # Componente 3
    output = format_output(result)

    return OutputData(output=output)

@app.get("/health")
async def health_check():
    return {{"status": "healthy"}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''

        return api_code

    def export_as_docker(self) -> str:
        """Exportar como Dockerfile"""

        dockerfile = f'''
FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "api.py"]
'''

        return dockerfile

    def export_as_webhook(self) -> str:
        """Exportar como webhook"""

        webhook_code = f'''
import requests
from typing import Dict

class {self.flow_name}Webhook:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def trigger(self, data: Dict) -> Dict:
        """Trigger el webhook"""
        response = requests.post(self.webhook_url, json=data)
        return response.json()

    def callback(self, event_data: Dict):
        """Procesar callback del webhook"""
        print(f"Webhook recibido: {{event_data}}")
'''

        return webhook_code


class DeploymentManager:
    """Gestiona deployment de flows"""

    def __init__(self):
        self.deployments = []
        self.environments = ["development", "staging", "production"]

    def create_deployment(self, flow_name: str, environment: str) -> Dict:
        """Crear un deployment"""

        deployment = {
            "id": len(self.deployments) + 1,
            "flow_name": flow_name,
            "environment": environment,
            "status": "pending",
            "url": f"https://{flow_name}-{environment}.langflow.app",
            "created": datetime.now().isoformat()
        }

        self.deployments.append(deployment)
        return deployment

    def get_deployment_status(self, deployment_id: int) -> Dict:
        """Obtener estado de deployment"""

        for dep in self.deployments:
            if dep["id"] == deployment_id:
                return {
                    "id": dep["id"],
                    "status": "active",
                    "uptime": "99.9%",
                    "requests": 10245,
                    "avg_latency": "245ms"
                }

        return {"error": "Deployment no encontrado"}

    def print_deployments(self):
        """Imprimir deployments"""

        print("\n🚀 DEPLOYMENTS ACTIVOS\n")

        for dep in self.deployments:
            print(f"  • {dep['flow_name']} ({dep['environment']})")
            print(f"    URL: {dep['url']}")
            print(f"    Status: {dep['status']}")
            print()


def main():
    """Demostración de exportación y deployment"""
    print("="*70)
    print(" MÓDULO 6: EXPORTACIÓN Y DEPLOYMENT")
    print("="*70)

    # Crear flujo
    exporter = FlowExporter("MiChatbot")

    # Agregar componentes
    print("\n🔧 CONFIGURANDO FLUJO\n")

    exporter.add_component({"name": "ChatInput", "type": "input"})
    exporter.add_component({"name": "ChatOpenAI", "type": "llm"})
    exporter.add_component({"name": "ChatOutput", "type": "output"})

    print("  ✓ Componentes agregados")

    # Agregar conexiones
    exporter.add_connection("ChatInput", "ChatOpenAI")
    exporter.add_connection("ChatOpenAI", "ChatOutput")

    print("  ✓ Conexiones establecidas")

    # Exportar formatos
    print("\n📦 EXPORTANDO FORMATOS\n")

    # JSON
    json_export = exporter.export_as_json()
    print("  ✓ JSON")
    print(f"    Tamaño: {len(json_export)} bytes")

    # Python API
    python_api = exporter.export_as_python_api()
    print("  ✓ Python FastAPI")
    print(f"    Líneas de código: {len(python_api.split(chr(10)))}")

    # Docker
    dockerfile = exporter.export_as_docker()
    print("  ✓ Dockerfile")

    # Webhook
    webhook = exporter.export_as_webhook()
    print("  ✓ Webhook")

    # Deployment manager
    print("\n" + "="*70)
    print("DEPLOYING AL CLOUD")
    print("="*70 + "\n")

    manager = DeploymentManager()

    for env in ["development", "staging"]:
        deployment = manager.create_deployment("MiChatbot", env)
        print(f"  ✓ Deployment a {env}: {deployment['url']}")

    manager.print_deployments()

    print("="*70 + "\n")


if __name__ == "__main__":
    main()
