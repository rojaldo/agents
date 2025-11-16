#!/usr/bin/env python3
"""
03_rag_document_processing.py - RAG (Retrieval Augmented Generation)

Demuestra el flujo RAG en Langflow:
[Upload PDF] → [Text Splitter] → [Embeddings] → [Vector Store]
                                                         ↓
[User Query] → [Similarity Search] → [LLM] → [Output]
"""

from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ejemplo_1_text_splitting():
    """Ejemplo 1: Dividir textos en chunks"""
    print("=" * 60)
    print("EJEMPLO 1: Text Splitting")
    print("=" * 60)

    # Documento largo
    documento = """
    LangChain es un framework que simplifica la construcción de aplicaciones con LLMs.
    Proporciona abstracciones sobre proveedores de modelos, manejo de memoria,
    cadenas de procesamiento y mucho más.

    Langflow es una interfaz visual para LangChain, permitiendo construir flujos
    sin escribir código. Es perfect para prototipado rápido.

    RAG (Retrieval Augmented Generation) es un patrón donde primero recuperas
    información relevante y luego la usas para generar respuestas.
    """

    # Splitter
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=100,
        chunk_overlap=20
    )

    chunks = splitter.split_text(documento)

    print(f"\n📄 Documento original:")
    print(f"   Longitud: {len(documento)} caracteres")
    print(f"\n✂️ Dividido en {len(chunks)} chunks:")

    for i, chunk in enumerate(chunks, 1):
        print(f"   Chunk {i}: {chunk[:50]}... ({len(chunk)} chars)")


def ejemplo_2_embeddings():
    """Ejemplo 2: Crear embeddings de textos"""
    print("\n" + "=" * 60)
    print("EJEMPLO 2: Embeddings")
    print("=" * 60)

    try:
        embeddings = OllamaEmbeddings(
            model="mistral",
            base_url="http://localhost:11434"
        )

        textos = [
            "Python es un lenguaje de programación",
            "JavaScript se usa para desarrollo web",
            "SQL es para bases de datos",
            "Python es fácil de aprender"
        ]

        print(f"\n🔢 Creando embeddings para {len(textos)} textos...")

        vectores = []
        for i, texto in enumerate(textos):
            print(f"   {i+1}. Embebiendo: {texto[:40]}...")
            try:
                vector = embeddings.embed_query(texto)
                vectores.append(vector)
                print(f"      ✅ Vector dimension: {len(vector)}")
                logger.info(f"Embedding creado: {len(vector)} dimensiones")
            except Exception as e:
                print(f"      ❌ Error: {e}")

        print(f"\n✅ Total de embeddings creados: {len(vectores)}")

    except Exception as e:
        print(f"❌ Error en embeddings: {e}")
        logger.error(f"Error: {e}")


def ejemplo_3_vector_store():
    """Ejemplo 3: Vector store (FAISS)"""
    print("\n" + "=" * 60)
    print("EJEMPLO 3: Vector Store (FAISS)")
    print("=" * 60)

    try:
        # Textos a indexar
        textos = [
            "Python es un lenguaje interpretado y dinámico",
            "JavaScript se ejecuta en navegadores",
            "Rust es un lenguaje seguro y rápido",
            "Java se usa en aplicaciones empresariales",
            "Go es ideal para microservicios"
        ]

        # Crear documentos
        documentos = [Document(page_content=texto) for texto in textos]

        # Crear embeddings
        embeddings = OllamaEmbeddings(
            model="mistral",
            base_url="http://localhost:11434"
        )

        print(f"\n📚 Creando vector store con {len(documentos)} documentos...")

        # Crear FAISS
        vector_store = FAISS.from_documents(documentos, embeddings)

        print(f"   ✅ Vector store creado")
        logger.info(f"Vector store con {len(documentos)} documentos")

        # Realizar búsquedas
        queries = [
            "¿Qué es Python?",
            "Lenguajes de programación",
            "Desarrollo web"
        ]

        print(f"\n🔍 Realizando búsquedas de similitud:\n")

        for query in queries:
            print(f"   Query: {query}")

            try:
                resultados = vector_store.similarity_search(query, k=2)

                for i, resultado in enumerate(resultados, 1):
                    print(f"      {i}. {resultado.page_content[:50]}...")

            except Exception as e:
                print(f"      ❌ Error: {e}")

    except Exception as e:
        print(f"❌ Error en vector store: {e}")
        logger.error(f"Error: {e}")


