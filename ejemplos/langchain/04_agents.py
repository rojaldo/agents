#!/usr/bin/env python3
"""
04_agents.py - Agentes con herramientas

Demuestra:
- Crear herramientas con @tool
- Crear agentes ReAct
- AgentExecutor con configuración
- Agentes con memoria
"""

import json
from typing import Optional
from langchain_community.llms import Ollama
from langchain_core.tools import tool, BaseTool
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field


# ============ DEFINICIÓN DE HERRAMIENTAS ============

@tool
def sumar(a: int, b: int) -> int:
    """Suma dos números.

    Args:
        a: Primer número
        b: Segundo número
    """
    return a + b


@tool
def multiplicar(a: int, b: int) -> int:
    """Multiplica dos números.

    Args:
        a: Primer número
        b: Segundo número
    """
    return a * b


@tool
def obtener_informacion_pais(pais: str) -> str:
    """Obtiene información sobre un país.

    Args:
        pais: Nombre del país
    """
    informacion = {
        "España": "Capital: Madrid, Población: 47 millones, Idioma: Español",
        "Francia": "Capital: París, Población: 67 millones, Idioma: Francés",
        "Italia": "Capital: Roma, Población: 59 millones, Idioma: Italiano",
        "Japón": "Capital: Tokio, Población: 125 millones, Idioma: Japonés",
    }
    return informacion.get(pais, f"No hay información sobre {pais}")


@tool
def buscar_en_wikipedia(termino: str) -> str:
    """Busca un término (simulado).

    Args:
        termino: Término a buscar
    """
    # Simulación de búsqueda
    terminos = {
        "inteligencia artificial": "La IA es el campo de estudio que busca crear máquinas inteligentes",
        "python": "Python es un lenguaje de programación interpretado",
        "langchain": "LangChain es un framework para aplicaciones LLM",
    }
    return terminos.get(termino.lower(), f"No encontré información sobre '{termino}'")


# ============ HERRAMIENTA PERSONALIZADA ============

class CalculadoraAvanzada(BaseTool):
    """Herramienta personalizada para operaciones matemáticas avanzadas"""

    name = "calculadora_avanzada"
    description = "Realiza operaciones matemáticas avanzadas"

    class ConfigSchema(BaseModel):
        operacion: str = Field(description="Tipo de operación: potencia, raiz, factorial")
        numero: float = Field(description="Número para la operación")

    args_schema = ConfigSchema

    def _run(self, operacion: str, numero: float) -> str:
        """Ejecutar operación"""
        try:
            if operacion.lower() == "potencia":
                resultado = numero ** 2
                return f"{numero}² = {resultado}"
            elif operacion.lower() == "raiz":
                resultado = numero ** 0.5
                return f"√{numero} = {resultado:.2f}"
            elif operacion.lower() == "factorial":
                import math
                resultado = math.factorial(int(numero))
                return f"{int(numero)}! = {resultado}"
            else:
                return f"Operación no soportada: {operacion}"
        except Exception as e:
            return f"Error en cálculo: {str(e)}"

    async def _arun(self, operacion: str, numero: float) -> str:
        """Versión asincrónica"""
        return self._run(operacion, numero)


# ============ EJEMPLOS ============

def ejemplo_agente_basico():
    """Agente simple con herramientas básicas"""
    print("=" * 60)
    print("EJEMPLO 1: Agente Básico con Herramientas")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    # Definir herramientas
    herramientas = [sumar, multiplicar]

    # Crear agente
    prompt_template = """Responde la siguiente pregunta usando las herramientas disponibles.

Tienes acceso a estas herramientas:
{tools}

Usa este formato exacto:
Thought: Tu razonamiento
Action: El nombre de la herramienta
Action Input: Los parámetros JSON para la herramienta
Observation: El resultado
... (repite Thought/Action/Observation si necesitas más pasos)
Final Answer: La respuesta final

Pregunta: {input}"""

    prompt = PromptTemplate.from_template(prompt_template)

    agente = create_react_agent(llm, herramientas, prompt)
    executor = AgentExecutor(
        agent=agente,
        tools=herramientas,
        verbose=False,
        max_iterations=5,
        handle_parsing_errors=True
    )

    # Ejecutar
    print("\nPregunta: ¿Cuánto es 15 multiplicado por 3?")
    resultado = executor.invoke({"input": "¿Cuánto es 15 multiplicado por 3?"})
    print(f"Respuesta: {resultado['output']}\n")


