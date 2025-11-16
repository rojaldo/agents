"""
MÓDULO 8: Ejemplo 1 - Neo4j Básico con Python
==============================================

Objetivo: Aprender los fundamentos de Neo4j con Python

Este ejemplo muestra cómo:
1. Conectar a Neo4j
2. Crear nodos y relaciones
3. Realizar consultas Cypher básicas
4. Trabajar con el driver oficial de Neo4j

PREREQUISITOS:
- Neo4j debe estar ejecutándose en Docker:
  docker run --name neo4j -p 7687:7687 -p 7474:7474 -e NEO4J_AUTH=neo4j/password neo4j:latest
"""

import sys

def verificar_neo4j():
    """Verificar que Neo4j está disponible."""
    print("Verificando conexión a Neo4j...")

    try:
        from neo4j import GraphDatabase

        URI = "bolt://localhost:7687"
        AUTH = ("neo4j", "password")

        driver = GraphDatabase.driver(URI, auth=AUTH)
        driver.verify_connectivity()
        driver.close()

        print("✓ Neo4j está disponible y accesible")
        return True

    except ImportError:
        print("✗ neo4j driver no instalado")
        print("  Instala con: pip install neo4j>=5.0.0")
        return False
    except Exception as e:
        print(f"✗ No se puede conectar a Neo4j: {e}")
        print("  Asegúrate de ejecutar:")
        print("  docker run --name neo4j -p 7687:7687 -p 7474:7474 \\")
        print("    -e NEO4J_AUTH=neo4j/password neo4j:latest")
        return False


def ejemplo_1_crear_nodos():
    """Crear nodos básicos en Neo4j."""
    print("\n" + "="*60)
    print("EJEMPLO 1: Crear Nodos")
    print("="*60)

    from neo4j import GraphDatabase

    URI = "bolt://localhost:7687"
    AUTH = ("neo4j", "password")

    driver = GraphDatabase.driver(URI, auth=AUTH)

    print("""
Concepto: Los nodos son las entidades principales en un grafo.
Similar a filas en SQL, pero con etiquetas (labels) y propiedades.

Sintaxis Cypher:
  CREATE (p:Persona {nombre: "Juan", edad: 30})
    """)

    # Limpiar datos previos
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

    # Crear nodos
    def crear_persona(tx, nombre, edad, ciudad):
        result = tx.run(
            "CREATE (p:Persona {nombre: $nombre, edad: $edad, ciudad: $ciudad}) "
            "RETURN p",
            nombre=nombre, edad=edad, ciudad=ciudad
        )
        return result.single()[0]

    with driver.session() as session:
        print("\nCreando personas...")

        personas = [
            ("Juan", 30, "Madrid"),
            ("María", 28, "Barcelona"),
            ("Carlos", 32, "Madrid"),
            ("Diana", 26, "Valencia"),
        ]

        for nombre, edad, ciudad in personas:
            persona = session.execute_write(crear_persona, nombre, edad, ciudad)
            print(f"  ✓ Creado: {persona['nombre']} ({persona['edad']} años, {persona['ciudad']})")

    # Verificar creación
    with driver.session() as session:
        result = session.run("MATCH (p:Persona) RETURN count(p) as total")
        total = result.single()["total"]
        print(f"\n✓ Total de personas creadas: {total}")

    driver.close()


def ejemplo_2_crear_relaciones():
    """Crear relaciones entre nodos."""
    print("\n" + "="*60)
    print("EJEMPLO 2: Crear Relaciones")
    print("="*60)

    from neo4j import GraphDatabase

    URI = "bolt://localhost:7687"
    AUTH = ("neo4j", "password")

    driver = GraphDatabase.driver(URI, auth=AUTH)

    print("""
Concepto: Las relaciones conectan nodos y tienen tipo y propiedades.
Son entidades de primera clase, no simples joins.

Sintaxis Cypher:
  MATCH (a:Persona {nombre: "Juan"}), (b:Persona {nombre: "María"})
  CREATE (a)-[:AMIGO_DE {desde: "2020-01-01"}]->(b)
    """)

    def crear_amistad(tx, nombre1, nombre2, desde):
        result = tx.run(
            """
            MATCH (a:Persona {nombre: $nombre1})
            MATCH (b:Persona {nombre: $nombre2})
            CREATE (a)-[r:AMIGO_DE {desde: $desde}]->(b)
            RETURN a.nombre, b.nombre, r.desde
            """,
            nombre1=nombre1, nombre2=nombre2, desde=desde
        )
        return result.single()

    with driver.session() as session:
        print("\nCreando amistades...")

        amistades = [
            ("Juan", "María", "2020-01-15"),
            ("Juan", "Carlos", "2019-06-10"),
            ("María", "Diana", "2021-03-20"),
            ("Carlos", "Diana", "2020-08-05"),
        ]

        for nombre1, nombre2, desde in amistades:
            rel = session.execute_write(crear_amistad, nombre1, nombre2, desde)
            print(f"  ✓ {rel[0]} → {rel[1]} (desde {rel[2]})")

    # Contar relaciones
    with driver.session() as session:
        result = session.run("MATCH ()-[r:AMIGO_DE]->() RETURN count(r) as total")
        total = result.single()["total"]
        print(f"\n✓ Total de amistades creadas: {total}")

    driver.close()


