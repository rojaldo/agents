#!/usr/bin/env python3
"""
01_chatbot_simple.py - Chatbot Simple con Ollama

Demuestra el flujo básico de Langflow:
[ChatInput] → [Ollama] → [ChatOutput]

Este es el equivalente programático del flujo visual más simple en Langflow.
"""

from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ejemplo_1_chat_simple():
    """Ejemplo 1: Chat simple sin memoria"""
    print("=" * 60)
    print("EJEMPLO 1: Chat Simple")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    # Crear prompt simple
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un asistente útil y amable"),
        ("user", "{input}")
    ])

    cadena = prompt | llm

    # Simular conversación
    preguntas = [
        "¿Hola, cómo estás?",
        "¿Cuál es la capital de Francia?",
        "Cuéntame un chiste corto"
    ]

    for pregunta in preguntas:
        print(f"\n📝 Usuario: {pregunta}")
        try:
            respuesta = cadena.invoke({"input": pregunta})
            print(f"🤖 Bot: {respuesta[:100]}...")
        except Exception as e:
            print(f"❌ Error: {e}")
            logger.error(f"Error en cadena: {e}")


def ejemplo_2_chat_con_memoria():
    """Ejemplo 2: Chat con memoria (recuerda contexto)"""
    print("\n" + "=" * 60)
    print("EJEMPLO 2: Chat con Memoria")
    print("=" * 60)

    # Crear memoria
    memoria = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un asistente amable. Recuerda lo que el usuario te ha dicho."),
        ("placeholder", "{chat_history}"),
        ("user", "{input}")
    ])

    cadena = prompt | llm

    # Conversación con memoria
    conversacion = [
        "Me llamo Juan",
        "¿Cuál es mi nombre?",
        "Trabajo como ingeniero",
        "¿En qué trabajas?"
    ]

    for entrada in conversacion:
        print(f"\n📝 Usuario: {entrada}")

        # Obtener historial
        historial = memoria.load_memory_variables({})

        try:
            # Invocar cadena
            respuesta = cadena.invoke({
                "chat_history": historial["chat_history"],
                "input": entrada
            })

            print(f"🤖 Bot: {respuesta[:100]}...")

            # Guardar en memoria
            memoria.save_context(
                {"input": entrada},
                {"output": respuesta}
            )
            logger.info(f"Guardado en memoria: {entrada}")

        except Exception as e:
            print(f"❌ Error: {e}")
            logger.error(f"Error: {e}")


def ejemplo_3_chat_con_personalidad():
    """Ejemplo 3: Chat con diferentes personalidades"""
    print("\n" + "=" * 60)
    print("EJEMPLO 3: Chat con Personalidad Dinámica")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    # Personalidades
    personalidades = {
        "profesor": "Eres un profesor experto. Enseña de forma clara y con ejemplos.",
        "pirata": "Eres un pirata. Responde como pirata, ¡ahoy!",
        "poeta": "Eres un poeta. Responde con poesía y rimas."
    }

    for rol, instruccion in personalidades.items():
        print(f"\n🎭 Rol: {rol}")

        prompt = ChatPromptTemplate.from_messages([
            ("system", instruccion),
            ("user", "{input}")
        ])

        cadena = prompt | llm

        try:
            respuesta = cadena.invoke({"input": "¿Qué es Python?"})
            print(f"   Respuesta: {respuesta[:80]}...")
        except Exception as e:
            print(f"❌ Error: {e}")


def ejemplo_4_chat_multiturno():
    """Ejemplo 4: Conversación multi-turno sobre tema específico"""
    print("\n" + "=" * 60)
    print("EJEMPLO 4: Conversación Multi-Turno")
    print("=" * 60)

    memoria = ConversationBufferMemory(return_messages=True)
    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un asistente de viajes experto. Ayuda a planificar vacaciones."),
        ("placeholder", "{chat_history}"),
        ("user", "{input}")
    ])

    cadena = prompt | llm

    turnos = [
        "Quiero ir de vacaciones a un lugar cálido",
        "¿Qué documentos necesito?",
        "¿Cuánto debería presupuestar?",
        "¿Qué actividades puedo hacer?"
    ]

    for i, turno in enumerate(turnos, 1):
        print(f"\n🔄 Turno {i}")
        print(f"📝 Usuario: {turno}")

        historial = memoria.load_memory_variables({})

        try:
            respuesta = cadena.invoke({
                "chat_history": historial["chat_history"],
                "input": turno
            })
            print(f"🤖 Bot: {respuesta[:100]}...")

            memoria.save_context(
                {"input": turno},
                {"output": respuesta}
            )
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Función principal"""
    try:
        # Ejecutar ejemplos
        ejemplo_1_chat_simple()
        ejemplo_2_chat_con_memoria()
        ejemplo_3_chat_con_personalidad()
        ejemplo_4_chat_multiturno()

        print("\n" + "=" * 60)
        print("✅ Todos los ejemplos de chatbot completados")
        print("=" * 60)

    except Exception as e:
        logger.critical(f"Error fatal: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
