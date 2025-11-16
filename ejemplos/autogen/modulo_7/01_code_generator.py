"""
Módulo 7: Casos de Uso Prácticos
Ejemplo 1: Code Generator Agent - Generación de código con Ollama
"""

import requests


class CodeGeneratorAgent:
    """Agente especializado en generación de código con Ollama"""

    def __init__(self, base_url="http://localhost:11434", model="mistral"):
        self.base_url = base_url
        self.model = model
        self.language = "python"
        self.generated_code = []

    def generate_function(self, requirements):
        """Generar función basada en requisitos"""
        prompt = f"""
Genera una función Python que cumpla estos requisitos:
{requirements}

Requisitos:
- Incluye docstring completo
- Manejo de errores
- Type hints
- Ejemplos de uso

Devuelve solo el código Python, sin explicaciones adicionales.
"""
        return self._call_ollama(prompt)

    def generate_class(self, class_name, methods):
        """Generar clase con métodos"""
        methods_str = ", ".join(methods)
        prompt = f"""
Crea una clase {class_name} con estos métodos: {methods_str}

Requisitos:
- Usa type hints
- Docstrings claros
- Patrón de diseño SOLID
- Constructor adecuado
- Métodos bien documentados

Devuelve solo el código Python.
"""
        return self._call_ollama(prompt)

    def review_code(self, code):
        """Revisar código y sugerir mejoras"""
        prompt = f"""
Revisa este código Python y sugiere mejoras:
```python
{code}
```

Evalúa:
1. Legibilidad
2. Performance
3. Seguridad
4. Type hints
5. Documentación

Proporciona un análisis detallado.
"""
        return self._call_ollama(prompt)

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
                result = response.json()
                code = result.get('response', '')
                self.generated_code.append(code)
                return code
            else:
                return f"Error: {response.status_code}"

        except requests.exceptions.ConnectionError:
            return "Error: No se puede conectar a Ollama. Ejecuta: ollama serve"
        except requests.exceptions.Timeout:
            return "Error: Timeout esperando respuesta de Ollama"
        except Exception as e:
            return f"Error: {str(e)}"

    def refactor_code(self, code):
        """Refactorización automática"""
        prompt = f"""
Refactoriza este código Python para mejorar:
1. Legibilidad
2. Mantenibilidad
3. Performance
4. Seguir best practices

```python
{code}
```

Devuelve solo el código refactorizado, sin explicaciones.
"""
        return self._call_ollama(prompt)

    def get_generated_count(self):
        """Obtener cantidad de códigos generados"""
        return len(self.generated_code)


def main():
    """Demostración del Code Generator"""
    print("Demostración: Code Generator Agent")
    print("-" * 60)

    agent = CodeGeneratorAgent()

    print(f"\n✅ Agente de generación de código configurado")
    print(f"   Modelo: {agent.model}")
    print(f"   Lenguaje: {agent.language}")

    # Caso 1: Generar función simple
    print("\n" + "="*60)
    print("📝 CASO 1: Generar función simple")
    print("="*60)

    requirements = """
    Una función que:
    - Reciba una lista de números
    - Retorne el promedio
    - Maneje excepciones si está vacía
    """

    print(f"Requisitos: {requirements}\n")
    print("Generando función...")

    code = agent.generate_function(requirements)

    if code.startswith("Error"):
        print(f"❌ {code}")
        print("\nPara usar este ejemplo:")
        print("1. Instala Ollama: https://ollama.ai")
        print("2. Ejecuta: ollama serve")
        print("3. Descarga un modelo: ollama pull mistral")
        return
    else:
        print("✓ Función generada:")
        print("-" * 40)
        print(code[:500])
        if len(code) > 500:
            print("... (código continúa)")
        print("-" * 40)

    # Caso 2: Generar clase
    print("\n" + "="*60)
    print("📝 CASO 2: Generar clase con métodos")
    print("="*60)

    class_name = "DataProcessor"
    methods = ["load", "validate", "process", "export"]

    print(f"Clase: {class_name}")
    print(f"Métodos: {', '.join(methods)}\n")
    print("Generando clase...")

    class_code = agent.generate_class(class_name, methods)

    if not class_code.startswith("Error"):
        print("✓ Clase generada:")
        print("-" * 40)
        print(class_code[:500])
        if len(class_code) > 500:
            print("... (código continúa)")
        print("-" * 40)

    # Caso 3: Revisar código
    print("\n" + "="*60)
    print("📝 CASO 3: Revisar código")
    print("="*60)

    code_to_review = """
def calculate_average(numbers):
    return sum(numbers) / len(numbers)
"""

    print(f"Código a revisar:")
    print("-" * 40)
    print(code_to_review)
    print("-" * 40)
    print("Analizando código...")

    review = agent.review_code(code_to_review)

    if not review.startswith("Error"):
        print("\n✓ Análisis de revisión:")
        print("-" * 40)
        print(review[:500])
        if len(review) > 500:
            print("... (análisis continúa)")
        print("-" * 40)

    # Estadísticas
    print("\n" + "="*60)
    print("📊 ESTADÍSTICAS")
    print("="*60)
    print(f"Total de códigos generados: {agent.get_generated_count()}")


if __name__ == "__main__":
    main()
