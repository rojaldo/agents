"""
MÓDULO 6: Ejemplo 2 - ChromaDB con Ollama para Embeddings
===========================================================

Objetivo: Usar ChromaDB con embeddings reales de Ollama

Este ejemplo muestra cómo:
1. Configurar Ollama para generar embeddings localmente
2. Usar ChromaDB con OllamaEmbeddings
3. Realizar búsqueda semántica con modelos locales
"""

import time
import sys

def verificar_ollama():
    """Verificar que Ollama está disponible."""
    print("Verificando Ollama...")

    try:
        import requests
        respuesta = requests.get("http://localhost:11434/api/tags", timeout=2)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            modelos = datos.get("models", [])
            print(f"✓ Ollama disponible")
            print(f"  Modelos instalados: {len(modelos)}")

            # Buscar modelo de embeddings
            tiene_embeddings = any("embed" in m.get("name", "").lower()
                                   for m in modelos)
            if tiene_embeddings:
                print(f"  ✓ Modelo de embeddings encontrado")
                return True
            else:
                print(f"  ⚠ No se encontró modelo de embeddings")
                print(f"    Instala uno con: ollama pull nomic-embed-text")
                return False

    except Exception as e:
        print(f"✗ Ollama no disponible: {e}")
        print(f"  Asegúrate de ejecutar: ollama serve")
        return False


def ejemplo_1_setup_chromadb_ollama():
    """Configurar ChromaDB con embeddings de Ollama."""
    print("\n" + "="*60)
    print("EJEMPLO 1: Setup ChromaDB + Ollama")
    print("="*60)

    try:
        from langchain_chroma import Chroma
        from langchain_ollama import OllamaEmbeddings

        print("✓ Importaciones exitosas")

        # Crear embeddings
        embeddings = OllamaEmbeddings(
            model="nomic-embed-text",
            base_url="http://localhost:11434"
        )

        print("✓ OllamaEmbeddings configurado")
        print(f"  Modelo: nomic-embed-text")
        print(f"  Dimensiones: 384")

        # Crear vector store
        vector_store = Chroma(
            collection_name="documentos_ollama",
            embedding_function=embeddings,
            persist_directory="./chroma_ollama_db",
            client_type="persistent"
        )

        print("✓ Vector Store configurado")
        print(f"  Directorio: ./chroma_ollama_db")

        return embeddings, vector_store

    except ImportError as e:
        print(f"✗ Error de importación: {e}")
        print(f"  Instala: pip install langchain langchain-chroma langchain-ollama")
        sys.exit(1)


def ejemplo_2_agregar_documentos_reales(vector_store):
    """Agregar documentos del dominio de IA."""
    print("\n" + "="*60)
    print("EJEMPLO 2: Agregar Documentos con Embeddings Ollama")
    print("="*60)

    from langchain_core.documents import Document

    # Documentos sobre temas de IA y bases de datos
    documentos_texto = [
        "Las bases de datos vectoriales almacenan embeddings numéricos de texto",
        "ChromaDB es una base de datos vectorial diseñada para IA",
        "Los modelos de embeddings convierten texto en vectores numéricos",
        "La búsqueda semántica encuentra documentos por significado, no por keywords",
        "Ollama permite ejecutar modelos de IA en local sin GPU",
        "Neo4j es una base de datos de grafos para relaciones complejas",
        "LangChain orquesta aplicaciones de IA con múltiples herramientas",
        "Los embeddings capturan el significado semántico del texto",
        "La similitud coseno mide el ángulo entre vectores (0-1)",
        "RAG combina recuperación de documentos con generación de LLM",
    ]

    # Convertir a Documents
    docs = [Document(page_content=texto) for texto in documentos_texto]

    print(f"Agregando {len(docs)} documentos...")

    inicio = time.time()
    vector_store.add_documents(docs)
    tiempo = time.time() - inicio

    print(f"✓ Documentos agregados exitosamente")
    print(f"  Tiempo total: {tiempo:.2f}s")
    print(f"  Tiempo promedio/doc: {tiempo/len(docs):.2f}s")

    return vector_store


def ejemplo_3_busqueda_semantica(vector_store):
    """Realizar búsquedas semánticas."""
    print("\n" + "="*60)
    print("EJEMPLO 3: Búsqueda Semántica Inteligente")
    print("="*60)

    consultas = [
        "¿Cómo almacenar embeddings en bases de datos?",
        "¿Qué es un modelo de embeddings?",
        "Quiero ejecutar IA localmente sin GPU",
        "¿Cómo hacer búsqueda por significado?",
    ]

    for i, consulta in enumerate(consultas, 1):
        print(f"\n{i}. Consulta: '{consulta}'")
        print("   Resultados:")

        inicio = time.time()
        resultados = vector_store.similarity_search(consulta, k=2)
        tiempo = time.time() - inicio

        for j, doc in enumerate(resultados, 1):
            print(f"      {j}. {doc.page_content[:60]}...")

        print(f"   Tiempo de búsqueda: {tiempo:.2f}s")


