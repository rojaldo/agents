import os
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Configuración
MODEL_NAME = "llama3.2:3b"
EMBEDDING_MODEL = "nomic-embed-text"
PERSIST_DIRECTORY = "./chroma_db"

def main():
    print(f"--- Ejemplo 04: Búsqueda Híbrida (Semántica + Keyword) ---")
    
    if not os.path.exists(PERSIST_DIRECTORY):
        print("Error: Ejecuta primero el ejemplo 02 para crear la base de datos.")
        return

    # 1. Configurar Retriever Semántico (Chroma)
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    vectorstore = Chroma(
        persist_directory=PERSIST_DIRECTORY, 
        embedding_function=embeddings,
        collection_name="course_knowledge"
    )
    # Obtenemos todos los documentos para inicializar BM25 (esto puede ser costoso en DBs grandes)
    # En producción, BM25 se gestionaría de forma más eficiente o con un motor como Elasticsearch/Qdrant
    print("Cargando documentos para índice de palabras clave...")
    all_docs = vectorstore.get() # Obtiene IDs y metadatos, pero necesitamos el contenido
    # Chroma.get() devuelve un dict, necesitamos reconstruir los documentos o usar el retriever base
    # Para simplificar este ejemplo, usaremos los documentos que el vectorstore ya tiene indexados
    # Nota: LangChain no expone fácilmente todos los docs de Chroma para BM25 sin re-leerlos.
    # Truco: Hacemos una búsqueda vacía o amplia si es posible, o mejor, re-cargamos usando el loader del ej 02
    # Para este ejemplo didáctico, asumiremos que podemos recuperar una muestra o re-usar la lógica de carga.
    
    # Re-cargamos documentos para BM25 (Simulación de entorno real donde tendrías un índice invertido)
    from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
    SOURCE_DIRECTORY = "../../contenidos-didacticos"
    loader = DirectoryLoader(SOURCE_DIRECTORY, glob="**/*.md", loader_cls=UnstructuredMarkdownLoader)
    docs = loader.load()
    
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # 2. Configurar Retriever de Palabras Clave (BM25)
    bm25_retriever = BM25Retriever.from_documents(splits)
    bm25_retriever.k = 3

    # 3. Configurar Retriever Semántico
    chroma_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # 4. Crear Ensemble Retriever
    # weights=[0.5, 0.5] da igual peso a ambos. Ajustar según necesidad.
    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, chroma_retriever], weights=[0.5, 0.5]
    )

    # 5. Cadena RAG
    template = """Responde basándote en el siguiente contexto recuperado:
    {context}
    
    Pregunta: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOllama(model=MODEL_NAME)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": ensemble_retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # 6. Prueba
    question = "¿Qué es un agente autónomo?"
    print(f"\nPregunta: {question}")
    
    print("Recuperando documentos (Híbrido)...")
    docs = ensemble_retriever.invoke(question)
    print(f"Se recuperaron {len(docs)} documentos combinados.")
    
    print("Generando respuesta...")
    response = rag_chain.invoke(question)
    print(f"\nRespuesta: {response}")

if __name__ == "__main__":
    main()
