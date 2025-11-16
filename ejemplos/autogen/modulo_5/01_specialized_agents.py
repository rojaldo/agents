"""
Módulo 5: Agentes Especializados
Ejemplo 1: Specialized Agents - Agentes con roles específicos
"""

import requests
from datetime import datetime


class SpecializedAgent:
    """Agente base especializado"""

    def __init__(self, name, role, base_url="http://localhost:11434", model="mistral"):
        self.name = name
        self.role = role
        self.base_url = base_url
        self.model = model
        self.expertise = []
        self.interactions = []

    def _call_ollama(self, prompt):
        """Hacer llamada a Ollama"""
        full_prompt = f"Eres un {self.role}.\n\n{prompt}"

        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "temperature": 0.7,
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

        except requests.exceptions.ConnectionError:
            return "Error: Ollama no disponible"
        except Exception as e:
            return f"Error: {str(e)}"

    def perform_task(self, task):
        """Realizar una tarea especializada"""
        response = self._call_ollama(task)

        self.interactions.append({
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "response": response
        })

        return response

    def get_info(self):
        """Obtener información del agente"""
        return {
            "name": self.name,
            "role": self.role,
            "interactions": len(self.interactions),
            "expertise": self.expertise
        }

    def print_info(self):
        """Imprimir información"""
        print(f"\n{self.name}")
        print(f"Rol: {self.role}")
        print(f"Interacciones: {len(self.interactions)}")
        if self.expertise:
            print(f"Especialidades: {', '.join(self.expertise)}")


class CodeReviewAgent(SpecializedAgent):
    """Agente especializado en revisión de código"""

    def __init__(self, **kwargs):
        super().__init__("Code Reviewer", "experto en revisión de código", **kwargs)
        self.expertise = ["Calidad de código", "Performance", "Seguridad", "Best practices"]

    def review_code(self, code):
        """Revisar código"""
        task = f"Revisa este código y sugiere mejoras:\n```python\n{code}\n```"
        return self.perform_task(task)


class DocumentationAgent(SpecializedAgent):
    """Agente especializado en documentación"""

    def __init__(self, **kwargs):
        super().__init__("Documentation Expert", "experto en documentación técnica", **kwargs)
        self.expertise = ["README", "API docs", "Tutoriales", "Guías"]

    def create_documentation(self, code, context):
        """Crear documentación"""
        task = f"Crea documentación para este código:\n{code}\n\nContexto: {context}"
        return self.perform_task(task)


class TestingAgent(SpecializedAgent):
    """Agente especializado en testing"""

    def __init__(self, **kwargs):
        super().__init__("Testing Expert", "experto en testing y QA", **kwargs)
        self.expertise = ["Unit tests", "Integration tests", "Test coverage", "Debugging"]

    def generate_tests(self, code):
        """Generar tests"""
        task = f"Genera tests unitarios completos para este código:\n```python\n{code}\n```"
        return self.perform_task(task)


class SecurityAgent(SpecializedAgent):
    """Agente especializado en seguridad"""

    def __init__(self, **kwargs):
        super().__init__("Security Expert", "experto en seguridad informática", **kwargs)
        self.expertise = ["Vulnerabilities", "Best practices", "Encryption", "Authentication"]

    def security_audit(self, code):
        """Auditoría de seguridad"""
        task = f"Realiza una auditoría de seguridad de este código:\n```python\n{code}\n```"
        return self.perform_task(task)


class Team:
    """Equipo de agentes especializados"""

    def __init__(self):
        self.agents = []

    def add_agent(self, agent):
        """Agregar agente al equipo"""
        self.agents.append(agent)

    def get_agent_by_name(self, name):
        """Obtener agente por nombre"""
        for agent in self.agents:
            if agent.name == name:
                return agent
        return None

    def get_team_stats(self):
        """Obtener estadísticas del equipo"""
        return {
            "total_agents": len(self.agents),
            "agents": [agent.get_info() for agent in self.agents],
            "total_interactions": sum(len(a.interactions) for a in self.agents)
        }

    def print_team_info(self):
        """Imprimir información del equipo"""
        print(f"\n{'═'*70}")
        print("EQUIPO DE AGENTES ESPECIALIZADOS")
        print("="*70)

        for agent in self.agents:
            agent.print_info()

        stats = self.get_team_stats()
        print(f"\nTotal de interacciones del equipo: {stats['total_interactions']}")
        print("="*70 + "\n")


def main():
    """Demostración de agentes especializados"""
    print("="*70)
    print(" MÓDULO 5: AGENTES ESPECIALIZADOS")
    print("="*70)

    # Crear equipo
    team = Team()

    # Agregar agentes
    print("\n🤖 Creando equipo de agentes especializados...\n")

    agents = [
        CodeReviewAgent(),
        DocumentationAgent(),
        TestingAgent(),
        SecurityAgent()
    ]

    for agent in agents:
        team.add_agent(agent)
        print(f"  ✓ {agent.name} agregado")

    # Código de prueba
    sample_code = """
def calculate_sum(numbers):
    total = 0
    for n in numbers:
        total += n
    return total

result = calculate_sum([1, 2, 3, 4, 5])
print(result)
"""

    print(f"\nCódigo para analizar:")
    print("-"*70)
    print(sample_code)
    print("-"*70)

    # Cada agente realiza su tarea
    print(f"\n{'═'*70}")
    print("ANÁLISIS POR AGENTES")
    print("="*70)

    # Code Reviewer
    print(f"\n[1] Code Reviewer")
    print("-"*70)
    review = team.get_agent_by_name("Code Reviewer").review_code(sample_code)

    if review.startswith("Error"):
        print(f"❌ {review}")
        print("\nPara usar este ejemplo:")
        print("1. Instala Ollama: https://ollama.ai")
        print("2. Ejecuta: ollama serve")
        print("3. Descarga un modelo: ollama pull mistral")
        return
    else:
        print(f"Revisión:\n{review[:200]}...\n")

    # Documentation Agent
    print(f"[2] Documentation Expert")
    print("-"*70)
    docs = team.get_agent_by_name("Documentation Expert").create_documentation(
        sample_code, "Función para sumar números"
    )

    if not docs.startswith("Error"):
        print(f"Documentación:\n{docs[:200]}...\n")

    # Testing Agent
    print(f"[3] Testing Expert")
    print("-"*70)
    tests = team.get_agent_by_name("Testing Expert").generate_tests(sample_code)

    if not tests.startswith("Error"):
        print(f"Tests:\n{tests[:200]}...\n")

    # Security Agent
    print(f"[4] Security Expert")
    print("-"*70)
    security = team.get_agent_by_name("Security Expert").security_audit(sample_code)

    if not security.startswith("Error"):
        print(f"Auditoría de seguridad:\n{security[:200]}...\n")

    # Mostrar estadísticas
    team.print_team_info()


if __name__ == "__main__":
    main()
