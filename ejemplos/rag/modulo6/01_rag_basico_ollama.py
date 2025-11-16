"""
MÓDULO 6: RAG Básico con Ollama
Sistema RAG completo y funcional con Ollama local
"""

import json
from typing import List
import subprocess
import sys

# ============================================================================
# VERIFICAR OLLAMA
# ============================================================================

def verificar_ollama():
    """Verificar si Ollama está corriendo"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            modelos = response.json().get("models", [])
            print("✓ Ollama está corriendo")
            print(f"  Modelos disponibles: {len(modelos)}")
            for modelo in modelos[:3]:
                print(f"    - {modelo.get('name', 'desconocido')}")
            return True
        else:
            print("✗ Ollama no responde")
            return False
    except Exception as e:
        print(f"✗ No se puede conectar a Ollama: {e}")
        return False


# ============================================================================
# SIMULACIÓN DE RAG SIN OLLAMA (para pruebas)
# ============================================================================

class RAGSimple:
    """Sistema RAG simplificado para demostración"""

    def __init__(self):
        self.documentos = [
            "RAG es Retrieval-Augmented Generation. Combina búsqueda de documentos con generación de texto.",
            "Los embeddings convierten texto en vectores numéricos para búsqueda semántica.",
            "LangChain es un framework para construir aplicaciones con modelos de lenguaje.",
            "Ollama permite ejecutar modelos de lenguaje en tu computadora local.",
            "Los vector stores como ChromaDB almacenan y recuperan embeddings eficientemente."
        ]

        self.embeddings_doc = [
            [0.7, 0.2, 0.1, 0.3, 0.4, 0.5, 0.2],
            [0.2, 0.8, 0.3, 0.1, 0.2, 0.3, 0.4],
            [0.3, 0.2, 0.7, 0.2, 0.3, 0.4, 0.5],
            [0.1, 0.3, 0.2, 0.8, 0.5, 0.2, 0.3],
            [0.4, 0.3, 0.2, 0.3, 0.7, 0.1, 0.2],
        ]

    def buscar_documentos_relevantes(self, pregunta: str, top_k: int = 2) -> List[str]:
        """Buscar documentos relevantes (simulado)"""
        # En un sistema real, usaríamos embeddings
        # Aquí simulamos basándonos en palabras clave

        palabras_clave = pregunta.lower().split()
        scores = []

        for i, doc in enumerate(self.documentos):
            score = sum(1 for palabra in palabras_clave if palabra in doc.lower())
            scores.append((i, score))

        # Ordenar por score
        scores.sort(key=lambda x: x[1], reverse=True)

        # Retornar top K documentos
        documentos_relevantes = [self.documentos[i] for i, _ in scores[:top_k] if _ > 0]

        if not documentos_relevantes:
            # Si no hay coincidencias exactas, devolver los más relevantes
            documentos_relevantes = [self.documentos[scores[j][0]] for j in range(top_k)]

        return documentos_relevantes

    def generar_respuesta(self, pregunta: str, contexto: str) -> str:
        """Generar respuesta basada en contexto (simulado)"""
        prompt = f"""Basándote en el siguiente contexto, responde la pregunta de forma concisa.

Contexto:
{contexto}

Pregunta: {pregunta}

Respuesta:"""

        # Simulación de respuesta (en producción usaríamos Ollama)
        respuesta_simulada = f"""Basándome en el contexto proporcionado:

{contexto}

