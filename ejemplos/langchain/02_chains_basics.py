#!/usr/bin/env python3
"""
02_chains_basics.py - Cadenas básicas y LCEL

Demuestra:
- Construcción de cadenas con LCEL
- Composición de múltiples componentes
- RunnableLambda para funciones personalizadas
- RunnableParallel para procesamiento paralelo
"""

from datetime import datetime
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel


def ejemplo_cadena_simple():
    """Cadena simple: prompt -> LLM -> output"""
    print("=" * 60)
    print("EJEMPLO 1: Cadena Simple")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    # Crear template
    template = """Eres un {rol}.
Pregunta: {pregunta}"""

    prompt = PromptTemplate(
        input_variables=["rol", "pregunta"],
        template=template
    )

    # Crear cadena con LCEL
    cadena = prompt | llm

    respuesta = cadena.invoke({
        "rol": "profesor de matemáticas",
        "pregunta": "¿Cuánto es 2+2?"
    })

    print(f"\nRol: profesor de matemáticas")
    print(f"Pregunta: ¿Cuánto es 2+2?")
    print(f"Respuesta: {respuesta}\n")


def ejemplo_cadena_completa():
    """Cadena completa: prompt -> LLM -> parser"""
    print("=" * 60)
    print("EJEMPLO 2: Cadena Completa con Parser")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")
    parser = StrOutputParser()

    template = """Resuelve este problema matemático:
{problema}

Proporciona solo la respuesta numérica."""

    prompt = PromptTemplate(
        input_variables=["problema"],
        template=template
    )

    # Cadena completa
    cadena = prompt | llm | parser

    resultado = cadena.invoke({
        "problema": "Si tengo 10 manzanas y doy 3, ¿cuántas me quedan?"
    })

    print(f"\nProblema: Si tengo 10 manzanas y doy 3, ¿cuántas me quedan?")
    print(f"Respuesta: {resultado.strip()}\n")


def ejemplo_runnable_lambda():
    """Usar RunnableLambda para funciones personalizadas"""
    print("=" * 60)
    print("EJEMPLO 3: RunnableLambda (Funciones Personalizadas)")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    # Función personalizada para procesar entrada
    def procesar_entrada(texto):
        """Convierte el texto a mayúsculas y agrega metadata"""
        return {
            "texto": texto.upper(),
            "longitud": len(texto),
            "timestamp": datetime.now().isoformat()
        }

    # Función para extraer solo el texto
    def extraer_texto(datos):
        return datos["texto"]

    # Construir cadena
    template = """Parafrasea esto en una línea:
{texto}"""

    prompt = PromptTemplate(
        input_variables=["texto"],
        template=template
    )

    cadena = (
        RunnableLambda(procesar_entrada)
        | RunnableLambda(extraer_texto)
        | prompt
        | llm
    )

    resultado = cadena.invoke("Los gatos duermen mucho durante el día")

    print(f"\nTexto original: Los gatos duermen mucho durante el día")
    print(f"Paráfrasis: {resultado.strip()}\n")


def ejemplo_paralelo():
    """Ejecutar múltiples cadenas en paralelo"""
    print("=" * 60)
    print("EJEMPLO 4: Procesamiento Paralelo")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    # Cadena 1: Resumen
    template_resumen = "Resume en 20 palabras: {texto}"
    cadena_resumen = PromptTemplate(
        input_variables=["texto"],
        template=template_resumen
    ) | llm

    # Cadena 2: Extracción de palabras clave
    template_keywords = "Extrae 3 palabras clave de: {texto}"
    cadena_keywords = PromptTemplate(
        input_variables=["texto"],
        template=template_keywords
    ) | llm

    # Cadena 3: Clasificación
    template_clasificacion = "Clasifica esto por tono: {texto}"
    cadena_clasificacion = PromptTemplate(
        input_variables=["texto"],
        template=template_clasificacion
    ) | llm

    # Ejecutar en paralelo
    paralelo = RunnableParallel(
        resumen=cadena_resumen,
        palabras_clave=cadena_keywords,
        tono=cadena_clasificacion
    )

    texto = "La inteligencia artificial está revolucionando el mundo de la tecnología"

    resultado = paralelo.invoke({"texto": texto})

    print(f"\nTexto: {texto}")
    print(f"\nResultados en paralelo:")
    print(f"  Resumen: {resultado['resumen'].strip()[:60]}...")
    print(f"  Palabras clave: {resultado['palabras_clave'].strip()[:60]}...")
    print(f"  Tono: {resultado['tono'].strip()[:60]}...\n")


def ejemplo_stream():
    """Streaming de respuestas (útil para UIs)"""
    print("=" * 60)
    print("EJEMPLO 5: Streaming")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")
    parser = StrOutputParser()

    template = "¿Qué es {concepto}?"

    prompt = PromptTemplate(
        input_variables=["concepto"],
        template=template
    )

    cadena = prompt | llm | parser

    print(f"\nPregunta: ¿Qué es la programación?")
    print("Respuesta (en streaming):\n")

    # Streaming: útil para mostrar respuestas en tiempo real
    for chunk in cadena.stream({"concepto": "la programación"}):
        print(chunk, end="", flush=True)

    print("\n")


def ejemplo_condicional():
    """Lógica condicional en cadenas"""
    print("=" * 60)
    print("EJEMPLO 6: Cadenas Condicionales")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    def seleccionar_template(entrada):
        """Selecciona template según el tipo de pregunta"""
        texto = entrada.lower()
        if "cómo" in texto or "pasos" in texto:
            return {
                "pregunta": entrada,
                "tipo": "procedimiento"
            }
        elif "qué es" in texto:
            return {
                "pregunta": entrada,
                "tipo": "definición"
            }
        else:
            return {
                "pregunta": entrada,
                "tipo": "general"
            }

    # Templates diferentes según el tipo
    template_procedimiento = """Explica paso a paso cómo resolver:
{pregunta}"""

    template_definicion = """Define claramente:
{pregunta}"""

    template_general = """Responde brevemente:
{pregunta}"""

    cadena_procedimiento = PromptTemplate(
        input_variables=["pregunta"],
        template=template_procedimiento
    ) | llm

    cadena_definicion = PromptTemplate(
        input_variables=["pregunta"],
        template=template_definicion
    ) | llm

    cadena_general = PromptTemplate(
        input_variables=["pregunta"],
        template=template_general
    ) | llm

    # Función que selecciona la cadena correcta
    def ejecutar_cadena_apropiada(entrada):
        datos = seleccionar_template(entrada)
        if datos["tipo"] == "procedimiento":
            return cadena_procedimiento.invoke(datos)
        elif datos["tipo"] == "definición":
            return cadena_definicion.invoke(datos)
        else:
            return cadena_general.invoke(datos)

    preguntas = [
        "¿Cómo hago una función en Python?",
        "¿Qué es una variable?",
        "¿Me ayudas con un problema?"
    ]

    print("\nCadenas condicionales:")
    for pregunta in preguntas:
        print(f"\nPregunta: {pregunta}")
        respuesta = ejecutar_cadena_apropiada(pregunta)
        print(f"Respuesta: {respuesta.strip()[:80]}...\n")


if __name__ == "__main__":
    try:
        ejemplo_cadena_simple()
        ejemplo_cadena_completa()
        ejemplo_runnable_lambda()
        ejemplo_paralelo()
        ejemplo_stream()
        ejemplo_condicional()

        print("=" * 60)
        print("✅ Todos los ejemplos de cadenas completados")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Asegúrate de que Ollama está ejecutándose")
