"""
MÓDULO 7: Ejemplo 1 - Conceptos Básicos de Grafos
===================================================

Objetivo: Entender estructuras de grafos sin BD externa

Este ejemplo muestra:
1. Creación de grafos con estructuras simples
2. Tipos de grafos (dirigidos, no dirigidos, ponderados)
3. Operaciones básicas (agregar nodos, relaciones, búsqueda)
4. Análisis simple de grafos
"""

class Nodo:
    """Representa un nodo en el grafo."""
    def __init__(self, id, propiedades=None):
        self.id = id
        self.propiedades = propiedades or {}

    def __repr__(self):
        return f"Nodo({self.id}, {self.propiedades})"


class Relacion:
    """Representa una relación entre nodos."""
    def __init__(self, tipo, origen, destino, propiedades=None):
        self.tipo = tipo
        self.origen = origen
        self.destino = destino
        self.propiedades = propiedades or {}
        self.peso = propiedades.get('peso', 1) if propiedades else 1

    def __repr__(self):
        return f"{self.origen.id}--[{self.tipo}]-->{self.destino.id}"


class GrafoDigido:
    """Grafo dirigido simple (las relaciones tienen dirección)."""
    def __init__(self):
        self.nodos = {}
        self.relaciones = []

    def agregar_nodo(self, id, propiedades=None):
        """Agregar un nodo al grafo."""
        if id not in self.nodos:
            self.nodos[id] = Nodo(id, propiedades)
        return self.nodos[id]

    def agregar_relacion(self, tipo, id_origen, id_destino, propiedades=None):
        """Agregar una relación dirigida A -> B."""
        if id_origen not in self.nodos or id_destino not in self.nodos:
            raise ValueError("Los nodos deben existir")

        relacion = Relacion(
            tipo,
            self.nodos[id_origen],
            self.nodos[id_destino],
            propiedades
        )
        self.relaciones.append(relacion)
        return relacion

    def obtener_vecinos_saliente(self, id_nodo):
        """Obtener nodos a los que apunta este nodo."""
        return [rel.destino for rel in self.relaciones if rel.origen.id == id_nodo]

    def obtener_vecinos_entrante(self, id_nodo):
        """Obtener nodos que apuntan a este nodo."""
        return [rel.origen for rel in self.relaciones if rel.destino.id == id_nodo]

    def centralidad_grado_saliente(self, id_nodo):
        """¿A cuántos nodos apunta?"""
        return len(self.obtener_vecinos_saliente(id_nodo))

    def centralidad_grado_entrante(self, id_nodo):
        """¿Cuántos nodos lo señalan?"""
        return len(self.obtener_vecinos_entrante(id_nodo))


class GrafoNoDirigido:
    """Grafo no dirigido simple (relaciones bidireccionales)."""
    def __init__(self):
        self.nodos = {}
        self.relaciones = []

    def agregar_nodo(self, id, propiedades=None):
        """Agregar un nodo."""
        if id not in self.nodos:
            self.nodos[id] = Nodo(id, propiedades)
        return self.nodos[id]

    def agregar_relacion(self, tipo, id_nodo1, id_nodo2, propiedades=None):
        """Agregar relación bidireccional."""
        if id_nodo1 not in self.nodos or id_nodo2 not in self.nodos:
            raise ValueError("Los nodos deben existir")

        rel1 = Relacion(tipo, self.nodos[id_nodo1], self.nodos[id_nodo2], propiedades)
        rel2 = Relacion(tipo, self.nodos[id_nodo2], self.nodos[id_nodo1], propiedades)

        self.relaciones.append(rel1)
        self.relaciones.append(rel2)

    def obtener_vecinos(self, id_nodo):
        """Obtener todos los nodos conectados."""
        vecinos = set()
        for rel in self.relaciones:
            if rel.origen.id == id_nodo:
                vecinos.add(rel.destino.id)
        return list(vecinos)

    def grado(self, id_nodo):
        """¿Cuántos nodos están conectados a este?"""
        return len(self.obtener_vecinos(id_nodo))


