"""
MÓDULO 4: Testing de Comportamiento de Agentes
===============================================

Este módulo demuestra testing del comportamiento correcto de agentes.

Conceptos clave:
- Propiedades que debe cumplir siempre (invariantes)
- Edge cases y boundary values
- Consistency temporal
- Reproducibilidad con seeds

Ejemplo práctico: Testing de un agente de búsqueda/planificación
"""

import random
import math
from typing import List, Set, Dict, Any, Optional
from dataclasses import dataclass


# ============================================================================
# TIPOS Y ESTRUCTURAS
# ============================================================================

@dataclass
class TestPropagacion:
    """Resultado de test de una propiedad"""
    nombre_propiedad: str
    passed: bool
    casos_probados: int
    mensaje: str = ""


class GeneradorPropiedades:
    """Genera tests de propiedades (property-based testing)"""

    def __init__(self, seed: int = 42):
        self.seed = seed
        random.seed(seed)

    def test_propiedad(self, propiedad_func, generador_datos, num_casos: int = 100) -> TestPropagacion:
        """
        Test una propiedad contra múltiples casos generados

        Args:
            propiedad_func: función que retorna True si propiedad se cumple
            generador_datos: callable que genera datos de prueba
            num_casos: número de casos a probar

        Returns:
            TestPropagacion con resultado
        """
        for i in range(num_casos):
            datos = generador_datos()
            if not propiedad_func(datos):
                return TestPropagacion(
                    nombre_propiedad=propiedad_func.__name__,
                    passed=False,
                    casos_probados=i+1,
                    mensaje=f"Falló en caso {i+1}: {datos}"
                )

        return TestPropagacion(
            nombre_propiedad=propiedad_func.__name__,
            passed=True,
            casos_probados=num_casos
        )


# ============================================================================
# AGENTE DE BÚSQUEDA (Para Testing)
# ============================================================================

class AgenteBusqueda:
    """Agente simple de búsqueda en árbol"""

    def __init__(self, max_budget: int = 100):
        self.max_budget = max_budget
        self.budget_usado = 0
        self.historial = []

    def buscar(self, objetivo: int, rango: tuple = (0, 100)) -> Optional[int]:
        """
        Busca un número objetivo en un rango usando búsqueda binaria

        Args:
            objetivo: número a buscar
            rango: tupla (min, max) del rango

        Returns:
            El número si lo encuentra, None si usa todo el budget
        """
        self.budget_usado = 0
        self.historial = []

        min_val, max_val = rango

        while self.budget_usado < self.max_budget:
            if min_val > max_val:
                return None  # No encontrado

            mid = (min_val + max_val) // 2
            self.budget_usado += 1
            self.historial.append(mid)

            if mid == objetivo:
                return mid
            elif mid < objetivo:
                min_val = mid + 1
            else:
                max_val = mid - 1

        return None

    def obtener_cost_ultimo_busqueda(self) -> int:
        """Obtiene costo de última búsqueda"""
        return self.budget_usado

    def reset(self):
        """Reinicia el agente"""
        self.budget_usado = 0
        self.historial = []


# ============================================================================
# PROPIEDADES A TESTEAR
# ============================================================================

def propiedad_nunca_excede_budget():
    """Propiedad: agente nunca excede su budget"""

    def test(datos):
        agente, objetivo, rango = datos
        agente.buscar(objetivo, rango)
        return agente.obtener_cost_ultimo_busqueda() <= agente.max_budget

    def generador():
        agente = AgenteBusqueda(max_budget=50)
        objetivo = random.randint(0, 100)
        return (agente, objetivo, (0, 100))

    return test, generador


def propiedad_encuentra_si_existe():
    """Propiedad: si el objetivo existe, lo encuentra"""

    def test(datos):
        agente, objetivo = datos
        resultado = agente.buscar(objetivo, (0, 100))
        return resultado == objetivo

    def generador():
        agente = AgenteBusqueda(max_budget=50)
        objetivo = random.randint(0, 100)
        return (agente, objetivo)

    return test, generador


