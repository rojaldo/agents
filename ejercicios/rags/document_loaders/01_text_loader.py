"""
Ejemplo de carga de documentos desde archivos de texto plano (.txt)
"""

from langchain.document_loaders import TextLoader, DirectoryLoader
from typing import List
from langchain.schema import Document


def cargar_archivo_texto(ruta_archivo: str) -> List[Document]:
    """
    Cargar un archivo de texto individual.

    Args:
        ruta_archivo: Ruta al archivo .txt a cargar

    Returns:
        Lista de documentos cargados
    """
    loader = TextLoader(ruta_archivo, encoding="utf-8")
    documents = loader.load()
    return documents


def cargar_directorio_texto(ruta_directorio: str, patron: str = "**/*.txt") -> List[Document]:
    """
    Cargar todos los archivos de texto de un directorio.

    Args:
        ruta_directorio: Ruta del directorio a cargar
        patron: Patrón glob para filtrar archivos (default: **/*.txt)

    Returns:
        Lista de documentos cargados
    """
    loader = DirectoryLoader(
        ruta_directorio,
        glob=patron,
        loader_cls=TextLoader
    )
    documents = loader.load()
    return documents


if __name__ == "__main__":
    # Ejemplo 1: Cargar un archivo individual
    print("=" * 60)
    print("Ejemplo 1: Cargar archivo de texto individual")
    print("=" * 60)

    try:
        # Crear archivo de ejemplo
        archivo_ejemplo = "/tmp/documento_ejemplo.txt"
        with open(archivo_ejemplo, "w", encoding="utf-8") as f:
            f.write("Este es un documento de ejemplo.\n")
            f.write("Contiene múltiples líneas de texto.\n")
            f.write("Es útil para probar document loaders.\n")

        # Cargar el archivo
        documentos = cargar_archivo_texto(archivo_ejemplo)
        print(f"Total de documentos cargados: {len(documentos)}\n")

        for i, doc in enumerate(documentos, 1):
            print(f"Documento {i}:")
            print(f"  Contenido: {doc.page_content[:100]}...")
            print(f"  Metadata: {doc.metadata}\n")

    except Exception as e:
        print(f"Error al cargar archivo: {e}\n")

    # Ejemplo 2: Cargar múltiples archivos de un directorio
    print("=" * 60)
    print("Ejemplo 2: Cargar múltiples archivos de un directorio")
    print("=" * 60)

    try:
        # Crear directorio con archivos de ejemplo
        import os
        import tempfile

        directorio_ejemplo = tempfile.mkdtemp()
        print(f"Directorio de ejemplo: {directorio_ejemplo}\n")

        # Crear múltiples archivos
        for i in range(3):
            archivo = os.path.join(directorio_ejemplo, f"documento_{i+1}.txt")
            with open(archivo, "w", encoding="utf-8") as f:
                f.write(f"Este es el documento número {i+1}.\n")
                f.write(f"Contiene información específica del documento {i+1}.\n")

        # Cargar todos los archivos
        documentos = cargar_directorio_texto(directorio_ejemplo)
        print(f"Total de documentos cargados: {len(documentos)}\n")

        for i, doc in enumerate(documentos, 1):
            print(f"Documento {i}:")
            print(f"  Archivo: {doc.metadata.get('source', 'N/A')}")
            print(f"  Contenido: {doc.page_content[:50]}...")
            print()

    except Exception as e:
        print(f"Error al cargar directorio: {e}\n")
