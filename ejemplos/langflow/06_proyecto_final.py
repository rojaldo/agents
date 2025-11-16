#!/usr/bin/env python3
"""
06_proyecto_final.py - Proyecto Integrado Final

Demuestra un proyecto completo que integra todos los conceptos:
- Chat con memoria
- Búsqueda web
- Procesamiento de documentos (RAG)
- Manejo de errores
- Exportable como API
"""

from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import CharacterTextSplitter
import logging
from datetime import datetime
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# EJEMPLO 1: Asistente Inteligente Simple
# ============================================================================

def ejemplo_1_asistente_simple():
    """Ejemplo 1: Asistente inteligente con conversación"""
    print("=" * 60)
    print("EJEMPLO 1: Asistente Inteligente Simple")
    print("=" * 60)

    class AsistenteInteligente:
        """Asistente básico con memoria y personalidad"""

        def __init__(self, nombre="Langflow Bot"):
            self.nombre = nombre
            self.memoria = ConversationBufferMemory(return_messages=True)
            self.llm = Ollama(model="mistral", base_url="http://localhost:11434")
            self.prompt = ChatPromptTemplate.from_messages([
                ("system", f"Eres {nombre}, un asistente útil y amable."),
                ("placeholder", "{chat_history}"),
                ("user", "{input}")
            ])
            self.cadena = self.prompt | self.llm
            self.historial_sesion = []

        def procesar(self, entrada: str) -> str:
            """Procesa una entrada y retorna respuesta"""
            try:
                historial = self.memoria.load_memory_variables({})

                respuesta = self.cadena.invoke({
                    "chat_history": historial["chat_history"],
                    "input": entrada
                })

                # Guardar en memoria
                self.memoria.save_context(
                    {"input": entrada},
                    {"output": respuesta}
                )

                # Guardar en historial de sesión
                self.historial_sesion.append({
                    "timestamp": datetime.now().isoformat(),
                    "usuario": entrada,
                    "asistente": respuesta[:100]
                })

                logger.info(f"Procesado: {entrada[:50]}...")
                return respuesta

            except Exception as e:
                logger.error(f"Error: {e}")
                return f"Disculpa, ocurrió un error: {str(e)}"

        def obtener_sesion(self):
            """Retorna historial de sesión"""
            return self.historial_sesion

    # Test
    asistente = AsistenteInteligente("Langflow Assistant")

    conversacion = [
        "Hola, ¿cómo estás?",
        "¿Cuál es tu nombre?",
        "¿Qué puedes hacer?",
        "Cuéntame un chiste corto"
    ]

    print(f"\n💬 Conversación con {asistente.nombre}:\n")

    for entrada in conversacion:
        print(f"👤 Usuario: {entrada}")
        respuesta = asistente.procesar(entrada)
        print(f"🤖 Bot: {respuesta[:80]}...\n")

    print(f"✅ Sesión completada con {len(asistente.historial_sesion)} turnos")


# ============================================================================
# EJEMPLO 2: Asistente con Web Search
# ============================================================================

