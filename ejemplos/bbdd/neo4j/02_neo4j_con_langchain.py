"""
MÓDULO 8: Ejemplo 2 - Neo4j con LangChain y Ollama
===================================================

Objetivo: Integrar Neo4j con LangChain para crear Knowledge Graphs

Este ejemplo muestra cómo:
1. Conectar Neo4j con LangChain
2. Extraer entidades y relaciones de texto usando LLM
3. Construir Knowledge Graphs automáticamente
4. Consultar grafos usando lenguaje natural

PREREQUISITOS:
- Neo4j ejecutándose (ver ejemplo anterior)
- Ollama con modelo mistral: ollama pull mistral
"""

import sys

def verificar_dependencias():
    """Verificar que todas las dependencias están disponibles."""
    print("Verificando dependencias...")

    errores = []

    # Verificar Neo4j
    try:
        from neo4j import GraphDatabase
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
        driver.verify_connectivity()
        driver.close()
        print("  ✓ Neo4j disponible")
    except Exception as e:
        errores.append(f"Neo4j no disponible: {e}")

    # Verificar Ollama
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            print("  ✓ Ollama disponible")
        else:
            errores.append("Ollama no responde correctamente")
    except Exception as e:
        errores.append(f"Ollama no disponible: {e}")

    # Verificar imports
    try:
        from langchain_community.graphs import Neo4jGraph
        from langchain_ollama import OllamaLLM
        print("  ✓ LangChain imports disponibles")
    except ImportError as e:
        errores.append(f"Error de importación: {e}")

    if errores:
        print("\n✗ Errores encontrados:")
        for error in errores:
            print(f"  - {error}")
        return False

    print("✓ Todas las dependencias disponibles\n")
    return True


def ejemplo_1_conexion_basica():
    """Conectar Neo4j con LangChain."""
    print("\n" + "="*60)
    print("EJEMPLO 1: Conexión Neo4j con LangChain")
    print("="*60)

    from langchain_community.graphs import Neo4jGraph

    print("""
LangChain proporciona Neo4jGraph para facilitar:
  - Conexión simplificada
  - Consultas en lenguaje natural
  - Integración con LLMs
  - Construcción automática de grafos
    """)

    # Conectar
    graph = Neo4jGraph(
        url="bolt://localhost:7687",
        username="neo4j",
        password="password"
    )

    # Limpiar datos previos
    graph.query("MATCH (n) DETACH DELETE n")

    print("✓ Conectado a Neo4j mediante LangChain")

    # Crear datos de ejemplo
    graph.query("""
        CREATE (p1:Persona {nombre: 'Juan', ocupacion: 'Desarrollador'})
        CREATE (p2:Persona {nombre: 'María', ocupacion: 'Data Scientist'})
        CREATE (p3:Persona {nombre: 'Carlos', ocupacion: 'DevOps'})

        CREATE (t1:Tecnologia {nombre: 'Python'})
        CREATE (t2:Tecnologia {nombre: 'Neo4j'})
        CREATE (t3:Tecnologia {nombre: 'Docker'})

        CREATE (p1)-[:USA]->(t1)
        CREATE (p1)-[:USA]->(t2)
        CREATE (p2)-[:USA]->(t1)
        CREATE (p2)-[:USA]->(t2)
        CREATE (p3)-[:USA]->(t3)
    """)

    print("✓ Datos de ejemplo creados")

    # Consultar
    resultado = graph.query("""
        MATCH (p:Persona)-[:USA]->(t:Tecnologia)
        RETURN p.nombre, collect(t.nombre) as tecnologias
    """)

    print("\nPersonas y sus tecnologías:")
    for record in resultado:
        print(f"  - {record['p.nombre']}: {', '.join(record['tecnologias'])}")

    return graph


