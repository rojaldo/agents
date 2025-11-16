"""
MÓDULO 3.2: Chunking - Dividir documentos en fragmentos
Técnicas para particionar documentos de forma óptima para RAG
"""

from typing import List
import json

# ============================================================================
# ESTRATEGIAS DE CHUNKING
# ============================================================================

class DocumentChunker:
    """Clase para dividir documentos en chunks optimizados"""

    @staticmethod
    def chunk_por_tamaño(texto: str, tamaño: int = 500, solapamiento: int = 50) -> List[str]:
        """
        Dividir documento por tamaño de caracteres con solapamiento

        Args:
            texto: Documento a dividir
            tamaño: Tamaño máximo del chunk en caracteres
            solapamiento: Caracteres que se repiten entre chunks

        Returns:
            Lista de chunks
        """
        chunks = []
        inicio = 0

        while inicio < len(texto):
            fin = inicio + tamaño
            chunk = texto[inicio:fin]
            chunks.append(chunk.strip())

            # Avanzar con solapamiento
            inicio = fin - solapamiento

        return [c for c in chunks if c]  # Eliminar chunks vacíos

    @staticmethod
    def chunk_por_párrafos(texto: str, min_chars: int = 100) -> List[str]:
        """
        Dividir documento respetando párrafos

        Args:
            texto: Documento a dividir
            min_chars: Mínimo de caracteres para mantener un párrafo

        Returns:
            Lista de chunks basados en párrafos
        """
        párrafos = texto.split("\n\n")
        chunks = []

        chunk_actual = ""
        for párrafo in párrafos:
            párrafo = párrafo.strip()
            if not párrafo:
                continue

            if len(chunk_actual) + len(párrafo) < 1000:
                chunk_actual += "\n\n" + párrafo if chunk_actual else párrafo
            else:
                if chunk_actual:
                    chunks.append(chunk_actual)
                chunk_actual = párrafo

        if chunk_actual:
            chunks.append(chunk_actual)

        return chunks

    @staticmethod
    def chunk_por_oraciones(texto: str) -> List[str]:
        """
        Dividir documento por oraciones

        Args:
            texto: Documento a dividir

        Returns:
            Lista de chunks basados en oraciones
        """
        # Separadores de oraciones
        separadores = [". ", "! ", "? ", "\n"]

        oraciones = [texto]
        for separador in separadores:
            nuevas_oraciones = []
            for oración in oraciones:
                partes = oración.split(separador)
                for i, parte in enumerate(partes[:-1]):
                    nuevas_oraciones.append(parte + separador.strip())
                nuevas_oraciones.append(partes[-1])
            oraciones = [o.strip() for o in nuevas_oraciones if o.strip()]

        # Agrupar oraciones pequeñas
        chunks = []
        chunk_actual = ""
        for oración in oraciones:
            if len(chunk_actual) + len(oración) < 500:
                chunk_actual += " " + oración if chunk_actual else oración
            else:
                if chunk_actual:
                    chunks.append(chunk_actual)
                chunk_actual = oración

        if chunk_actual:
            chunks.append(chunk_actual)

        return chunks


# ============================================================================
# DEMOSTRACIÓN
# ============================================================================

