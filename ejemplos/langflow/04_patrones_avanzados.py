#!/usr/bin/env python3
"""
04_patrones_avanzados.py - Patrones Avanzados de Langflow

Demuestra patrones complejos:
- Routing condicional
- Fallbacks y retry
- Error handling
- Componentes personalizados
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_core.runnables import RunnableBranch
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ejemplo_1_conditional_routing():
    """Ejemplo 1: Routing condicional (elegir camino según entrada)"""
    print("=" * 60)
    print("EJEMPLO 1: Conditional Routing")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    # Rama técnica
    rama_tecnica = ChatPromptTemplate.from_template(
        "Eres experto en programación. Responde técnicamente: {pregunta}"
    ) | llm

    # Rama general
    rama_general = ChatPromptTemplate.from_template(
        "Eres asistente general. Responde simplemente: {pregunta}"
    ) | llm

    # Router: detecta si es técnica o general
    def detect_tecnica(x):
        palabras_tecnicas = ["código", "programación", "python", "javascript", "api", "database"]
        return any(word in x.get("pregunta", "").lower() for word in palabras_tecnicas)

    # Crear rama
    rama = RunnableBranch(
        (detect_tecnica, rama_tecnica),
        rama_general
    )

    # Test
    preguntas = [
        "¿Cómo escribo un código en Python?",
        "¿Cuál es tu película favorita?",
        "¿Cómo llamo una API en JavaScript?",
        "¿Qué es la amistad?"
    ]

    print(f"\n🔀 Routing de {len(preguntas)} preguntas:\n")

    for pregunta in preguntas:
        print(f"❓ {pregunta}")

        try:
            respuesta = rama.invoke({"pregunta": pregunta})
            tipo = "TÉCNICA" if detect_tecnica({"pregunta": pregunta}) else "GENERAL"
            print(f"   [{tipo}] {respuesta[:80]}...")
            logger.info(f"Routed as {tipo}: {pregunta}")

        except Exception as e:
            print(f"   ❌ Error: {e}")


def ejemplo_2_fallback_pattern():
    """Ejemplo 2: Fallback - usar alternativa si falla"""
    print("\n" + "=" * 60)
    print("EJEMPLO 2: Fallback Pattern")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    # Cadena principal (exigente)
    cadena_principal = ChatPromptTemplate.from_template(
        "Eres doctor especialista. Diagnostica esta enfermedad: {sintoma}"
    ) | llm

    # Cadena fallback (más general)
    cadena_fallback = ChatPromptTemplate.from_template(
        "Describe este síntoma: {sintoma}"
    ) | llm

    # Combinar con fallback
    cadena_segura = cadena_principal.with_fallbacks([cadena_fallback])

    sintomas = [
        "Dolor de cabeza persistente",
        "Fiebre alta",
        "Tos seca"
    ]

    print(f"\n🔄 Evaluando {len(sintomas)} síntomas con fallback:\n")

    for sintoma in sintomas:
        print(f"🏥 Síntoma: {sintoma}")

        try:
            # Intenta principal, si falla usa fallback
            respuesta = cadena_segura.invoke({"sintoma": sintoma})
            print(f"   ✅ {respuesta[:100]}...")

        except Exception as e:
            print(f"   ❌ Error incluso con fallback: {e}")


def ejemplo_3_error_handling():
    """Ejemplo 3: Manejo completo de errores"""
    print("\n" + "=" * 60)
    print("EJEMPLO 3: Error Handling")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    def invocar_seguro(pregunta):
        """Invocar con manejo completo de errores"""
        try:
            prompt = ChatPromptTemplate.from_template("Responde: {pregunta}")
            cadena = prompt | llm
            resultado = cadena.invoke({"pregunta": pregunta})
            logger.info(f"✅ Éxito: {pregunta}")
            return resultado

        except TimeoutError:
            logger.error("⏱️  Timeout - cadena tardó demasiado")
            return "Disculpa, el sistema tardó demasiado"

        except ValueError as e:
            logger.error(f"❌ Validación: {e}")
            return f"Input inválido: {str(e)}"

        except ConnectionError:
            logger.error("🔌 Sin conexión")
            return "No hay conexión con el servidor"

        except Exception as e:
            logger.critical(f"💥 Error inesperado: {e}")
            return "Error inesperado. Contacta soporte."

    # Test
    preguntas = [
        "¿Hola?",
        "Cuéntame un chiste",
        "¿Qué es la IA?"
    ]

    print(f"\n🛡️ Manejando {len(preguntas)} preguntas con error handling:\n")

    for pregunta in preguntas:
        print(f"❓ {pregunta}")
        respuesta = invocar_seguro(pregunta)
        print(f"   {respuesta[:100]}...\n")


def ejemplo_4_componente_personalizado():
    """Ejemplo 4: Componente personalizado (simulado)"""
    print("\n" + "=" * 60)
    print("EJEMPLO 4: Componente Personalizado")
    print("=" * 60)

    # Simulación de componente personalizado
    class ComponentePersonalizado:
        def __init__(self, nombre):
            self.nombre = nombre

        def procesar(self, entrada):
            """Lógica personalizada del componente"""
            if not entrada:
                raise ValueError("Entrada vacía")

            # Simulación de procesamiento
            procesado = {
                "entrada_original": entrada,
                "entrada_normalizada": entrada.lower().strip(),
                "longitud": len(entrada),
                "es_pregunta": entrada.endswith("?"),
                "es_comando": entrada.startswith("/")
            }
            return procesado

        def __call__(self, entrada):
            return self.procesar(entrada)

    # Usar componente
    comp = ComponentePersonalizado("MiComponente")

    entradas = [
        "¿Hola?",
        "Cuéntame un chiste",
        "/help",
        ""
    ]

    print(f"\n🔧 Procesando con componente personalizado:\n")

    for entrada in entradas:
        print(f"📥 Entrada: '{entrada}'")

        try:
            resultado = comp(entrada)
            print(f"   ✅ Procesado: {resultado}")
            logger.info(f"Componente procesó: {entrada}")

        except ValueError as e:
            print(f"   ❌ Error: {e}")


def ejemplo_5_composicion_compleja():
    """Ejemplo 5: Composición compleja de componentes"""
    print("\n" + "=" * 60)
    print("EJEMPLO 5: Composición Compleja")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    # Pipeline complejo
    def pipeline_completo(pregunta):
        """Pipeline: Validar → Clasificar → Responder → Formatear"""

        # 1. Validación
        if not pregunta or len(pregunta) < 3:
            return "❌ Pregunta muy corta"

        # 2. Clasificación
        es_tecnica = any(word in pregunta.lower() for word in ["código", "api", "programación"])
        tipo = "Técnica" if es_tecnica else "General"

        # 3. Respuesta
        try:
            prompt = ChatPromptTemplate.from_template(
                f"Como experto en {tipo.lower()}, responde: {{pregunta}}"
            )
            cadena = prompt | llm
            respuesta = cadena.invoke({"pregunta": pregunta})

            # 4. Formateo
            resultado_final = {
                "tipo": tipo,
                "pregunta": pregunta,
                "respuesta": respuesta[:100] + "...",
                "estado": "✅"
            }
            return resultado_final

        except Exception as e:
            return {
                "tipo": tipo,
                "pregunta": pregunta,
                "respuesta": str(e),
                "estado": "❌"
            }

    # Test
    preguntas = [
        "¿Cómo hago un código en Python?",
        "¿Cuál es tu música favorita?",
        "¿API REST?"
    ]

    print(f"\n🔀 Pipeline completo para {len(preguntas)} preguntas:\n")

    for pregunta in preguntas:
        resultado = pipeline_completo(pregunta)
        print(f"Pregunta: {resultado['pregunta']}")
        print(f"Tipo: {resultado['tipo']}")
        print(f"Respuesta: {resultado['respuesta']}")
        print(f"Estado: {resultado['estado']}\n")


def main():
    """Función principal"""
    try:
        ejemplo_1_conditional_routing()
        ejemplo_2_fallback_pattern()
        ejemplo_3_error_handling()
        ejemplo_4_componente_personalizado()
        ejemplo_5_composicion_compleja()

        print("=" * 60)
        print("✅ Todos los ejemplos avanzados completados")
        print("=" * 60)

    except Exception as e:
        logger.critical(f"Error fatal: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
