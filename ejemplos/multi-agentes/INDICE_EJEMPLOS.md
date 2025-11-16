# Índice Completo de Ejemplos

## 📋 Estructura Jerárquica

```
ejemplos/multi-agentes/
│
├── 📚 DOCUMENTACIÓN
│   ├── README.md                    # Guía completa del proyecto
│   ├── INICIO_RAPIDO.md            # Primeros 10 minutos
│   ├── CONCEPTOS.md                # Teoría fundamental
│   ├── INDICE_EJEMPLOS.md          # Este archivo
│   └── RESUMEN_ENTREGA.md          # Lo que incluye el proyecto
│
├── 🛠️ UTILIDADES (Módulos reutilizables)
│   └── utilidades/
│       ├── ollama_client.py        # Cliente Ollama
│       ├── agent_base.py           # Clase base Agent
│       └── __init__.py
│
├── 📖 MÓDULO 1: Fundamentos (2 ejemplos)
│   └── modulo1/
│       ├── 01_agente_basico.py     ⭐ EMPEZAR AQUÍ
│       ├── 02_arquitecturas.py
│       └── __init__.py
│
├── 💬 MÓDULO 2: Comunicación (1 ejemplo)
│   └── modulo2/
│       ├── 01_comunicacion_basica.py
│       └── __init__.py
│
├── 🎯 MÓDULO 3: Coordinación (1 ejemplo)
│   └── modulo3/
│       ├── 01_coordinacion.py
│       └── __init__.py
│
├── 🤝 MÓDULO 4: Colaboración (1 ejemplo)
│   └── modulo4/
│       ├── 01_colaboracion.py
│       └── __init__.py
│
├── 💼 MÓDULO 5: Negociación (1 ejemplo)
│   └── modulo5/
│       ├── 01_negociacion.py
│       └── __init__.py
│
└── ✨ EXTRAS
    └── (proyectos integradores propuestos)
```

---

## 🚀 Orden Recomendado de Ejecución

### Nivel 1: Conceptos Básicos (30 minutos)

1. **Leer**: `CONCEPTOS.md`
   - Entender qué es un agente
   - Comprender el ciclo percepto-acción
   - Ver las arquitecturas

2. **Ejecutar**: `modulo1/01_agente_basico.py`
   ```bash
   python modulo1/01_agente_basico.py
   ```
   - Ver un agente funcionando
   - Entender la implementación

3. **Ejecutar**: `modulo1/02_arquitecturas.py`
   ```bash
   python modulo1/02_arquitecturas.py
   ```
   - Comparar tres arquitecturas
   - Entender pros/contras

### Nivel 2: Comunicación y Coordinación (45 minutos)

4. **Ejecutar**: `modulo2/01_comunicacion_basica.py`
   ```bash
   python modulo2/01_comunicacion_basica.py
   ```
   - Tres paradigmas: Síncrona, Asíncrona, Pub-Sub
   - Message Brokers

5. **Ejecutar**: `modulo3/01_coordinacion.py`
   ```bash
   python modulo3/01_coordinacion.py
   ```
   - Cómo evitar conflictos
   - Acceso a recursos compartidos

### Nivel 3: Colaboración y Negociación (45 minutos)

6. **Ejecutar**: `modulo4/01_colaboracion.py`
   ```bash
   python modulo4/01_colaboracion.py
   ```
   - Equipos colaborativos
   - Votación y consenso
   - Delegación

7. **Ejecutar**: `modulo5/01_negociacion.py`
   ```bash
   python modulo5/01_negociacion.py
   ```
   - Protocolo oferta-contraoferta
   - BATNA y zona de acuerdo
   - Estrategias competitivas

---

## 📝 Descripción Detallada de Ejemplos

### MÓDULO 1: Fundamentos

#### `01_agente_basico.py` ⭐ PUNTO DE INICIO
```python
# Qué demuestra:
- Ciclo percepto-acción completo
- Implementación de un agente autónomo
- Integración con Ollama
- Uso de IA para razonamiento

# Clases principales:
- AgenteAutonomo(Agent)

# Tiempo ejecución: 30-60 segundos por ciclo
# Salida esperada: 3 ciclos de percepto-acción
```

