"""
MÓDULO 10: Casos de Uso Prácticos - QA sobre Documentos
Sistema práctico para responder preguntas sobre documentos
"""

import json
from typing import List, Dict
from pathlib import Path

# ============================================================================
# SISTEMA DE QA SOBRE DOCUMENTOS
# ============================================================================

class SistemaQADocumentos:
    """Sistema Q&A sobre documentos - Caso práctico real"""

    def __init__(self):
        self.documentos = self._cargar_documentos()

    def _cargar_documentos(self) -> List[Dict]:
        """Cargar documentos de prueba"""
        return [
            {
                "id": 1,
                "titulo": "Introducción a Python",
                "contenido": """
Python es un lenguaje de programación interpretado de alto nivel.
Fue creado por Guido van Rossum y lanzado en 1991.
Se caracteriza por su sintaxis simple y legible.
Python es ampliamente usado en:
- Desarrollo web (Django, Flask)
- Ciencia de datos (Pandas, NumPy)
- Machine learning (TensorFlow, PyTorch)
- Automatización de tareas
- Scripting y desarrollo de herramientas
Es gratuito y de código abierto.
                """,
                "palabras_clave": ["python", "lenguaje", "programación"]
            },
            {
                "id": 2,
                "titulo": "RAG - Retrieval-Augmented Generation",
                "contenido": """
RAG es una arquitectura que combina recuperación de documentos con generación de texto.
El proceso funciona en dos fases:
1. Recuperación: Buscar documentos relevantes en una base de datos
2. Generación: Usar esos documentos para generar una respuesta

Ventajas de RAG:
- Respuestas más precisas basadas en datos reales
- Fácil de actualizar con nuevos documentos
- Mantiene privacidad de datos sensibles
- Permite citar fuentes de información
- Funciona con modelos más pequeños

RAG es especialmente útil para:
- Chatbots de soporte técnico
- Sistemas de Q&A
- Análisis de documentos
                """,
                "palabras_clave": ["rag", "retrieval", "generación", "documento"]
            },
            {
                "id": 3,
                "titulo": "Ollama - Modelos Locales",
                "contenido": """
Ollama es una herramienta que permite ejecutar modelos de lenguaje localmente.
Principales características:
- Modelos disponibles: Mistral, Llama2, Neural-Chat, TinyLlama
- No requiere GPUs potentes
- Todo se ejecuta en tu máquina (sin APIs externas)
- Privacidad total de los datos

Uso básico:
ollama pull mistral
ollama serve

Modelos recomendados:
- Mistral 7B: Mejor relación velocidad/calidad
- Llama2 7B: Muy versátil
- TinyLlama 1.1B: Rápido para desarrollo
                """,
                "palabras_clave": ["ollama", "modelos", "local"]
            }
        ]

    def buscar_documentos(self, pregunta: str, top_k: int = 3) -> List[Dict]:
        """Buscar documentos relevantes"""
        palabras_pregunta = set(pregunta.lower().split())

        scores = []
        for doc in self.documentos:
            # Calcular score de relevancia
            palabras_doc = set(doc["contenido"].lower().split())
            score = len(palabras_pregunta & palabras_doc)

            # Bonus por palabras clave
            for palabra_clave in doc["palabras_clave"]:
                if palabra_clave in palabras_pregunta:
                    score += 5

            scores.append((doc, score))

        # Ordenar por score
        scores.sort(key=lambda x: x[1], reverse=True)

        # Retornar top K
        documentos_relevantes = [doc for doc, score in scores[:top_k] if score > 0]
        return documentos_relevantes

    def generar_respuesta(self, pregunta: str, documentos: List[Dict]) -> str:
        """Generar respuesta basada en documentos"""
        if not documentos:
            return "No encontré documentos relacionados con tu pregunta."

        contexto = "\n---\n".join([d["contenido"] for d in documentos])

        respuesta = f"""Basándome en los documentos encontrados:

CONTEXTO:
{contexto[:500]}...

RESPUESTA:
Tu pregunta sobre '{pregunta}' se relaciona con los temas mencionados arriba.
Los documentos proporcionan información detallada sobre este tema.
"""
        return respuesta

    def responder(self, pregunta: str) -> Dict:
        """Flujo completo de Q&A"""
        # Buscar documentos
        documentos = self.buscar_documentos(pregunta)

        # Generar respuesta
        respuesta = self.generar_respuesta(pregunta, documentos)

        # Retornar resultado
        return {
            "pregunta": pregunta,
            "documentos_encontrados": len(documentos),
            "titulos_documentos": [d["titulo"] for d in documentos],
            "respuesta": respuesta
        }


