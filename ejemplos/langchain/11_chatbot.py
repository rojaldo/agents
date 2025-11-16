#!/usr/bin/env python3
"""
11_chatbot.py - Chatbots Conversacionales Completos

Demuestra:
- Chat simple con memoria
- Multi-turn conversations
- Diferentes estilos de conversación
"""

from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama


def ejemplo_chatbot_simple():
    """Chatbot básico con memoria"""
    print("=" * 60)
    print("EJEMPLO 1: Chatbot Simple")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")
    memoria = ConversationBufferMemory(return_messages=True)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un asistente amable y útil."),
        ("placeholder", "{chat_history}"),
        ("user", "{input}")
    ])

    cadena = prompt | llm

    print("\nChatbot (escribe 'salir' para terminar):")
    print("Conversación:")

    contador = 0
    try:
        while True:
            usuario_input = input("\nTú: ").strip()

            if usuario_input.lower() in ["salir", "exit", "quit"]:
                print("¡Hasta luego!")
                break

            if not usuario_input:
                continue

            # Obtener historial
            historial = memoria.load_memory_variables({})

            # Generar respuesta
            try:
                respuesta = cadena.invoke({
                    "chat_history": historial['chat_history'],
                    "input": usuario_input
                })
                print(f"Bot: {respuesta}")

                # Guardar en memoria
                memoria.save_context(
                    {"input": usuario_input},
                    {"output": respuesta}
                )

                contador += 1

            except Exception as e:
                print(f"Error en respuesta: {e}")

        print(f"\nTotal de turnos: {contador}")

    except KeyboardInterrupt:
        print("\n\nChat interrumpido.")


def ejemplo_chatbot_personalizado():
    """Chatbot con personalidad"""
    print("=" * 60)
    print("EJEMPLO 2: Chatbot Personalizado (Demo)")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")
    memoria = ConversationBufferMemory(return_messages=True)

    # Diferentes sistemas de chatbot
    chatbots = {
        "profesor": {
            "system": "Eres un profesor experto. Enseña de forma clara y haciendo preguntas.",
            "describe": "Profesor educativo"
        },
        "amigo": {
            "system": "Eres un amigo amable y comprensivo. Sé empático y casual.",
            "describe": "Amigo amable"
        },
        "asistente": {
            "system": "Eres un asistente profesional. Sé breve y eficiente.",
            "describe": "Asistente profesional"
        }
    }

    print("\nModos disponibles: profesor, amigo, asistente")
    modo = input("Elige modo (default: amigo): ").strip().lower() or "amigo"

    if modo not in chatbots:
        print(f"Modo no disponible. Usando 'amigo'")
        modo = "amigo"

    config = chatbots[modo]

    prompt = ChatPromptTemplate.from_messages([
        ("system", config["system"]),
        ("placeholder", "{chat_history}"),
        ("user", "{input}")
    ])

    cadena = prompt | llm

    print(f"\n🤖 Modo: {config['describe']}")
    print("(Escribe preguntas de prueba. Escribe 'salir' para terminar)\n")

    # Preguntas de demostración
    preguntas_demo = [
        "¿Cuál es tu recomendación para aprender programación?",
        "¿Cómo te va hoy?",
    ]

    for pregunta in preguntas_demo:
        try:
            print(f"Tú: {pregunta}")

            historial = memoria.load_memory_variables({})

            respuesta = cadena.invoke({
                "chat_history": historial['chat_history'],
                "input": pregunta
            })

            print(f"Bot: {respuesta}\n")

            memoria.save_context(
                {"input": pregunta},
                {"output": respuesta}
            )

        except Exception as e:
            print(f"Error: {e}\n")

    print("Demo completada.")


