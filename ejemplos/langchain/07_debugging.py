#!/usr/bin/env python3
"""
07_debugging.py - Debugging, Logging y Testing

Demuestra:
- Verbose mode para ver el razonamiento
- Logging estructurado
- Testing de componentes
- Inspección de cadenas
"""

import logging
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
from langchain.agents import create_react_agent, AgentExecutor


# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============ EJEMPLOS ============

def ejemplo_verbose_mode():
    """Ver flujo detallado de agente"""
    print("=" * 60)
    print("EJEMPLO 1: Verbose Mode (Modo Detallado)")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    @tool
    def sumar(a: int, b: int) -> int:
        """Suma dos números"""
        return a + b

    @tool
    def multiplicar(a: int, b: int) -> int:
        """Multiplica dos números"""
        return a * b

    herramientas = [sumar, multiplicar]

    prompt = PromptTemplate.from_template("""
Tienes acceso a: {tools}

{format_instructions}

Pregunta: {{input}}""")

    try:
        agente = create_react_agent(llm, herramientas, prompt)

        # verbose=True muestra cada paso del razonamiento
        executor = AgentExecutor(
            agent=agente,
            tools=herramientas,
            verbose=True,  # Esto muestra Thought/Action/Observation
            max_iterations=5
        )

        print("\nEjecutando con verbose=True:")
        resultado = executor.invoke({"input": "¿Cuánto es 5 * 3?"})
        print(f"\nResultado final: {resultado['output']}\n")

    except Exception as e:
        logger.warning(f"Ejemplo verbose no completado (Ollama puede no estar activo): {e}")


def ejemplo_logging():
    """Logging estructurado"""
    print("=" * 60)
    print("EJEMPLO 2: Logging Estructurado")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")
    parser = StrOutputParser()

    template = "Responde brevemente: {pregunta}"
    prompt = PromptTemplate.from_template(template)
    cadena = prompt | llm | parser

    print("\nInvocando con logging...")
    logger.info("Iniciando cadena de QA")

    try:
        pregunta = "¿Qué es un LLM?"
        logger.debug(f"Input: {pregunta}")

        resultado = cadena.invoke({"pregunta": pregunta})

        logger.info(f"Éxito. Output length: {len(resultado)} caracteres")
        logger.debug(f"Output: {resultado[:100]}...")

        print(f"Respuesta: {resultado}\n")

    except Exception as e:
        logger.error(f"Error en cadena: {e}", exc_info=True)


def ejemplo_inspeccionar_cadena():
    """Inspeccionar estructura de una cadena"""
    print("=" * 60)
    print("EJEMPLO 3: Inspeccionar Cadena")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    template = "Pregunta: {pregunta}\nRespuesta:"
    prompt = PromptTemplate.from_template(template)
    cadena = prompt | llm

    print("\nInspección de la cadena:")

    # Ver esquema de entrada
    try:
        print("\n📥 Esquema de entrada:")
        print(f"  {cadena.input_schema}")
    except Exception:
        print("  (no disponible)")

    # Ver esquema de salida
    try:
        print("\n📤 Esquema de salida:")
        print(f"  {cadena.output_schema}")
    except Exception:
        print("  (no disponible)")

    # Ver el gráfico (si está disponible)
    try:
        print("\n🔗 Gráfico de la cadena:")
        # graph = cadena.get_graph()
        # print(f"  {graph}")
        print("  (disponible en visualizadores)")
    except Exception:
        print("  (no disponible)")

    print()


