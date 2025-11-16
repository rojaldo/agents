# Guía Didáctica: Evaluación y Testing de Agentes IA

## 📚 Introducción

La evaluación rigurosa de agentes es crítica para garantizar que funcionen correctamente, de forma confiable y segura. Esta guía cubre los conceptos fundamentales y proporciona ejemplos prácticos usando LangChain y Ollama.

## 🎯 Objetivos de Aprendizaje

Después de completar esta guía, podrás:

- Definir métricas apropiadas para evaluar agentes
- Crear benchmarks de evaluación con anotación manual
- Escribir tests a múltiples niveles (unit, integration, functional, stress)
- Debuggear comportamientos inesperados
- Usar LLMs para evaluación automática

## 📖 Estructura

```
01_metricas_desempeno.py      → Métricas de efectividad, eficiencia, robustez
02_benchmarks_datasets.py     → Crear y gestionar benchmarks
03_testing_agentes.py         → Unit, integration, functional, stress tests
04_testing_comportamiento.py  → Testing de propiedades e invariantes
05_debugging_agentes.py       → Logging, profiling, reproducción de ejecuciones
06_llm_como_juez.py          → LLMs como evaluadores automáticos
```

---

## 1️⃣ Módulo 1: Métricas de Desempeño

### Concepto

Las métricas nos permiten **medir objetivamente** qué tan bien funciona un agente.

```
┌─────────────────────────────────────────────────────────┐
│                    MÉTRICAS DE AGENTES                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  EFECTIVIDAD: ¿QUÉ TAN BIEN HACE SU TRABAJO?          │
│  ├─ Accuracy: % de predicciones correctas             │
│  ├─ Precision: De los positivos, cuántos acertó       │
│  ├─ Recall: De los positivos reales, cuántos encontró │
│  ├─ F1-Score: Balance entre precision y recall        │
│  └─ AUC-ROC: Robustez a diferentes umbrales           │
│                                                         │
│  EFICIENCIA: ¿CUÁNTO CUESTA EN RECURSOS?              │
│  ├─ Latencia: Tiempo respuesta (p95, p99)            │
│  ├─ Throughput: Requests por segundo                  │
│  ├─ CPU: Uso de procesador                           │
│  ├─ Memoria: RAM consumida                           │
│  └─ Costo: Dinero por query (si APIs pagas)          │
│                                                         │
│  ROBUSTEZ: ¿QUÉ TAN BIEN MANEJA FALLOS?              │
│  ├─ Error Rate: % de requests que fallan              │
│  ├─ MTBF: Tiempo promedio entre fallos               │
│  ├─ Recovery Time: Cuánto tarda en recuperarse        │
│  └─ Consistency: Respuestas consistentes              │
│                                                         │
│  SEGURIDAD: ¿ES SEGURO USARLO?                        │
│  ├─ Violation Rate: Cuántas veces violó restricción   │
│  ├─ Fairness: Equidad entre grupos                    │
│  └─ Adversarial Robustness: Resistencia a ataques    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Ejemplo Práctico

```bash
python 01_metricas_desempeno.py
```

Esto demuestra:
- Calcular matriz de confusión (TP, TN, FP, FN)
- Computar accuracy, precision, recall, F1-score
- Medir latencias y percentiles (p95, p99)
- Evaluar robustez con múltiples intentos

### Caso de Uso Real

**Agente Q&A Empresa:**
```
✓ Accuracy: 92% (busca balance)
✓ Latencia p95: 150ms (aceptable)
✓ Error Rate: 0.1% (muy bueno)
✓ Fairness: 0.95/1.0 (equitativo)

DECISIÓN: Deploy en producción
```

---

## 2️⃣ Módulo 2: Benchmarks y Datasets

### Concepto

Un **benchmark** es un conjunto de ejemplos para evaluar agentes de forma justa y reproducible.

```
┌─────────────────────────────────────────────────────────┐
│              ANATOMÍA DE UN BENCHMARK BUENO             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  REPRESENTATIVO                                         │
│  └─ Cubre casos típicos Y edge cases                  │
│  └─ Distribucion similar a producción                │
│  └─ Suficientemente grande (1000+ ejemplos)          │
│                                                         │
│  DESAFIANTE                                            │
│  └─ No trivial de completar                          │
│  └─ Discrimina entre agentes buenos y malos          │
│  └─ Evita saturación (todo >99%)                     │
│                                                         │
│  REPRODUCIBLE                                          │
│  └─ Resultados consistentes                          │
│  └─ Random seeds fijos                               │
│  └─ Documentación clara                              │
│                                                         │
│  INTERPRETABLE                                         │
│  └─ Fácil analizar resultados                        │
│  └─ Errores trazables                                │
│  └─ Fallos informativos                              │
│                                                         │
│  PÚBLICO O COMPARTIBLE                                │
│  └─ Útil científicamente                             │
│  └─ Facilita colaboración                            │
│  └─ Tracking de progreso                             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Anotación por Múltiples Evaluadores

