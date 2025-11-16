"""
Módulo 3: Patrones de Conversación
Ejemplo 1: Conversation Patterns - Patrones básicos de conversación
"""

import requests
from datetime import datetime


class ConversationManager:
    """Gestor de conversaciones entre múltiples agentes"""

    def __init__(self, base_url="http://localhost:11434", model="mistral"):
        self.base_url = base_url
        self.model = model
        self.conversations = []

    def _call_ollama(self, prompt, system_prompt=""):
        """Hacer llamada a Ollama"""
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt

        payload = {
            "model": self.model,
            "prompt": full_prompt,
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
            return "Error: Ollama no disponible"
        except Exception as e:
            return f"Error: {str(e)}"

    def simple_conversation(self, topic):
        """Patrón 1: Conversación simple (Q&A)"""
        print(f"\n{'═'*70}")
        print(f"PATRÓN 1: CONVERSACIÓN SIMPLE")
        print("="*70)

        question = f"Explícame brevemente: {topic}"
        print(f"\nPregunta: {question}\n")

        response = self._call_ollama(question)

        if response.startswith("Error"):
            return response

        print(f"Respuesta:\n{response[:300]}...")

        return response

    def iterative_conversation(self, initial_topic):
        """Patrón 2: Conversación iterativa (múltiples turnos)"""
        print(f"\n{'═'*70}")
        print(f"PATRÓN 2: CONVERSACIÓN ITERATIVA")
        print("="*70)

        conversation = []

        # Turno 1
        q1 = f"¿Qué es {initial_topic}?"
        print(f"\n[Turno 1] Pregunta: {q1}")
        r1 = self._call_ollama(q1)

        if r1.startswith("Error"):
            return r1

        print(f"Respuesta: {r1[:150]}...\n")
        conversation.append({"q": q1, "a": r1})

        # Turno 2
        q2 = f"¿Cuáles son los beneficios principales de {initial_topic}?"
        print(f"[Turno 2] Pregunta: {q2}")
        r2 = self._call_ollama(q2)
        print(f"Respuesta: {r2[:150]}...\n")
        conversation.append({"q": q2, "a": r2})

        # Turno 3
        q3 = f"¿Cómo se usa {initial_topic} en la práctica?"
        print(f"[Turno 3] Pregunta: {q3}")
        r3 = self._call_ollama(q3)
        print(f"Respuesta: {r3[:150]}...\n")
        conversation.append({"q": q3, "a": r3})

        self.conversations.append({
            "type": "iterative",
            "topic": initial_topic,
            "turns": conversation,
            "timestamp": datetime.now().isoformat()
        })

        return conversation

    def collaborative_conversation(self):
        """Patrón 3: Conversación colaborativa (múltiples agentes)"""
        print(f"\n{'═'*70}")
        print(f"PATRÓN 3: CONVERSACIÓN COLABORATIVA")
        print("="*70)

        topic = "Machine Learning"

        # Agente 1: Explicador
        print(f"\nAgente 1 - Explicador:")
        print(f"Pregunta: ¿Qué es {topic}?")
        q1 = f"Explica {topic} de forma académica"
        r1 = self._call_ollama(q1, "Eres un académico explicando conceptos")

        if r1.startswith("Error"):
            return r1

        print(f"Respuesta: {r1[:150]}...\n")

        # Agente 2: Crítico
        print(f"Agente 2 - Crítico:")
        print(f"Pregunta: ¿Cuáles son las limitaciones de {topic}?")
        q2 = f"Critica y señala limitaciones de {topic}"
        r2 = self._call_ollama(q2, "Eres un crítico analizando limitaciones")
        print(f"Respuesta: {r2[:150]}...\n")

        # Agente 3: Práctico
        print(f"Agente 3 - Práctico:")
        print(f"Pregunta: ¿Cómo se aplica {topic} en el mundo real?")
        q3 = f"Explica aplicaciones prácticas de {topic}"
        r3 = self._call_ollama(q3, "Eres un ingeniero enfocado en aplicaciones prácticas")
        print(f"Respuesta: {r3[:150]}...\n")

        return [
            {"agent": "Explicador", "response": r1},
            {"agent": "Crítico", "response": r2},
            {"agent": "Práctico", "response": r3}
        ]

    def print_stats(self):
        """Imprimir estadísticas"""
        print(f"\n{'═'*70}")
        print("ESTADÍSTICAS DE CONVERSACIONES")
        print("="*70)
        print(f"Total de conversaciones: {len(self.conversations)}")
        for i, conv in enumerate(self.conversations, 1):
            print(f"  {i}. {conv['type']}: {conv['topic']}")
        print("="*70 + "\n")


def main():
    """Demostración de patrones de conversación"""
    print("="*70)
    print(" MÓDULO 3: PATRONES DE CONVERSACIÓN")
    print("="*70)

    manager = ConversationManager()

    # Patrón 1: Simple
    result1 = manager.simple_conversation("Programación")

    if result1.startswith("Error"):
        print(f"\n❌ {result1}")
        print("\nPara usar este ejemplo:")
        print("1. Instala Ollama: https://ollama.ai")
        print("2. Ejecuta: ollama serve")
        print("3. Descarga un modelo: ollama pull mistral")
        return

    # Patrón 2: Iterativo
    result2 = manager.iterative_conversation("Python")

    # Patrón 3: Colaborativo
    result3 = manager.collaborative_conversation()

    # Estadísticas
    manager.print_stats()


if __name__ == "__main__":
    main()
