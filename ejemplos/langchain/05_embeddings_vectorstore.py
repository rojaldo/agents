#!/usr/bin/env python3
"""
05_embeddings_vectorstore.py - Embeddings y Vector Stores

Demuestra:
- Generar embeddings con Ollama
- Crear y usar vector stores (FAISS)
- Búsqueda de similitud
- Text splitters
"""

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os


def ejemplo_embeddings():
    """Generar embeddings de texto"""
    print("=" * 60)
    print("EJEMPLO 1: Generación de Embeddings")
    print("=" * 60)

    # Crear embeddings
    embeddings = OllamaEmbeddings(
        model="mistral",
        base_url="http://localhost:11434"
    )

    print("\nGenerando embeddings para textos...")

    textos = [
        "Python es un lenguaje de programación",
        "Los gatos son animales domésticos",
        "La inteligencia artificial es fascinante"
    ]

    for texto in textos:
        vector = embeddings.embed_query(texto)
        print(f"\n✓ Texto: {texto[:40]}...")
        print(f"  Dimensión del vector: {len(vector)}")
        print(f"  Primeros 5 valores: {vector[:5]}")


def ejemplo_text_splitter():
    """Dividir textos largos en chunks"""
    print("\n" + "=" * 60)
    print("EJEMPLO 2: Text Splitter")
    print("=" * 60)

    # Texto largo
    texto_largo = """
    Python es un lenguaje de programación versátil y poderoso. Se utiliza en diversos campos como:
    - Desarrollo web con Django y Flask
    - Ciencia de datos con NumPy y Pandas
    - Inteligencia artificial con TensorFlow
    - Automatización de tareas

    JavaScript es el lenguaje de la web. Se ejecuta en navegadores y servidores (Node.js).

    Rust es un lenguaje moderno enfocado en seguridad y rendimiento.

    LangChain es un framework para construir aplicaciones con Large Language Models.
    """

    # Splitter simple
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = splitter.split_text(texto_largo)

    print(f"\nTexto original: {len(texto_largo)} caracteres")
    print(f"Número de chunks: {len(chunks)}")
    print("\nChunks generados:")

    for i, chunk in enumerate(chunks):
        print(f"\n[{i+1}] ({len(chunk)} caracteres)")
        print(f"    {chunk[:60].strip()}...")


def ejemplo_vector_store_basico():
    """Crear un vector store simple"""
    print("\n" + "=" * 60)
    print("EJEMPLO 3: Vector Store Básico (FAISS)")
    print("=" * 60)

    embeddings = OllamaEmbeddings(
        model="mistral",
        base_url="http://localhost:11434"
    )

    # Crear documentos
    documentos = [
        Document(page_content="Python es versátil para desarrollo web"),
        Document(page_content="JavaScript domina el desarrollo frontend"),
        Document(page_content="Rust ofrece rendimiento y seguridad"),
        Document(page_content="Los gatos son felinos"),
        Document(page_content="Los perros son leales"),
    ]

    print(f"\nCreando vector store con {len(documentos)} documentos...")

    # Crear FAISS vector store
    vector_store = FAISS.from_documents(
        documentos,
        embeddings
    )

    print("✓ Vector store creado")

    # Búsqueda
    print("\nRealizando búsquedas...")

    consultas = [
        "programación web",
        "animales domésticos"
    ]

    for consulta in consultas:
        print(f"\n🔍 Búsqueda: '{consulta}'")
        resultados = vector_store.similarity_search(consulta, k=2)
        for i, doc in enumerate(resultados, 1):
            print(f"   [{i}] {doc.page_content}")


def ejemplo_similarity_search():
    """Búsqueda por similitud con puntuaciones"""
    print("\n" + "=" * 60)
    print("EJEMPLO 4: Búsqueda con Relevancia")
    print("=" * 60)

    embeddings = OllamaEmbeddings(
        model="mistral",
        base_url="http://localhost:11434"
    )

    documentos = [
        Document(page_content="Python se usa para ciencia de datos"),
        Document(page_content="NumPy es librería para cálculos numéricos"),
        Document(page_content="Pandas maneja estructuras de datos"),
        Document(page_content="Django es un framework web"),
        Document(page_content="Flask es un microframework"),
    ]

    vector_store = FAISS.from_documents(documentos, embeddings)

    print("\nBúsqueda con scores de relevancia...")

    consulta = "análisis de datos"
    print(f"\n🔍 Consulta: '{consulta}'")

    resultados = vector_store.similarity_search_with_relevance_scores(consulta, k=3)

    for i, (doc, score) in enumerate(resultados, 1):
        relevancia = "█" * int(score * 10) + "░" * (10 - int(score * 10))
        print(f"\n[{i}] Relevancia: {score:.2%} {relevancia}")
        print(f"    Contenido: {doc.page_content}")


