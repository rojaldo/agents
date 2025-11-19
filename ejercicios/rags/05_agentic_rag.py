import os
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain.tools.retriever import create_retriever_tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor

# Configuración
MODEL_NAME = "llama3.2:3b"
EMBEDDING_MODEL = "nomic-embed-text"
PERSIST_DIRECTORY = "./chroma_db"

def main():
    print(f"--- Ejemplo 05: RAG Agéntico (Router/Tools) ---")
    
    if not os.path.exists(PERSIST_DIRECTORY):
        print("Error: Ejecuta primero el ejemplo 02 para crear la base de datos.")
        return

    # 1. Preparar Vector Store y Retriever
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    vectorstore = Chroma(
        persist_directory=PERSIST_DIRECTORY, 
        embedding_function=embeddings,
        collection_name="course_knowledge"
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # 2. Crear Herramienta (Tool)
    # Convertimos el retriever en una herramienta que el agente puede invocar
    tool = create_retriever_tool(
        retriever,
        "buscar_curso_agentes",
        "Busca información específica sobre el curso de Agentes de IA, temarios, herramientas y conceptos."
    )
    tools = [tool]

    # 3. Configurar LLM
    # Nota: Para tool calling, es mejor usar modelos que lo soporten bien.
    # Llama 3.2 soporta tool calling, pero a veces requiere prompts específicos.
    # LangChain maneja esto, pero la fiabilidad depende del modelo local.
    llm = ChatOllama(model=MODEL_NAME, temperature=0)

    # 4. Definir Prompt del Agente
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un asistente útil. Si te preguntan sobre el curso, usa la herramienta de búsqueda. Si es un saludo o charla general, responde directamente."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    # 5. Crear Agente
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # 6. Pruebas
    queries = [
        "Hola, ¿cómo estás?",  # Debería responder sin buscar
        "¿Qué temas cubre el módulo de evaluación?", # Debería usar la herramienta
        "Cuéntame un chiste corto." # Debería responder sin buscar
    ]

    for q in queries:
        print(f"\n--- Usuario: {q} ---")
        try:
            response = agent_executor.invoke({"input": q})
            print(f"Agente: {response['output']}")
        except Exception as e:
            print(f"Error ejecutando agente: {e}")
            print("Nota: Asegúrate de que tu versión de Ollama y el modelo soportan 'tool calling'.")

if __name__ == "__main__":
    main()
