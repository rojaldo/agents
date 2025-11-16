"""
MÓDULO 4: Embeddings
Convertir texto en vectores numéricos para búsqueda semántica
"""

import json
from typing import List

# ============================================================================
# SIMULACIÓN DE EMBEDDINGS (sin LangChain)
# ============================================================================

class SimpleEmbedding:
    """Simulación simple de embeddings usando técnicas básicas"""

    @staticmethod
    def crear_embedding_tf(texto: str, dimensión: int = 50) -> List[float]:
        """
        Crear embedding usando Term Frequency
        (simplificado para fines educativos)
        """
        palabras = texto.lower().split()
        vector = [0.0] * dimensión

        # Asignar valores basados en frecuencia de palabras
        freq_palabras = {}
        for palabra in palabras:
            freq_palabras[palabra] = freq_palabras.get(palabra, 0) + 1

        # Mapear a dimensiones
        for i, (palabra, freq) in enumerate(freq_palabras.items()):
            idx = hash(palabra) % dimensión
            vector[idx] += freq / len(palabras)

        # Normalizar
        norma = sum(v * v for v in vector) ** 0.5
        if norma > 0:
            vector = [v / norma for v in vector]

        return vector

    @staticmethod
    def similitud_coseno(v1: List[float], v2: List[float]) -> float:
        """Calcular similitud coseno entre dos vectores"""
        producto_punto = sum(a * b for a, b in zip(v1, v2))
        norma_v1 = sum(a * a for a in v1) ** 0.5
        norma_v2 = sum(b * b for b in v2) ** 0.5

        if norma_v1 == 0 or norma_v2 == 0:
            return 0.0

        return producto_punto / (norma_v1 * norma_v2)


# ============================================================================
# DEMOSTRACIÓN CON LANGCHAIN Y OLLAMA
# ============================================================================

def demostrar_embeddings():
    """Demostración de embeddings para RAG"""

    print("=" * 70)
    print("MÓDULO 4: Embeddings")
    print("=" * 70)

    # Textos de ejemplo
    documentos = [
        "Python es un lenguaje de programación poderoso y versátil",
        "El aprendizaje automático utiliza algoritmos para aprender de datos",
        "RAG combina búsqueda con generación de texto inteligente",
        "Los embeddings convierten texto en vectores numéricos",
        "La similitud coseno mide la similitud entre dos vectores"
    ]

    pregunta = "¿Cómo funcionan los embeddings?"

    print("\n📝 DOCUMENTOS DISPONIBLES:")
    print("-" * 70)
    for i, doc in enumerate(documentos, 1):
        print(f"{i}. {doc}")

    print(f"\n❓ PREGUNTA: {pregunta}")

    # ========================================================================
    # CREAR EMBEDDINGS (SIMULADO)
    # ========================================================================
    print("\n" + "=" * 70)
    print("CREANDO EMBEDDINGS")
    print("=" * 70)

    embedding_generator = SimpleEmbedding()

    # Generar embeddings para documentos
    embeddings_docs = []
    for i, doc in enumerate(documentos):
        embedding = embedding_generator.crear_embedding_tf(doc)
        embeddings_docs.append({
            "id": i,
            "texto": doc,
            "embedding": embedding,
            "dimensión": len(embedding)
        })
        print(f"✓ Embedding {i + 1} creado (dimensión: {len(embedding)})")

    # Generar embedding para la pregunta
    embedding_pregunta = embedding_generator.crear_embedding_tf(pregunta)
    print(f"✓ Embedding de pregunta creado (dimensión: {len(embedding_pregunta)})")

    # ========================================================================
    # BÚSQUEDA SEMÁNTICA
    # ========================================================================
    print("\n" + "=" * 70)
    print("BÚSQUEDA SEMÁNTICA - Encontrar documentos relevantes")
    print("=" * 70)

    similitudes = []
    for doc_data in embeddings_docs:
        similitud = embedding_generator.similitud_coseno(
            embedding_pregunta,
            doc_data["embedding"]
        )
        similitudes.append({
            "documento": doc_data["texto"],
            "similitud": similitud
        })

    # Ordenar por similitud
    similitudes.sort(key=lambda x: x["similitud"], reverse=True)

    print(f"\nDocumentos ordenados por similitud a: '{pregunta}'")
    print("-" * 70)
    for i, item in enumerate(similitudes, 1):
        barra = "█" * int(item["similitud"] * 20)
        print(f"{i}. [{item['similitud']:.3f}] {barra}")
        print(f"   {item['documento']}")

    # ========================================================================
    # INFORMACIÓN TÉCNICA
    # ========================================================================
    print("\n" + "=" * 70)
    print("INFORMACIÓN TÉCNICA")
    print("=" * 70)

    info = {
        "Tipo de embedding": "Term Frequency (simplificado)",
        "Dimensión": len(embedding_pregunta),
        "Similitud máxima": max(s["similitud"] for s in similitudes),
        "Similitud mínima": min(s["similitud"] for s in similitudes),
        "Documentos procesados": len(documentos),
        "Método de búsqueda": "Similitud Coseno"
    }

    for clave, valor in info.items():
        print(f"  • {clave}: {valor}")

    # ========================================================================
    # CÓMO USAR CON OLLAMA EN PRODUCCIÓN
    # ========================================================================
    print("\n" + "=" * 70)
    print("USANDO EMBEDDINGS REALES CON OLLAMA")
    print("=" * 70)

    codigo_ejemplo = '''
# Con LangChain y Ollama
from langchain_ollama import OllamaEmbeddings

# Crear embeddings con Ollama
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Crear embedding de un texto
vector = embeddings.embed_query("RAG es increíble")
print(f"Dimensión del vector: {len(vector)}")

# Crear embeddings de múltiples documentos
doc_vectors = embeddings.embed_documents([
    "Texto 1",
    "Texto 2",
    "Texto 3"
])
    '''

    print("\nCódigo Python para usar embeddings reales:")
    print("-" * 70)
    print(codigo_ejemplo)

    # ========================================================================
    # GUARDAR RESULTADOS
    # ========================================================================
    resultados = {
        "embeddings": [
            {
                "id": e["id"],
                "texto": e["texto"],
                "dimensión": e["dimensión"],
                "embedding_preview": e["embedding"][:5]  # Primeros 5 valores
            }
            for e in embeddings_docs
        ],
        "búsqueda": {
            "pregunta": pregunta,
            "resultados": similitudes[:3]  # Top 3
        }
    }

    with open("embeddings_result.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)

    print("\n✓ Resultados guardados en embeddings_result.json")
    print("✅ Embeddings demostrados exitosamente")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    demostrar_embeddings()