**Conceptos cubiertos:**
- Definición de agente
- Autonomía
- Racionalidad
- Ciclo percepto-acción

#### `02_arquitecturas.py`
```python
# Qué demuestra:
- Tres arquitecturas en acción
- Cómo cada una coordina agentes
- Ventajas y desventajas

# Clases principales:
- AgenteCoordinador (centralizada)
- AgenteDescentralizado (P2P)
- AgenteJerarquico (jerárquica)

# Tiempo ejecución: 2-3 minutos total
# Salida esperada: Tabla comparativa
```

**Conceptos cubiertos:**
- Arquitectura centralizada
- Arquitectura descentralizada (P2P)
- Arquitectura jerárquica
- Comparación: escalabilidad vs control

---

### MÓDULO 2: Comunicación

#### `01_comunicacion_basica.py`
```python
# Qué demuestra:
- Message Broker simple implementado
- Tres paradigmas de comunicación
- Estadísticas de comunicación

# Clases principales:
- MessageBroker
- AgenteConComunicacion(Agent)

# Tiempo ejecución: 1-2 minutos
# Salida esperada: Logs de mensajes
```

**Conceptos cubiertos:**
- Comunicación síncrona (bloqueante)
- Comunicación asíncrona (no-bloqueante)
- Publish-Subscribe
- Message Brokers
- Garantías de entrega

**Paradigmas implementados:**
```
Síncrona:     emisor → espera → receptor
Asíncrona:    emisor → cola → receptor (después)
Pub-Sub:      publicador → [tópico] → suscriptores
```

---

### MÓDULO 3: Coordinación

#### `01_coordinacion.py`
```python
# Qué demuestra:
- Acceso a recurso compartido
- Cómo evitar conflictos
- Tres estrategias de coordinación

# Clases principales:
- RecursoCompartido
- CoordinadorCentralizado
- AgenteConCoordinacion(Agent)

# Tiempo ejecución: 1-2 minutos
# Salida esperada: Orden de acceso a recurso
```

**Conceptos cubiertos:**
- Coordinación centralizada
- Coordinación jerárquica
- Coordinación distribuida
- Exclusión mutua
- Evitar deadlocks

**Ejemplo: Tres agentes, un recurso**
```
Coordinador asigna: Agente1 → Recurso
                    Agente2 → Espera
                    Agente3 → Espera

Después Agente1 libera...
Coordinador asigna: Agente2 → Recurso
```

---

### MÓDULO 4: Colaboración

#### `01_colaboracion.py`
```python
# Qué demuestra:
- Equipos de agentes especializados
- Delegación de tareas
- Votación para consenso
- Supervisión y monitoreo

# Clases principales:
- EquipoColaborativo
- AgenteColaborador(Agent)

# Tiempo ejecución: 2-3 minutos
# Salida esperada: Estados del equipo
```

**Conceptos cubiertos:**
- Formación de equipos
- Delegación de tareas
- Votación y consenso
- Supervisión
- Resolución de conflictos

**Estructura típica:**
```
Equipo Desarrollo
├── Alice (Data Scientist)
├── Bob (ML Engineer)
├── Charlie (Backend)
└── Diana (DevOps)

Tareas delegadas:
Alice → Data Processing
Bob → Feature Engineering
Charlie → API Development
Diana → Deployment
```

**Voting:**
```
Tema: "¿Tensorflow o PyTorch?"
Alice:   PyTorch
Bob:     PyTorch
Charlie: Tensorflow
Diana:   PyTorch

Resultado: PyTorch (3 votos vs 1)
```

---

### MÓDULO 5: Negociación

#### `01_negociacion.py`
```python
# Qué demuestra:
- Protocolo oferta-contraoferta
- BATNA y zona de acuerdo
- Utilidad en negociación
- Estrategias diferentes

# Clases principales:
- NegociacionBilateral
- AgenteNegociador(Agent)
- Utilidad
- Oferta

# Tiempo ejecución: 1-2 minutos
# Salida esperada: Negociaciones y acuerdos
```

