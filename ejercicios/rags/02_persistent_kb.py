import os
import shutil
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Configuración
MODEL_NAME = "llama3.2:3b"
EMBEDDING_MODEL = "nomic-embed-text"
PERSIST_DIRECTORY = "./chroma_db"
SOURCE_DIRECTORY = "../../contenidos-didacticos" # Ajusta esta ruta a tus archivos

def load_documents():
    """Carga documentos desde el directorio especificado."""
    if not os.path.exists(SOURCE_DIRECTORY):
        print(f"Directorio no encontrado: {SOURCE_DIRECTORY}")
        return []
    
    print(f"Cargando documentos desde {SOURCE_DIRECTORY}...")
    # Cargamos archivos Markdown
    loader = DirectoryLoader(
        SOURCE_DIRECTORY, 
        glob="**/*.md", 
        loader_cls=UnstructuredMarkdownLoader,
        show_progress=True
    )
    documents = loader.load()
    print(f"Se cargaron {len(documents)} documentos.")
    return documents

def split_documents(documents):
    """Divide los documentos en chunks más pequeños."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Documentos divididos en {len(chunks)} chunks.")
    return chunks

def get_vectorstore():
    """Obtiene o crea la base de datos vectorial persistente."""
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    
    if os.path.exists(PERSIST_DIRECTORY) and os.listdir(PERSIST_DIRECTORY):
        print(f"Cargando base de datos vectorial existente desde {PERSIST_DIRECTORY}...")
        vectorstore = Chroma(
            persist_directory=PERSIST_DIRECTORY, 
            embedding_function=embeddings,
            collection_name="course_knowledge"
        )
    else:
        print("Creando nueva base de datos vectorial...")
        documents = load_documents()
        if not documents:
            print("No hay documentos para procesar.")
            return None
            
        chunks = split_documents(documents)
        
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=PERSIST_DIRECTORY,
            collection_name="course_knowledge"
        )
        print("Base de datos creada y guardada.")
        
    return vectorstore

def main():
    print(f"--- Ejemplo 02: Base de Conocimiento Persistente ---")
    
    # 1. Obtener Vector Store
    vectorstore = get_vectorstore()
    if not vectorstore:
        return

    # 2. Crear Retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # 3. Configurar RAG Chain
    template = """Usa el siguiente contexto para responder a la pregunta.
    Si no sabes la respuesta, di simplemente que no lo sabes, no intentes inventar una respuesta.
    
    Contexto: {context}
    
    Pregunta: {question}
    
    Respuesta:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOllama(model=MODEL_NAME)
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # 4. Loop de preguntas
    print("\n--- Sistema listo. Escribe 'salir' para terminar. ---")
    while True:
        question = input("\nPregunta: ")
        if question.lower() in ["salir", "exit", "quit"]:
            break
            
        print("Buscando y generando respuesta...")
        try:
            response = rag_chain.invoke(question)
            print(f"\nRespuesta: {response}")
            
            # Opcional: Ver fuentes
            # docs = retriever.invoke(question)
            # print(f"\nFuentes: {[doc.metadata.get('source') for doc in docs]}")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    # Instalar dependencia necesaria para cargar markdown si falla
    # pip install unstructured markdown
    main()
