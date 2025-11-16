"""
Módulo 5: Casos de Uso Prácticos
Ejemplo 1: Chatbot de atención al cliente
"""

from datetime import datetime
from typing import Dict, List


class CustomerServiceBot:
    """Chatbot de atención al cliente"""

    def __init__(self):
        self.conversations = []
        self.current_conversation = []
        self.knowledge_base = {
            "horarios": "Abierto de 9:00 a 18:00 de lunes a viernes",
            "devoluciones": "Las devoluciones se aceptan dentro de 30 días",
            "envios": "Envío gratis para órdenes mayores a $50",
            "contacto": "Email: support@example.com, Tel: 1-800-XXX-XXXX"
        }

    def classify_intent(self, message: str) -> str:
        """Clasificar intención del usuario"""

        intents = {
            "horarios": ["horario", "abierto", "cerrado", "horas"],
            "devoluciones": ["devolver", "reembolso", "devolucion"],
            "envios": ["envio", "delivery", "entregar"],
            "contacto": ["email", "telefono", "contacto"],
            "escalacion": ["hablar humano", "gerente", "supervisor"]
        }

        for intent, keywords in intents.items():
            if any(keyword in message.lower() for keyword in keywords):
                return intent

        return "general"

    def handle_intent(self, intent: str, message: str) -> str:
        """Manejar intención y generar respuesta"""

        if intent == "escalacion":
            return "Conectando con un agente humano. Por favor espere..."

        if intent in self.knowledge_base:
            return f"Información: {self.knowledge_base[intent]}"

        return "Gracias por tu pregunta. ¿Hay algo más en lo que pueda ayudarte?"

    def process_message(self, user_message: str) -> str:
        """Procesar mensaje del usuario"""

        # Clasificar intención
        intent = self.classify_intent(user_message)

        # Generar respuesta
        bot_response = self.handle_intent(intent, user_message)

        # Guardar en conversación
        self.current_conversation.append({
            "user": user_message,
            "bot": bot_response,
            "intent": intent,
            "timestamp": datetime.now().isoformat()
        })

        return bot_response

    def start_conversation(self) -> str:
        """Iniciar conversación"""
        self.current_conversation = []
        greeting = "Hola! Bienvenido a nuestro servicio de atención al cliente. ¿Cómo puedo ayudarte?"
        self.current_conversation.append({
            "bot": greeting,
            "timestamp": datetime.now().isoformat()
        })
        return greeting

    def end_conversation(self) -> Dict:
        """Terminar conversación y guardar"""

        record = {
            "id": len(self.conversations),
            "timestamp": datetime.now().isoformat(),
            "messages": len(self.current_conversation),
            "conversation": self.current_conversation
        }

        self.conversations.append(record)
        return record

    def get_stats(self) -> Dict:
        """Obtener estadísticas"""

        total_messages = sum(len(c["conversation"]) for c in self.conversations)

        return {
            "total_conversations": len(self.conversations),
            "total_messages": total_messages,
            "avg_messages_per_conv": total_messages // len(self.conversations) if self.conversations else 0
        }

    def print_conversation(self):
        """Imprimir conversación actual"""

        print("\n💬 CONVERSACIÓN:\n")

        for i, exchange in enumerate(self.current_conversation, 1):
            if "user" in exchange:
                print(f"  {i}. 👤 Usuario: {exchange['user']}")
            if "bot" in exchange:
                print(f"     🤖 Bot: {exchange['bot']}")


def main():
    """Demostración de chatbot de atención al cliente"""
    print("="*70)
    print(" MÓDULO 5: CASOS DE USO PRÁCTICOS")
    print("="*70)

    bot = CustomerServiceBot()

    # Iniciar conversación
    print("\n🤖 CHATBOT DE ATENCIÓN AL CLIENTE\n")
    greeting = bot.start_conversation()
    print(f"  {greeting}\n")

    # Simular interacciones
    user_inputs = [
        "¿Cuál es tu horario de atención?",
        "¿Puedo devolver un producto?",
        "¿Cuánto cuesta el envío?",
        "Necesito hablar con un gerente",
        "Gracias por tu ayuda"
    ]

    for user_input in user_inputs:
        print(f"  👤 Usuario: {user_input}")
        response = bot.process_message(user_input)
        print(f"  🤖 Bot: {response}\n")

    # Mostrar conversación
    bot.print_conversation()

    # Terminar conversación
    bot.end_conversation()

    # Estadísticas
    stats = bot.get_stats()
    print("\n" + "="*70)
    print("ESTADÍSTICAS")
    print("="*70 + "\n")

    print(f"  Total de conversaciones: {stats['total_conversations']}")
    print(f"  Total de mensajes: {stats['total_messages']}")
    print(f"  Promedio de mensajes: {stats['avg_messages_per_conv']}")

    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
