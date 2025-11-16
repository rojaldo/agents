"""
MÓDULO 6: Ejemplo 4 - Sistema RAG Avanzado con ChromaDB
========================================================

Objetivo: Construir un sistema RAG completo con ChromaDB y Ollama

Este ejemplo muestra cómo:
1. Cargar y procesar documentos
2. Dividir texto en chunks óptimos
3. Crear embeddings y almacenar en ChromaDB
4. Implementar sistema RAG (Retrieval Augmented Generation)
5. Realizar consultas con contexto

RAG = Retrieval Augmented Generation:
  1. Recuperar documentos relevantes (Retrieval)
  2. Usar como contexto para LLM (Augmented)
  3. Generar respuesta informada (Generation)

PREREQUISITOS:
- Ollama con mistral y nomic-embed-text
"""

import sys
import time

def verificar_dependencias():
    """Verificar dependencias."""
    print("Verificando dependencias...")

    errores = []

    # Ollama
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            print("  ✓ Ollama disponible")
        else:
            errores.append("Ollama no responde")
    except Exception as e:
        errores.append(f"Ollama: {e}")

    # Imports
    try:
        from langchain_chroma import Chroma
        from langchain_ollama import OllamaLLM, OllamaEmbeddings
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain_core.documents import Document
        print("  ✓ Dependencias importadas")
    except ImportError as e:
        errores.append(f"Import: {e}")

    if errores:
        print("\n✗ Errores:")
        for e in errores:
            print(f"  - {e}")
        return False

    print("✓ Sistema listo\n")
    return True


def ejemplo_1_que_es_rag():
    """Explicar qué es RAG."""
    print("\n" + "="*60)
    print("EJEMPLO 1: ¿Qué es RAG?")
    print("="*60)

    print("""
RAG (Retrieval Augmented Generation)

PROBLEMA:
  Los LLMs tienen conocimiento limitado a su fecha de entrenamiento.
  No pueden acceder a:
    - Documentos privados de tu empresa
    - Información actualizada
    - Datos específicos de tu dominio

SOLUCIÓN - RAG:

┌─────────────────────────────────────────────────┐
│  1. Usuario hace pregunta                       │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  2. Buscar documentos relevantes                │
│     (búsqueda vectorial en ChromaDB)            │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  3. Construir prompt con contexto:              │
│     "Usa estos documentos: [docs]               │
│      Pregunta: [pregunta]"                      │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  4. LLM genera respuesta basada en contexto     │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  5. Devolver respuesta al usuario               │
└─────────────────────────────────────────────────┘

VENTAJAS:

✓ LLM responde con información actualizada
✓ Basado en tus documentos privados
✓ Reduce alucinaciones
✓ Fuentes verificables
✓ Más preciso para tu dominio

COMPONENTES:

1. Vector Store (ChromaDB):
   - Almacena embeddings de documentos
   - Búsqueda por similitud semántica

2. Embeddings (Ollama):
   - Convierte texto → vectores
   - Modelo: nomic-embed-text

3. LLM (Ollama):
   - Genera respuestas
   - Modelo: mistral

4. Orchestrator (LangChain):
   - Coordina todo el flujo
   - Maneja prompts y cadenas
    """)