**¿Por qué múltiples anotadores?**
- Detecta ambigüedades en los ejemplos
- Mide la calidad del dataset
- Proporciona verdad consensuada

**Cohen's Kappa: Medida de Acuerdo**
```
Kappa = 1.0    → Acuerdo perfecto
Kappa > 0.80   → Excelente (usar dataset)
Kappa 0.60-0.80 → Sustancial (mejorar instrucciones)
Kappa < 0.60   → Pobre (revisar dataset)
```

### Ejemplo Práctico

```bash
python 02_benchmarks_datasets.py
```

Esto demuestra:
- Crear dataset con ejemplos
- Anotar por múltiples anotadores
- Calcular Cohen's Kappa
- Medir sesgo en el benchmark
- Dividir en train/val/test

---

## 3️⃣ Módulo 3: Testing de Agentes

### Pirámide de Testing

```
                    ▲
                   / \
                  /   \
                 / S.T.\        Stress Tests (lenta, integral)
                /-------\       - 1000 requests
               /         \      - Uso de memoria
              /  I.T.    \      Integration Tests (medianos)
             /___________\      - Multi-componentes
            /             \
           / U.T.          \    Unit Tests (rápidos)
          /_________________\   - Componentes individuales
          Velocidad ←→ Cobertura
```

### Tipos de Tests

| Tipo | Scope | Velocidad | Uso |
|------|-------|-----------|-----|
| **Unit** | Función individual | ⚡ 1-10ms | Debugging rápido |
| **Integration** | Múltiples componentes | ⏱️ 10-100ms | Verificar interfaces |
| **Functional** | End-to-end | 🐌 100ms-10s | Validar casos uso |
| **Stress** | Bajo carga extrema | 🐌🐌 10s+ | Límites del sistema |

### Ejemplo Práctico

```bash
python 03_testing_agentes.py
```

Esto demuestra:
- Escribir unit tests con fixtures
- Tests de integración
- Functional tests (casos de uso)
- Stress tests (muchas queries)

---

## 4️⃣ Módulo 4: Testing de Comportamiento

### Propiedades Invariantes

```
Un invariante es una propiedad que SIEMPRE debe ser verdadera
```

**Ejemplos:**
```python
def propiedad_nunca_excede_budget():
    """Agente nunca excede su presupuesto"""
    assert agent.spent <= agent.max_budget

def propiedad_encuentra_si_existe():
    """Si objetivo existe, lo encuentra"""
    assert agent.find(target) == target

def propiedad_no_contradicion():
    """No contradice decisión previa sin razón"""
    assert consistent_decision_making()
```

### Edge Cases

```
Valores límite que deben manejar:
├─ Vacío: [], "", None
├─ Máximo: len(text) > 1M, 1000+ requests
├─ Inválido: tipos incorrectos, formatos rotos
└─ Combinatorios: interacciones inesperadas
```

### Ejemplo Práctico

```bash
python 04_testing_comportamiento.py
```

Esto demuestra:
- Property-based testing
- Edge cases y boundary values
- Tests de consistency
- Reproducibilidad con seeds

---

## 5️⃣ Módulo 5: Debugging de Agentes

### Técnicas de Logging

```
DEBUG    → Muy verbose, para desarrollo
INFO     → Información general importante
WARNING  → Algo inesperado
ERROR    → Problema serio, pero recoverable
CRITICAL → Fallo del sistema
```

### Herramientas de Debugging

```python
# 1. LOGGING ESTRATÉGICO
logger.debug(f"Decidiendo con: {percepts}")
logger.warning(f"Threat level alto: {threat}")
logger.error(f"Fallo en búsqueda: {error}")

# 2. SNAPSHOTS DE ESTADO
snapshot = {
    'beliefs': agent.beliefs,
    'goals': agent.goals,
    'health': agent.health,
    'timestamp': time.time()
}

# 3. PROFILING
profiler = cProfile.Profile()
profiler.enable()
agent.run()
profiler.disable()
stats = pstats.Stats(profiler)
stats.print_stats(10)  # Top 10 funciones

# 4. REPRODUCCIÓN
# Guardar todos los eventos + inputs/outputs
# Permite replay exacto para debugging offline
```

