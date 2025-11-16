# Ejemplos Prácticos: Evaluación y Testing de Agentes IA

> **Aprende a evaluar, testear y debuggear agentes IA de forma sistemática**

## 📂 Contenidos

Este directorio contiene 6 ejemplos prácticos funcionales que implementan los conceptos del módulo de evaluación y testing:

```
evaluacion/
├── 01_metricas_desempeno.py      (200+ líneas)  → Módulo 1
├── 02_benchmarks_datasets.py     (280+ líneas)  → Módulo 2
├── 03_testing_agentes.py         (340+ líneas)  → Módulo 3
├── 04_testing_comportamiento.py  (310+ líneas)  → Módulo 4
├── 05_debugging_agentes.py       (280+ líneas)  → Módulo 5
├── 06_llm_como_juez.py          (320+ líneas)  → Módulo 6
├── GUIA_EVALUACION_AGENTES.md    (Completa)   → Guía Didáctica
└── README.md                     (Este archivo)
```

**Total: ~1,900 líneas de código funcional + documentación completa**

---

## 🚀 Inicio Rápido

### 1. Ver contenidos

```bash
ls -la /home/rojaldo/cursos/agents/ejemplos/evaluacion/
```

### 2. Ejecutar Ejemplo 1 (sin dependencias externas)

```bash
python /home/rojaldo/cursos/agents/ejemplos/evaluacion/01_metricas_desempeno.py
```

### 3. Ejecutar otros ejemplos

```bash
# Ejemplo 2: Benchmarks
python 02_benchmarks_datasets.py

# Ejemplo 3: Testing
python 03_testing_agentes.py

# Ejemplo 4: Comportamiento
python 04_testing_comportamiento.py

# Ejemplo 5: Debugging
python 05_debugging_agentes.py

# Ejemplo 6: LLM Juez (requiere Ollama)
python 06_llm_como_juez.py
```

### 4. Leer guía completa

```bash
cat GUIA_EVALUACION_AGENTES.md
```

---

## 📖 Descripción de Módulos

### Módulo 1: Métricas de Desempeño (01_metricas_desempeno.py)

Implementa framework integral de métricas:
- **Efectividad**: Accuracy, Precision, Recall, F1-Score, AUC-ROC
- **Eficiencia**: Latencia (p50, p95, p99), Throughput, CPU/Memoria
- **Robustez**: Error Rate, MTBF (Mean Time Between Failures), Recovery Time
- **Seguridad**: Tasa de violación, Fairness Score

**Conceptos**: Matriz de confusión, percentiles, distribuciones

---

### Módulo 2: Benchmarks y Datasets (02_benchmarks_datasets.py)

Gestión completa de benchmarks:
- Crear datasets con ejemplos de evaluación
- Anotación por múltiples anotadores (inter-annotator agreement)
- Medir Cohen's Kappa (debe ser > 0.80)
- Detectar y mitigar sesgo (selection bias, annotation bias)
- Dividir en train/val/test manteniendo proporciones

**Conceptos**: Anotación, concordancia, versionado de datasets

---

### Módulo 3: Testing de Agentes (03_testing_agentes.py)

Testing en múltiples niveles:
- **Unit Tests**: Componentes individuales (rápido)
- **Integration Tests**: Múltiples componentes juntos
- **Functional Tests**: Casos de uso end-to-end
- **Stress Tests**: Bajo carga extrema (1000+ requests)

**Conceptos**: Test suites, assertions, mocks, code coverage

---

### Módulo 4: Testing de Comportamiento (04_testing_comportamiento.py)

Testing de propiedades y comportamiento:
- **Propiedades invariantes**: Lo que SIEMPRE debe ser verdadero
- **Edge cases**: Valores límite (vacío, máximo, inválido)
- **Consistency**: Determinismo y reproducibilidad
- **Property-based testing**: Genera datos automáticamente

**Conceptos**: Invariantes, generadores, seeds, boundary values

---

### Módulo 5: Debugging de Agentes (05_debugging_agentes.py)

Herramientas y técnicas de debugging:
- **Logging estratégico**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Snapshots de estado**: Captura estado en puntos específicos
- **Profiling**: Encuentra qué funciones tardan más
- **Reproducción**: Replay de ejecuciones para debugging offline
- **Post-mortem**: Análisis de errores después de ocurrir

