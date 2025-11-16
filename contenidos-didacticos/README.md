# 📚 Contenidos Didácticos: Agentes de IA

## ¿Qué encontrarás aquí?

Tres documentos completos con **explicaciones claras, ejemplos de código y diagramas**:

1. **01-MULTI-AGENTES-COORDINACION.md** (2500+ líneas)
   - Cómo funcionan agentes autónomos
   - Cómo múltiples agentes se coordinan
   - Arquitecturas (centralizada, descentralizada, jerárquica)
   - Comunicación síncrona, asíncrona, Pub-Sub

2. **02-MEMORIA-CONTEXTO.md** (2000+ líneas)
   - 5 tipos de memoria en agentes (sensorial, trabajo, episódica, semántica, procedural)
   - Cómo persistir y recuperar estado
   - Event sourcing
   - Jerarquía de memoria (inspirada en humanos)

3. **03-EVALUACION-TESTING.md** (2000+ líneas)
   - Métricas: Accuracy, Precision, Recall, F1
   - Latency, Throughput, Robustness
   - Benchmarking y testing
   - Logging y monitoreo en producción

## 🎯 ¿Para quién es esto?

- **Estudiantes**: Quiero aprender sobre agentes IA
- **Docentes**: Necesito material educativo claro
- **Desarrolladores**: Quiero ejemplos funcionales
- **Investigadores**: Quiero base teórica sólida

## 🚀 Cómo empezar (5 minutos)

```bash
1. Lee INDICE-GENERAL.md → Entender estructura
2. Elige tu nivel:
   - PRINCIPIANTE: Multi-Agentes → Fundamentos
   - INTERMEDIO: Todo en orden
   - AVANZADO: Enfócate en temas específicos
3. Abre el documento correspondiente
4. Lee sección, estudia código, intenta reproducir
```

## 📖 Contenidos Principales

### Módulo 1: Multi-Agentes y Coordinación

**Conceptos Clave:**
- ✅ ¿Qué es un agente?
- ✅ Ciclo percepto-acción (Percibir → Razonar → Actuar)
- ✅ Arquitectura centralizada (1 coordinador)
- ✅ Arquitectura descentralizada (P2P)
- ✅ Arquitectura jerárquica (múltiples niveles)
- ✅ Comunicación: Síncrona, asíncrona, Pub-Sub

**Ejemplo Código:**
```python
class Agent:
    def perceive(self, environment):
        return percepts
    
    def reason(self, percepts):
        return decision
    
    def act(self, decision):
        return result
    
    def step(self, environment):
        percepts = self.perceive(environment)
        decision = self.reason(percepts)
        result = self.act(decision)
        return result
```

### Módulo 2: Memoria y Contexto

**Tipos de Memoria:**
1. **Sensorial** (ms) - Sensaciones brutas
2. **Trabajo** (s-min) - Información actual
3. **Episódica** (años) - Eventos específicos
4. **Semántica** (años) - Hechos abstractos
5. **Procedural** (años) - Habilidades

**Jerarquía Visual:**
```
SENSORIAL (input)
    ↓ [Atención]
TRABAJO (procesando)
    ↓ [Consolidación]
┌────────┬──────────┬──────────┐
↓        ↓          ↓          ↓
EPISÓDICA SEMÁNTICA PROCEDURAL
```

### Módulo 3: Evaluación y Testing

**Métricas Principales:**
| Tipo | Métrica | Fórmula | Rango |
|------|---------|---------|-------|
| Efectividad | Accuracy | (TP+TN)/Total | 0-100% |
| | Precision | TP/(TP+FP) | 0-100% |
| | Recall | TP/(TP+FN) | 0-100% |
| | F1-Score | 2*(Prec*Rec)/(Prec+Rec) | 0-1 |
| Eficiencia | Latency P95 | 95th percentile | ms |
| | Throughput | Requests/sec | RPS |
| Robustez | Error Rate | Errores/Total | % |
| | MTBF | Horas/Fallo | horas |

## 💻 Requisitos

- Python 3.6+
- Conocimiento básico de programación
- Entendimiento de POO (clases, herencia)
- Lápiz y papel (para diagramas)

## 📊 Estadísticas

- **Total de contenido**: 6500+ líneas
- **Ejemplos de código**: 50+
- **Diagramas ASCII**: 30+
- **Casos reales**: 15+
- **Ejercicios**: 20+

## 🗺️ Mapa Visual

```
AGENTE IA
├─ ¿Cómo funciona? → MULTI-AGENTES
├─ ¿Qué recuerda? → MEMORIA
└─ ¿Qué tan bueno? → EVALUACIÓN
```

## ⭐ Highlights

### 🔴 Momento Eureka #1: El Ciclo Percepto-Acción
```
Agente = while True:
    percibe
    razona
    actúa
```

### 🟠 Momento Eureka #2: Tipos de Memoria
```
"¿Por qué algunos agentes parecen olvidar todo?"
→ Porque no implementan memoria persistente
```