### Post-Mortem Analysis

```
Cuando falla en producción:
1. Recolectar datos (logs, traces, state snapshots)
2. Construir timeline de eventos
3. Identificar anomalía (cuándo cambió)
4. Rastrear causa raíz (qué causó cambio)
5. Proponer fix (cómo prevenir)
```

### Ejemplo Práctico

```bash
python 05_debugging_agentes.py
```

Esto demuestra:
- Configurar logging en múltiples niveles
- Capturar snapshots de estado
- Profiling de funciones
- Reproducción de ejecuciones

---

## 6️⃣ Módulo 6: LLMs como Jueces Evaluadores

### ¿Cuándo Usar LLM para Evaluación?

| Caso | ¿LLM? | ¿Manual? | Hybrid |
|------|-------|---------|--------|
| Presencia de palabra clave | ✓ | - | - |
| Relevancia/coherencia | ✓ | - | **✓** |
| Exactitud factual | - | ✓ | **✓** |
| Comparación pares | - | ✓ | - |
| Escala masiva | **✓** | - | - |

### Variabilidad en LLMs

```
Fuentes de variabilidad:
├─ Temperatura: 0.0 (determinístico) → 1.0 (aleatorio)
├─ Prompt phrasing: pequeños cambios = resultados diferentes
├─ Context window: qué información ve
├─ Modelo: diferentes LLMs, versiones
└─ Calibración: sesgos inherentes

Mitigación:
├─ Usa temperatura baja (0.1-0.3)
├─ Ejecuta múltiples trials
├─ Usa ensemble de LLMs
├─ Valida contra manual en muestra
└─ Implementa appeal process
```

### Calibración LLM vs Manual

```
Cohen's Kappa (LLM vs Humano):
< 0.60 → Pobre, requiere ajuste
0.60-0.80 → Aceptable, monitorear
> 0.80 → Bueno, usar en producción

Benchmarkiar en ~50-100 ejemplos
antes de producción
```

### Ejemplo Práctico

```bash
python 06_llm_como_juez.py
```

Esto demuestra:
- Diseñar prompts para evaluación
- Evaluar respuestas con LLM
- Comparar con evaluación manual
- Medir variabilidad vs temperatura

---

## 🚀 Ejemplos Combinados

### Flujo Completo: Evaluación de Agente

```
┌─────────────────────────────────────────────────────┐
│  1. CREAR BENCHMARK (Módulo 2)                      │
│     └─ 100 ejemplos anotados por 3 humanos         │
│     └─ Cohen's Kappa: 0.85 ✓                       │
├─────────────────────────────────────────────────────┤
│  2. DEFINIR MÉTRICAS (Módulo 1)                     │
│     └─ Efectividad: Accuracy, Precision, Recall    │
│     └─ Eficiencia: Latencia p95, Throughput        │
│     └─ Robustez: Error Rate, Recovery Time         │
├─────────────────────────────────────────────────────┤
│  3. ESCRIBIR TESTS (Módulos 3 & 4)                 │
│     └─ Unit tests: 50+ tests                       │
│     └─ Behavioral tests: propiedades invariantes    │
│     └─ Stress tests: 1000+ queries                 │
├─────────────────────────────────────────────────────┤
│  4. EJECUTAR EVALUACIÓN                             │
│     ├─ Tests: 95% pass ✓                           │
│     ├─ Accuracy: 92% ✓                             │
│     ├─ Latencia p95: 150ms ✓                       │
│     └─ Error Rate: 0.05% ✓                         │
├─────────────────────────────────────────────────────┤
│  5. DEBUGGEAR SI FALLA (Módulo 5)                  │
│     └─ Analizar logs y traces                      │
│     └─ Reproducir escenario problemático           │
│     └─ Usar profiler para encontrar cuello botella │
├─────────────────────────────────────────────────────┤
│  6. EVALUACIÓN CON LLM (Módulo 6)                  │
│     └─ Usar LLM para evaluación rápida (pre-screen)│
│     └─ Validar muestra con humanos                 │
│     └─ Correlación LLM vs Manual: 0.82 ✓           │
├─────────────────────────────────────────────────────┤
│  7. DEPLOY & MONITOREO                             │
│     └─ Setup métricas en producción                │
│     └─ Alertas si degrada                          │
│     └─ Validación periódica (cada mes)             │
└─────────────────────────────────────────────────────┘
```

---

## 📋 Checklist de Testing

