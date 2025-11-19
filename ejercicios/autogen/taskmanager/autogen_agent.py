import autogen
from tasks import get_tasks, add_task, delete_task

# --- Configuración AutoGen ---

def run_autogen(message: str, history):
    config_list = [
        {
            "model": "llama3.2:3b",
            "base_url": "http://localhost:11434/v1",
            "api_key": "ollama",
        }
    ]

    llm_config = {
        "config_list": config_list,
        "temperature": 0.7,
    }

    # Asistente
    assistant = autogen.AssistantAgent(
        name="assistant",
        llm_config=llm_config,
        system_message="Eres un gestor de tareas divertido y amable. "
                       "Puedes llamar a las funciones 'add_task', 'delete_task' y 'get_tasks' para gestionar la lista. "
                       "Responde siempre en español y con buen humor. "
                       "Cuando hayas terminado la acción, informa al usuario."
    )

    # Proxy de Usuario (ejecuta código/funciones)
    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=1, # Limitamos para evitar bucles en este chat simple
        code_execution_config={"work_dir": "coding", "use_docker": False},
        function_map={
            "add_task": add_task,
            "delete_task": delete_task,
            "get_tasks": get_tasks
        }
    )
    
    # Registrar funciones para que el asistente sepa usarlas
    autogen.register_function(
        add_task,
        caller=assistant,
        executor=user_proxy,
        name="add_task",
        description="Añade una tarea a la lista."
    )
    
    autogen.register_function(
        delete_task,
        caller=assistant,
        executor=user_proxy,
        name="delete_task",
        description="Elimina una tarea por su índice."
    )

    autogen.register_function(
        get_tasks,
        caller=assistant,
        executor=user_proxy,
        name="get_tasks",
        description="Obtiene la lista actual de tareas."
    )

    # Iniciar chat
    # Nota: AutoGen suele imprimir en consola. Capturar la respuesta para el chat de Gradio es un poco truco.
    # Para simplificar, usaremos initiate_chat y devolveremos el último mensaje del asistente.
    
    chat_res = user_proxy.initiate_chat(
        assistant,
        message=message,
        summary_method="last_msg"
    )
    
    # chat_res.summary contiene el resumen o último mensaje
    return str(chat_res.summary)
