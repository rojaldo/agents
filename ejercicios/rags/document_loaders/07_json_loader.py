"""
Ejemplo de carga de documentos desde archivos JSON (.json)
"""

import json
from typing import List, Dict, Any
from langchain.schema import Document


def cargar_json_simple(ruta_archivo: str) -> List[Document]:
    """
    Cargar documentos desde un archivo JSON.

    Args:
        ruta_archivo: Ruta al archivo JSON

    Returns:
        Lista de documentos
    """
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        datos = json.load(f)

    documents = []

    if isinstance(datos, list):
        # Si es una lista, cada elemento es un documento
        for item in datos:
            documents.append(Document(
                page_content=json.dumps(item, ensure_ascii=False, indent=2),
                metadata={
                    "source": "json",
                    "type": "item",
                    "id": item.get("id") if isinstance(item, dict) else None
                }
            ))
    else:
        # Si es un objeto, todo el contenido es un documento
        documents.append(Document(
            page_content=json.dumps(datos, ensure_ascii=False, indent=2),
            metadata={"source": "json", "type": "object"}
        ))

    return documents


def cargar_jsonl(ruta_archivo: str) -> List[Document]:
    """
    Cargar documentos desde un archivo JSONL (JSON Lines).

    Cada línea contiene un objeto JSON.

    Args:
        ruta_archivo: Ruta al archivo JSONL

    Returns:
        Lista de documentos
    """
    documents = []

    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        for num_linea, linea in enumerate(f, 1):
            if linea.strip():
                try:
                    item = json.loads(linea)
                    documents.append(Document(
                        page_content=json.dumps(item, ensure_ascii=False),
                        metadata={
                            "source": "jsonl",
                            "line": num_linea,
                            "id": item.get("id") if isinstance(item, dict) else None
                        }
                    ))
                except json.JSONDecodeError as e:
                    print(f"Error en línea {num_linea}: {e}")

    return documents


def cargar_json_anidado(
    ruta_archivo: str,
    clave_contenido: str = None,
    clave_items: str = None
) -> List[Document]:
    """
    Cargar JSON con estructura anidada.

    Args:
        ruta_archivo: Ruta al archivo JSON
        clave_contenido: Clave que contiene el contenido principal
        clave_items: Clave que contiene la lista de items

    Returns:
        Lista de documentos
    """
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        datos = json.load(f)

    documents = []

    # Obtener items de varias formas posibles
    if clave_items:
        items = datos.get(clave_items, [])
    else:
        items = datos.get('items', datos.get('data', datos.get('records', [])))

    # Si items está vacío, asumir que datos es la lista
    if not items and isinstance(datos, list):
        items = datos

    for item in items:
        # Obtener contenido
        if clave_contenido and isinstance(item, dict) and clave_contenido in item:
            contenido = str(item[clave_contenido])
        else:
            contenido = json.dumps(item, ensure_ascii=False) if isinstance(item, dict) else str(item)

        # Crear documento
        documents.append(Document(
            page_content=contenido,
            metadata={
                "source": "json",
                "id": item.get("id") if isinstance(item, dict) else None,
                "titulo": item.get("titulo", item.get("title")) if isinstance(item, dict) else None
            }
        ))

    return documents


def extraer_campo(ruta_archivo: str, campo: str) -> List[str]:
    """
    Extraer un campo específico de todos los items en JSON.

    Args:
        ruta_archivo: Ruta al archivo JSON
        campo: Nombre del campo a extraer

    Returns:
        Lista de valores del campo
    """
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        datos = json.load(f)

    valores = []

    # Manejar lista o objeto
    items = datos if isinstance(datos, list) else datos.get('items', [datos])

    for item in items:
        if isinstance(item, dict) and campo in item:
            valores.append(item[campo])

    return valores


def fusionar_campos(
    ruta_archivo: str,
    campos: List[str],
    separador: str = " | "
) -> List[Document]:
    """
    Fusionar múltiples campos en un solo contenido.

    Args:
        ruta_archivo: Ruta al archivo JSON
        campos: Campos a fusionar
        separador: Separador entre campos

    Returns:
        Lista de documentos
    """
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        datos = json.load(f)

    documents = []
    items = datos if isinstance(datos, list) else datos.get('items', [datos])

    for item in items:
        if isinstance(item, dict):
            contenido = separador.join(
                f"{campo}: {item.get(campo, 'N/A')}"
                for campo in campos
            )

            documents.append(Document(
                page_content=contenido,
                metadata={
                    "source": "json",
                    "id": item.get("id")
                }
            ))

    return documents


