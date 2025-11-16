# Conceptos Fundamentales: Sistemas Multi-Agente

## 1. ¿Qué es un Agente?

Un **agente** es una entidad de software que:

### Ciclo Percepto-Acción
```
┌─────────┐
│ Percibe │ (Obtiene información del ambiente)
│         │
└────┬────┘
     │
┌────▼────────┐
│   Razona    │ (Procesa y decide usando IA)
│             │
└────┬────────┘
     │
┌────▼────────┐
│   Actúa     │ (Ejecuta acciones)
│             │
└─────────────┘
```

### Ejemplo Real
```
Un agente de compras:
• PERCIBE: precios actuales, inventario
• RAZONA: ¿debo comprar ahora o esperar?
• ACTÚA: realiza compra o espera
```

### Propiedad Fundamental: AUTONOMÍA
- Toma decisiones propias
- No necesita órdenes constantes
- Aprende de su experiencia

---

## 2. Sistemas Multi-Agente

Cuando **múltiples agentes** trabajan juntos:

### Ventajas
- ✅ Escalabilidad: más agentes = más capacidad
- ✅ Robustez: si uno falla, otros continúan
- ✅ Flexibilidad: agentes especializados
- ✅ Paralelismo: trabajan simultáneamente

### Desafíos
- ❌ Coordinación: ¿cómo se ponen de acuerdo?
- ❌ Conflictos: ¿qué pasa si chocan intereses?
- ❌ Comunicación: ¿cómo se hablan?
- ❌ Consistencia: ¿quién tiene la verdad?

---

## 3. Arquitecturas

### 3.1 CENTRALIZADA
```
         ┌─────────────┐
         │ Coordinador │
         │   Central   │
         └──────┬──────┘
                │
        ┌───┬───┼───┬───┐
        │   │   │   │   │
       [A] [B] [C] [D] [E]
      Agentes
```

**Características:**
- Un "jefe" que controla todo
- Decisiones óptimas globales
- Punto único de fallo

**Ejemplo:** CEO de una empresa pequeña

### 3.2 DESCENTRALIZADA (P2P)
```
    [A] ←→ [B]
    ↕       ↕
    [D] ←→ [C]
```

**Características:**
- Todos iguales, sin jefe
- Negociación local
- Mayor resiliencia

**Ejemplo:** Red Bitcoin, usuarios en torrent

### 3.3 JERÁRQUICA
```
        ┌─────┐
        │CEO  │
        └────┬┘
           ┌─┴─┐
        ┌──┴┐ ┌┴──┐
       [M1]  [M2]
       ┌┴┐  ┌┴─┐
      [A][B][C][D]

CEO > Managers > Agentes
```

**Características:**
- Múltiples niveles
- Balance entre control y distribución
- Mejor escalabilidad que centralizada

**Ejemplo:** Organización empresarial típica

---

## 4. Comunicación

### 4.1 SÍNCRONA (Bloqueante)
```
Agente A                    Agente B
   │                          │
   ├─ "¿Hola?" ──────────────→ │
   │    ESPERA RESPUESTA        │
   │                       (procesa)
   │ ← "Hola, ¿qué tal?" ───────┤
   │                          │
```

**Ventajas:** Confirmación inmediata
**Desventajas:** Puede bloquear todo

### 4.2 ASÍNCRONA (No-bloqueante)
```
Agente A              Cola de Mensajes      Agente B
   │                       │                    │
   ├─ "¿Hola?" ──────────→ │                    │
   │  CONTINÚA trabajando  │                    │
   │                       └──→ "¿Hola?" ──────→ │
   │                                        (procesa)
```

**Ventajas:** Mayor rendimiento
**Desventajas:** Menos garantía de entrega

### 4.3 PUBLISH-SUBSCRIBE
```
Publicador         Tópico:temperatura        Suscriptores
    │                  │                         │
    │                  │                      [Logger]
    ├─ "25°C" ────────→ │                        │
    │                  │                      [Alertas]
    │                  │                        │
    │                  └──→ "25°C" ────────────→ [Dashboard]
```

**Ventajas:** Máxima desacoplamiento
**Desventajas:** Menos control directo

---

## 5. Coordinación

¿Cómo se ponen de acuerdo múltiples agentes para actuar sin conflictos?

### 5.1 COORDINACIÓN CENTRALIZADA
```
Coordinador decide:
"Alice: procesa datos"
"Bob: valida resultados"
"Charlie: guarda en BD"
```

**Problema:** Si el coordinador falla, ¡caos!

### 5.2 COORDINACIÓN JERÁRQUICA
```
Manager1: "Alice, procesa A; Bob, procesa B"
Manager2: "Charlie, valida A; Diana, valida B"
```

