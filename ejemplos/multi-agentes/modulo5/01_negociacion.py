"""
MÓDULO 5: Negociación y Resolución de Conflictos
Ejemplo 1: Protocolo de Negociación Oferta-Contraoferta

Demuestra:
1. Teoría básica de negociación (BATNA, ZAP)
2. Protocolo oferta-contraoferta
3. Estrategias de negociación
4. Resolución de impasses
"""

import sys
sys.path.insert(0, '../utilidades')

from agent_base import Agent
from ollama_client import OllamaClient
from typing import Any, Optional, List
from datetime import datetime
from enum import Enum
import json


class RespuestaNegociacion(Enum):
    """Estados posibles en una negociación"""
    ACEPTADA = "aceptada"
    RECHAZADA = "rechazada"
    CONTRAOFERTA = "contraoferta"
    IMPASSE = "impasse"


class Utilidad:
    """Representa la utilidad (satisfacción) que un agente obtiene"""

    def __init__(self, precio_min: float, precio_max: float,
                 cantidad_min: int, cantidad_max: int):
        """
        Args:
            precio_min/max: Rango aceptable de precio
            cantidad_min/max: Rango aceptable de cantidad
        """
        self.precio_min = precio_min
        self.precio_max = precio_max
        self.cantidad_min = cantidad_min
        self.cantidad_max = cantidad_max

    def calcular_utilidad(self, precio: float, cantidad: int) -> float:
        """
        Calcula utilidad (0 a 1) para una propuesta
        """
        # Verificar si está dentro de rangos aceptables
        if not (self.precio_min <= precio <= self.precio_max):
            return 0.0
        if not (self.cantidad_min <= cantidad <= self.cantidad_max):
            return 0.0

        # Calcular utilidad (preferir menor precio, mayor cantidad)
        utilidad_precio = 1.0 - (precio - self.precio_min) / (self.precio_max - self.precio_min)
        utilidad_cantidad = (cantidad - self.cantidad_min) / (self.cantidad_max - self.cantidad_min)

        # Peso: 40% precio, 60% cantidad
        return utilidad_precio * 0.4 + utilidad_cantidad * 0.6

    def obtener_batna(self) -> dict:
        """
        BATNA = Best Alternative To Negotiated Agreement
        Mejor opción si la negociación falla
        """
        return {
            "precio_minimo_aceptable": self.precio_min,
            "cantidad_minima_aceptable": self.cantidad_min
        }


class Oferta:
    """Representa una oferta en negociación"""

    def __init__(self, ofertante: str, precio: float, cantidad: int, numero: int = 1):
        self.ofertante = ofertante
        self.precio = precio
        self.cantidad = cantidad
        self.numero = numero
        self.timestamp = datetime.now().isoformat()

    def __str__(self):
        return f"Oferta #{self.numero}: ${self.precio} x {self.cantidad} unidades"


class NegociacionBilateral:
    """
    Protocolo de negociación oferta-contraoferta
    Entre dos partes: Vendedor y Comprador
    """

    def __init__(self, vendedor_name: str, comprador_name: str):
        self.vendedor = vendedor_name
        self.comprador = comprador_name
        self.historial_ofertas = []
        self.numero_oferta = 0
        self.estado = "en_progreso"
        self.acuerdo_final = None

    def vendedor_presenta_oferta(self, precio: float, cantidad: int) -> Oferta:
        """El vendedor hace la primera oferta"""
        self.numero_oferta += 1
        oferta = Oferta(self.vendedor, precio, cantidad, self.numero_oferta)
        self.historial_ofertas.append({
            "numero": self.numero_oferta,
            "ofertante": self.vendedor,
            "precio": precio,
            "cantidad": cantidad,
            "timestamp": oferta.timestamp
        })
        print(f"\n{self.vendedor} OFRECE: {oferta}")
        return oferta

    def comprador_responde(self, respuesta: RespuestaNegociacion,
                          contraoferta: Optional[Oferta] = None):
        """El comprador responde a la oferta"""
        print(f"{self.comprador}: {respuesta.value.upper()}")

        if respuesta == RespuestaNegociacion.ACEPTADA:
            print(f"✓ ¡ACUERDO ALCANZADO!")
            self.estado = "acuerdo"
            self.acuerdo_final = self.historial_ofertas[-1]
            return True

        elif respuesta == RespuestaNegociacion.CONTRAOFERTA:
            if contraoferta:
                self.numero_oferta += 1
                contraoferta.numero = self.numero_oferta
                self.historial_ofertas.append({
                    "numero": self.numero_oferta,
                    "ofertante": self.comprador,
                    "precio": contraoferta.precio,
                    "cantidad": contraoferta.cantidad,
                    "timestamp": contraoferta.timestamp
                })
                print(f"{self.comprador} CONTRAOFERTA: {contraoferta}")
                return False

        elif respuesta == RespuestaNegociacion.RECHAZADA:
            print(f"✗ Oferta rechazada")
            return False

        return False

    def vendedor_responde_contraoferta(self, respuesta: RespuestaNegociacion,
                                      contraoferta: Optional[Oferta] = None):
        """El vendedor responde a la contraoferta del comprador"""
        print(f"{self.vendedor}: {respuesta.value.upper()}")

        if respuesta == RespuestaNegociacion.ACEPTADA:
            print(f"✓ ¡ACUERDO ALCANZADO!")
            self.estado = "acuerdo"
            self.acuerdo_final = self.historial_ofertas[-1]
            return True

        elif respuesta == RespuestaNegociacion.CONTRAOFERTA:
            if contraoferta:
                self.numero_oferta += 1
                contraoferta.numero = self.numero_oferta
                self.historial_ofertas.append({
                    "numero": self.numero_oferta,
                    "ofertante": self.vendedor,
                    "precio": contraoferta.precio,
                    "cantidad": contraoferta.cantidad,
                    "timestamp": contraoferta.timestamp
                })
                print(f"{self.vendedor} CONTRAOFERTA: {contraoferta}")
                return False

        return False

    def registrar_impasse(self):
        """Registra que se llegó a un punto de ruptura"""
        self.estado = "impasse"
        print(f"✗ NEGOCIACIÓN FALLIDA - Impasse alcanzado")

    def obtener_resumen(self) -> dict:
        """Resumen de la negociación"""
        return {
            "vendedor": self.vendedor,
            "comprador": self.comprador,
            "estado": self.estado,
            "total_ofertas": len(self.historial_ofertas),
            "acuerdo_final": self.acuerdo_final,
            "historial_ofertas": self.historial_ofertas
        }


