"""03_TESTING_SUITE.PY - Suite de Tests con pytest/unittest"""

import pytest
import time
import random
from typing import List


class Agente:
    """Agente simple para testing"""
    def __init__(self, nombre: str = "agente_test"):
        self.nombre = nombre
        self.salud = 100
        self.energia = 100
        self.acciones = []

    def tomar_danio(self, danio: int) -> None:
        if not self._validar_danio(danio):
            raise ValueError("Daño inválido")
        self.salud = max(0, self.salud - danio)

    def _validar_danio(self, danio: int) -> bool:
        return 0 <= danio <= self.salud + 100

    def ejecutar_accion(self, accion: str) -> str:
        self.acciones.append(accion)
        if self.energia >= 10:
            self.energia -= 10
            return f"OK: {accion}"
        return "ERROR: Sin energía"

    def recuperarse(self) -> None:
        self.salud = min(100, self.salud + 20)
        self.energia = min(100, self.energia + 30)


# ============================================================================
# UNIT TESTS
# ============================================================================

class TestAgente:
    """Tests unitarios del agente"""

    @pytest.fixture
    def agente(self):
        """Fixture: crear agente limpio"""
        return Agente()

    def test_crear_agente(self, agente):
        """Test: crear agente"""
        assert agente.nombre == "agente_test"
        assert agente.salud == 100

    def test_tomar_danio(self, agente):
        """Test: tomar daño"""
        agente.tomar_danio(30)
        assert agente.salud == 70

    def test_danio_invalido(self, agente):
        """Test: daño inválido lanza error"""
        with pytest.raises(ValueError):
            agente.tomar_danio(-10)

    def test_ejecutar_accion(self, agente):
        """Test: ejecutar acción"""
        resultado = agente.ejecutar_accion("atacar")
        assert "OK" in resultado
        assert agente.energia == 90

    def test_sin_energia(self, agente):
        """Test: sin energía suficiente"""
        agente.energia = 5
        resultado = agente.ejecutar_accion("atacar")
        assert "ERROR" in resultado

    def test_recuperacion(self, agente):
        """Test: recuperación"""
        agente.salud = 50
        agente.energia = 30
        agente.recuperarse()
        assert agente.salud == 70
        assert agente.energia == 60


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegracion:
    """Tests de integración"""

    def test_batalla_simple(self):
        """Test: batalla entre dos agentes"""
        a1 = Agente("A")
        a2 = Agente("B")

        # Batalla
        a1.tomar_danio(30)
        a2.tomar_danio(50)

        # Ambos siguen vivos
        assert a1.salud > 0
        assert a2.salud > 0

    def test_flujo_completo(self):
        """Test: flujo completo agente"""
        agente = Agente()

        # Acciones
        agente.ejecutar_accion("explorar")
        agente.ejecutar_accion("combatir")
        agente.tomar_danio(25)
        agente.recuperarse()

        assert len(agente.acciones) == 2
        assert agente.salud >= 75


# ============================================================================
# FUNCTIONAL TESTS
# ============================================================================

class TestFuncional:
    """Tests funcionales"""

    def test_agente_sobrevive_batalla(self):
        """Test: agente sobrevive batalla típica"""
        agente = Agente()

        for _ in range(5):
            agente.tomar_danio(10)
            agente.recuperarse()

        assert agente.salud > 0

    def test_historial_acciones(self):
        """Test: historial de acciones se mantiene"""
        agente = Agente()

        acciones = ["atacar", "defender", "huir"]
        for acc in acciones:
            agente.ejecutar_accion(acc)

        assert agente.acciones == acciones


# ============================================================================
# STRESS TESTS
# ============================================================================

def test_stress_muchos_agentes():
    """Test: crear 1000 agentes"""
    agentes = [Agente(f"A{i}") for i in range(1000)]
    assert len(agentes) == 1000


def test_stress_muchas_acciones():
    """Test: 10000 acciones"""
    agente = Agente()

    inicio = time.time()
    for i in range(10000):
        if agente.energia > 10:
            agente.ejecutar_accion(f"accion_{i}")
        else:
            agente.recuperarse()
    duracion = time.time() - inicio

    # Debería ser rápido (< 1 segundo)
    assert duracion < 1.0
    assert len(agente.acciones) > 0


# ============================================================================
# EDGE CASES
# ============================================================================

def test_edge_salud_cero():
    """Test: salud exactamente 0"""
    agente = Agente()
    agente.tomar_danio(100)
    assert agente.salud == 0


def test_edge_energia_vacia():
    """Test: energía completamente vacía"""
    agente = Agente()
    agente.energia = 0
    resultado = agente.ejecutar_accion("atacar")
    assert "ERROR" in resultado


# ============================================================================
# EJECUCIÓN DE TESTS
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("SUITE DE TESTS")
    print("=" * 80)

    print("\nEjecutar con pytest:")
    print("  pytest 03_testing_suite.py -v")

    print("\nEjecutar con cobertura:")
    print("  pytest 03_testing_suite.py --cov=agente")

    print("\n" + "=" * 80)
    print("✓ Suite de tests lista")
    print("=" * 80)
