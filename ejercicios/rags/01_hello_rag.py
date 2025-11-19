import os
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. Configuración
# Asegúrate de tener Ollama corriendo con: ollama serve
# Y haber descargado los modelos: ollama pull llama3.2 y ollama pull nomic-embed-text
MODEL_NAME = "llama3.2:3b"
EMBEDDING_MODEL = "nomic-embed-text"

print(f"--- Iniciando Ejemplo 01: Hello World RAG ---")
print(f"Usando LLM: {MODEL_NAME} y Embeddings: {EMBEDDING_MODEL}")

# 2. Datos de Ejemplo (Simulando una base de conocimiento)
# En un caso real, esto vendría de archivos PDF, TXT, etc.
texts = [
    "El curso de Agentes de IA cubre el uso de LangChain y CrewAI.",
    "LangChain es un framework para desarrollar aplicaciones impulsadas por modelos de lenguaje.",
    "CrewAI permite orquestar múltiples agentes autónomos para tareas complejas.",
    "Ollama es una herramienta para ejecutar LLMs localmente de manera fácil.",
    "RAG significa Retrieval-Augmented Generation (Generación Aumentada por Recuperación).",
    "El instructor del curso prefiere usar ejemplos prácticos sobre teoría pura."
]

# Convertimos los textos a objetos Document de LangChain
documents = [Document(page_content=text) for text in texts]

# 3. Crear Vector Store (En Memoria)
# Usamos Chroma en modo efímero (sin persistencia en disco para este ejemplo)
print("Creando base de datos vectorial en memoria...")
embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    collection_name="hello_rag_collection"
)

# 4. Crear el Retriever (Recuperador)
# Configuramos para que nos devuelva los 2 documentos más relevantes (k=2)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# 5. Definir el Prompt
template = """Responde a la pregunta basándote SOLO en el siguiente contexto:
{context}

Pregunta: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

# 6. Inicializar el LLM
llm = ChatOllama(model=MODEL_NAME)

# 7. Construir la Cadena (Chain)
# La cadena sigue el flujo: 
# 1. Toma la pregunta
# 2. Busca contexto relevante (retriever)
# 3. Pasa contexto y pregunta al prompt
# 4. Pasa el prompt al LLM
# 5. Parsea la salida a string

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 8. Ejecutar la Cadena
question = "¿Qué herramientas se usan en el curso para agentes?"
print(f"\nPregunta: {question}")
print("Generando respuesta...")

response = rag_chain.invoke(question)

print(f"\nRespuesta:\n{response}")

# Ejemplo adicional para ver qué recuperó
print("\n--- Debug: Documentos recuperados ---")
retrieved_docs = retriever.invoke(question)
for i, doc in enumerate(retrieved_docs):
    print(f"Doc {i+1}: {doc.page_content}")