**Conceptos**: Event logging, profiling, state inspection, tracing

---

### Módulo 6: LLMs como Jueces (06_llm_como_juez.py)

Evaluación automática con LLMs (vía Ollama):
- Usar LLM para evaluación rápida y escalable
- Métricas cualitativas (relevancia, exactitud) vs cuantitativas
- Variabilidad en evaluaciones (temperatura, prompts)
- Calibración LLM vs evaluación manual
- Mitigación de sesgos

**Conceptos**: Prompts estructurados, temperatura, Cohen's Kappa, ensemble

---

## 🎯 Flujo de Aprendizaje

```
SEMANA 1: Fundamentos
├─ Lee GUIA_EVALUACION_AGENTES.md (secciones 1-2)
├─ Ejecuta 01_metricas_desempeno.py
└─ Experimenta modificando valores

SEMANA 2: Benchmarks y Testing
├─ Lee secciones 2-3 de guía
├─ Ejecuta 02_benchmarks_datasets.py
├─ Ejecuta 03_testing_agentes.py
└─ Practica: Crea tu propio benchmark

SEMANA 3: Comportamiento y Debugging
├─ Lee secciones 4-5 de guía
├─ Ejecuta 04_testing_comportamiento.py
├─ Ejecuta 05_debugging_agentes.py
└─ Practica: Debuggea un escenario real

SEMANA 4: Evaluación Avanzada
├─ Lee sección 6 de guía
├─ Configura Ollama (instrucciones abajo)
├─ Ejecuta 06_llm_como_juez.py
└─ Proyecto: Evalúa tu propio agente
```

---

## ⚙️ Setup Ollama (Opcional)

Para ejemplos con LLM, necesitas Ollama:

```bash
# 1. Instala Ollama (https://ollama.ai)

# 2. Inicia servicio (en terminal separada)
ollama serve

# 3. Descarga modelo (en otra terminal)
ollama pull mistral

# 4. Verifica
curl http://localhost:11434/api/generate -d '{"model":"mistral","prompt":"test"}'
```

Sin Ollama: Los ejemplos funcionan en modo simulación automático.

---

## 📊 Características de los Ejemplos

✓ **Completamente funcionales**: No requieren datos externos
✓ **Autodocumentados**: Código claro con comentarios
✓ **Didácticos**: Diseñados para aprender
✓ **Modulares**: Código reutilizable en tus proyectos
✓ **Sin dependencias pesadas**: Funcionan con dependencias mínimas
✓ **Con salidas visuales**: Formatos claros y fáciles de entender

---

## 📚 Recursos

- **GUIA_EVALUACION_AGENTES.md**: Guía didáctica completa (recomendado leer primero)
- **Código comentado**: Cada ejemplo tiene docstrings y comentarios explicativos
- Ejemplos en este directorio

---

## ✅ Checklist de Ejecución

```
□ 01_metricas_desempeno.py      ✓ (independiente)
□ 02_benchmarks_datasets.py     ✓ (independiente)
□ 03_testing_agentes.py         ✓ (independiente)
□ 04_testing_comportamiento.py  ✓ (independiente)
□ 05_debugging_agentes.py       ✓ (independiente)
□ 06_llm_como_juez.py          ✓ (con/sin Ollama)
□ GUIA_EVALUACION_AGENTES.md    ✓ (lectura recomendada)
```

---

## 📖 Guía de Uso de Cada Módulo

### Para Aprender
1. Lee la sección correspondiente en GUIA_EVALUACION_AGENTES.md
2. Ejecuta el ejemplo
3. Modifica valores para experimentar
4. Estudia el código

### Para Aplicar a Tu Proyecto
1. Copia el código como base
2. Adáptalo a tu agente específico
3. Ejecuta para validar
4. Integra en CI/CD

### Para Referencia
- Usa como template para tus propios tests
- Consulta cuando necesites específicas

---

## 🎓 Conclusión

Después de completar estos ejemplos:
- Entenderás evaluación rigurosa de agentes
- Podrás escribir tests en múltiples niveles
- Sabrás cómo debuggear comportamientos inesperados
- Estarás listo para producción

**Próximo paso**: Aplicar estas técnicas a tu agente.

---

**Versión**: 1.0
**Fecha**: 2024-11-13
**Total de código**: ~1,900 líneas
**Tiempo estimado**: 4 semanas

¡Feliz aprendizaje!
