"""
Módulo 7: Mejores Prácticas
Ejemplo 1: Patrones de diseño efectivo para agentes y tareas
"""

from datetime import datetime


class BestPracticesDemo:
    """Demostración de mejores prácticas en CrewAI"""

    def __init__(self):
        self.execution_log = []

    def demonstrate_agent_design(self):
        """Mostrar principios de diseño efectivo de agentes"""
        print("\n" + "="*70)
        print("1. DISEÑO EFECTIVO DE AGENTES")
        print("="*70)

        # Ejemplo BIEN: Rol específico
        print("\n✓ BIEN - Rol específico y detallado:")
        good_agent = {
            "role": "Analista de Tendencias de Mercado Senior",
            "goal": "Identificar 5-10 tendencias emergentes en IA",
            "backstory": """
Especialista en análisis de mercado con 10 años de experiencia en tecnología.
Has publicado 20+ reportes en medios especializados.
Tienes acceso a bases de datos proprietarias y red de contactos en Fortune 500.
            """
        }
        print(f"  Rol: {good_agent['role']}")
        print(f"  Goal: {good_agent['goal']}")

        # Ejemplo MAL: Rol genérico
        print("\n✗ MAL - Rol demasiado genérico:")
        bad_agent = {
            "role": "Analista",
            "goal": "Analizar mercado",
            "backstory": "Eres un analista"
        }
        print(f"  Rol: {bad_agent['role']}")
        print(f"  Goal: {bad_agent['goal']}")

        return {
            "good_example": good_agent,
            "bad_example": bad_agent
        }

    def demonstrate_task_structuring(self):
        """Mostrar cómo estructurar tareas efectivamente"""
        print("\n" + "="*70)
        print("2. ESTRUCTURACIÓN EFECTIVA DE TAREAS")
        print("="*70)

        # Tarea bien estructurada
        print("\n✓ BIEN - Descripción clara y específica:")
        good_task = {
            "description": """
Investiga las tendencias emergentes del mercado de IA en 2024.
Enfócate en: modelos de IA, aplicaciones nuevas, regulaciones, empresas líderes.
Incluye datos de al menos 3 fuentes confiables.
            """,
            "expected_output": """
Reporte en markdown con:
- 5-10 tendencias principales
- Análisis de impacto (alto/medio/bajo)
- Empresas afectadas
- Proyecciones para 2025
            """,
            "dependencies": []
        }
        print(f"  Descripción:\n{good_task['description']}")
        print(f"  Output esperado:\n{good_task['expected_output']}")

        # Tarea mal estructurada
        print("\n✗ MAL - Descripción vaga:")
        bad_task = {
            "description": "Investiga IA",
            "expected_output": "Reporte",
            "dependencies": []
        }
        print(f"  Descripción: {bad_task['description']}")
        print(f"  Output esperado: {bad_task['expected_output']}")

        return {
            "good_example": good_task,
            "bad_example": bad_task
        }

    def demonstrate_dependencies(self):
        """Mostrar uso correcto de dependencias"""
        print("\n" + "="*70)
        print("3. GESTIÓN DE DEPENDENCIAS")
        print("="*70)

        tasks = [
            {
                "name": "research_task",
                "description": "Investigar datos del mercado",
                "depends_on": []
            },
            {
                "name": "analysis_task",
                "description": "Analizar datos investigados",
                "depends_on": ["research_task"]
            },
            {
                "name": "reporting_task",
                "description": "Escribir reporte basado en análisis",
                "depends_on": ["analysis_task"]
            }
        ]

        print("\n✓ Orden correcto de dependencias (Pipeline):")
        for task in tasks:
            indent = "  " * len(task['depends_on'])
            deps = " -> ".join(task['depends_on']) if task['depends_on'] else "Inicial"
            print(f"{indent}[{task['name']}] ({deps})")
            print(f"{indent}  └─ {task['description']}")

        return tasks

    def demonstrate_cost_optimization(self):
        """Mostrar estrategias de optimización de costos"""
        print("\n" + "="*70)
        print("4. OPTIMIZACIÓN DE COSTOS")
        print("="*70)

        # Estrategia 1: Usar modelos apropiados
        print("\n1️⃣  Usar modelos según complejidad de tarea:")
        models = {
            "simple_tasks": {
                "model": "gpt-3.5-turbo",
                "cost_per_1k_tokens": 0.5,
                "examples": ["Clasificación simple", "Resumen de texto"]
            },
            "complex_tasks": {
                "model": "gpt-4",
                "cost_per_1k_tokens": 3.0,
                "examples": ["Análisis estratégico", "Generación de código"]
            }
        }

        for task_type, config in models.items():
            print(f"\n   {task_type.upper()}:")
            print(f"   Modelo: {config['model']} (${config['cost_per_1k_tokens']}/1k tokens)")
            print(f"   Casos: {', '.join(config['examples'])}")

        # Estrategia 2: Limitar iteraciones
        print("\n2️⃣  Limitar iteraciones máximas:")
        print("   agent = Agent(")
        print("       role='Investigador',")
        print("       goal='Investigar...',")
        print("       max_iterations=3  # Limita intentos")
        print("   )")

        # Estrategia 3: Implementar caching
        print("\n3️⃣  Implementar caching de resultados:")
        cache_example = {
            "key": "hash(task_description + agent_role)",
            "benefits": [
                "Evita re-procesamiento de tareas idénticas",
                "Reduce consumo de tokens",
                "Mejora velocidad de respuesta"
            ]
        }
        print(f"   Estrategia: {cache_example['key']}")
        print("   Beneficios:")
        for benefit in cache_example['benefits']:
            print(f"   - {benefit}")

        return {
            "model_selection": models,
            "max_iterations": 3,
            "caching_enabled": True
        }

    def print_summary(self):
        """Imprimir resumen de mejores prácticas"""
        print("\n" + "="*70)
        print("RESUMEN DE MEJORES PRÁCTICAS")
        print("="*70)

        practices = {
            "Diseño de Agentes": [
                "✓ Roles específicos y sin ambigüedad",
                "✓ Goals medibles y alcanzables",
                "✓ Backstories detallados y creíbles",
                "✓ Herramientas bien asignadas"
            ],
            "Estructuración de Tareas": [
                "✓ Descripciones claras y detalladas",
                "✓ Expected outputs bien definidos",
                "✓ Dependencias lógicas y explícitas",
                "✓ Validación de outputs"
            ],
            "Optimización": [
                "✓ Usar modelos apropiados por tarea",
                "✓ Limitar iteraciones máximas",
                "✓ Implementar caching",
                "✓ Monitorizar costos"
            ]
        }

        for category, practices_list in practices.items():
            print(f"\n{category}:")
            for practice in practices_list:
                print(f"  {practice}")

        print("\n" + "="*70 + "\n")


def main():
    """Demostración completa de mejores prácticas"""
    print("="*70)
    print(" MÓDULO 7: MEJORES PRÁCTICAS EN CREWAI")
    print("="*70)

    demo = BestPracticesDemo()

    # Ejecutar demostraciones
    demo.demonstrate_agent_design()
    demo.demonstrate_task_structuring()
    demo.demonstrate_dependencies()
    demo.demonstrate_cost_optimization()
    demo.print_summary()


if __name__ == "__main__":
    main()
