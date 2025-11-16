# Índice: Evaluación y Testing de Agentes IA

## 📚 Estructura Completa

Este módulo proporciona **una guía didáctica integral** con ejemplos funcionales para aprender evaluación y testing de agentes IA.

```
📁 evaluacion/
├── 📄 INDICE.md (este archivo)
├── 📄 README.md (inicio rápido)
├── 📘 GUIA_EVALUACION_AGENTES.md (guía didáctica completa)
│
├── 🐍 Ejemplos Funcionales:
│   ├── 01_metricas_desempeno.py (Módulo 1)
│   ├── 02_benchmarks_datasets.py (Módulo 2)
│   ├── 03_testing_agentes.py (Módulo 3)
│   ├── 04_testing_comportamiento.py (Módulo 4)
│   ├── 05_debugging_agentes.py (Módulo 5)
│   └── 06_llm_como_juez.py (Módulo 6)
```

---

## 🎯 Mapa de Aprendizaje

### Ruta de Aprendizaje Recomendada

```
┌─────────────────────────────────────────────────────────────┐
│ 1. COMIENZA AQUÍ                                            │
│    └─ Lee: README.md (5 min)                               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. LEE GUÍA COMPLETA (en secciones)                         │
│    ├─ Introducción & Módulo 1 (20 min)                     │
│    ├─ Módulos 2-3 (30 min)                                 │
│    ├─ Módulos 4-5 (30 min)                                 │
│    └─ Módulo 6 (25 min)                                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. EJECUTA EJEMPLOS (uno por uno)                           │
│    ├─ 01_metricas_desempeno.py (3 min)                     │
│    ├─ 02_benchmarks_datasets.py (4 min)                    │
│    ├─ 03_testing_agentes.py (5 min)                        │
│    ├─ 04_testing_comportamiento.py (4 min)                 │
│    ├─ 05_debugging_agentes.py (3 min)                      │
│    └─ 06_llm_como_juez.py (5 min con Ollama)              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. EXPERIMENTA Y ADAPTA                                     │
│    └─ Modifica ejemplos para tu caso de uso                │
└─────────────────────────────────────────────────────────────┘
```

---

## 📖 Descripción de Archivos

### README.md
**Lectura recomendada para comenzar**
- Inicio rápido
- Descripción brevde cada módulo
- Setup de Ollama
- FAQ

### GUIA_EVALUACION_AGENTES.md
**Guía didáctica completa y detallada**
- Introducción y conceptos
- Explicación detallada de cada módulo
- Diagramas ASCII para visualizar conceptos
- Casos de uso reales
- Mejores prácticas
- Checklist de testing

**Recomendación**: Lee en varias sesiones
- Sesión 1: Intro + Módulos 1-2
- Sesión 2: Módulos 3-4
- Sesión 3: Módulos 5-6 + Conclusión

---

## 🐍 Ejemplos de Código

### Módulo 1: Métricas de Desempeño
**Archivo**: `01_metricas_desempeno.py`

Aprenderás:
- Calcular accuracy, precision, recall, F1-score
- Medir latencias y percentiles
- Evaluar robustez
- Implementar framework integral

Ejecución:
```bash
python 01_metricas_desempeno.py
```

Tiempo: ~3 minutos

---

### Módulo 2: Benchmarks y Datasets
**Archivo**: `02_benchmarks_datasets.py`

Aprenderás:
- Crear datasets desde cero
- Anotar con múltiples anotadores
- Medir Cohen's Kappa (acuerdo entre anotadores)
- Detectar sesgo
- Dividir train/val/test

Ejecución:
```bash
python 02_benchmarks_datasets.py
```

Tiempo: ~4 minutos

---

### Módulo 3: Testing de Agentes
**Archivo**: `03_testing_agentes.py`

Aprenderás:
- Unit tests (componentes individuales)
- Integration tests (múltiples componentes)
- Functional tests (casos de uso)
- Stress tests (bajo carga)

Ejecución:
```bash
python 03_testing_agentes.py
```

Tiempo: ~5 minutos

---

### Módulo 4: Testing de Comportamiento
**Archivo**: `04_testing_comportamiento.py`

Aprenderás:
- Property-based testing
- Edge cases y boundary values
- Consistency y reproducibilidad
- Testing con seeds

Ejecución:
```bash
python 04_testing_comportamiento.py
```

Tiempo: ~4 minutos

---

### Módulo 5: Debugging de Agentes
**Archivo**: `05_debugging_agentes.py`

Aprenderás:
- Logging estratégico
- Snapshots de estado
- Profiling
- Reproducción de ejecuciones
- Post-mortem analysis

Ejecución:
```bash
python 05_debugging_agentes.py
```

Tiempo: ~3 minutos

---

### Módulo 6: LLMs como Jueces
**Archivo**: `06_llm_como_juez.py`

Aprenderás:
- Usar LLMs para evaluación automática
- Variabilidad en LLMs
- Calibración vs evaluación manual
- Mitigación de sesgos

Ejecución:
```bash
python 06_llm_como_juez.py
```

Tiempo: ~5 minutos (+ tiempo de Ollama si está disponible)

**Nota**: Funciona con o sin Ollama (modo simulación automático)

