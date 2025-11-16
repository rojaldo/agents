# Contenidos Didácticos: Evaluación y Testing de Agentes IA

## 📚 Índice
1. [Módulo 1: Métricas de Desempeño](#módulo-1)
2. [Módulo 2: Benchmarks y Datasets](#módulo-2)
3. [Módulo 3: Testing Funcional](#módulo-3)
4. [Módulo 4: Debugging y Monitoreo](#módulo-4)

---

## <a name="módulo-1"></a>Módulo 1: Métricas de Desempeño de Agentes

### ¿Por Qué Métricas?

Imagina que construiste un agente de IA. ¿Cómo sabes si es BUENO?

```
Pregunta: "¿Mi agente es bueno?"

Respuestas MALAS:
  ❌ "Parece que funciona"
  ❌ "La mayoría de veces acierta"
  ❌ "Mis amigos dicen que está bien"

Respuestas BUENAS:
  ✅ "Accuracy del 94.3% en 10,000 muestras"
  ✅ "Latencia P95 de 120ms"
  ✅ "Maneja fallos en 99.9% de casos"
```

Las MÉTRICAS nos permiten MEDIR y COMPARAR.

### 1.1 Framework General de Métricas

```python
class MetricFramework:
    """
    CATEGORÍAS DE MÉTRICAS

    ┌─────────────────────────────────────────┐
    │ 1. EFECTIVIDAD: ¿Hace lo que debe?      │
    │    - Accuracy, Precision, Recall, F1    │
    │                                          │
    │ 2. EFICIENCIA: ¿A qué costo?             │
    │    - Latencia, Throughput, Recursos     │
    │                                          │
    │ 3. ROBUSTEZ: ¿Qué tan resiliente?       │
    │    - Error Rate, Recovery Time          │
    │                                          │
    │ 4. SEGURIDAD: ¿Es seguro?               │
    │    - Violaciones, Fairness, Adversarial │
    │                                          │
    │ 5. ESCALABILIDAD: ¿Funciona más grande? │
    │    - Performance con + carga            │
    └─────────────────────────────────────────┘
    """

    def __init__(self):
        self.metrics = {}
        self.measurements = []


# ═════════════════════════════════════════════════════════════════
# 1️⃣ MÉTRICAS DE EFECTIVIDAD
# ═════════════════════════════════════════════════════════════════

class EffectivenessMetrics:
    """
    ¿QUÉ TAN BIEN HACE LO QUE DEBE?

    CASO: Agente clasifica emails en Spam / No-Spam

    Matriz de confusión:
    ┌──────────────────┬──────────────────┐
    │ Predice SPAM     │ Predice NO-SPAM  │
    ├──────────────────┼──────────────────┤
    │ TP: 95 Correcto  │ FN: 5 Perdidos   │ Realmente SPAM
    │ (detectó spam)   │ (no detectó)     │
    ├──────────────────┼──────────────────┤
    │ FP: 3 Error      │ TN: 97 Correcto  │ Realmente NO-SPAM
    │ (falsa alarma)   │ (detectó bien)   │
    └──────────────────┴──────────────────┘

    Donde:
    - TP (True Positive): Predijo SPAM, era SPAM ✓
    - TN (True Negative): Predijo NO-SPAM, era NO-SPAM ✓
    - FP (False Positive): Predijo SPAM, era NO-SPAM ✗
    - FN (False Negative): Predijo NO-SPAM, era SPAM ✗
    """

    def __init__(self, true_positives, true_negatives,
                 false_positives, false_negatives):
        self.TP = true_positives      # 95
        self.TN = true_negatives      # 97
        self.FP = false_positives     # 3
        self.FN = false_negatives     # 5

    def accuracy(self):
        """
        ACCURACY: ¿Cuántas predicciones fueron correctas?

        Fórmula: (TP + TN) / Total

        Rango: 0% (todos mal) → 100% (todos bien)

        Interpretación: De 200 emails, ¿cuántos clasificó bien?
        """
        total = self.TP + self.TN + self.FP + self.FN
        acc = (self.TP + self.TN) / total * 100
        return f"Accuracy: {acc:.1f}%"

        # Ejemplo:
        # (95 + 97) / 200 = 192/200 = 96%
        # El agente clasifica BIEN el 96% de emails

    def precision(self):
        """
        PRECISION: De los que predijo como SPAM, ¿cuántos eran realmente SPAM?

        Pregunta: Si te digo "es SPAM", ¿confío?

        Fórmula: TP / (TP + FP)

        Rango: 0% (sin confianza) → 100% (muy confiable)
        """
        if self.TP + self.FP == 0:
            return 0

        prec = self.TP / (self.TP + self.FP) * 100
        return f"Precision: {prec:.1f}%"

        # Ejemplo:
        # TP=95, FP=3 → 95/(95+3) = 95/98 = 96.9%
        # Si te digo "es SPAM", tengo 96.9% de confianza

    def recall(self):
        """
        RECALL: De TODOS los SPAMs reales, ¿cuántos detecté?

        Pregunta: ¿De cuántos spams reales me entero?

        Fórmula: TP / (TP + FN)

        Rango: 0% (no detecta) → 100% (detecta todos)
        """
        if self.TP + self.FN == 0:
            return 0

        rec = self.TP / (self.TP + self.FN) * 100
        return f"Recall: {rec:.1f}%"

        # Ejemplo:
        # TP=95, FN=5 → 95/(95+5) = 95/100 = 95%
        # Detecté el 95% de todos los spams

    def f1_score(self):
        """
        F1-SCORE: Promedio armónico de Precision y Recall

        Usa esto cuando PRECISION y RECALL son igualmente importantes

        Fórmula: 2 * (precision * recall) / (precision + recall)

        Rango: 0 (terrible) → 1 (perfecto)
        """
        prec = self.TP / (self.TP + self.FP) if (self.TP + self.FP) > 0 else 0
        rec = self.TP / (self.TP + self.FN) if (self.TP + self.FN) > 0 else 0

        if prec + rec == 0:
            return 0

        f1 = 2 * (prec * rec) / (prec + rec)
        return f"F1-Score: {f1:.2f}"

        # Ejemplo: Precision=0.969, Recall=0.95
        # F1 = 2 * (0.969 * 0.95) / (0.969 + 0.95)
        #    = 2 * 0.920 / 1.919
        #    = 0.960

    def compare_agents(self):
        """
        Comparación práctica entre dos agentes
        """

        print("""
        AGENTE A vs AGENTE B

        ┌─────────────┬────────────┬────────────┐
        │ Métrica     │ Agente A   │ Agente B   │
        ├─────────────┼────────────┼────────────┤
        │ Accuracy    │ 96.0%      │ 92.0%      │ Mejor: A
        │ Precision   │ 96.9%      │ 99.0%      │ Mejor: B (menos falsos positivos)
        │ Recall      │ 95.0%      │ 89.0%      │ Mejor: A (detecta más spams)
        │ F1-Score    │ 0.960      │ 0.940      │ Mejor: A (balance general)
        └─────────────┴────────────┴────────────┘

        DECISIÓN:
        - ¿Importa más NO dejar pasar spam? → Agente B (alta precision)
        - ¿Importa detectar todo spam posible? → Agente A (alto recall)
        - ¿Queremos balance? → Agente A (F1 mayor)
        """)


# ═════════════════════════════════════════════════════════════════
# 2️⃣ MÉTRICAS DE EFICIENCIA
# ═════════════════════════════════════════════════════════════════

class EfficiencyMetrics:
    """
    ¿A QUÉ COSTO DE RECURSOS?
    """

    def __init__(self):
        self.requests = []      # [(request_time, response_time), ...]
        self.cpu_usage = []
        self.memory_usage = []
        self.cost_per_request = []

    def latency(self):
        """
        LATENCIA: ¿Cuánto tarda en responder?

        Medidas clave: P50, P95, P99 (percentiles)

        EJEMPLO: 1000 requests ordenados por tiempo
        """

        response_times = [50, 55, 60, ..., 150, 200]  # 1000 valores

        # P50: 50% de requests son ≤ este tiempo
        p50 = sorted(response_times)[len(response_times) // 2]
        # → "50% de requests responden en ≤ 100ms"

        # P95: 95% de requests son ≤ este tiempo
        p95 = sorted(response_times)[int(len(response_times) * 0.95)]
        # → "95% de requests responden en ≤ 150ms"

        # P99: 99% de requests son ≤ este tiempo
        p99 = sorted(response_times)[int(len(response_times) * 0.99)]
        # → "99% de requests responden en ≤ 200ms"

        print(f"""
        LATENCIA:
        - P50 (mediana): {p50}ms - Tiempo típico
        - P95: {p95}ms - Tiempo lentitud tolerable
        - P99: {p99}ms - Peor caso aceptable
        """)

        return {'p50': p50, 'p95': p95, 'p99': p99}

    def throughput(self):
        """
        THROUGHPUT: ¿Cuántas requests por segundo?

        RPS = Requests Per Second

        EJEMPLO:
        - Agente A: 1000 RPS
        - Agente B: 500 RPS
        → Agente A es 2x más rápido
        """

        total_time = 100  # segundos
        num_requests = 50000

        rps = num_requests / total_time
        print(f"Throughput: {rps} RPS")

        return rps

    def resource_usage(self):
        """
        CONSUMO DE RECURSOS

        Medir:
        - CPU: % utilización
        - Memory: MB / GB usados
        - Disk: I/O operaciones
        """

        resources = {
            'cpu_percent': 45,      # 45% de CPU
            'memory_mb': 512,       # 512 MB de RAM
            'memory_percent': 25,   # 25% del total
            'disk_io_ops': 1000,    # 1000 operaciones/sec
        }

        print(f"""
        RECURSOS:
        - CPU: {resources['cpu_percent']}%
        - Memoria: {resources['memory_mb']}MB ({resources['memory_percent']}%)
        - Disk I/O: {resources['disk_io_ops']} ops/sec
        """)

        return resources

    def cost_per_operation(self):
        """
        COSTO MONETARIO

        Importante si usas APIs pagas (OpenAI, etc.)

        EJEMPLO: GPT-4 cuesta por token
        """

        inputs_tokens = 150
        outputs_tokens = 50
        price_input = 0.03 / 1000  # $0.03 por 1000 tokens
        price_output = 0.06 / 1000  # $0.06 por 1000 tokens

        cost = (inputs_tokens * price_input +
                outputs_tokens * price_output)

        print(f"Costo por request: ${cost:.4f}")
        return cost


# ═════════════════════════════════════════════════════════════════
# 3️⃣ MÉTRICAS DE ROBUSTEZ
# ═════════════════════════════════════════════════════════════════

class RobustnessMetrics:
    """
    ¿QUÉ TAN RESILIENTE ES?
    """

    def __init__(self):
        self.total_requests = 10000
        self.failed_requests = 15
        self.failures = []  # timestamps of failures

    def error_rate(self):
        """
        ERROR RATE: ¿Cuántas requests fallan?

        Target típico: < 0.1%
        """
        error_rate = self.failed_requests / self.total_requests * 100
        print(f"Error Rate: {error_rate:.3f}%")

        if error_rate < 0.1:
            print("✓ Excelente: < 0.1%")
        elif error_rate < 0.5:
            print("✓ Bueno: < 0.5%")
        elif error_rate < 1:
            print("⚠ Aceptable: < 1%")
        else:
            print("✗ Inaceptable: > 1%")

    def mean_time_between_failures(self):
        """
        MTBF: Promedio de tiempo entre fallos

        EJEMPLO:
        - 10 fallos en 100 horas de operación
        - MTBF = 100 / 10 = 10 horas
        → Fallo cada 10 horas

        Mayor MTBF = Más confiable
        """
        uptime_hours = 1000
        num_failures = 10

        mtbf = uptime_hours / num_failures
        print(f"MTBF: {mtbf} horas entre fallos")

        return mtbf

    def recovery_time(self):
        """
        RECOVERY TIME: ¿Cuánto tarda en recuperarse?

        EJEMPLO:
        - Fallo detectado: 14:00:00
        - Sistema recuperado: 14:02:30
        - Recovery time: 150 segundos
        """
        detection_time = 14.0  # 14:00
        recovery_time = 14.042  # 14:02:30

        downtime = (recovery_time - detection_time) * 60 * 60  # segundos
        print(f"Downtime: {downtime:.0f} segundos ({downtime/60:.1f} minutos)")

        return downtime

    def consistency_check(self):
        """
        CONSISTENCY: ¿Da misma respuesta para mismo input?

        Importante para debugging
        """

        def query_agent(input_data):
            # Agente responde
            return "response"

        # Hacer same query 10 veces
        input_data = "What is 2+2?"
        responses = set()

        for i in range(10):
            response = query_agent(input_data)
            responses.add(response)

        if len(responses) == 1:
            print("✓ Determinista: Siempre da misma respuesta")
        else:
            print(f"⚠ No-determinista: Da {len(responses)} respuestas diferentes")


# ═════════════════════════════════════════════════════════════════
# RESUMEN: TABLA DE MÉTRICAS
# ═════════════════════════════════════════════════════════════════

print("""
MÉTRICA               FÓRMULA              IDEAL       CUÁNDO USAR
──────────────────────────────────────────────────────────────────
EFECTIVIDAD:
Accuracy             (TP+TN)/Total        ↑ Alto      Clases balanceadas
Precision            TP/(TP+FP)           ↑ Alto      Falsos pos. costosos
Recall               TP/(TP+FN)           ↑ Alto      Falsos neg. costosos
F1-Score             Promedio             ↑ Alto      Balance importante

EFICIENCIA:
Latency (P95)        Percentil 95%        ↓ Bajo      User experience
Throughput (RPS)     Req/segundo          ↑ Alto      Capacidad
Memory usage         MB / % total         ↓ Bajo      Escalabilidad
Cost/op              Dinero/request       ↓ Bajo      APIs pagas

ROBUSTEZ:
Error rate           Fallos/total         ↓ <0.1%     Confiabilidad
MTBF                 Horas/fallo          ↑ Alto      Disponibilidad
Recovery time        Seg hasta funcionar   ↓ Bajo      Tolerancia fallos
Consistency          % mismas respuestas   ↑ 100%      Debugging
──────────────────────────────────────────────────────────────────
""")
```

### 1.2 Elección de Métricas

```python
class ChooseMetrics:
    """
    ¿QUÉ MÉTRICAS USAR?

    REGLA DE ORO:
    Las métricas deben alinearse con OBJETIVOS DE NEGOCIO

    NO elijas arbitrariamente
    """

    @staticmethod
    def case_email_spam_filter():
        """
        CASO: Filtro de spam de email

        OBJETIVOS:
        1. No dejar pasar spam (alta recall)
        2. No marcar email legítimo como spam (alta precision)
        3. Responder rápido (baja latencia)

        MÉTRICAS:
        ✓ Recall: Detecta 95%+ de spam
        ✓ Precision: Solo 1% falsas alarmas
        ✓ Latency P95: < 100ms
        ✓ Throughput: > 10000 RPS
        """
        pass

    @staticmethod
    def case_medical_diagnosis():
        """
        CASO: Agente diagnosticador médico

        OBJETIVOS:
        1. No perder ninguna enfermedad crítica (recall >> precision)
        2. Respuestas consistentes (doctors revisarán)
        3. NO importa tanto la velocidad (es medicina, no urgente)

        MÉTRICAS:
        ✓ Recall: ≥ 98% (No perder enfermedades)
        ✓ Consistency: 100% (Determinista)
        ✓ Robustness: 99.99% uptime
        ✗ Latency: No importante
        ✗ Throughput: No importante
        """
        pass

    @staticmethod
    def case_autonomous_vehicles():
        """
        CASO: Agente conducción autónoma

        OBJETIVOS:
        1. Máxima seguridad (casi 100% correcto)
        2. Muy bajo latency (decisiones en ms)
        3. Máxima robustez (no puede fallar)

        MÉTRICAS:
        ✓ Accuracy: > 99.9%
        ✓ Latency P99: < 50ms
        ✓ Error rate: < 0.001%
        ✓ MTBF: > 1000000 horas
        ✓ Adversarial robustness: Resiste ataques
        ✗ Cost: No importante
        """
        pass
```

---

## <a name="módulo-2"></a>Módulo 2: Benchmarks y Datasets

### 2.1 Creando Buen Benchmark

```python
class BenchmarkDesign:
    """
    UN BENCHMARK es un CONJUNTO DE PRUEBAS
    que permite medir desempeño de forma estándar y reproducible
    """

    def __init__(self):
        self.test_cases = []
        self.expected_outputs = []

    # ───────────────────────────────────────────────────────────
    # CARACTERÍSTICA 1: REPRESENTATIVO
    # ───────────────────────────────────────────────────────────

    def create_representative_benchmark(self):
        """
        El benchmark debe cubrir CASOS TÍPICOS

        EJEMPLO: Spam filter
        - 60% emails legítimos normales
        - 30% spam obvio
        - 7% spam sofisticado
        - 3% edge cases (emails muy cortos, etc.)

        IGUAL A la distribución en PRODUCCIÓN
        """

        benchmark_spam = {
            'normal_legitimate': 600,      # 60%
            'obvious_spam': 300,           # 30%
            'sophisticated_spam': 70,      # 7%
            'edge_cases': 30                # 3%
        }

        total = sum(benchmark_spam.values())
        print(f"Benchmark total: {total} casos")
        print("Distribución representa mundo real ✓")

    # ───────────────────────────────────────────────────────────
    # CARACTERÍSTICA 2: DESAFIANTE
    # ───────────────────────────────────────────────────────────

    def create_challenging_benchmark(self):
        """
        El benchmark debe SER DIFÍCIL

        NO: Todos los agentes sacan > 99%
        SÍ: Diferencia entre agentes buenos y malos
        """

        # ✗ BENCHMARK FÁCIL (malo):
        easy_cases = [
            ("Compra viagra aquí", "SPAM"),
            ("Hola, ¿cómo estás?", "NOT_SPAM"),
            ("GANAR MILLONES AHORA", "SPAM"),
        ]

        # Agente A: 100% accuracy (trivial!)
        # Agente B: 100% accuracy (trivial!)
        # No podemos distinguir calidad

        # ✓ BENCHMARK DIFÍCIL (bueno):
        hard_cases = [
            ("Únete a nuestro programa de loyalidad", "?"),  # Podría ser
            ("Te ofrezco excelentes resultados en marketing", "?"),  # Ambiguo
            ("Cambio de política en nuestro servicio", "?"),  # Legítimo o spam?
        ]

        # Agente A: 85% accuracy
        # Agente B: 92% accuracy
        # Podemos ver diferencia

    # ───────────────────────────────────────────────────────────
    # CARACTERÍSTICA 3: REPRODUCIBLE
    # ───────────────────────────────────────────────────────────

    def create_reproducible_benchmark(self):
        """
        MISMOS RESULTADOS cada vez que ejecuto

        Requisitos:
        1. Fijar random seed
        2. Documentar exactamente las pruebas
        3. Usar datos públicos o guardados
        """

        import random
        import numpy as np

        # Fijar seeds para reproducibilidad
        random.seed(42)
        np.random.seed(42)

        # Generar benchmark (determinístico ahora)
        benchmark_cases = []
        for i in range(1000):
            case = {
                'email': f"email_{i}",
                'is_spam': random.choice([True, False])
            }
            benchmark_cases.append(case)

        # Próxima ejecución con seed=42 dará EXACTAMENTE lo mismo
        print("✓ Reproducible: Mismos resultados siempre")

    # ───────────────────────────────────────────────────────────
    # CARACTERÍSTICA 4: INTERPRETABLE
    # ───────────────────────────────────────────────────────────

    def create_interpretable_benchmark(self):
        """
        Fácil de entender DÓNDE FALLA

        MALO: "Accuracy 92%"
        BUENO:
        """

        results = {
            'overall_accuracy': '92%',
            'breakdown': {
                'legitimate_emails': '98% accuracy',
                'obvious_spam': '99% accuracy',
                'sophisticated_spam': '75% accuracy',  # ← DÉBIL AQUÍ
                'edge_cases': '60% accuracy',          # ← MUY DÉBIL
            },
            'error_analysis': {
                'false_negatives': 15,  # Spam no detectado
                'false_positives': 8,   # Legítimos marcados spam
            }
        }

        print("""
        ANÁLISIS DETALLADO:
        - Muy bueno con spam obvio
        - Malo con spam sofisticado ← MEJORA AQUÍ
        - Muy malo con edge cases ← FOCO FUTURO
        """)

        return results
```

### 2.2 Datasets Públicos

```python
class PublicDatasets:
    """
    Datasets existentes para evaluar agentes
    """

    @staticmethod
    def text_classification():
        """
        CLASIFICACIÓN DE TEXTO
        """
        print("""
        Dataset: IMDB
        - 50,000 reviews de películas
        - Etiquetas: Positivo/Negativo
        - Tarea: Sentiment analysis
        - Baseline: 88% accuracy

        Dataset: 20 Newsgroups
        - 18,846 documentos de noticias
        - 20 categorías
        - Tarea: Clasificación temática
        - Baseline: 75% accuracy
        """)

    @staticmethod
    def question_answering():
        """
        RESPUESTA DE PREGUNTAS
        """
        print("""
        Dataset: SQuAD (Stanford Question Answering Dataset)
        - 100,000+ preguntas sobre Wikipedia
        - Formato: Pregunta + Párrafo + Respuesta
        - Tarea: Encontrar respuesta en texto
        - Métrica: F1-score
        - SOTA: 95.5+ F1-score

        Dataset: Natural Questions
        - 300,000 preguntas reales de usuarios
        - Múltiples párrafos candidatos
        - Tarea: Ranking de párrafos
        """)

    @staticmethod
    def dialogue_systems():
        """
        SISTEMAS DE DIÁLOGO
        """
        print("""
        Dataset: BLEU scores
        - Para evaluar traducción/paráfrasis
        - Compara contra referencias
        - Rango: 0-100 (100 = perfecto)

        Dataset: ROUGE scores
        - Para resúmenes
        - Overlap de palabras vs referencia

        Dataset: Human Evaluation
        - Lo mejor: Personas califican respuestas
        - Caro pero definitivo
        """)
```

---

## <a name="módulo-3"></a>Módulo 3: Testing Funcional

### 3.1 Unit Tests para Agentes

```python
import unittest

class AgentTests(unittest.TestCase):
    """
    TESTING de componentes individuales del agente
    """

    def setUp(self):
        """Preparación antes de cada test"""
        self.agent = SimpleAgent(name="TestAgent")

    def test_perception_works(self):
        """
        TEST: ¿Percibe correctamente?
        """
        environment = {'temperature': 25, 'light': 100}

        percepts = self.agent.perceive(environment)

        # Asegurarse que percibió
        self.assertIn('temperature', percepts)
        self.assertEqual(percepts['temperature'], 25)

    def test_reasoning_with_data(self):
        """
        TEST: ¿Razona correctamente?
        """
        test_data = {'temperature': 30}

        decision = self.agent.reason(test_data)

        # Si temperatura > 28, debería decidir enfriar
        self.assertEqual(decision, 'cool_down')

    def test_action_execution(self):
        """
        TEST: ¿Ejecuta acciones correctamente?
        """
        # Si decide enfriar, debería activar AC
        result = self.agent.act('cool_down')

        self.assertTrue(result['success'])
        self.assertEqual(result['action'], 'ac_on')

    def test_state_updates(self):
        """
        TEST: ¿Actualiza estado correctamente?
        """
        initial_state = self.agent.state.copy()

        # Ejecutar una acción
        self.agent.step({'temperature': 30})

        # Estado debería cambiar
        self.assertNotEqual(self.agent.state, initial_state)


class MultiAgentTests(unittest.TestCase):
    """
    TESTING de interacción entre agentes
    """

    def test_communication_delivery(self):
        """
        TEST: ¿Se entregan mensajes?
        """
        agentA = Agent('A')
        agentB = Agent('B')

        # A envía mensaje a B
        message = {'content': 'Hello', 'to': 'B'}
        agentA.send(message)

        # B debería recibir
        received = agentB.inbox.get_nowait()
        self.assertEqual(received['content'], 'Hello')

    def test_coordination_protocol(self):
        """
        TEST: ¿Protocolo de coordinación funciona?
        """
        # Dos agentes deben coordinar acceso a recurso
        resource = SharedResource()
        agentA = Agent('A')
        agentB = Agent('B')

        # A adquiere recurso
        success_a = agentA.acquire(resource)
        self.assertTrue(success_a)

        # B no debería poder adquirir (A lo tiene)
        success_b = agentB.acquire(resource, timeout=1)
        self.assertFalse(success_b)

        # A libera
        agentA.release(resource)

        # Ahora B debería poder adquirir
        success_b = agentB.acquire(resource)
        self.assertTrue(success_b)


# Ejecutar tests:
# python -m unittest discover
```

### 3.2 Integration Tests

```python
class IntegrationTests(unittest.TestCase):
    """
    TESTING de TODO el sistema junto
    """

    def setUp(self):
        """Crear sistema completo"""
        self.system = MultiAgentSystem()
        self.system.add_agent(ProducerAgent('P1'))
        self.system.add_agent(ConsumerAgent('C1'))

    def test_end_to_end_transaction(self):
        """
        TEST: ¿Flujo completo funciona?

        Escenario: Productor crea item, consumidor lo consume
        """
        # Productor crea item
        item = self.system.agents['P1'].produce('data')
        self.assertIsNotNone(item)

        # Sistema distribuye
        self.system.distribute()

        # Consumidor recibió
        self.assertTrue(self.system.agents['C1'].has_item(item))

    def test_fault_tolerance(self):
        """
        TEST: ¿Sistema tolera fallos?
        """
        # Sistema funciona inicialmente
        result1 = self.system.process()
        self.assertTrue(result1)

        # Simular fallo de un agente
        self.system.agents['P1'].fail()

        # Sistema continúa (otros agentes trabajan)
        result2 = self.system.process()
        # Debería funcionar parcialmente
        self.assertTrue(result2 or len(self.system.agents) > 1)
```

---

## <a name="módulo-4"></a>Módulo 4: Debugging y Monitoreo

### 4.1 Logging Estratégico

```python
import logging
from datetime import datetime

class AgentLogger:
    """
    LOGGING para entender QUÉ HACE el agente
    """

    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.logger = logging.getLogger(agent_name)

    def log_perception(self, percepts):
        """Log: Qué percibió"""
        self.logger.info(f"PERCEPTS: {percepts}")

    def log_decision(self, decision, reasoning):
        """Log: Qué decidió y por qué"""
        self.logger.info(f"DECISION: {decision} (reason: {reasoning})")

    def log_action(self, action, result):
        """Log: Qué hizo y resultado"""
        self.logger.info(f"ACTION: {action} → {result}")

    def log_error(self, error, context):
        """Log: Errores con contexto"""
        self.logger.error(f"ERROR: {error} in {context}")

    # Ejemplo de uso:
    def example(self):
        """
        Logs de una sesión típica:

        INFO: PERCEPTS: {'temp': 25, 'light': 100}
        INFO: DECISION: cool_down (reason: temp > 24)
        INFO: ACTION: turn_on_ac → success
        ERROR: CONNECTION_TIMEOUT to AgentB in coordination_step
        """
        pass


# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),  # Guardar en archivo
        logging.StreamHandler()             # También en consola
    ]
)

# ANÁLISIS DE LOGS:
print("""
CUÁNDO REVISAR LOGS:

1. Comportamiento extraño:
   "¿Por qué el agente hizo X?"
   → Revisar DECISION logs

2. Rendimiento lento:
   "¿Por qué tarda tanto?"
   → Revisar timestamps entre eventos

3. Error intermitente:
   "¿Cuándo falla exactamente?"
   → Buscar ERROR logs cercanos

4. Decisión incorrecta:
   "¿Cómo llegó a esa conclusión?"
   → Ver PERCEPTS → DECISION chain
""")
```

### 4.2 Monitoreo en Producción

```python
class ProductionMonitoring:
    """
    MONITOREO DE AGENTE EN PRODUCCIÓN
    """

    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.metrics = {
            'requests_total': 0,
            'requests_success': 0,
            'requests_error': 0,
            'avg_latency': 0,
            'last_error': None,
            'uptime': 0
        }

    def track_request(self, success, latency, error=None):
        """Rastrear cada request"""
        self.metrics['requests_total'] += 1

        if success:
            self.metrics['requests_success'] += 1
        else:
            self.metrics['requests_error'] += 1
            self.metrics['last_error'] = error

        # Actualizar latency promedio
        old_avg = self.metrics['avg_latency']
        self.metrics['avg_latency'] = (
            (old_avg * (self.metrics['requests_total'] - 1) + latency) /
            self.metrics['requests_total']
        )

    def alert_if_threshold_exceeded(self):
        """Alerta si métricas salen de control"""

        alerts = []

        # Error rate > 1%
        error_rate = (self.metrics['requests_error'] /
                      self.metrics['requests_total'] * 100)
        if error_rate > 1:
            alerts.append(f"⚠️  Error rate {error_rate:.1f}% (umbral: 1%)")

        # Latency > 500ms
        if self.metrics['avg_latency'] > 500:
            alerts.append(f"⚠️  Latency {self.metrics['avg_latency']:.0f}ms "
                         f"(umbral: 500ms)")

        # No responde en 10 minutos
        # ...

        return alerts

    def generate_report(self):
        """Generar reporte de salud"""
        print(f"""
        HEALTH REPORT: {self.agent_name}
        ─────────────────────────────────────
        Total requests: {self.metrics['requests_total']}
        Success: {self.metrics['requests_success']} ✓
        Errors: {self.metrics['requests_error']} ✗
        Error rate: {self.metrics['requests_error']/self.metrics['requests_total']*100:.2f}%
        Avg latency: {self.metrics['avg_latency']:.0f}ms
        Last error: {self.metrics['last_error']}
        ─────────────────────────────────────
        Alerts: {self.alert_if_threshold_exceeded() or 'None'}
        """)
```

---

## Resumen Completo

```
EVALUACIÓN Y TESTING = Verificar que agente funciona como se espera

NIVELES:

1. MÉTRICAS
   → Cuantificar desempeño
   → Ejemplos: Accuracy, Latency, Error rate

2. TESTS
   → Automatizar verificación
   → Unit tests, Integration tests

3. BENCHMARKS
   → Comparar múltiples agentes
   → Conjunto de pruebas estándar

4. MONITOREO
   → Vigilar en producción
   → Alertas si algo falla

TODO JUNTO = CONFIANZA EN AGENTE
```

