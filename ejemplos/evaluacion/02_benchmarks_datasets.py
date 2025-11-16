"""
02_BENCHMARKS_DATASETS.PY
=========================

Ejemplo didáctico: Creación y Gestión de Benchmarks

Implementa:
- Creación de datasets con ejemplos
- Anotación y validación
- Medición de acuerdo entre anotadores (Inter-Annotator Agreement)
- Sesgo en benchmarks
- Versionado de datasets
"""

import json
import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime


@dataclass
class Ejemplo:
    """Un ejemplo en el dataset"""
    id: str
    entrada: str
    salida_esperada: str
    anotaciones: List[str] = field(default_factory=list)
    consenso: Optional[str] = None
    dificultad: float = 0.5  # 0.0-1.0
    tags: List[str] = field(default_factory=list)


class Dataset:
    """Gestiona dataset de evaluación"""

    def __init__(self, nombre: str, version: str = "1.0"):
        self.nombre = nombre
        self.version = version
        self.ejemplos: List[Ejemplo] = []
        self.anotadores: List[str] = []
        self.metadata = {}
        self.creado_en = datetime.now().isoformat()

    def agregar_ejemplo(self, ejemplo: Ejemplo) -> None:
        """Agrega un ejemplo"""
        self.ejemplos.append(ejemplo)

    def agregar_anotaciones(self, ejemplo_id: str, anotador: str, valor: str) -> None:
        """Agrega anotación de anotador"""
        if anotador not in self.anotadores:
            self.anotadores.append(anotador)

        for ej in self.ejemplos:
            if ej.id == ejemplo_id:
                ej.anotaciones.append(valor)
                break

    def calcular_consenso(self) -> None:
        """Calcula consenso para cada ejemplo"""
        for ej in self.ejemplos:
            if ej.anotaciones:
                # Votación mayoritaria
                from collections import Counter
                contador = Counter(ej.anotaciones)
                ej.consenso = contador.most_common(1)[0][0]

    def cohens_kappa(self, ej_id: str) -> float:
        """Calcula Cohen's Kappa para concordancia entre 2 anotadores"""
        for ej in self.ejemplos:
            if ej.id == ej_id and len(ej.anotaciones) >= 2:
                a1, a2 = ej.anotaciones[0], ej.anotaciones[1]

                # Acuerdo observado
                po = 1.0 if a1 == a2 else 0.0

                # Acuerdo por azar (simplificado)
                pe = 0.5

                kappa = (po - pe) / (1 - pe) if pe < 1 else 1.0
                return kappa

        return 0.0

    def medir_sesgo(self) -> Dict:
        """Mide sesgo en el dataset"""
        sesgo = {
            "distribucion_dificultad": {},
            "distribucion_tags": {},
            "acuerdo_promedio": 0.0
        }

        # Distribución de dificultad
        difs = [e.dificultad for e in self.ejemplos]
        sesgo["distribucion_dificultad"] = {
            "baja": sum(1 for d in difs if d < 0.33) / len(difs) if difs else 0,
            "media": sum(1 for d in difs if 0.33 <= d < 0.67) / len(difs) if difs else 0,
            "alta": sum(1 for d in difs if d >= 0.67) / len(difs) if difs else 0
        }

        # Acuerdo promedio entre anotadores
        kaos = []
        for ej in self.ejemplos:
            if len(ej.anotaciones) >= 2:
                kappa = self.cohens_kappa(ej.id)
                kaos.append(kappa)

        if kaos:
            sesgo["acuerdo_promedio"] = sum(kaos) / len(kaos)

        return sesgo

    def obtener_estadisticas(self) -> Dict:
        """Estadísticas del dataset"""
        return {
            "nombre": self.nombre,
            "version": self.version,
            "total_ejemplos": len(self.ejemplos),
            "total_anotadores": len(self.anotadores),
            "anotadores": self.anotadores,
            "ejemplos_anotados": sum(1 for e in self.ejemplos if e.consenso),
            "con_consenso": sum(1 for e in self.ejemplos if e.consenso),
            "creado_en": self.creado_en
        }

    def exportar_json(self, ruta: str) -> None:
        """Exporta dataset a JSON"""
        datos = {
            "metadata": self.obtener_estadisticas(),
            "sesgo": self.medir_sesgo(),
            "ejemplos": [
                {
                    "id": e.id,
                    "entrada": e.entrada,
                    "salida_esperada": e.salida_esperada,
                    "consenso": e.consenso,
                    "anotaciones_count": len(e.anotaciones),
                    "dificultad": e.dificultad
                }
                for e in self.ejemplos
            ]
        }

        with open(ruta, "w") as f:
            json.dump(datos, f, indent=2)