def ejemplo_3_consultas_basicas():
    """Realizar consultas Cypher básicas."""
    print("\n" + "="*60)
    print("EJEMPLO 3: Consultas Cypher Básicas")
    print("="*60)

    from neo4j import GraphDatabase

    URI = "bolt://localhost:7687"
    AUTH = ("neo4j", "password")

    driver = GraphDatabase.driver(URI, auth=AUTH)

    with driver.session() as session:
        # Consulta 1: Buscar personas
        print("\n1. Buscar todas las personas:")
        result = session.run("MATCH (p:Persona) RETURN p.nombre, p.edad, p.ciudad")
        for record in result:
            print(f"   - {record['p.nombre']}: {record['p.edad']} años, {record['p.ciudad']}")

        # Consulta 2: Buscar amigos de una persona
        print("\n2. Amigos de Juan:")
        result = session.run(
            """
            MATCH (p:Persona {nombre: 'Juan'})-[:AMIGO_DE]->(amigo)
            RETURN amigo.nombre, amigo.edad
            """
        )
        for record in result:
            print(f"   - {record['amigo.nombre']} ({record['amigo.edad']} años)")

        # Consulta 3: Personas mayores de 28
        print("\n3. Personas mayores de 28 años:")
        result = session.run(
            """
            MATCH (p:Persona)
            WHERE p.edad > 28
            RETURN p.nombre, p.edad
            ORDER BY p.edad DESC
            """
        )
        for record in result:
            print(f"   - {record['p.nombre']}: {record['p.edad']} años")

        # Consulta 4: Personas de Madrid
        print("\n4. Personas de Madrid:")
        result = session.run(
            """
            MATCH (p:Persona)
            WHERE p.ciudad = 'Madrid'
            RETURN p.nombre
            """
        )
        for record in result:
            print(f"   - {record['p.nombre']}")

        # Consulta 5: Amigos de amigos (2 niveles)
        print("\n5. Amigos de amigos de Juan (distancia 2):")
        result = session.run(
            """
            MATCH (juan:Persona {nombre: 'Juan'})-[:AMIGO_DE*2]->(amigo_amigo)
            RETURN DISTINCT amigo_amigo.nombre
            """
        )
        for record in result:
            print(f"   - {record['amigo_amigo.nombre']}")

    driver.close()


def ejemplo_4_agregaciones():
    """Realizar agregaciones y análisis."""
    print("\n" + "="*60)
    print("EJEMPLO 4: Agregaciones y Análisis")
    print("="*60)

    from neo4j import GraphDatabase

    URI = "bolt://localhost:7687"
    AUTH = ("neo4j", "password")

    driver = GraphDatabase.driver(URI, auth=AUTH)

    with driver.session() as session:
        # Número de amigos por persona
        print("\n1. Número de amigos por persona:")
        result = session.run(
            """
            MATCH (p:Persona)
            OPTIONAL MATCH (p)-[:AMIGO_DE]->(amigos)
            RETURN p.nombre, count(amigos) as num_amigos
            ORDER BY num_amigos DESC
            """
        )
        for record in result:
            print(f"   - {record['p.nombre']}: {record['num_amigos']} amigos")

        # Edad promedio
        print("\n2. Edad promedio de las personas:")
        result = session.run(
            """
            MATCH (p:Persona)
            RETURN avg(p.edad) as edad_promedio
            """
        )
        edad_promedio = result.single()["edad_promedio"]
        print(f"   - {edad_promedio:.1f} años")

        # Distribución por ciudad
        print("\n3. Distribución por ciudad:")
        result = session.run(
            """
            MATCH (p:Persona)
            RETURN p.ciudad, count(p) as total
            ORDER BY total DESC
            """
        )
        for record in result:
            print(f"   - {record['p.ciudad']}: {record['total']} personas")

    driver.close()