def ejemplo_2_asistente_web_search():
    """Ejemplo 2: Asistente que puede buscar en web"""
    print("\n" + "=" * 60)
    print("EJEMPLO 2: Asistente con Web Search")
    print("=" * 60)

    class AsistenteWebSearch:
        """Asistente que integra búsqueda web"""

        def __init__(self):
            self.llm = Ollama(model="mistral", base_url="http://localhost:11434")
            self.search = DuckDuckGoSearchRun()
            self.memoria = ConversationBufferMemory(return_messages=True)

        def detectar_necesidad_busqueda(self, entrada: str) -> bool:
            """Detecta si la entrada requiere búsqueda web"""
            palabras_clave = ["actualidad", "noticias", "hoy", "últimas", "actual", "precio", "clima"]
            return any(palabra in entrada.lower() for palabra in palabras_clave)

        def procesar(self, entrada: str) -> dict:
            """Procesa entrada con búsqueda opcional"""
            try:
                resultado = {
                    "entrada": entrada,
                    "necesita_busqueda": self.detectar_necesidad_busqueda(entrada),
                    "busqueda": None,
                    "respuesta": None,
                    "fuente": "llm"
                }

                # Si necesita búsqueda
                if resultado["necesita_busqueda"]:
                    print(f"   🔍 Buscando en web...")
                    resultado["busqueda"] = self.search.run(entrada)
                    resultado["fuente"] = "web_search"

                    # Usar búsqueda en respuesta
                    prompt = ChatPromptTemplate.from_template(
                        f"Basándote en esta información: {{info}}\n\n"
                        f"Responde la pregunta: {{pregunta}}"
                    )
                    cadena = prompt | self.llm

                    resultado["respuesta"] = cadena.invoke({
                        "info": resultado["busqueda"][:200],
                        "pregunta": entrada
                    })

                else:
                    # Respuesta directa
                    prompt = ChatPromptTemplate.from_template("Responde: {pregunta}")
                    cadena = prompt | self.llm
                    resultado["respuesta"] = cadena.invoke({"pregunta": entrada})

                logger.info(f"Procesado con fuente: {resultado['fuente']}")
                return resultado

            except Exception as e:
                logger.error(f"Error: {e}")
                return {
                    "entrada": entrada,
                    "error": str(e),
                    "respuesta": "No pude procesar tu pregunta"
                }

    asistente = AsistenteWebSearch()

    preguntas = [
        "¿Cómo estás?",
        "¿Qué noticias hay hoy?",
        "¿Cuál es la capital de Francia?",
        "¿Cuál es el precio actual de Bitcoin?"
    ]

    print(f"\n🌐 Asistente con Web Search:\n")

    for pregunta in preguntas:
        print(f"❓ Pregunta: {pregunta}")
        resultado = asistente.procesar(pregunta)

        if "error" not in resultado:
            print(f"   Fuente: {resultado['fuente']}")
            if resultado["busqueda"]:
                print(f"   Info web: {resultado['busqueda'][:50]}...")
            print(f"   Respuesta: {resultado['respuesta'][:80]}...\n")
        else:
            print(f"   ❌ Error: {resultado['error']}\n")


# ============================================================================
# EJEMPLO 3: Asistente con RAG
# ============================================================================

def ejemplo_3_asistente_rag():
    """Ejemplo 3: Asistente que integra RAG"""
    print("\n" + "=" * 60)
    print("EJEMPLO 3: Asistente con RAG")
    print("=" * 60)

    class AsistenteRAG:
        """Asistente que usa RAG para responder sobre documentos"""

        def __init__(self):
            self.llm = Ollama(model="mistral", base_url="http://localhost:11434")
            self.vector_store = None
            self.documentos_cargados = []

        def cargar_documentos(self, textos: list):
            """Carga documentos en el vector store"""
            try:
                print(f"   📚 Cargando {len(textos)} documentos...")

                documentos = [Document(page_content=texto) for texto in textos]
                self.documentos_cargados = documentos

                embeddings = OllamaEmbeddings(
                    model="mistral",
                    base_url="http://localhost:11434"
                )

                self.vector_store = FAISS.from_documents(documentos, embeddings)
                print(f"   ✅ {len(documentos)} documentos cargados")
                logger.info(f"Vector store creado con {len(documentos)} documentos")

                return True

            except Exception as e:
                logger.error(f"Error al cargar documentos: {e}")
                return False

        def consultar(self, pregunta: str) -> dict:
            """Consulta usando RAG"""
            if not self.vector_store:
                return {
                    "pregunta": pregunta,
                    "error": "No hay documentos cargados"
                }

            try:
                # Retrieval
                docs = self.vector_store.similarity_search(pregunta, k=2)
                context = "\n".join([doc.page_content for doc in docs])

                # Generation
                prompt = ChatPromptTemplate.from_template(
                    "Basándote en:\n{context}\n\nResponde: {pregunta}"
                )
                cadena = prompt | self.llm

                respuesta = cadena.invoke({
                    "context": context,
                    "pregunta": pregunta
                })

                logger.info(f"Consulta RAG completada: {pregunta}")

                return {
                    "pregunta": pregunta,
                    "documentos_recuperados": len(docs),
                    "respuesta": respuesta
                }

            except Exception as e:
                logger.error(f"Error en RAG: {e}")
                return {
                    "pregunta": pregunta,
                    "error": str(e)
                }

    # Test
    asistente = AsistenteRAG()

    documentos = [
        "Langflow es una plataforma visual para construir aplicaciones con LLMs",
        "Python es un lenguaje de programación versátil y poderoso",
        "RAG combina retrieval de documentos con generación de texto",
        "FastAPI es un framework moderno para construir APIs en Python",
        "Los embeddings permiten calcular similitud semántica entre textos"
    ]

    print(f"\n📖 Cargando documentos...")
    asistente.cargar_documentos(documentos)

    preguntas = [
        "¿Qué es Langflow?",
        "¿Para qué sirven los embeddings?",
        "¿Qué es RAG?"
    ]

    print(f"\n💭 Consultando documentos:\n")

    for pregunta in preguntas:
        print(f"❓ {pregunta}")
        resultado = asistente.consultar(pregunta)

        if "error" not in resultado:
            print(f"   📚 Documentos: {resultado['documentos_recuperados']}")
            print(f"   📝 Respuesta: {resultado['respuesta'][:80]}...\n")
        else:
            print(f"   ❌ Error: {resultado['error']}\n")


