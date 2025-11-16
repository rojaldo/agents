"""
MÓDULO 8: Chat con Memoria
Sistema de chat RAG que mantiene contexto de conversación
"""

import json
from typing import List
from datetime import datetime

# ============================================================================
# GESTOR DE MEMORIA DE CONVERSACIÓN
# ============================================================================

class MemoriaConversacion:
    """Gestiona el historial de conversación"""

    def __init__(self, max_mensajes: int = 10):
        self.mensajes = []
        self.max_mensajes = max_mensajes

    def agregar_mensaje(self, rol: str, contenido: str):
        """Agregar un mensaje al historial"""
        self.mensajes.append({
            "rol": rol,  # "usuario" o "asistente"
            "contenido": contenido,
            "timestamp": datetime.now().isoformat()
        })

        # Mantener solo los últimos N mensajes
        if len(self.mensajes) > self.max_mensajes:
            self.mensajes = self.mensajes[-self.max_mensajes:]

    def obtener_contexto(self) -> str:
        """Obtener el historial como contexto"""
        contexto = "Historial de conversación:\n"
        for msg in self.mensajes:
            rol = "Usuario" if msg["rol"] == "usuario" else "Asistente"
            contexto += f"\n{rol}: {msg['contenido']}"
        return contexto

    def obtener_ultimos_mensajes(self, n: int = 3) -> List[dict]:
        """Obtener los últimos N mensajes"""
        return self.mensajes[-n:]

    def limpiar(self):
        """Limpiar historial"""
        self.mensajes = []


# ============================================================================
# DEMOSTRACIÓN DE CHAT CON MEMORIA
# ============================================================================

