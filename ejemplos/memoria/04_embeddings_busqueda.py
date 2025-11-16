"""
04_EMBEDDINGS_BUSQUEDA.PY
==========================

Ejemplo didáctico: Embeddings y Búsqueda Semántica

Demuestra:
- Convertir texto a embeddings (representación vectorial)
- Búsqueda semántica usando similitud de coseno
- Comparación con búsqueda por palabras clave
- Indexación simple de vectores

REQUISITOS PREVIOS:
- pip install sentence-transformers numpy scikit-learn
"""

import json
import math
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import numpy as np
from pathlib import Path


# ============================================================================
# SIMULACIÓN DE EMBEDDINGS (SIN DEPENDENCIAS EXTERNAS)
# ============================================================================

@dataclass
class Documento:
    """Representa un documento con su contenido y embedding"""
    id: str
    titulo: str
    contenido: str
    embedding: Optional[List[float]] = None
    tokens: List[str] = None

    def __post_init__(self):
        if self.tokens is None:
            # Tokenización simple
            self.tokens = self.contenido.lower().split()


class GeneradorEmbeddings:
    """
    Genera embeddings simples basados en frecuencia de términos.
    En producción, usarías sentence-transformers o OpenAI embeddings.

    Este es un ejemplo educativo que muestra el concepto.
    """

    def __init__(self, vocabulario: Optional[List[str]] = None):
        self.vocabulario = vocabulario or []
        self.dim = 100  # dimensión del embedding

    def construir_vocabulario(self, documentos: List[Documento]) -> None:
        """Construye vocabulario a partir de documentos"""
        todas_palabras = set()
        for doc in documentos:
            todas_palabras.update(doc.tokens)

        # Tomar las palabras más frecuentes
        frecuencia = {}
        for doc in documentos:
            for palabra in doc.tokens:
                frecuencia[palabra] = frecuencia.get(palabra, 0) + 1

        palabras_ordenadas = sorted(
            frecuencia.items(),
            key=lambda x: x[1],
            reverse=True
        )
        self.vocabulario = [p[0] for p in palabras_ordenadas[:self.dim]]

    def generar_embedding(self, texto: str) -> List[float]:
        """
        Genera embedding usando TF-IDF simplificado.
        En producción: usar sentence-transformers, OpenAI, etc.
        """
        tokens = texto.lower().split()

        # Contar frecuencias
        frecuencias = {}
        for token in tokens:
            frecuencias[token] = frecuencias.get(token, 0) + 1

        # Crear vector basado en vocabulario
        embedding = []
        for palabra_vocab in self.vocabulario:
            # TF: frecuencia de término normalizado
            tf = frecuencias.get(palabra_vocab, 0) / max(len(tokens), 1)
            embedding.append(tf)

        # Normalizar a magnitud 1
        magnitud = math.sqrt(sum(x**2 for x in embedding))
        if magnitud > 0:
            embedding = [x / magnitud for x in embedding]
        else:
            embedding = [0.0] * self.dim

        return embedding

    def generar_embeddings_batch(self, documentos: List[Documento]) -> None:
        """Genera embeddings para múltiples documentos"""
        for doc in documentos:
            doc.embedding = self.generar_embedding(
                f"{doc.titulo} {doc.contenido}"
            )


# ============================================================================
# BÚSQUEDA VECTORIAL
# ============================================================================

class CalculadorSimilitud:
    """Calcula similitud entre vectores"""

    @staticmethod
    def similitud_coseno(vec1: List[float], vec2: List[float]) -> float:
        """Calcula similitud coseno entre dos vectores (0.0 a 1.0)"""
        if not vec1 or not vec2:
            return 0.0

        # Producto punto
        producto_punto = sum(a * b for a, b in zip(vec1, vec2))

        # Magnitudes
        mag1 = math.sqrt(sum(x**2 for x in vec1))
        mag2 = math.sqrt(sum(x**2 for x in vec2))

        if mag1 == 0 or mag2 == 0:
            return 0.0

        return producto_punto / (mag1 * mag2)

    @staticmethod
    def distancia_euclidiana(vec1: List[float], vec2: List[float]) -> float:
        """Calcula distancia euclidiana"""
        return math.sqrt(sum((a - b)**2 for a, b in zip(vec1, vec2)))

    @staticmethod
    def similitud_jaccard(conj1: set, conj2: set) -> float:
        """Similitud Jaccard para conjuntos de palabras"""
        if not conj1 and not conj2:
            return 1.0

        interseccion = len(conj1 & conj2)
        union = len(conj1 | conj2)

        return interseccion / union if union > 0 else 0.0


# ============================================================================
# ÍNDICE VECTORIAL SIMPLE
# ============================================================================