def demo_benchmarks():
    """Demuestra creación de benchmarks"""

    print("=" * 80)
    print("DEMOSTRACIÓN: CREACIÓN Y GESTIÓN DE BENCHMARKS")
    print("=" * 80)

    # Crear dataset
    dataset = Dataset("qa_benchmark", version="1.0")

    print("\n1. CREACIÓN DE EJEMPLOS")
    print("-" * 80)

    # Agregar ejemplos
    ejemplos_data = [
        ("¿Cuál es la capital de Francia?", "París", 0.2),
        ("¿Cuál es el teorema de Pitágoras?", "a² + b² = c²", 0.4),
        ("¿Cuál es la sentido de la vida?", "42", 0.8),
        ("¿Quién escribió Don Quijote?", "Miguel de Cervantes", 0.3),
        ("¿Cuál es la masa del fotón?", "0", 0.7),
    ]

    for i, (pregunta, respuesta, dificultad) in enumerate(ejemplos_data):
        ej = Ejemplo(
            id=f"ej_{i}",
            entrada=pregunta,
            salida_esperada=respuesta,
            dificultad=dificultad
        )
        dataset.agregar_ejemplo(ej)

    print(f"Ejemplos creados: {len(dataset.ejemplos)}")

    # Anotaciones simuladas
    print("\n2. ANOTACIÓN POR MÚLTIPLES ANOTADORES")
    print("-" * 80)

    anotadores = ["alice", "bob", "charlie"]

    for ej in dataset.ejemplos:
        for anotador in anotadores:
            # Simular acuerdo ~80% con la respuesta correcta
            if random.random() < 0.8:
                valor = ej.salida_esperada
            else:
                valor = f"{ej.salida_esperada}_variante"

            dataset.agregar_anotaciones(ej.id, anotador, valor)

    print(f"Anotadores: {dataset.anotadores}")
    print(f"Total anotaciones: {sum(len(e.anotaciones) for e in dataset.ejemplos)}")

    # Calcular consenso
    print("\n3. CÁLCULO DE CONSENSO")
    print("-" * 80)

    dataset.calcular_consenso()

    print("Ejemplos con consenso:")
    for ej in dataset.ejemplos:
        kappa = dataset.cohens_kappa(ej.id)
        print(f"  {ej.id}: {ej.consenso} (kappa={kappa:.2f})")

    # Análisis de sesgo
    print("\n4. ANÁLISIS DE SESGO")
    print("-" * 80)

    sesgo = dataset.medir_sesgo()
    print(f"Distribución de dificultad:")
    print(f"  Baja:   {sesgo['distribucion_dificultad']['baja']:.1%}")
    print(f"  Media:  {sesgo['distribucion_dificultad']['media']:.1%}")
    print(f"  Alta:   {sesgo['distribucion_dificultad']['alta']:.1%}")
    print(f"\nAcuerdo promedio entre anotadores: {sesgo['acuerdo_promedio']:.3f}")

    # Estadísticas
    print("\n5. ESTADÍSTICAS DEL DATASET")
    print("-" * 80)

    stats = dataset.obtener_estadisticas()
    for clave, valor in stats.items():
        print(f"  {clave}: {valor}")

    print("\n" + "=" * 80)
    print("Conclusión: Benchmarks bien construidos son esenciales")
    print("para evaluación justa de agentes")
    print("=" * 80)


if __name__ == "__main__":
    demo_benchmarks()
