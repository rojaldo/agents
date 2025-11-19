import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# Configuración
MODEL_NAME = "ollama/llama3.2:3b" # CrewAI usa formato provider/model
EMBEDDING_MODEL = "nomic-embed-text"
PERSIST_DIRECTORY = "./chroma_db"

# 1. Definir Herramienta de Búsqueda
# Usamos el decorador @tool de CrewAI para crear una herramienta personalizada
# que consulta nuestra base de datos Chroma existente.

class SearchTools:
    @tool("Buscar en Base de Conocimiento")
    def search_knowledge_base(query: str):
        """Útil para buscar información específica sobre cursos, temarios y conceptos técnicos 
        en la base de conocimiento. Recibe una pregunta o término de búsqueda."""
        
        if not os.path.exists(PERSIST_DIRECTORY):
            return "Error: La base de datos no existe. Ejecuta 02_persistent_kb.py primero."

        try:
            embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
            vectorstore = Chroma(
                persist_directory=PERSIST_DIRECTORY, 
                embedding_function=embeddings,
                collection_name="course_knowledge"
            )
            retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
            docs = retriever.invoke(query)
            
            return "\n\n".join([doc.page_content for doc in docs])
        except Exception as e:
            return f"Error buscando en la base de datos: {str(e)}"

def main():
    print(f"--- Ejemplo 07: RAG con CrewAI ---")
    
    # 2. Configurar LLM
    # CrewAI puede usar Ollama directamente
    my_llm = LLM(
        model=MODEL_NAME,
        base_url="http://localhost:11434"
    )

    # 3. Definir Agentes
    researcher = Agent(
        role='Investigador de IA',
        goal='Buscar información precisa sobre conceptos de IA en la base de conocimiento.',
        backstory='Eres un experto en encontrar información técnica. Tu trabajo es buscar en la documentación y extraer los hechos clave.',
        tools=[SearchTools.search_knowledge_base],
        verbose=True,
        llm=my_llm
    )

    writer = Agent(
        role='Redactor Técnico',
        goal='Escribir respuestas claras y educativas basadas en la investigación.',
        backstory='Eres un redactor técnico que sabe explicar conceptos complejos de forma sencilla. Usas la información que te da el investigador.',
        verbose=True,
        llm=my_llm
    )

    # 4. Definir Tareas
    question = "¿Cuáles son los componentes principales de LangChain?"
    print(f"\nPregunta del usuario: {question}\n")

    task1 = Task(
        description=f'Busca información detallada sobre: {question}. Usa la herramienta de búsqueda.',
        expected_output='Un resumen de los puntos clave encontrados en la documentación.',
        agent=researcher
    )

    task2 = Task(
        description=f'Usando la información encontrada, escribe una respuesta completa y didáctica a la pregunta: {question}',
        expected_output='Un párrafo explicativo bien redactado en español.',
        agent=writer,
        context=[task1] # El output de task1 pasa a task2
    )

    # 5. Ejecutar Crew
    crew = Crew(
        agents=[researcher, writer],
        tasks=[task1, task2],
        verbose=True,
        process=Process.sequential
    )

    result = crew.kickoff()
    
    print("\n\n########################")
    print("## Resultado Final ##")
    print("########################\n")
    print(result)

if __name__ == "__main__":
    main()
