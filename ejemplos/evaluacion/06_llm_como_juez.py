"""
MÓDULO 6: Evaluación con LLMs como Jueces
==========================================

Este módulo demuestra cómo usar LLMs (vía Ollama) como evaluadores automáticos.

Conceptos clave:
- LLMs para evaluación automática de respuestas
- Métricas cualitativas vs cuantitativas
- Variabilidad en evaluaciones de LLM
- Mitigación de variabilidad
- Calibración LLM vs evaluación manual
- Best practices

Ejemplo práctico: Evaluador automático para respuestas Q&A
"""

import json
import random
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from enum import Enum
try:
    from langchain_ollama import OllamaLLM
    OLLAMA_DISPONIBLE = True
except ImportError:
    OLLAMA_DISPONIBLE = False


# ============================================================================
# TIPOS Y ENUMS
# ============================================================================

class EscalaLikert(Enum):
    """Escala Likert estándar para evaluación"""
    MUY_POBRE = 1
    POBRE = 2
    NEUTRO = 3
    BUENO = 4
    MUY_BUENO = 5


@dataclass
class EvaluacionRespuesta:
    """Resultado de evaluación de una respuesta"""
    pregunta: str
    respuesta: str
    evaluador: str  # 'llm' o 'humano'
    relevancia: int  # 1-5
    exactitud: int  # 1-5
    completitud: int  # 1-5
    claridad: int  # 1-5
    explicacion: str = ""
    temperatura_llm: float = 0.3
    modelo_llm: str = "mistral"

    def puntuacion_promedio(self) -> float:
        """Calcula puntuación promedio"""
        return (self.relevancia + self.exactitud + self.completitud + self.claridad) / 4

    def a_dict(self) -> Dict[str, Any]:
        return {
            "pregunta": self.pregunta,
            "respuesta": self.respuesta,
            "evaluador": self.evaluador,
            "relevancia": self.relevancia,
            "exactitud": self.exactitud,
            "completitud": self.completitud,
            "claridad": self.claridad,
            "puntuacion_promedio": self.puntuacion_promedio(),
            "explicacion": self.explicacion,
            "temperatura": self.temperatura_llm,
            "modelo": self.modelo_llm
        }


# ============================================================================
# EVALUADOR CON LLM
# ============================================================================