def ejemplo_4_rag_basico():
    """Ejemplo 4: RAG básico (Retrieval + Generation)"""
    print("\n" + "=" * 60)
    print("EJEMPLO 4: RAG Básico")
    print("=" * 60)

    try:
        # Documentos
        textos = [
            "LangChain es un framework para construir aplicaciones con LLMs",
            "Langflow proporciona una interfaz visual para LangChain",
            "RAG combina recuperación de documentos con generación de texto",
            "Los embeddings permiten buscar similaridad semántica",
            "Vector stores almacenan embeddings para búsqueda rápida"
        ]

        documentos = [Document(page_content=texto) for texto in textos]

        # Crear vector store
        embeddings = OllamaEmbeddings(
            model="mistral",
            base_url="http://localhost:11434"
        )

        vector_store = FAISS.from_documents(documentos, embeddings)

        # LLM
        llm = Ollama(model="mistral", base_url="http://localhost:11434")

        # Prompt
        prompt = ChatPromptTemplate.from_template(
            """Basado en estos documentos:
{context}

Responde la pregunta: {question}"""
        )

        # Simulación de queries RAG
        queries = [
            "¿Qué es Langflow?",
            "¿Cómo funciona RAG?",
            "¿Para qué sirven los embeddings?"
        ]

        print(f"\n🔄 Ejecutando RAG para {len(queries)} queries:\n")

        for query in queries:
            print(f"❓ Pregunta: {query}")

            try:
                # Paso 1: Retrieval
                docs_relevantes = vector_store.similarity_search(query, k=2)
                context = "\n".join([doc.page_content for doc in docs_relevantes])

                print(f"   📚 Documentos recuperados: {len(docs_relevantes)}")

                # Paso 2: Generation
                respuesta = llm.invoke(
                    prompt.format(context=context, question=query)
                )

                print(f"   🤖 Respuesta: {respuesta[:100]}...")
                logger.info(f"RAG completado para: {query}")

            except Exception as e:
                print(f"   ❌ Error: {e}")

    except Exception as e:
        print(f"❌ Error en RAG: {e}")
        logger.error(f"Error: {e}")


def ejemplo_5_rag_avanzado():
    """Ejemplo 5: RAG con búsqueda por relevancia"""
    print("\n" + "=" * 60)
    print("EJEMPLO 5: RAG Avanzado (con scores)")
    print("=" * 60)

    try:
        # Documentos
        textos = [
            "Python es fácil de aprender",
            "JavaScript dominó el desarrollo web",
            "Rust garantiza seguridad de memoria",
            "Go es excelente para concurrencia"
        ]

        documentos = [Document(page_content=texto) for texto in textos]

        embeddings = OllamaEmbeddings(
            model="mistral",
            base_url="http://localhost:11434"
        )

        vector_store = FAISS.from_documents(documentos, embeddings)

        # Búsqueda con scores
        query = "lenguajes de programación"

        print(f"\n🔍 Búsqueda: {query}\n")

        try:
            resultados = vector_store.similarity_search_with_relevance_scores(query, k=3)

            for (doc, score) in resultados:
                porcentaje = score * 100
                print(f"   [{porcentaje:.1f}%] {doc.page_content}")

            logger.info(f"Búsqueda completada: {len(resultados)} resultados")

        except Exception as e:
            print(f"   ❌ Error: {e}")

    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Error: {e}")


def main():
    """Función principal"""
    try:
        ejemplo_1_text_splitting()
        ejemplo_2_embeddings()
        ejemplo_3_vector_store()
        ejemplo_4_rag_basico()
        ejemplo_5_rag_avanzado()

        print("\n" + "=" * 60)
        print("✅ Todos los ejemplos de RAG completados")
        print("=" * 60)

    except Exception as e:
        logger.critical(f"Error fatal: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