if __name__ == "__main__":
    print("=" * 60)
    print("Ejemplo: Carga de archivos JSON (.json)")
    print("=" * 60)
    print()

    print("Funciones disponibles:")
    print("1. cargar_json_simple(ruta) - Carga JSON simple")
    print("2. cargar_jsonl(ruta) - Carga JSONL (JSON Lines)")
    print("3. cargar_json_anidado(ruta, clave_contenido) - Carga JSON anidado")
    print("4. extraer_campo(ruta, campo) - Extrae un campo específico")
    print("5. fusionar_campos(ruta, campos) - Fusiona múltiples campos")
    print()

    # Ejemplo 1: JSON simple (lista)
    print("Ejemplo 1: JSON con lista de objetos")
    print("-" * 60)

    try:
        # Crear archivo JSON de ejemplo
        json_path = "/tmp/datos.json"
        datos_json = [
            {
                "id": 1,
                "titulo": "Primer artículo",
                "contenido": "Este es el contenido del primer artículo"
            },
            {
                "id": 2,
                "titulo": "Segundo artículo",
                "contenido": "Este es el contenido del segundo artículo"
            }
        ]

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(datos_json, f, ensure_ascii=False, indent=2)

        # Cargar
        documentos = cargar_json_simple(json_path)
        print(f"Total de documentos: {len(documentos)}\n")

        for i, doc in enumerate(documentos, 1):
            print(f"Documento {i}:")
            print(f"  ID: {doc.metadata['id']}")
            print(f"  Contenido: {doc.page_content[:60]}...")
            print()

    except Exception as e:
        print(f"Error: {e}\n")

    # Ejemplo 2: JSONL
    print("Ejemplo 2: Archivo JSONL (JSON Lines)")
    print("-" * 60)

    try:
        # Crear archivo JSONL
        jsonl_path = "/tmp/datos.jsonl"
        with open(jsonl_path, 'w', encoding='utf-8') as f:
            f.write('{"id": 1, "mensaje": "Primera línea"}\n')
            f.write('{"id": 2, "mensaje": "Segunda línea"}\n')
            f.write('{"id": 3, "mensaje": "Tercera línea"}\n')

        # Cargar
        documentos = cargar_jsonl(jsonl_path)
        print(f"Total de documentos: {len(documentos)}\n")

        for doc in documentos:
            print(f"  Línea {doc.metadata['line']}: {doc.page_content}")

    except Exception as e:
        print(f"Error: {e}\n")

    # Ejemplo 3: JSON anidado
    print("\nEjemplo 3: JSON con estructura anidada")
    print("-" * 60)

    try:
        # Crear JSON anidado
        json_anidado_path = "/tmp/datos_anidados.json"
        datos_anidados = {
            "metadata": {
                "total": 2,
                "pagina": 1
            },
            "items": [
                {
                    "id": 1,
                    "titulo": "Producto A",
                    "descripcion": "Descripción del producto A",
                    "precio": 99.99
                },
                {
                    "id": 2,
                    "titulo": "Producto B",
                    "descripcion": "Descripción del producto B",
                    "precio": 149.99
                }
            ]
        }

        with open(json_anidado_path, 'w', encoding='utf-8') as f:
            json.dump(datos_anidados, f, ensure_ascii=False, indent=2)

        # Cargar especificando claves
        documentos = cargar_json_anidado(
            json_anidado_path,
            clave_contenido="descripcion",
            clave_items="items"
        )

        print(f"Total de documentos: {len(documentos)}\n")

        for doc in documentos:
            print(f"Contenido: {doc.page_content}")
            print(f"Metadata: {doc.metadata}\n")

    except Exception as e:
        print(f"Error: {e}\n")

    # Ejemplo 4: Fusionar campos
    print("Ejemplo 4: Fusionar múltiples campos")
    print("-" * 60)

    try:
        json_path = "/tmp/datos.json"

        documentos = fusionar_campos(
            json_path,
            campos=["id", "titulo"],
            separador=" -> "
        )

        print("Documentos con campos fusionados:\n")
        for doc in documentos:
            print(f"  {doc.page_content}")

    except Exception as e:
        print(f"Error: {e}")