def ejemplo_4_busqueda_con_scores(vector_store):
    """Búsqueda con puntuaciones de similitud."""
    print("\n" + "="*60)
    print("EJEMPLO 4: Búsqueda con Scores de Similitud")
    print("="*60)

    consulta = "bases de datos para machine learning"

    print(f"Consulta: '{consulta}'")
    print("\nResultados con scores de similitud:")

    resultados_con_scores = vector_store.similarity_search_with_score(
        consulta, k=3
    )

    for i, (doc, score) in enumerate(resultados_con_scores, 1):
        # Score está entre 0 y 1 (1 = perfectamente similar)
        porcentaje = score * 100
        print(f"\n{i}. Similitud: {porcentaje:.1f}%")
        print(f"   Contenido: {doc.page_content}")


def ejemplo_5_comparacion_modelos():
    """Comparar embeddings entre consultas similares."""
    print("\n" + "="*60)
    print("EJEMPLO 5: Comparación de Similitud Semántica")
    print("="*60)

    from langchain_ollama import OllamaEmbeddings
    import numpy as np

    try:
        embeddings = OllamaEmbeddings(model="nomic-embed-text")

        textos = [
            "base de datos vectorial",
            "almacenar embeddings",
            "búsqueda semántica",
            "gato pequeño",
            "perro pequeño",
        ]

        print(f"Analizando similitud entre {len(textos)} textos...\n")

        # Generar embeddings
        vectores = []
        for texto in textos:
            vec = embeddings.embed_query(texto)
            vectores.append(np.array(vec))

        # Calcular similitud coseno
        print("Matriz de Similitud Coseno:\n")

        # Headers
        print("      ", end="")
        for t in textos:
            print(f"{t[:12]:12} ", end="")
        print()

        for i, texto1 in enumerate(textos):
            print(f"{texto1[:6]:6} ", end="")

            for j, texto2 in enumerate(textos):
                # Similitud coseno
                dot_product = np.dot(vectores[i], vectores[j])
                norma1 = np.linalg.norm(vectores[i])
                norma2 = np.linalg.norm(vectores[j])

                similaridad = dot_product / (norma1 * norma2)

                print(f"{similaridad:12.3f} ", end="")

            print()

        print("\nObservaciones:")
        print("  - 'base de datos vectorial' vs 'almacenar embeddings': muy similar")
        print("  - 'gato pequeño' vs 'perro pequeño': similar (animales)")
        print("  - Vectores ≠ búsqueda exacta, sino significado semántico")

    except Exception as e:
        print(f"Error: {e}")
        print("Asegúrate de tener nomic-embed-text instalado en Ollama")


def ejemplo_6_uso_avanzado():
    """Mostrar uso avanzado: como_retriever en cadenas LangChain."""
    print("\n" + "="*60)
    print("EJEMPLO 6: Uso Avanzado - Como Retriever")
    print("="*60)

    print("""
Patrón común en RAG:

1. Crear vector store (ChromaDB + Ollama)
2. Convertir a retriever
3. Usar en cadena con LLM

Ejemplo:

    from langchain_ollama import OllamaLLM
    from langchain.chains import RetrievalQA

    vector_store = setup_chromadb_ollama()
    retriever = vector_store.as_retriever(k=3)

    llm = OllamaLLM(model="mistral")

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever
    )

    respuesta = qa_chain.run("¿Qué es ChromaDB?")

Beneficios:
  ✓ LLM responde basado en documentos relevantes
  ✓ Todo ejecutado localmente
  ✓ Sin costos de API
  ✓ Privacidad garantizada
    """)


def main():
    """Ejecutar todos los ejemplos."""
    print("\n")
    print("█" * 60)
    print("█  CHROMADB + OLLAMA: BÚSQUEDA SEMÁNTICA LOCAL")
    print("█" * 60)

    # Verificar Ollama
    if not verificar_ollama():
        print("\n⚠ Instalando modelo de embeddings...")
        print("  Ejecuta: ollama pull nomic-embed-text")
        return

    # Setup
    embeddings, vector_store = ejemplo_1_setup_chromadb_ollama()

    # Agregar documentos
    vector_store = ejemplo_2_agregar_documentos_reales(vector_store)

    # Búsqueda
    ejemplo_3_busqueda_semantica(vector_store)

    # Con scores
    ejemplo_4_busqueda_con_scores(vector_store)

    # Comparación
    try:
        ejemplo_5_comparacion_modelos()
    except Exception as e:
        print(f"\n⚠ Ejemplo 5 omitido: {e}")

    # Uso avanzado
    ejemplo_6_uso_avanzado()

    print("\n" + "="*60)
    print("✓ Ejemplos completados")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