def ejemplo_2_extraccion_entidades():
    """Extraer entidades y relaciones de texto usando LLM."""
    print("\n" + "="*60)
    print("EJEMPLO 2: Extracción de Entidades con LLM")
    print("="*60)

    from langchain_community.graphs import Neo4jGraph
    from langchain_ollama import OllamaLLM

    print("""
Concepto: Usar un LLM para extraer automáticamente:
  - Entidades (personas, lugares, organizaciones)
  - Relaciones entre entidades
  - Propiedades de cada entidad

Esto permite construir Knowledge Graphs desde texto no estructurado.
    """)

    graph = Neo4jGraph(
        url="bolt://localhost:7687",
        username="neo4j",
        password="password"
    )

    # Limpiar
    graph.query("MATCH (n) DETACH DELETE n")

    llm = OllamaLLM(model="mistral", temperature=0)

    # Texto de ejemplo
    texto = """
    LangChain es un framework para desarrollar aplicaciones con LLMs.
    Fue creado por Harrison Chase en 2022.
    LangChain soporta múltiples proveedores de LLM como OpenAI, Anthropic y Ollama.
    Neo4j puede integrarse con LangChain para crear Knowledge Graphs.
    """

    print(f"Texto a procesar:\n{texto}\n")

    # Prompt para extraer entidades y relaciones
    prompt = f"""
Extrae entidades y relaciones del siguiente texto.
Devuelve SOLO código Cypher para Neo4j, sin explicaciones.

Formato esperado:
CREATE (e1:Entidad {{nombre: "..."}})
CREATE (e2:Entidad {{nombre: "..."}})
CREATE (e1)-[:RELACION]->(e2)

Texto:
{texto}

Código Cypher:
"""

    print("Extrayendo entidades y relaciones con LLM...")
    cypher = llm.invoke(prompt)

    print(f"\nCypher generado:")
    print(cypher)

    # Ejecutar (con manejo de errores)
    try:
        # Limpiar el cypher de markdown si viene envuelto
        cypher_clean = cypher.replace("```cypher", "").replace("```", "").strip()
        graph.query(cypher_clean)
        print("\n✓ Grafo creado exitosamente")

        # Mostrar resultado
        resultado = graph.query("""
            MATCH (n)
            OPTIONAL MATCH (n)-[r]->(m)
            RETURN n, r, m
            LIMIT 10
        """)

        print("\nEntidades y relaciones creadas:")
        for record in resultado:
            if record['r']:
                print(f"  - {record['n']} → [{record['r'].type}] → {record['m']}")
            else:
                print(f"  - {record['n']}")

    except Exception as e:
        print(f"\n⚠ Error ejecutando Cypher: {e}")
        print("  El LLM puede generar Cypher no válido ocasionalmente")


def ejemplo_3_consultas_lenguaje_natural():
    """Consultar el grafo usando lenguaje natural."""
    print("\n" + "="*60)
    print("EJEMPLO 3: Consultas en Lenguaje Natural")
    print("="*60)

    from langchain_community.graphs import Neo4jGraph
    from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
    from langchain_ollama import OllamaLLM

    print("""
GraphCypherQAChain permite:
  1. Usuario hace pregunta en lenguaje natural
  2. LLM genera consulta Cypher
  3. Se ejecuta en Neo4j
  4. LLM interpreta resultados y responde

¡Todo automático!
    """)

    graph = Neo4jGraph(
        url="bolt://localhost:7687",
        username="neo4j",
        password="password"
    )

    # Crear grafo de ejemplo
    graph.query("MATCH (n) DETACH DELETE n")
    graph.query("""
        CREATE (langchain:Framework {nombre: 'LangChain', tipo: 'AI Framework'})
        CREATE (neo4j:Database {nombre: 'Neo4j', tipo: 'Graph Database'})
        CREATE (ollama:Tool {nombre: 'Ollama', tipo: 'LLM Runtime'})
        CREATE (python:Language {nombre: 'Python'})

        CREATE (langchain)-[:SOPORTA]->(neo4j)
        CREATE (langchain)-[:SOPORTA]->(ollama)
        CREATE (langchain)-[:ESCRITO_EN]->(python)
        CREATE (neo4j)-[:TIENE_DRIVER_PARA]->(python)
    """)

    print("✓ Grafo de ejemplo creado")

    # Configurar cadena
    llm = OllamaLLM(model="mistral", temperature=0)

    cypher_chain = GraphCypherQAChain.from_llm(
        llm=llm,
        graph=graph,
        verbose=True,
        return_intermediate_steps=True
    )

    # Preguntas en lenguaje natural
    preguntas = [
        "¿Qué frameworks hay en la base de datos?",
        "¿Qué soporta LangChain?",
        "¿En qué lenguaje está escrito LangChain?",
    ]

    for pregunta in preguntas:
        print(f"\n{'='*60}")
        print(f"Pregunta: {pregunta}")
        print(f"{'='*60}")

        try:
            resultado = cypher_chain.invoke({"query": pregunta})

            print(f"\nCypher generado:")
            if 'intermediate_steps' in resultado:
                for step in resultado['intermediate_steps']:
                    if 'query' in step:
                        print(f"  {step['query']}")

            print(f"\nRespuesta:")
            print(f"  {resultado['result']}")

        except Exception as e:
            print(f"⚠ Error: {e}")
            print("  El LLM puede tener dificultades con consultas complejas")