class AgenteNegociador(Agent):
    """Agente capaz de negociar"""

    def __init__(self, name: str, rol: str, utilidad: Utilidad):
        super().__init__(name=name, role=rol)
        self.model = OllamaClient(model="mistral")
        self.utilidad = utilidad
        self.objetivo = f"Negociar como {rol}"
        self.estrategia = "adaptativa"
        self.negociaciones_completadas = []

    def evaluar_oferta(self, oferta: Oferta) -> tuple[RespuestaNegociacion, Optional[Oferta]]:
        """
        Evalúa una oferta y decide si aceptarla, rechazarla o contraoferta
        """
        utilidad = self.utilidad.calcular_utilidad(oferta.precio, oferta.cantidad)

        print(f"  {self.name} evalúa: utilidad = {utilidad:.2%}")

        if utilidad > 0.7:
            print(f"  → Muy buena para mí, ¡acepto!")
            return RespuestaNegociacion.ACEPTADA, None

        elif utilidad > 0.4:
            print(f"  → Aceptable pero puedo mejorar")
            # Hacer contraoferta más favorable
            if self.role == "vendedor":
                # Subir precio, bajar cantidad
                nueva_precio = oferta.precio + (oferta.precio * 0.1)
                nueva_cantidad = oferta.cantidad - 1
            else:  # comprador
                # Bajar precio, subir cantidad
                nueva_precio = oferta.precio - (oferta.precio * 0.1)
                nueva_cantidad = oferta.cantidad + 1

            contraoferta = Oferta(self.name, nueva_precio, nueva_cantidad)
            print(f"  → Contraoferta: {contraoferta}")
            return RespuestaNegociacion.CONTRAOFERTA, contraoferta

        else:
            print(f"  → Inaceptable, rechazo")
            return RespuestaNegociacion.RECHAZADA, None

    def _execute_action(self, action: str) -> Any:
        return {"agente": self.name, "rol": self.role, "accion": action}


