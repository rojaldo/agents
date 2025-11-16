#!/usr/bin/env python3
"""
03_memory.py - Gestión de memoria en conversaciones

Demuestra:
- ConversationBufferMemory
- ConversationWindowMemory
- Chatbots con contexto
- Guardado y carga de memoria
"""

from langchain.memory import (
    ConversationBufferMemory,
    ConversationBufferWindowMemory
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import HumanMessage, AIMessage


def ejemplo_buffer_memory():
    """Memoria que almacena todo el historial"""
    print("=" * 60)
    print("EJEMPLO 1: ConversationBufferMemory")
    print("=" * 60)

    memoria = ConversationBufferMemory(
        memory_key="history",
        return_messages=True
    )

    # Simular conversación
    print("\nAñadiendo mensajes a la memoria...")

    memoria.chat_memory.add_user_message("Hola, soy Juan")
    memoria.chat_memory.add_ai_message("Mucho gusto Juan, ¿cómo estás?")

    memoria.chat_memory.add_user_message("Estoy bien, trabajo en Python")
    memoria.chat_memory.add_ai_message("Excelente, Python es un lenguaje poderoso")

    memoria.chat_memory.add_user_message("¿Y cuál es mi nombre?")
    memoria.chat_memory.add_ai_message("Tu nombre es Juan, lo mencionaste al principio")

    # Obtener historial
    historial = memoria.load_memory_variables({})

    print("\nHistorial completo:")
    for msg in historial['history']:
        print(f"  {msg.type}: {msg.content}")


def ejemplo_window_memory():
    """Memoria que mantiene solo los últimos N intercambios"""
    print("\n" + "=" * 60)
    print("EJEMPLO 2: ConversationWindowMemory (últimos 2 turnos)")
    print("=" * 60)

    memoria_ventana = ConversationBufferWindowMemory(
        k=2,  # Mantener solo 2 últimos intercambios
        memory_key="history",
        return_messages=True
    )

    # Agregar varios mensajes
    mensajes = [
        ("Usuario: Primer mensaje", "IA: Primera respuesta"),
        ("Usuario: Segundo mensaje", "IA: Segunda respuesta"),
        ("Usuario: Tercer mensaje", "IA: Tercera respuesta"),
        ("Usuario: Cuarto mensaje", "IA: Cuarta respuesta"),
    ]

    print("\nAñadiendo 4 intercambios a memoria con k=2...")
    for i, (user, ai) in enumerate(mensajes):
        memoria_ventana.save_context(
            {"input": user},
            {"output": ai}
        )
        print(f"  Intercambio {i+1}: añadido")

    # La memoria solo mantiene los últimos 2
    historial = memoria_ventana.load_memory_variables({})

    print("\nHistorial después (solo últimos 2 intercambios):")
    for msg in historial['history']:
        print(f"  {msg.type}: {msg.content[:50]}...")


def ejemplo_chatbot_conversacional():
    """Chatbot que mantiene contexto entre turnos"""
    print("\n" + "=" * 60)
    print("EJEMPLO 3: Chatbot Conversacional Interactivo")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")
    memoria = ConversationBufferMemory(
        return_messages=True,
        memory_key="chat_history"
    )

    # Template del chatbot
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un asistente amable y útil. Recuerda lo que el usuario te ha dicho."),
        ("placeholder", "{chat_history}"),
        ("user", "{input}")
    ])

    cadena = prompt | llm | StrOutputParser()

    print("\nChatbot conversacional (escribe 'salir' para terminar):")
    print("(El bot mantendrá contexto de la conversación)\n")

    while True:
        usuario_input = input("Tú: ").strip()

        if usuario_input.lower() in ["salir", "exit", "quit"]:
            print("¡Hasta luego!")
            break

        if not usuario_input:
            continue

        try:
            # Obtener historial
            historial = memoria.load_memory_variables({})

            # Generar respuesta
            respuesta = cadena.invoke({
                "chat_history": historial['chat_history'],
                "input": usuario_input
            })

            print(f"Bot: {respuesta}\n")

            # Guardar en memoria
            memoria.save_context(
                {"input": usuario_input},
                {"output": respuesta}
            )

        except Exception as e:
            print(f"Error: {e}")