def ejemplo_chatbot_con_ventana():
    """Chatbot que olvida conversaciones antiguas"""
    print("=" * 60)
    print("EJEMPLO 3: Chatbot con Ventana de Memoria")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    # Memory window: mantiene solo los últimos 2 turnos
    memoria = ConversationBufferWindowMemory(
        k=2,
        return_messages=True,
        memory_key="chat_history"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un asistente. Solo recuerdas los últimos turnos."),
        ("placeholder", "{chat_history}"),
        ("user", "{input}")
    ])

    cadena = prompt | llm

    print("\nChatbot con ventana de memoria (k=2)")
    print("Solo recuerda los últimos 2 turnos\n")

    preguntas = [
        "Mi nombre es Juan",
        "Cuál es mi nombre?",
        "Trabajo en tecnología",
        "¿Qué hace un ingeniero?",
        "¿Cuál es mi nombre nuevamente?"
    ]

    for i, pregunta in enumerate(preguntas, 1):
        try:
            print(f"{i}. Tú: {pregunta}")

            historial = memoria.load_memory_variables({})
            print(f"   (Mensajes en memoria: {len(historial['chat_history'])})")

            respuesta = cadena.invoke({
                "chat_history": historial['chat_history'],
                "input": pregunta
            })

            print(f"   Bot: {respuesta.strip()[:80]}...\n")

            memoria.save_context(
                {"input": pregunta},
                {"output": respuesta}
            )

        except Exception as e:
            print(f"   Error: {e}\n")


def ejemplo_multi_turn():
    """Conversación multi-turno demostrativa"""
    print("=" * 60)
    print("EJEMPLO 4: Multi-Turn Conversation (Demo)")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")
    memoria = ConversationBufferMemory(return_messages=True)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un asistente de viajes. Ayuda a planificar vacaciones."),
        ("placeholder", "{chat_history}"),
        ("user", "{input}")
    ])

    cadena = prompt | llm

    print("\nConversación de múltiples turnos sobre viajes:\n")

    conversacion = [
        "Quiero ir de vacaciones a un lugar cálido",
        "¿Qué documentos necesito?",
        "¿Cómo me presupuesto?",
    ]

    for i, mensaje in enumerate(conversacion, 1):
        try:
            print(f"Turno {i}")
            print(f"Tú: {mensaje}")

            historial = memoria.load_memory_variables({})

            respuesta = cadena.invoke({
                "chat_history": historial['chat_history'],
                "input": mensaje
            })

            print(f"Bot: {respuesta.strip()[:100]}...\n")

            memoria.save_context(
                {"input": mensaje},
                {"output": respuesta}
            )

        except Exception as e:
            print(f"Error: {e}\n")

    print("Demo de conversación completada.")


def ejemplo_stats_conversacion():
    """Estadísticas de la conversación"""
    print("=" * 60)
    print("EJEMPLO 5: Estadísticas de Conversación")
    print("=" * 60)

    memoria = ConversationBufferMemory(return_messages=True)

    # Simular conversación
    intercambios = [
        ("Hola", "Hola, ¿cómo estás?"),
        ("Bien", "Me alegra escuchar eso"),
        ("¿Qué es Python?", "Python es un lenguaje de programación"),
    ]

    print("\nCargando conversación...")

    for user_input, ai_output in intercambios:
        memoria.save_context(
            {"input": user_input},
            {"output": ai_output}
        )

    # Obtener estadísticas
    historial = memoria.load_memory_variables({})
    mensajes = historial['chat_history']

    print("\n📊 Estadísticas:")
    print(f"  Total de mensajes: {len(mensajes)}")
    print(f"  Turnos: {len(intercambios)}")

    # Longitud promedio
    longitudes = [len(msg.content) for msg in mensajes]
    promedio = sum(longitudes) / len(longitudes) if longitudes else 0

    print(f"  Longitud promedio: {promedio:.0f} caracteres")
    print(f"  Mensaje más corto: {min(longitudes)} caracteres")
    print(f"  Mensaje más largo: {max(longitudes)} caracteres")

    print("\n📝 Historial:")
    for i, msg in enumerate(mensajes, 1):
        rol = "Usuario" if msg.type == "human" else "Asistente"
        print(f"  {i}. [{rol}] {msg.content[:50]}...")

    print()


if __name__ == "__main__":
    try:
        # Ejemplo 1: Chatbot interactivo (comentado para no bloquear)
        print("Nota: Ejemplo 1 es interactivo (descomenta para probar)\n")

        # ejemplo_chatbot_simple()

        # Ejemplos de demostración
        ejemplo_chatbot_personalizado()
        ejemplo_chatbot_con_ventana()
        ejemplo_multi_turn()
        ejemplo_stats_conversacion()

        print("=" * 60)
        print("✅ Todos los ejemplos de chatbot completados")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