### 🟡 Momento Eureka #3: Elegir Métricas
```
"¿Mi agente es bueno?"
NO: Visualmente bien
SÍ: Accuracy 94.3%, P95 latency 120ms
```

## 🎓 Cómo Estudiar

### Método 1: Rápido (2 horas)
- Lee: Secciones de "Concepto Clave"
- Entiende: Diagramas principales
- Experimenta: 2-3 ejemplos de código

### Método 2: Completo (1-2 semanas)
- Lee: Cada sección completamente
- Estudia: Todos los ejemplos
- Practica: Modificar código
- Proyecta: Crear sistema propio

### Método 3: Maestría (1 mes)
- Domina: Todo el material
- Experimenta: Variaciones
- Crea: Sistema complejo
- Documenta: Decisiones

## 🛠️ Ejercicios Prácticos

### Nivel 1: Crear agente simple
```python
# Agente termostato
agent = Thermostat('TH-1')
agent.perceive({'temperature': 28})
agent.step({'target': 24})
```

### Nivel 2: Multi-agentes
```python
# Sistemas 5 agentes comunicándose
system = MultiAgentSystem()
for i in range(5):
    system.add_agent(Agent(f'A{i}'))
system.run(10)  # 10 pasos
```

### Nivel 3: Completo
```python
# Sistema con memoria + evaluación
system = CompleteSystem()
system.add_agents()
system.run()
system.evaluate(metrics=['accuracy', 'latency'])
```

## 📈 Progresión Recomendada

```
Día 1: Conceptos (Agentes + Ciclo percepto-acción)
Día 2: Arquitecturas (3 tipos)
Día 3: Comunicación (Síncrono + Asíncrono)
Día 4: Memoria (5 tipos)
Día 5: Persistencia (Guardar/restaurar)
Día 6: Métricas (Accuracy, Precision, Recall)
Día 7: Testing (Unit tests, Benchmarks)
Día 8-10: Proyecto final (Integrar todo)
```

## 🔗 Relaciones entre Temas

```
Multi-Agentes
├─ Necesitan → Comunicación (M2)
├─ Mantienen → Memoria (M2)
└─ Requieren → Evaluación (M3)

Memoria
├─ Influye en → Decisiones (M1)
├─ Se valida con → Testing (M3)
└─ Se mide con → Métricas (M3)

Evaluación
├─ Mide → Agentes (M1)
├─ Valida → Memoria (M2)
└─ Usa → Benchmarks
```

## 💡 Tips de Aprendizaje

1. **Dibuja** los diagramas a mano mientras lees
2. **Ejecuta** el código de ejemplo
3. **Modifica** el código para experimentar
4. **Explica** con tus palabras
5. **Implementa** en tu proyecto

## ❓ Preguntas Frecuentes

**P: ¿Necesito ser experto en Python?**
R: No, Python básico es suficiente. Los ejemplos son simples.

**P: ¿Puedo saltarme partes?**
R: Sí, pero la secuencia lógica es M1 → M2 → M3.

**P: ¿Hay videos?**
R: No en este set, solo texto + código + diagramas.

**P: ¿Cómo práctico?**
R: Hay ejercicios en cada módulo. Además, crea tu propio agente.

## 📞 Ayuda Rápida

### No entiendo el ciclo percepto-acción
→ Ve a M1, sección 1.1, hay 3 diagramas

### No sé qué tipo de memoria usar
→ Ve a M2, hay tabla comparativa

### No sé qué métrica elegir
→ Ve a M3, sección "Elección de Métricas"

## 🎯 Objetivo Final

Después de estos contenidos, deberías poder:

✅ Explicar qué es un agente en 1 párrafo
✅ Diseñar arquitectura multi-agente
✅ Implementar comunicación entre agentes
✅ Diseñar sistema de memoria
✅ Elegir métricas apropiadas
✅ Crear tests y benchmarks
✅ Monitorear agente en producción

## 📄 Archivos en esta Carpeta

```
contenidos-didacticos/
├── INDICE-GENERAL.md              # Mapa completo
├── 01-MULTI-AGENTES-COORDINACION.md   # Módulo 1
├── 02-MEMORIA-CONTEXTO.md         # Módulo 2
├── 03-EVALUACION-TESTING.md       # Módulo 3
└── README.md                       # Este archivo
```

## 🚀 Empezar Ahora

```bash
1. Abre INDICE-GENERAL.md
2. Elige tu nivel
3. Lee el módulo 1
4. Practica con código
5. Continúa con módulos 2 y 3
```

## 📈 Estructura de Aprendizaje

```
Principiante → Intermedio → Avanzado

Principiante:
- Leer conceptos clave
- Ver diagramas
- Correr ejemplos simples

Intermedio:
- Entender todo el código
- Modificar ejemplos
- Resolver ejercicios

Avanzado:
- Crear sistemas complejos
- Optimizar desempeño
- Investigar temas nuevos
```

---

**¡Bienvenido a los Agentes de IA! 🤖**

Estos contenidos te guiarán desde conceptos básicos hasta sistemas complejos y evaluación en producción.

Happy Learning! 🚀

