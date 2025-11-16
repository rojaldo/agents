"""
MÓDULO 11: Ejemplo 1 - Búsqueda Híbrida (Vectorial + Grafos)
==============================================================

Objetivo: Combinar búsqueda vectorial (ChromaDB) con búsqueda en grafos (Neo4j)

Este ejemplo muestra cómo:
1. Integrar ChromaDB y Neo4j en un solo sistema
2. Realizar búsqueda semántica con vectores
3. Enriquecer resultados con relaciones del grafo
4. Combinar ambos enfoques para respuestas más precisas

CONCEPTO:
- Vectores: Encuentran documentos similares por significado
- Grafos: Encuentran entidades relacionadas y contexto
- Híbrido: Combina ambos para máxima relevancia

PREREQUISITOS:
- Neo4j ejecutándose
- Ollama con mistral y nomic-embed-text
"""

import sys

def verificar_sistema():
    """Verificar que todo está disponible."""
    print("Verificando sistema híbrido...")

    errores = []

    # Neo4j
    try:
        from neo4j import GraphDatabase
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
        driver.verify_connectivity()
        driver.close()
        print("  ✓ Neo4j disponible")
    except Exception as e:
        errores.append(f"Neo4j: {e}")

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
        from langchain_community.graphs import Neo4jGraph
        from langchain_ollama import OllamaLLM, OllamaEmbeddings
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


def ejemplo_1_arquitectura_hibrida():
    """Explicar arquitectura híbrida."""
    print("\n" + "="*60)
    print("EJEMPLO 1: Arquitectura Híbrida")
    print("="*60)

    print("""
ARQUITECTURA DEL SISTEMA:

┌─────────────────────────────────────────────────┐
│                 Usuario                         │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│            Sistema Híbrido RAG                  │
│                                                 │
│  1. Recibe pregunta                             │
│  2. Busca en AMBOS sistemas                     │
│  3. Combina resultados                          │
│  4. Genera respuesta con LLM                    │
└──────────┬─────────────────┬────────────────────┘
           │                 │
           ▼                 ▼
┌──────────────────┐  ┌──────────────────┐
│   ChromaDB       │  │     Neo4j        │
│   (Vectores)     │  │    (Grafos)      │
│                  │  │                  │
│ • Búsqueda       │  │ • Relaciones     │
│   semántica      │  │ • Entidades      │
│ • Similitud      │  │ • Conexiones     │
│ • Documentos     │  │ • Contexto       │
└──────────────────┘  └──────────────────┘

VENTAJAS:

✓ Búsqueda Semántica (ChromaDB):
  - Encuentra documentos por significado
  - No requiere keywords exactas
  - Basada en embeddings

✓ Relaciones y Contexto (Neo4j):
  - Entidades conectadas
  - Caminos entre conceptos
  - Estructura del conocimiento

✓ Combinación:
  - Más preciso que cada uno solo
  - Respuestas contextualizadas
  - Menor ruido en resultados

CASOS DE USO:

→ Asistentes de investigación
→ Sistemas de recomendación complejos
→ Análisis de documentos legales
→ Knowledge Management empresarial
→ Detección de fraude con contexto
    """)


