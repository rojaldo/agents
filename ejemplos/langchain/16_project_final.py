#!/usr/bin/env python3
"""
16_project_final.py - Proyecto Final: Sistema de Asistente Inteligente

Integra:
- Chat con memoria
- RAG
- Agentes con herramientas
- Error handling
"""

import logging
from typing import List, Optional
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain.schema import Document
from langchain_core.tools import tool
from langchain.agents import create_react_agent, AgentExecutor


# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============ MÓDULOS DEL PROYECTO ============

class ConfigManager:
    """Gestionar configuración centralizada"""

    OLLAMA_MODEL = "mistral"
    OLLAMA_URL = "http://localhost:11434"
    MAX_MEMORIA_TURNOS = 10

    @staticmethod
    def get_llm() -> Ollama:
        """Crear instancia del LLM"""
        return Ollama(
            model=ConfigManager.OLLAMA_MODEL,
            base_url=ConfigManager.OLLAMA_URL
        )


class ChatModule:
    """Módulo de chat conversacional"""

    def __init__(self):
        self.llm = ConfigManager.get_llm()
        self.memoria = ConversationBufferMemory(return_messages=True)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Eres un asistente inteligente y útil."),
            ("placeholder", "{chat_history}"),
            ("user", "{input}")
        ])
        self.chain = self.prompt | self.llm

    def chat(self, user_input: str) -> str:
        """Procesar mensaje del usuario"""
        try:
            historial = self.memoria.load_memory_variables({})

            respuesta = self.chain.invoke({
                "chat_history": historial['chat_history'],
                "input": user_input
            })

            self.memoria.save_context(
                {"input": user_input},
                {"output": respuesta}
            )

            logger.info(f"Chat: {len(user_input)} chars → {len(respuesta)} chars")
            return respuesta

        except Exception as e:
            logger.error(f"Error en chat: {e}")
            return "Error al procesar la solicitud"

    def clear_history(self):
        """Limpiar historial"""
        self.memoria.clear()
        logger.info("Historial limpiado")


class RAGModule:
    """Módulo de Recuperación (RAG)"""

    def __init__(self):
        self.embeddings = OllamaEmbeddings(model="mistral")
        self.vector_store = None
        logger.info("RAG Module inicializado")

    def load_documents(self, texts: List[str]):
        """Cargar documentos"""
        try:
            docs = [Document(page_content=text) for text in texts]
            self.vector_store = FAISS.from_documents(docs, self.embeddings)
            logger.info(f"Cargados {len(texts)} documentos")
        except Exception as e:
            logger.error(f"Error cargando documentos: {e}")

    def search(self, query: str, k: int = 3) -> List[str]:
        """Buscar documentos relevantes"""
        try:
            if not self.vector_store:
                logger.warning("Vector store vacío")
                return []

            results = self.vector_store.similarity_search(query, k=k)
            logger.info(f"Búsqueda: {len(results)} resultados")
            return [doc.page_content for doc in results]

        except Exception as e:
            logger.error(f"Error en búsqueda: {e}")
            return []


class AgentModule:
    """Módulo de agentes con herramientas"""

    def __init__(self):
        self.llm = ConfigManager.get_llm()
        self._setup_tools()
        logger.info("Agent Module inicializado")

    def _setup_tools(self):
        """Configurar herramientas del agente"""

        @tool
        def obtener_fecha() -> str:
            """Obtiene la fecha actual"""
            from datetime import date
            return str(date.today())

        @tool
        def sumar(a: int, b: int) -> int:
            """Suma dos números"""
            return a + b

        @tool
        def multiplicar(a: int, b: int) -> int:
            """Multiplica dos números"""
            return a * b

        self.herramientas = [obtener_fecha, sumar, multiplicar]

    def ejecutar(self, tarea: str) -> str:
        """Ejecutar tarea con agente"""
        try:
            prompt = """Eres un asistente que puede usar herramientas.
Tienes acceso a: {tools}

{format_instructions}

Tarea: {{input}}"""

            from langchain_core.prompts import PromptTemplate
            prompt_obj = PromptTemplate.from_template(prompt)

            agente = create_react_agent(self.llm, self.herramientas, prompt_obj)
            executor = AgentExecutor(
                agent=agente,
                tools=self.herramientas,
                verbose=False,
                max_iterations=5
            )

            resultado = executor.invoke({"input": tarea})
            logger.info(f"Agente completó tarea")
            return resultado.get("output", "No hay resultado")

        except Exception as e:
            logger.error(f"Error en agente: {e}")
            return f"Error: {str(e)}"


