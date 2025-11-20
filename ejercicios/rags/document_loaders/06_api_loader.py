"""
Ejemplo de carga de documentos desde APIs RESTful
"""

from typing import List, Iterator, Optional, Dict, Any
from langchain.schema import Document
import json


class APIDocumentLoader:
    """
    Loader personalizado para cargar documentos desde APIs RESTful.
    """

    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None):
        """
        Inicializar el loader.

        Args:
            base_url: URL base de la API
            headers: Headers HTTP (opcional)
        """
        self.base_url = base_url
        self.headers = headers or {}

    def load(self, page_size: int = 10) -> Iterator[Document]:
        """
        Cargar documentos con paginación.

        Args:
            page_size: Tamaño de página

        Yields:
            Documentos cargados
        """
        try:
            import requests
        except ImportError:
            raise ImportError(
                "requests no está disponible. "
                "Instala con: pip install requests"
            )

        page = 1
        while True:
            try:
                response = requests.get(
                    f"{self.base_url}?page={page}&limit={page_size}",
                    headers=self.headers,
                    timeout=10
                )
                response.raise_for_status()
                data = response.json()

                # Asumir estructura {items: [...]}
                items = data.get('items', data.get('data', []))

                if not items:
                    break

                for item in items:
                    yield Document(
                        page_content=json.dumps(item, ensure_ascii=False),
                        metadata={
                            "source": "api",
                            "url": self.base_url,
                            "id": item.get("id"),
                            "page": page
                        }
                    )

                page += 1

            except Exception as e:
                print(f"Error al cargar página {page}: {e}")
                break


def cargar_api_simple(url: str, headers: Optional[Dict[str, str]] = None) -> List[Document]:
    """
    Cargar documentos desde una API simple (sin paginación).

    Args:
        url: URL de la API
        headers: Headers HTTP (opcional)

    Returns:
        Lista de documentos
    """
    try:
        import requests
    except ImportError:
        raise ImportError(
            "requests no está disponible. "
            "Instala con: pip install requests"
        )

    response = requests.get(url, headers=headers or {}, timeout=10)
    response.raise_for_status()
    data = response.json()

    documents = []

    # Manejar respuesta como lista
    if isinstance(data, list):
        items = data
    else:
        # Manejar respuesta como objeto con items
        items = data.get('items', data.get('data', [data]))

    for item in items:
        documents.append(Document(
            page_content=json.dumps(item, ensure_ascii=False),
            metadata={
                "source": "api",
                "url": url,
                "id": item.get("id") if isinstance(item, dict) else None
            }
        ))

    return documents


def cargar_api_con_autenticacion(
    url: str,
    token: str,
    token_type: str = "Bearer"
) -> List[Document]:
    """
    Cargar documentos desde una API con autenticación.

    Args:
        url: URL de la API
        token: Token de autenticación
        token_type: Tipo de token (default: Bearer)

    Returns:
        Lista de documentos
    """
    headers = {
        "Authorization": f"{token_type} {token}",
        "Content-Type": "application/json"
    }
    return cargar_api_simple(url, headers)


def transformar_items_api(items: List[Dict[str, Any]], campos: List[str]) -> str:
    """
    Transformar items de API extrayendo campos específicos.

    Args:
        items: Lista de items de la API
        campos: Campos a extraer

    Returns:
        Texto formateado
    """
    resultado = []

    for item in items:
        linea = " | ".join(
            f"{campo}: {item.get(campo, 'N/A')}" for campo in campos
        )
        resultado.append(linea)

    return "\n".join(resultado)


if __name__ == "__main__":
    print("=" * 60)
    print("Ejemplo: Carga de documentos desde APIs RESTful")
    print("=" * 60)
    print()

    print("Clases y funciones disponibles:")
    print("1. APIDocumentLoader - Loader con paginación")
    print("2. cargar_api_simple(url) - Carga simple sin paginación")
    print("3. cargar_api_con_autenticacion(url, token) - Carga con token")
    print("4. transformar_items_api(items, campos) - Transforma datos")
    print()

    # Ejemplo 1: Mock de API con JSONPlaceholder
    print("Ejemplo 1: Cargar desde API pública (JSONPlaceholder)")
    print("-" * 60)

    try:
        import requests

        # Usar API pública para demostración
        url = "https://jsonplaceholder.typicode.com/posts?_limit=3"

        print(f"Cargando desde: {url}\n")

        documentos = cargar_api_simple(url)
        print(f"Total de documentos cargados: {len(documentos)}\n")

        for i, doc in enumerate(documentos[:2], 1):
            contenido = json.loads(doc.page_content)
            print(f"Documento {i}:")
            print(f"  ID: {doc.metadata['id']}")
            print(f"  Título: {contenido.get('title', 'N/A')}")
            print(f"  URL: {doc.metadata['url']}\n")

    except Exception as e:
        print(f"Error (verifica tu conexión): {e}\n")

    # Ejemplo 2: APIDocumentLoader con paginación
    print("Ejemplo 2: Loader con paginación")
    print("-" * 60)

    print("""
# Uso con paginación personalizada
loader = APIDocumentLoader(
    base_url="https://api.example.com/articulos",
    headers={"Authorization": "Bearer tu_token"}
)

# Cargar con página size de 20
for document in loader.load(page_size=20):
    print(f"ID: {document.metadata['id']}")
    print(f"Página: {document.metadata['page']}")
    print(f"Contenido: {document.page_content[:100]}...")
    """)

    # Ejemplo 3: Autenticación
    print("\nEjemplo 3: Con token de autenticación")
    print("-" * 60)

    print("""
# Cargar con autenticación Bearer
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

documentos = cargar_api_con_autenticacion(
    url="https://api.example.com/datos",
    token=token,
    token_type="Bearer"
)

for doc in documentos:
    print(doc.page_content)
    """)

    # Ejemplo 4: Transformar datos
    print("\nEjemplo 4: Transformar datos de API")
    print("-" * 60)

    try:
        import requests

        response = requests.get("https://jsonplaceholder.typicode.com/users?_limit=2")
        usuarios = response.json()

        # Transformar extrayendo campos específicos
        texto = transformar_items_api(
            usuarios,
            campos=["id", "name", "email"]
        )

        print("Datos transformados:")
        print(texto)

    except Exception as e:
        print(f"Error: {e}")
