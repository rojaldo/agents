import os
import autogen
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# Configuración
MODEL_NAME = "llama3.2:3b"
EMBEDDING_MODEL = "nomic-embed-text"
PERSIST_DIRECTORY = "./chroma_db"

# 1. Definir Función de Búsqueda (Tool)
def search_knowledge_base(query: str) -> str:
    """Busca información en la base de conocimiento del curso."""
    print(f"\n[Tool] Buscando: {query}...")
    
    if not os.path.exists(PERSIST_DIRECTORY):
        return "Error: La base de datos no existe."

    try:
        embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
        vectorstore = Chroma(
            persist_directory=PERSIST_DIRECTORY, 
            embedding_function=embeddings,
            collection_name="course_knowledge"
        )
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        docs = retriever.invoke(query)
        
        results = "\n\n".join([f"--- Documento ---\n{doc.page_content}" for doc in docs])
        return results if results else "No se encontró información relevante."
    except Exception as e:
        return f"Error en búsqueda: {str(e)}"

def main():
    print("--- Ejemplo 08: RAG con AutoGen (Function Calling) ---")

    # 2. Configurar AutoGen con Ollama
    config_list = [
        {
            "model": MODEL_NAME,
            "base_url": "http://localhost:11434/v1",
            "api_key": "ollama",
        }
    ]
    
    llm_config = {
        "config_list": config_list,
        "temperature": 0,
        # Registramos la función que el agente puede llamar
        "functions": [
            {
                "name": "search_knowledge_base",
                "description": "Busca información técnica en la base de conocimiento sobre cursos y agentes.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "La consulta de búsqueda o pregunta específica.",
                        }
                    },
                    "required": ["query"],
                },
            }
        ],
    }

    # 3. Definir Agentes
    
    # Asistente: Es quien recibe la tarea y decide llamar a la función
    assistant = autogen.AssistantAgent(
        name="assistant",
        llm_config=llm_config,
        system_message="Eres un asistente útil. Si te preguntan algo que no sabes, usa la función 'search_knowledge_base' para buscar información. Responde en español."
    )

    # User Proxy: Es quien ejecuta la función (tool executor)
    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=5,
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config=False, # No ejecutamos código Python arbitrario, solo funciones registradas
    )

    # 4. Registrar la función para ejecución
    user_proxy.register_function(
        function_map={
            "search_knowledge_base": search_knowledge_base
        }
    )

    # 5. Iniciar Chat
    question = "¿Qué es RAG y cómo se relaciona con LangChain?"
    print(f"\nPregunta: {question}\n")
    
    user_proxy.initiate_chat(
        assistant,
        message=question
    )

if __name__ == "__main__":
    main()