class IndiceVectorial:
    """
    Índice simple de vectores con búsqueda por similitud.
    En producción: usar Pinecone, Weaviate, Chroma, etc.
    """

    def __init__(self):
        self.documentos: Dict[str, Documento] = {}
        self.embeddings: Dict[str, List[float]] = {}

    def agregar_documento(self, documento: Documento) -> None:
        """Agrega documento al índice"""
        if documento.embedding is None:
            raise ValueError(f"Documento {documento.id} sin embedding")

        self.documentos[documento.id] = documento
        self.embeddings[documento.id] = documento.embedding

    def agregar_documentos(self, documentos: List[Documento]) -> None:
        """Agrega múltiples documentos"""
        for doc in documentos:
            self.agregar_documento(doc)

    def buscar_por_similitud(
        self,
        query_embedding: List[float],
        k: int = 5,
        umbral_minimo: float = 0.0
    ) -> List[Tuple[Documento, float]]:
        """
        Busca documentos más similares a una query.
        Retorna lista de (documento, similitud) ordenada por similitud.
        """
        resultados = []

        for doc_id, doc_embedding in self.embeddings.items():
            similitud = CalculadorSimilitud.similitud_coseno(
                query_embedding,
                doc_embedding
            )

            if similitud >= umbral_minimo:
                resultados.append((self.documentos[doc_id], similitud))

        # Ordenar por similitud descendente
        resultados.sort(key=lambda x: x[1], reverse=True)

        return resultados[:k]

    def buscar(self, query: str, generador: GeneradorEmbeddings, k: int = 5) -> List[Dict]:
        """
        Búsqueda de alto nivel: texto -> embedding -> búsqueda
        """
        query_embedding = generador.generar_embedding(query)
        resultados = self.buscar_por_similitud(query_embedding, k=k)

        return [
            {
                "id": doc.id,
                "titulo": doc.titulo,
                "contenido": doc.contenido[:100] + "...",
                "similitud": round(sim, 3)
            }
            for doc, sim in resultados
        ]


# ============================================================================
# BÚSQUEDA HÍBRIDA (KEYWORD + VECTORIAL)
# ============================================================================

class BuscadorHibrido:
    """
    Combina búsqueda por palabras clave y búsqueda vectorial.
    Mejor cobertura: obtiene resultados exactos y semánticos.
    """

    def __init__(self, indice: IndiceVectorial, generador: GeneradorEmbeddings):
        self.indice = indice
        self.generador = generador

    def busqueda_palabras_clave(
        self,
        query: str,
        k: int = 5
    ) -> List[Tuple[str, float]]:
        """Búsqueda exacta por palabras clave"""
        palabras_query = set(query.lower().split())
        resultados = []

        for doc_id, doc in self.indice.documentos.items():
            palabras_doc = set(doc.tokens)
            similitud = CalculadorSimilitud.similitud_jaccard(
                palabras_query,
                palabras_doc
            )

            if similitud > 0:
                resultados.append((doc_id, similitud))

        resultados.sort(key=lambda x: x[1], reverse=True)
        return resultados[:k]

    def busqueda_semantica(
        self,
        query: str,
        k: int = 5
    ) -> List[Tuple[str, float]]:
        """Búsqueda semántica por embeddings"""
        query_embedding = self.generador.generar_embedding(query)
        resultados_obj = self.indice.buscar_por_similitud(query_embedding, k=k)
        return [(doc.id, sim) for doc, sim in resultados_obj]

    def busqueda_hibrida(
        self,
        query: str,
        k: int = 5,
        peso_keyword: float = 0.3,
        peso_semantica: float = 0.7
    ) -> List[Dict]:
        """
        Combina resultados de búsqueda por palabras clave y semántica.
        Retorna top-k resultados con score combinado.
        """
        resultados_keyword = self.busqueda_palabras_clave(query, k=k*2)
        resultados_semantica = self.busqueda_semantica(query, k=k*2)

        # Convertir a diccionarios indexados por doc_id
        scores = {}

        for doc_id, sim in resultados_keyword:
            scores[doc_id] = sim * peso_keyword

        for doc_id, sim in resultados_semantica:
            scores[doc_id] = scores.get(doc_id, 0) + sim * peso_semantica

        # Ordenar por score combinado
        resultados_ordenados = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            {
                "id": doc_id,
                "titulo": self.indice.documentos[doc_id].titulo,
                "contenido": self.indice.documentos[doc_id].contenido[:100] + "...",
                "score_combinado": round(score, 3)
            }
            for doc_id, score in resultados_ordenados[:k]
        ]


# ============================================================================
# DEMOSTRACIÓN
# ============================================================================