def ejemplo_agente_informacion():
    """Agente que busca y proporciona información"""
    print("=" * 60)
    print("EJEMPLO 2: Agente Buscador de Información")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    herramientas = [obtener_informacion_pais, buscar_en_wikipedia]

    prompt = PromptTemplate.from_template("""
Responde estas preguntas usando las herramientas disponibles.

Herramientas:
{tools}

Formato:
Thought: [Tu razonamiento]
Action: [Nombre de herramienta]
Action Input: [Parámetros JSON]
Observation: [Resultado]

Pregunta: {input}
""")

    agente = create_react_agent(llm, herramientas, prompt)
    executor = AgentExecutor(agent=agente, tools=herramientas, verbose=False, max_iterations=5)

    # Probar
    preguntas = [
        "¿Cuál es la capital de España?",
        "¿Qué es Python?"
    ]

    for pregunta in preguntas:
        print(f"\nPregunta: {pregunta}")
        try:
            resultado = executor.invoke({"input": pregunta})
            print(f"Respuesta: {resultado['output']}\n")
        except Exception as e:
            print(f"Error: {e}\n")


def ejemplo_agente_completo():
    """Agente con múltiples tipos de herramientas"""
    print("=" * 60)
    print("EJEMPLO 3: Agente Completo Multi-Herramientas")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    # Combinar herramientas
    herramientas = [
        sumar,
        multiplicar,
        obtener_informacion_pais,
        buscar_en_wikipedia,
        CalculadoraAvanzada()
    ]

    prompt = PromptTemplate.from_template("""
Eres un asistente útil que puede usar herramientas para ayudar.

Herramientas disponibles:
{tools}

Sigue este formato:
Thought: [Razonamiento]
Action: [Herramienta]
Action Input: [Parámetros en JSON]
Observation: [Resultado]
... (repite si necesitas más)
Final Answer: [Tu respuesta final]

Pregunta: {input}""")

    agente = create_react_agent(llm, herramientas, prompt)
    executor = AgentExecutor(
        agent=agente,
        tools=herramientas,
        verbose=False,
        max_iterations=8
    )

    # Tareas
    tareas = [
        "¿Cuánto es 20 + 5?",
        "Dame información sobre Italia",
        "¿Cuál es la raíz cuadrada de 16?",
    ]

    for tarea in tareas:
        print(f"\n📋 Tarea: {tarea}")
        try:
            resultado = executor.invoke({"input": tarea})
            print(f"✓ Resultado: {resultado['output']}\n")
        except Exception as e:
            print(f"✗ Error: {str(e)[:100]}\n")


def ejemplo_configuracion_agente():
    """Demostrar diferentes configuraciones del AgentExecutor"""
    print("=" * 60)
    print("EJEMPLO 4: Configuración del Agente")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")
    herramientas = [sumar, multiplicar]

    prompt = PromptTemplate.from_template("""
{tools}
{input}""")

    agente = create_react_agent(llm, herramientas, prompt)

    print("\nConfiguraciones de AgentExecutor:")

    # Configuración 1: Máximo de iteraciones bajo
    print("\n1️⃣  max_iterations=3 (limite bajo, puede no encontrar respuesta)")
    executor1 = AgentExecutor(
        agent=agente,
        tools=herramientas,
        verbose=False,
        max_iterations=3
    )

    # Configuración 2: Manejo de errores
    print("2️⃣  handle_parsing_errors=True (más tolerante con errores)")
    executor2 = AgentExecutor(
        agent=agente,
        tools=herramientas,
        verbose=False,
        handle_parsing_errors=True
    )

    # Configuración 3: Detención temprana
    print("3️⃣  early_stopping_method='force' (detiene al exceder iteraciones)")
    executor3 = AgentExecutor(
        agent=agente,
        tools=herramientas,
        verbose=False,
        early_stopping_method="force",
        max_iterations=5
    )

    print("\n✓ Las configuraciones afectan cómo el agente maneja:")
    print("  - Número máximo de intentos")
    print("  - Manejo de errores de parseo")
    print("  - Estrategia de detención")


def ejemplo_flujo_agente():
    """Mostrar el flujo de pensamiento del agente"""
    print("\n" + "=" * 60)
    print("EJEMPLO 5: Flujo de Razonamiento del Agente")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")
    herramientas = [sumar, multiplicar]

    prompt = PromptTemplate.from_template("""
{tools}
{input}""")

    agente = create_react_agent(llm, herramientas, prompt)
    executor = AgentExecutor(agent=agente, tools=herramientas, verbose=True, max_iterations=5)

    print("\nEjecutando con verbose=True para ver el razonamiento:")
    print("-" * 60)

    try:
        resultado = executor.invoke({"input": "¿Cuánto es (10 + 5) * 2?"})
        print("-" * 60)
        print(f"Resultado final: {resultado['output']}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    try:
        ejemplo_agente_basico()
        ejemplo_agente_informacion()
        ejemplo_agente_completo()
        ejemplo_configuracion_agente()

        # Descomenta para ver flujo detallado (verbose)
        # ejemplo_flujo_agente()

        print("\n" + "=" * 60)
        print("✅ Todos los ejemplos de agentes completados")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Asegúrate de que Ollama está ejecutándose")
        import traceback
        traceback.print_exc()
