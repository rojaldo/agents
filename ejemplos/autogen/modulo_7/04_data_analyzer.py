"""
Módulo 7: Casos de Uso Prácticos
Ejemplo 4: Data Analyzer Agent - Análisis de datos con Ollama
"""

import requests
from datetime import datetime


class DataAnalyzerAgent:
    """Agente especializado en análisis de datos"""

    def __init__(self, base_url="http://localhost:11434", model="mistral"):
        self.base_url = base_url
        self.model = model
        self.analyses = []

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
                result = response.json().get('response', '')
                self.analyses.append({
                    "timestamp": datetime.now(),
                    "result": result
                })
                return result
            else:
                return f"Error: {response.status_code}"

        except requests.exceptions.ConnectionError:
            return "Error: No se puede conectar a Ollama. Ejecuta: ollama serve"
        except requests.exceptions.Timeout:
            return "Error: Timeout"
        except Exception as e:
            return f"Error: {str(e)}"

    def analyze_dataset_statistics(self, data_description):
        """Analizar estadísticas de un dataset"""
        prompt = f"""
Proporciona un análisis estadístico para este dataset:

{data_description}

Incluye:
1. Estadísticas descriptivas
2. Distribuciones
3. Correlaciones potenciales
4. Anomalías
5. Patrones interesantes
"""
        return self._call_ollama(prompt)

    def identify_patterns(self, data_info):
        """Identificar patrones en datos"""
        prompt = f"""
Identifica patrones y relaciones en estos datos:

{data_info}

Busca:
1. Tendencias temporales
2. Agrupamientos
3. Relaciones entre variables
4. Puntos de inflexión
5. Patrones cíclicos
"""
        return self._call_ollama(prompt)

    def suggest_visualizations(self, data_type):
        """Sugerir visualizaciones apropiadas"""
        prompt = f"""
Sugiere las mejores formas de visualizar este tipo de datos:

Tipo de datos: {data_type}

Para cada visualización, explica:
1. Tipo de gráfico
2. Variables a representar
3. Cuándo usarla
4. Ventajas y limitaciones
5. Ejemplos de código con matplotlib/seaborn
"""
        return self._call_ollama(prompt)

    def generate_insights(self, analysis_summary):
        """Generar insights de negocio"""
        prompt = f"""
Basado en este análisis de datos, genera insights de negocio:

{analysis_summary}

Proporciona:
1. Hallazgos principales
2. Implicaciones comerciales
3. Recomendaciones de acción
4. Métricas clave a monitorear
5. Próximos pasos sugeridos
"""
        return self._call_ollama(prompt)

    def get_analysis_count(self):
        """Obtener cantidad de análisis realizados"""
        return len(self.analyses)

    def print_summary(self):
        """Imprimir resumen"""
        print("\n" + "="*60)
        print("RESUMEN DE ANÁLISIS DE DATOS")
        print("="*60)
        print(f"Total de análisis realizados: {self.get_analysis_count()}")
        print("="*60 + "\n")


def main():
    """Demostración del Data Analyzer"""
    print("Demostración: Data Analyzer Agent")
    print("-" * 60)

    analyzer = DataAnalyzerAgent()

    print("\n📊 Agente de análisis de datos cargado")
    print(f"   Modelo: {analyzer.model}")

    # Simulación de datos
    sample_data = """
Dataset: Ventas mensuales de productos electrónicos
- 24 meses de datos históricos
- 5 categorías de productos (Smartphones, Laptops, Tablets, Accesorios, Otros)
- Variables: Ventas (en unidades), Ingresos (USD), Devoluciones (%)
- Rango: Enero 2022 - Diciembre 2023

Ejemplo de datos:
Mes 1: Smartphones 450 unidades ($22,500), Laptops 120 unidades ($36,000)
...
"""

    # Caso 1: Estadísticas
    print("\n📈 CASO 1: Análisis Estadístico")
    print("="*60)
    print("Analizando estadísticas del dataset...\n")

    stats = analyzer.analyze_dataset_statistics(sample_data)

    if stats.startswith("Error"):
        print(f"❌ {stats}")
        print("\nPara usar este ejemplo:")
        print("1. Instala Ollama: https://ollama.ai")
        print("2. Ejecuta: ollama serve")
        print("3. Descarga un modelo: ollama pull mistral")
        return
    else:
        print("✓ Análisis estadístico:")
        print("-" * 40)
        print(stats[:400])
        if len(stats) > 400:
            print("... (análisis continúa)")
        print("-" * 40)

    # Caso 2: Patrones
    print("\n🔍 CASO 2: Identificación de Patrones")
    print("="*60)
    print("Identificando patrones en los datos...\n")

    patterns = analyzer.identify_patterns(sample_data)

    if not patterns.startswith("Error"):
        print("✓ Patrones identificados:")
        print("-" * 40)
        print(patterns[:400])
        if len(patterns) > 400:
            print("... (patrones continúan)")
        print("-" * 40)

    # Caso 3: Visualizaciones
    print("\n📊 CASO 3: Sugerencias de Visualización")
    print("="*60)
    print("Sugiriendo visualizaciones...\n")

    visualizations = analyzer.suggest_visualizations("Series temporal multivariable con categorías")

    if not visualizations.startswith("Error"):
        print("✓ Visualizaciones sugeridas:")
        print("-" * 40)
        print(visualizations[:400])
        if len(visualizations) > 400:
            print("... (sugerencias continúan)")
        print("-" * 40)

    # Caso 4: Insights
    print("\n💡 CASO 4: Insights de Negocio")
    print("="*60)
    print("Generando insights...\n")

    insights_summary = """
    Hallazgo 1: Crecimiento del 35% en Smartphones Q2
    Hallazgo 2: Devoluciones de Laptops aumentaron 12%
    Hallazgo 3: Accesorios muestran patrón estacional
    """

    insights = analyzer.generate_insights(insights_summary)

    if not insights.startswith("Error"):
        print("✓ Insights generados:")
        print("-" * 40)
        print(insights[:400])
        if len(insights) > 400:
            print("... (insights continúan)")
        print("-" * 40)

    # Resumen
    analyzer.print_summary()


if __name__ == "__main__":
    main()