def ejemplo_2_preparar_documentos():
    """Cargar y preparar documentos."""
    print("\n" + "="*60)
    print("EJEMPLO 2: Preparar Documentos")
    print("="*60)

    from langchain_core.documents import Document
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    print("""
Paso 1: Crear/cargar documentos
Paso 2: Dividir en chunks (fragmentos)
Paso 3: Generar embeddings
    """)

    # Documentos de ejemplo (simularían PDFs, webs, etc.)
    documentos_raw = [
        """
        ChromaDB es una base de datos vectorial de código abierto diseñada para aplicaciones de IA.
        Características principales:
        - Embeddings automáticos
        - Persistencia local
        - API simple en Python
        - Integración con LangChain
        - Ideal para prototipos y desarrollo local
        """,
        """
        Los embeddings son representaciones numéricas de texto en espacios vectoriales.
        Un modelo de embeddings como nomic-embed-text convierte palabras y frases en vectores de 384 dimensiones.
        Textos similares en significado tienen vectores cercanos en el espacio.
        Esto permite búsqueda semántica en lugar de búsqueda por keywords.
        """,
        """
        LangChain es un framework para desarrollar aplicaciones con modelos de lenguaje.
        Proporciona:
        - Chains: Secuencias de operaciones con LLMs
        - Agents: Sistemas que toman decisiones
        - Memory: Gestión de contexto y conversaciones
        - Retrievers: Búsqueda en documentos
        - Integraciones: ChromaDB, Neo4j, Ollama, OpenAI, etc.
        """,
        """
        Ollama permite ejecutar LLMs localmente sin necesidad de GPU potente.
        Modelos disponibles:
        - mistral: 7B parámetros, excelente para chat
        - llama2: 7B/13B parámetros
        - nomic-embed-text: Para embeddings (384 dims)
        - phi: Modelo pequeño y rápido
        Ventajas: Privacidad, sin costos API, totalmente local.
        """,
        """
        RAG (Retrieval Augmented Generation) combina búsqueda con generación.
        Flujo:
        1. Indexar documentos en vector store
        2. Usuario hace pregunta
        3. Buscar documentos relevantes
        4. Incluir documentos en prompt
        5. LLM genera respuesta basada en contexto
        Esto reduce alucinaciones y permite respuestas actualizadas.
        """
    ]

    # Convertir a Documents
    print("\n1. Creando objetos Document...")
    docs = [
        Document(
            page_content=texto.strip(),
            metadata={"source": f"doc_{i}", "tema": tema}
        )
        for i, (texto, tema) in enumerate([
            (documentos_raw[0], "ChromaDB"),
            (documentos_raw[1], "Embeddings"),
            (documentos_raw[2], "LangChain"),
            (documentos_raw[3], "Ollama"),
            (documentos_raw[4], "RAG"),
        ])
    ]

    print(f"   ✓ {len(docs)} documentos creados")

    # Text Splitter
    print("\n2. Configurando Text Splitter...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,  # Tamaño de cada chunk
        chunk_overlap=50,  # Solapamiento entre chunks
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    print(f"""
   Configuración:
   - Chunk size: 200 caracteres
   - Overlap: 50 caracteres
   - Separadores: párrafos, líneas, oraciones
    """)

    # Dividir documentos
    print("3. Dividiendo documentos en chunks...")
    chunks = text_splitter.split_documents(docs)

    print(f"   ✓ {len(chunks)} chunks creados (de {len(docs)} documentos)\n")

    # Mostrar ejemplo
    print("Ejemplo de chunk:")
    print(f"   Contenido: {chunks[0].page_content[:100]}...")
    print(f"   Metadata: {chunks[0].metadata}")

    return chunks


def ejemplo_3_crear_vector_store(chunks):
    """Crear vector store con ChromaDB."""
    print("\n" + "="*60)
    print("EJEMPLO 3: Crear Vector Store")
    print("="*60)

    from langchain_chroma import Chroma
    from langchain_ollama import OllamaEmbeddings
    import os
    import shutil

    print("Creando embeddings y almacenando en ChromaDB...\n")

    # Limpiar directorio previo
    db_dir = "./rag_chromadb"
    if os.path.exists(db_dir):
        shutil.rmtree(db_dir)

    # Configurar embeddings
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    print("1. Generando embeddings con Ollama...")
    print("   Modelo: nomic-embed-text (384 dimensiones)")

    inicio = time.time()

    # Crear vector store
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_dir,
        collection_name="rag_docs"
    )

    tiempo = time.time() - inicio

    print(f"   ✓ Completado en {tiempo:.2f}s")
    print(f"   ✓ {len(chunks)} chunks indexados")
    print(f"   ✓ Persistido en: {db_dir}")

    # Verificar
    print("\n2. Verificando vector store...")
    collection = vector_store._collection
    print(f"   Total documentos: {collection.count()}")

    return vector_store


def ejemplo_4_busqueda_simple(vector_store):
    """Realizar búsqueda simple."""
    print("\n" + "="*60)
    print("EJEMPLO 4: Búsqueda Semántica")
    print("="*60)

    consultas = [
        "¿Qué es una base de datos vectorial?",
        "¿Cómo ejecutar LLMs localmente?",
        "¿Qué es RAG y cómo funciona?",
    ]

    for consulta in consultas:
        print(f"\nConsulta: '{consulta}'")
        print("-" * 60)

        # Buscar
        inicio = time.time()
        resultados = vector_store.similarity_search(consulta, k=2)
        tiempo = time.time() - inicio

        print(f"Top 2 resultados ({tiempo:.3f}s):\n")

        for i, doc in enumerate(resultados, 1):
            print(f"{i}. {doc.page_content[:150]}...")
            print(f"   Fuente: {doc.metadata.get('tema', 'N/A')}\n")