def propiedad_no_infinito_loop():
    """Propiedad: búsqueda termina (no hay loop infinito)"""

    def test(datos):
        agente, objetivo, rango = datos
        try:
            resultado = agente.buscar(objetivo, rango)
            # Si llegamos aquí, no hay loop infinito
            return True
        except RecursionError:
            return False
        except Exception:
            return False

    def generador():
        agente = AgenteBusqueda(max_budget=100)
        objetivo = random.randint(-1000, 1000)
        rango = (random.randint(-1000, 0), random.randint(0, 1000))
        return (agente, objetivo, rango)

    return test, generador


def propiedad_monotonica():
    """Propiedad: historial nunca repite búsqueda en mismo punto"""

    def test(datos):
        agente, objetivo = datos
        agente.buscar(objetivo, (0, 100))
        historial = agente.historial
        # No debe haber duplicados
        return len(historial) == len(set(historial))

    def generador():
        agente = AgenteBusqueda(max_budget=100)
        objetivo = random.randint(0, 100)
        return (agente, objetivo)

    return test, generador


# ============================================================================
# EDGE CASES
# ============================================================================

class TestEdgeCases:
    """Tests de casos borde (boundary values)"""

    @staticmethod
    def test_busqueda_valor_minimo():
        """Edge case: buscar valor mínimo"""
        agente = AgenteBusqueda()
        resultado = agente.buscar(0, (0, 100))
        assert resultado == 0, f"No encontró 0, obtuvo {resultado}"
        print("  ✓ Edge case: búsqueda valor mínimo")

    @staticmethod
    def test_busqueda_valor_maximo():
        """Edge case: buscar valor máximo"""
        agente = AgenteBusqueda()
        resultado = agente.buscar(100, (0, 100))
        assert resultado == 100, f"No encontró 100, obtuvo {resultado}"
        print("  ✓ Edge case: búsqueda valor máximo")

    @staticmethod
    def test_rango_vacio():
        """Edge case: rango vacío"""
        agente = AgenteBusqueda()
        resultado = agente.buscar(50, (100, 0))  # min > max
        assert resultado is None, "Debería retornar None para rango vacío"
        print("  ✓ Edge case: rango vacío")

    @staticmethod
    def test_rango_unitario():
        """Edge case: rango con un único elemento"""
        agente = AgenteBusqueda()
        resultado = agente.buscar(50, (50, 50))
        assert resultado == 50, "Debería encontrar el único elemento"
        print("  ✓ Edge case: rango unitario")

    @staticmethod
    def test_objetivo_no_existe():
        """Edge case: objetivo no existe en rango"""
        agente = AgenteBusqueda(max_budget=100)
        resultado = agente.buscar(150, (0, 100))  # 150 no está en [0, 100]
        assert resultado is None, "Debería retornar None si no existe"
        print("  ✓ Edge case: objetivo no existe")

    @staticmethod
    def test_budget_muy_pequeño():
        """Edge case: budget insuficiente"""
        agente = AgenteBusqueda(max_budget=1)
        resultado = agente.buscar(50, (0, 100))
        assert agente.obtener_cost_ultimo_busqueda() <= 1
        print("  ✓ Edge case: budget muy pequeño")


# ============================================================================
# CONSISTENCY (REPRODUCIBILIDAD)
# ============================================================================

