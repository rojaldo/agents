#!/usr/bin/env python3
"""
01_basic_llm.py - Ejemplo básico de uso de LangChain con Ollama

Este ejemplo demuestra:
- Inicializar un modelo Ollama
- Crear prompts simples
- Invocar el modelo
- Usar output parsers básicos
"""

from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


def ejemplo_basico():
    """Ejemplo más simple posible"""
    print("=" * 60)
    print("EJEMPLO 1: LLM Básico")
    print("=" * 60)

    # Crear instancia del modelo
    llm = Ollama(
        model="mistral",
        base_url="http://localhost:11434",
        temperature=0.7,
    )

    # Ejecutar consulta simple
    respuesta = llm.invoke("¿Qué es un LLM en una línea?")
    print(f"\nPregunta: ¿Qué es un LLM en una línea?")
    print(f"Respuesta: {respuesta}\n")


def ejemplo_con_template():
    """Usar prompts con templates"""
    print("=" * 60)
    print("EJEMPLO 2: Prompts con Templates")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    # Crear template
    template = """Eres un {rol} experto.
Pregunta: {pregunta}
Respuesta breve:"""

    prompt = PromptTemplate(
        input_variables=["rol", "pregunta"],
        template=template
    )

    # Invocar con parámetros
    respuesta = llm.invoke(prompt.format(
        rol="profesor de Python",
        pregunta="¿Qué es un decorador?"
    ))

    print(f"\nRol: Profesor de Python")
    print(f"Pregunta: ¿Qué es un decorador?")
    print(f"Respuesta: {respuesta}\n")


def ejemplo_con_parser():
    """Usar output parsers"""
    print("=" * 60)
    print("EJEMPLO 3: Output Parsers")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")
    parser = StrOutputParser()

    # El parser simplemente devuelve el string tal cual
    respuesta = llm.invoke("Dame 3 números aleatorios")
    resultado_parseado = parser.parse(respuesta)

    print(f"\nPregunta: Dame 3 números aleatorios")
    print(f"Respuesta parseada: {resultado_parseado}\n")


def ejemplo_lcel():
    """Usar LCEL (LangChain Expression Language)"""
    print("=" * 60)
    print("EJEMPLO 4: LCEL (LangChain Expression Language)")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    template = """Traduce al {idioma}:
{texto}"""

    prompt = PromptTemplate(
        input_variables=["idioma", "texto"],
        template=template
    )

    parser = StrOutputParser()

    # Composición con LCEL (operador pipe |)
    cadena = prompt | llm | parser

    resultado = cadena.invoke({
        "idioma": "francés",
        "texto": "Hola, ¿cómo estás?"
    })

    print(f"\nTexto original: Hola, ¿cómo estás?")
    print(f"Idioma destino: Francés")
    print(f"Traducción: {resultado}\n")


def ejemplo_batch():
    """Procesar múltiples inputs en batch"""
    print("=" * 60)
    print("EJEMPLO 5: Batch Processing")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    template = "¿Cuál es la capital de {pais}?"
    prompt = PromptTemplate(
        input_variables=["pais"],
        template=template
    )

    cadena = prompt | llm

    # Procesar múltiples inputs
    paises = [
        {"pais": "Francia"},
        {"pais": "Japón"},
        {"pais": "Brasil"}
    ]

    resultados = cadena.batch(paises)

    print("\nProcesamiento en batch:")
    for pais, resultado in zip(paises, resultados):
        print(f"  {pais['pais']}: {resultado.strip()[:60]}...")


def ejemplo_configuracion():
    """Demostrar diferentes configuraciones de temperatura"""
    print("\n" + "=" * 60)
    print("EJEMPLO 6: Configuración de Parámetros")
    print("=" * 60)

    # Temperatura baja = más determinista
    llm_determinista = Ollama(
        model="mistral",
        base_url="http://localhost:11434",
        temperature=0.0,
    )

    # Temperatura alta = más creativo
    llm_creativo = Ollama(
        model="mistral",
        base_url="http://localhost:11434",
        temperature=0.9,
    )

    prompt = "Escribe una palabra aleatoria"

    print(f"\nCon temperatura=0.0 (determinista):")
    print(f"  {llm_determinista.invoke(prompt).strip()[:50]}...")

    print(f"\nCon temperatura=0.9 (creativo):")
    print(f"  {llm_creativo.invoke(prompt).strip()[:50]}...")


if __name__ == "__main__":
    try:
        ejemplo_basico()
        ejemplo_con_template()
        ejemplo_con_parser()
        ejemplo_lcel()
        ejemplo_batch()
        ejemplo_configuracion()

        print("\n" + "=" * 60)
        print("✅ Todos los ejemplos completados correctamente")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("¿Está Ollama ejecutándose en http://localhost:11434?")