def ejemplo_5_busqueda_con_scores(vector_store):
    """Búsqueda con scores de similitud."""
    print("\n" + "="*60)
    print("EJEMPLO 5: Búsqueda con Scores")
    print("="*60)

    consulta = "embeddings vectoriales"

    print(f"Consulta: '{consulta}'\n")

    resultados = vector_store.similarity_search_with_score(consulta, k=3)

    print("Resultados con scores de similitud:\n")

    for i, (doc, score) in enumerate(resultados, 1):
        # Score más bajo = más similar (distancia)
        similitud = 1 / (1 + score)  # Convertir a 0-1
        print(f"{i}. Similitud: {similitud:.3f}")
        print(f"   {doc.page_content[:100]}...")
        print(f"   Tema: {doc.metadata.get('tema', 'N/A')}\n")


def ejemplo_6_rag_completo(vector_store):
    """Sistema RAG completo."""
    print("\n" + "="*60)
    print("EJEMPLO 6: RAG Completo")
    print("="*60)

    from langchain_ollama import OllamaLLM

    llm = OllamaLLM(model="mistral", temperature=0.3)

    pregunta = "¿Qué ventajas tiene usar Ollama con ChromaDB?"

    print(f"Pregunta: {pregunta}\n")

    # Paso 1: Recuperar documentos relevantes
    print("Paso 1: Recuperando documentos relevantes...")
    docs = vector_store.similarity_search(pregunta, k=3)
    print(f"  ✓ {len(docs)} documentos recuperados\n")

    # Paso 2: Construir contexto
    print("Paso 2: Construyendo contexto...")
    contexto = "\n\n".join([doc.page_content for doc in docs])
    print(f"  ✓ Contexto de {len(contexto)} caracteres\n")

    # Paso 3: Construir prompt
    prompt = f"""
Usa la siguiente información para responder la pregunta.
Si no sabes la respuesta, di que no lo sabes.

CONTEXTO:
{contexto}

PREGUNTA: {pregunta}

RESPUESTA:
"""

    print("Paso 3: Generando respuesta con LLM...")
    inicio = time.time()
    respuesta = llm.invoke(prompt)
    tiempo = time.time() - inicio

    print(f"  ✓ Respuesta generada en {tiempo:.2f}s\n")

    # Mostrar resultado
    print("="*60)
    print("RESPUESTA:")
    print("="*60)
    print(respuesta)
    print("="*60)

    print("\nFUENTES:")
    for i, doc in enumerate(docs, 1):
        print(f"  {i}. {doc.metadata.get('tema', 'N/A')}")


class RAGSystem:
    """Sistema RAG completo y reutilizable."""

    def __init__(self, persist_directory="./rag_chromadb"):
        from langchain_chroma import Chroma
        from langchain_ollama import OllamaLLM, OllamaEmbeddings

        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.llm = OllamaLLM(model="mistral", temperature=0.3)

        self.vector_store = Chroma(
            collection_name="rag_docs",
            embedding_function=self.embeddings,
            persist_directory=persist_directory
        )

    def agregar_documentos(self, documentos):
        """Agregar documentos al sistema."""
        from langchain.text_splitter import RecursiveCharacterTextSplitter

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )

        chunks = text_splitter.split_documents(documentos)
        self.vector_store.add_documents(chunks)

        return len(chunks)

    def consultar(self, pregunta, k=3):
        """Realizar consulta RAG."""

        # Recuperar documentos
        docs = self.vector_store.similarity_search(pregunta, k=k)

        # Construir contexto
        contexto = "\n\n".join([doc.page_content for doc in docs])

        # Prompt
        prompt = f"""
Responde basándote en el siguiente contexto.
Si no sabes, di que no lo sabes.

CONTEXTO:
{contexto}

PREGUNTA: {pregunta}

RESPUESTA:
"""

        # Generar respuesta
        respuesta = self.llm.invoke(prompt)

        return {
            "respuesta": respuesta,
            "fuentes": [doc.metadata for doc in docs],
            "num_docs": len(docs)
        }


