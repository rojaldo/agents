"""
Ejemplo de carga de documentos desde archivos CSV (.csv)
"""

import csv
from typing import List, Optional
from langchain.schema import Document

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


def cargar_csv_simple(
    ruta_archivo: str,
    columna_contenido: Optional[str] = None,
    delimitador: str = ","
) -> List[Document]:
    """
    Cargar documentos desde un archivo CSV usando csv module.

    Args:
        ruta_archivo: Ruta al archivo CSV
        columna_contenido: Columna a usar como contenido (opcional)
        delimitador: Delimitador del CSV (default: ",")

    Returns:
        Lista de documentos
    """
    documents = []

    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        lector = csv.DictReader(f, delimiter=delimitador)

        for num_fila, fila in enumerate(lector, 1):
            # Usar columna específica o todas las columnas
            if columna_contenido and columna_contenido in fila:
                contenido = fila[columna_contenido]
            else:
                contenido = " | ".join(f"{k}: {v}" for k, v in fila.items())

            documents.append(Document(
                page_content=contenido,
                metadata={
                    "source": "csv",
                    "filename": ruta_archivo,
                    "row": num_fila,
                    "id": fila.get("id", f"row_{num_fila}")
                }
            ))

    return documents


def cargar_csv_pandas(
    ruta_archivo: str,
    columna_contenido: Optional[str] = None
) -> List[Document]:
    """
    Cargar documentos desde un archivo CSV usando pandas.

    Args:
        ruta_archivo: Ruta al archivo CSV
        columna_contenido: Columna a usar como contenido (opcional)

    Returns:
        Lista de documentos
    """
    if not HAS_PANDAS:
        raise ImportError(
            "pandas no está disponible. "
            "Instala con: pip install pandas"
        )

    df = pd.read_csv(ruta_archivo)
    documents = []

    for idx, fila in df.iterrows():
        if columna_contenido and columna_contenido in fila.index:
            contenido = str(fila[columna_contenido])
        else:
            contenido = fila.to_string()

        documents.append(Document(
            page_content=contenido,
            metadata={
                "source": "csv",
                "row": idx,
                "filename": ruta_archivo,
                "id": fila.get("id") if "id" in fila.index else idx
            }
        ))

    return documents


def cargar_csv_multicolumna(
    ruta_archivo: str,
    columnas_contenido: List[str],
    separador: str = " | "
) -> List[Document]:
    """
    Cargar CSV combinando múltiples columnas como contenido.

    Args:
        ruta_archivo: Ruta al archivo CSV
        columnas_contenido: Columnas a combinar
        separador: Separador entre columnas

    Returns:
        Lista de documentos
    """
    documents = []

    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        lector = csv.DictReader(f)

        for num_fila, fila in enumerate(lector, 1):
            # Combinar columnas especificadas
            contenido = separador.join(
                f"{col}: {fila.get(col, 'N/A')}" for col in columnas_contenido
                if col in fila
            )

            documents.append(Document(
                page_content=contenido,
                metadata={
                    "source": "csv",
                    "row": num_fila,
                    "id": fila.get("id", f"row_{num_fila}")
                }
            ))

    return documents


def cargar_csv_filtrado(
    ruta_archivo: str,
    columna_filtro: str,
    valor_filtro: str,
    columna_contenido: Optional[str] = None
) -> List[Document]:
    """
    Cargar CSV filtrando por una columna específica.

    Args:
        ruta_archivo: Ruta al archivo CSV
        columna_filtro: Columna para filtrar
        valor_filtro: Valor a buscar
        columna_contenido: Columna a usar como contenido

    Returns:
        Lista de documentos
    """
    documents = []

    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        lector = csv.DictReader(f)

        for num_fila, fila in enumerate(lector, 1):
            # Filtrar
            if columna_filtro not in fila or fila[columna_filtro] != valor_filtro:
                continue

            # Contenido
            if columna_contenido and columna_contenido in fila:
                contenido = fila[columna_contenido]
            else:
                contenido = " | ".join(f"{k}: {v}" for k, v in fila.items())

            documents.append(Document(
                page_content=contenido,
                metadata={
                    "source": "csv",
                    "row": num_fila,
                    "id": fila.get("id"),
                    "filtro": f"{columna_filtro}={valor_filtro}"
                }
            ))

    return documents


