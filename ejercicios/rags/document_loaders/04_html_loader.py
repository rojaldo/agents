"""
Ejemplo de carga de documentos desde páginas web (HTML)
"""

from typing import List, Union
from langchain.schema import Document

try:
    from langchain.document_loaders import UnstructuredHTMLLoader
    HAS_UNSTRUCTURED_HTML = True
except ImportError:
    HAS_UNSTRUCTURED_HTML = False

try:
    from langchain.document_loaders import WebBaseLoader
    HAS_WEB_LOADER = True
except ImportError:
    HAS_WEB_LOADER = False


def cargar_html_local(ruta_archivo: str) -> List[Document]:
    """
    Cargar un archivo HTML local.

    Args:
        ruta_archivo: Ruta al archivo HTML

    Returns:
        Lista de documentos cargados
    """
    if not HAS_UNSTRUCTURED_HTML:
        raise ImportError(
            "UnstructuredHTMLLoader no está disponible. "
            "Instala con: pip install unstructured[html]"
        )

    loader = UnstructuredHTMLLoader(ruta_archivo)
    documents = loader.load()
    return documents


def cargar_url(url: str) -> List[Document]:
    """
    Cargar una página web desde URL.

    Args:
        url: URL de la página web a cargar

    Returns:
        Lista de documentos cargados
    """
    if not HAS_WEB_LOADER:
        raise ImportError(
            "WebBaseLoader no está disponible. "
            "Instala con: pip install langchain-community"
        )

    loader = WebBaseLoader(url)
    documents = loader.load()
    return documents


def cargar_urls_multiples(urls: List[str]) -> List[Document]:
    """
    Cargar múltiples páginas web desde URLs.

    Args:
        urls: Lista de URLs a cargar

    Returns:
        Lista de documentos cargados de todas las URLs
    """
    if not HAS_WEB_LOADER:
        raise ImportError(
            "WebBaseLoader no está disponible. "
            "Instala con: pip install langchain-community"
        )

    loader = WebBaseLoader(urls)
    documents = loader.load()
    return documents


def extraer_metadatos(documents: List[Document]) -> dict:
    """
    Extraer metadatos de los documentos cargados.

    Args:
        documents: Lista de documentos

    Returns:
        Diccionario con información de metadatos
    """
    info = {
        "total_documentos": len(documents),
        "fuentes": set(),
        "titulos": set(),
        "metadatos_completos": []
    }

    for doc in documents:
        metadata = doc.metadata
        info["metadatos_completos"].append(metadata)

        if "source" in metadata:
            info["fuentes"].add(metadata["source"])
        if "title" in metadata:
            info["titulos"].add(metadata["title"])

    return {
        "total_documentos": info["total_documentos"],
        "fuentes": list(info["fuentes"]),
        "titulos": list(info["titulos"]),
        "metadatos_completos": info["metadatos_completos"]
    }


if __name__ == "__main__":
    print("=" * 60)
    print("Ejemplo: Carga de páginas web (HTML)")
    print("=" * 60)
    print()

    print("Funciones disponibles:")
    print("1. cargar_html_local(ruta) - Carga archivo HTML local")
    print("2. cargar_url(url) - Carga página web desde URL")
    print("3. cargar_urls_multiples(urls) - Carga múltiples URLs")
    print("4. extraer_metadatos(documents) - Extrae información de metadatos")
    print()

    # Ejemplo 1: Crear y cargar archivo HTML local
    print("Ejemplo 1: Cargar archivo HTML local")
    print("-" * 60)

    try:
        # Crear archivo HTML de ejemplo
        html_ejemplo = "/tmp/pagina_ejemplo.html"
        with open(html_ejemplo, "w", encoding="utf-8") as f:
            f.write("""
            <html>
                <head>
                    <title>Página de Ejemplo</title>
                </head>
                <body>
                    <h1>Bienvenido</h1>
                    <p>Este es un archivo HTML de ejemplo.</p>
                    <p>Contiene múltiples párrafos de texto.</p>
                </body>
            </html>
            """)

        # Cargar el archivo
        if HAS_UNSTRUCTURED_HTML:
            documentos = cargar_html_local(html_ejemplo)
            print(f"Total de documentos cargados: {len(documentos)}\n")
            for doc in documentos:
                print(f"Contenido: {doc.page_content[:100]}...")
                print(f"Metadata: {doc.metadata}\n")
        else:
            print("UnstructuredHTMLLoader no disponible")

    except Exception as e:
        print(f"Error: {e}\n")

    # Ejemplo 2: Cargar desde URL (requiere conexión a internet)
    print("\nEjemplo 2: Cargar página web desde URL")
    print("-" * 60)

    if HAS_WEB_LOADER:
        print("Para cargar desde URL, usa:")
        print()
        print("from langchain.document_loaders import WebBaseLoader")
        print()
        print("# URL individual")
        print("loader = WebBaseLoader('https://example.com')")
        print("documents = loader.load()")
        print()
        print("# Múltiples URLs")
        print("urls = [")
        print("    'https://example.com/page1',")
        print("    'https://example.com/page2',")
        print("]")
        print("loader = WebBaseLoader(urls)")
        print("documents = loader.load()")
    else:
        print("WebBaseLoader no disponible")

    print()
    print("Ejemplo de estructura de documento:")
    print()
    print("Document {")
    print("    page_content: 'Contenido de la página...',")
    print("    metadata: {")
    print("        'source': 'https://example.com',")
    print("        'title': 'Título de la página'")
    print("    }")
    print("}")
