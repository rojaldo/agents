"""
Módulo 11: Proyecto Final
Ejemplo 1: Final Project - Sistema completo de análisis de código
"""

import requests
from datetime import datetime
from collections import defaultdict


class CodeAnalysisProject:
    """Proyecto final: Sistema de análisis de código con múltiples agentes"""

    def __init__(self, base_url="http://localhost:11434", model="mistral"):
        self.base_url = base_url
        self.model = model
        self.project_name = "CodeAnalyzer"
        self.agents = {
            "generator": "Code Generator",
            "analyzer": "Code Analyzer",
            "reviewer": "Code Reviewer",
            "documenter": "Documenter"
        }
        self.artifacts = defaultdict(list)
        self.metrics = {
            "total_analyses": 0,
            "issues_found": 0,
            "suggestions_made": 0,
            "success_rate": 0.0
        }
        self.start_time = datetime.now()

    def _call_ollama(self, prompt, timeout=30):
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
                timeout=timeout
            )

            if response.status_code == 200:
                return response.json().get('response', '')
            else:
                return f"Error: {response.status_code}"

        except requests.exceptions.ConnectionError:
            return "Error: No se puede conectar a Ollama"
        except requests.exceptions.Timeout:
            return "Error: Timeout"
        except Exception as e:
            return f"Error: {str(e)}"

    def analyze_code(self, code, analysis_type="comprehensive"):
        """Análisis integral de código"""
        print(f"\n🔍 Analizando código ({analysis_type})...")

        prompt = f"""
Realiza un análisis {analysis_type} de este código Python:

```python
{code}
```

Para análisis completo, incluye:
1. Calidad del código
2. Posibles bugs
3. Performance
4. Seguridad
5. Mejoras sugeridas
"""

        result = self._call_ollama(prompt)
        self.artifacts["analyses"].append({
            "type": analysis_type,
            "timestamp": datetime.now(),
            "result": result
        })

        self.metrics["total_analyses"] += 1

        return result

    def generate_documentation(self, code):
        """Generar documentación automática"""
        print(f"\n📚 Generando documentación...")

        prompt = f"""
Crea documentación clara y profesional para este código:

```python
{code}
```

Incluye:
1. Descripción general
2. Parámetros y tipos
3. Valor de retorno
4. Ejemplos de uso
5. Excepciones posibles
"""

        result = self._call_ollama(prompt)
        self.artifacts["documentation"].append({
            "timestamp": datetime.now(),
            "content": result
        })

        return result

    def generate_tests(self, code):
        """Generar tests automáticos"""
        print(f"\n✅ Generando tests unitarios...")

        prompt = f"""
Genera tests unitarios exhaustivos para este código con pytest:

```python
{code}
```

Incluye:
1. Tests para casos normales
2. Tests para casos extremos
3. Tests para manejo de errores
4. Tests de performance si aplica
"""

        result = self._call_ollama(prompt)
        self.artifacts["tests"].append({
            "timestamp": datetime.now(),
            "tests": result
        })

        return result

    def create_report(self):
        """Crear reporte final del proyecto"""
        print(f"\n📊 Compilando reporte final...")

        uptime = datetime.now() - self.start_time

        report = {
            "project_name": self.project_name,
            "timestamp": datetime.now().isoformat(),
            "uptime": str(uptime),
            "agents": self.agents,
            "metrics": {
                "total_analyses": self.metrics["total_analyses"],
                "analyses_generated": len(self.artifacts["analyses"]),
                "documentation_generated": len(self.artifacts["documentation"]),
                "test_suites_generated": len(self.artifacts["tests"]),
                "success_rate": self.calculate_success_rate()
            }
        }

        return report

    def calculate_success_rate(self):
        """Calcular tasa de éxito"""
        total_operations = (
            len(self.artifacts["analyses"]) +
            len(self.artifacts["documentation"]) +
            len(self.artifacts["tests"])
        )

        if total_operations == 0:
            return 0.0

        successful = sum(1 for analysis in self.artifacts["analyses"]
                        if not analysis["result"].startswith("Error"))
        successful += len(self.artifacts["documentation"])
        successful += len(self.artifacts["tests"])

        return (successful / total_operations) * 100 if total_operations > 0 else 0.0

    def run_complete_workflow(self, code):
        """Ejecutar flujo completo"""
        print(f"\n{'='*70}")
        print(f"PROYECTO FINAL: {self.project_name}")
        print("="*70)

        print(f"\n👥 Agentes disponibles:")
        for role, name in self.agents.items():
            print(f"   - {name}")

        # Paso 1: Análisis
        analysis = self.analyze_code(code)

        if analysis.startswith("Error"):
            print(f"❌ {analysis}")
            print("\nPara usar este ejemplo:")
            print("1. Instala Ollama: https://ollama.ai")
            print("2. Ejecuta: ollama serve")
            print("3. Descarga un modelo: ollama pull mistral")
            return None

        print(f"✓ Análisis completado")
        print(f"  Resultado: {analysis[:150]}...")

        # Paso 2: Documentación
        docs = self.generate_documentation(code)
        if not docs.startswith("Error"):
            print(f"✓ Documentación generada")

        # Paso 3: Tests
        tests = self.generate_tests(code)
        if not tests.startswith("Error"):
            print(f"✓ Tests generados")

        # Paso 4: Reporte
        report = self.create_report()

        return report

    def print_final_report(self, report):
        """Imprimir reporte final"""
        if not report:
            return

        print(f"\n{'='*70}")
        print("REPORTE FINAL DEL PROYECTO")
        print("="*70)

        print(f"\n📋 Información del Proyecto:")
        print(f"   Nombre: {report['project_name']}")
        print(f"   Timestamp: {report['timestamp']}")
        print(f"   Duración: {report['uptime']}")

        print(f"\n📊 Métricas:")
        metrics = report['metrics']
        print(f"   Análisis totales: {metrics['total_analyses']}")
        print(f"   Documentación generada: {metrics['documentation_generated']}")
        print(f"   Suites de tests generadas: {metrics['test_suites_generated']}")
        print(f"   Tasa de éxito: {metrics['success_rate']:.1f}%")

        print(f"\n👥 Agentes Utilizados:")
        for role, name in report['agents'].items():
            print(f"   - {name}")

        print("="*70 + "\n")


def main():
    """Función principal"""
    print("Demostración: Final Project - Sistema de Análisis de Código")
    print("-" * 70)

    # Código de prueba
    sample_code = """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# Ejemplo de uso
if __name__ == "__main__":
    data = [64, 34, 25, 12, 22, 11, 90]
    print(bubble_sort(data))
"""

    # Crear proyecto
    project = CodeAnalysisProject()

    # Ejecutar flujo completo
    report = project.run_complete_workflow(sample_code)

    # Mostrar reporte
    project.print_final_report(report)


if __name__ == "__main__":
    main()
