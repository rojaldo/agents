"""
01_METRICAS_DESEMPENO.PY
========================

Ejemplo didáctico: Framework de Métricas de Desempeño de Agentes

Implementa métricas de:
- Efectividad: Accuracy, Precision, Recall, F1-Score, AUC-ROC
- Eficiencia: Latency, Throughput, Resource Usage
- Robustez: Error Rate, MTBF, Recovery Time
- Seguridad: Violation Rate, Fairness

REQUISITOS PREVIOS:
- pip install numpy scipy
"""

import time
import random
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from enum import Enum
import math


# ============================================================================
# TIPOS Y ENUMS
# ============================================================================

class CategoriaMetrica(Enum):
    """Categorías de métricas"""
    EFECTIVIDAD = "efectividad"
    EFICIENCIA = "eficiencia"
    ROBUSTEZ = "robustez"
    SEGURIDAD = "seguridad"


@dataclass
class Prediccion:
    """Representa una predicción del agente"""
    id: str
    predicho: bool  # True/False (positivo/negativo)
    real: bool  # Verdad del terreno
    latencia_ms: float = 0.0
    confianza: float = 0.5  # 0.0 a 1.0
    timestamp: float = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()

    @property
    def es_correcto(self) -> bool:
        """¿Predicción es correcta?"""
        return self.predicho == self.real


# ============================================================================
# MÉTRICAS DE EFECTIVIDAD
# ============================================================================

class MetricasEfectividad:
    """Calcula métricas de efectividad (accuracy, precision, recall, etc.)"""

    def __init__(self):
        self.predicciones: List[Prediccion] = []

    def agregar_prediccion(self, prediccion: Prediccion) -> None:
        """Agrega una predicción"""
        self.predicciones.append(prediccion)

    def _calcular_confusion_matrix(self) -> Tuple[int, int, int, int]:
        """Calcula matriz de confusión: TP, FP, FN, TN"""
        tp = sum(1 for p in self.predicciones if p.predicho and p.real)
        fp = sum(1 for p in self.predicciones if p.predicho and not p.real)
        fn = sum(1 for p in self.predicciones if not p.predicho and p.real)
        tn = sum(1 for p in self.predicciones if not p.predicho and not p.real)
        return tp, fp, fn, tn

    def accuracy(self) -> float:
        """Porcentaje de predicciones correctas"""
        if not self.predicciones:
            return 0.0
        tp, fp, fn, tn = self._calcular_confusion_matrix()
        total = tp + tn + fp + fn
        return (tp + tn) / total if total > 0 else 0.0

    def precision(self) -> float:
        """De los positivos predichos, cuántos fueron reales"""
        tp, fp, _, _ = self._calcular_confusion_matrix()
        denominador = tp + fp
        return tp / denominador if denominador > 0 else 0.0

    def recall(self) -> float:
        """De los positivos reales, cuántos encontró"""
        tp, _, fn, _ = self._calcular_confusion_matrix()
        denominador = tp + fn
        return tp / denominador if denominador > 0 else 0.0

    def f1_score(self) -> float:
        """Promedio armónico de precision y recall"""
        p = self.precision()
        r = self.recall()
        denominador = p + r
        if denominador == 0:
            return 0.0
        return 2 * (p * r) / denominador

    def auc_roc(self) -> float:
        """Area Under Curve - Receiver Operating Characteristic"""
        # Simplified implementation
        if not self.predicciones:
            return 0.5

        # Ordenar por confianza
        ordenadas = sorted(self.predicciones, key=lambda p: p.confianza, reverse=True)

        # Calcular AUC aproximado
        tp_rate = []
        fp_rate = []

        tp_total = sum(1 for p in self.predicciones if p.real)
        fp_total = sum(1 for p in self.predicciones if not p.real)

        tp_acum, fp_acum = 0, 0

        for pred in ordenadas:
            if pred.real:
                tp_acum += 1
            else:
                fp_acum += 1

            tp_rate.append(tp_acum / max(tp_total, 1))
            fp_rate.append(fp_acum / max(fp_total, 1))

        # Calcular área bajo la curva
        auc = 0.0
        for i in range(1, len(fp_rate)):
            auc += (fp_rate[i] - fp_rate[i-1]) * tp_rate[i]

        return auc

    def obtener_resumen(self) -> Dict:
        """Resumen de métricas de efectividad"""
        return {
            "accuracy": round(self.accuracy(), 3),
            "precision": round(self.precision(), 3),
            "recall": round(self.recall(), 3),
            "f1_score": round(self.f1_score(), 3),
            "auc_roc": round(self.auc_roc(), 3),
            "total_predicciones": len(self.predicciones)
        }