def ejemplo_persistencia():
    """Guardar y cargar vector store"""
    print("\n" + "=" * 60)
    print("EJEMPLO 5: Persistencia de Vector Store")
    print("=" * 60)

    embeddings = OllamaEmbeddings(
        model="mistral",
        base_url="http://localhost:11434"
    )

    documentos = [
        Document(page_content="LangChain simplifica desarrollo con LLMs"),
        Document(page_content="Los agentes pueden usar herramientas"),
    ]

    # Crear y guardar
    db_path = "./temp_vectorstore"

    print(f"\n📝 Creando vector store en '{db_path}'...")
    vector_store = FAISS.from_documents(documentos, embeddings)

    # Guardar
    vector_store.save_local(db_path)
    print("✓ Vector store guardado")

    # Cargar
    print(f"\n📖 Cargando vector store desde '{db_path}'...")
    vector_store_cargado = FAISS.load_local(
        db_path,
        embeddings,
        allow_dangerous_deserialization=True
    )
    print("✓ Vector store cargado")

    # Verificar
    print("\nVerificando búsqueda en vector store cargado:")
    resultado = vector_store_cargado.similarity_search("herramientas", k=1)
    print(f"  {resultado[0].page_content}")

    # Limpiar
    import shutil
    if os.path.exists(db_path):
        shutil.rmtree(db_path)
        print(f"\n🧹 Directorio temporal '{db_path}' eliminado")


def ejemplo_crear_coleccion_documentos():
    """Crear un vector store a partir de múltiples textos"""
    print("\n" + "=" * 60)
    print("EJEMPLO 6: Colección de Documentos")
    print("=" * 60)

    embeddings = OllamaEmbeddings(
        model="mistral",
        base_url="http://localhost:11434"
    )

    # Base de conocimiento
    base_conocimiento = {
        "Python": """Python es un lenguaje interpretado de alto nivel.
        Se usa para desarrollo web, ciencia de datos, automatización.
        Tiene una sintaxis clara y comunidad grande.""",

        "JavaScript": """JavaScript es el lenguaje de la web.
        Se ejecuta en navegadores y con Node.js en servidores.
        Es versátil y tiene un ecosistema enorme.""",

        "AI": """La inteligencia artificial es el campo que busca crear máquinas inteligentes.
        Incluye machine learning, deep learning, procesamiento de lenguaje natural.
        Está revolucionando muchas industrias.""",
    }

    # Crear documentos
    documentos = [
        Document(
            page_content=contenido,
            metadata={"topic": topic}
        )
        for topic, contenido in base_conocimiento.items()
    ]

    print(f"\nCreando vector store con {len(documentos)} tópicos...")

    vector_store = FAISS.from_documents(documentos, embeddings)

    # Recuperador
    print("\nUsando como recuperador:")

    queries = ["¿Qué es Python?", "¿Dónde se usa JavaScript?", "Cuéntame sobre IA"]

    for query in queries:
        print(f"\n❓ {query}")
        resultados = vector_store.similarity_search(query, k=1)
        for doc in resultados:
            tema = doc.metadata.get("topic", "Desconocido")
            print(f"  📌 Tema: {tema}")
            print(f"  📄 {doc.page_content[:80]}...")


if __name__ == "__main__":
    try:
        print("\n🚀 Iniciando ejemplos de Embeddings y Vector Stores\n")

        ejemplo_embeddings()
        ejemplo_text_splitter()
        ejemplo_vector_store_basico()
        ejemplo_similarity_search()
        ejemplo_persistencia()
        ejemplo_crear_coleccion_documentos()

        print("\n" + "=" * 60)
        print("✅ Todos los ejemplos de embeddings completados")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Asegúrate de que Ollama está ejecutándose")
        import traceback
        traceback.print_exc()