if __name__ == "__main__":
    print("=" * 60)
    print("Ejemplo: Carga de archivos CSV (.csv)")
    print("=" * 60)
    print()

    print("Funciones disponibles:")
    print("1. cargar_csv_simple(ruta, columna) - Carga simple")
    print("2. cargar_csv_pandas(ruta, columna) - Carga con pandas")
    print("3. cargar_csv_multicolumna(ruta, columnas) - Fusiona columnas")
    print("4. cargar_csv_filtrado(ruta, col, val) - Carga con filtro")
    print()

    # Ejemplo 1: CSV simple
    print("Ejemplo 1: Carga simple de CSV")
    print("-" * 60)

    try:
        # Crear archivo CSV de ejemplo
        csv_path = "/tmp/datos.csv"
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["id", "nombre", "email", "ciudad"])
            writer.writeheader()
            writer.writerows([
                {"id": "1", "nombre": "Juan", "email": "juan@example.com", "ciudad": "Madrid"},
                {"id": "2", "nombre": "María", "email": "maria@example.com", "ciudad": "Barcelona"},
                {"id": "3", "nombre": "Carlos", "email": "carlos@example.com", "ciudad": "Valencia"},
            ])

        # Cargar
        documentos = cargar_csv_simple(csv_path)
        print(f"Total de documentos: {len(documentos)}\n")

        for i, doc in enumerate(documentos[:2], 1):
            print(f"Documento {i}:")
            print(f"  Row: {doc.metadata['row']}")
            print(f"  Contenido: {doc.page_content[:50]}...")
            print()

    except Exception as e:
        print(f"Error: {e}\n")

    # Ejemplo 2: CSV con columna específica
    print("Ejemplo 2: Usar columna específica como contenido")
    print("-" * 60)

    try:
        csv_path = "/tmp/datos.csv"

        documentos = cargar_csv_simple(csv_path, columna_contenido="nombre")
        print(f"Documentos usando columna 'nombre':\n")

        for doc in documentos:
            print(f"  {doc.page_content}")

    except Exception as e:
        print(f"Error: {e}\n")

    # Ejemplo 3: CSV con pandas
    print("Ejemplo 3: Cargar con pandas")
    print("-" * 60)

    if HAS_PANDAS:
        try:
            csv_path = "/tmp/datos.csv"

            documentos = cargar_csv_pandas(csv_path, columna_contenido="email")
            print(f"Total de documentos: {len(documentos)}\n")

            print("Primeros 2 documentos:")
            for doc in documentos[:2]:
                print(f"  {doc.page_content}")

        except Exception as e:
            print(f"Error: {e}")
    else:
        print("pandas no está instalado")
        print("Instala con: pip install pandas\n")

    # Ejemplo 4: Fusionar columnas
    print("\nEjemplo 4: Fusionar múltiples columnas")
    print("-" * 60)

    try:
        csv_path = "/tmp/datos.csv"

        documentos = cargar_csv_multicolumna(
            csv_path,
            columnas_contenido=["nombre", "ciudad"],
            separador=" -> "
        )

        print("Documentos con columnas fusionadas:\n")

        for doc in documentos:
            print(f"  {doc.page_content}")

    except Exception as e:
        print(f"Error: {e}\n")

    # Ejemplo 5: CSV filtrado
    print("\nEjemplo 5: Cargar con filtro")
    print("-" * 60)

    try:
        csv_path = "/tmp/datos.csv"

        documentos = cargar_csv_filtrado(
            csv_path,
            columna_filtro="ciudad",
            valor_filtro="Madrid",
            columna_contenido="nombre"
        )

        print(f"Personas de Madrid: {len(documentos)}\n")

        for doc in documentos:
            print(f"  {doc.page_content}")
            print(f"  Metadata: {doc.metadata}")

    except Exception as e:
        print(f"Error: {e}")