def demo_embeddings_busqueda():
    """Demuestra embeddings y búsqueda semántica"""

    print("=" * 80)
    print("DEMOSTRACIÓN: EMBEDDINGS Y BÚSQUEDA SEMÁNTICA")
    print("=" * 80)

    # Crear corpus de documentos
    documentos = [
        Documento(
            id="doc_1",
            titulo="Laptop gaming de alta performance",
            contenido="Laptop con GPU RTX 4090, procesador Intel i9, 32GB RAM, "
                     "pantalla 144Hz ideal para videojuegos y edición video"
        ),
        Documento(
            id="doc_2",
            titulo="MacBook Pro para desarrolladores",
            contenido="Computadora portátil Mac con chip M3 Max, perfecta para "
                     "desarrollo software, diseño gráfico y programación"
        ),
        Documento(
            id="doc_3",
            titulo="Tablet educativa para niños",
            contenido="Tablet de 10 pulgadas con apps educativas, batería larga, "
                     "pantalla IPS perfecta para enseñanza interactiva"
        ),
        Documento(
            id="doc_4",
            titulo="Monitor 4K ultra ancho",
            contenido="Monitor de 49 pulgadas con resolución 5120x1440, ideal para "
                     "trabajo creativo, trading y configuración multi-monitor"
        ),
        Documento(
            id="doc_5",
            titulo="Teclado mecánico gamer RGB",
            contenido="Teclado mecánico switches azules, iluminación RGB programable, "
                     "ideal para gaming competitivo y escritura profesional"
        ),
    ]

    print("\n1. PREPARACIÓN: GENERACIÓN DE EMBEDDINGS")
    print("-" * 80)

    generador = GeneradorEmbeddings()
    generador.construir_vocabulario(documentos)
    generador.generar_embeddings_batch(documentos)

    print(f"Vocabulario construido: {len(generador.vocabulario)} términos")
    print(f"Dimensión de embeddings: {generador.dim}")
    print(f"Documentos procesados: {len(documentos)}")

    # Crear índice
    indice = IndiceVectorial()
    indice.agregar_documentos(documentos)
    print(f"Documentos indexados: {len(indice.documentos)}")

    # Búsqueda semántica
    print("\n2. BÚSQUEDA SEMÁNTICA (EMBEDDINGS)")
    print("-" * 80)

    queries = [
        "laptop para programar",
        "pantalla de alta resolución",
        "dispositivo educativo",
    ]

    for query in queries:
        print(f"\nBúsqueda: '{query}'")
        resultados = indice.buscar(query, generador, k=3)
        for i, res in enumerate(resultados, 1):
            print(f"  {i}. {res['titulo']} (similitud: {res['similitud']})")

    # Búsqueda híbrida
    print("\n3. BÚSQUEDA HÍBRIDA (KEYWORDS + SEMÁNTICA)")
    print("-" * 80)

    buscador_hibrido = BuscadorHibrido(indice, generador)

    for query in ["gaming monitor RGB", "apple desarrollo", "educación niños"]:
        print(f"\nBúsqueda: '{query}'")

        # Solo keywords
        print("  - Búsqueda por palabras clave:")
        keyword_results = buscador_hibrido.busqueda_palabras_clave(query, k=2)
        for doc_id, sim in keyword_results:
            print(f"    {indice.documentos[doc_id].titulo} (Jaccard: {sim:.2f})")

        # Solo semántica
        print("  - Búsqueda semántica:")
        semantic_results = buscador_hibrido.busqueda_semantica(query, k=2)
        for doc_id, sim in semantic_results:
            print(f"    {indice.documentos[doc_id].titulo} (coseno: {sim:.2f})")

        # Híbrida
        print("  - Búsqueda híbrida (30% keyword, 70% semántica):")
        hybrid_results = buscador_hibrido.busqueda_hibrida(query, k=2)
        for res in hybrid_results:
            print(f"    {res['titulo']} (score: {res['score_combinado']})")

    # Comparación de similitud
    print("\n4. ANÁLISIS DE SIMILITUD ENTRE DOCUMENTOS")
    print("-" * 80)

    doc1 = documentos[0]  # laptop gaming
    doc2 = documentos[1]  # macbook

    similitud = CalculadorSimilitud.similitud_coseno(
        doc1.embedding,
        doc2.embedding
    )

    print(f"Similitud entre '{doc1.titulo}' y '{doc2.titulo}':")
    print(f"  Similitud coseno: {similitud:.3f}")
    print(f"  Interpretación: {'muy similar' if similitud > 0.7 else 'moderadamente similar' if similitud > 0.4 else 'poco similar'}")

    # Matriz de similitud
    print("\n5. MATRIZ DE SIMILITUD ENTRE DOCUMENTOS")
    print("-" * 80)

    print("  ", end="")
    for doc in documentos:
        print(f"{doc.id:8}", end="")
    print()

    for i, doc1 in enumerate(documentos):
        print(f"{doc1.id}: ", end="")
        for j, doc2 in enumerate(documentos):
            sim = CalculadorSimilitud.similitud_coseno(
                doc1.embedding,
                doc2.embedding
            )
            print(f"{sim:7.2f} ", end="")
        print()

    print("\n" + "=" * 80)
    print("Conclusión: Embeddings permiten búsqueda semántica más allá")
    print("de coincidencias exactas, combinables con búsqueda híbrida")
    print("=" * 80)


if __name__ == "__main__":
    demo_embeddings_busqueda()