def demostrar_chat_con_memoria():
    """Demostración de un sistema de chat RAG con memoria"""

    print("=" * 70)
    print("MÓDULO 8: Chat con Memoria")
    print("=" * 70)

    # Crear memoria
    memoria = MemoriaConversacion(max_mensajes=20)

    # Base de conocimiento simulada
    documentos_base = [
        {
            "titulo": "Python Basics",
            "contenido": "Python fue creado por Guido van Rossum en 1989. Es conocido por su sintaxis simple. Se usa para web, data science y automatización."
        },
        {
            "titulo": "RAG Systems",
            "contenido": "RAG combina recuperación con generación. Mejora la precisión de respuestas usando contexto. Ideal para QA sobre bases de conocimiento."
        },
        {
            "titulo": "Machine Learning",
            "contenido": "ML permite a máquinas aprender de datos sin programación explícita. Incluye supervisado, no supervisado y refuerzo."
        },
        {
            "titulo": "LLMs",
            "contenido": "Los Modelos de Lenguaje Grande (LLMs) como GPT pueden generar texto coherente. Ollama permite ejecutarlos localmente sin APIs."
        }
    ]

    # Simulación de conversación
    conversacion = [
        "¿Qué es Python?",
        "¿Para qué sirve?",
        "¿Quién lo creó?",
        "¿Cómo se relaciona con Machine Learning?",
        "¿Puedo usar RAG con Ollama?",
        "¿Cómo mantengo la memoria en un chat?",
    ]

    print("\n" + "=" * 70)
    print("SIMULACIÓN DE CHAT CON MEMORIA")
    print("=" * 70)

    resultados_chat = []

    for i, pregunta in enumerate(conversacion, 1):
        print(f"\n📨 TURNO {i}")
        print("-" * 70)

        # Usuario
        print(f"Usuario: {pregunta}")
        memoria.agregar_mensaje("usuario", pregunta)

        # Buscar documentos relevantes
        palabras_clave = pregunta.lower().split()
        doc_relevante = None
        for doc in documentos_base:
            if any(palabra in doc["contenido"].lower() for palabra in palabras_clave):
                doc_relevante = doc
                break

        # Generar respuesta con contexto y memoria
        contexto_conversacion = memoria.obtener_contexto()

        respuesta_simulada = f"""Basándome en el historial y el contexto:

Contexto: {doc_relevante["contenido"] if doc_relevante else "Información general"}

La respuesta es: {generar_respuesta_contextual(pregunta, doc_relevante)}"""

        print(f"Asistente: {respuesta_simulada[:100]}...")
        memoria.agregar_mensaje("asistente", respuesta_simulada)

        # Guardar resultado
        resultados_chat.append({
            "turno": i,
            "pregunta": pregunta,
            "documentos_utilizados": doc_relevante["titulo"] if doc_relevante else "Ninguno",
            "respuesta_preview": respuesta_simulada[:100]
        })

    # ========================================================================
    # MOSTRAR ESTADO DE MEMORIA
    # ========================================================================
    print("\n" + "=" * 70)
    print("ESTADO ACTUAL DE LA MEMORIA")
    print("=" * 70)

    print(f"Total de mensajes en memoria: {len(memoria.mensajes)}")
    print(f"Capacidad máxima: {memoria.max_mensajes}")
    print("\nÚltimos 3 mensajes:")

    for msg in memoria.obtener_ultimos_mensajes(3):
        rol = "👤 Usuario" if msg["rol"] == "usuario" else "🤖 Asistente"
        contenido_preview = msg["contenido"][:60] + "..."
        print(f"  {rol}: {contenido_preview}")

    # ========================================================================
    # VENTAJAS DE MEMORIA EN CHAT
    # ========================================================================
    print("\n" + "=" * 70)
    print("VENTAJAS DE MEMORIA EN CHAT")
    print("=" * 70)

    ventajas = {
        "Contexto": "El chat entiende referencias a mensajes anteriores",
        "Coherencia": "Las respuestas son más consistentes",
        "Personalizaci ón": "El asistente recuerda preferencias del usuario",
        "Reducción": "Se evita repetir información",
        "Eficiencia": "Menos tokens necesarios para el LLM"
    }

    for ventaja, descripción in ventajas.items():
        print(f"  ✓ {ventaja}: {descripción}")

    # ========================================================================
    # CÓDIGO PARA USAR CON OLLAMA
    # ========================================================================
    print("\n" + "=" * 70)
    print("CÓDIGO PARA USAR CON OLLAMA")
    print("=" * 70)

    codigo = '''
from langchain_ollama import OllamaLLM
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# Crear LLM
llm = OllamaLLM(model="mistral")

# Crear memoria
memory = ConversationBufferMemory()

# Crear cadena con memoria
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

# Usar en conversación
respuesta = conversation.predict(input="¿Qué es RAG?")
respuesta = conversation.predict(input="¿Puedo usarlo en Ollama?")
    '''

    print(codigo)

    # ========================================================================
    # GUARDAR RESULTADOS
    # ========================================================================
    resultado_final = {
        "sistema": "Chat con Memoria",
        "turnos": len(conversacion),
        "mensajes_totales": len(memoria.mensajes),
        "conversacion": resultados_chat,
        "historial_completo": [
            {
                "rol": msg["rol"],
                "contenido": msg["contenido"][:100],
                "timestamp": msg["timestamp"]
            }
            for msg in memoria.mensajes
        ]
    }

    with open("chat_memoria.json", "w", encoding="utf-8") as f:
        json.dump(resultado_final, f, ensure_ascii=False, indent=2)

    print("\n✓ Resultados guardados en chat_memoria.json")
    print("✅ Chat con memoria demostrado exitosamente")


def generar_respuesta_contextual(pregunta: str, documento: dict) -> str:
    """Generar una respuesta contextual (simulado)"""
    respuestas_simuladas = {
        "python": "Python es un lenguaje versátil creado en 1989.",
        "machine": "Machine Learning es una rama de la IA que aprende de datos.",
        "rag": "RAG es una técnica que combina búsqueda con generación de texto.",
        "ollama": "Ollama permite ejecutar modelos de lenguaje localmente.",
        "memoria": "La memoria permite al chat mantener contexto de conversación."
    }

    for clave, respuesta in respuestas_simuladas.items():
        if clave in pregunta.lower():
            return respuesta

    return "Esa es una pregunta interesante sobre temas complejos."


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    demostrar_chat_con_memoria()
