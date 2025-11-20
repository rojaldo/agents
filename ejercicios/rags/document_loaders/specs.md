# Ejemplos de docuement loaders para RAGS

A continuación se presentan algunos ejemplos de cómo utilizar diferentes document loaders por categorías, usando las librerías y técnicas más recomendadas para cada caso.

## Ejemplo para cargar documentos desde archivos de texto plano (.txt)

```python
from langchain.document_loaders import TextLoader

# Cargar un archivo de texto
loader = TextLoader("documento.txt", encoding="utf-8")
documents = loader.load()

for doc in documents:
    print(f"Contenido: {doc.page_content}")
    print(f"Metadata: {doc.metadata}")
```

**Usando DirectoryLoader para múltiples archivos:**

```python
from langchain.document_loaders import DirectoryLoader, TextLoader

# Cargar todos los archivos .txt de un directorio
loader = DirectoryLoader("./documentos", glob="**/*.txt", loader_cls=TextLoader)
documents = loader.load()

print(f"Total de documentos cargados: {len(documents)}")
```

## Ejemplo para cargar documentos desde archivos PDF (.pdf)

```python
from langchain.document_loaders import PyPDFLoader

# Cargar un archivo PDF
loader = PyPDFLoader("documento.pdf")
documents = loader.load()

for doc in documents:
    print(f"Página: {doc.metadata.get('page', 'N/A')}")
    print(f"Contenido: {doc.page_content[:100]}...")
```

**Usando PDFPlumberLoader para mayor precisión:**

```python
from langchain.document_loaders import PDFPlumberLoader

# Cargar PDF con mejor extracción de texto
loader = PDFPlumberLoader("documento.pdf")
documents = loader.load()

print(f"Total de páginas: {len(documents)}")
for doc in documents:
    print(f"Página {doc.metadata['page']}: {doc.page_content[:50]}...")
```

## Ejemplo para cargar documentos desde archivos Word (.docx)

```python
from langchain.document_loaders import Docx2txtLoader

# Cargar un archivo Word
loader = Docx2txtLoader("documento.docx")
documents = loader.load()

for doc in documents:
    print(f"Contenido: {doc.page_content}")
    print(f"Archivo: {doc.metadata.get('source', 'N/A')}")
```

**Alternativa con mejor preservación de formato:**

```python
from langchain.document_loaders import UnstructuredWordDocumentLoader

# Cargar con preservación de estructura
loader = UnstructuredWordDocumentLoader("documento.docx")
documents = loader.load()

print(f"Total de elementos extraídos: {len(documents)}")
```

## Ejemplo para cargar documentos desde páginas web (HTML)

```python
from langchain.document_loaders import UnstructuredHTMLLoader

# Cargar un archivo HTML local
loader = UnstructuredHTMLLoader("pagina.html")
documents = loader.load()

for doc in documents:
    print(f"Contenido: {doc.page_content[:100]}...")
```

**Cargar desde URL usando WebBaseLoader:**

```python
from langchain.document_loaders import WebBaseLoader

# Cargar página web desde URL
loader = WebBaseLoader("https://example.com")
documents = loader.load()

print(f"Total de documentos: {len(documents)}")
for doc in documents:
    print(f"Título: {doc.metadata.get('title', 'N/A')}")
    print(f"URL: {doc.metadata.get('source', 'N/A')}")
    print(f"Contenido: {doc.page_content[:50]}...")
```

**Cargar múltiples URLs:**

```python
from langchain.document_loaders import WebBaseLoader

urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3"
]

loader = WebBaseLoader(urls)
documents = loader.load()
```

## Ejemplo para cargar documentos desde bases de datos SQL

```python
from langchain.document_loaders import SQLDatabase
from langchain_community.document_loaders.sql import SQLDatabaseLoader
import sqlite3

# Conectar a base de datos SQLite
db = SQLDatabase.from_uri("sqlite:///base_datos.db")

# Crear loader
loader = SQLDatabaseLoader(db=db, query="SELECT * FROM usuarios LIMIT 10")
documents = loader.load()

for doc in documents:
    print(doc.page_content)
```

**Con PostgreSQL:**

```python
from langchain.document_loaders import SQLDatabase
from sqlalchemy import create_engine

# Conectar a PostgreSQL
engine = create_engine("postgresql://usuario:contraseña@localhost/base_datos")
db = SQLDatabase(engine)

# Consultar tabla específica
loader = SQLDatabaseLoader(
    db=db,
    query="SELECT id, titulo, contenido FROM articulos WHERE activo = true"
)
documents = loader.load()

print(f"Total de documentos: {len(documents)}")
```

**Con MySQL:**

```python
from langchain.document_loaders import SQLDatabase

# Conectar a MySQL
db = SQLDatabase.from_uri(
    "mysql+pymysql://usuario:contraseña@localhost/base_datos"
)

loader = SQLDatabaseLoader(db=db, query="SELECT * FROM documentos")
documents = loader.load()
```

## Ejemplo para cargar documentos desde APIs RESTful

```python
from langchain.document_loaders import GenericLoader
from langchain_community.document_loaders.generic import GenericLoader
import requests
from typing import Any, List

# Opción 1: Usando requests directamente
def cargar_api_rest(url: str, headers: dict = None) -> List[dict]:
    """Cargar datos desde API REST"""
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Ejemplo
api_url = "https://api.example.com/articulos"
headers = {"Authorization": "Bearer token_aqui"}
datos = cargar_api_rest(api_url, headers)

# Convertir a documentos
from langchain.schema import Document

documents = [
    Document(
        page_content=str(item),
        metadata={"source": "api", "id": item.get("id")}
    )
    for item in datos
]

for doc in documents:
    print(doc.page_content)
```

