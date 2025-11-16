#!/usr/bin/env python3
"""
06_rag_system.py - Sistema RAG (Retrieval Augmented Generation) Completo

Demuestra:
- Crear un sistema RAG simple
- Diferentes estrategias de retrieval
- Generación de respuestas basadas en documentos
- RAG conversacional
"""

from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter


# ============ BASE DE CONOCIMIENTO ============

BASE_CONOCIMIENTO = """
Python:
Python es un lenguaje de programación interpretado, dinámico y versátil.
Se utiliza en múltiples campos: desarrollo web, ciencia de datos, automatización, inteligencia artificial.
La sintaxis es clara y legible, lo que lo hace ideal para aprender programación.
Tiene una comunidad grande y un ecosistema rico de librerías como NumPy, Pandas, Django, Flask.

JavaScript:
JavaScript es el lenguaje de programación de la web.
Se ejecuta en navegadores y también en servidores (Node.js).
Es versátil, con frameworks como React, Vue, Angular para frontend y Express para backend.
Es basado en prototipos y tiene características funcionales.
Es el lenguaje más usado en desarrollo web.

Rust:
Rust es un lenguaje moderno enfocado en seguridad y rendimiento.
Combina la velocidad de C++ con garantías de seguridad en memoria.
Es ideal para sistemas embebidos, infraestructura y aplicaciones de alto rendimiento.
Tiene un borrow checker que previene errores comunes de memoria.

LangChain:
LangChain es un framework de código abierto para construir aplicaciones con Large Language Models.
Proporciona abstracciones para trabajar con diferentes modelos, cadenas, memoria y agentes.
Soporta múltiples proveedores: OpenAI, Anthropic, Ollama, Google, etc.
Incluye RAG (Retrieval Augmented Generation) para consultas sobre documentos.
Tiene LangSmith para debugging y monitoreo de aplicaciones.

Inteligencia Artificial:
La inteligencia artificial es el campo de la informática que busca crear máquinas inteligentes.
Incluye machine learning (aprendizaje automático) donde sistemas aprenden de datos.
Deep learning usa redes neuronales profundas para tareas complejas.
NLP (procesamiento de lenguaje natural) permite máquinas entender y generar texto.
Aplicaciones: reconocimiento de voz, visión por computadora, sistemas de recomendación.

Vector Stores:
Los vector stores son bases de datos especializadas para almacenar y buscar vectores.
Son esenciales para RAG, permiten búsqueda semántica rápida.
Ejemplos: FAISS (local), Pinecone (cloud), Chroma, Weaviate.
Funcionan convirtiendo texto a embeddings (vectores numéricos).
Permiten encontrar documentos similares mediante búsqueda vectorial.
"""


# ============ UTILIDADES ============

def crear_base_datos_rag():
    """Crear una base de datos RAG a partir del conocimiento"""
    print("📚 Creando base de datos RAG...")

    # Dividir el texto en chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = splitter.split_text(BASE_CONOCIMIENTO)

    # Crear documentos
    documentos = [
        Document(
            page_content=chunk,
            metadata={"source": "base_conocimiento", "index": i}
        )
        for i, chunk in enumerate(chunks)
    ]

    # Crear vector store
    embeddings = OllamaEmbeddings(
        model="mistral",
        base_url="http://localhost:11434"
    )

    vector_store = FAISS.from_documents(documentos, embeddings)

    print(f"✓ Base de datos creada con {len(documentos)} chunks\n")

    return vector_store


# ============ EJEMPLOS RAG ============

def ejemplo_rag_simple():
    """RAG simple: buscar y generar respuesta"""
    print("=" * 60)
    print("EJEMPLO 1: RAG Simple (Retrieve + Generate)")
    print("=" * 60)

    vector_store = crear_base_datos_rag()
    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    # Template RAG
    template = """Basándote en el siguiente contexto, responde la pregunta.

Contexto:
{contexto}

Pregunta: {pregunta}

Respuesta:"""

    prompt = PromptTemplate(
        input_variables=["contexto", "pregunta"],
        template=template
    )

    cadena = prompt | llm

    # Ejecutar RAG
    preguntas = [
        "¿Para qué se usa Python?",
        "¿Cuál es la diferencia entre Rust y C++?",
        "¿Qué es LangChain?",
    ]

    for pregunta in preguntas:
        print(f"\n🔍 Pregunta: {pregunta}")

        # Retrieve: Buscar documentos relevantes
        documentos_relevantes = vector_store.similarity_search(pregunta, k=2)

        # Augment: Preparar contexto
        contexto = "\n".join([
            f"- {doc.page_content[:150]}..."
            for doc in documentos_relevantes
        ])

        # Generate: Generar respuesta
        respuesta = cadena.invoke({
            "contexto": contexto,
            "pregunta": pregunta
        })

        print(f"📄 Documentos usados: {len(documentos_relevantes)}")
        print(f"✓ Respuesta: {respuesta.strip()}\n")


