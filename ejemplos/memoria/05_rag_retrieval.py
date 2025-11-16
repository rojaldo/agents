"""
05_RAG_RETRIEVAL.PY
====================

Ejemplo didáctico: RAG (Retrieval-Augmented Generation)

Demuestra la arquitectura RAG completa:
1. Pregunta del usuario
2. Conversión a embedding
3. Búsqueda de documentos relevantes
4. Creación de prompt con contexto
5. Generación de respuesta con LLM
6. Retorno al usuario

Este ejemplo simula el pipeline sin dependencia de LLM externo,
pero está diseñado para integración fácil con Ollama/LangChain.

REQUISITOS PREVIOS:
- pip install langchain ollama
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
from datetime import datetime
import json


# ============================================================================
# TIPOS Y ESTRUCTURAS
# ============================================================================

class TipoFuente(Enum):
    """Tipos de fuentes de documentos"""
    ARCHIVO = "archivo"
    WEBAPI = "webapi"
    BASEDATOS = "basedatos"
    MANUAL = "manual"


@dataclass
class DocumentoFuente:
    """Documento indexado en la base de conocimiento"""
    id: str
    titulo: str
    contenido: str
    fuente: TipoFuente
    fecha_creacion: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict = field(default_factory=dict)

    def obtener_fragmento(self, max_chars: int = 500) -> str:
        """Retorna fragmento del contenido"""
        if len(self.contenido) <= max_chars:
            return self.contenido
        return self.contenido[:max_chars] + "..."


@dataclass
class ResultadoRAG:
    """Resultado de una búsqueda RAG"""
    query: str
    documentos_recuperados: List[DocumentoFuente]
    scores_relevancia: List[float]
    contexto_generado: str
    respuesta: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


# ============================================================================
# BASE DE CONOCIMIENTO
# ============================================================================

class BaseConocimiento:
    """
    Almacena y gestiona documentos para RAG.
    Simula una base de datos vectorial simple.
    """

    def __init__(self):
        self.documentos: Dict[str, DocumentoFuente] = {}
        self.indice_invertido: Dict[str, List[str]] = {}  # palabra -> lista de doc_ids

    def agregar_documento(self, documento: DocumentoFuente) -> None:
        """Agrega documento a la base de conocimiento"""
        self.documentos[documento.id] = documento

        # Crear índice invertido simple
        palabras = set(documento.contenido.lower().split())
        for palabra in palabras:
            if palabra not in self.indice_invertido:
                self.indice_invertido[palabra] = []
            self.indice_invertido[palabra].append(documento.id)

    def agregar_documentos_batch(self, documentos: List[DocumentoFuente]) -> None:
        """Agrega múltiples documentos"""
        for doc in documentos:
            self.agregar_documento(doc)

    def obtener_documento(self, doc_id: str) -> Optional[DocumentoFuente]:
        """Obtiene un documento por ID"""
        return self.documentos.get(doc_id)

    def listar_documentos(self) -> List[DocumentoFuente]:
        """Lista todos los documentos"""
        return list(self.documentos.values())

    def buscar_por_palabras_clave(
        self,
        query: str,
        top_k: int = 5
    ) -> List[Tuple[DocumentoFuente, float]]:
        """
        Búsqueda simple por palabras clave.
        Retorna documentos ordenados por número de matches.
        """
        palabras_query = set(query.lower().split())
        scores = {}

        # Contar coincidencias por documento
        for palabra in palabras_query:
            if palabra in self.indice_invertido:
                for doc_id in self.indice_invertido[palabra]:
                    scores[doc_id] = scores.get(doc_id, 0) + 1

        # Normalizar scores
        if scores:
            max_score = max(scores.values())
            scores = {doc_id: score / max_score for doc_id, score in scores.items()}

        # Ordenar por score
        docs_ordenados = sorted(
            [(self.documentos[doc_id], score)
             for doc_id, score in scores.items()],
            key=lambda x: x[1],
            reverse=True
        )

        return docs_ordenados[:top_k]

    def resumen_estadisticas(self) -> Dict:
        """Resumen estadístico de la base de conocimiento"""
        return {
            "documentos_totales": len(self.documentos),
            "palabras_unicas": len(self.indice_invertido),
            "documentos_por_fuente": {
                fuente.value: sum(
                    1 for doc in self.documentos.values()
                    if doc.fuente == fuente
                )
                for fuente in TipoFuente
            }
        }


# ============================================================================
# PIPELINE RAG
# ============================================================================

class PipelineRAG:
    """
    Implementa el pipeline completo de RAG:
    Query -> Retrieval -> Context -> Generation -> Response
    """

    def __init__(self, base_conocimiento: BaseConocimiento):
        self.base_conocimiento = base_conocimiento
        self.historial_consultas: List[ResultadoRAG] = []

    def procesar_query(
        self,
        query: str,
        top_k_docs: int = 3,
        max_contexto_chars: int = 2000
    ) -> ResultadoRAG:
        """
        Procesa una query completa a través del pipeline RAG.
        """

        # 1. RECUPERACIÓN: Buscar documentos relevantes
        print(f"\n[RAG] Procesando: {query}")
        print("  [1/5] Recuperando documentos relevantes...")

        docs_relevantes, scores = self._recuperar_documentos(
            query,
            top_k=top_k_docs
        )

        # 2. CONSTRUCCIÓN DE CONTEXTO
        print("  [2/5] Construyendo contexto...")
        contexto = self._construir_contexto(
            docs_relevantes,
            max_chars=max_contexto_chars
        )

        # 3. ENRIQUECIMIENTO DEL PROMPT
        print("  [3/5] Enriqueciendo prompt...")
        prompt_completo = self._crear_prompt(query, contexto, docs_relevantes)

        # 4. GENERACIÓN (simulada)
        print("  [4/5] Generando respuesta...")
        respuesta = self._generar_respuesta(query, contexto)

        # 5. POSTPROCESAMIENTO
        print("  [5/5] Postprocesamiento...")
        resultado = ResultadoRAG(
            query=query,
            documentos_recuperados=docs_relevantes,
            scores_relevancia=scores,
            contexto_generado=contexto,
            respuesta=respuesta
        )

        self.historial_consultas.append(resultado)
        return resultado

    def _recuperar_documentos(
        self,
        query: str,
        top_k: int
    ) -> Tuple[List[DocumentoFuente], List[float]]:
        """Paso 1: Recuperación de documentos"""
        resultados = self.base_conocimiento.buscar_por_palabras_clave(query, top_k=top_k)

        docs = [doc for doc, _ in resultados]
        scores = [score for _, score in resultados]

        print(f"    Documentos recuperados: {len(docs)}")
        for doc, score in zip(docs, scores):
            print(f"      - {doc.titulo} (relevancia: {score:.2f})")

        return docs, scores

    def _construir_contexto(
        self,
        documentos: List[DocumentoFuente],
        max_chars: int = 2000
    ) -> str:
        """Paso 2: Construcción de contexto"""
        contexto_partes = ["CONTEXTO RELEVANTE:"]
        chars_usados = 0

        for i, doc in enumerate(documentos, 1):
            seccion = f"\n[Fuente {i}] {doc.titulo}\n{doc.contenido}"

            if chars_usados + len(seccion) <= max_chars:
                contexto_partes.append(seccion)
                chars_usados += len(seccion)
            else:
                # Truncar para ajustarse al límite
                espacio_restante = max_chars - chars_usados
                if espacio_restante > 100:
                    contexto_partes.append(
                        f"\n[Fuente {i}] {doc.titulo}\n"
                        f"{doc.contenido[:espacio_restante]}..."
                    )
                break

        contexto = "\n".join(contexto_partes)
        print(f"    Contexto construido: {len(contexto)} caracteres")
        return contexto

    def _crear_prompt(
        self,
        query: str,
        contexto: str,
        documentos: List[DocumentoFuente]
    ) -> str:
        """Paso 3: Creación de prompt enriquecido"""
        prompt = f"""Eres un asistente experto que responde basándose en documentación.