class EvaluadorLLM:
    """Evaluador que usa LLM como juez"""

    def __init__(self, modelo: str = "mistral", temperatura: float = 0.3):
        """
        Inicializa evaluador

        Args:
            modelo: nombre del modelo en Ollama
            temperatura: temperatura para variación en respuestas
        """
        self.modelo = modelo
        self.temperatura = temperatura

        if OLLAMA_DISPONIBLE:
            self.llm = OllamaLLM(model=modelo, temperature=temperatura)
        else:
            self.llm = None
            print("⚠️  Ollama no disponible, usando simulación")

    def evaluar_respuesta(self, pregunta: str, respuesta: str,
                         respuesta_esperada: str = None) -> EvaluacionRespuesta:
        """
        Evalúa una respuesta usando LLM

        Args:
            pregunta: pregunta realizada
            respuesta: respuesta a evaluar
            respuesta_esperada: respuesta esperada (opcional para contexto)

        Returns:
            EvaluacionRespuesta con scores
        """

        contexto_esperada = f"\n\nRESPUESTA ESPERADA (para referencia): {respuesta_esperada}" \
                           if respuesta_esperada else ""

        prompt = f"""
Evalúa la siguiente respuesta en escala 1-5 para cada criterio:

PREGUNTA: {pregunta}

RESPUESTA A EVALUAR: {respuesta}{contexto_esperada}

Criterios de evaluación:
1. Relevancia (1-5): ¿Responde la pregunta sin desviarse?
2. Exactitud (1-5): ¿Es la información correcta?
3. Completitud (1-5): ¿Es suficientemente completa?
4. Claridad (1-5): ¿Es clara y fácil de entender?

Responde en formato JSON puro sin código ni markdown:
{{
  "relevancia": <1-5>,
  "exactitud": <1-5>,
  "completitud": <1-5>,
  "claridad": <1-5>,
  "explicacion": "<explicación breve>"
}}
"""

        if self.llm:
            try:
                respuesta_llm = self.llm.invoke(prompt)
                scores = self._parsear_respuesta_json(respuesta_llm)
            except Exception as e:
                print(f"Error evaluando con LLM: {e}")
                scores = self._generar_scores_simulados()
        else:
            # Usar simulación si Ollama no está disponible
            scores = self._generar_scores_simulados()

        return EvaluacionRespuesta(
            pregunta=pregunta,
            respuesta=respuesta,
            evaluador="llm",
            relevancia=scores.get("relevancia", 3),
            exactitud=scores.get("exactitud", 3),
            completitud=scores.get("completitud", 3),
            claridad=scores.get("claridad", 3),
            explicacion=scores.get("explicacion", ""),
            temperatura_llm=self.temperatura,
            modelo_llm=self.modelo
        )

    def _parsear_respuesta_json(self, respuesta: str) -> Dict[str, Any]:
        """Parsea JSON de la respuesta del LLM"""
        try:
            # Buscar JSON en la respuesta
            inicio = respuesta.find('{')
            fin = respuesta.rfind('}') + 1
            if inicio >= 0 and fin > 0:
                json_str = respuesta[inicio:fin]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass
        return {}

    def _generar_scores_simulados(self) -> Dict[str, Any]:
        """Genera scores simulados para testing"""
        # Simulación realista
        base_score = random.randint(2, 5)
        variacion = random.randint(-1, 1)

        return {
            "relevancia": max(1, min(5, base_score + variacion)),
            "exactitud": max(1, min(5, base_score + variacion)),
            "completitud": max(1, min(5, base_score + variacion)),
            "claridad": max(1, min(5, base_score + variacion)),
            "explicacion": "Evaluación simulada (Ollama no disponible)"
        }


# ============================================================================
# EVALUADOR MANUAL (HUMANO)
# ============================================================================

class EvaluadorHumano:
    """Simula evaluación manual por humanos"""

    def __init__(self, consistencia: float = 0.8):
        """
        Args:
            consistencia: qué tan consistente es el evaluador (0-1)
        """
        self.consistencia = consistencia

    def evaluar_respuesta(self, pregunta: str, respuesta: str,
                         respuesta_esperada: str = None) -> EvaluacionRespuesta:
        """
        Simula evaluación humana

        Args:
            pregunta: pregunta realizada
            respuesta: respuesta a evaluar
            respuesta_esperada: respuesta esperada

        Returns:
            EvaluacionRespuesta
        """

        # Evaluación humana más consistente pero lenta
        # Aquí simulamos basado en similitud con respuesta esperada
        puntuacion_base = 3

        if respuesta_esperada:
            # Simular similitud
            similitud = len(set(respuesta.split()) & set(respuesta_esperada.split())) / \
                       max(len(respuesta.split()), len(respuesta_esperada.split()))
            puntuacion_base = int(1 + similitud * 4)  # Escala 1-5

        # Agregar consistencia
        if random.random() < self.consistencia:
            variacion = random.randint(-1, 1)
        else:
            variacion = random.randint(-2, 2)

        scores = {
            "relevancia": max(1, min(5, puntuacion_base + variacion)),
            "exactitud": max(1, min(5, puntuacion_base + variacion)),
            "completitud": max(1, min(5, puntuacion_base + variacion - 1)),
            "claridad": max(1, min(5, puntuacion_base + variacion))
        }

        return EvaluacionRespuesta(
            pregunta=pregunta,
            respuesta=respuesta,
            evaluador="humano",
            relevancia=scores["relevancia"],
            exactitud=scores["exactitud"],
            completitud=scores["completitud"],
            claridad=scores["claridad"],
            explicacion="Evaluación manual"
        )


