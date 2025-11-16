"""
MÓDULO 6: Ejemplo 1 - ChromaDB Básico
======================================

Objetivo: Aprender los fundamentos de ChromaDB con Ollama

ChromaDB es la opción ideal para:
- Desarrollo y prototipado
- Aplicaciones sin infraestructura
- Búsqueda semántica rápida
- Integración con LangChain
"""

import chromadb
import time

def crear_cliente_chromadb():
    """
    Crear cliente de ChromaDB con persistencia local.

    Por defecto, ChromaDB guarda los datos en memoria.
    Para persistencia, usamos PersistentClient.
    """
    # ChromaDB 0.4+ usa PersistentClient
    client = chromadb.PersistentClient(path="./chroma_db")
    return client


def ejemplo_1_crear_coleccion():
    """Crear una colección en ChromaDB."""
    print("\n" + "="*60)
    print("EJEMPLO 1: Crear Colección")
    print("="*60)

    client = crear_cliente_chromadb()

    # Eliminar colección si ya existe
    try:
        client.delete_collection(name="documentos")
    except:
        pass

    # Crear colección
    coleccion = client.create_collection(
        name="documentos",
        metadata={"hnsw:space": "cosine"}  # Usar similitud coseno
    )

    print(f"✓ Colección creada: {coleccion.name}")
    print(f"  Espacio métrico: Cosine (similitud semántica)")
    print(f"  Documentos: {coleccion.count()}")

    return client, coleccion


def ejemplo_2_agregar_documentos(client, coleccion):
    """Agregar documentos con embeddings."""
    print("\n" + "="*60)
    print("EJEMPLO 2: Agregar Documentos")
    print("="*60)

    documentos = [
        "Python es un lenguaje de programación versátil",
        "Las bases de datos vectoriales permiten búsqueda semántica",
        "Ollama ejecuta LLMs en local sin GPU",
        "Neo4j es una base de datos de grafos",
        "LangChain conecta LLMs con datos externos",
        "Los embeddings representan texto como vectores numéricos",
    ]

    ids = [f"doc_{i}" for i in range(len(documentos))]

    # ChromaDB genera automáticamente embeddings
    # Nota: ChromaDB usa un modelo por defecto, pero podemos especificar otro
    inicio = time.time()

    coleccion.add(
        ids=ids,
        documents=documentos,
        metadatas=[{"source": "curso"} for _ in documentos]
    )

    tiempo = time.time() - inicio

    print(f"✓ {len(documentos)} documentos agregados")
    print(f"  Tiempo: {tiempo:.2f}s")
    print(f"  Total en colección: {coleccion.count()}")
    print(f"\n  Documentos agregados:")
    for i, doc in enumerate(documentos[:3], 1):
        print(f"    {i}. {doc[:50]}...")


def ejemplo_3_busqueda_basica(coleccion):
    """Realizar búsqueda semántica."""
    print("\n" + "="*60)
    print("EJEMPLO 3: Búsqueda Semántica")
    print("="*60)

    try:
        consulta = "¿Qué permite búsqueda inteligente en textos?"

        # Búsqueda sin scores
        resultados = coleccion.query(
            query_texts=[consulta],
            n_results=3
        )

        print(f"Consulta: '{consulta}'")
        print(f"\nTop 3 resultados:")

        for i, (doc, meta) in enumerate(
            zip(resultados['documents'][0],
                resultados['metadatas'][0]),
            1
        ):
            print(f"\n  {i}. {doc}")
            print(f"     Metadata: {meta}")

    except Exception as e:
        print(f"⚠ Error en búsqueda: {e}")
        print("  ChromaDB necesita embeddings para buscar")
        print("  Esto es esperado sin conexión a Ollama/OpenAI")