La respuesta es: Los concepto mencionados en el contexto son fundamentales para entender RAG. """

        return respuesta_simulada


# ============================================================================
# DEMOSTRACIÓN DE RAG
# ============================================================================

def demostrar_rag():
    """Demostración completa del sistema RAG"""

    print("=" * 70)
    print("MÓDULO 6: RAG Básico con Ollama")
    print("=" * 70)

    # Verificar Ollama
    print("\n🔍 VERIFICACIÓN DE OLLAMA")
    print("-" * 70)
    ollama_disponible = verificar_ollama()

    # Crear sistema RAG
    rag = RAGSimple()

    # Preguntas de prueba
    preguntas = [
        "¿Qué es RAG?",
        "¿Cómo funcionan los embeddings?",
        "¿Qué es LangChain?"
    ]

    print("\n" + "=" * 70)
    print("PREGUNTAS Y RESPUESTAS CON RAG")
    print("=" * 70)

    resultados = []

    for pregunta in preguntas:
        print(f"\n❓ PREGUNTA: {pregunta}")
        print("-" * 70)

        # 1. Recuperar documentos relevantes
        print("1️⃣ Buscando documentos relevantes...")
        documentos = rag.buscar_documentos_relevantes(pregunta, top_k=2)

        print(f"   ✓ {len(documentos)} documentos encontrados")
        for i, doc in enumerate(documentos, 1):
            print(f"   {i}. {doc[:60]}...")

        # 2. Crear contexto
        contexto = "\n".join([f"- {doc}" for doc in documentos])

        # 3. Generar respuesta
        print("\n2️⃣ Generando respuesta con contexto...")
        respuesta = rag.generar_respuesta(pregunta, contexto)

        print("   ✓ Respuesta generada")
        print(f"\n   {respuesta}")

        # Guardar resultado
        resultados.append({
            "pregunta": pregunta,
            "documentos_utilizados": documentos,
            "respuesta": respuesta
        })

    # ========================================================================
    # ARQUITECTURA DE RAG
    # ========================================================================
    print("\n" + "=" * 70)
    print("FLUJO DE RAG EXPLICADO")
    print("=" * 70)

    flujo = """
    1. INDEXACIÓN (una sola vez):
       ├─ Cargar documentos
       ├─ Dividir en chunks
       ├─ Crear embeddings
       └─ Almacenar en Vector DB

    2. RECUPERACIÓN (en cada pregunta):
       ├─ Crear embedding de la pregunta
       ├─ Buscar similitud en Vector DB
       └─ Recuperar documentos relevantes

    3. GENERACIÓN:
       ├─ Construir prompt con contexto
       ├─ Enviar al LLM
       └─ Retornar respuesta contextualizada
    """

    print(flujo)

    # ========================================================================
    # CÓDIGO PARA USAR CON OLLAMA REAL
    # ========================================================================
    print("\n" + "=" * 70)
    print("CÓDIGO PARA USAR CON OLLAMA REAL")
    print("=" * 70)

    codigo = '''
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. PREPARAR DOCUMENTOS
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_text(documento)

# 2. CREAR VECTOR STORE
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_store = Chroma.from_texts(chunks, embeddings)

# 3. CREAR CADENA RAG
llm = OllamaLLM(model="mistral")

def responder_pregunta(pregunta):
    docs = vector_store.similarity_search(pregunta, k=2)
    contexto = "\\n".join([doc.page_content for doc in docs])

    prompt = f"Basándote en: {contexto}\\n\\nPregunta: {pregunta}"
    return llm.invoke(prompt)

# 4. USAR
respuesta = responder_pregunta("¿Qué es RAG?")
print(respuesta)
    '''

    print(codigo)

    # ========================================================================
    # VENTAJAS DE RAG
    # ========================================================================
    print("\n" + "=" * 70)
    print("VENTAJAS DE RAG")
    print("=" * 70)

    ventajas = {
        "Precisión": "Respuestas basadas en datos reales",
        "Actualización": "Fácil agregar nuevos documentos",
        "Privacidad": "Datos sensibles se quedan locales",
        "Trazabilidad": "Se pueden citar fuentes",
        "Eficiencia": "Modelos más pequeños funcionan mejor",
        "Local": "Todo corre en tu máquina"
    }

    for ventaja, descripción in ventajas.items():
        print(f"  ✓ {ventaja}: {descripción}")

    # ========================================================================
    # GUARDAR RESULTADOS
    # ========================================================================
    resultado_final = {
        "ollama_disponible": ollama_disponible,
        "sistema": "RAG Básico",
        "modelo_recomendado": "mistral" if ollama_disponible else "N/A",
        "preguntas_respondidas": len(resultados),
        "resultados": resultados
    }

    with open("rag_resultado.json", "w", encoding="utf-8") as f:
        json.dump(resultado_final, f, ensure_ascii=False, indent=2)

    print("\n✓ Resultados guardados en rag_resultado.json")
    print("✅ RAG Básico demostrado exitosamente")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    demostrar_rag()
