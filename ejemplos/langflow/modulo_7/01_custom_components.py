"""
Módulo 7: Componentes Personalizados
Ejemplo 1: Crear y registrar componentes personalizados
"""

from datetime import datetime
from abc import ABC, abstractmethod


class CustomComponent(ABC):
    """Clase base para componentes personalizados"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.inputs = {}
        self.outputs = {}
        self.execution_count = 0
        self.created_at = datetime.now()

    @abstractmethod
    def execute(self, **kwargs):
        """Ejecutar el componente"""
        pass

    def get_metadata(self):
        """Obtener metadatos del componente"""
        return {
            "name": self.name,
            "description": self.description,
            "inputs": list(self.inputs.keys()),
            "outputs": list(self.outputs.keys()),
            "executions": self.execution_count,
            "created": self.created_at.isoformat()
        }


class TextToUpperComponent(CustomComponent):
    """Componente personalizado: convertir texto a mayúsculas"""

    def __init__(self):
        super().__init__(
            "TextToUpper",
            "Convierte texto a mayúsculas"
        )
        self.inputs = {"text": "string"}
        self.outputs = {"result": "string"}

    def execute(self, text: str) -> str:
        """Ejecutar transformación"""
        self.execution_count += 1
        result = text.upper()
        self.outputs["result"] = result
        return result


class TextLengthComponent(CustomComponent):
    """Componente personalizado: calcular longitud de texto"""

    def __init__(self):
        super().__init__(
            "TextLength",
            "Calcula la longitud del texto"
        )
        self.inputs = {"text": "string"}
        self.outputs = {"length": "number"}

    def execute(self, text: str) -> int:
        """Calcular longitud"""
        self.execution_count += 1
        length = len(text)
        self.outputs["length"] = length
        return length


class SentimentAnalysisComponent(CustomComponent):
    """Componente personalizado: análisis de sentimientos"""

    def __init__(self):
        super().__init__(
            "SentimentAnalysis",
            "Analiza el sentimiento del texto"
        )
        self.inputs = {"text": "string"}
        self.outputs = {"sentiment": "string", "score": "number"}

    def execute(self, text: str) -> dict:
        """Analizar sentimiento"""
        self.execution_count += 1

        # Simular análisis
        positive_words = ["bueno", "excelente", "maravilloso", "fantástico", "amor"]
        negative_words = ["malo", "horrible", "odio", "terrible", "decepción"]

        sentiment_score = 0
        for word in positive_words:
            sentiment_score += text.lower().count(word)
        for word in negative_words:
            sentiment_score -= text.lower().count(word)

        if sentiment_score > 0:
            sentiment = "positive"
        elif sentiment_score < 0:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        result = {"sentiment": sentiment, "score": sentiment_score}
        self.outputs.update(result)

        return result


class ComponentRegistry:
    """Registro de componentes personalizados"""

    def __init__(self):
        self.components = {}

    def register(self, component: CustomComponent):
        """Registrar componente"""
        self.components[component.name] = component

    def get_component(self, name: str) -> CustomComponent:
        """Obtener componente por nombre"""
        return self.components.get(name)

    def list_components(self) -> list:
        """Listar todos los componentes"""
        return list(self.components.values())

    def use_component(self, name: str, **kwargs):
        """Usar un componente registrado"""
        component = self.get_component(name)
        if component:
            return component.execute(**kwargs)
        return None

    def print_registry(self):
        """Imprimir registro de componentes"""
        print("\n📚 REGISTRO DE COMPONENTES PERSONALIZADOS\n")

        for comp in self.list_components():
            metadata = comp.get_metadata()
            print(f"  {metadata['name']}")
            print(f"    Descripción: {metadata['description']}")
            print(f"    Inputs: {', '.join(metadata['inputs'])}")
            print(f"    Outputs: {', '.join(metadata['outputs'])}")
            print(f"    Ejecuciones: {metadata['executions']}")
            print()


def main():
    """Demostración de componentes personalizados"""
    print("="*70)
    print(" MÓDULO 7: COMPONENTES PERSONALIZADOS")
    print("="*70)

    # Crear registro
    registry = ComponentRegistry()

    # Registrar componentes
    print("\n✏️  REGISTRANDO COMPONENTES\n")

    components = [
        TextToUpperComponent(),
        TextLengthComponent(),
        SentimentAnalysisComponent()
    ]

    for comp in components:
        registry.register(comp)
        print(f"  ✓ {comp.name} registrado")

    # Usar componentes
    print("\n🚀 USANDO COMPONENTES\n")

    test_text = "¡Hola! Este es un texto de prueba excelente"

    # Componente 1
    print("[1] TextToUpper")
    result1 = registry.use_component("TextToUpper", text=test_text)
    print(f"    Resultado: {result1}\n")

    # Componente 2
    print("[2] TextLength")
    result2 = registry.use_component("TextLength", text=test_text)
    print(f"    Resultado: {result2} caracteres\n")

    # Componente 3
    print("[3] SentimentAnalysis")
    result3 = registry.use_component("SentimentAnalysis", text=test_text)
    print(f"    Sentimiento: {result3['sentiment']}")
    print(f"    Score: {result3['score']}\n")

    # Mostrar registro
    registry.print_registry()

    print("="*70 + "\n")


if __name__ == "__main__":
    main()