def ejemplo_4_knowledge_graph_automatico():
    """Construir Knowledge Graph desde múltiples textos."""
    print("\n" + "="*60)
    print("EJEMPLO 4: Knowledge Graph Automático")
    print("="*60)

    from langchain_community.graphs import Neo4jGraph
    from langchain_core.documents import Document
    from langchain_ollama import OllamaLLM

    print("""
Construir un Knowledge Graph completo desde textos:
  1. Procesar múltiples documentos
  2. Extraer entidades y relaciones de cada uno
  3. Consolidar en un grafo unificado
    """)

    graph = Neo4jGraph(
        url="bolt://localhost:7687",
        username="neo4j",
        password="password"
    )

    # Limpiar
    graph.query("MATCH (n) DETACH DELETE n")

    llm = OllamaLLM(model="mistral", temperature=0)

    # Documentos sobre tecnología
    documentos = [
        "Python es un lenguaje de programación creado por Guido van Rossum",
        "LangChain es un framework de Python para aplicaciones con LLMs",
        "Neo4j es una base de datos de grafos escrita en Java",
        "ChromaDB es una base de datos vectorial para embeddings",
    ]

    print("Procesando documentos...\n")

    for i, doc in enumerate(documentos, 1):
        print(f"{i}. {doc}")

        # Extraer y crear grafo
        prompt = f"""
Extrae las entidades principales y crea código Cypher.
IMPORTANTE: Usa MERGE en lugar de CREATE para evitar duplicados.

Formato:
MERGE (e1:TipoEntidad {{nombre: "Nombre"}})
MERGE (e2:TipoEntidad {{nombre: "Nombre"}})
MERGE (e1)-[:TIPO_RELACION]->(e2)

Texto: {doc}

Cypher:
"""

        cypher = llm.invoke(prompt)
        cypher_clean = cypher.replace("```cypher", "").replace("```", "").strip()

        try:
            graph.query(cypher_clean)
            print(f"   ✓ Procesado")
        except Exception as e:
            print(f"   ⚠ Error: {e}")

    # Mostrar grafo resultante
    print("\nGrafo consolidado:")

    resultado = graph.query("""
        MATCH (n)
        RETURN labels(n)[0] as tipo, count(n) as cantidad
        ORDER BY cantidad DESC
    """)

    print("\nEntidades por tipo:")
    for record in resultado:
        print(f"  - {record['tipo']}: {record['cantidad']}")

    resultado = graph.query("""
        MATCH ()-[r]->()
        RETURN type(r) as relacion, count(r) as cantidad
        ORDER BY cantidad DESC
    """)

    print("\nRelaciones por tipo:")
    for record in resultado:
        print(f"  - {record['relacion']}: {record['cantidad']}")


def ejemplo_5_ventajas_integracion():
    """Mostrar ventajas de Neo4j + LangChain + Ollama."""
    print("\n" + "="*60)
    print("EJEMPLO 5: Ventajas de la Integración")
    print("="*60)

    print("""
VENTAJAS DE NEO4J + LANGCHAIN + OLLAMA:

1. Knowledge Graph Automático:
   ✓ Extrae entidades de texto sin reglas manuales
   ✓ Identifica relaciones automáticamente
   ✓ Construye grafos desde documentos

2. Consultas en Lenguaje Natural:
   ✓ Usuarios no necesitan saber Cypher
   ✓ LLM traduce pregunta → Cypher → respuesta
   ✓ Interfaz conversacional

3. Todo Local y Privado:
   ✓ Ollama ejecuta LLM localmente
   ✓ Neo4j en tu máquina/red
   ✓ Sin enviar datos a APIs externas
   ✓ Sin costos de uso

4. Casos de Uso:
   ✓ Análisis de documentos legales
   ✓ Investigación académica
   ✓ Gestión de conocimiento empresarial
   ✓ Detección de relaciones ocultas

LIMITACIONES:

  ⚠ LLMs locales (mistral, llama2) son menos precisos que GPT-4
  ⚠ Extracción de entidades puede tener errores
  ⚠ Cypher generado puede necesitar revisión
  ⚠ Requiere recursos computacionales significativos

MEJORES PRÁCTICAS:

  → Validar Cypher generado antes de ejecutar
  → Usar MERGE en lugar de CREATE para evitar duplicados
  → Implementar manejo de errores robusto
  → Revisar manualmente el grafo resultante
  → Usar temperatura baja (0-0.2) para extracción
    """)


def main():
    """Ejecutar todos los ejemplos."""
    print("\n")
    print("█" * 60)
    print("█  NEO4J + LANGCHAIN + OLLAMA")
    print("█" * 60)

    # Verificar
    if not verificar_dependencias():
        print("\n⚠ Dependencias faltantes")
        return

    # Ejecutar ejemplos
    ejemplo_1_conexion_basica()
    ejemplo_2_extraccion_entidades()
    ejemplo_3_consultas_lenguaje_natural()
    ejemplo_4_knowledge_graph_automatico()
    ejemplo_5_ventajas_integracion()

    print("\n" + "="*60)
    print("✓ Todos los ejemplos completados")
    print("="*60)
    print("\nRecursos:")
    print("  - Neo4j Browser: http://localhost:7474")
    print("  - Visualiza el grafo creado")
    print("  - Experimenta con tus propios textos")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