# ============================================================================
# EJEMPLO 4: Asistente Completo Integrado
# ============================================================================

def ejemplo_4_asistente_completo():
    """Ejemplo 4: Asistente que integra todo"""
    print("\n" + "=" * 60)
    print("EJEMPLO 4: Asistente Inteligente Completo")
    print("=" * 60)

    class AsistenteCompleto:
        """Asistente que integra todos los conceptos"""

        def __init__(self, nombre="Smart Assistant"):
            self.nombre = nombre
            self.memoria = ConversationBufferMemory(return_messages=True)
            self.llm = Ollama(model="mistral", base_url="http://localhost:11434")
            self.vector_store = None
            self.metricas = {
                "total_consultas": 0,
                "consultas_exitosas": 0,
                "consultas_fallidas": 0,
                "promedio_respuesta": 0
            }

        def validar_entrada(self, entrada: str) -> tuple[bool, str]:
            """Valida la entrada"""
            if not entrada:
                return False, "Entrada vacía"
            if len(entrada) < 3:
                return False, "Entrada muy corta"
            return True, "OK"

        def clasificar_consulta(self, entrada: str) -> str:
            """Clasifica el tipo de consulta"""
            if "?" in entrada:
                return "pregunta"
            elif any(palabra in entrada.lower() for palabra in ["python", "código", "api", "programación"]):
                return "tecnica"
            elif any(palabra in entrada.lower() for palabra in ["hola", "cómo", "gracias"]):
                return "conversacion"
            else:
                return "general"

        def procesar(self, entrada: str) -> dict:
            """Procesa una entrada completa"""
            self.metricas["total_consultas"] += 1

            # 1. Validación
            valida, mensaje = self.validar_entrada(entrada)
            if not valida:
                self.metricas["consultas_fallidas"] += 1
                return {
                    "entrada": entrada,
                    "estado": "error",
                    "error": mensaje
                }

            try:
                # 2. Clasificación
                tipo = self.clasificar_consulta(entrada)

                # 3. Procesamiento
                historial = self.memoria.load_memory_variables({})

                prompt = ChatPromptTemplate.from_messages([
                    ("system", f"Eres {self.nombre}, un asistente inteligente"),
                    ("placeholder", "{chat_history}"),
                    ("user", "{input}")
                ])
                cadena = prompt | self.llm

                respuesta = cadena.invoke({
                    "chat_history": historial["chat_history"],
                    "input": entrada
                })

                # 4. Guardar en memoria
                self.memoria.save_context(
                    {"input": entrada},
                    {"output": respuesta}
                )

                self.metricas["consultas_exitosas"] += 1

                resultado = {
                    "entrada": entrada,
                    "tipo": tipo,
                    "respuesta": respuesta,
                    "estado": "éxito",
                    "timestamp": datetime.now().isoformat()
                }

                logger.info(f"Procesada consulta {tipo}: {entrada[:50]}...")
                return resultado

            except Exception as e:
                self.metricas["consultas_fallidas"] += 1
                logger.error(f"Error: {e}")
                return {
                    "entrada": entrada,
                    "estado": "error",
                    "error": str(e)
                }

        def obtener_metricas(self) -> dict:
            """Obtiene métricas de uso"""
            tasa_exito = 0
            if self.metricas["total_consultas"] > 0:
                tasa_exito = self.metricas["consultas_exitosas"] / self.metricas["total_consultas"] * 100

            return {
                **self.metricas,
                "tasa_exito_pct": round(tasa_exito, 2)
            }

    # Test
    asistente = AsistenteCompleto("Smart Assistant")

    conversacion = [
        "Hola, ¿cómo estás?",
        "¿Qué es Python?",
        "Cuéntame un chiste",
        "¿Cómo hago un API en Python?",
        "Gracias por tu ayuda"
    ]

    print(f"\n🤖 Conversación con {asistente.nombre}:\n")

    for entrada in conversacion:
        print(f"👤 Usuario: {entrada}")
        resultado = asistente.procesar(entrada)

        if resultado["estado"] == "éxito":
            print(f"   Tipo: {resultado['tipo']}")
            print(f"🤖 Bot: {resultado['respuesta'][:80]}...\n")
        else:
            print(f"   ❌ Error: {resultado.get('error', 'Error desconocido')}\n")

    # Mostrar métricas
    print("\n📊 Métricas de la sesión:")
    metricas = asistente.obtener_metricas()
    for clave, valor in metricas.items():
        print(f"   {clave}: {valor}")