def ejemplo_2_crear_datos():
    """Crear datos en ambos sistemas."""
    print("\n" + "="*60)
    print("EJEMPLO 2: Poblar Sistemas con Datos")
    print("="*60)

    from langchain_chroma import Chroma
    from langchain_community.graphs import Neo4jGraph
    from langchain_ollama import OllamaEmbeddings
    from langchain_core.documents import Document

    # Conectar sistemas
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    vector_store = Chroma(
        collection_name="hibrido_docs",
        embedding_function=embeddings,
        persist_directory="./hibrido_chroma"
    )

    graph = Neo4jGraph(
        url="bolt://localhost:7687",
        username="neo4j",
        password="password"
    )

    # Limpiar datos previos
    graph.query("MATCH (n) DETACH DELETE n")

    print("Sistemas conectados\n")

    # Datos sobre tecnología
    documentos_texto = [
        {
            "contenido": "ChromaDB es una base de datos vectorial diseñada para aplicaciones de IA. "
                        "Permite almacenar embeddings y realizar búsqueda semántica eficiente.",
            "metadata": {"tipo": "database", "categoria": "vectorial"}
        },
        {
            "contenido": "Neo4j es la base de datos de grafos líder mundial. "
                        "Usa el lenguaje Cypher para consultas y es ideal para modelar relaciones complejas.",
            "metadata": {"tipo": "database", "categoria": "grafo"}
        },
        {
            "contenido": "LangChain es un framework de Python para construir aplicaciones con LLMs. "
                        "Soporta integraciones con ChromaDB, Neo4j y múltiples proveedores de modelos.",
            "metadata": {"tipo": "framework", "categoria": "ai"}
        },
        {
            "contenido": "Ollama permite ejecutar modelos de lenguaje grandes localmente. "
                        "Soporta modelos como Mistral, Llama2 y Phi sin necesidad de GPU.",
            "metadata": {"tipo": "runtime", "categoria": "ai"}
        },
        {
            "contenido": "Los embeddings son representaciones vectoriales de texto. "
                        "Modelos como nomic-embed-text convierten palabras en vectores numéricos.",
            "metadata": {"tipo": "concepto", "categoria": "ai"}
        },
    ]

    # 1. Agregar a ChromaDB
    print("1. Agregando a ChromaDB (vectores)...")
    docs = [
        Document(page_content=d["contenido"], metadata=d["metadata"])
        for d in documentos_texto
    ]
    vector_store.add_documents(docs)
    print(f"   ✓ {len(docs)} documentos agregados\n")

    # 2. Agregar a Neo4j (grafo)
    print("2. Agregando a Neo4j (grafo)...")

    graph.query("""
        // Crear tecnologías
        CREATE (chromadb:Tecnologia {nombre: 'ChromaDB', tipo: 'Database', categoria: 'Vectorial'})
        CREATE (neo4j:Tecnologia {nombre: 'Neo4j', tipo: 'Database', categoria: 'Grafo'})
        CREATE (langchain:Tecnologia {nombre: 'LangChain', tipo: 'Framework', categoria: 'AI'})
        CREATE (ollama:Tecnologia {nombre: 'Ollama', tipo: 'Runtime', categoria: 'AI'})
        CREATE (embeddings:Concepto {nombre: 'Embeddings', categoria: 'AI'})

        // Crear relaciones
        CREATE (langchain)-[:INTEGRA_CON]->(chromadb)
        CREATE (langchain)-[:INTEGRA_CON]->(neo4j)
        CREATE (langchain)-[:INTEGRA_CON]->(ollama)

        CREATE (chromadb)-[:ALMACENA]->(embeddings)
        CREATE (ollama)-[:GENERA]->(embeddings)

        CREATE (chromadb)-[:COMPLEMENTA]->(neo4j)
        CREATE (neo4j)-[:COMPLEMENTA]->(chromadb)
    """)

    print("   ✓ Entidades y relaciones creadas\n")

    # Verificar
    resultado = graph.query("MATCH (n) RETURN count(n) as total")
    print(f"   Total nodos en Neo4j: {resultado[0]['total']}")

    resultado = graph.query("MATCH ()-[r]->() RETURN count(r) as total")
    print(f"   Total relaciones en Neo4j: {resultado[0]['total']}")

    return vector_store, graph


def ejemplo_3_busqueda_hibrida_simple(vector_store, graph):
    """Búsqueda híbrida simple."""
    print("\n" + "="*60)
    print("EJEMPLO 3: Búsqueda Híbrida Simple")
    print("="*60)

    pregunta = "¿Cómo funcionan las bases de datos vectoriales?"

    print(f"Pregunta: {pregunta}\n")

    # 1. Búsqueda vectorial
    print("1. Búsqueda VECTORIAL (ChromaDB):")
    vector_results = vector_store.similarity_search(pregunta, k=2)

    for i, doc in enumerate(vector_results, 1):
        print(f"\n   {i}. {doc.page_content[:80]}...")
        print(f"      Metadata: {doc.metadata}")

    # 2. Búsqueda en grafo
    print("\n2. Búsqueda en GRAFO (Neo4j):")
    print("   Buscando tecnologías relacionadas con 'vectorial'...\n")

    graph_results = graph.query("""
        MATCH (t:Tecnologia)
        WHERE t.categoria CONTAINS 'Vectorial' OR t.tipo CONTAINS 'Database'
        OPTIONAL MATCH (t)-[r]->(related)
        RETURN t.nombre as tecnologia, t.categoria as categoria,
               collect(related.nombre) as relacionados
    """)

    for result in graph_results:
        print(f"   - {result['tecnologia']} ({result['categoria']})")
        if result['relacionados']:
            print(f"     Relacionado con: {', '.join([r for r in result['relacionados'] if r])}")

    # 3. Combinar resultados
    print("\n3. RESULTADOS COMBINADOS:")
    print(f"""
   Búsqueda Vectorial encontró: {len(vector_results)} documentos relevantes
   Búsqueda en Grafo encontró: {len(graph_results)} entidades relacionadas

   La combinación proporciona:
   ✓ Contenido relevante (de vectores)
   ✓ Relaciones y contexto (de grafo)
   ✓ Visión más completa del tema
    """)


