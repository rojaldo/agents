"""
Módulo 5: Casos de Uso Prácticos
Ejemplo 1: Sistema de investigación y análisis de mercado
"""

from datetime import datetime


class ResearchCrew:
    """Crew para investigación de mercado"""

    def __init__(self):
        self.researcher = {
            "role": "Investigador de Mercado",
            "goal": "Recopilar datos de mercado confiables"
        }
        self.analyst = {
            "role": "Analista Estratégico",
            "goal": "Generar insights accionables"
        }
        self.reporter = {
            "role": "Redactor Ejecutivo",
            "goal": "Presentar hallazgos de forma clara"
        }
        self.findings = []

    def research_market(self, market_topic):
        """Fase 1: Investigación"""
        print(f"\n[1] INVESTIGACIÓN")
        print(f"    Investigador: {self.researcher['role']}")
        print(f"    Tema: {market_topic}")

        findings = {
            "timestamp": datetime.now().isoformat(),
            "topic": market_topic,
            "research_findings": [
                "Tendencia 1: Crecimiento del 25% en IA",
                "Tendencia 2: Aumento en adopción empresarial",
                "Tendencia 3: Nuevas regulaciones en preparación",
                "Tendencia 4: Mayor enfoque en seguridad",
                "Tendencia 5: Competencia intensificada"
            ]
        }

        self.findings.append(findings)
        print(f"    ✓ 5 tendencias identificadas")
        return findings

    def analyze_findings(self):
        """Fase 2: Análisis"""
        if not self.findings:
            return None

        print(f"\n[2] ANÁLISIS")
        print(f"    Analista: {self.analyst['role']}")

        analysis = {
            "implications": [
                "Oportunidad: Empresas con soluciones completas liderarán",
                "Riesgo: Falta de regulación clara genera incertidumbre",
                "Estrategia: Enfoque en diferenciación y seguridad",
                "Recomendación: Inversión en investigación y desarrollo"
            ],
            "market_size": "$500B en 2024",
            "growth_rate": "25% anual"
        }

        print(f"    ✓ Análisis completado")
        print(f"    Tamaño de mercado estimado: {analysis['market_size']}")
        print(f"    Tasa de crecimiento: {analysis['growth_rate']}")
        return analysis

    def generate_report(self):
        """Fase 3: Reporte"""
        print(f"\n[3] GENERACIÓN DE REPORTE")
        print(f"    Reportero: {self.reporter['role']}")

        report = {
            "title": "Análisis de Mercado de IA 2024",
            "executive_summary": "El mercado de IA continúa creciendo con oportunidades significativas",
            "sections": {
                "Tendencias": 5,
                "Análisis": 4,
                "Recomendaciones": 3
            },
            "generated_at": datetime.now().isoformat()
        }

        print(f"    ✓ Reporte: {report['title']}")
        print(f"    Secciones: {len(report['sections'])}")
        return report

    def kickoff(self, market_topic):
        """Ejecutar crew completo"""
        print("="*70)
        print("CREW DE INVESTIGACIÓN DE MERCADO")
        print("="*70)

        # Ejecutar fases
        research = self.research_market(market_topic)
        analysis = self.analyze_findings()
        report = self.generate_report()

        print("\n" + "="*70)
        print("RESUMEN DE EJECUCIÓN")
        print("="*70)
        print(f"\n✓ Investigación completada")
        print(f"✓ Análisis realizado")
        print(f"✓ Reporte generado")
        print(f"\nTipo de reporte: {report['title']}")
        print(f"Generado: {report['generated_at']}")

        return {
            "research": research,
            "analysis": analysis,
            "report": report
        }


def main():
    """Demostración de casos de uso prácticos"""
    print("="*70)
    print(" MÓDULO 5: CASOS DE USO PRÁCTICOS")
    print("="*70)

    # Crear crew de investigación
    crew = ResearchCrew()

    # Ejecutar
    result = crew.kickoff("Mercado de Inteligencia Artificial")

    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