# ============================================================================
# EJEMPLO 5: Exportación a Configuración JSON
# ============================================================================

def ejemplo_5_exportar_configuracion():
    """Ejemplo 5: Exportar configuración de asistente"""
    print("\n" + "=" * 60)
    print("EJEMPLO 5: Exportar Configuración de Proyecto")
    print("=" * 60)

    config_proyecto = {
        "nombre": "Asistente Inteligente Langflow",
        "version": "1.0.0",
        "descripcion": "Asistente AI integrado con múltiples capacidades",
        "componentes": [
            {
                "nombre": "Chat Module",
                "tipo": "conversacion",
                "llm": "mistral",
                "memoria": "ConversationBufferMemory"
            },
            {
                "nombre": "Web Search Module",
                "tipo": "busqueda",
                "herramienta": "DuckDuckGo"
            },
            {
                "nombre": "RAG Module",
                "tipo": "recuperacion",
                "vector_store": "FAISS",
                "embeddings": "OllamaEmbeddings"
            },
            {
                "nombre": "Error Handler",
                "tipo": "manejo_errores",
                "estrategia": "fallback_y_retry"
            }
        ],
        "endpoints_api": [
            {
                "path": "/chat",
                "metodo": "POST",
                "descripcion": "Procesar mensaje de chat"
            },
            {
                "path": "/search",
                "metodo": "POST",
                "descripcion": "Buscar en web"
            },
            {
                "path": "/query",
                "metodo": "POST",
                "descripcion": "Consultar RAG"
            },
            {
                "path": "/health",
                "metodo": "GET",
                "descripcion": "Health check"
            }
        ],
        "configuracion_servidor": {
            "host": "0.0.0.0",
            "puerto": 8000,
            "workers": 4,
            "timeout": 60
        },
        "configuracion_llm": {
            "modelo": "mistral",
            "url_base": "http://localhost:11434",
            "timeout": 30
        },
        "seguridad": {
            "autenticacion": "tokens",
            "rate_limiting": True,
            "cors_habilitado": True
        }
    }

    print("\n📋 Configuración del Proyecto:\n")
    print(json.dumps(config_proyecto, indent=2, ensure_ascii=False))

    # Guardar configuración
    config_json = json.dumps(config_proyecto, indent=2, ensure_ascii=False)
    print(f"\n✅ Configuración generada ({len(config_json)} bytes)")
    logger.info("Configuración de proyecto exportada")


def main():
    """Función principal"""
    try:
        ejemplo_1_asistente_simple()
        ejemplo_2_asistente_web_search()
        ejemplo_3_asistente_rag()
        ejemplo_4_asistente_completo()
        ejemplo_5_exportar_configuracion()

        print("\n" + "=" * 60)
        print("✅ Proyecto integrado completado con éxito")
        print("=" * 60)

    except Exception as e:
        logger.critical(f"Error fatal: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