---

## ⏱️ Tiempo Total

| Actividad | Tiempo |
|-----------|--------|
| Leer README | 5 min |
| Leer GUIA completa | 2 horas |
| Ejecutar ejemplos | 25 min |
| Experimentar | Variable |
| **TOTAL** | **3 horas** |

---

## 🔗 Referencias Cruzadas

### Si quieres aprender sobre...

**Métricas**
- Leer: GUIA_EVALUACION_AGENTES.md (Módulo 1)
- Código: 01_metricas_desempeno.py
- Conceptos clave: Matriz de confusión, percentiles, MTBF

**Benchmarks**
- Leer: GUIA_EVALUACION_AGENTES.md (Módulo 2)
- Código: 02_benchmarks_datasets.py
- Conceptos clave: Cohen's Kappa, anotación, sesgo

**Testing**
- Leer: GUIA_EVALUACION_AGENTES.md (Módulo 3)
- Código: 03_testing_agentes.py
- Conceptos clave: Unit/Integration/Functional/Stress tests

**Comportamiento**
- Leer: GUIA_EVALUACION_AGENTES.md (Módulo 4)
- Código: 04_testing_comportamiento.py
- Conceptos clave: Invariantes, edge cases, reproducibilidad

**Debugging**
- Leer: GUIA_EVALUACION_AGENTES.md (Módulo 5)
- Código: 05_debugging_agentes.py
- Conceptos clave: Logging, profiling, tracing

**Evaluación con LLM**
- Leer: GUIA_EVALUACION_AGENTES.md (Módulo 6)
- Código: 06_llm_como_juez.py
- Conceptos clave: Prompts, calibración, variabilidad

---

## ✅ Checklist de Completitud

### Lectura
- [ ] README.md
- [ ] GUIA_EVALUACION_AGENTES.md (completa)

### Ejemplos (ejecutar)
- [ ] 01_metricas_desempeno.py
- [ ] 02_benchmarks_datasets.py
- [ ] 03_testing_agentes.py
- [ ] 04_testing_comportamiento.py
- [ ] 05_debugging_agentes.py
- [ ] 06_llm_como_juez.py

### Experimentación
- [ ] Modificar ejemplo 1 para tu agente
- [ ] Crear benchmark custom
- [ ] Escribir tests propios
- [ ] Implementar logging

---

## 🎓 Después de Completar

Una vez termines todos los módulos:

1. **Entiender qué evaluar**: Métricas apropiadas
2. **Cómo crear benchmarks**: Datasets de calidad (kappa > 0.80)
3. **Testing sistemático**: Unit → Integration → Functional → Stress
4. **Debugging efectivo**: Logging, profiling, reproducción
5. **Evaluación con LLM**: Uso de LLMs para evaluación rápida

---

## 💡 Consejos Prácticos

1. **No intentes todo a la vez**
   - Sigue el flujo de aprendizaje propuesto
   - Una semana por 2-3 módulos

2. **Experimenta con los ejemplos**
   - Modifica valores
   - Agrega casos de prueba
   - Adapta a tu agente

3. **Usa la guía como referencia**
   - Búscala cuando necesites refrescar conceptos
   - Vuelve a leer secciones relevantes

4. **Documenta tu progreso**
   - Toma notas mientras aprendes
   - Crea tu propio checklist de testing

---

## 📚 Recursos Adicionales

### En este directorio
- README.md - Inicio rápido
- GUIA_EVALUACION_AGENTES.md - Guía completa
- Código comentado de ejemplos

### Externo
- "The Art of Software Testing" - Glenford Myers
- "Continuous Integration" - Paul Duvall et al.
- Papers sobre benchmarking y fairness

---

## 🆘 Ayuda

**¿Por dónde empiezo?**
→ Lee README.md (5 min)

**¿Necesito Ollama?**
→ No es obligatorio. Los ejemplos funcionan sin él.

**¿Qué ejemplo debería ver primero?**
→ 01_metricas_desempeno.py (no tiene dependencias externas)

**¿Cómo aplico esto a mi agente?**
→ Sigue los ejercicios al final de GUIA_EVALUACION_AGENTES.md

**¿Tengo dudas?**
→ Revisa el FAQ en README.md o GUIA_EVALUACION_AGENTES.md

---

## 📊 Estadísticas

- **Archivos**: 9 (7 ejemplos + 2 documentos)
- **Líneas de código**: ~1,900
- **Líneas de documentación**: ~2,500
- **Tiempo de aprendizaje**: 3-4 horas
- **Ejemplos funcionales**: 6
- **Conceptos cubiertos**: 40+

---

## 🎯 Objetivo Final

Al completar este módulo, podrás:

✓ Definir métricas apropiadas para evaluar agentes
✓ Crear benchmarks de calidad con anotación múltiple
✓ Escribir tests a múltiples niveles
✓ Debuggear comportamientos inesperados sistemáticamente
✓ Usar LLMs para evaluación automática
✓ Implementar evaluación en producción

---

**Versión**: 1.0
**Fecha**: 2024-11-13
**Actualización**: Completo y listo para usar

¡Comienza por README.md y sigue el flujo de aprendizaje!
