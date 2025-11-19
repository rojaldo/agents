# --- Estado Global (Simulado para la demo) ---
# En una app real multi-usuario, esto debería gestionarse con gr.State o una base de datos
TASKS = []

# --- Herramientas / Funciones ---

def get_tasks() -> str:
    """Devuelve la lista actual de tareas."""
    if not TASKS:
        return "La lista de tareas está vacía. ¡Añade algo divertido!"
    return "\n".join([f"{i+1}. {t}" for i, t in enumerate(TASKS)])

def add_task(task_description: str) -> str:
    """Añade una nueva tarea a la lista. La descripción no puede estar vacía."""
    if not task_description or not task_description.strip():
        return "¡Oye! No puedo añadir una tarea vacía. Escribe algo."
    TASKS.append(task_description)
    return f"¡Hecho! He añadido '{task_description}' a tu lista. ¡A por ello!"

def delete_task(task_index: int) -> str:
    """Elimina una tarea por su número de índice (empezando por 1)."""
    try:
        idx = int(task_index) - 1
        if 0 <= idx < len(TASKS):
            removed = TASKS.pop(idx)
            return f"¡Adiós! He eliminado '{removed}' de la lista. ¡Una menos!"
        else:
            return f"Mmm, no encuentro la tarea número {task_index}. Revisa la lista."
    except ValueError:
        return "Necesito un número válido para borrar la tarea."