def ejemplo_1_grafo_red_social():
    """Crear un grafo dirigido de una red social."""
    print("\n" + "="*60)
    print("EJEMPLO 1: Red Social (Grafo Dirigido)")
    print("="*60)

    print("""
Concepto: En Twitter/X, cuando Juan SIGUE a María, no implica que
María lo siga. Las relaciones tienen DIRECCIÓN.

Estructura:
  Juan → María  (Juan sigue a María)
  María → Carlos
  Carlos → Juan
    """)

    grafo = GrafoDigido()

    # Crear nodos
    usuarios = {
        'juan': {'edad': 30},
        'maria': {'edad': 28},
        'carlos': {'edad': 35},
        'diana': {'edad': 26}
    }

    for usuario, props in usuarios.items():
        grafo.agregar_nodo(usuario, props)

    # Agregar relaciones (seguimientos)
    grafo.agregar_relacion('SIGUE', 'juan', 'maria')
    grafo.agregar_relacion('SIGUE', 'maria', 'carlos')
    grafo.agregar_relacion('SIGUE', 'carlos', 'juan')
    grafo.agregar_relacion('SIGUE', 'diana', 'juan')
    grafo.agregar_relacion('SIGUE', 'diana', 'maria')

    print("\nGrafo creado:")
    print(f"  Nodos: {len(grafo.nodos)}")
    print(f"  Relaciones: {len(grafo.relaciones)}")

    # Análisis
    print("\nAnálisis de Centralidad:")
    print("\nSaliente (¿A quién sigue?)")
    for usuario in usuarios.keys():
        vecinos = [v.id for v in grafo.obtener_vecinos_saliente(usuario)]
        print(f"  {usuario}: sigue a {vecinos}")

    print("\nEntrante (¿Quién lo sigue?)")
    for usuario in usuarios.keys():
        seguidores = [v.id for v in grafo.obtener_vecinos_entrante(usuario)]
        print(f"  {usuario}: seguido por {seguidores}")

    print("\nInfluencia (número de seguidores):")
    for usuario in usuarios.keys():
        influencia = grafo.centralidad_grado_entrante(usuario)
        print(f"  {usuario}: {influencia} seguidores")

    print("\nObservación:")
    print("  - Juan es el más influyente (3 seguidores)")
    print("  - Diana tiene audiencia pequeña (0 seguidores)")


def ejemplo_2_amistades_no_dirigidas():
    """Crear un grafo no dirigido de amistades."""
    print("\n" + "="*60)
    print("EJEMPLO 2: Amistades (Grafo No Dirigido)")
    print("="*60)

    print("""
Concepto: Si Juan es amigo de María, María es amigo de Juan.
No hay DIRECCIÓN en la relación.

Estructura:
  Juan ← → María
  María ← → Carlos
  Carlos ← → Juan
    """)

    grafo = GrafoNoDirigido()

    personas = ['juan', 'maria', 'carlos', 'diana', 'eva']
    for persona in personas:
        grafo.agregar_nodo(persona)

    # Amistades bidireccionales
    grafo.agregar_relacion('AMIGO', 'juan', 'maria')
    grafo.agregar_relacion('AMIGO', 'maria', 'carlos')
    grafo.agregar_relacion('AMIGO', 'carlos', 'juan')
    grafo.agregar_relacion('AMIGO', 'diana', 'eva')
    grafo.agregar_relacion('AMIGO', 'diana', 'juan')

    print("\nGrupo de amigos:")
    for persona in personas:
        amigos = grafo.obtener_vecinos(persona)
        grado = grafo.grado(persona)
        print(f"  {persona}: {amigos} (grado: {grado})")

    print("\nComunidades identificadas:")
    print("  - Comunidad 1: {Juan, María, Carlos, Diana} - todos conectados")
    print("  - Comunidad 2: {Eva} - conectada solo a Diana")


def ejemplo_3_grafo_ponderado():
    """Crear un grafo ponderado (ciudades con distancias)."""
    print("\n" + "="*60)
    print("EJEMPLO 3: Rutas Ponderadas (Grafo Ponderado)")
    print("="*60)

    print("""
Concepto: Las relaciones tienen PESO (distancia, costo, etc.)
Útil para: rutas óptimas, cálculo de caminos más cortos

Estructura:
  Madrid -- 400km --> Barcelona
  Madrid -- 500km --> Valencia
  Barcelona -- 350km --> Valencia
    """)

    grafo = GrafoNoDirigido()

    ciudades = ['madrid', 'barcelona', 'valencia', 'bilbao']
    for ciudad in ciudades:
        grafo.agregar_nodo(ciudad)

    # Rutas con distancia
    rutas = [
        ('madrid', 'barcelona', {'peso': 620, 'tiempo_h': 6}),
        ('madrid', 'valencia', {'peso': 360, 'tiempo_h': 3.5}),
        ('barcelona', 'valencia', {'peso': 350, 'tiempo_h': 3}),
        ('madrid', 'bilbao', {'peso': 400, 'tiempo_h': 4}),
    ]

    for c1, c2, props in rutas:
        grafo.agregar_relacion('CONECTA', c1, c2, props)

    print("\nRed de ciudades:")
    for rel in grafo.relaciones[:len(rutas)]:
        if rel.origen.id < rel.destino.id:  # Evitar duplicados
            distancia = rel.propiedades.get('peso', '?')
            tiempo = rel.propiedades.get('tiempo_h', '?')
            print(f"  {rel.origen.id} <--[{distancia}km, {tiempo}h]--> {rel.destino.id}")

    print("\nConexiones por ciudad:")
    for ciudad in ciudades:
        vecinos = grafo.obtener_vecinos(ciudad)
        if vecinos:
            print(f"  {ciudad}: conecta con {vecinos}")