def ejemplo_5_actualizacion_eliminacion():
    """Actualizar y eliminar nodos/relaciones."""
    print("\n" + "="*60)
    print("EJEMPLO 5: Actualización y Eliminación")
    print("="*60)

    from neo4j import GraphDatabase

    URI = "bolt://localhost:7687"
    AUTH = ("neo4j", "password")

    driver = GraphDatabase.driver(URI, auth=AUTH)

    with driver.session() as session:
        # Actualizar propiedad
        print("\n1. Actualizar edad de Juan:")
        result = session.run(
            """
            MATCH (p:Persona {nombre: 'Juan'})
            SET p.edad = 31
            RETURN p.nombre, p.edad
            """
        )
        record = result.single()
        print(f"   ✓ {record['p.nombre']} ahora tiene {record['p.edad']} años")

        # Agregar nueva propiedad
        print("\n2. Agregar email a María:")
        result = session.run(
            """
            MATCH (p:Persona {nombre: 'María'})
            SET p.email = 'maria@example.com'
            RETURN p.nombre, p.email
            """
        )
        record = result.single()
        print(f"   ✓ {record['p.nombre']}: {record['p.email']}")

        # Eliminar propiedad
        print("\n3. Eliminar ciudad de Carlos:")
        result = session.run(
            """
            MATCH (p:Persona {nombre: 'Carlos'})
            REMOVE p.ciudad
            RETURN p.nombre, p.ciudad
            """
        )
        record = result.single()
        print(f"   ✓ Ciudad de Carlos: {record['p.ciudad']}")

    driver.close()


def ejemplo_6_ventajas_neo4j():
    """Mostrar ventajas de Neo4j."""
    print("\n" + "="*60)
    print("EJEMPLO 6: Ventajas de Neo4j")
    print("="*60)

    print("""
VENTAJAS:
  ✓ Rendimiento en consultas de relaciones (tiempo constante)
  ✓ Lenguaje Cypher intuitivo y expresivo
  ✓ Visualización integrada (Neo4j Browser)
  ✓ ACID completo
  ✓ Escalabilidad para miles de millones de nodos
  ✓ Algoritmos de grafos integrados (con GDS)

CUÁNDO USAR:
  → Redes sociales
  → Sistemas de recomendación
  → Detección de fraude
  → Knowledge graphs
  → Gestión de identidad y accesos
  → Network y IT operations

COMPARACIÓN CON SQL:

  SQL (JOIN pesado):
    SELECT amigo.nombre
    FROM personas p1
    JOIN amistades ON p1.id = amistades.persona_id
    JOIN personas amigo ON amistades.amigo_id = amigo.id
    WHERE p1.nombre = 'Juan'

  Neo4j (Natural):
    MATCH (p:Persona {nombre: 'Juan'})-[:AMIGO_DE]->(amigo)
    RETURN amigo.nombre

ACCESO:
  - Neo4j Browser: http://localhost:7474
  - Credenciales: neo4j / password
    """)


def main():
    """Ejecutar todos los ejemplos."""
    print("\n")
    print("█" * 60)
    print("█  NEO4J: BASE DE DATOS DE GRAFOS")
    print("█" * 60)

    # Verificar Neo4j
    if not verificar_neo4j():
        print("\n⚠ Neo4j no está disponible. Inicia Neo4j con:")
        print("  docker run --name neo4j -p 7687:7687 -p 7474:7474 \\")
        print("    -e NEO4J_AUTH=neo4j/password neo4j:latest")
        return

    # Ejecutar ejemplos
    ejemplo_1_crear_nodos()
    ejemplo_2_crear_relaciones()
    ejemplo_3_consultas_basicas()
    ejemplo_4_agregaciones()
    ejemplo_5_actualizacion_eliminacion()
    ejemplo_6_ventajas_neo4j()

    print("\n" + "="*60)
    print("✓ Todos los ejemplos completados")
    print("="*60)
    print("\nPróximos pasos:")
    print("  - Visita Neo4j Browser: http://localhost:7474")
    print("  - Experimenta con consultas Cypher")
    print("  - Explora la visualización del grafo")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