**Con paginación:**

```python
import requests
from langchain.schema import Document
from typing import List, Iterator

class APIDocumentLoader:
    def __init__(self, base_url: str, headers: dict = None):
        self.base_url = base_url
        self.headers = headers or {}

    def load(self, page_size: int = 10) -> Iterator[Document]:
        page = 1
        while True:
            response = requests.get(
                f"{self.base_url}?page={page}&limit={page_size}",
                headers=self.headers
            )
            data = response.json()

            if not data.get('items'):
                break

            for item in data['items']:
                yield Document(
                    page_content=str(item),
                    metadata={
                        "source": "api",
                        "id": item.get("id"),
                        "page": page
                    }
                )
            page += 1

# Uso
loader = APIDocumentLoader("https://api.example.com/articulos")
documents = list(loader.load())
```

## Ejemplo para cargar documentos desde archivos JSON (.json)

```python
import json
from langchain.schema import Document
from typing import List

# Cargar JSON simple
def cargar_json(ruta_archivo: str) -> List[Document]:
    """Cargar documentos desde archivo JSON"""
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        datos = json.load(f)

    documents = []
    if isinstance(datos, list):
        for item in datos:
            documents.append(Document(
                page_content=json.dumps(item),
                metadata={"source": "json", "type": "item"}
            ))
    else:
        documents.append(Document(
            page_content=json.dumps(datos),
            metadata={"source": "json"}
        ))

    return documents

# Uso
documentos = cargar_json("datos.json")
for doc in documentos:
    print(doc.page_content)
```

**JSON Lines (JSONL):**

```python
import json
from langchain.schema import Document
from typing import List

def cargar_jsonl(ruta_archivo: str) -> List[Document]:
    """Cargar documentos desde archivo JSONL"""
    documents = []
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        for linea in f:
            if linea.strip():
                item = json.loads(linea)
                documents.append(Document(
                    page_content=json.dumps(item),
                    metadata={
                        "source": "jsonl",
                        "id": item.get("id")
                    }
                ))
    return documents

# Uso
documentos = cargar_jsonl("datos.jsonl")
print(f"Total de documentos: {len(documentos)}")
```

**JSON con estructura anidada:**

```python
import json
from langchain.schema import Document

def cargar_json_anidado(ruta_archivo: str, clave_contenido: str) -> list:
    """Cargar JSON con estructura anidada"""
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        datos = json.load(f)

    documents = []

    # Si es un diccionario con items
    items = datos.get('items', datos.get('data', datos.get('records', [])))

    for item in items:
        contenido = item.get(clave_contenido, json.dumps(item))
        documents.append(Document(
            page_content=str(contenido),
            metadata={
                "source": "json",
                "id": item.get("id"),
                "titulo": item.get("titulo", "Sin título")
            }
        ))

    return documents

# Uso
documentos = cargar_json_anidado("datos.json", clave_contenido="descripcion")
```

## Ejemplo para cargar documentos desde archivos CSV (.csv)

```python
import csv
from langchain.schema import Document
from typing import List

# Cargar CSV simple
def cargar_csv(ruta_archivo: str, columna_contenido: str = None) -> List[Document]:
    """Cargar documentos desde archivo CSV"""
    documents = []

    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            # Usar una columna específica o todas las columnas
            if columna_contenido and columna_contenido in fila:
                contenido = fila[columna_contenido]
            else:
                contenido = str(fila)

            documents.append(Document(
                page_content=contenido,
                metadata={
                    "source": "csv",
                    "filename": ruta_archivo,
                    "id": fila.get("id", "unknown")
                }
            ))

    return documents

# Uso
documentos = cargar_csv("datos.csv", columna_contenido="descripcion")
for doc in documentos:
    print(f"ID: {doc.metadata['id']}")
    print(f"Contenido: {doc.page_content}")
```

**Usando pandas (más flexible):**

```python
import pandas as pd
from langchain.schema import Document
from typing import List

def cargar_csv_pandas(ruta_archivo: str, columna_contenido: str = None) -> List[Document]:
    """Cargar CSV usando pandas"""
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
                "filename": ruta_archivo
            }
        ))

    return documents

# Uso
documentos = cargar_csv_pandas("datos.csv")
print(f"Total de filas: {len(documentos)}")
```

**CSV con múltiples columnas como contenido:**

```python
import csv
from langchain.schema import Document

def cargar_csv_multicolumna(ruta_archivo: str, columnas_contenido: list) -> list:
    """Cargar CSV combinando múltiples columnas"""
    documents = []

    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            # Combinar múltiples columnas
            contenido = " | ".join(
                f"{col}: {fila.get(col, '')}" for col in columnas_contenido
            )

            documents.append(Document(
                page_content=contenido,
                metadata={
                    "source": "csv",
                    "id": fila.get("id"),
                    "titulo": fila.get("titulo", "Sin título")
                }
            ))

    return documents

# Uso
docs = cargar_csv_multicolumna(
    "datos.csv",
    columnas_contenido=["titulo", "descripcion", "categoria"]
)
```
