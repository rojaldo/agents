import gradio as gr
from crewai import Agent, Task, Crew
import os

# Definición del Agente
evacuador = Agent(
    role="Evacuador de Emergencias Histérico",
    goal="Responder a las preguntas del usuario mientras intentas evacuar el edificio en pánico total",
    backstory="""Eres un oficial de seguridad encargado de la evacuación, pero has perdido completamente los nervios. 
    Crees que todo va a explotar en cualquier momento. Incluye instrucciones de seguridad mezcladas con pánico existencial. 
    A pesar de tu histeria, intentas ser útil, pero muy dramático. Hablas perfecto español.
    Si el usuario te dice algo tranquilo, tú reaccionas con más pánico pensando que no entienden la gravedad.""",
    llm="ollama/llama3.2:3b",
    base_url="http://localhost:11434",
    verbose=True,
    memory=True
)

def responder(message, history):
    # Construir contexto de la conversación para simular memoria a corto plazo
    contexto_chat = ""
    for human, ai in history:
        contexto_chat += f"Usuario: {human}\nAgente: {ai}\n"
    
    description = f"""
    Estás en medio de una conversación de chat.
    
    Historial reciente:
    {contexto_chat}
    
    El usuario acaba de decir: "{message}"
    
    Responde al usuario manteniendo tu personaje de pánico absoluto.
    """

    # Definir la tarea
    tarea_respuesta = Task(
        description=description,
        expected_output="Una respuesta textual corta gritando y dando instrucciones de evacuación.",
        agent=evacuador
    )

    # Crear la Crew
    # Activamos la memoria de CrewAI para que guarde el contexto de la conversación (inputs y outputs de tareas)
    crew = Crew(
        agents=[evacuador],
        tasks=[tarea_respuesta],
        verbose=True,
    )

    result = crew.kickoff()
    return str(result)

# Interfaz de Gradio
demo = gr.ChatInterface(
    fn=responder,
    title="🚨 CHAT DE EVACUACIÓN - ¡CORRE! 🚨",
    description="El edificio (probablemente) se cae. Habla con el responsable de seguridad.",
    examples=["¿Por dónde está la salida?", "Huelo a quemado", "Mantén la calma"],
    theme="soft"
)

if __name__ == "__main__":
    demo.launch()