**Conceptos cubiertos:**
- Teoría de negociación
- BATNA (Best Alternative To Negotiated Agreement)
- ZAP (Zona de Acuerdo Posible)
- Utilidad (value function)
- Protocolo oferta-contraoferta

**Ejemplo: Compra-Venta**
```
Vendedor BATNA: Precio mín $80, cantidad mín 10
Comprador BATNA: Precio máx $120, cantidad máx 100

RONDA 1:
Vendedor: "70 unidades a $140"
Comprador: "Utilidad = 0.65, contraoferta:"
         "80 unidades a $100"

RONDA 2:
Vendedor: "Utilidad = 0.55, contraoferta:"
         "60 unidades a $130"
Comprador: "Utilidad = 0.85, ACEPTO"

RESULTADO: 60 unidades a $130
```

---

## 🎮 Ejercicios Progresivos

### Nivel 1: Exploración (15 minutos)
```bash
# Solo ejecutar y observar
python modulo1/01_agente_basico.py
python modulo1/02_arquitecturas.py
python modulo2/01_comunicacion_basica.py
```

### Nivel 2: Modificación (30 minutos)
```python
# Editar modulo1/01_agente_basico.py:

# Cambio 1: Más ciclos
for i in range(10):  # Antes: 3
    agente.step(ambiente)

# Cambio 2: Objetivo diferente
agente.objective = "Aprender sobre IA"

# Cambio 3: Más agentes
agentes = [
    AgenteAutonomo(f"Agente-{i}", f"Objetivo-{i}")
    for i in range(5)  # Crear 5
]
```

### Nivel 3: Integración (1 hora)
```python
# Crear sistema que combine múltiples módulos:
# - Agentes (Módulo 1)
# - Que se comunican (Módulo 2)
# - Coordinados (Módulo 3)
# - En un equipo (Módulo 4)
# - Negociando (Módulo 5)
```

---

## 🔍 Búsqueda Rápida de Conceptos

| Concepto | Archivo | Línea |
|----------|---------|-------|
| Agente autónomo | modulo1/01_agente_basico.py | ~30 |
| Arquitectura centralizada | modulo1/02_arquitecturas.py | ~90 |
| Message Broker | modulo2/01_comunicacion_basica.py | ~20 |
| Coordinación | modulo3/01_coordinacion.py | ~80 |
| Equipo colaborativo | modulo4/01_colaboracion.py | ~40 |
| Negociación | modulo5/01_negociacion.py | ~100 |

---

## 📊 Estadísticas del Proyecto

```
Total de archivos:     12
Archivos de código:    8
Archivos de documentación: 4

Líneas de código:      ~2000
Líneas de documentación: ~3000

Clases implementadas:  15+
Ejemplos ejecutables:  7

Conceptos cubiertos:   40+
Patrones de diseño:    10+
```

---

## ✅ Checklist de Completitud

- [x] Ejemplos del Módulo 1
  - [x] Agente básico
  - [x] Arquitecturas

- [x] Ejemplos del Módulo 2
  - [x] Comunicación básica

- [x] Ejemplos del Módulo 3
  - [x] Coordinación

- [x] Ejemplos del Módulo 4
  - [x] Colaboración

- [x] Ejemplos del Módulo 5
  - [x] Negociación

- [x] Documentación
  - [x] README principal
  - [x] Inicio rápido
  - [x] Conceptos
  - [x] Índice de ejemplos

- [x] Utilidades
  - [x] Cliente Ollama
  - [x] Clase base Agent
  - [x] Message Broker

---

## 🎓 Cómo Usar Este Índice

1. **Primera vez**: Sigue "Orden Recomendado de Ejecución"
2. **Buscar concepto**: Usa "Búsqueda Rápida de Conceptos"
3. **Entender un módulo**: Lee su "Descripción Detallada"
4. **Practicar**: Haz los "Ejercicios Progresivos"
5. **Verificar**: Usa el "Checklist de Completitud"

---

## 🔗 Navegación

- [← Volver a README](README.md)
- [← Inicio Rápido](INICIO_RAPIDO.md)
- [← Conceptos Fundamentales](CONCEPTOS.md)

---

**Última actualización:** 2025
**Versión:** 1.0
**Estado:** Completo ✅