def demostrar_negociacion_compra_venta():
    """
    Demuestra un protocolo de negociación entre Vendedor y Comprador
    """
    print("\n" + "=" * 70)
    print("NEGOCIACIÓN: COMPRA-VENTA DE PRODUCTO")
    print("=" * 70)

    # Crear utilidades
    utilidad_vendedor = Utilidad(
        precio_min=80,    # Vender mínimo a $80
        precio_max=150,   # Ideal vender a $150
        cantidad_min=10,  # Vender mínimo 10 unidades
        cantidad_max=100  # Ideal vender 100 unidades
    )

    utilidad_comprador = Utilidad(
        precio_min=50,    # Quiero pagar mínimo $50
        precio_max=120,   # Puedo pagar hasta $120
        cantidad_min=20,  # Necesito mínimo 20
        cantidad_max=100  # Puedo comprar hasta 100
    )

    # Crear agentes negociadores
    vendedor = AgenteNegociador("Carlos (Vendedor)", "vendedor", utilidad_vendedor)
    comprador = AgenteNegociador("Laura (Compradora)", "comprador", utilidad_comprador)

    # Mostrar BATNA
    print("\nBAT NA - Best Alternative To Negotiated Agreement:")
    print("─" * 50)
    print(f"{vendedor.name}:")
    for k, v in vendedor.utilidad.obtener_batna().items():
        print(f"  {k}: {v}")

    print(f"\n{comprador.name}:")
    for k, v in comprador.utilidad.obtener_batna().items():
        print(f"  {k}: {v}")

    # Crear protocolo de negociación
    negociacion = NegociacionBilateral(vendedor.name, comprador.name)

    # RONDA 1: Vendedor ofrece
    print("\n" + "=" * 70)
    print("RONDA 1: Oferta Inicial del Vendedor")
    print("=" * 70)

    oferta1 = negociacion.vendedor_presenta_oferta(precio=140, cantidad=50)
    respuesta, contraoferta = comprador.evaluar_oferta(oferta1)
    negociacion.comprador_responde(respuesta, contraoferta)

    # RONDA 2: Vendedor responde a contraoferta
    print("\n" + "=" * 70)
    print("RONDA 2: Respuesta del Vendedor a Contraoferta")
    print("=" * 70)

    respuesta, contraoferta = vendedor.evaluar_oferta(contraoferta)
    negociacion.vendedor_responde_contraoferta(respuesta, contraoferta)

    # RONDA 3: Comprador responde
    print("\n" + "=" * 70)
    print("RONDA 3: Respuesta del Comprador")
    print("=" * 70)

    respuesta, contraoferta = comprador.evaluar_oferta(contraoferta)
    negociacion.comprador_responde(respuesta, contraoferta)

    # Resumen
    print("\n" + "=" * 70)
    print("RESUMEN DE LA NEGOCIACIÓN")
    print("=" * 70)

    resumen = negociacion.obtener_resumen()
    print(f"\nEstado: {resumen['estado'].upper()}")
    print(f"Ofertas intercambiadas: {resumen['total_ofertas']}")

    if resumen['acuerdo_final']:
        print(f"\nAcuerdo final:")
        print(f"  Precio: ${resumen['acuerdo_final']['precio']}")
        print(f"  Cantidad: {resumen['acuerdo_final']['cantidad']} unidades")
        print(f"  Ofertante: {resumen['acuerdo_final']['ofertante']}")

    return negociacion


def demostrar_negociacion_fallida():
    """
    Demuestra una negociación que llega a impasse
    """
    print("\n" + "=" * 70)
    print("NEGOCIACIÓN FALLIDA - Impasse")
    print("=" * 70)

    # Utilidades incompatibles
    utilidad_vendedor = Utilidad(
        precio_min=100,
        precio_max=200,
        cantidad_min=50,
        cantidad_max=200
    )

    utilidad_comprador = Utilidad(
        precio_min=10,
        precio_max=50,
        cantidad_min=5,
        cantidad_max=20
    )

    vendedor = AgenteNegociador("Miguel (Vendedor)", "vendedor", utilidad_vendedor)
    comprador = AgenteNegociador("Rosa (Compradora)", "comprador", utilidad_comprador)

    negociacion = NegociacionBilateral(vendedor.name, comprador.name)

    print("\nEscenario: Expectativas completamente incompatibles")
    print("─" * 50)

    # Oferta inicial
    oferta1 = negociacion.vendedor_presenta_oferta(precio=150, cantidad=100)
    respuesta, _ = comprador.evaluar_oferta(oferta1)

    if respuesta == RespuestaNegociacion.RECHAZADA:
        print("\n✗ El comprador rechaza la oferta inicial")
        print("✗ Las partes están demasiado alejadas")
        negociacion.registrar_impasse()

    return negociacion


def comparar_estrategias_negociacion():
    """Compara diferentes estrategias de negociación"""
    print("\n" + "=" * 70)
    print("ESTRATEGIAS DE NEGOCIACIÓN")
    print("=" * 70)

    estrategias = {
        "COMPETITIVA": {
            "Objetivo": "Maximizar ganancia propia",
            "Transparencia": "Baja - Ocultar info",
            "Apertura": "Ofrecer poco, pedir mucho",
            "Resultado": "Ganador-Perdedor (win-lose)",
            "Riesgo": "Represalias futuras"
        },
        "COLABORATIVA": {
            "Objetivo": "Maximizar ganancia mutua",
            "Transparencia": "Alta - Compartir info",
            "Apertura": "Propuestas creativas",
            "Resultado": "Ganador-Ganador (win-win)",
            "Riesgo": "Posible explotación"
        },
        "COMPROMISO": {
            "Objetivo": "Split the difference",
            "Transparencia": "Media",
            "Apertura": "Ceder algo, ganar algo",
            "Resultado": "Perdedor-Perdedor (lose-lose)",
            "Riesgo": "Nadie satisfecho completamente"
        }
    }

    for estrategia, props in estrategias.items():
        print(f"\n{estrategia}:")
        for prop, valor in props.items():
            print(f"  {prop:15} {valor}")


if __name__ == "__main__":
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║    NEGOCIACIÓN ENTRE AGENTES                              ║")
    print("║                                                            ║")
    print("║  Protocolo: Oferta-Contraoferta                           ║")
    print("║  Conceptos: BATNA, Zona de Acuerdo Posible (ZAP)          ║")
    print("║  Estrategias: Competitiva, Colaborativa, Compromiso       ║")
    print("╚════════════════════════════════════════════════════════════╝\n")

    try:
        demostrar_negociacion_compra_venta()
        demostrar_negociacion_fallida()
        comparar_estrategias_negociacion()

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
