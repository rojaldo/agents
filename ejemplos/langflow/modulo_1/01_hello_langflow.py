"""
Módulo 1: Introducción a Langflow
Ejemplo 1: Conceptos básicos de flujos y componentes
"""

from datetime import datetime


class LangflowComponent:
    """Componente base simulado de Langflow"""

    def __init__(self, name, component_type):
        self.name = name
        self.component_type = component_type
        self.inputs = {}
        self.outputs = {}
        self.created_at = datetime.now()

    def execute(self):
        """Ejecutar el componente"""
        raise NotImplementedError

    def get_info(self):
        """Obtener información del componente"""
        return {
            "name": self.name,
            "type": self.component_type,
            "created": self.created_at.isoformat()
        }


class InputComponent(LangflowComponent):
    """Componente de entrada de usuario"""

    def __init__(self):
        super().__init__("User Input", "input")

    def execute(self, user_message):
        """Procesar entrada del usuario"""
        self.outputs["message"] = user_message
        return user_message


class ChatOpenAIComponent(LangflowComponent):
    """Componente simulado de ChatOpenAI"""

    def __init__(self):
        super().__init__("ChatOpenAI", "llm")
        self.model = "gpt-4"

    def execute(self, prompt):
        """Simular respuesta del modelo"""
        responses = {
            "hola": "¡Hola! ¿Cómo estás?",
            "cómo funciona langflow": "Langflow es una plataforma visual para construir flujos con LLMs",
            "qué es un componente": "Un componente es un bloque reutilizable en Langflow",
            "cuéntame sobre ia": "La IA es inteligencia artificial que permite a máquinas aprender"
        }

        response = responses.get(prompt.lower(), f"Respuesta a: {prompt}")
        self.outputs["response"] = response
        return response


class OutputComponent(LangflowComponent):
    """Componente de salida"""

    def __init__(self):
        super().__init__("Chat Output", "output")

    def execute(self, message):
        """Mostrar salida"""
        self.outputs["final_message"] = message
        return message


class SimpleFlow:
    """Flujo Langflow simple"""

    def __init__(self):
        self.components = {}
        self.connections = []
        self.execution_history = []

    def add_component(self, component):
        """Agregar componente al flujo"""
        self.components[component.name] = component
        return component

    def connect(self, source_name, target_name):
        """Conectar dos componentes"""
        self.connections.append((source_name, target_name))

    def execute(self, user_message):
        """Ejecutar flujo"""
        print("\n" + "="*70)
        print("EJECUTANDO FLUJO LANGFLOW")
        print("="*70)

        # Paso 1: Entrada
        print("\n[1] INPUT COMPONENT")
        print(f"    Mensaje: {user_message}")
        input_comp = self.components.get("User Input")
        message = input_comp.execute(user_message)

        # Paso 2: LLM
        print("\n[2] CHAT OPENAI COMPONENT")
        llm_comp = self.components.get("ChatOpenAI")
        response = llm_comp.execute(message)
        print(f"    Respuesta: {response}")

        # Paso 3: Output
        print("\n[3] OUTPUT COMPONENT")
        output_comp = self.components.get("Chat Output")
        final = output_comp.execute(response)

        execution_record = {
            "timestamp": datetime.now().isoformat(),
            "input": user_message,
            "output": final
        }
        self.execution_history.append(execution_record)

        print("\n" + "="*70)
        return final

    def get_info(self):
        """Obtener información del flujo"""
        return {
            "components": len(self.components),
            "connections": len(self.connections),
            "executions": len(self.execution_history)
        }


def main():
    """Demostración de introducción a Langflow"""
    print("="*70)
    print(" MÓDULO 1: INTRODUCCIÓN A LANGFLOW")
    print("="*70)

    # Crear flujo
    print("\n🔧 Creando flujo Langflow...\n")

    flow = SimpleFlow()

    # Agregar componentes
    input_comp = flow.add_component(InputComponent())
    llm_comp = flow.add_component(ChatOpenAIComponent())
    output_comp = flow.add_component(OutputComponent())

    print(f"  ✓ {input_comp.name} agregado")
    print(f"  ✓ {llm_comp.name} agregado")
    print(f"  ✓ {output_comp.name} agregado")

    # Conectar componentes
    print("\n📊 Conectando componentes...\n")

    flow.connect("User Input", "ChatOpenAI")
    flow.connect("ChatOpenAI", "Chat Output")

    print("  ✓ User Input → ChatOpenAI")
    print("  ✓ ChatOpenAI → Chat Output")

    # Visualizar flujo
    print("\n📐 Visualización del flujo:\n")
    print("  [User Input]")
    print("       ↓")
    print("  [ChatOpenAI]")
    print("       ↓")
    print("  [Chat Output]")

    # Ejecutar flujo con diferentes inputs
    print("\n🚀 Ejecutando flujo...\n")

    test_messages = [
        "Hola",
        "Cómo funciona Langflow",
        "Qué es un componente"
    ]

    for msg in test_messages:
        flow.execute(msg)
        print()

    # Mostrar resumen
    print("\n" + "="*70)
    print("RESUMEN DEL FLUJO")
    print("="*70)

    info = flow.get_info()
    print(f"\n✓ Componentes: {info['components']}")
    print(f"✓ Conexiones: {info['connections']}")
    print(f"✓ Ejecuciones: {info['executions']}")

    print(f"\n📝 Historial de ejecuciones:")
    for i, execution in enumerate(flow.execution_history, 1):
        print(f"\n  {i}. Input: {execution['input']}")
        print(f"     Output: {execution['output']}")

    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
