"""
MÓDULO 3: Testing de Agentes (Unit, Integration, Functional, Stress)
=====================================================================

Este módulo demuestra estrategias de testing para agentes IA.

Conceptos clave:
- Unit Testing: test componentes individuales
- Integration Testing: test múltiples componentes juntos
- Functional Testing: test desde perspectiva usuario (end-to-end)
- Stress Testing: test bajo carga extrema
- Regression Testing: asegurar que cambios no rompan nada

Ejemplo práctico: Testing de un agente Q&A con LLM
"""

import time
import random
from typing import List, Dict, Any, Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod


# ============================================================================
# TIPOS Y ESTRUCTURAS
# ============================================================================

@dataclass
class TestResult:
    """Resultado de una prueba"""
    nombre: str
    passed: bool
    mensaje: str = ""
    tiempo_ejecucion_ms: float = 0.0
    tipo: str = "unit"  # unit, integration, functional, stress


class TestSuite:
    """Suite de tests"""

    def __init__(self, nombre: str):
        self.nombre = nombre
        self.tests: List[Callable] = []
        self.resultados: List[TestResult] = []

    def agregar_test(self, test_func: Callable) -> None:
        """Agrega un test a la suite"""
        self.tests.append(test_func)

    def ejecutar(self) -> None:
        """Ejecuta todos los tests"""
        print(f"\n{'='*80}")
        print(f"EJECUTANDO SUITE: {self.nombre}")
        print(f"{'='*80}\n")

        for test_func in self.tests:
            inicio = time.time()
            try:
                # Ejecutar test (debe lanzar excepción si falla)
                test_func()
                tiempo_ms = (time.time() - inicio) * 1000

                resultado = TestResult(
                    nombre=test_func.__name__,
                    passed=True,
                    mensaje="OK",
                    tiempo_ejecucion_ms=tiempo_ms
                )
                print(f"✓ {test_func.__name__}: {tiempo_ms:.2f}ms")

            except AssertionError as e:
                tiempo_ms = (time.time() - inicio) * 1000
                resultado = TestResult(
                    nombre=test_func.__name__,
                    passed=False,
                    mensaje=str(e),
                    tiempo_ejecucion_ms=tiempo_ms
                )
                print(f"✗ {test_func.__name__}: FALLO - {str(e)}")

            except Exception as e:
                tiempo_ms = (time.time() - inicio) * 1000
                resultado = TestResult(
                    nombre=test_func.__name__,
                    passed=False,
                    mensaje=f"ERROR: {str(e)}",
                    tiempo_ejecucion_ms=tiempo_ms
                )
                print(f"✗ {test_func.__name__}: ERROR - {str(e)}")

            self.resultados.append(resultado)

        # Resumen
        self.imprimir_resumen()

    def imprimir_resumen(self) -> None:
        """Imprime resumen de resultados"""
        print(f"\n{'-'*80}")
        print("RESUMEN")
        print(f"{'-'*80}")

        total = len(self.resultados)
        pasados = sum(1 for r in self.resultados if r.passed)
        fallados = total - pasados

        print(f"Total tests: {total}")
        print(f"Pasados: {pasados} ✓")
        print(f"Fallados: {fallados} ✗")
        print(f"Success rate: {(pasados/total)*100:.1f}%")

        tiempo_total_ms = sum(r.tiempo_ejecucion_ms for r in self.resultados)
        print(f"Tiempo total: {tiempo_total_ms:.2f}ms")


# ============================================================================
# MOCK: AGENTE Q&A SIMPLE
# ============================================================================

class AgenteQA:
    """Agente simple de preguntas y respuestas"""

    def __init__(self):
        self.historial = []
        self.errores = 0

    def responder(self, pregunta: str) -> str:
        """Responde a una pregunta"""
        # Simular respuesta
        if not pregunta:
            raise ValueError("Pregunta vacía")

        if "error" in pregunta.lower():
            self.errores += 1
            raise Exception("Error procesando pregunta")

        respuesta = f"Respuesta a: {pregunta[:50]}"
        self.historial.append({"pregunta": pregunta, "respuesta": respuesta})
        return respuesta

    def reset(self):
        """Reinicia el agente"""
        self.historial = []
        self.errores = 0

    def obtener_historial(self) -> List[Dict]:
        """Obtiene historial de interacciones"""
        return self.historial