**Ventaja:** Distribución de responsabilidad

### 5.3 COORDINACIÓN DISTRIBUIDA
```
Turnos basados en timestamps:
Alice (t=1) → Bob (t=2) → Charlie (t=3)
```

**Ventaja:** Sin punto central, totalmente resiliente

---

## 6. Colaboración

### ¿Cómo trabajan juntos hacia un objetivo común?

#### FASES:

1. **Formación de Equipo**
   - Se reúnen agentes con roles complementarios
   - Data Scientist + ML Engineer + DevOps

2. **Delegación**
   - Se asignan tareas específicas
   - "Alice: procesar datos"

3. **Ejecución**
   - Cada agente ejecuta su parte
   - Comunicación si hay problemas

4. **Votación/Consenso**
   - Decisiones críticas se votan
   - Mayoría simple o supermayoría

5. **Entrega**
   - Resultado final combinado

---

## 7. Negociación

### Escenario: Vendedor y Comprador

#### CONCEPTOS CLAVE:

**BATNA** = Best Alternative To Negotiated Agreement
```
Vendedor BATNA:
  - Precio mínimo: $80
  - Cantidad mínima: 10

Comprador BATNA:
  - Precio máximo: $120
  - Cantidad máxima: 100
```

**ZAP** = Zona de Acuerdo Posible
```
Si BATNA Vendedor < BATNA Comprador → ¡Existe ZAP!
80 < 120 ✓ → Hay rango de negociación
```

#### PROTOCOLO: Oferta-Contraoferta

```
RONDA 1:
Vendedor: "Te doy 50 unidades por $140"
Comprador: "No es suficiente. Te doy $100 por 80 unidades"

RONDA 2:
Vendedor: "Mejor precio para mí: $130 por 60 unidades"
Comprador: "Aceptado ✓"

ACUERDO: 60 unidades a $130
```

---

## 8. Teoría de Juegos (Opcional)

### Dilema del Prisionero

Dos prisioneros. Cada uno puede:
- **Cooperar** (callar)
- **Traicionar** (delatar)

**Matriz de Pagos:**
```
           B: Calla    B: Delata
A: Calla      (-1,-1)    (-3, 0)
A: Delata     (0, -3)    (-2,-2)
```

**Resultado**: Ambos traicionan (punto de equilibrio)
**Lección**: Incentivos individuales ≠ óptimo global

---

## 9. Conceptos de Implementación

### Clase Agent (Base)

```python
class Agent:
    def perceive(self, environment):
        # Obtener información
        return sensores

    def reason(self, percepts):
        # Procesar con IA
        return decision

    def act(self, decision):
        # Ejecutar
        return resultado
```

### Message Broker

```
Agente A → [Broker de Mensajes] → Agente B
           (almacena, entrega)
```

### Protocolo de Comunicación

```
Reglas acordadas:
1. Formato: JSON
2. Tiempo máximo respuesta: 10 segundos
3. Reintentos si no hay respuesta
4. Acknowledgment (ACK)
```

---

## 10. Resumen Comparativo

| Aspecto | Centralizada | Jerárquica | Distribuida |
|---------|-------------|-----------|------------|
| **Control** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **Escalabilidad** | ⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Resiliencia** | ⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Complejidad** | ⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Mejor Para** | Control crítico | Empresas | P2P, Blockchain |

---

## Analogía del Mundo Real

### Analogía: Restaurante

**CENTRALIZADA:**
- Chef (coordinador) controla todo
- Meseros, cocineros obedecen órdenes
- ✓ Control, ✗ Inflexible

**JERÁRQUICA:**
- Chef jefe → Sous chefs → Cocineros/Meseros
- Cada nivel coordina su grupo
- ✓ Balance, ✓ Escalable

**DISTRIBUIDA:**
- Toda la cocina se auto-organiza
- Cada chef sabe qué hacer
- ✓ Creativa, ✗ Caótica

---

## Preguntas de Comprensión

1. ¿Cuáles son las tres partes del ciclo percepto-acción?
2. ¿Cuál es la principal ventaja de los sistemas descentralizados?
3. ¿Qué es BATNA en negociación?
4. ¿Cuándo elegirías una arquitectura jerárquica vs centralizada?
5. ¿Cuál es la diferencia entre comunicación síncrona y asíncrona?

---

## Referencias Adicionales

- 📖 [README Completo](README.md)
- 🚀 [Inicio Rápido](INICIO_RAPIDO.md)
- 💻 [Ejemplos Funcionales](.)

---

**Recuerda**: Los sistemas multi-agente permiten resolver problemas complejos
dividiéndolos en partes simples que múltiples agentes pueden manejar.