def ejemplo_4_rag_hibrido_completo(vector_store, graph):
    """Sistema RAG híbrido completo."""
    print("\n" + "="*60)
    print("EJEMPLO 4: RAG Híbrido Completo")
    print("="*60)

    from langchain_ollama import OllamaLLM

    llm = OllamaLLM(model="mistral", temperature=0.3)

    pregunta = "¿Qué tecnologías puedo usar para búsqueda semántica?"

    print(f"Pregunta: {pregunta}\n")

    # Paso 1: Búsqueda vectorial
    print("Paso 1: Búsqueda vectorial...")
    vector_docs = vector_store.similarity_search(pregunta, k=3)
    contexto_vectorial = "\n".join([doc.page_content for doc in vector_docs])
    print(f"  ✓ {len(vector_docs)} documentos encontrados")

    # Paso 2: Búsqueda en grafo
    print("\nPaso 2: Búsqueda en grafo...")
    graph_results = graph.query("""
        MATCH (t:Tecnologia)-[r]->(related)
        WHERE t.categoria = 'AI' OR t.categoria = 'Vectorial'
        RETURN t.nombre, type(r) as relacion, related.nombre as conectado
    """)

    contexto_grafo = "Relaciones entre tecnologías:\n"
    for result in graph_results:
        contexto_grafo += f"- {result['t.nombre']} {result['relacion']} {result['conectado']}\n"
    print(f"  ✓ {len(graph_results)} relaciones encontradas")

    # Paso 3: Combinar contextos
    print("\nPaso 3: Generando respuesta con LLM...")
    contexto_completo = f"""
INFORMACIÓN DE DOCUMENTOS (búsqueda vectorial):
{contexto_vectorial}

RELACIONES ENTRE TECNOLOGÍAS (grafo de conocimiento):
{contexto_grafo}
"""

    prompt = f"""
Usa la siguiente información para responder la pregunta.
Menciona tanto las tecnologías como sus relaciones.

{contexto_completo}

Pregunta: {pregunta}

Respuesta:
"""

    respuesta = llm.invoke(prompt)

    print("\n" + "="*60)
    print("RESPUESTA FINAL:")
    print("="*60)
    print(respuesta)
    print("="*60)


class HybridRAG:
    """Sistema RAG híbrido completo."""

    def __init__(self):
        from langchain_chroma import Chroma
        from langchain_community.graphs import Neo4jGraph
        from langchain_ollama import OllamaLLM, OllamaEmbeddings

        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.llm = OllamaLLM(model="mistral", temperature=0.3)

        self.vector_store = Chroma(
            collection_name="hibrido_docs",
            embedding_function=self.embeddings,
            persist_directory="./hibrido_chroma"
        )

        self.graph = Neo4jGraph(
            url="bolt://localhost:7687",
            username="neo4j",
            password="password"
        )

    def buscar(self, pregunta, k_vectores=3, k_grafo=5):
        """Buscar en ambos sistemas."""

        # Vectorial
        vector_docs = self.vector_store.similarity_search(pregunta, k=k_vectores)

        # Grafo - buscar entidades relevantes
        graph_results = self.graph.query(f"""
            MATCH (n)
            OPTIONAL MATCH (n)-[r]-(connected)
            RETURN n, r, connected
            LIMIT {k_grafo}
        """)

        return {
            "vectores": vector_docs,
            "grafo": graph_results
        }

    def responder(self, pregunta):
        """Responder usando búsqueda híbrida."""

        resultados = self.buscar(pregunta)

        # Construir contexto
        contexto = "DOCUMENTOS RELEVANTES:\n"
        for doc in resultados["vectores"]:
            contexto += f"- {doc.page_content}\n"

        contexto += "\nRELACIONES Y ENTIDADES:\n"
        for item in resultados["grafo"]:
            if item['r']:
                contexto += f"- {item['n']} → {item['connected']}\n"

        # Generar respuesta
        prompt = f"""
Responde basándote en la siguiente información:

{contexto}

Pregunta: {pregunta}

Respuesta:
"""

        return self.llm.invoke(prompt)


