"""
Módulo 2: Conceptos Fundamentales
Ejemplo 1: Basic Agents - Agentes con roles específicos
"""

from datetime import datetime


class Agent:
    """Agente con rol, goal y backstory"""

    def __init__(self, role, goal, backstory, tools=None):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools = tools or []
        self.interactions = []
        self.created_at = datetime.now()

    def think(self, problem):
        """Procesar un problema"""
        thought = {
            "timestamp": datetime.now().isoformat(),
            "problem": problem,
            "role": self.role,
            "reasoning": f"Como {self.role}, debo {self.goal}..."
        }
        self.interactions.append(thought)
        return thought

    def act(self, action):
        """Tomar una acción"""
        return f"{self.role} está ejecutando: {action}"

    def get_profile(self):
        """Obtener perfil del agente"""
        return {
            "role": self.role,
            "goal": self.goal,
            "backstory": self.backstory,
            "tools": len(self.tools),
            "interactions": len(self.interactions),
            "uptime": str(datetime.now() - self.created_at)
        }


class Task:
    """Tarea asignada a un agente"""

    def __init__(self, description, expected_output, agent):
        self.description = description
        self.expected_output = expected_output
        self.agent = agent
        self.status = "pending"
        self.result = None
        self.created_at = datetime.now()

    def execute(self):
        """Ejecutar la tarea"""
        self.status = "in_progress"

        # Agente piensa
        thought = self.agent.think(self.description)

        # Agente actúa
        action = self.agent.act(self.description)

        # Resultado
        self.result = {
            "task": self.description,
            "agent": self.agent.role,
            "thinking": thought["reasoning"],
            "action": action,
            "output": self.expected_output
        }

        self.status = "completed"
        return self.result

    def get_info(self):
        """Obtener información de la tarea"""
        return {
            "description": self.description,
            "agent": self.agent.role,
            "status": self.status,
            "duration": str(datetime.now() - self.created_at) if self.status == "completed" else "N/A"
        }


def main():
    """Demostración de agentes básicos"""
    print("="*70)
    print(" MÓDULO 2: AGENTES Y TAREAS BÁSICOS")
    print("="*70)

    # Crear agentes
    print("\n🤖 Creando agentes especializados...\n")

    python_expert = Agent(
        role="Python Expert",
        goal="Escribir código Python limpio y eficiente",
        backstory="Experto en Python con 15 años de experiencia en sistemas distribuidos"
    )
    print(f"  ✓ {python_expert.role} creado")

    code_reviewer = Agent(
        role="Code Reviewer",
        goal="Revisar código y sugerir mejoras",
        backstory="Especialista en code review con enfoque en best practices"
    )
    print(f"  ✓ {code_reviewer.role} creado")

    tester = Agent(
        role="QA Tester",
        goal="Asegurar calidad mediante testing exhaustivo",
        backstory="QA con experiencia en testing automatizado y manual"
    )
    print(f"  ✓ {tester.role} creado")

    # Crear tareas
    print("\n📋 Creando tareas...\n")

    task1 = Task(
        description="Escribe una función para calcular el factorial de un número",
        expected_output="Código Python con tests incluidos",
        agent=python_expert
    )
    print(f"  1. {task1.description}")

    task2 = Task(
        description="Revisa el código generado y sugiere mejoras",
        expected_output="Reporte con 5-10 sugerencias de mejora",
        agent=code_reviewer
    )
    print(f"  2. {task2.description}")

    task3 = Task(
        description="Prueba la función con múltiples casos de prueba",
        expected_output="Reporte de tests con cobertura",
        agent=tester
    )
    print(f"  3. {task3.description}")

    # Ejecutar tareas
    print("\n🚀 Ejecutando tareas...\n")

    tasks = [task1, task2, task3]

    for i, task in enumerate(tasks, 1):
        print(f"[{i}] Ejecutando: {task.description}")
        result = task.execute()
        print(f"    ✓ Estado: {task.status}")
        print(f"    Agente: {result['agent']}")
        print()

    # Mostrar resumen
    print("\n" + "="*70)
    print("RESUMEN DE EJECUCIÓN")
    print("="*70)

    print(f"\nAgentes:")
    for agent in [python_expert, code_reviewer, tester]:
        profile = agent.get_profile()
        print(f"\n  {agent.role}:")
        print(f"    Goal: {profile['goal']}")
        print(f"    Tareas completadas: {profile['interactions']}")

    print(f"\nTareas:")
    for task in tasks:
        info = task.get_info()
        print(f"  {info['description']}: {info['status']}")

    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