def ejemplo_resumen_memory():
    """Mostrar cómo la memoria maneja conversaciones largas"""
    print("\n" + "=" * 60)
    print("EJEMPLO 4: Manejo de Conversaciones Largas")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    # Memoria con límite de ventana
    memoria = ConversationBufferWindowMemory(
        k=3,
        memory_key="history",
        return_messages=True
    )

    print("\nSimulando una conversación de 5 turnos con memory window k=3:")

    conversacion = [
        ("Mi nombre es María", "Gusto en conocerte María"),
        ("Soy ingeniera", "Excelente, ingeniería es fascinante"),
        ("Trabajo en IA", "¡Qué interesante!"),
        ("Tengo 5 años de experiencia", "Eso es muy valioso"),
        ("¿Cuál es mi nombre?", "Tu nombre es María")
    ]

    for i, (user, ia) in enumerate(conversacion, 1):
        memoria.save_context(
            {"input": user},
            {"output": ia}
        )

        historial = memoria.load_memory_variables({})

        print(f"\n--- Turno {i} ---")
        print(f"Usuario: {user}")
        print(f"IA: {ia}")
        print(f"Mensajes en memoria: {len(historial['history'])}")

        for j, msg in enumerate(historial['history'], 1):
            print(f"  [{j}] {msg.type}: {msg.content[:40]}...")


def ejemplo_memoria_persistente():
    """Guardar y cargar memoria"""
    print("\n" + "=" * 60)
    print("EJEMPLO 5: Guardar y Cargar Memoria")
    print("=" * 60)

    # Crear y llenar memoria
    memoria = ConversationBufferMemory()

    print("\nCreando memoria con datos...")

    datos_conversacion = [
        ({"input": "Hola, ¿qué tal?"}, {"output": "¡Hola! Todo bien, gracias"}),
        ({"input": "¿Cuál es tu nombre?"}, {"output": "Soy un asistente de IA"}),
    ]

    for inputs, outputs in datos_conversacion:
        memoria.save_context(inputs, outputs)
        print(f"  Guardado: {inputs['input']}")

    # Mostrar memoria
    print("\nContenido de la memoria:")
    contenido = memoria.load_memory_variables({})
    print(contenido['history'])

    # En producción, guardarías esto en una base de datos
    print("\n✓ En producción, guardarías esta memoria en:")
    print("  - Base de datos (PostgreSQL, MongoDB)")
    print("  - Redis para caché")
    print("  - Archivos JSON/YAML")


def ejemplo_memoria_personalizada():
    """Crear una memoria personalizada"""
    print("\n" + "=" * 60)
    print("EJEMPLO 6: Memoria Personalizada")
    print("=" * 60)

    class MemoriaSimple:
        """Memoria simple basada en lista"""

        def __init__(self):
            self.historial = []

        def save_context(self, inputs, outputs):
            self.historial.append({
                "usuario": inputs.get("input"),
                "respuesta": outputs.get("output")
            })

        def load_memory_variables(self):
            return {
                "num_turnos": len(self.historial),
                "historial": self.historial
            }

        def clear(self):
            self.historial = []

    # Usar
    memoria_simple = MemoriaSimple()

    print("\nUsando memoria personalizada...")

    for i in range(3):
        memoria_simple.save_context(
            {"input": f"Pregunta {i+1}"},
            {"output": f"Respuesta {i+1}"}
        )

    variables = memoria_simple.load_memory_variables()

    print(f"\nTotal de turnos: {variables['num_turnos']}")
    print("Historial:")
    for item in variables['historial']:
        print(f"  - {item['usuario']} -> {item['respuesta']}")


if __name__ == "__main__":
    try:
        ejemplo_buffer_memory()
        ejemplo_window_memory()

        # Comentado para no ser interactivo en testing automático
        # Descomenta si quieres probar el chatbot interactivo
        # ejemplo_chatbot_conversacional()

        ejemplo_resumen_memory()
        ejemplo_memoria_persistente()
        ejemplo_memoria_personalizada()

        print("\n" + "=" * 60)
        print("✅ Todos los ejemplos de memoria completados")
        print("=" * 60)
        print("\n💡 Para probar el chatbot interactivo, descomenta")
        print("   la línea en la función main()")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Asegúrate de que Ollama está ejecutándose")
