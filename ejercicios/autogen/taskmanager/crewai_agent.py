from crewai import Agent, Task, Crew
from crewai.tools import tool
from tasks import get_tasks, add_task, delete_task

# --- Configuración CrewAI ---

@tool("Listar Tareas")
def tool_get_tasks():
    """Muestra todas las tareas pendientes."""
    return get_tasks()

@tool("Añadir Tarea")
def tool_add_task(descripcion: str):
    """Añade una tarea a la lista."""
    return add_task(descripcion)

@tool("Eliminar Tarea")
def tool_delete_task(numero: int):
    """Elimina una tarea dada su posición numérica en la lista."""
    return delete_task(numero)

def run_crewai(message: str, history):
    # Agente
    manager = Agent(
        role="Gestor de Tareas",
        goal="Gestionar la lista de tareas del usuario de forma eficiente.",
        backstory="Eres un asistente personal. Te encanta organizar cosas. "
                  "Siempre respondes en español con un tono divertido.",
        tools=[tool_get_tasks, tool_add_task, tool_delete_task],
        llm="ollama/llama3.2:3b",
        base_url="http://localhost:11434",
        verbose=True
    )

    # Tarea
    task = Task(
        description=f"""
        El usuario ha enviado el siguiente mensaje: "{message}"
        
        Tu objetivo es:
        1. Entender qué quiere hacer el usuario (añadir, borrar o listar tareas).
        2. EJECUTAR la herramienta correspondiente (tool_add_task, tool_delete_task o tool_get_tasks). ¡Es obligatorio usar una herramienta si el usuario pide una acción!
        3. Una vez ejecutada la herramienta, responder al usuario confirmando lo que has hecho.
        
        Si el usuario solo saluda o conversa, responde amablemente sin usar herramientas.
        """,
        expected_output="Una respuesta final en texto para el usuario confirmando la acción realizada (ej: 'He añadido comprar pan a la lista').",
        agent=manager
    )

    crew = Crew(
        agents=[manager],
        tasks=[task],
        verbose=True
    )

    result = crew.kickoff()
    return str(result)