def ejemplo_5_clase_hibrida():
    """Demostrar clase HybridRAG."""
    print("\n" + "="*60)
    print("EJEMPLO 5: Clase HybridRAG Reutilizable")
    print("="*60)

    print("""
La clase HybridRAG encapsula todo el sistema:
  - Conexión a ChromaDB y Neo4j
  - Búsqueda en ambos sistemas
  - Combinación de resultados
  - Generación de respuestas

Uso:
    hybrid = HybridRAG()
    respuesta = hybrid.responder("¿Qué es LangChain?")
    print(respuesta)
    """)

    hybrid = HybridRAG()

    preguntas = [
        "¿Qué es LangChain?",
        "¿Cómo se relacionan ChromaDB y Neo4j?",
    ]

    for pregunta in preguntas:
        print(f"\nPregunta: {pregunta}")
        print("-" * 60)

        try:
            respuesta = hybrid.responder(pregunta)
            print(respuesta)
        except Exception as e:
            print(f"Error: {e}")


def ejemplo_6_ventajas_hibrido():
    """Ventajas del enfoque híbrido."""
    print("\n" + "="*60)
    print("EJEMPLO 6: Ventajas del Sistema Híbrido")
    print("="*60)

    print("""
COMPARACIÓN:

┌─────────────────┬──────────────┬──────────────┬──────────────┐
│                 │ Solo Vectores│ Solo Grafos  │   Híbrido    │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Búsqueda        │              │              │              │
│ Semántica       │      ✓       │      ✗       │      ✓       │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Relaciones      │              │              │              │
│ Explícitas      │      ✗       │      ✓       │      ✓       │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Contexto        │              │              │              │
│ Estructurado    │      ✗       │      ✓       │      ✓       │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Escalabilidad   │     Alta     │    Media     │    Media     │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Precisión       │    Media     │    Media     │     Alta     │
└─────────────────┴──────────────┴──────────────┴──────────────┘

CUÁNDO USAR HÍBRIDO:

✓ Necesitas búsqueda semántica Y relaciones
✓ Documentos con entidades interconectadas
✓ Análisis de redes con contenido textual
✓ Sistemas de recomendación avanzados
✓ Knowledge graphs con búsqueda
✓ Investigación y análisis complejo

CUÁNDO NO USAR:

✗ Solo necesitas uno de los dos
✗ Volumen muy alto (simplicidad > precisión)
✗ Recursos limitados
✗ Prototipo rápido

MEJORES PRÁCTICAS:

→ Mantener sincronizados ambos sistemas
→ Decidir qué datos van a cada sistema
→ Vectores: contenido largo, documentos
→ Grafos: entidades, relaciones, metadatos
→ Implementar caché para reducir latencia
→ Monitorear rendimiento de cada componente
    """)


def main():
    """Ejecutar todos los ejemplos."""
    print("\n")
    print("█" * 60)
    print("█  BÚSQUEDA HÍBRIDA: VECTORES + GRAFOS")
    print("█" * 60)

    if not verificar_sistema():
        print("\n⚠ Sistema no está listo")
        return

    ejemplo_1_arquitectura_hibrida()
    vector_store, graph = ejemplo_2_crear_datos()
    ejemplo_3_busqueda_hibrida_simple(vector_store, graph)
    ejemplo_4_rag_hibrido_completo(vector_store, graph)
    ejemplo_5_clase_hibrida()
    ejemplo_6_ventajas_hibrido()

    print("\n" + "="*60)
    print("✓ Todos los ejemplos completados")
    print("="*60)
    print("\nPróximos pasos:")
    print("  - Experimenta con tus propios datos")
    print("  - Visualiza el grafo en Neo4j Browser")
    print("  - Compara resultados híbridos vs individuales")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
