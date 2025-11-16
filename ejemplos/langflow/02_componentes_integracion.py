#!/usr/bin/env python3
"""
02_componentes_integracion.py - Componentes e Integraciones

Demuestra componentes de Langflow:
- WebSearch (búsqueda web)
- HTTPRequest (llamadas a APIs)
- Text processing components
"""

from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_community.llms import Ollama
from langchain_community.tools import DuckDuckGoSearchRun
import requests
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ejemplo_1_web_search():
    """Ejemplo 1: Integración con búsqueda web"""
    print("=" * 60)
    print("EJEMPLO 1: Web Search Integration")
    print("=" * 60)

    # Crear búsqueda web
    search = DuckDuckGoSearchRun()

    # Preguntas que requieren búsqueda
    preguntas = [
        "¿Cuál es el clima en Madrid?",
        "Últimas noticias sobre tecnología",
        "Precio actual del Bitcoin"
    ]

    for pregunta in preguntas:
        print(f"\n🔍 Buscando: {pregunta}")
        try:
            resultados = search.run(pregunta)
            print(f"   Resultados: {resultados[:100]}...")
        except Exception as e:
            print(f"❌ Error: {e}")
            logger.error(f"Error en búsqueda: {e}")


def ejemplo_2_http_request():
    """Ejemplo 2: Llamadas HTTP a APIs"""
    print("\n" + "=" * 60)
    print("EJEMPLO 2: HTTP Request to External API")
    print("=" * 60)

    # Simulación de diferentes tipos de requests
    requests_config = [
        {
            "nombre": "JSONPlaceholder GET",
            "url": "https://jsonplaceholder.typicode.com/posts/1",
            "metodo": "GET",
            "descripcion": "Obtener post de ejemplo"
        },
        {
            "nombre": "API Status Check",
            "url": "https://status.github.com/api/status.json",
            "metodo": "GET",
            "descripcion": "Estado de GitHub"
        }
    ]

    for config in requests_config:
        print(f"\n🌐 {config['nombre']}")
        print(f"   URL: {config['url']}")
        print(f"   Descripción: {config['descripcion']}")

        try:
            respuesta = requests.get(config['url'], timeout=5)

            if respuesta.status_code == 200:
                datos = respuesta.json()
                print(f"   ✅ Éxito (Status: {respuesta.status_code})")
                print(f"   Datos: {json.dumps(datos)[:100]}...")
                logger.info(f"Request exitoso: {config['nombre']}")
            else:
                print(f"   ❌ Error: {respuesta.status_code}")

        except Exception as e:
            print(f"   ❌ Error: {e}")
            logger.error(f"Error en request: {e}")


def ejemplo_3_prompt_template():
    """Ejemplo 3: Prompt Templates para composición"""
    print("\n" + "=" * 60)
    print("EJEMPLO 3: Prompt Template Composition")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    # Template con variables
    template = """Eres un experto en {tema}.

Tu tarea es {tarea}.

Nivel de detalle: {nivel}

Responde directamente sin explicación adicional."""

    prompt = PromptTemplate(
        template=template,
        input_variables=["tema", "tarea", "nivel"]
    )

    configs = [
        {
            "tema": "Python",
            "tarea": "Explicar decoradores",
            "nivel": "Principiante"
        },
        {
            "tema": "JavaScript",
            "tarea": "Explicar closures",
            "nivel": "Intermedio"
        },
        {
            "tema": "Rust",
            "tarea": "Explicar ownership",
            "nivel": "Avanzado"
        }
    ]

    cadena = prompt | llm

    for config in configs:
        print(f"\n📚 Tema: {config['tema']}")
        print(f"   Tarea: {config['tarea']}")
        print(f"   Nivel: {config['nivel']}")

        try:
            respuesta = cadena.invoke(config)
            print(f"   Respuesta: {respuesta[:80]}...")
        except Exception as e:
            print(f"❌ Error: {e}")


def ejemplo_4_text_processing():
    """Ejemplo 4: Procesamiento de textos"""
    print("\n" + "=" * 60)
    print("EJEMPLO 4: Text Processing Components")
    print("=" * 60)

    # Función para procesar texto
    def procesar_texto(texto):
        """Simula componentes de procesamiento"""
        procesados = {
            "original": texto,
            "longitud": len(texto),
            "palabras": len(texto.split()),
            "mayuscula": texto.upper(),
            "minuscula": texto.lower(),
            "revertido": texto[::-1]
        }
        return procesados

    textos = [
        "Langflow es una plataforma visual para construir aplicaciones con LLMs",
        "Los componentes son bloques reutilizables",
        "Las integraciones permiten conectar APIs externas"
    ]

    for texto in textos:
        print(f"\n📄 Texto original: {texto[:50]}...")

        resultado = procesar_texto(texto)

        print(f"   Longitud: {resultado['longitud']} caracteres")
        print(f"   Palabras: {resultado['palabras']}")
        print(f"   Mayúscula: {resultado['mayuscula'][:40]}...")


def ejemplo_5_json_parsing():
    """Ejemplo 5: Parsing JSON con LLM"""
    print("\n" + "=" * 60)
    print("EJEMPLO 5: JSON Parsing with LLM")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    # Prompt que genera JSON
    template = """Analiza esta información y devuelve un JSON válido.

Información: {info}

Devuelve SOLO JSON válido con campos: nombre, tipo, descripción, prioridad.
Sin explicaciones adicionales."""

    prompt = PromptTemplate(
        template=template,
        input_variables=["info"]
    )

    cadena = prompt | llm

    informaciones = [
        "iPhone 15 - Último smartphone de Apple con chip A17",
        "Python - Lenguaje de programación versátil y poderoso",
        "PostgreSQL - Base de datos relacional de código abierto"
    ]

    for info in informaciones:
        print(f"\n🔄 Analizando: {info[:40]}...")

        try:
            respuesta = cadena.invoke({"info": info})

            # Intenta parsear como JSON
            try:
                datos_json = json.loads(respuesta)
                print(f"   ✅ JSON válido: {json.dumps(datos_json, indent=2)[:100]}...")
                logger.info(f"JSON parseado correctamente")
            except json.JSONDecodeError:
                print(f"   ⚠️  Respuesta no es JSON válido: {respuesta[:100]}...")

        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Función principal"""
    try:
        ejemplo_1_web_search()
        ejemplo_2_http_request()
        ejemplo_3_prompt_template()
        ejemplo_4_text_processing()
        ejemplo_5_json_parsing()

        print("\n" + "=" * 60)
        print("✅ Todos los ejemplos de componentes completados")
        print("=" * 60)

    except Exception as e:
        logger.critical(f"Error fatal: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