# ============================================================================
# UNIT TESTS
# ============================================================================

def test_agente_responde():
    """UT: Agente responde a pregunta válida"""
    agente = AgenteQA()
    respuesta = agente.responder("¿Cuál es 2+2?")
    assert respuesta is not None
    assert len(respuesta) > 0
    print("  [UT] Agente responde correctamente")


def test_agente_rechaza_entrada_vacia():
    """UT: Agente rechaza entrada vacía"""
    agente = AgenteQA()
    try:
        agente.responder("")
        assert False, "Debería haber lanzado excepción"
    except ValueError:
        print("  [UT] Agente rechaza entrada vacía")


def test_agente_registra_historial():
    """UT: Agente registra historial de preguntas"""
    agente = AgenteQA()
    agente.responder("Pregunta 1")
    agente.responder("Pregunta 2")

    historial = agente.obtener_historial()
    assert len(historial) == 2
    assert historial[0]["pregunta"] == "Pregunta 1"
    print("  [UT] Agente registra historial")


def test_agente_reset():
    """UT: Agente se reinicia correctamente"""
    agente = AgenteQA()
    agente.responder("Pregunta 1")
    agente.reset()

    historial = agente.obtener_historial()
    assert len(historial) == 0
    print("  [UT] Agente se reinicia")


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

def test_agente_multiples_preguntas():
    """IT: Agente maneja múltiples preguntas en secuencia"""
    agente = AgenteQA()

    preguntas = [
        "¿Cuál es la capital de Francia?",
        "¿Cuánto es 2+2?",
        "¿Quién escribió Don Quijote?"
    ]

    for pregunta in preguntas:
        respuesta = agente.responder(pregunta)
        assert respuesta is not None

    assert len(agente.obtener_historial()) == len(preguntas)
    print("  [IT] Agente maneja múltiples preguntas")


def test_agente_manejo_errores():
    """IT: Agente maneja errores sin fallar completamente"""
    agente = AgenteQA()

    try:
        agente.responder("Pregunta normal")
        agente.responder("pregunta con error")  # Activará error
    except Exception:
        pass

    # Agente sigue funcionando
    respuesta = agente.responder("Otra pregunta")
    assert respuesta is not None
    print("  [IT] Agente maneja errores")


# ============================================================================
# FUNCTIONAL TESTS
# ============================================================================

def test_caso_uso_basico():
    """FT: Caso de uso básico: usuario hace preguntas y recibe respuestas"""
    agente = AgenteQA()

    # Simulación de flujo de usuario
    preguntas_usuario = [
        "¿Dónde está el Museo del Prado?",
        "¿Qué es la fotosíntesis?",
        "¿Cuándo se escribió La Odisea?"
    ]

    respuestas = []
    for pregunta in preguntas_usuario:
        respuesta = agente.responder(pregunta)
        respuestas.append(respuesta)
        assert respuesta is not None, f"No se obtuvo respuesta para: {pregunta}"

    assert len(respuestas) == len(preguntas_usuario)
    print("  [FT] Caso de uso básico completado")


def test_sesion_completa():
    """FT: Sesión completa del agente"""
    agente = AgenteQA()

    # Inicializar sesión
    assert len(agente.obtener_historial()) == 0

    # Hacer preguntas
    for i in range(5):
        agente.responder(f"Pregunta {i+1}")

    # Verificar estado
    assert len(agente.obtener_historial()) == 5

    # Limpiar
    agente.reset()
    assert len(agente.obtener_historial()) == 0

    print("  [FT] Sesión completa correcta")


# ============================================================================
# STRESS TESTS
# ============================================================================