def demostrar_chunking():
    """Demostración de diferentes estrategias de chunking"""

    # Documento de prueba
    documento = """
    La Inteligencia Artificial (IA) es el campo de estudio que se ocupa de crear máquinas inteligentes.
    Estas máquinas pueden realizar tareas que normalmente requieren inteligencia humana.

    Existen varios tipos de IA:

    1. IA Débil (Narrow AI): Diseñada para tareas específicas.
    2. IA Fuerte (General AI): Tendría inteligencia general como los humanos.
    3. IA Super: Hipotética IA que superaría la inteligencia humana.

    El aprendizaje automático es un subcampo de la IA. Los modelos de ML aprenden
    patrones de los datos sin ser explícitamente programados.

    El aprendizaje profundo utiliza redes neuronales con múltiples capas.
    Ha revolucionado campos como la visión por computadora y el procesamiento del lenguaje natural.

    RAG combina recuperación de documentos con generación de texto. Es especialmente útil
    para sistemas que necesitan acceder a información actualizada o específica del dominio.
    """

    print("=" * 70)
    print("MÓDULO 3.2: Chunking de Documentos")
    print("=" * 70)

    chunker = DocumentChunker()

    # ========================================================================
    # 1. CHUNKING POR TAMAÑO
    # ========================================================================
    print("\n1️⃣ CHUNKING POR TAMAÑO (500 caracteres, 50 solapamiento)")
    print("-" * 70)

    chunks_tamaño = chunker.chunk_por_tamaño(documento, tamaño=500, solapamiento=50)
    print(f"Total de chunks: {len(chunks_tamaño)}")

    for i, chunk in enumerate(chunks_tamaño, 1):
        preview = chunk[:60].replace("\n", " ") + "..."
        print(f"  Chunk {i}: ({len(chunk)} chars) {preview}")

    # ========================================================================
    # 2. CHUNKING POR PÁRRAFOS
    # ========================================================================
    print("\n2️⃣ CHUNKING POR PÁRRAFOS")
    print("-" * 70)

    chunks_párrafos = chunker.chunk_por_párrafos(documento)
    print(f"Total de chunks: {len(chunks_párrafos)}")

    for i, chunk in enumerate(chunks_párrafos, 1):
        preview = chunk[:60].replace("\n", " ") + "..."
        palabras = len(chunk.split())
        print(f"  Chunk {i}: ({palabras} palabras) {preview}")

    # ========================================================================
    # 3. CHUNKING POR ORACIONES
    # ========================================================================
    print("\n3️⃣ CHUNKING POR ORACIONES")
    print("-" * 70)

    chunks_oraciones = chunker.chunk_por_oraciones(documento)
    print(f"Total de chunks: {len(chunks_oraciones)}")

    for i, chunk in enumerate(chunks_oraciones, 1):
        preview = chunk[:60].replace("\n", " ") + "..."
        palabras = len(chunk.split())
        print(f"  Chunk {i}: ({palabras} palabras) {preview}")

    # ========================================================================
    # 4. ANÁLISIS COMPARATIVO
    # ========================================================================
    print("\n" + "=" * 70)
    print("ANÁLISIS COMPARATIVO")
    print("=" * 70)

    resultados = {
        "Por Tamaño": {
            "chunks": len(chunks_tamaño),
            "promedio_chars": sum(len(c) for c in chunks_tamaño) / len(chunks_tamaño),
            "ventajas": "Mejor control sobre el tamaño",
            "desventajas": "Puede cortar contenido importante"
        },
        "Por Párrafos": {
            "chunks": len(chunks_párrafos),
            "promedio_chars": sum(len(c) for c in chunks_párrafos) / len(chunks_párrafos),
            "ventajas": "Respeta estructura del documento",
            "desventajas": "Chunks de tamaño variable"
        },
        "Por Oraciones": {
            "chunks": len(chunks_oraciones),
            "promedio_chars": sum(len(c) for c in chunks_oraciones) / len(chunks_oraciones),
            "ventajas": "Mantiene coherencia semántica",
            "desventajas": "Más chunks, mayor procesamiento"
        }
    }

    for estrategia, stats in resultados.items():
        print(f"\n{estrategia}:")
        print(f"  - Total chunks: {stats['chunks']}")
        print(f"  - Promedio chars/chunk: {stats['promedio_chars']:.0f}")
        print(f"  - Ventajas: {stats['ventajas']}")
        print(f"  - Desventajas: {stats['desventajas']}")

    # ========================================================================
    # 5. GUARDAR CHUNKS
    # ========================================================================
    print("\n" + "=" * 70)
    print("GUARDANDO CHUNKS PARA PROCESAMIENTO")
    print("=" * 70)

    chunks_json = {
        "estrategia": "párrafos",
        "total_chunks": len(chunks_párrafos),
        "chunks": [
            {
                "id": i,
                "contenido": chunk,
                "longitud_caracteres": len(chunk),
                "numero_palabras": len(chunk.split())
            }
            for i, chunk in enumerate(chunks_párrafos, 1)
        ]
    }

    with open("chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks_json, f, ensure_ascii=False, indent=2)

    print(f"✓ {len(chunks_párrafos)} chunks guardados en chunks.json")
    print("\n✅ Chunking completado exitosamente")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    demostrar_chunking()