# ============================================================================
# MÉTRICAS DE EFICIENCIA
# ============================================================================

class MetricasEficiencia:
    """Calcula métricas de eficiencia (latency, throughput, recursos)"""

    def __init__(self):
        self.latencias: List[float] = []
        self.tiempos_inicio: List[float] = []
        self.cpu_usage: List[float] = []
        self.memory_usage: List[float] = []

    def registrar_latencia(self, latencia_ms: float) -> None:
        """Registra latencia de una request"""
        self.latencias.append(latencia_ms)

    def registrar_intervalo_temporal(self, inicio: float, fin: float) -> None:
        """Registra intervalo temporal para calcular throughput"""
        self.tiempos_inicio.append(fin - inicio)

    def latencia_promedio(self) -> float:
        """Latencia promedio en ms"""
        if not self.latencias:
            return 0.0
        return sum(self.latencias) / len(self.latencias)

    def latencia_percentil(self, percentil: int) -> float:
        """Latencia en percentil específico (p50, p95, p99)"""
        if not self.latencias:
            return 0.0
        ordenadas = sorted(self.latencias)
        indice = int(len(ordenadas) * percentil / 100)
        return ordenadas[min(indice, len(ordenadas) - 1)]

    def throughput_rps(self, duracion_total_s: float) -> float:
        """Requests por segundo (RPS)"""
        if duracion_total_s <= 0:
            return 0.0
        return len(self.latencias) / duracion_total_s

    def cpu_promedio(self) -> float:
        """Porcentaje promedio de CPU"""
        if not self.cpu_usage:
            return 0.0
        return sum(self.cpu_usage) / len(self.cpu_usage)

    def memory_pico(self) -> float:
        """Uso máximo de memoria"""
        return max(self.memory_usage) if self.memory_usage else 0.0

    def obtener_resumen(self, duracion_total_s: float) -> Dict:
        """Resumen de métricas de eficiencia"""
        return {
            "latencia_promedio_ms": round(self.latencia_promedio(), 2),
            "latencia_p50_ms": round(self.latencia_percentil(50), 2),
            "latencia_p95_ms": round(self.latencia_percentil(95), 2),
            "latencia_p99_ms": round(self.latencia_percentil(99), 2),
            "throughput_rps": round(self.throughput_rps(duracion_total_s), 2),
            "cpu_promedio_pct": round(self.cpu_promedio(), 1),
            "memory_pico_mb": round(self.memory_pico(), 1)
        }


# ============================================================================
# MÉTRICAS DE ROBUSTEZ
# ============================================================================

class MetricasRobustez:
    """Calcula métricas de robustez"""

    def __init__(self):
        self.intentos_totales = 0
        self.fallos = 0
        self.tiempos_fallo = []
        self.tiempos_recuperacion = []

    def registrar_intento(self, exito: bool) -> None:
        """Registra un intento"""
        self.intentos_totales += 1
        if not exito:
            self.fallos += 1
            self.tiempos_fallo.append(time.time())

    def registrar_recuperacion(self, tiempo_s: float) -> None:
        """Registra tiempo de recuperación de un fallo"""
        self.tiempos_recuperacion.append(tiempo_s)

    def error_rate(self) -> float:
        """Porcentaje de requests que fallan"""
        if self.intentos_totales == 0:
            return 0.0
        return (self.fallos / self.intentos_totales) * 100

    def mean_time_between_failures(self) -> float:
        """Promedio de tiempo entre fallos (MTBF)"""
        if len(self.tiempos_fallo) <= 1:
            return float('inf')

        intervalos = []
        for i in range(1, len(self.tiempos_fallo)):
            intervalos.append(self.tiempos_fallo[i] - self.tiempos_fallo[i-1])

        return sum(intervalos) / len(intervalos) if intervalos else float('inf')

    def mean_recovery_time(self) -> float:
        """Promedio de tiempo de recuperación"""
        if not self.tiempos_recuperacion:
            return 0.0
        return sum(self.tiempos_recuperacion) / len(self.tiempos_recuperacion)

    def obtener_resumen(self) -> Dict:
        """Resumen de métricas de robustez"""
        return {
            "error_rate_pct": round(self.error_rate(), 2),
            "intentos_totales": self.intentos_totales,
            "fallos": self.fallos,
            "mtbf_s": round(self.mean_time_between_failures(), 2),
            "mean_recovery_time_s": round(self.mean_recovery_time(), 2)
        }