```
ANTES DE PRODUCCIÓN:
□ ¿Definiste métricas claras?
□ ¿Tienes benchmark representativo (kappa > 0.80)?
□ ¿Pasaron todos los unit tests?
□ ¿Cobertura de código > 80%?
□ ¿Funciona bajo estrés (stress test ok)?
□ ¿Propiedades invariantes verificadas?
□ ¿Logs y debugging implementados?
□ ¿Evaluación LLM calibrada vs manual?
□ ¿SLAs definidos y monitoreados?
□ ¿Plan de rollback si falla?

REGULARMENTE EN PRODUCCIÓN:
□ Revisar métricas diariamente
□ Validar evaluación LLM cada mes
□ Tests de regresión con cada cambio
□ Post-mortem de incidentes
□ Actualizar benchmark (evitar data drift)
```

---

## 💡 Mejores Prácticas

### 1. Métricas

✓ **Alineadas con objetivos de negocio**
- No solo accuracy, también latencia y cost

✓ **Múltiples perspectivas**
- Efectividad, eficiencia, robustez

✓ **Computables eficientemente**
- Métricas que se pueden medir en tiempo real

✓ **Interpretables para stakeholders**
- Evita métricas matemáticas complejas

### 2. Benchmarks

✓ **Versionados**
```
benchmark_v1.0.json  → Original
benchmark_v1.1.json  → Agregado 50 ejemplos
benchmark_v2.0.json  → Rediseño completo
```

✓ **Documentados**
```
{
  "name": "qa_benchmark",
  "version": "1.0",
  "description": "Q&A en español",
  "num_examples": 1000,
  "annotation_guidelines": "...",
  "inter_annotator_agreement": {
    "cohen_kappa": 0.85,
    "annotators": 3
  }
}
```

✓ **Divididos correctamente**
```
Train: 70% (700 ejemplos)
Val: 15% (150 ejemplos)
Test: 15% (150 ejemplos, NUNCA vistos durante entrenamiento)
```

### 3. Testing

✓ **Automated en CI/CD**
```bash
# Cada commit
pytest test_suite/ --cov=src/ --cov-report=html
```

✓ **Determinístico**
```python
random.seed(42)
np.random.seed(42)
torch.manual_seed(42)
```

✓ **Coverage > 80%**
- Encuentra bugs antes de producción

### 4. Debugging

✓ **Estructura logs**
```json
{
  "timestamp": "2024-01-15T10:30:45Z",
  "level": "WARNING",
  "agent_id": "agent_001",
  "function": "decide",
  "message": "Low confidence in decision",
  "data": {"confidence": 0.35, "options": 5}
}
```

✓ **Reproducible**
- Guarda todos los inputs/outputs
- Permite replay exacto

### 5. Evaluación

✓ **Múltiples métodos**
- LLM rápido para grandes volúmenes
- Manual para validación y casos difíciles

✓ **Calibrado**
- Valida LLM contra manual regularmente
- Ajusta umbrales basado en datos reales

✓ **Monitoreado**
- Alertas si calibración se degrada
- Appeal process para usuarios

---

## 📚 Recursos Adicionales

### Tutoriales
- Ejemplos funcionales en `ejemplos/evaluacion/`
- Ejecuta: `python 01_metricas_desempeno.py`

### Referencias
- "The Art of Software Testing" - Myers
- "Benchmarking Machine Learning" - paper
- "AI Safety and Alignment" - paper

### Herramientas
- `pytest` - Framework de testing
- `pytest-cov` - Cobertura de código
- `cProfile` - Profiling de Python
- `logging` - Logging estándar

---

## ❓ Preguntas Frecuentes

**P: ¿Cuántas métricas necesito?**
R: Mínimo 5: accuracy, precision, recall, latencia p95, error rate

**P: ¿Qué tamaño debe tener mi benchmark?**
R: Mínimo 100 para desarrollo, 1000+ para producción

**P: ¿Cómo sé si mi agente está listo para producción?**
R: Cuando pasa todos los tests, métricas cumplen SLAs, y evaluación LLM está calibrada (kappa > 0.80)

**P: ¿Puedo usar solo LLM para evaluación?**
R: Para producción, valida contra manual en ~50-100 ejemplos primero

**P: ¿Con qué frecuencia debo validar?**
R: Diario en producción, mensual para re-calibración

---

## 🎓 Conclusión

La evaluación rigurosa es la diferencia entre:
- ✗ Agentes que "parecen" funcionar
- ✓ Agentes que **garantizadamente** funcionan

Usa estas técnicas sistemáticamente para construir agentes confiables.

---

**Última actualización:** 2024-11-13
**Autor:** Curso de Agentes de IA
