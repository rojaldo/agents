"""
Módulo 7: Casos de Uso Prácticos
Ejemplo 3: Programming Team - Sistema de desarrollo colaborativo
"""

import requests
from datetime import datetime


class ProgrammingTeam:
    """Equipo de desarrollo colaborativo con múltiples especialistas simulados"""

    def __init__(self, base_url="http://localhost:11434", model="mistral"):
        self.base_url = base_url
        self.model = model
        self.artifacts = {
            "code": [],
            "tests": [],
            "docs": [],
            "reviews": []
        }
        self.team_members = {
            "generator": "Code Generator",
            "reviewer": "Code Reviewer",
            "tester": "Test Writer",
            "documenter": "Documenter"
        }

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

    def develop_feature(self, feature_spec):
        """Desarrollo completo de una feature"""
        print(f"\n🚀 Iniciando desarrollo de feature: {feature_spec}")
        print("="*60)

        results = {
            "spec": feature_spec,
            "timestamp": datetime.now(),
            "stages": {}
        }

        # 1. Generación de código
        print("\n1️⃣  Generando código...")
        code_prompt = f"""
Genera código Python para esta feature:
{feature_spec}

Requisitos:
- Code limpio y documentado
- Type hints
- Manejo de errores
"""
        code = self._call_ollama(code_prompt)
        results["stages"]["code"] = code
        self.artifacts["code"].append(code)

        if not code.startswith("Error"):
            print("✓ Código generado")
            print("-" * 40)
            print(code[:200] + "..." if len(code) > 200 else code)
            print("-" * 40)
        else:
            return results

        # 2. Revisión de código
        print("\n2️⃣  Revisando código...")
        review_prompt = f"""
Revisa brevemente este código y sugiere mejoras:
```python
{code}
```
"""
        review = self._call_ollama(review_prompt)
        results["stages"]["review"] = review
        self.artifacts["reviews"].append(review)

        if not review.startswith("Error"):
            print("✓ Revisión completada")
            print("-" * 40)
            print(review[:200] + "..." if len(review) > 200 else review)
            print("-" * 40)

        # 3. Generación de tests
        print("\n3️⃣  Generando tests...")
        test_prompt = f"""
Genera tests unitarios para este código:
```python
{code}
```

Usa unittest o pytest.
"""
        tests = self._call_ollama(test_prompt)
        results["stages"]["tests"] = tests
        self.artifacts["tests"].append(tests)

        if not tests.startswith("Error"):
            print("✓ Tests generados")
            print("-" * 40)
            print(tests[:200] + "..." if len(tests) > 200 else tests)
            print("-" * 40)

        # 4. Documentación
        print("\n4️⃣  Generando documentación...")
        doc_prompt = f"""
Crea documentación para este código:
```python
{code}
```

Incluye:
- Descripción general
- Parámetros
- Ejemplos de uso
"""
        docs = self._call_ollama(doc_prompt)
        results["stages"]["docs"] = docs
        self.artifacts["docs"].append(docs)

        if not docs.startswith("Error"):
            print("✓ Documentación generada")
            print("-" * 40)
            print(docs[:200] + "..." if len(docs) > 200 else docs)
            print("-" * 40)

        print("\n✅ Feature desarrollada exitosamente")

        return results

    def debug_code(self, code, error_message):
        """Debugging colaborativo"""
        print(f"\n🐛 Debugging: {error_message}")
        print("="*60)

        results = {
            "original_error": error_message,
            "timestamp": datetime.now(),
            "stages": {}
        }

        # Análisis del error
        print("\n1️⃣  Analizando error...")
        analysis_prompt = f"""
Analiza este error en el código:

Código:
```python
{code}
```

Error:
{error_message}

¿Cuál es la causa?
"""
        analysis = self._call_ollama(analysis_prompt)
        results["stages"]["analysis"] = analysis

        if not analysis.startswith("Error"):
            print("✓ Análisis completado")

        # Generar fix
        print("\n2️⃣  Generando solución...")
        fix_prompt = f"""
Corrige este código:
```python
{code}
```

Error: {error_message}

Proporciona el código corregido.
"""
        fix = self._call_ollama(fix_prompt)
        results["stages"]["fix"] = fix

        if not fix.startswith("Error"):
            print("✓ Solución generada")
            print("-" * 40)
            print(fix[:300] + "..." if len(fix) > 300 else fix)
            print("-" * 40)

        return results

    def get_artifacts_summary(self):
        """Resumen de artefactos generados"""
        summary = {
            "total_code_files": len(self.artifacts["code"]),
            "total_tests": len(self.artifacts["tests"]),
            "total_docs": len(self.artifacts["docs"]),
            "total_reviews": len(self.artifacts["reviews"]),
            "team_members": self.team_members
        }
        return summary

    def print_summary(self):
        """Imprimir resumen del equipo"""
        summary = self.get_artifacts_summary()
        print("\n" + "="*60)
        print("RESUMEN DEL EQUIPO DE DESARROLLO")
        print("="*60)
        print(f"Miembros del equipo: {', '.join(summary['team_members'].values())}")
        print(f"\nArtefactos generados:")
        print(f"  - Archivos de código: {summary['total_code_files']}")
        print(f"  - Tests: {summary['total_tests']}")
        print(f"  - Documentación: {summary['total_docs']}")
        print(f"  - Revisiones: {summary['total_reviews']}")
        print("="*60 + "\n")


def main():
    """Demostración del Programming Team"""
    print("Demostración: Programming Team - Sistema Colaborativo")
    print("-" * 60)

    team = ProgrammingTeam()

    print("\n👥 Equipo de desarrollo cargado")
    for role, member in team.team_members.items():
        print(f"   - {member}")

    # Feature 1: Función simple
    feature_spec = """
    Una función que calcule el factorial de un número
    - Entrada: número entero positivo
    - Salida: factorial del número
    - Manejo de errores para números negativos
    """

    result = team.develop_feature(feature_spec)

    if result["stages"]["code"].startswith("Error"):
        print("\n⚠️  No se puede conectar a Ollama")
        print("Para usar este ejemplo:")
        print("1. Instala Ollama: https://ollama.ai")
        print("2. Ejecuta: ollama serve")
        print("3. Descarga un modelo: ollama pull mistral")
        return

    # Debug de ejemplo
    print("\n" + "="*60)
    print("SIMULANDO DEBUGGING")
    print("="*60)

    bad_code = """
def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n-1)
"""

    error_msg = "RecursionError: maximum recursion depth exceeded"

    debug_result = team.debug_code(bad_code, error_msg)

    # Resumen
    team.print_summary()


if __name__ == "__main__":
    main()