# ============================================================================
# COMPARADOR DE EVALUACIONES
# ============================================================================

class ComparadorEvaluaciones:
    """Compara evaluaciones LLM vs manual"""

    @staticmethod
    def calcular_correlacion(evaluaciones_llm: List[EvaluacionRespuesta],
                            evaluaciones_humano: List[EvaluacionRespuesta]) -> float:
        """
        Calcula correlación entre evaluaciones LLM y humano

        Returns:
            Correlación (0-1), donde 1 es acuerdo perfecto
        """
        if len(evaluaciones_llm) != len(evaluaciones_humano):
            return 0.0

        diferencias = []
        for llm, humano in zip(evaluaciones_llm, evaluaciones_humano):
            diff = abs(llm.puntuacion_promedio() - humano.puntuacion_promedio())
            diferencias.append(diff)

        # Correlación inversa a diferencia promedio
        diff_promedio = sum(diferencias) / len(diferencias)
        correlacion = 1.0 - (diff_promedio / 5.0)  # Normalizar a 0-1

        return max(0.0, correlacion)

    @staticmethod
    def imprimir_comparacion(evaluaciones_llm: List[EvaluacionRespuesta],
                            evaluaciones_humano: List[EvaluacionRespuesta]) -> None:
        """Imprime comparación entre evaluaciones"""

        print("\n" + "="*80)
        print("COMPARACIÓN: LLM vs MANUAL")
        print("="*80 + "\n")

        print(f"{'Métrica':<20} {'LLM':<15} {'Manual':<15} {'Diferencia':<15}")
        print("-"*80)

        scores_llm = [e.puntuacion_promedio() for e in evaluaciones_llm]
        scores_humano = [e.puntuacion_promedio() for e in evaluaciones_humano]

        promedio_llm = sum(scores_llm) / len(scores_llm) if scores_llm else 0
        promedio_humano = sum(scores_humano) / len(scores_humano) if scores_humano else 0
        diferencia = abs(promedio_llm - promedio_humano)

        print(f"{'Puntuación promedio':<20} {promedio_llm:<15.2f} {promedio_humano:<15.2f} {diferencia:<15.2f}")

        # Variabilidad
        if len(scores_llm) > 1:
            varianza_llm = sum((x - promedio_llm) ** 2 for x in scores_llm) / len(scores_llm)
            std_llm = varianza_llm ** 0.5
        else:
            std_llm = 0

        if len(scores_humano) > 1:
            varianza_humano = sum((x - promedio_humano) ** 2 for x in scores_humano) / len(scores_humano)
            std_humano = varianza_humano ** 0.5
        else:
            std_humano = 0

        print(f"{'Desv. Estándar':<20} {std_llm:<15.2f} {std_humano:<15.2f}")

        # Correlación
        correlacion = ComparadorEvaluaciones.calcular_correlacion(evaluaciones_llm, evaluaciones_humano)
        print(f"{'Correlación':<20} {correlacion:<15.3f}")


# ============================================================================
# DEMOSTRACIÓN
# ============================================================================