def ejemplo_rag_con_contexto():
    """RAG con más contexto y formato mejorado"""
    print("=" * 60)
    print("EJEMPLO 2: RAG Mejorado con Contexto Detallado")
    print("=" * 60)

    vector_store = crear_base_datos_rag()
    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    template = """Eres un asistente experto. Responde usando el contexto proporcionado.

CONTEXTO:
{contexto}

PREGUNTA: {pregunta}

INSTRUCCIONES:
- Basa tu respuesta en el contexto
- Se conciso pero completo
- Si el contexto no tiene info, di "La información no está disponible"

RESPUESTA:"""

    prompt = PromptTemplate(
        input_variables=["contexto", "pregunta"],
        template=template
    )

    cadena = prompt | llm | StrOutputParser()

    print("\n📋 Sistema RAG Avanzado\n")

    preguntas = [
        "¿Cuáles son las aplicaciones de la inteligencia artificial?",
        "¿Qué ventajas tiene Vector Stores?",
    ]

    for pregunta in preguntas:
        print(f"\n❓ {pregunta}")

        # Retrieve con múltiples documentos
        docs = vector_store.similarity_search(pregunta, k=3)

        contexto = "\n".join([
            f"{i+1}. {doc.page_content}"
            for i, doc in enumerate(docs)
        ])

        respuesta = cadena.invoke({
            "contexto": contexto,
            "pregunta": pregunta
        })

        print(f"\n{respuesta}\n")


def ejemplo_rag_con_relevancia():
    """RAG considerando scores de relevancia"""
    print("=" * 60)
    print("EJEMPLO 3: RAG con Filtro de Relevancia")
    print("=" * 60)

    vector_store = crear_base_datos_rag()
    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    template = """Con base en:
{contexto}

Responde: {pregunta}"""

    prompt = PromptTemplate(
        input_variables=["contexto", "pregunta"],
        template=template
    )

    cadena = prompt | llm

    pregunta = "¿Qué es Machine Learning?"

    print(f"\n🔍 Pregunta: {pregunta}")

    # Búsqueda con scores
    resultados = vector_store.similarity_search_with_relevance_scores(pregunta, k=5)

    print(f"\n📊 Resultados de búsqueda (filtrados por relevancia):")

    # Filtrar por relevancia mínima
    umbral = 0.3
    documentos_relevantes = [
        (doc, score) for doc, score in resultados
        if score >= umbral
    ]

    for i, (doc, score) in enumerate(documentos_relevantes, 1):
        print(f"\n[{i}] Relevancia: {score:.0%}")
        print(f"   {doc.page_content[:100]}...")

    # Generar respuesta
    contexto = "\n".join([
        doc.page_content for doc, _ in documentos_relevantes
    ])

    respuesta = cadena.invoke({
        "contexto": contexto,
        "pregunta": pregunta
    })

    print(f"\n✓ Respuesta generada: {respuesta.strip()}\n")


def ejemplo_comparacion_retrieval():
    """Comparar diferentes estrategias de retrieval"""
    print("=" * 60)
    print("EJEMPLO 4: Comparación de Estrategias de Retrieval")
    print("=" * 60)

    vector_store = crear_base_datos_rag()

    pregunta = "¿Cuáles son los usos de Python?"

    print(f"\n🔍 Pregunta: {pregunta}\n")

    # Estrategia 1: Top 1
    print("Estrategia 1: Top 1 documento")
    docs = vector_store.similarity_search(pregunta, k=1)
    print(f"  {docs[0].page_content[:80]}...\n")

    # Estrategia 2: Top 3
    print("Estrategia 2: Top 3 documentos")
    docs = vector_store.similarity_search(pregunta, k=3)
    for i, doc in enumerate(docs, 1):
        print(f"  [{i}] {doc.page_content[:60]}...")
    print()

    # Estrategia 3: Con threshold de relevancia
    print("Estrategia 3: Con relevancia > 0.4")
    resultados = vector_store.similarity_search_with_relevance_scores(pregunta, k=5)
    documentos_filtrados = [doc for doc, score in resultados if score > 0.4]
    print(f"  Documentos encontrados: {len(documentos_filtrados)}")
    for i, doc in enumerate(documentos_filtrados, 1):
        print(f"  [{i}] {doc.page_content[:60]}...")
    print()


def ejemplo_rag_iterativo():
    """RAG iterativo: refinar búsqueda según respuesta anterior"""
    print("=" * 60)
    print("EJEMPLO 5: RAG Iterativo")
    print("=" * 60)

    vector_store = crear_base_datos_rag()
    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    print("\nBúsqueda iterativa (simula múltiples turnos de RAG)\n")

    # Primera búsqueda
    pregunta1 = "¿Qué es Python?"

    print(f"1️⃣  Primera búsqueda: '{pregunta1}'")
    docs1 = vector_store.similarity_search(pregunta1, k=1)
    print(f"   Resultado: {docs1[0].page_content[:80]}...")

    # Segunda búsqueda refinada
    pregunta2 = "¿Para qué usos es especialmente bueno Python?"

    print(f"\n2️⃣  Búsqueda refinada: '{pregunta2}'")
    docs2 = vector_store.similarity_search(pregunta2, k=1)
    print(f"   Resultado: {docs2[0].page_content[:80]}...")

    # Tercera búsqueda más específica
    pregunta3 = "¿Qué librerías tiene Python?"

    print(f"\n3️⃣  Búsqueda específica: '{pregunta3}'")
    docs3 = vector_store.similarity_search(pregunta3, k=1)
    print(f"   Resultado: {docs3[0].page_content[:80]}...\n")


if __name__ == "__main__":
    try:
        print("\n🚀 Sistema RAG (Retrieval Augmented Generation)\n")

        ejemplo_rag_simple()
        ejemplo_rag_con_contexto()
        ejemplo_rag_con_relevancia()
        ejemplo_comparacion_retrieval()
        ejemplo_rag_iterativo()

        print("=" * 60)
        print("✅ Todos los ejemplos de RAG completados")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Asegúrate de que Ollama está ejecutándose")
        import traceback
        traceback.print_exc()