def ejemplo_testing_unitario():
    """Testing básico de componentes"""
    print("=" * 60)
    print("EJEMPLO 4: Testing Unitario")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    def test_llm_responde():
        """Test: LLM devuelve respuesta no vacía"""
        try:
            respuesta = llm.invoke("¿Hola?")
            assert respuesta is not None, "Respuesta es None"
            assert len(respuesta) > 0, "Respuesta está vacía"
            assert isinstance(respuesta, str), "Respuesta no es string"
            print("✅ test_llm_responde: PASÓ")
            return True
        except AssertionError as e:
            print(f"❌ test_llm_responde: FALLÓ - {e}")
            return False
        except Exception as e:
            print(f"⚠️  test_llm_responde: ERROR - {e}")
            return False

    def test_llm_razonable():
        """Test: Respuesta tiene longitud razonable"""
        try:
            respuesta = llm.invoke("¿Qué es Python?")
            assert len(respuesta) > 10, "Respuesta muy corta"
            assert len(respuesta) < 5000, "Respuesta muy larga"
            print("✅ test_llm_razonable: PASÓ")
            return True
        except AssertionError as e:
            print(f"❌ test_llm_razonable: FALLÓ - {e}")
            return False
        except Exception as e:
            print(f"⚠️  test_llm_razonable: ERROR - {e}")
            return False

    def test_prompt_template():
        """Test: Template funciona"""
        try:
            template = "Responde: {pregunta}"
            prompt = PromptTemplate.from_template(template)
            resultado = prompt.format(pregunta="¿Qué tal?")
            assert "¿Qué tal?" in resultado
            print("✅ test_prompt_template: PASÓ")
            return True
        except AssertionError as e:
            print(f"❌ test_prompt_template: FALLÓ - {e}")
            return False
        except Exception as e:
            print(f"⚠️  test_prompt_template: ERROR - {e}")
            return False

    print("\nEjecutando tests...")
    tests = [test_llm_responde, test_llm_razonable, test_prompt_template]

    resultados = [test() for test in tests]

    print(f"\n📊 Resultado: {sum(resultados)}/{len(resultados)} tests pasaron\n")


def ejemplo_error_handling():
    """Manejo de errores"""
    print("=" * 60)
    print("EJEMPLO 5: Error Handling")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    def invocar_seguro(prompt_text, timeout=None):
        """Invocar con manejo de errores"""
        try:
            # Cadena con timeout opcional
            cadena = llm
            if timeout:
                cadena = cadena.with_timeout(timeout)

            resultado = cadena.invoke(prompt_text)
            logger.info(f"Éxito: {len(resultado)} caracteres")
            return resultado

        except TimeoutError:
            logger.error("Timeout: La respuesta tardó demasiado")
            return "Disculpa, el sistema tardó demasiado."

        except ValueError as e:
            logger.error(f"Error de valor: {e}")
            return f"Error de entrada: {str(e)}"

        except Exception as e:
            logger.critical(f"Error inesperado: {e}", exc_info=True)
            return "Error inesperado. El equipo ha sido notificado."

    print("\n1️⃣  Invocación normal:")
    resultado = invocar_seguro("¿Qué es Python?")
    print(f"   {resultado[:80]}...\n")

    print("2️⃣  Con timeout (no debería fallar):")
    resultado = invocar_seguro("¿Qué es JavaScript?", timeout=30)
    print(f"   {resultado[:80]}...\n")


def ejemplo_comparar_respuestas():
    """Comparar respuestas de diferentes configuraciones"""
    print("=" * 60)
    print("EJEMPLO 6: Comparar Respuestas")
    print("=" * 60)

    from difflib import SequenceMatcher

    def similitud(texto1, texto2):
        """Calcula similitud entre textos"""
        return SequenceMatcher(None, texto1, texto2).ratio()

    # Dos configuraciones
    llm1 = Ollama(model="mistral", temperature=0.0)  # Determinista
    llm2 = Ollama(model="mistral", temperature=0.9)  # Creativo

    pregunta = "Dime un hecho sobre la Luna"

    try:
        print(f"\nPregunta: {pregunta}\n")

        resp1 = llm1.invoke(pregunta)
        print(f"Configuración 1 (temp=0.0):\n  {resp1[:100]}...")

        resp2 = llm2.invoke(pregunta)
        print(f"\nConfiguración 2 (temp=0.9):\n  {resp2[:100]}...")

        sim = similitud(resp1, resp2)
        print(f"\nSimilitud: {sim:.0%}\n")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    try:
        ejemplo_verbose_mode()
        ejemplo_logging()
        ejemplo_inspeccionar_cadena()
        ejemplo_testing_unitario()
        ejemplo_error_handling()
        ejemplo_comparar_respuestas()

        print("=" * 60)
        print("✅ Todos los ejemplos de debugging completados")
        print("=" * 60)

    except Exception as e:
        logger.critical(f"Error fatal: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
