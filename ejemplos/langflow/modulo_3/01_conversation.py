"""
Módulo 3: Conversaciones y Chat
Ejemplo 1: Sistema de chat con historial
"""

from datetime import datetime
from typing import List, Dict


class Message:
    """Representa un mensaje en la conversación"""

    def __init__(self, role: str, content: str):
        self.role = role  # "user" o "assistant"
        self.content = content
        self.timestamp = datetime.now()

    def __str__(self):
        return f"{self.role.upper()}: {self.content}"


class ConversationMemory:
    """Gestiona el historial de conversación"""

    def __init__(self, max_messages: int = 10):
        self.messages: List[Message] = []
        self.max_messages = max_messages

    def add_message(self, role: str, content: str):
        """Agregar mensaje al historial"""
        message = Message(role, content)
        self.messages.append(message)

        # Limitar historial
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)

    def get_context(self) -> str:
        """Obtener contexto para LLM"""
        return "\n".join(str(m) for m in self.messages[-5:])

    def get_history(self) -> List[Dict]:
        """Obtener historial completo"""
        return [
            {
                "role": m.role,
                "content": m.content,
                "timestamp": m.timestamp.isoformat()
            }
            for m in self.messages
        ]

    def clear(self):
        """Limpiar historial"""
        self.messages.clear()

    def print_history(self):
        """Imprimir historial"""
        print("\n📝 HISTORIAL DE CONVERSACIÓN\n")
        for i, message in enumerate(self.messages, 1):
            print(f"  {i}. {message}")


class ChatInterface:
    """Interfaz de chat mejorada"""

    def __init__(self):
        self.memory = ConversationMemory()
        self.system_prompt = "Eres un asistente amable que ayuda con preguntas sobre IA"
        self.conversation_count = 0

    def process_input(self, user_input: str) -> str:
        """Procesar entrada del usuario"""

        # Agregar mensaje del usuario al historial
        self.memory.add_message("user", user_input)
        self.conversation_count += 1

        # Simular respuesta del modelo
        response = self._generate_response(user_input)

        # Agregar respuesta del asistente
        self.memory.add_message("assistant", response)

        return response

    def _generate_response(self, user_input: str) -> str:
        """Generar respuesta simulada"""

        responses = {
            "hola": "¡Hola! ¿Cómo puedo ayudarte hoy?",
            "qué eres": "Soy un asistente de IA entrenado para ayudarte",
            "bye": "¡Adiós! Fue un placer hablar contigo",
            "gracias": "¡De nada! Estoy aquí para ayudarte",
            "ayuda": "Puedo responder preguntas sobre IA y tecnología"
        }

        for key, response in responses.items():
            if key in user_input.lower():
                return response

        return f"Entiendo que preguntaste sobre '{user_input}'. Déjame ayudarte con eso."

    def get_stats(self) -> Dict:
        """Obtener estadísticas de conversación"""
        return {
            "total_messages": len(self.memory.messages),
            "exchanges": self.conversation_count // 2,
            "user_messages": sum(1 for m in self.memory.messages if m.role == "user"),
            "assistant_messages": sum(1 for m in self.memory.messages if m.role == "assistant")
        }

    def print_stats(self):
        """Imprimir estadísticas"""
        stats = self.get_stats()
        print("\n📊 ESTADÍSTICAS DE CONVERSACIÓN\n")
        print(f"  Total de mensajes: {stats['total_messages']}")
        print(f"  Intercambios: {stats['exchanges']}")
        print(f"  Mensajes de usuario: {stats['user_messages']}")
        print(f"  Mensajes de asistente: {stats['assistant_messages']}")


def main():
    """Demostración de conversaciones en Langflow"""
    print("="*70)
    print(" MÓDULO 3: CONVERSACIONES Y CHAT")
    print("="*70)

    chat = ChatInterface()

    print("\n🤖 INICIANDO CHAT CON MEMORIA\n")
    print(f"  Sistema: {chat.system_prompt}\n")

    # Simular conversación
    conversation = [
        "Hola",
        "Qué eres",
        "Puedes ayudarme con IA",
        "Gracias",
        "Bye"
    ]

    print("💬 CONVERSACIÓN:\n")

    for user_input in conversation:
        response = chat.process_input(user_input)
        print(f"  👤 Usuario: {user_input}")
        print(f"  🤖 Asistente: {response}\n")

    # Mostrar historial
    chat.memory.print_history()

    # Mostrar estadísticas
    chat.print_stats()

    # Demostrar contexto para LLM
    print("\n📋 CONTEXTO PARA LLM (últimos 5 mensajes)\n")
    print(chat.memory.get_context())

    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