def ejemplo_7_clase_rag():
    """Usar clase RAG."""
    print("\n" + "="*60)
    print("EJEMPLO 7: Clase RAG Reutilizable")
    print("="*60)

    print("""
La clase RAGSystem encapsula todo:
  - Vector store
  - Embeddings
  - LLM
  - Métodos de consulta

Uso simple:
    rag = RAGSystem()
    resultado = rag.consultar("¿Qué es ChromaDB?")
    print(resultado['respuesta'])
    """)

    rag = RAGSystem()

    preguntas = [
        "¿Qué es LangChain?",
        "¿Para qué sirven los embeddings?",
    ]

    for pregunta in preguntas:
        print(f"\nPregunta: {pregunta}")
        print("-" * 60)

        try:
            resultado = rag.consultar(pregunta, k=2)
            print(resultado['respuesta'])
            print(f"\n(Basado en {resultado['num_docs']} documentos)")
        except Exception as e:
            print(f"Error: {e}")


def ejemplo_8_mejores_practicas():
    """Mejores prácticas para RAG."""
    print("\n" + "="*60)
    print("EJEMPLO 8: Mejores Prácticas RAG")
    print("="*60)

    print("""
MEJORES PRÁCTICAS:

1. CHUNK SIZE:
   → Muy pequeño (100): Pierde contexto
   → Muy grande (2000): Ruido en resultados
   ✓ Óptimo: 500-1000 caracteres
   ✓ Overlap: 10-20% del chunk size

2. NÚMERO DE DOCUMENTOS (k):
   → Muy pocos (k=1): Puede perder información
   → Muchos (k=10): Ruido, límite de tokens
   ✓ Óptimo: k=3-5

3. EMBEDDINGS:
   → Para inglés: all-MiniLM-L6-v2, nomic-embed-text
   → Para multilenguaje: paraphrase-multilingual
   ✓ Local: nomic-embed-text (384 dims, rápido)

4. PROMPTS:
   ✓ Instruir claramente al LLM
   ✓ Incluir "Si no sabes, di que no lo sabes"
   ✓ Pedir que cite fuentes cuando sea posible

5. METADATA:
   ✓ Incluir: fuente, fecha, autor, sección
   ✓ Permite filtrar resultados
   ✓ Útil para rastreo de fuentes

6. EVALUACIÓN:
   → Verificar manualmente respuestas
   → Medir relevancia de documentos recuperados
   → Iterar en chunk size y k

7. RENDIMIENTO:
   ✓ Caché de embeddings ya calculados
   ✓ Batch processing para documentos grandes
   ✓ Considerar índices especializados (HNSW, IVF)

LIMITACIONES:

  ⚠ LLM puede "alucinar" aunque tenga contexto
  ⚠ Búsqueda vectorial no es perfecta
  ⚠ Requiere buenos documentos fuente
  ⚠ Límite de tokens del LLM (contexto)

CUÁNDO USAR RAG:

  ✓ Documentación empresarial
  ✓ Base de conocimiento
  ✓ Soporte técnico
  ✓ Investigación académica
  ✓ Análisis de documentos legales

CUÁNDO NO USAR:

  ✗ Preguntas de conocimiento general
  ✗ Cálculos matemáticos
  ✗ Razonamiento lógico complejo
  ✗ Datos tabulares estructurados
    """)


def main():
    """Ejecutar todos los ejemplos."""
    print("\n")
    print("█" * 60)
    print("█  SISTEMA RAG AVANZADO CON CHROMADB")
    print("█" * 60)

    if not verificar_dependencias():
        print("\n⚠ Dependencias no disponibles")
        return

    ejemplo_1_que_es_rag()
    chunks = ejemplo_2_preparar_documentos()
    vector_store = ejemplo_3_crear_vector_store(chunks)
    ejemplo_4_busqueda_simple(vector_store)
    ejemplo_5_busqueda_con_scores(vector_store)
    ejemplo_6_rag_completo(vector_store)
    ejemplo_7_clase_rag()
    ejemplo_8_mejores_practicas()

    print("\n" + "="*60)
    print("✓ Todos los ejemplos completados")
    print("="*60)
    print("\nPróximos pasos:")
    print("  - Experimenta con tus propios documentos")
    print("  - Ajusta chunk_size y overlap")
    print("  - Prueba diferentes valores de k")
    print("  - Itera en los prompts")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