def ejemplo_4_filtrado_metadata(client):
    """Filtrar documentos por metadata."""
    print("\n" + "="*60)
    print("EJEMPLO 4: Filtrado por Metadata")
    print("="*60)

    # Eliminar y crear colección con más metadata
    try:
        client.delete_collection(name="articulos")
    except:
        pass

    col = client.get_or_create_collection("articulos")

    articulos = [
        ("Intro a Python", "tutorial", "Básico"),
        ("Bases de datos vectoriales", "articulo", "Avanzado"),
        ("FastAPI en 5 minutos", "tutorial", "Intermedio"),
    ]

    for i, (titulo, tipo, nivel) in enumerate(articulos):
        col.add(
            ids=[f"art_{i}"],
            documents=[titulo],
            metadatas=[{"tipo": tipo, "nivel": nivel}]
        )

    print(f"✓ {len(articulos)} artículos agregados")

    # Filtrar
    query_filter = {"tipo": "tutorial"}
    resultados = col.query(
        query_texts=["cómo aprender programación"],
        n_results=5,
        where=query_filter
    )

    print(f"\nBúsqueda de 'cómo aprender programación'")
    print(f"Filtro: tipo='tutorial'")
    print(f"\nResultados encontrados:")
    for doc in resultados['documents'][0]:
        print(f"  - {doc}")


def ejemplo_5_actualizacion_eliminacion(client):
    """Actualizar y eliminar documentos."""
    print("\n" + "="*60)
    print("EJEMPLO 5: Actualizar y Eliminar")
    print("="*60)

    # Eliminar y crear colección
    try:
        client.delete_collection(name="versiones")
    except:
        pass

    col = client.get_or_create_collection("versiones")

    # Crear documento
    col.add(
        ids=["v1"],
        documents=["Versión 1.0 del documento"]
    )

    print(f"✓ Documento original agregado")
    print(f"  Contenido: 'Versión 1.0 del documento'")

    # Actualizar
    col.update(
        ids=["v1"],
        documents=["Versión 2.0 mejorada del documento"]
    )

    print(f"\n✓ Documento actualizado")
    print(f"  Contenido: 'Versión 2.0 mejorada del documento'")

    # Obtener
    resultado = col.get(ids=["v1"])
    print(f"\n  Contenido actual: '{resultado['documents'][0]}'")

    # Eliminar
    col.delete(ids=["v1"])
    print(f"\n✓ Documento eliminado")
    print(f"  Total documentos: {col.count()}")


def ejemplo_6_caracteristicas_chromadb():
    """Mostrar características clave de ChromaDB."""
    print("\n" + "="*60)
    print("EJEMPLO 6: Características Clave de ChromaDB")
    print("="*60)

    print("""
VENTAJAS:
  ✓ Instalación simple: pip install chromadb
  ✓ Sin servidores externos
  ✓ Embeddings automáticos
  ✓ Excelente para prototipado
  ✓ LangChain integration
  ✓ Persistencia local

DESVENTAJAS:
  ✗ Máx 1M de vectores
  ✗ Single-machine
  ✗ No ideal para producción crítica

CUÁNDO USAR:
  → Desarrollo local
  → Prototipos rápidos
  → RAG simple
  → Proyectos personales
  → Educación/aprendizaje

CUÁNDO NO USAR:
  → Millones de vectores
  → Alta disponibilidad requerida
  → Múltiples máquinas
  → Alta concurrencia
    """)


def main():
    """Ejecutar todos los ejemplos."""
    print("\n")
    print("█" * 60)
    print("█  CHROMADB: BASE DE DATOS VECTORIAL LOCAL")
    print("█" * 60)

    # Crear cliente
    client, coleccion = ejemplo_1_crear_coleccion()

    # Agregar documentos
    ejemplo_2_agregar_documentos(client, coleccion)

    # Búsqueda básica
    ejemplo_3_busqueda_basica(coleccion)

    # Filtrado
    ejemplo_4_filtrado_metadata(client)

    # Actualización
    ejemplo_5_actualizacion_eliminacion(client)

    # Características
    ejemplo_6_caracteristicas_chromadb()

    print("\n" + "="*60)
    print("✓ Todos los ejemplos completados exitosamente")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
