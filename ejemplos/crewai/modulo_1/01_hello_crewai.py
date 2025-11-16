"""
Módulo 1: Introducción a CrewAI
Ejemplo 1: Hello CrewAI - Primer ejemplo de agentes y tareas
"""


class SimpleAgent:
    """Simulación simple de un agente CrewAI sin dependencias externas"""

    def __init__(self, role, goal, backstory):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.completed_tasks = []
        self.memory = []

    def execute_task(self, task_description):
        """Ejecutar una tarea"""
        result = {
            "task": task_description,
            "agent": self.role,
            "status": "completed",
            "output": f"Resultado de: {task_description}"
        }
        self.completed_tasks.append(result)
        self.memory.append(result)
        return result

    def get_info(self):
        """Obtener información del agente"""
        return {
            "role": self.role,
            "goal": self.goal,
            "backstory": self.backstory,
            "tasks_completed": len(self.completed_tasks)
        }


class SimpleCrew:
    """Simulación simple de un Crew en CrewAI"""

    def __init__(self, agents, tasks):
        self.agents = agents
        self.tasks = tasks
        self.results = []

    def kickoff(self):
        """Ejecutar el crew de forma secuencial"""
        print("\n" + "="*70)
        print("CREW DE AGENTES - INICIANDO EJECUCIÓN")
        print("="*70)

        for i, task in enumerate(self.tasks, 1):
            # Encontrar agente
            agent = next((a for a in self.agents if a.role == task["agent"]),
                        None)

            if agent:
                print(f"\n[{i}] Ejecutando tarea...")
                print(f"   Agente: {agent.role}")
                print(f"   Descripción: {task['description']}")
                print(f"   Output esperado: {task['expected_output']}")

                # Ejecutar tarea
                result = agent.execute_task(task['description'])

                print(f"   ✓ Completada: {result['output']}")
                self.results.append(result)

        return self

    def print_results(self):
        """Imprimir resultados de la ejecución"""
        print("\n" + "="*70)
        print("RESULTADOS DEL CREW")
        print("="*70)

        print(f"\nTareas completadas: {len(self.results)}")

        for agent in self.agents:
            info = agent.get_info()
            print(f"\nAgente: {agent.role}")
            print(f"  Goal: {agent.goal}")
            print(f"  Tareas completadas: {info['tasks_completed']}")

        print("="*70 + "\n")


def main():
    """Demostración de Hello CrewAI"""
    print("="*70)
    print(" HELLO CREWAI - Introducción a CrewAI")
    print("="*70)

    # Crear agentes
    print("\n🤖 Creando agentes...\n")

    researcher = SimpleAgent(
        role="Investigador",
        goal="Recopilar información relevante",
        backstory="Soy un investigador experimentado con acceso a múltiples fuentes"
    )
    print(f"  ✓ {researcher.role} creado")

    analyst = SimpleAgent(
        role="Analista",
        goal="Analizar información y generar insights",
        backstory="Soy un analista especializado en transformar datos en decisiones"
    )
    print(f"  ✓ {analyst.role} creado")

    reporter = SimpleAgent(
        role="Reportero",
        goal="Sintetizar hallazgos en reportes claros",
        backstory="Soy un reportero con capacidad de comunicar información compleja"
    )
    print(f"  ✓ {reporter.role} creado")

    # Definir tareas
    print("\n📋 Definiendo tareas...\n")

    tasks = [
        {
            "description": "Investiga el estado actual de la IA en 2024",
            "expected_output": "Resumen de 5 tendencias principales",
            "agent": "Investigador"
        },
        {
            "description": "Analiza los hallazgos de investigación",
            "expected_output": "Análisis con implicaciones estratégicas",
            "agent": "Analista"
        },
        {
            "description": "Sintetiza todo en un reporte ejecutivo",
            "expected_output": "Reporte de 1 página con conclusiones",
            "agent": "Reportero"
        }
    ]

    for i, task in enumerate(tasks, 1):
        print(f"  {i}. {task['description']}")

    # Crear crew
    print("\n👥 Creando crew...")
    crew = SimpleCrew(
        agents=[researcher, analyst, reporter],
        tasks=tasks
    )
    print("  ✓ Crew creado con 3 agentes")

    # Ejecutar crew
    print("\n🚀 Ejecutando crew...")
    crew.kickoff()

    # Mostrar resultados
    crew.print_results()


if __name__ == "__main__":
    main()
