"""
Ejemplo 3: Servidor MCP con RAG usando LangChain y Ollama

Este ejemplo demuestra cómo crear un servidor MCP que implementa
Retrieval Augmented Generation (RAG) usando LangChain, Ollama
y embeddings locales.
"""

import json
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate


class ServidorMCPRAG:
    """
    Servidor MCP que implementa RAG para consultas sobre documentos.
    """

    def __init__(
        self,
        modelo_llm: str = "llama3.2",
        modelo_embeddings: str = "nomic-embed-text"
    ):
        """
        Inicializa el servidor MCP con capacidades RAG.

        Args:
            modelo_llm: Modelo de Ollama para generación de texto
            modelo_embeddings: Modelo de Ollama para embeddings
        """
        self.nombre = "Servidor MCP RAG"
        self.version = "1.0.0"
        self.modelo_llm = modelo_llm
        self.modelo_embeddings = modelo_embeddings

        # Inicializar LLM y embeddings
        print(f"🔧 Inicializando LLM con modelo: {modelo_llm}")
        self.llm = OllamaLLM(model=modelo_llm, temperature=0.3)

        print(f"🔧 Inicializando embeddings con modelo: {modelo_embeddings}")
        self.embeddings = OllamaEmbeddings(model=modelo_embeddings)

        # Inicializar text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len
        )

        # Almacenar vectorstores por colección
        self.vectorstores: Dict[str, FAISS] = {}

        # Registrar herramientas
        self.herramientas = {
            "crear_coleccion": self.crear_coleccion,
            "agregar_documentos": self.agregar_documentos,
            "consultar": self.consultar,
            "buscar_similar": self.buscar_similar,
            "listar_colecciones": self.listar_colecciones
        }

        self.historial = []
        print(f"✓ Servidor MCP RAG inicializado")

    def crear_coleccion(self, nombre: str, descripcion: str = "") -> Dict[str, Any]:
        """
        Crea una nueva colección de documentos.

        Args:
            nombre: Nombre de la colección
            descripcion: Descripción opcional de la colección

        Returns:
            Información sobre la colección creada
        """
        try:
            if nombre in self.vectorstores:
                return {
                    "error": f"La colección '{nombre}' ya existe",
                    "exito": False
                }

            # Crear vectorstore vacío con documento dummy
            doc_inicial = Document(
                page_content="Colección inicializada",
                metadata={"tipo": "sistema"}
            )

            self.vectorstores[nombre] = FAISS.from_documents(
                [doc_inicial],
                self.embeddings
            )

            resultado = {
                "exito": True,
                "nombre": nombre,
                "descripcion": descripcion,
                "timestamp": datetime.now().isoformat()
            }

            self._registrar_operacion("crear_coleccion", nombre, resultado)
            return resultado

        except Exception as e:
            return {"error": str(e), "exito": False}

    def agregar_documentos(
        self,
        coleccion: str,
        textos: List[str],
        metadatos: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Agrega documentos a una colección existente.

        Args:
            coleccion: Nombre de la colección
            textos: Lista de textos a agregar
            metadatos: Lista opcional de metadatos para cada documento

        Returns:
            Información sobre los documentos agregados
        """
        try:
            if coleccion not in self.vectorstores:
                return {
                    "error": f"La colección '{coleccion}' no existe",
                    "exito": False
                }

            # Preparar documentos
            documentos = []
            for i, texto in enumerate(textos):
                # Dividir texto en chunks
                chunks = self.text_splitter.split_text(texto)

                for chunk in chunks:
                    metadata = metadatos[i] if metadatos and i < len(metadatos) else {}
                    metadata["chunk_index"] = len(documentos)
                    metadata["timestamp"] = datetime.now().isoformat()

                    doc = Document(
                        page_content=chunk,
                        metadata=metadata
                    )
                    documentos.append(doc)

            # Agregar a vectorstore
            self.vectorstores[coleccion].add_documents(documentos)

            resultado = {
                "exito": True,
                "coleccion": coleccion,
                "documentos_agregados": len(textos),
                "chunks_creados": len(documentos),
                "timestamp": datetime.now().isoformat()
            }

            self._registrar_operacion("agregar_documentos", coleccion, resultado)
            return resultado

        except Exception as e:
            return {"error": str(e), "exito": False}

    def consultar(
        self,
        coleccion: str,
        pregunta: str,
        k: int = 3
    ) -> Dict[str, Any]:
        """
        Realiza una consulta RAG sobre una colección.

        Args:
            coleccion: Nombre de la colección
            pregunta: Pregunta a responder
            k: Número de documentos relevantes a recuperar

        Returns:
            Respuesta generada y documentos fuente
        """
        try:
            if coleccion not in self.vectorstores:
                return {
                    "error": f"La colección '{coleccion}' no existe",
                    "exito": False
                }

            # Crear prompt personalizado
            prompt_template = """Usa el siguiente contexto para responder la pregunta de manera clara y concisa.
Si no puedes responder basándote en el contexto, indícalo.

Contexto: {context}

Pregunta: {question}

Respuesta:"""

            PROMPT = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
            )

            # Crear chain de QA
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vectorstores[coleccion].as_retriever(
                    search_kwargs={"k": k}
                ),
                return_source_documents=True,
                chain_type_kwargs={"prompt": PROMPT}
            )

            # Ejecutar consulta
            resultado_qa = qa_chain.invoke({"query": pregunta})

            # Preparar respuesta
            documentos_fuente = [
                {
                    "contenido": doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in resultado_qa["source_documents"]
            ]

            resultado = {
                "exito": True,
                "pregunta": pregunta,
                "respuesta": resultado_qa["result"],
                "documentos_fuente": documentos_fuente,
                "num_documentos_usados": len(documentos_fuente),
                "timestamp": datetime.now().isoformat()
            }

            self._registrar_operacion("consultar", pregunta, resultado)
            return resultado

        except Exception as e:
            return {"error": str(e), "exito": False}

    def buscar_similar(
        self,
        coleccion: str,
        texto: str,
        k: int = 5
    ) -> Dict[str, Any]:
        """
        Busca documentos similares en una colección.

        Args:
            coleccion: Nombre de la colección
            texto: Texto de búsqueda
            k: Número de resultados a retornar

        Returns:
            Documentos similares encontrados
        """
        try:
            if coleccion not in self.vectorstores:
                return {
                    "error": f"La colección '{coleccion}' no existe",
                    "exito": False
                }

            # Realizar búsqueda de similitud
            documentos = self.vectorstores[coleccion].similarity_search(
                texto,
                k=k
            )

            resultados = [
                {
                    "contenido": doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in documentos
            ]

            resultado = {
                "exito": True,
                "texto_busqueda": texto,
                "resultados": resultados,
                "num_resultados": len(resultados),
                "timestamp": datetime.now().isoformat()
            }

            self._registrar_operacion("buscar_similar", texto, resultado)
            return resultado

        except Exception as e:
            return {"error": str(e), "exito": False}

    def listar_colecciones(self) -> Dict[str, Any]:
        """
        Lista todas las colecciones disponibles.

        Returns:
            Información sobre las colecciones
        """
        colecciones = []

        for nombre, vectorstore in self.vectorstores.items():
            # Obtener número aproximado de documentos
            try:
                # FAISS no tiene método directo para contar documentos
                # pero podemos obtener el índice
                num_docs = vectorstore.index.ntotal
            except:
                num_docs = "desconocido"

            colecciones.append({
                "nombre": nombre,
                "num_documentos": num_docs
            })

        resultado = {
            "exito": True,
            "colecciones": colecciones,
            "total": len(colecciones),
            "timestamp": datetime.now().isoformat()
        }

        return resultado

    def _registrar_operacion(self, herramienta: str, entrada: str, salida: Any):
        """Registra una operación en el historial."""
        self.historial.append({
            "herramienta": herramienta,
            "entrada": entrada,
            "salida": salida,
            "timestamp": datetime.now().isoformat()
        })

    def obtener_info(self) -> Dict[str, Any]:
        """Obtiene información del servidor."""
        return {
            "nombre": self.nombre,
            "version": self.version,
            "modelo_llm": self.modelo_llm,
            "modelo_embeddings": self.modelo_embeddings,
            "herramientas": list(self.herramientas.keys()),
            "colecciones": list(self.vectorstores.keys()),
            "total_operaciones": len(self.historial)
        }


# Ejemplo de uso
async def main():
    print("=" * 70)
    print("Servidor MCP con RAG - LangChain y Ollama")
    print("=" * 70)

    # Crear servidor
    servidor = ServidorMCPRAG(
        modelo_llm="llama3.2",
        modelo_embeddings="nomic-embed-text"
    )

    # Mostrar información
    info = servidor.obtener_info()
    print(f"\n📋 Información del servidor:")
    print(json.dumps(info, indent=2, ensure_ascii=False))

    # Ejemplo 1: Crear colección
    print(f"\n{'='*70}")
    print("Ejemplo 1: Crear colección de documentos")
    print("="*70)

    resultado = servidor.crear_coleccion(
        "documentacion_ia",
        "Documentación sobre inteligencia artificial"
    )
    print(f"Colección creada: {resultado}")

    # Ejemplo 2: Agregar documentos
    print(f"\n{'='*70}")
    print("Ejemplo 2: Agregar documentos a la colección")
    print("="*70)

    documentos = [
        """
        Machine Learning es una rama de la inteligencia artificial que permite
        a las computadoras aprender de los datos sin ser explícitamente programadas.
        Los algoritmos de ML pueden identificar patrones en datos y hacer predicciones
        basadas en esos patrones.
        """,
        """
        Deep Learning es un subconjunto del Machine Learning que utiliza redes
        neuronales artificiales con múltiples capas. Estas redes pueden aprender
        representaciones jerárquicas de los datos, lo que las hace especialmente
        efectivas para tareas como reconocimiento de imágenes y procesamiento
        del lenguaje natural.
        """,
        """
        El Procesamiento del Lenguaje Natural (NLP) es un campo de la IA que
        se centra en la interacción entre computadoras y lenguaje humano.
        Las aplicaciones de NLP incluyen traducción automática, análisis de
        sentimientos, chatbots y resumen de textos.
        """,
        """
        Los modelos de lenguaje grandes (LLMs) como GPT son sistemas de IA
        entrenados con enormes cantidades de texto. Pueden generar texto coherente,
        responder preguntas y realizar diversas tareas de procesamiento de lenguaje
        con notable precisión.
        """
    ]

    metadatos = [
        {"tema": "Machine Learning", "autor": "Sistema"},
        {"tema": "Deep Learning", "autor": "Sistema"},
        {"tema": "NLP", "autor": "Sistema"},
        {"tema": "LLMs", "autor": "Sistema"}
    ]

    resultado = servidor.agregar_documentos(
        "documentacion_ia",
        documentos,
        metadatos
    )
    print(f"Documentos agregados: {resultado['documentos_agregados']}")
    print(f"Chunks creados: {resultado['chunks_creados']}")

    # Ejemplo 3: Realizar consultas RAG
    print(f"\n{'='*70}")
    print("Ejemplo 3: Consultas RAG")
    print("="*70)

    preguntas = [
        "¿Qué es Machine Learning?",
        "¿Cuál es la diferencia entre ML y Deep Learning?",
        "¿Para qué se usa el NLP?",
        "¿Qué son los LLMs?"
    ]

    for pregunta in preguntas:
        print(f"\n❓ Pregunta: {pregunta}")
        resultado = servidor.consultar("documentacion_ia", pregunta, k=2)

        if resultado["exito"]:
            print(f"✅ Respuesta: {resultado['respuesta']}")
            print(f"📚 Documentos usados: {resultado['num_documentos_usados']}")
        else:
            print(f"❌ Error: {resultado.get('error')}")

    # Ejemplo 4: Búsqueda por similitud
    print(f"\n{'='*70}")
    print("Ejemplo 4: Búsqueda por similitud")
    print("="*70)

    resultado = servidor.buscar_similar(
        "documentacion_ia",
        "redes neuronales profundas",
        k=3
    )

    if resultado["exito"]:
        print(f"🔍 Encontrados {resultado['num_resultados']} documentos similares:")
        for i, doc in enumerate(resultado['resultados'], 1):
            print(f"\n{i}. Tema: {doc['metadata'].get('tema', 'N/A')}")
            print(f"   Contenido: {doc['contenido'][:100]}...")

    # Ejemplo 5: Listar colecciones
    print(f"\n{'='*70}")
    print("Ejemplo 5: Listar colecciones")
    print("="*70)

    resultado = servidor.listar_colecciones()
    print(f"Total de colecciones: {resultado['total']}")
    for col in resultado['colecciones']:
        print(f"  - {col['nombre']}: {col['num_documentos']} documentos")

    # Mostrar estadísticas
    print(f"\n{'='*70}")
    print("📊 Estadísticas del servidor")
    print("="*70)
    print(f"Total de operaciones: {len(servidor.historial)}")


if __name__ == "__main__":
    asyncio.run(main())