class SmartAssistant:
    """Sistema integrado de asistente inteligente"""

    def __init__(self):
        self.chat = ChatModule()
        self.rag = RAGModule()
        self.agent = AgentModule()
        logger.info("SmartAssistant inicializado")

    def procesar(self, entrada: str, tipo: str = "chat") -> str:
        """Procesar entrada según tipo"""

        if tipo == "chat":
            return self.chat.chat(entrada)

        elif tipo == "buscar":
            resultados = self.rag.search(entrada)
            if resultados:
                return f"Documentos encontrados:\n" + \
                       "\n".join([f"- {r[:80]}..." for r in resultados])
            else:
                return "No se encontraron documentos"

        elif tipo == "tarea":
            return self.agent.ejecutar(entrada)

        else:
            return "Tipo no reconocido"

    def demo_completo(self):
        """Demo del sistema completo"""
        print("\n" + "=" * 60)
        print("DEMO: Sistema de Asistente Inteligente")
        print("=" * 60)

        # Cargar base de conocimiento
        print("\n1️⃣  Cargando base de conocimiento...")
        documentos = [
            "Python es un lenguaje de programación versátil",
            "JavaScript se usa para desarrollo web",
            "Rust es un lenguaje seguro y rápido",
            "LangChain es un framework para LLMs"
        ]
        self.rag.load_documents(documentos)
        print("   ✓ Base de conocimiento cargada")

        # Chat
        print("\n2️⃣  Probando chat...")
        try:
            resp = self.chat.chat("Hola, ¿cómo estás?")
            print(f"   Bot: {resp[:80]}...")
        except:
            print("   (Ollama no disponible)")

        # Búsqueda
        print("\n3️⃣  Probando búsqueda...")
        resultados = self.rag.search("¿Qué es Python?")
        if resultados:
            print(f"   ✓ Encontrados {len(resultados)} documentos")
        else:
            print("   (No disponible)")

        # Agente
        print("\n4️⃣  Probando agente...")
        try:
            resultado = self.agent.ejecutar("¿Cuánto es 5 más 3?")
            print(f"   ✓ Agente respondió")
        except:
            print("   (Ollama no disponible)")

        print("\n✅ Demo completada\n")


def ejemplo_basico():
    """Ejemplo básico del sistema"""
    print("=" * 60)
    print("EJEMPLO: Sistema de Asistente Inteligente")
    print("=" * 60)

    asistente = SmartAssistant()

    # Cargar documentos
    asistente.rag.load_documents([
        "Python es un lenguaje interpretado y dinámico",
        "JavaScript se ejecuta en navegadores",
        "LangChain permite construir apps con LLMs"
    ])

    # Interacciones
    interacciones = [
        ("Hola", "chat"),
        ("¿Qué es Python?", "buscar"),
        ("Calcula 10 * 5", "tarea"),
    ]

    for entrada, tipo in interacciones:
        try:
            print(f"\n📝 Entrada: {entrada}")
            print(f"📂 Tipo: {tipo}")

            resultado = asistente.procesar(entrada, tipo)
            print(f"✓ Resultado: {resultado[:100]}...")

        except Exception as e:
            print(f"⚠️  Error: {e}")

    print()


def main():
    """Función principal"""
    try:
        # Ejecutar ejemplo básico
        ejemplo_basico()

        # Demo completo
        asistente = SmartAssistant()
        asistente.demo_completo()

        print("=" * 60)
        print("✅ Proyecto final completado")
        print("=" * 60)

    except Exception as e:
        logger.critical(f"Error fatal: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