def demo_llm_juez():
    """Demuestra evaluación con LLM como juez"""

    print("=" * 80)
    print("EVALUACIÓN CON LLMs COMO JUECES")
    print("=" * 80)

    # Dataset de prueba
    dataset = [
        {
            "pregunta": "¿Cuál es la capital de Francia?",
            "respuesta": "París, ubicada en el norte de Francia, es la capital del país.",
            "respuesta_esperada": "París"
        },
        {
            "pregunta": "¿Cuánto es 2+2?",
            "respuesta": "La suma de 2+2 es igual a 4.",
            "respuesta_esperada": "4"
        },
        {
            "pregunta": "¿Quién escribió Don Quijote?",
            "respuesta": "Don Quijote fue escrito por Miguel de Cervantes en 1605.",
            "respuesta_esperada": "Miguel de Cervantes"
        },
    ]

    # 1. EVALUACIÓN CON LLM
    print("\n1. EVALUACIÓN CON LLM (múltiples temperaturas)")
    print("-" * 80)

    evaluador_llm = EvaluadorLLM(modelo="mistral", temperatura=0.3)

    evaluaciones_llm = []
    for item in dataset:
        print(f"\nEvaluando: {item['pregunta'][:50]}...")
        eval_resultado = evaluador_llm.evaluar_respuesta(
            item["pregunta"],
            item["respuesta"],
            item["respuesta_esperada"]
        )
        evaluaciones_llm.append(eval_resultado)
        print(f"  Puntuación: {eval_resultado.puntuacion_promedio():.2f}")

    # 2. EVALUACIÓN MANUAL
    print("\n2. EVALUACIÓN MANUAL (simulada)")
    print("-" * 80)

    evaluador_humano = EvaluadorHumano(consistencia=0.85)

    evaluaciones_humano = []
    for item in dataset:
        print(f"Evaluador humano evalúa: {item['pregunta'][:50]}...")
        eval_resultado = evaluador_humano.evaluar_respuesta(
            item["pregunta"],
            item["respuesta"],
            item["respuesta_esperada"]
        )
        evaluaciones_humano.append(eval_resultado)
        print(f"  Puntuación: {eval_resultado.puntuacion_promedio():.2f}")

    # 3. COMPARACIÓN
    print("\n3. ANÁLISIS COMPARATIVO")
    print("-" * 80)

    ComparadorEvaluaciones.imprimir_comparacion(evaluaciones_llm, evaluaciones_humano)

    # 4. VARIABILIDAD EN LLM
    print("\n4. VARIABILIDAD DE LLM (múltiples trials)")
    print("-" * 80)

    print("\nEvaluando misma respuesta 5 veces con diferentes temperaturas:")

    pregunta_test = dataset[0]["pregunta"]
    respuesta_test = dataset[0]["respuesta"]

    scores_por_temp = {}
    for temp in [0.1, 0.3, 0.5, 0.7, 0.9]:
        evaluador = EvaluadorLLM(temperatura=temp)
        eval_res = evaluador.evaluar_respuesta(pregunta_test, respuesta_test)
        scores_por_temp[temp] = eval_res.puntuacion_promedio()
        print(f"  Temperatura {temp}: {eval_res.puntuacion_promedio():.2f}")

    # 5. BEST PRACTICES
    print("\n" + "=" * 80)
    print("BEST PRACTICES PARA EVALUACIÓN CON LLM")
    print("=" * 80)

    print(f"""
✓ DISEÑO DE PROMPTS:
  - Sé específico en criterios de evaluación
  - Incluye ejemplos (few-shot learning)
  - Usa formato estructurado (JSON)
  - Proporciona contexto suficiente

✓ MITIGACIÓN DE VARIABILIDAD:
  - Usa temperatura baja (0.1-0.3) para consistencia
  - Ejecuta múltiples trials y promedia
  - Usa ensemble de múltiples LLMs
  - Valida contra evaluación manual en muestra

✓ CALIBRACIÓN:
  - Compara LLM vs humano en ~50-100 ejemplos
  - Ajusta prompts basado en discrepancias
  - Documental sesgos encontrados
  - Establece SLA de correlación (e.g., > 0.80)

✓ MONITOREO:
  - Valida periódicamente (cada mes)
  - Revisa cambios en distribución de scores
  - Mantén muestras de evaluación humana
  - Implementa appeal process para usuarios

RESULTADOS EN ESTE EJEMPLO:
  - Correlación LLM vs Manual: {ComparadorEvaluaciones.calcular_correlacion(evaluaciones_llm, evaluaciones_humano):.3f}
  - Variabilidad con temperatura: {(max(scores_por_temp.values()) - min(scores_por_temp.values())):.2f} puntos
    """)


if __name__ == "__main__":
    demo_llm_juez()
