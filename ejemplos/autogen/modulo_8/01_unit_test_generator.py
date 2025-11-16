"""
Módulo 8: Testing y Debugging
Ejemplo 1: Unit Test Generator - Generación automática de tests
"""

import requests
from datetime import datetime


class UnitTestGenerator:
    """Generador automático de tests unitarios"""

    def __init__(self, base_url="http://localhost:11434", model="mistral"):
        self.base_url = base_url
        self.model = model
        self.generated_tests = []

    def _call_ollama(self, prompt):
        """Hacer llamada a Ollama"""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": 0.6,
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

    def generate_unit_tests(self, code, framework="pytest"):
        """Generar tests unitarios"""
        prompt = f"""
Genera tests unitarios usando {framework} para este código:

```python
{code}
```

Incluye:
1. Tests para casos normales
2. Tests para casos extremos
3. Tests para manejo de errores
4. Mocking si es necesario
5. Cobertura completa
"""
        result = self._call_ollama(prompt)
        self.generated_tests.append({"type": "unit", "code": code, "tests": result})
        return result

    def generate_integration_tests(self, system_description):
        """Generar tests de integración"""
        prompt = f"""
Genera tests de integración para este sistema:

{system_description}

Los tests deben:
1. Probar interacciones entre componentes
2. Verificar flujos completos
3. Usar fixtures y setup/teardown
4. Incluir tests de datos reales
"""
        return self._call_ollama(prompt)

    def suggest_test_coverage(self, code):
        """Sugerir estrategia de cobertura"""
        prompt = f"""
Analiza este código y sugiere una estrategia de testing:

```python
{code}
```

Proporciona:
1. Casos de prueba críticos
2. Caminos de ejecución importantes
3. Condiciones límite
4. Errores esperados
5. Meta de cobertura recomendada
"""
        return self._call_ollama(prompt)

    def get_generated_tests_count(self):
        """Obtener cantidad de tests generados"""
        return len(self.generated_tests)

    def print_summary(self):
        """Imprimir resumen"""
        print("\n" + "="*60)
        print("RESUMEN DE TESTS GENERADOS")
        print("="*60)
        print(f"Total de suites generadas: {self.get_generated_tests_count()}")
        print("="*60 + "\n")


def main():
    """Demostración del Test Generator"""
    print("Demostración: Unit Test Generator")
    print("-" * 60)

    generator = UnitTestGenerator()

    # Código de ejemplo
    sample_code = """
def calculate_bmi(weight, height):
    '''Calculate BMI from weight (kg) and height (m)'''
    if height <= 0:
        raise ValueError("Height must be positive")
    if weight <= 0:
        raise ValueError("Weight must be positive")

    bmi = weight / (height ** 2)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    return round(bmi, 1), category
"""

    print("\n📝 CASO 1: Generación de Tests Unitarios")
    print("="*60)
    print("Código a testear:")
    print("-" * 40)
    print(sample_code)
    print("-" * 40)
    print("\nGenerando tests con pytest...\n")

    tests = generator.generate_unit_tests(sample_code, "pytest")

    if tests.startswith("Error"):
        print(f"❌ {tests}")
        print("\nPara usar este ejemplo:")
        print("1. Instala Ollama: https://ollama.ai")
        print("2. Ejecuta: ollama serve")
        print("3. Descarga un modelo: ollama pull mistral")
        return
    else:
        print("✓ Tests generados:")
        print("-" * 40)
        print(tests[:500])
        if len(tests) > 500:
            print("... (tests continúan)")
        print("-" * 40)

    # Caso 2: Cobertura
    print("\n🎯 CASO 2: Análisis de Cobertura")
    print("="*60)
    print("Analizando cobertura recomendada...\n")

    coverage = generator.suggest_test_coverage(sample_code)

    if not coverage.startswith("Error"):
        print("✓ Estrategia de cobertura:")
        print("-" * 40)
        print(coverage[:400])
        if len(coverage) > 400:
            print("... (análisis continúa)")
        print("-" * 40)

    # Resumen
    generator.print_summary()


if __name__ == "__main__":
    main()