# ============================================================================
# MÉTRICAS DE SEGURIDAD
# ============================================================================

class MetricasSeguridad:
    """Calcula métricas de seguridad"""

    def __init__(self):
        self.violaciones = 0
        self.intentos_totales = 0
        self.resultados_por_grupo = {}  # para fairness

    def registrar_intento_seguridad(self, violacion: bool, grupo: str = "default") -> None:
        """Registra un intento de seguridad"""
        self.intentos_totales += 1
        if violacion:
            self.violaciones += 1

        # Tracking por grupo para fairness
        if grupo not in self.resultados_por_grupo:
            self.resultados_por_grupo[grupo] = {"violaciones": 0, "total": 0}

        self.resultados_por_grupo[grupo]["total"] += 1
        if violacion:
            self.resultados_por_grupo[grupo]["violaciones"] += 1

    def tasa_violacion(self) -> float:
        """Porcentaje de violaciones de seguridad"""
        if self.intentos_totales == 0:
            return 0.0
        return (self.violaciones / self.intentos_totales) * 100

    def fairness_score(self) -> float:
        """Equidad: cuánto varían las tasas entre grupos"""
        if len(self.resultados_por_grupo) <= 1:
            return 1.0  # Perfecto si un grupo o ninguno

        tasas = []
        for grupo_data in self.resultados_por_grupo.values():
            tasa = (grupo_data["violaciones"] / max(grupo_data["total"], 1)) * 100
            tasas.append(tasa)

        # Fairness es inverso a varianza
        if not tasas:
            return 1.0

        media = sum(tasas) / len(tasas)
        varianza = sum((t - media) ** 2 for t in tasas) / len(tasas)
        std_dev = varianza ** 0.5

        # Normalize to 0-1
        fairness = max(0.0, 1.0 - (std_dev / 100))
        return fairness

    def obtener_resumen(self) -> Dict:
        """Resumen de métricas de seguridad"""
        resumen = {
            "tasa_violacion_pct": round(self.tasa_violacion(), 2),
            "violaciones": self.violaciones,
            "intentos": self.intentos_totales,
            "fairness_score": round(self.fairness_score(), 3)
        }

        # Detalles por grupo
        resumen["por_grupo"] = {}
        for grupo, data in self.resultados_por_grupo.items():
            tasa_grupo = (data["violaciones"] / max(data["total"], 1)) * 100
            resumen["por_grupo"][grupo] = round(tasa_grupo, 2)

        return resumen


# ============================================================================
# FRAMEWORK INTEGRADO
# ============================================================================

