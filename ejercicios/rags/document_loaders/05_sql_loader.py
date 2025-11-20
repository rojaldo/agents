"""
Ejemplo de carga de documentos desde bases de datos SQL
"""

from typing import List, Any
from langchain.schema import Document
import sqlite3

try:
    from langchain.document_loaders import SQLDatabase
    HAS_SQL_LOADER = True
except ImportError:
    HAS_SQL_LOADER = False


def crear_bd_ejemplo() -> str:
    """
    Crear una base de datos SQLite de ejemplo.

    Returns:
        Ruta de la base de datos creada
    """
    db_path = "/tmp/ejemplo.db"

    # Conectar y crear tabla
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Crear tabla
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL,
            descripcion TEXT
        )
    """)

    # Insertar datos de ejemplo
    usuarios = [
        (1, "Juan Pérez", "juan@example.com", "Desarrollador Python con 5 años de experiencia"),
        (2, "María García", "maria@example.com", "Ingeniera de datos especializada en ML"),
        (3, "Carlos López", "carlos@example.com", "DevOps engineer enfocado en infraestructura cloud"),
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO usuarios (id, nombre, email, descripcion) VALUES (?, ?, ?, ?)",
        usuarios
    )

    conn.commit()
    conn.close()

    return db_path


def cargar_desde_sqlite(db_path: str, query: str) -> List[Document]:
    """
    Cargar documentos desde una base de datos SQLite.

    Args:
        db_path: Ruta a la base de datos SQLite
        query: Consulta SQL a ejecutar

    Returns:
        Lista de documentos
    """
    # Conectar a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Ejecutar consulta
    cursor.execute(query)
    columnas = [description[0] for description in cursor.description]
    filas = cursor.fetchall()
    conn.close()

    # Convertir a documentos
    documents = []
    for fila in filas:
        # Crear diccionario de fila
        fila_dict = dict(zip(columnas, fila))

        # Crear contenido
        contenido = " | ".join(f"{k}: {v}" for k, v in fila_dict.items())

        documents.append(Document(
            page_content=contenido,
            metadata={
                "source": "sqlite",
                "database": db_path,
                "id": fila_dict.get("id")
            }
        ))

    return documents


def cargar_tabla_completa(db_path: str, tabla: str) -> List[Document]:
    """
    Cargar una tabla completa de SQLite.

    Args:
        db_path: Ruta a la base de datos
        tabla: Nombre de la tabla

    Returns:
        Lista de documentos
    """
    query = f"SELECT * FROM {tabla}"
    return cargar_desde_sqlite(db_path, query)


def cargar_con_filtro(db_path: str, tabla: str, condicion: str = None) -> List[Document]:
    """
    Cargar datos de una tabla con filtro opcional.

    Args:
        db_path: Ruta a la base de datos
        tabla: Nombre de la tabla
        condicion: Condición WHERE (opcional)

    Returns:
        Lista de documentos
    """
    if condicion:
        query = f"SELECT * FROM {tabla} WHERE {condicion}"
    else:
        query = f"SELECT * FROM {tabla}"

    return cargar_desde_sqlite(db_path, query)


if __name__ == "__main__":
    print("=" * 60)
    print("Ejemplo: Carga de bases de datos SQL")
    print("=" * 60)
    print()

    print("Funciones disponibles:")
    print("1. crear_bd_ejemplo() - Crea BD SQLite de ejemplo")
    print("2. cargar_desde_sqlite(db_path, query) - Carga con consulta SQL")
    print("3. cargar_tabla_completa(db_path, tabla) - Carga tabla completa")
    print("4. cargar_con_filtro(db_path, tabla, condicion) - Carga con filtro")
    print()

    # Ejemplo 1: Crear BD y cargar tabla completa
    print("Ejemplo 1: Crear BD de ejemplo y cargar tabla")
    print("-" * 60)

    try:
        # Crear BD de ejemplo
        db_path = crear_bd_ejemplo()
        print(f"Base de datos creada en: {db_path}\n")

        # Cargar tabla completa
        documentos = cargar_tabla_completa(db_path, "usuarios")
        print(f"Total de documentos cargados: {len(documentos)}\n")

        for i, doc in enumerate(documentos, 1):
            print(f"Documento {i}:")
            print(f"  Contenido: {doc.page_content}")
            print(f"  Metadata: {doc.metadata}\n")

    except Exception as e:
        print(f"Error: {e}\n")

    # Ejemplo 2: Cargar con filtro
    print("Ejemplo 2: Cargar con filtro")
    print("-" * 60)

    try:
        db_path = crear_bd_ejemplo()

        # Cargar con filtro
        documentos = cargar_con_filtro(
            db_path,
            "usuarios",
            condicion="id > 1"
        )

        print(f"Documentos con id > 1: {len(documentos)}\n")

        for doc in documentos:
            print(f"Contenido: {doc.page_content}")

    except Exception as e:
        print(f"Error: {e}\n")

    # Ejemplo 3: Consulta personalizada
    print("\nEjemplo 3: Consulta personalizada")
    print("-" * 60)

    try:
        db_path = crear_bd_ejemplo()

        # Consulta personalizada
        query = "SELECT nombre, email FROM usuarios WHERE id <= 2"
        documentos = cargar_desde_sqlite(db_path, query)

        print(f"Resultados de consulta personalizada: {len(documentos)}\n")

        for doc in documentos:
            print(f"Contenido: {doc.page_content}\n")

    except Exception as e:
        print(f"Error: {e}\n")

    print("Ejemplo para PostgreSQL:")
    print("-" * 60)
    print("""
from langchain.document_loaders import SQLDatabase
from sqlalchemy import create_engine

# Conectar a PostgreSQL
engine = create_engine("postgresql://usuario:contraseña@localhost/base_datos")
db = SQLDatabase(engine)

# Cargar con consulta
from langchain_community.document_loaders.sql import SQLDatabaseLoader
loader = SQLDatabaseLoader(
    db=db,
    query="SELECT * FROM articulos WHERE activo = true"
)
documents = loader.load()
    """)
