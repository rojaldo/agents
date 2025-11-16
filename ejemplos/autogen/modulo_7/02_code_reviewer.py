"""
Módulo 7: Casos de Uso Prácticos
Ejemplo 2: Code Reviewer Agent - Revisión de código con análisis detallado
"""

import requests
from datetime import datetime


class CodeReviewerAgent:
    """Agente especializado en revisión de código"""

    def __init__(self, base_url="http://localhost:11434", model="mistral"):
        self.base_url = base_url
        self.model = model
        self.reviews = []
        self.issues_found = 0

    def review_code(self, code, language="python"):
        """Revisar código y sugerir mejoras"""
        prompt = f"""
Revisa este código {language} y proporciona un análisis detallado:
```{language}
{code}
```

Evalúa en estos aspectos:
1. **Legibilidad**: ¿Es fácil de entender?
2. **Performance**: ¿Hay optimizaciones posibles?
3. **Seguridad**: ¿Hay vulnerabilidades?
4. **Type hints**: ¿Tiene anotaciones de tipo?
5. **Documentación**: ¿Está bien documentado?
6. **Best Practices**: ¿Sigue los estándares?

Proporciona:
- Un resumen general
- Problemas encontrados
- Recomendaciones específicas
"""
        return self._call_ollama(prompt, language)

    def check_performance(self, code):
        """Analizar rendimiento del código"""
        prompt = f"""
Analiza el rendimiento de este código Python:
```python
{code}
```

Proporciona:
1. Complejidad temporal
2. Complejidad espacial
3. Posibles cuellos de botella
4. Optimizaciones recomendadas
"""
        return self._call_ollama(prompt, "python")

    def check_security(self, code):
        """Verificar vulnerabilidades de seguridad"""
        prompt = f"""
Revisa este código Python en busca de vulnerabilidades de seguridad:
```python
{code}
```

Busca:
1. Inyección de SQL
2. Inyección de código
3. Desbordamiento de búfer
4. Gestión insegura de contraseñas
5. Otras vulnerabilidades OWASP

Para cada problema encontrado, sugiere una solución.
"""
        return self._call_ollama(prompt, "python")

    def suggest_refactoring(self, code):
        """Sugerir refactorización"""
        prompt = f"""
Sugiere refactorizaciones para este código Python:
```python
{code}
```

Proporciona:
1. Problemas de diseño
2. Violaciones de SOLID
3. Oportunidades de simplificación
4. Código duplicado
5. Métodos muy largos
6. Refactorizaciones específicas con ejemplos
"""
        return self._call_ollama(prompt, "python")

    def _call_ollama(self, prompt, language="python"):
        """Hacer llamada a Ollama"""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": 0.5,  # Menor temperatura para análisis más consistente
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
                review = result.get('response', '')
                self.reviews.append({
                    "timestamp": datetime.now(),
                    "language": language,
                    "review": review
                })
                return review
            else:
                return f"Error: {response.status_code}"

        except requests.exceptions.ConnectionError:
            return "Error: No se puede conectar a Ollama. Ejecuta: ollama serve"
        except requests.exceptions.Timeout:
            return "Error: Timeout esperando respuesta"
        except Exception as e:
            return f"Error: {str(e)}"

    def get_review_count(self):
        """Obtener cantidad de revisiones realizadas"""
        return len(self.reviews)

    def print_stats(self):
        """Imprimir estadísticas"""
        print("\n" + "="*60)
        print("ESTADÍSTICAS DE REVISIONES")
        print("="*60)
        print(f"Total de revisiones: {self.get_review_count()}")
        if self.reviews:
            last_review = self.reviews[-1]
            print(f"Última revisión: {last_review['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Lenguaje: {last_review['language']}")
        print("="*60 + "\n")


def main():
    """Demostración del Code Reviewer"""
    print("Demostración: Code Reviewer Agent")
    print("-" * 60)

    reviewer = CodeReviewerAgent()

    # Código de prueba (código de baja calidad a propósito)
    bad_code = """
def calc(x,y,z):
    result = 0
    for i in range(x):
        for j in range(y):
            for k in range(z):
                result = result + 1
    return result

def process(data):
    print(data)
    x = []
    for i in data:
        x.append(i * 2)
    return x
"""

    print("\n📝 CASO 1: Revisión General de Código")
    print("="*60)
    print("Código a revisar:")
    print("-" * 40)
    print(bad_code)
    print("-" * 40)
    print("\nAnalizando código...\n")

    review = reviewer.review_code(bad_code)

    if review.startswith("Error"):
        print(f"❌ {review}")
        print("\nPara usar este ejemplo:")
        print("1. Instala Ollama: https://ollama.ai")
        print("2. Ejecuta: ollama serve")
        print("3. Descarga un modelo: ollama pull mistral")
        return
    else:
        print("✓ Análisis de revisión:")
        print("-" * 40)
        print(review[:600])
        if len(review) > 600:
            print("... (análisis continúa)")
        print("-" * 40)

    # Caso 2: Análisis de performance
    print("\n📊 CASO 2: Análisis de Rendimiento")
    print("="*60)
    print("Analizando rendimiento...\n")

    perf_analysis = reviewer.check_performance(bad_code)

    if not perf_analysis.startswith("Error"):
        print("✓ Análisis de rendimiento:")
        print("-" * 40)
        print(perf_analysis[:500])
        if len(perf_analysis) > 500:
            print("... (análisis continúa)")
        print("-" * 40)

    # Caso 3: Refactorización
    print("\n♻️  CASO 3: Sugerencias de Refactorización")
    print("="*60)
    print("Generando sugerencias...\n")

    refactor = reviewer.suggest_refactoring(bad_code)

    if not refactor.startswith("Error"):
        print("✓ Sugerencias de refactorización:")
        print("-" * 40)
        print(refactor[:500])
        if len(refactor) > 500:
            print("... (sugerencias continúan)")
        print("-" * 40)

    # Estadísticas
    reviewer.print_stats()


if __name__ == "__main__":
    main()
