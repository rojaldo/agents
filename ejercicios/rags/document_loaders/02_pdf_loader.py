"""
Ejemplo de carga de documentos desde archivos PDF (.pdf)
"""

from langchain.document_loaders import PyPDFLoader
from typing import List
from langchain.schema import Document

try:
    from langchain.document_loaders import PDFPlumberLoader
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False


def cargar_pdf_pypdf(ruta_archivo: str) -> List[Document]:
    """
    Cargar un archivo PDF usando PyPDFLoader.

    Args:
        ruta_archivo: Ruta al archivo PDF

    Returns:
        Lista de documentos (uno por página)
    """
    loader = PyPDFLoader(ruta_archivo)
    documents = loader.load()
    return documents


def cargar_pdf_plumber(ruta_archivo: str) -> List[Document]:
    """
    Cargar un archivo PDF usando PDFPlumberLoader (mayor precisión).

    Args:
        ruta_archivo: Ruta al archivo PDF

    Returns:
        Lista de documentos (uno por página)

    Nota:
        Requiere instalar: pip install pdfplumber
    """
    if not HAS_PDFPLUMBER:
        raise ImportError(
            "PDFPlumberLoader no está disponible. "
            "Instala con: pip install pdfplumber"
        )

    loader = PDFPlumberLoader(ruta_archivo)
    documents = loader.load()
    return documents


def extraer_info_pdf(documents: List[Document]) -> dict:
    """
    Extraer información útil de los documentos PDF.

    Args:
        documents: Lista de documentos cargados

    Returns:
        Diccionario con información del PDF
    """
    info = {
        "total_paginas": len(documents),
        "metadatas": [],
        "contenido_resumen": []
    }

    for doc in documents:
        info["metadatas"].append(doc.metadata)
        # Guardar primeros 100 caracteres de cada página
        info["contenido_resumen"].append(doc.page_content[:100])

    return info


if __name__ == "__main__":
    # Nota: Este ejemplo requiere un archivo PDF real para funcionar
    # Se proporciona la estructura y funciones para usar con archivos PDF

    print("=" * 60)
    print("Ejemplo: Carga de archivos PDF")
    print("=" * 60)
    print()

    print("Funciones disponibles:")
    print("1. cargar_pdf_pypdf(ruta_archivo) - Carga PDF con PyPDFLoader")
    print("2. cargar_pdf_plumber(ruta_archivo) - Carga PDF con PDFPlumberLoader")
    print("3. extraer_info_pdf(documents) - Extrae información del PDF")
    print()

    # Ejemplo de uso (descomentar si tienes un PDF)
    """
    # Cargar un PDF
    ruta_pdf = "documento.pdf"

    try:
        documentos = cargar_pdf_pypdf(ruta_pdf)
        print(f"Total de páginas: {len(documentos)}")

        # Mostrar información
        for i, doc in enumerate(documentos, 1):
            print(f"\\nPágina {i}:")
            print(f"  Metadata: {doc.metadata}")
            print(f"  Contenido (primeros 100 caracteres):")
            print(f"  {doc.page_content[:100]}...")

    except FileNotFoundError:
        print(f"Error: El archivo {ruta_pdf} no fue encontrado")

    # Alternativa con PDFPlumber
    try:
        documentos = cargar_pdf_plumber(ruta_pdf)
        info = extraer_info_pdf(documentos)
        print(f"\\nTotal de páginas (PDFPlumber): {info['total_paginas']}")

    except ImportError as e:
        print(f"Error: {e}")
    """

    # Demostración de estructura
    print("Ejemplo de estructura de un documento cargado desde PDF:")
    print()
    print("Document {")
    print("    page_content: 'Texto extraído del PDF...',")
    print("    metadata: {")
    print("        'source': 'documento.pdf',")
    print("        'page': 0")
    print("    }")
    print("}")