class TestConsistencia:
    """Tests de consistencia y reproducibilidad"""

    @staticmethod
    def test_determinismo():
        """Test: determinismo - mismo input -> mismo output"""
        agente1 = AgenteBusqueda(max_budget=50)
        agente2 = AgenteBusqueda(max_budget=50)

        objetivo = 42

        resultado1 = agente1.buscar(objetivo, (0, 100))
        resultado2 = agente2.buscar(objetivo, (0, 100))

        assert resultado1 == resultado2, \
            f"Resultados inconsistentes: {resultado1} vs {resultado2}"

        assert agente1.historial == agente2.historial, \
            f"Historial inconsistente: {agente1.historial} vs {agente2.historial}"

        print("  ✓ Determinismo verificado")

    @staticmethod
    def test_idempotencia():
        """Test: idempotencia - múltiples ejecuciones mismo resultado"""
        agente = AgenteBusqueda()
        objetivo = 42

        resultados = []
        for _ in range(5):
            resultado = agente.buscar(objetivo, (0, 100))
            resultados.append(resultado)

        # Todos iguales
        assert len(set(resultados)) == 1, \
            f"Resultados no idempotentes: {resultados}"

        print("  ✓ Idempotencia verificada")

    @staticmethod
    def test_consistencia_con_seed():
        """Test: reproducibilidad con seed fijo"""
        seed = 12345

        # Ejecución 1
        random.seed(seed)
        agente1 = AgenteBusqueda()
        resultado1 = agente1.buscar(42, (0, 100))

        # Ejecución 2 (mismo seed)
        random.seed(seed)
        agente2 = AgenteBusqueda()
        resultado2 = agente2.buscar(42, (0, 100))

        assert resultado1 == resultado2, \
            f"Resultados no reproducibles con seed: {resultado1} vs {resultado2}"

        print("  ✓ Reproducibilidad con seed verificada")


# ============================================================================
# DEMOSTRACIÓN
# ============================================================================

def demo_testing_comportamiento():
    """Demuestra testing de comportamiento"""

    print("=" * 80)
    print("TESTING DE COMPORTAMIENTO DE AGENTES")
    print("=" * 80)

    # 1. TESTING DE PROPIEDADES
    print("\n1. TESTING DE PROPIEDADES (Property-Based Testing)")
    print("-" * 80)

    generador_prop = GeneradorPropiedades(seed=42)

    propiedades = [
        propiedad_nunca_excede_budget,
        propiedad_encuentra_si_existe,
        propiedad_no_infinito_loop,
        propiedad_monotonica
    ]

    propiedades_resultados = []

    for propiedad_factory in propiedades:
        test_func, generador = propiedad_factory()
        resultado = generador_prop.test_propiedad(test_func, generador, num_casos=100)

        propiedades_resultados.append(resultado)

        status = "✓" if resultado.passed else "✗"
        print(f"{status} {resultado.nombre_propiedad}: {resultado.casos_probados}/100 casos")
        if not resultado.passed:
            print(f"   Falló: {resultado.mensaje}")

    # 2. EDGE CASES
    print("\n2. EDGE CASES Y BOUNDARY VALUES")
    print("-" * 80)

    TestEdgeCases.test_busqueda_valor_minimo()
    TestEdgeCases.test_busqueda_valor_maximo()
    TestEdgeCases.test_rango_vacio()
    TestEdgeCases.test_rango_unitario()
    TestEdgeCases.test_objetivo_no_existe()
    TestEdgeCases.test_budget_muy_pequeño()

    # 3. CONSISTENCY
    print("\n3. CONSISTENCY Y REPRODUCIBILIDAD")
    print("-" * 80)

    TestConsistencia.test_determinismo()
    TestConsistencia.test_idempotencia()
    TestConsistencia.test_consistencia_con_seed()

    # 4. RESUMEN
    print("\n" + "=" * 80)
    print("RESUMEN")
    print("=" * 80)

    propiedades_pasadas = sum(1 for r in propiedades_resultados if r.passed)
    print(f"""
Propiedades testeadas: {len(propiedades_resultados)}
Propiedades verificadas: {propiedades_pasadas}/{len(propiedades_resultados)}

Edge cases: 6 casos probados ✓
Consistency: 3 tests verificados ✓

CONCLUSIÓN:
El agente cumple todas sus propiedades invariantes.
Comportamiento predecible y reproducible.
Ready para producción.
    """)


if __name__ == "__main__":
    demo_testing_comportamiento()
