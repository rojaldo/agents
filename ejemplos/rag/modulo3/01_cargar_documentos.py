"""
MÓDULO 3.1: Cargar Documentos
Ejemplos de cómo cargar diferentes tipos de documentos para RAG
"""

from pathlib import Path
import json

# ============================================================================
# CREAR DOCUMENTOS DE PRUEBA
# ============================================================================

def crear_documentos_ejemplo():
    """Crear archivos de ejemplo para trabajar con RAG"""

    ejemplos_dir = Path("documentos_ejemplo")
    ejemplos_dir.mkdir(exist_ok=True)

    # 1. Crear archivo de texto
    documento_texto = """
    # Guía de RAG (Retrieval-Augmented Generation)

    ## ¿Qué es RAG?

    RAG es una técnica que combina búsqueda de información con generación de texto.
    Permite que los modelos de lenguaje accedan a información externa relevante
    antes de generar una respuesta.

    ## Ventajas de RAG

    1. Precisión mejorada: Las respuestas se basan en datos reales
    2. Información actualizada: Acceso a datos recientes
    3. Datos privados: Información corporativa no se expone
    4. Trazabilidad: Se pueden citar las fuentes

    ## Arquitectura

    El flujo típico es:
    1. Cargar documento
    2. Dividir en chunks
    3. Crear embeddings
    4. Almacenar en vector DB
    5. Recuperar documentos relevantes
    6. Generar respuesta con contexto
    """

    with open(ejemplos_dir / "rag_guide.txt", "w", encoding="utf-8") as f:
        f.write(documento_texto)

    # 2. Crear archivo JSON con documentos estructurados
    documentos_json = [
        {
            "titulo": "Python Basics",
            "contenido": "Python es un lenguaje de programación versátil. Fue creado por Guido van Rossum en 1989. Se conoce por su sintaxis simple y legible.",
            "categoria": "programacion"
        },
        {
            "titulo": "Machine Learning Intro",
            "contenido": "El aprendizaje automático es un subcampo de la inteligencia artificial. Los algoritmos de ML aprenden de los datos sin ser explícitamente programados.",
            "categoria": "ia"
        },
        {
            "titulo": "RAG Systems",
            "contenido": "Los sistemas RAG combinan recuperación de documentos con generación de texto. Son útiles para QA sobre bases de conocimiento específicas.",
            "categoria": "nlp"
        }
    ]

    with open(ejemplos_dir / "documentos.json", "w", encoding="utf-8") as f:
        json.dump(documentos_json, f, ensure_ascii=False, indent=2)

    print(f"✓ Documentos de ejemplo creados en: {ejemplos_dir}/")
    return ejemplos_dir


# ============================================================================
# CARGAR DOCUMENTOS
# ============================================================================

def cargar_documento_texto(ruta):
    """Cargar un documento de texto simple"""
    print(f"\n📄 Cargando documento de texto: {ruta}")

    with open(ruta, "r", encoding="utf-8") as f:
        contenido = f.read()

    return {
        "fuente": str(ruta),
        "tipo": "texto",
        "contenido": contenido,
        "longitud": len(contenido)
    }


def cargar_documento_json(ruta):
    """Cargar documentos desde JSON"""
    print(f"\n📄 Cargando documentos JSON: {ruta}")

    with open(ruta, "r", encoding="utf-8") as f:
        documentos = json.load(f)

    docs_procesados = []
    for doc in documentos:
        docs_procesados.append({
            "titulo": doc.get("titulo", ""),
            "contenido": doc.get("contenido", ""),
            "categoria": doc.get("categoria", ""),
            "fuente": str(ruta),
            "tipo": "json"
        })

    return docs_procesados


def cargar_multiples_documentos(directorio):
    """Cargar todos los documentos de un directorio"""
    print(f"\n📁 Cargando documentos desde: {directorio}")

    directorio = Path(directorio)
    todos_los_docs = []

    # Cargar archivos TXT
    for archivo_txt in directorio.glob("*.txt"):
        doc = cargar_documento_texto(archivo_txt)
        todos_los_docs.append(doc)

    # Cargar archivos JSON
    for archivo_json in directorio.glob("*.json"):
        docs = cargar_documento_json(archivo_json)
        todos_los_docs.extend(docs)

    return todos_los_docs


# ============================================================================
# PROCESAR Y MOSTRAR DOCUMENTOS
# ============================================================================

def procesar_documentos(documentos):
    """Procesar y preparar documentos para chunking"""
    print(f"\n⚙️ Procesando {len(documentos)} documentos...")

    documentos_procesados = []

    for doc in documentos:
        doc_proc = {
            "fuente": doc.get("fuente", ""),
            "tipo": doc.get("tipo", ""),
            "titulo": doc.get("titulo", ""),
            "contenido": doc.get("contenido", ""),
            "longitud_caracteres": len(doc.get("contenido", "")),
            "numero_palabras": len(doc.get("contenido", "").split()),
            "numero_lineas": len(doc.get("contenido", "").split("\n"))
        }
        documentos_procesados.append(doc_proc)

        print(f"  ✓ {doc_proc['titulo'] or doc_proc['fuente']}")
        print(f"    - {doc_proc['numero_palabras']} palabras")
        print(f"    - {doc_proc['longitud_caracteres']} caracteres")

    return documentos_procesados


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("MÓDULO 3.1: Cargar Documentos para RAG")
    print("=" * 70)

    # Crear documentos de ejemplo
    directorio_docs = crear_documentos_ejemplo()

    # Cargar los documentos
    documentos = cargar_multiples_documentos(directorio_docs)

    # Procesar documentos
    docs_procesados = procesar_documentos(documentos)

    # Resumen
    print("\n" + "=" * 70)
    print("RESUMEN")
    print("=" * 70)
    print(f"Total de documentos cargados: {len(docs_procesados)}")
    print(f"Palabras totales: {sum(d['numero_palabras'] for d in docs_procesados)}")
    print(f"Caracteres totales: {sum(d['longitud_caracteres'] for d in docs_procesados)}")
    print("\n✅ Documentos cargados exitosamente")
