"""
Módulo 1: Introducción a AutoGen
Ejemplo 1: Hello World - Primer programa con AutoGen y Ollama
"""

import requests
from datetime import datetime


class SimpleAssistant:
    """Agente asistente simple que responde preguntas"""

    def __init__(self, base_url="http://localhost:11434", model="mistral", name="Assistant"):
        self.base_url = base_url
        self.model = model
        self.name = name
        self.conversation_history = []

    def _call_ollama(self, prompt):
        """Hacer llamada a Ollama"""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": 0.7,
            "stream": False
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                return response.json().get('response', '')
            else:
                return f"Error: {response.status_code}"

        except requests.exceptions.ConnectionError:
            return "Error: No se puede conectar a Ollama. Ejecuta: ollama serve"
        except requests.exceptions.Timeout:
            return "Error: Timeout"
        except Exception as e:
            return f"Error: {str(e)}"

    def respond(self, message):
        """Responder a un mensaje"""
        response = self._call_ollama(message)

        # Guardar en historial
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user_message": message,
            "assistant_response": response
        })

        return response

    def get_conversation_count(self):
        """Obtener cantidad de intercambios"""
        return len(self.conversation_history)

    def print_conversation_history(self):
        """Imprimir historial de conversación"""
        print(f"\n{'='*70}")
        print(f"HISTORIAL DE CONVERSACIÓN - {self.name}")
        print("="*70)

        for i, exchange in enumerate(self.conversation_history, 1):
            print(f"\n[{i}] Hora: {exchange['timestamp']}")
            print(f"Usuario: {exchange['user_message']}")
            print(f"Asistente: {exchange['assistant_response'][:150]}...")

        print(f"\n{'='*70}\n")


def main():
    """Función principal - Hello World"""
    print("="*70)
    print(" AUTOGEN: HELLO WORLD - Primer Programa")
    print("="*70)

    # Crear asistente
    print("\n🤖 Creando asistente...")
    assistant = SimpleAssistant(name="Mi Primer Asistente")
    print(f"✓ Asistente '{assistant.name}' creado")
    print(f"  Modelo: {assistant.model}")
    print(f"  Servidor: {assistant.base_url}")

    # Primera pregunta
    print("\n" + "="*70)
    print("PRIMERA CONVERSACIÓN")
    print("="*70)

    question1 = "¿Hola! ¿Quién eres?"
    print(f"\n👤 Usuario: {question1}")
    print("\n🤖 Asistente (pensando...)")

    response1 = assistant.respond(question1)

    if response1.startswith("Error"):
        print(f"❌ {response1}")
        print("\nPara usar este ejemplo:")
        print("1. Instala Ollama: https://ollama.ai")
        print("2. Ejecuta: ollama serve")
        print("3. Descarga un modelo: ollama pull mistral")
        return
    else:
        print(f"✓ Respuesta recibida:")
        print("-"*70)
        print(response1[:300])
        if len(response1) > 300:
            print("... (respuesta continúa)")
        print("-"*70)

    # Segunda pregunta
    print("\n" + "="*70)
    print("SEGUNDA CONVERSACIÓN")
    print("="*70)

    question2 = "¿Cuál es el propósito de AutoGen?"
    print(f"\n👤 Usuario: {question2}")
    print("\n🤖 Asistente (pensando...)")

    response2 = assistant.respond(question2)

    if not response2.startswith("Error"):
        print(f"✓ Respuesta recibida:")
        print("-"*70)
        print(response2[:300])
        if len(response2) > 300:
            print("... (respuesta continúa)")
        print("-"*70)

    # Tercera pregunta
    print("\n" + "="*70)
    print("TERCERA CONVERSACIÓN")
    print("="*70)

    question3 = "Dame 3 ventajas de usar agentes de IA"
    print(f"\n👤 Usuario: {question3}")
    print("\n🤖 Asistente (pensando...)")

    response3 = assistant.respond(question3)

    if not response3.startswith("Error"):
        print(f"✓ Respuesta recibida:")
        print("-"*70)
        print(response3[:300])
        if len(response3) > 300:
            print("... (respuesta continúa)")
        print("-"*70)

    # Mostrar estadísticas
    print("\n" + "="*70)
    print("ESTADÍSTICAS")
    print("="*70)
    print(f"Total de intercambios: {assistant.get_conversation_count()}")
    print("="*70 + "\n")

    # Mostrar historial (opcional)
    # assistant.print_conversation_history()


if __name__ == "__main__":
    main()