def ejemplo_4_busqueda_dfs():
    """Búsqueda en profundidad (DFS) en un grafo."""
    print("\n" + "="*60)
    print("EJEMPLO 4: Búsqueda en Profundidad (DFS)")
    print("="*60)

    print("""
Concepto: Explorar el grafo siguiendo cada rama hasta el final
Útil para: encontrar caminos, ciclos, componentes conectadas

Algoritmo:
  1. Visitar nodo actual
  2. Para cada vecino no visitado:
     - Hacer DFS recursivamente
    """)

    grafo = GrafoDigido()

    # Crear árbol de contenidos
    grafo.agregar_nodo('Python')
    grafo.agregar_nodo('Conceptos')
    grafo.agregar_nodo('Variables')
    grafo.agregar_nodo('Tipos')
    grafo.agregar_nodo('Strings')
    grafo.agregar_nodo('Números')
    grafo.agregar_nodo('Listas')
    grafo.agregar_nodo('Operaciones')

    grafo.agregar_relacion('CONTIENE', 'Python', 'Conceptos')
    grafo.agregar_relacion('CONTIENE', 'Conceptos', 'Variables')
    grafo.agregar_relacion('CONTIENE', 'Conceptos', 'Tipos')
    grafo.agregar_relacion('CONTIENE', 'Tipos', 'Strings')
    grafo.agregar_relacion('CONTIENE', 'Tipos', 'Números')
    grafo.agregar_relacion('CONTIENE', 'Tipos', 'Listas')
    grafo.agregar_relacion('CONTIENE', 'Conceptos', 'Operaciones')

    def dfs(nodo_id, visitados=None, profundidad=0):
        """Búsqueda en profundidad."""
        if visitados is None:
            visitados = set()

        if nodo_id in visitados:
            return

        visitados.add(nodo_id)
        indentacion = "  " * profundidad
        print(f"{indentacion}├─ {nodo_id}")

        vecinos = [v.id for v in grafo.obtener_vecinos_saliente(nodo_id)]
        for vecino in vecinos:
            dfs(vecino, visitados, profundidad + 1)

    print("\nEstructura del curso (DFS):")
    dfs('Python')

    print("\nObservaciones:")
    print("  - Estructura jerárquica claraexploración profunda")
    print("  - Orden: Python → Conceptos → Variables → Tipos → ...")


def ejemplo_5_casos_uso():
    """Mostrar casos de uso de grafos."""
    print("\n" + "="*60)
    print("EJEMPLO 5: Casos de Uso de Grafos")
    print("="*60)

    casos = {
        "Redes Sociales": {
            "Nodos": ["Personas"],
            "Relaciones": ["AMIGO", "SIGUE", "MENCIONA"],
            "Preguntas": [
                "¿Amigos en común?",
                "¿Influenciadores?",
                "¿Comunidades?"
            ]
        },
        "Recomendaciones": {
            "Nodos": ["Usuarios", "Productos", "Categorías"],
            "Relaciones": ["COMPRO", "VISTO", "PERTENECE"],
            "Preguntas": [
                "¿Qué compraron usuarios similares?",
                "¿Productos relacionados?",
                "¿Tendencias de categorías?"
            ]
        },
        "Sistemas de Rutas": {
            "Nodos": ["Ciudades", "Estaciones"],
            "Relaciones": ["CONECTA", "DISTANCIA"],
            "Preguntas": [
                "¿Ruta más corta?",
                "¿Tiempo mínimo?",
                "¿Alternativas?"
            ]
        },
        "Control de Versiones": {
            "Nodos": ["Commits"],
            "Relaciones": ["PADRE_DE", "RAMA"],
            "Preguntas": [
                "¿Historia del código?",
                "¿Conflictos de merge?",
                "¿Cambios afectados?"
            ]
        },
    }

    for caso, detalles in casos.items():
        print(f"\n{caso}:")
        print(f"  Nodos: {detalles['Nodos']}")
        print(f"  Relaciones: {detalles['Relaciones']}")
        print(f"  Preguntas típicas:")
        for preg in detalles['Preguntas']:
            print(f"    - {preg}")


def main():
    """Ejecutar todos los ejemplos."""
    print("\n")
    print("█" * 60)
    print("█  CONCEPTOS BÁSICOS DE GRAFOS")
    print("█" * 60)

    ejemplo_1_grafo_red_social()
    ejemplo_2_amistades_no_dirigidas()
    ejemplo_3_grafo_ponderado()
    ejemplo_4_busqueda_dfs()
    ejemplo_5_casos_uso()

    print("\n" + "="*60)
    print("✓ Ejemplos completados")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
