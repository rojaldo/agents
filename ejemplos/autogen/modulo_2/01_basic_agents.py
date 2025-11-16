"""
Módulo 2: Fundamentos de Agentes
Ejemplo 1: Basic Agents - Creación de agentes especializados
"""

import requests
from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """Clase base para todos los agentes"""

    def __init__(self, name, base_url="http://localhost:11434", model="mistral"):
        self.name = name
        self.base_url = base_url
        self.model = model
        self.messages = []

    @abstractmethod
    def system_prompt(self):
        """Sistema de prompt específico del agente"""
        pass

    def _call_ollama(self, prompt):
        """Hacer llamada a Ollama"""
        full_prompt = self.system_prompt() + "\n\n" + prompt

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

    def respond(self, message):
        """Procesar un mensaje"""
        response = self._call_ollama(message)
        self.messages.append({"user": message, "agent": response})
        return response


class PythonExpertAgent(BaseAgent):
    """Agente experto en Python"""

    def system_prompt(self):
        return """Eres un experto en programación Python.
Tu especialidad es:
- Escritura de código limpio y eficiente
- Best practices de Python
- Debugging y optimización
- Explicaciones claras

Responde siempre con código cuando sea relevante."""


class DataAnalystAgent(BaseAgent):
    """Agente especializado en análisis de datos"""

    def system_prompt(self):
        return """Eres un experto analista de datos.
Tu especialidad es:
- Análisis exploratorio de datos
- Visualización de información
- Estadística descriptiva
- Insights y recomendaciones

Proporciona análisis estructura y accionables."""


class SecurityExpertAgent(BaseAgent):
    """Agente especializado en seguridad"""

    def system_prompt(self):
        return """Eres un experto en seguridad informática.
Tu especialidad es:
- Identificación de vulnerabilidades
- Mejores prácticas de seguridad
- Criptografía básica
- Análisis de riesgos

Enfatiza siempre la importancia de la seguridad."""


class DocumentationExpertAgent(BaseAgent):
    """Agente especializado en documentación"""

    def system_prompt(self):
        return """Eres un experto en documentación técnica.
Tu especialidad es:
- Escritura clara y concisa
- Estructura de documentos
- Ejemplos educativos
- Guías paso a paso

Documenta de forma profesional y accesible."""


def demonstrate_agent(agent, prompt):
    """Demostrar un agente respondiendo a una pregunta"""
    print(f"\n{'─'*70}")
    print(f"Agente: {agent.name}")
    print("─"*70)
    print(f"Pregunta: {prompt}")
    print("\nRespuesta:")
    print("─"*70)

    response = agent.respond(prompt)

    if response.startswith("Error"):
        print(f"❌ {response}")
        return False
    else:
        print(response[:400])
        if len(response) > 400:
            print("... (respuesta continúa)")
        print("─"*70)
        return True


def main():
    """Demostración de agentes especializados"""
    print("="*70)
    print(" MÓDULO 2: AGENTES ESPECIALIZADOS")
    print("="*70)

    # Crear agentes
    print("\n🤖 Creando agentes especializados...\n")

    agents = [
        PythonExpertAgent("Python Expert"),
        DataAnalystAgent("Data Analyst"),
        SecurityExpertAgent("Security Expert"),
        DocumentationExpertAgent("Documentation Expert")
    ]

    for agent in agents:
        print(f"  ✓ {agent.name} creado")

    # Preguntas especializadas
    questions = {
        "Python Expert": "¿Cuál es la diferencia entre una lista y una tupla en Python?",
        "Data Analyst": "¿Cuáles son los pasos principales en análisis de datos?",
        "Security Expert": "¿Qué es OWASP y cuáles son los top 10 riesgos?",
        "Documentation Expert": "¿Cuál es la estructura ideal de un README.md?"
    }

    print("\n" + "="*70)
    print("DEMOSTRACIONES DE AGENTES")
    print("="*70)

    success_count = 0
    for agent in agents:
        question = questions[agent.name]
        if demonstrate_agent(agent, question):
            success_count += 1
        else:
            print("\n⚠️  Ollama no está disponible")
            print("Para usar este ejemplo:")
            print("1. Instala Ollama: https://ollama.ai")
            print("2. Ejecuta: ollama serve")
            print("3. Descarga un modelo: ollama pull mistral")
            return

    # Resumen
    print("\n" + "="*70)
    print("RESUMEN")
    print("="*70)
    print(f"Total de agentes: {len(agents)}")
    print(f"Agentes exitosos: {success_count}/{len(agents)}")

    print("\nEspecialidades:")
    for agent in agents:
        print(f"  • {agent.name}: {len(agent.messages)} interacciones")

    print("="*70 + "\n")


if __name__ == "__main__":
    main()
