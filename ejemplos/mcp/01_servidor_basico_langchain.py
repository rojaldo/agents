"""
Ejemplo 1: Servidor MCP Básico con LangChain y Ollama

Este ejemplo demuestra cómo crear un servidor MCP que expone
herramientas de LangChain usando Ollama como modelo local.
"""

import json
import asyncio
from datetime import datetime
from typing import Dict, Any, List
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


class ServidorMCPLangChain:
    """
    Servidor MCP que integra LangChain con Ollama para proporcionar
    herramientas de procesamiento de lenguaje natural.
    """

    def __init__(self, modelo: str = "llama3.2"):
        """
        Inicializa el servidor MCP con un modelo de Ollama.

        Args:
            modelo: Nombre del modelo de Ollama a usar
        """
        self.nombre = "Servidor MCP LangChain"
        self.version = "1.0.0"
        self.modelo = modelo

        # Inicializar LLM de Ollama
        self.llm = OllamaLLM(model=modelo, temperature=0.7)

        # Registrar herramientas disponibles
        self.herramientas = {
            "generar_texto": self.generar_texto,
            "resumir_texto": self.resumir_texto,
            "analizar_sentimiento": self.analizar_sentimiento,
            "responder_pregunta": self.responder_pregunta
        }

        self.historial = []
        print(f"✓ Servidor MCP inicializado con modelo: {modelo}")

    def generar_texto(self, prompt: str, max_tokens: int = 200) -> Dict[str, Any]:
        """
        Genera texto basado en un prompt usando LangChain y Ollama.

        Args:
            prompt: El prompt para generar texto
            max_tokens: Número máximo de tokens a generar

        Returns:
            Diccionario con el texto generado y metadata
        """
        try:
            template = PromptTemplate(
                input_variables=["prompt"],
                template="{prompt}"
            )

            chain = LLMChain(llm=self.llm, prompt=template)
            resultado = chain.invoke({"prompt": prompt})

            respuesta = {
                "texto_generado": resultado["text"],
                "modelo": self.modelo,
                "timestamp": datetime.now().isoformat()
            }

            self._registrar_operacion("generar_texto", prompt, respuesta)
            return respuesta

        except Exception as e:
            return {"error": str(e)}

    def resumir_texto(self, texto: str) -> Dict[str, Any]:
        """
        Resume un texto usando LangChain y Ollama.

        Args:
            texto: El texto a resumir

        Returns:
            Diccionario con el resumen y metadata
        """
        try:
            template = PromptTemplate(
                input_variables=["texto"],
                template="""Resume el siguiente texto de manera concisa y clara:

Texto: {texto}

Resumen:"""
            )

            chain = LLMChain(llm=self.llm, prompt=template)
            resultado = chain.invoke({"texto": texto})

            respuesta = {
                "resumen": resultado["text"],
                "longitud_original": len(texto),
                "longitud_resumen": len(resultado["text"]),
                "timestamp": datetime.now().isoformat()
            }

            self._registrar_operacion("resumir_texto", texto[:100], respuesta)
            return respuesta

        except Exception as e:
            return {"error": str(e)}

    def analizar_sentimiento(self, texto: str) -> Dict[str, Any]:
        """
        Analiza el sentimiento de un texto.

        Args:
            texto: El texto a analizar

        Returns:
            Diccionario con el análisis de sentimiento
        """
        try:
            template = PromptTemplate(
                input_variables=["texto"],
                template="""Analiza el sentimiento del siguiente texto.
Responde SOLO con una palabra: POSITIVO, NEGATIVO o NEUTRAL.

Texto: {texto}

Sentimiento:"""
            )

            chain = LLMChain(llm=self.llm, prompt=template)
            resultado = chain.invoke({"texto": texto})

            sentimiento = resultado["text"].strip().upper()

            respuesta = {
                "sentimiento": sentimiento,
                "texto_analizado": texto,
                "timestamp": datetime.now().isoformat()
            }

            self._registrar_operacion("analizar_sentimiento", texto, respuesta)
            return respuesta

        except Exception as e:
            return {"error": str(e)}

    def responder_pregunta(self, pregunta: str, contexto: str = "") -> Dict[str, Any]:
        """
        Responde una pregunta, opcionalmente con contexto.

        Args:
            pregunta: La pregunta a responder
            contexto: Contexto adicional para la respuesta

        Returns:
            Diccionario con la respuesta
        """
        try:
            if contexto:
                template = PromptTemplate(
                    input_variables=["contexto", "pregunta"],
                    template="""Basándote en el siguiente contexto, responde la pregunta de manera clara y concisa.

Contexto: {contexto}

Pregunta: {pregunta}

Respuesta:"""
                )
                resultado = LLMChain(llm=self.llm, prompt=template).invoke({
                    "contexto": contexto,
                    "pregunta": pregunta
                })
            else:
                template = PromptTemplate(
                    input_variables=["pregunta"],
                    template="{pregunta}"
                )
                resultado = LLMChain(llm=self.llm, prompt=template).invoke({
                    "pregunta": pregunta
                })

            respuesta = {
                "respuesta": resultado["text"],
                "pregunta": pregunta,
                "con_contexto": bool(contexto),
                "timestamp": datetime.now().isoformat()
            }

            self._registrar_operacion("responder_pregunta", pregunta, respuesta)
            return respuesta

        except Exception as e:
            return {"error": str(e)}

    def _registrar_operacion(self, herramienta: str, entrada: str, salida: Any):
        """Registra una operación en el historial."""
        self.historial.append({
            "herramienta": herramienta,
            "entrada": entrada,
            "salida": salida,
            "timestamp": datetime.now().isoformat()
        })

    def obtener_historial(self) -> List[Dict[str, Any]]:
        """Obtiene el historial de operaciones."""
        return self.historial

    def listar_herramientas(self) -> List[str]:
        """Lista las herramientas disponibles."""
        return list(self.herramientas.keys())

    def obtener_info(self) -> Dict[str, Any]:
        """Obtiene información del servidor."""
        return {
            "nombre": self.nombre,
            "version": self.version,
            "modelo": self.modelo,
            "herramientas": self.listar_herramientas(),
            "total_operaciones": len(self.historial)
        }