PREGUNTA DEL USUARIO:
{query}

{contexto}

INSTRUCCIONES:
1. Responde basándote ÚNICAMENTE en la información del contexto
2. Si la información no está disponible, indica que se requiere más datos
3. Cita las fuentes utilizadas
4. Sé conciso pero completo

RESPUESTA:"""

        print(f"    Prompt completo: {len(prompt)} caracteres")
        return prompt

    def _generar_respuesta(self, query: str, contexto: str) -> str:
        """
        Paso 4: Generación de respuesta.
        Simulado aquí; en producción usarías Ollama con LangChain:

        from langchain.llms import Ollama
        llm = Ollama(model="mistral")
        response = llm(prompt)
        """

        # Simulación: generar respuesta heurística
        if "precio" in query.lower():
            return "Según los documentos recuperados, los precios varían según el modelo específico. Por favor consulte las especificaciones detalladas en las fuentes citadas."

        elif "características" in query.lower() or "especificaciones" in query.lower():
            return f"He encontrado información sobre las características solicitadas en los documentos contextuales. Las fuentes proporcionan detalles técnicos completos al respecto."

        elif "cómo" in query.lower():
            return "Basándome en la documentación recuperada, aquí está el procedimiento detallado que se describe en los documentos de referencia."

        else:
            return "He encontrado información relevante en la base de conocimiento que responde a tu pregunta. Los detalles se encuentran en las fuentes citadas anteriormente."

    def obtener_resumen_consulta(self, resultado: ResultadoRAG) -> Dict:
        """Crea un resumen legible de una consulta"""
        return {
            "consulta": resultado.query,
            "documentos_usados": len(resultado.documentos_recuperados),
            "documentos": [
                {
                    "titulo": doc.titulo,
                    "relevancia": round(score, 2)
                }
                for doc, score in zip(
                    resultado.documentos_recuperados,
                    resultado.scores_relevancia
                )
            ],
            "contexto_size": len(resultado.contexto_generado),
            "respuesta_preview": resultado.respuesta[:200] + "...",
            "timestamp": resultado.timestamp
        }

    def obtener_estadisticas(self) -> Dict:
        """Estadísticas del pipeline RAG"""
        return {
            "consultas_procesadas": len(self.historial_consultas),
            "documentos_en_base": len(self.base_conocimiento.documentos),
            "promedio_docs_por_consulta": (
                sum(len(r.documentos_recuperados)
                    for r in self.historial_consultas)
                / max(len(self.historial_consultas), 1)
            ),
            "timestamp": datetime.now().isoformat()
        }


# ============================================================================
# INTEGRACIÓN CON OLLAMA (CONFIGURACIÓN PARA PRODUCCIÓN)
# ============================================================================

def crear_pipeline_rag_con_ollama() -> None:
    """
    Ejemplo de cómo integrar el pipeline RAG con Ollama.
    Descomentar cuando Ollama esté disponible.
    """
    codigo_ejemplo = """
    # INTEGRACIÓN CON OLLAMA - PSEUDOCÓDIGO

    from langchain.llms import Ollama
    from langchain.prompts import PromptTemplate

    # Inicializar LLM local
    ollama = Ollama(model="mistral")  # u otro modelo disponible

    # En PipelineRAG._generar_respuesta():
    def _generar_respuesta(self, query: str, contexto: str) -> str:
        prompt = self._crear_prompt(query, contexto, [])
        respuesta = ollama(prompt)
        return respuesta

    # USO:
    pipeline = PipelineRAG(base_conocimiento)
    resultado = pipeline.procesar_query("¿Cuál es el precio?")
    print(resultado.respuesta)
    """
    return codigo_ejemplo


# ============================================================================
# DEMOSTRACIÓN
# ============================================================================

def demo_rag():
    """Demuestra el pipeline RAG completo"""

    print("=" * 80)
    print("DEMOSTRACIÓN: RAG (RETRIEVAL-AUGMENTED GENERATION)")
    print("=" * 80)

    # Crear base de conocimiento
    print("\n1. CONSTRUCCIÓN DE BASE DE CONOCIMIENTO")
    print("-" * 80)

    base = BaseConocimiento()

    # Agregar documentos
    documentos = [
        DocumentoFuente(
            id="doc_laptop_gaming",
            titulo="Especificaciones: Laptop Gaming RTX 4090",
            contenido="Laptop gamer de alta performance con GPU NVIDIA RTX 4090, "
                     "procesador Intel i9-13900HX, 32GB DDR5, SSD 2TB NVMe. "
                     "Pantalla 4K 144Hz, batería 86Wh. Precio: $3,500 USD. "
                     "Peso: 2.8kg. Garantía: 2 años.",
            fuente=TipoFuente.ARCHIVO,
            metadata={"categoria": "computadoras", "tipo": "laptop"}
        ),
        DocumentoFuente(
            id="doc_macbook",
            titulo="MacBook Pro M3 Max - Especificaciones",
            contenido="MacBook Pro 16 pulgadas con chip Apple M3 Max, 36GB RAM unificada, "
                     "512GB SSD. Pantalla Liquid Retina XDR, batería 100Wh dura hasta 18h. "
                     "Precio: $3,999 USD. Ideal para profesionales de video, audio e IA. "
                     "Peso: 2.15kg.",
            fuente=TipoFuente.ARCHIVO,
            metadata={"categoria": "computadoras", "tipo": "laptop"}
        ),
        DocumentoFuente(
            id="doc_soporte_tecnico",
            titulo="Guía de Soporte Técnico",
            contenido="Procedimientos de soporte para laptops: 1) Reinicia el equipo, "
                     "2) Actualiza drivers, 3) Verifica temperatura, 4) Contacta soporte si persiste. "
                     "Email soporte: support@tech.com. Teléfono: 1-800-TECH-HELP. "
                     "Horarios: Lun-Vie 9am-6pm PST.",
            fuente=TipoFuente.MANUAL,
            metadata={"categoria": "soporte"}
        ),
        DocumentoFuente(
            id="doc_comparacion",
            titulo="Comparativa: Gaming vs Productividad",
            contenido="Laptops gaming priorizan GPU y rendimiento gráfico, ideales para juegos. "
                     "Laptops de productividad optimizan CPU y RAM para tareas profesionales. "
                     "Gaming típicamente: RTX 4060+, 16GB+ RAM. Productividad: CPU de alto rendimiento, "
                     "16GB+ RAM. Duración batería: Gaming 3-5h, Productividad 8-18h.",
            fuente=TipoFuente.ARCHIVO,
            metadata={"categoria": "comparacion"}
        ),
    ]

    base.agregar_documentos_batch(documentos)
    print(f"Documentos agregados: {len(documentos)}")

    # Estadísticas
    stats = base.resumen_estadisticas()
    print(f"Estadísticas base de conocimiento:")
    for clave, valor in stats.items():
        print(f"  {clave}: {valor}")

    # Crear pipeline
    print("\n2. PROCESAMIENTO DE QUERIES ЧЕРЕЗ RAG")
    print("-" * 80)

    pipeline = PipelineRAG(base)

    # Procesar queries
    queries = [
        "¿Cuál es el precio de una laptop gaming con RTX 4090?",
        "¿Cómo contacto al soporte técnico?",
        "¿Qué laptop es mejor para desarrollo de software?",
    ]

    resultados = []
    for query in queries:
        resultado = pipeline.procesar_query(query, top_k_docs=2)
        resultados.append(resultado)

    # Mostrar resultados
    print("\n3. RESULTADOS DE CONSULTAS")
    print("-" * 80)

    for i, resultado in enumerate(resultados, 1):
        print(f"\n[Consulta {i}]")
        resumen = pipeline.obtener_resumen_consulta(resultado)

        print(f"  Pregunta: {resumen['consulta']}")
        print(f"  Documentos utilizados: {resumen['documentos_usados']}")
        for doc_info in resumen['documentos']:
            print(f"    - {doc_info['titulo']} (relevancia: {doc_info['relevancia']})")

        print(f"  Respuesta generada:")
        print(f"    {resultado.respuesta}")

    # Estadísticas finales
    print("\n4. ESTADÍSTICAS DEL PIPELINE")
    print("-" * 80)

    stats_pipeline = pipeline.obtener_estadisticas()
    for clave, valor in stats_pipeline.items():
        if isinstance(valor, float):
            print(f"  {clave}: {valor:.2f}")
        else:
            print(f"  {clave}: {valor}")

    # Mostrar información sobre integración con Ollama
    print("\n5. INTEGRACIÓN CON OLLAMA (PRODUCCIÓN)")
    print("-" * 80)
    print("Para usar con Ollama en producción:")
    print("""
  1. Instalar Ollama: https://ollama.ai
  2. Ejecutar: ollama serve
  3. En otra terminal: ollama pull mistral
  4. Descomentar integración en _generar_respuesta()
  5. Pasar prompt al modelo Ollama
    """)

    print("\n" + "=" * 80)
    print("Conclusión: RAG combina recuperación de información con generación")
    print("para respuestas fundamentadas, reduciendo alucinaciones del LLM")
    print("=" * 80)


if __name__ == "__main__":
    demo_rag()