def test_stress_muchas_preguntas():
    """ST: Agente bajo estrés con muchas preguntas"""
    agente = AgenteQA()

    num_preguntas = 1000
    inicio = time.time()

    for i in range(num_preguntas):
        agente.responder(f"Pregunta {i}")

    tiempo_total_ms = (time.time() - inicio) * 1000
    latencia_promedio_ms = tiempo_total_ms / num_preguntas

    assert latencia_promedio_ms < 100, f"Latencia demasiado alta: {latencia_promedio_ms}ms"
    print(f"  [ST] Procesadas {num_preguntas} preguntas en {tiempo_total_ms:.2f}ms")
    print(f"       Latencia promedio: {latencia_promedio_ms:.2f}ms")


def test_stress_memoria():
    """ST: Agente bajo estrés de memoria"""
    agente = AgenteQA()

    # Generar muchas preguntas largas
    preguntas_largas = [
        "Esta es una pregunta muy larga " * 100 for _ in range(100)
    ]

    for pregunta in preguntas_largas:
        try:
            agente.responder(pregunta)
        except MemoryError:
            assert False, "Agente falló por memoria"

    assert len(agente.obtener_historial()) == len(preguntas_largas)
    print(f"  [ST] Procesadas {len(preguntas_largas)} preguntas largas")


def test_stress_concurrencia_simulada():
    """ST: Simular múltiples usuarios simultáneamente"""
    num_usuarios = 50
    preguntas_por_usuario = 20

    agentes = [AgenteQA() for _ in range(num_usuarios)]
    inicio = time.time()

    for agente in agentes:
        for i in range(preguntas_por_usuario):
            agente.responder(f"Pregunta {i}")

    tiempo_total_ms = (time.time() - inicio) * 1000
    total_preguntas = num_usuarios * preguntas_por_usuario

    print(f"  [ST] {num_usuarios} usuarios × {preguntas_por_usuario} preguntas")
    print(f"       Total: {total_preguntas} en {tiempo_total_ms:.2f}ms")


# ============================================================================
# DEMOSTRACIÓN
# ============================================================================

def ejecutar_tests():
    """Ejecuta toda la suite de tests"""

    print("=" * 80)
    print("TESTING DE AGENTES - SUITE COMPLETA")
    print("=" * 80)

    # Suite de Unit Tests
    suite_unit = TestSuite("Unit Tests")
    suite_unit.agregar_test(test_agente_responde)
    suite_unit.agregar_test(test_agente_rechaza_entrada_vacia)
    suite_unit.agregar_test(test_agente_registra_historial)
    suite_unit.agregar_test(test_agente_reset)
    suite_unit.ejecutar()

    # Suite de Integration Tests
    suite_integration = TestSuite("Integration Tests")
    suite_integration.agregar_test(test_agente_multiples_preguntas)
    suite_integration.agregar_test(test_agente_manejo_errores)
    suite_integration.ejecutar()

    # Suite de Functional Tests
    suite_functional = TestSuite("Functional Tests")
    suite_functional.agregar_test(test_caso_uso_basico)
    suite_functional.agregar_test(test_sesion_completa)
    suite_functional.ejecutar()

    # Suite de Stress Tests
    suite_stress = TestSuite("Stress Tests")
    suite_stress.agregar_test(test_stress_muchas_preguntas)
    suite_stress.agregar_test(test_stress_memoria)
    suite_stress.agregar_test(test_stress_concurrencia_simulada)
    suite_stress.ejecutar()

    # Resumen general
    print("\n" + "=" * 80)
    print("RESUMEN GENERAL")
    print("=" * 80)

    all_results = (suite_unit.resultados + suite_integration.resultados +
                   suite_functional.resultados + suite_stress.resultados)

    total = len(all_results)
    pasados = sum(1 for r in all_results if r.passed)
    fallados = total - pasados

    print(f"Total tests: {total}")
    print(f"Pasados: {pasados} ✓")
    print(f"Fallados: {fallados} ✗")
    print(f"Success rate: {(pasados/total)*100:.1f}%")


if __name__ == "__main__":
    ejecutar_tests()
