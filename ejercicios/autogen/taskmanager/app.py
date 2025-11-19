import gradio as gr
from crewai_agent import run_crewai
from autogen_agent import run_autogen
from tasks import get_tasks

# --- Interfaz Gradio ---

def chat_logic(message, history, backend):
    if backend == "CrewAI":
        return run_crewai(message, history)
    else:
        return run_autogen(message, history)

def update_task_view():
    return get_tasks()

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 📝 Gestor de Tareas con IA (CrewAI / AutoGen)")
    
    with gr.Row():
        with gr.Column(scale=2):
            chatbot = gr.ChatInterface(
                fn=chat_logic,
                additional_inputs=[
                    gr.Dropdown(choices=["CrewAI", "AutoGen"], value="CrewAI", label="Motor de IA")
                ],
                title="Chat de Tareas",
                description="Pídeme que añada, borre o liste tus tareas.",
                examples=[
                    ["Añade comprar leche", "CrewAI"],
                    ["Borra la tarea 1", "CrewAI"],
                    ["¿Qué tengo que hacer?", "AutoGen"]
                ],
            )
        
        with gr.Column(scale=1):
            gr.Markdown("### 📋 Lista de Tareas en Tiempo Real")
            task_display = gr.Textbox(label="Tareas Actuales", value=get_tasks(), interactive=False, lines=10)
            refresh_btn = gr.Button("🔄 Actualizar Lista")
            
            # Actualizar la lista cuando se pulsa el botón (o idealmente tras cada mensaje, pero requiere eventos complejos)
            refresh_btn.click(fn=update_task_view, outputs=task_display)
            
            # Intentar actualizar la lista automáticamente cada vez que el chatbot responde (usando eventos de gradio si fuera posible facilmente)
            # Por simplicidad, el usuario puede dar a refrescar o lo hacemos con un timer si fuera necesario.

if __name__ == "__main__":
    demo.launch()