# ============================================================================
# DEMOSTRACIÓN
# ============================================================================

def demostrar_qa_documentos():
    """Demostración del sistema Q&A"""

    print("=" * 70)
    print("MÓDULO 10: Q&A sobre Documentos")
    print("=" * 70)

    # Crear sistema
    qa_system = SistemaQADocumentos()

    print(f"\n📚 Base de conocimiento cargada:")
    print(f"   Total de documentos: {len(qa_system.documentos)}")
    for doc in qa_system.documentos:
        print(f"   - {doc['titulo']}")

    # Preguntas de ejemplo
    preguntas = [
        "¿Qué es Python y para qué sirve?",
        "¿Cómo funciona RAG?",
        "¿Puedo usar Ollama en mi computadora?",
        "¿Cuál es la diferencia entre Python y otros lenguajes?"
    ]

    print("\n" + "=" * 70)
    print("PREGUNTAS Y RESPUESTAS")
    print("=" * 70)

    resultados = []

    for pregunta in preguntas:
        print(f"\n❓ {pregunta}")
        print("-" * 70)

        # Procesar pregunta
        resultado = qa_system.responder(pregunta)

        # Mostrar documentos encontrados
        print(f"Documentos encontrados: {resultado['documentos_encontrados']}")
        for titulo in resultado['titulos_documentos']:
            print(f"  ✓ {titulo}")

        # Mostrar respuesta
        print(f"\n{resultado['respuesta'][:300]}...")

        resultados.append(resultado)

    # ========================================================================
    # ESTADÍSTICAS
    # ========================================================================
    print("\n" + "=" * 70)
    print("ESTADÍSTICAS DEL SISTEMA")
    print("=" * 70)

    documentos_utilizados = sum(r['documentos_encontrados'] for r in resultados)
    print(f"  • Preguntas procesadas: {len(resultados)}")
    print(f"  • Documentos reutilizados: {documentos_utilizados}")
    print(f"  • Promedio documentos por pregunta: {documentos_utilizados / len(resultados):.1f}")

    # ========================================================================
    # CÓDIGO PARA PRODUCCIÓN
    # ========================================================================
    print("\n" + "=" * 70)
    print("CÓDIGO PARA USAR CON OLLAMA EN PRODUCCIÓN")
    print("=" * 70)

    codigo = '''
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

# 1. CARGAR DOCUMENTOS
from langchain_community.document_loaders import TextLoader
loader = TextLoader("documentos.txt")
docs = loader.load()

# 2. PREPARAR DOCUMENTOS
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# 3. CREAR VECTOR STORE
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_store = Chroma.from_documents(chunks, embeddings)

# 4. CREAR SISTEMA QA
llm = OllamaLLM(model="mistral")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever()
)

# 5. USAR
respuesta = qa_chain.invoke({"query": "¿Qué es RAG?"})
print(respuesta)
    '''

    print(codigo)

    # ========================================================================
    # CASOS DE USO
    # ========================================================================
    print("\n" + "=" * 70)
    print("CASOS DE USO REALES")
    print("=" * 70)

    casos = {
        "Soporte Técnico": "Responder preguntas sobre bases de conocimiento",
        "Análisis Legal": "Buscar información en documentos legales",
        "Servicio al Cliente": "Responder preguntas frecuentes automáticamente",
        "Búsqueda Empresarial": "Acceso a información interna de la empresa",
        "E-learning": "Responder preguntas de estudiantes sobre material"
    }

    for caso, descripción in casos.items():
        print(f"  ✓ {caso}: {descripción}")

    # ========================================================================
    # GUARDAR RESULTADOS
    # ========================================================================
    resultado_final = {
        "sistema": "Q&A sobre Documentos",
        "documentos_totales": len(qa_system.documentos),
        "preguntas_procesadas": len(resultados),
        "resultados": resultados
    }

    with open("qa_resultado.json", "w", encoding="utf-8") as f:
        json.dump(resultado_final, f, ensure_ascii=False, indent=2)

    print("\n✓ Resultados guardados en qa_resultado.json")
    print("✅ Sistema Q&A demostrado exitosamente")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    demostrar_qa_documentos()