class FrameworkMetricas:
    """Framework integrado de métricas"""

    def __init__(self):
        self.efectividad = MetricasEfectividad()
        self.eficiencia = MetricasEficiencia()
        self.robustez = MetricasRobustez()
        self.seguridad = MetricasSeguridad()

    def agregar_resultado_query(
        self,
        prediccion: Prediccion,
        violacion_seguridad: bool = False,
        grupo: str = "default"
    ) -> None:
        """Agrega resultado de una query/predicción"""
        # Efectividad
        self.efectividad.agregar_prediccion(prediccion)

        # Eficiencia
        self.eficiencia.registrar_latencia(prediccion.latencia_ms)

        # Robustez
        self.robustez.registrar_intento(True)  # Asumimos éxito si no hay excepción

        # Seguridad
        self.seguridad.registrar_intento_seguridad(violacion_seguridad, grupo)

    def obtener_reporte_completo(self, duracion_total_s: float = 60.0) -> Dict:
        """Genera reporte completo con todas las métricas"""
        return {
            "efectividad": self.efectividad.obtener_resumen(),
            "eficiencia": self.eficiencia.obtener_resumen(duracion_total_s),
            "robustez": self.robustez.obtener_resumen(),
            "seguridad": self.seguridad.obtener_resumen()
        }

    def print_reporte(self, duracion_total_s: float = 60.0) -> None:
        """Imprime reporte formateado"""
        reporte = self.obtener_reporte_completo(duracion_total_s)

        print("\n" + "=" * 80)
        print("REPORTE DE MÉTRICAS DE DESEMPEÑO")
        print("=" * 80)

        # EFECTIVIDAD
        print("\n📊 EFECTIVIDAD")
        print("-" * 80)
        ef = reporte["efectividad"]
        print(f"  Accuracy:       {ef['accuracy']:.1%}")
        print(f"  Precision:      {ef['precision']:.1%}")
        print(f"  Recall:         {ef['recall']:.1%}")
        print(f"  F1-Score:       {ef['f1_score']:.1%}")
        print(f"  AUC-ROC:        {ef['auc_roc']:.1%}")
        print(f"  Total:          {ef['total_predicciones']} predicciones")

        # EFICIENCIA
        print("\n⚡ EFICIENCIA")
        print("-" * 80)
        efi = reporte["eficiencia"]
        print(f"  Latencia promedio:  {efi['latencia_promedio_ms']:.2f} ms")
        print(f"  Latencia p50:       {efi['latencia_p50_ms']:.2f} ms")
        print(f"  Latencia p95:       {efi['latencia_p95_ms']:.2f} ms")
        print(f"  Latencia p99:       {efi['latencia_p99_ms']:.2f} ms")
        print(f"  Throughput:         {efi['throughput_rps']:.2f} RPS")
        print(f"  CPU promedio:       {efi['cpu_promedio_pct']:.1f}%")
        print(f"  Memoria pico:       {efi['memory_pico_mb']:.1f} MB")

        # ROBUSTEZ
        print("\n🛡️  ROBUSTEZ")
        print("-" * 80)
        rob = reporte["robustez"]
        print(f"  Error rate:         {rob['error_rate_pct']:.2f}%")
        print(f"  Intentos:           {rob['intentos_totales']}")
        print(f"  Fallos:             {rob['fallos']}")
        print(f"  MTBF:               {rob['mtbf_s']:.2f} segundos")
        print(f"  Tiempo recuperación: {rob['mean_recovery_time_s']:.2f} segundos")

        # SEGURIDAD
        print("\n🔐 SEGURIDAD")
        print("-" * 80)
        seg = reporte["seguridad"]
        print(f"  Tasa violación:     {seg['tasa_violacion_pct']:.2f}%")
        print(f"  Violaciones:        {seg['violaciones']}/{seg['intentos']}")
        print(f"  Fairness score:     {seg['fairness_score']:.3f}")
        if seg["por_grupo"]:
            print(f"  Por grupo:")
            for grupo, tasa in seg["por_grupo"].items():
                print(f"    - {grupo}: {tasa:.2f}%")

        print("\n" + "=" * 80)


# ============================================================================
# DEMOSTRACIÓN
# ============================================================================

def demo_metricas():
    """Demuestra el framework de métricas"""

    print("=" * 80)
    print("DEMOSTRACIÓN: FRAMEWORK DE MÉTRICAS DE DESEMPEÑO")
    print("=" * 80)

    # Crear framework
    framework = FrameworkMetricas()

    print("\n1. SIMULACIÓN DE PREDICCIONES")
    print("-" * 80)

    # Simular 100 predicciones
    random.seed(42)
    for i in range(100):
        # Generar predicción con sesgo hacia correctas
        real = random.random() < 0.6
        predicho = random.random() < 0.7 if real else random.random() < 0.3

        latencia = random.gauss(50, 10)  # Latencia gaussiana ~50ms
        confianza = random.random()

        prediccion = Prediccion(
            id=f"pred_{i}",
            predicho=predicho,
            real=real,
            latencia_ms=max(5, latencia),  # Mínimo 5ms
            confianza=max(0, min(1, confianza))
        )

        # Registrar violación de seguridad (5% de probabilidad)
        violacion = random.random() < 0.05
        grupo = random.choice(["grupoA", "grupoB", "grupoC"])

        framework.agregar_resultado_query(prediccion, violacion, grupo)

        # CPU y memoria aleatorios
        framework.eficiencia.cpu_usage.append(random.gauss(35, 10))
        framework.eficiencia.memory_usage.append(random.gauss(256, 50))

        # Algunos fallos de robustez (2% de probabilidad)
        if random.random() < 0.02:
            framework.robustez.registrar_intento(False)
            framework.robustez.registrar_recuperacion(random.gauss(2, 0.5))

    print(f"Predicciones procesadas: 100")
    print(f"Latencias registradas: {len(framework.eficiencia.latencias)}")

    # Mostrar reporte
    framework.print_reporte(duracion_total_s=60.0)

    print("\n" + "=" * 80)
    print("Conclusión: Framework permite medir desempeño integral")
    print("de agentes desde múltiples perspectivas")
    print("=" * 80)


if __name__ == "__main__":
    demo_metricas()