# Ejemplo de uso
async def main():
    print("=" * 60)
    print("Servidor MCP con LangChain y Ollama")
    print("=" * 60)

    # Crear servidor
    servidor = ServidorMCPLangChain(modelo="llama3.2")

    # Mostrar información
    info = servidor.obtener_info()
    print(f"\n📋 Información del servidor:")
    print(json.dumps(info, indent=2, ensure_ascii=False))

    # Ejemplo 1: Generar texto
    print(f"\n{'='*60}")
    print("Ejemplo 1: Generar texto")
    print("="*60)
    resultado = servidor.generar_texto(
        "Escribe un párrafo corto sobre la inteligencia artificial"
    )
    print(f"Texto generado:\n{resultado['texto_generado']}")

    # Ejemplo 2: Resumir texto
    print(f"\n{'='*60}")
    print("Ejemplo 2: Resumir texto")
    print("="*60)
    texto_largo = """
    La inteligencia artificial es una rama de la informática que se centra en crear
    sistemas capaces de realizar tareas que normalmente requieren inteligencia humana.
    Esto incluye el aprendizaje automático, el procesamiento del lenguaje natural,
    el reconocimiento de patrones y la toma de decisiones. Los sistemas de IA modernos
    pueden analizar grandes cantidades de datos, aprender de ellos y mejorar su
    rendimiento con el tiempo sin ser explícitamente programados para cada tarea específica.
    """
    resultado = servidor.resumir_texto(texto_largo)
    print(f"Texto original ({resultado['longitud_original']} caracteres)")
    print(f"Resumen ({resultado['longitud_resumen']} caracteres):\n{resultado['resumen']}")

    # Ejemplo 3: Analizar sentimiento
    print(f"\n{'='*60}")
    print("Ejemplo 3: Analizar sentimiento")
    print("="*60)
    textos = [
        "¡Este producto es excelente! Estoy muy satisfecho con mi compra.",
        "El servicio fue terrible y el producto llegó dañado.",
        "El producto es aceptable, cumple con lo esperado."
    ]

    for texto in textos:
        resultado = servidor.analizar_sentimiento(texto)
        print(f"Texto: {texto}")
        print(f"Sentimiento: {resultado['sentimiento']}\n")

    # Ejemplo 4: Responder preguntas
    print(f"\n{'='*60}")
    print("Ejemplo 4: Responder preguntas")
    print("="*60)
    contexto = "Python es un lenguaje de programación de alto nivel conocido por su sintaxis clara y legible."
    pregunta = "¿Qué es Python?"

    resultado = servidor.responder_pregunta(pregunta, contexto)
    print(f"Pregunta: {pregunta}")
    print(f"Respuesta: {resultado['respuesta']}")

    # Mostrar historial
    print(f"\n{'='*60}")
    print("Historial de operaciones")
    print("="*60)
    historial = servidor.obtener_historial()
    print(f"Total de operaciones: {len(historial)}")

    for i, op in enumerate(historial, 1):
        print(f"\n{i}. {op['herramienta']} - {op['timestamp']}")


if __name__ == "__main__":
    asyncio.run(main())
