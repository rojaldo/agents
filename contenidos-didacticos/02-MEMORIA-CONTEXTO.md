# Contenidos Didácticos: Memoria y Contexto en Agentes

## 📚 Índice
1. [Módulo 1: Tipos de Memoria](#módulo-1)
2. [Módulo 2: Gestión de Estado](#módulo-2)
3. [Módulo 3: Memoria a Corto Plazo](#módulo-3)
4. [Módulo 4: Memoria a Largo Plazo](#módulo-4)

---

## <a name="módulo-1"></a>Módulo 1: Tipos de Memoria en Agentes

### ¿Por Qué Memoria?

Imaginemos dos escenarios:

```
AGENTE SIN MEMORIA:
┌────────────────────────────────────────────┐
│  Usuario: "Hola, soy Carlos"               │
│  Usuario: "Me duele la cabeza"             │
│                                             │
│  [5 minutos después]                       │
│                                             │
│  Usuario: "¿Cómo me llamo?"                │
│  Agente: "No sé, no tengo memoria"        │
│                                             │
│  ❌ INÚTIL: No aprende de experiencias     │
└────────────────────────────────────────────┘

AGENTE CON MEMORIA:
┌────────────────────────────────────────────┐
│  Usuario: "Hola, soy Carlos"               │
│  Agente: [GUARDA en memoria]               │
│                                             │
│  Usuario: "Me duele la cabeza"             │
│  Agente: [GUARDA en memoria]               │
│  Agente: "Sugiero paracetamol"             │
│                                             │
│  [5 minutos después]                       │
│                                             │
│  Usuario: "¿Cómo me llamo?"                │
│  Agente: "Carlos! ¿Te sigue doliendo?"    │
│                                             │
│  ✅ INTELIGENTE: Aprende y contextualiza   │
└────────────────────────────────────────────┘
```

### 1.1 Jerarquía de Memoria (Inspirada en Humanos)

```python
from datetime import datetime, timedelta
from enum import Enum

class MemoryHierarchy:
    """
    SIMILAR AL CEREBRO HUMANO

    ┌─────────────────────────────────────────────┐
    │      MEMORIA SENSORIAL                      │
    │  (Milisegundos - Muy breve)                 │
    │  "Veo rojo, escucho sonido"                 │
    └─────────────────────────────────────────────┘
                      ↓
    ┌─────────────────────────────────────────────┐
    │      MEMORIA DE TRABAJO                     │
    │  (Segundos - Información actual)             │
    │  "Estoy resolviendo este problema"          │
    └─────────────────────────────────────────────┘
                      ↓
    ┌─────────────────────────────────────────────┐
    │      MEMORIA A LARGO PLAZO                  │
    │  (Años - Información permanente)            │
    │                                              │
    │  ├─ EPISÓDICA: "El 13/11 pasó X"           │
    │  ├─ SEMÁNTICA: "París es capital de Francia"│
    │  └─ PROCEDURAL: "Cómo conducir"            │
    └─────────────────────────────────────────────┘
    """

    def __init__(self):
        self.sensory_buffer = []      # Milisegundos
        self.working_memory = {}      # Segundos-minutos
        self.episodic_memory = []     # Eventos con fecha
        self.semantic_memory = {}     # Hechos atemporales
        self.procedural_memory = {}   # Habilidades


# ═════════════════════════════════════════════════════════════════
# 1️⃣ MEMORIA SENSORIAL
# ═════════════════════════════════════════════════════════════════

class SensoryMemory:
    """
    DURACIÓN: Milisegundos
    CAPACIDAD: Muy grande (todo lo que ve/oye)
    CONTENIDO: Sensaciones brutas sin procesar

    ANALOGÍA HUMANA:
    - Ves una luz roja
    - En 1-2 segundos desaparece de visión sensorial
    - Pero influye en memoria de trabajo
    """

    def __init__(self, buffer_size=1000):
        self.buffer = []
        self.buffer_size = buffer_size
        self.ttl = 0.5  # Time-to-live: 500ms

    def add_sensation(self, sensation):
        """
        Agrega sensación bruta
        """
        sensation['timestamp'] = datetime.now()

        self.buffer.append(sensation)

        # Mantener tamaño máximo
        if len(self.buffer) > self.buffer_size:
            self.buffer.pop(0)

    def get_current(self):
        """
        Obtiene sensaciones ACTUALES (< 500ms)
        """
        now = datetime.now()
        current = [
            s for s in self.buffer
            if (now - s['timestamp']).total_seconds() < self.ttl
        ]
        return current

    def example_robot_vision(self):
        """
        Ejemplo: Robot que ve obstáculos
        """
        # Sensor ve objeto
        self.add_sensation({
            'type': 'vision',
            'object': 'ball',
            'distance': 0.5,
            'position': (100, 50)
        })

        # Milisegundos después
        current = self.get_current()
        print(f"Robot VE AHORA: {current}")
        # → [{'type': 'vision', 'object': 'ball', ...}]

        # Después de 1 segundo
        import time
        time.sleep(1)

        current = self.get_current()
        print(f"Robot VE AHORA: {current}")
        # → [] (Desapareció de sensorial)


# ═════════════════════════════════════════════════════════════════
# 2️⃣ MEMORIA DE TRABAJO (Working Memory)
# ═════════════════════════════════════════════════════════════════

class WorkingMemory:
    """
    DURACIÓN: Segundos a minutos
    CAPACIDAD: Limitada (típicamente 4-7 items, "7±2")
    CONTENIDO: Información ACTUALMENTE en uso

    ANALOGÍA HUMANA:
    - Estás resolviendo un problema matemático
    - Mantienes los números en mente
    - "Tengo los números: 3, 5, 8 en mi cabeza"
    - Cuando terminas, olvidas

    EN AGENTES:
    - Variables locales de función
    - Parámetros actuales
    - Contexto de conversación
    """

    def __init__(self, capacity=7):
        self.data = {}
        self.capacity = capacity
        self.access_count = {}

    def store(self, key, value):
        """
        Guarda en memoria de trabajo
        """
        if len(self.data) >= self.capacity:
            # Quitar el menos usado
            least_used = min(self.access_count, key=self.access_count.get)
            del self.data[least_used]
            del self.access_count[least_used]

        self.data[key] = value
        self.access_count[key] = 0

    def retrieve(self, key):
        """
        Obtiene de memoria de trabajo
        """
        if key in self.data:
            self.access_count[key] += 1
            return self.data[key]
        return None

    def example_math_problem(self):
        """
        Ejemplo: Resolver 3 + 5 * 2

        Paso 1: Multiplicar 5 * 2
        """
        self.store('operand1', 5)
        self.store('operand2', 2)
        self.store('operation', '*')

        result = self.retrieve('operand1') * self.retrieve('operand2')
        # Resultado: 10

        """
        Paso 2: Sumar 3 + 10
        """
        self.store('operand1', 3)
        self.store('operand2', result)
        self.store('operation', '+')

        final = self.retrieve('operand1') + self.retrieve('operand2')
        # Resultado: 13

        # Ahora olvida números (no son relevantes)
        self.data.clear()

    def example_conversation_context(self):
        """
        Ejemplo: Contexto de conversación

        Usuario: "Mi nombre es Alice"
        Agente: [Guarda en working memory]
        """
        self.store('user_name', 'Alice')
        self.store('conversation_topic', 'introduction')
        self.store('message_count', 1)

        """
        Usuario: "Trabajo en tecnología"
        Agente: [Actualiza working memory]
        """
        self.store('user_job', 'technology')
        self.store('message_count', 2)

        """
        Usuario: "¿Cuál es mi nombre?"
        Agente: [Busca en working memory]
        """
        name = self.retrieve('user_name')
        print(f"Tu nombre es {name}")  # Alice


# ═════════════════════════════════════════════════════════════════
# 3️⃣ MEMORIA EPISÓDICA
# ═════════════════════════════════════════════════════════════════

class EpisodicMemory:
    """
    REGISTRA EVENTOS ESPECÍFICOS

    DURACIÓN: Años
    CONTENIDO: "El 13/11/2025 pasó X"
    TEMPORAL: Cronológico

    ANALOGÍA HUMANA:
    - "El 25/12/2020 me caí del bicicleta"
    - "El 15/3/2022 vi a mi primer concierto"
    - Recuerdas QUÉ pasó, CUÁNDO pasó, DÓNDE

    EN AGENTES:
    - Logs de interacciones
    - Historial de conversaciones
    - Registro de decisiones
    """

    def __init__(self):
        self.episodes = []

    def record_episode(self, event):
        """
        Registra un evento con timestamp
        """
        episode = {
            'timestamp': datetime.now(),
            'event': event,
            'context': self._capture_context()
        }
        self.episodes.append(episode)
        print(f"✓ Episodio grabado: {event}")

    def _capture_context(self):
        """Captura contexto del evento"""
        return {
            'date': datetime.now().date(),
            'time': datetime.now().time()
        }

    def recall_episode(self, query):
        """
        Busca episodios que coincidan

        Ejemplo: "¿Cuándo hablamos de X?"
        """
        matches = [
            ep for ep in self.episodes
            if query in ep['event']
        ]
        return matches

    def example_doctor_agent(self):
        """
        Ejemplo: Agente doctor que recuerda episodios
        """
        # Episodio 1: Primera visita
        self.record_episode(
            event="Paciente Carlos llegó con dolor de cabeza",
        )

        # Episodio 2: Prescripción
        self.record_episode(
            event="Prescribí paracetamol a Carlos"
        )

        # Episodio 3: Seguimiento
        self.record_episode(
            event="Carlos reporta mejoría"
        )

        # Más tarde: Búsqueda
        history = self.recall_episode("Carlos")

        for episode in history:
            print(f"[{episode['timestamp']}] {episode['event']}")

        # OUTPUT:
        # [2025-11-13 14:30:15.123456] Paciente Carlos llegó...
        # [2025-11-13 14:32:45.654321] Prescribí paracetamol...
        # [2025-11-13 14:35:12.987654] Carlos reporta mejoría


# ═════════════════════════════════════════════════════════════════
# 4️⃣ MEMORIA SEMÁNTICA
# ═════════════════════════════════════════════════════════════════

class SemanticMemory:
    """
    CONOCIMIENTO ABSTRACTO DESCONTEXTUALIZADO

    DURACIÓN: Años
    CONTENIDO: "Hechos, conceptos, relaciones"
    ATEMPORAL: "París es capital" (sin fecha)

    ANALOGÍA HUMANA:
    - "París es la capital de Francia"
    - "El agua hierve a 100°C"
    - "Einstein descubrió la relatividad"
    - Sabes HECHOS sin recordar CUÁNDO aprendiste

    EN AGENTES:
    - Base de conocimiento
    - Ontologías
    - Reglas de negocio
    """

    def __init__(self):
        self.facts = {}  # Almacén de hechos
        self.rules = []  # Reglas de inferencia

    def store_fact(self, subject, relation, object):
        """
        Almacena un hecho: Sujeto - Relación - Objeto
        """
        key = f"{subject}_{relation}"
        self.facts[key] = object

    def retrieve_fact(self, subject, relation):
        """
        Recupera un hecho
        """
        key = f"{subject}_{relation}"
        return self.facts.get(key)

    def add_rule(self, condition, consequence):
        """
        Agrega una regla: Si X entonces Y
        """
        self.rules.append({
            'condition': condition,
            'consequence': consequence
        })

    def infer(self, query):
        """
        Infiere conocimiento aplicando reglas
        """
        # Aplicar todas las reglas
        for rule in self.rules:
            if rule['condition'](self.facts):
                return rule['consequence'](self.facts)

    def example_geography_knowledge(self):
        """
        Ejemplo: Agente que sabe geografía
        """
        # Almacenar hechos
        self.store_fact('París', 'capital_of', 'Francia')
        self.store_fact('Madrid', 'capital_of', 'España')
        self.store_fact('Lisboa', 'capital_of', 'Portugal')
        self.store_fact('Francia', 'contains', 'París')

        # Recuperar hechos
        capital = self.retrieve_fact('París', 'capital_of')
        print(f"París es capital de: {capital}")
        # → Francia

        # Agregar regla
        self.add_rule(
            condition=lambda facts: 'Francia_contains' in facts,
            consequence=lambda facts: f"Francia contiene {facts['Francia_contains']}"
        )

    def example_medical_knowledge(self):
        """
        Ejemplo: Agente médico con reglas
        """
        # Hechos
        self.store_fact('fiebre', 'temperature', '>38C')
        self.store_fact('tos', 'symptom', 'true')
        self.store_fact('dolor_cabeza', 'symptom', 'true')

        # Reglas
        self.add_rule(
            condition=lambda f: (
                f.get('fiebre_temperature') == '>38C' and
                f.get('tos_symptom') == 'true'
            ),
            consequence=lambda f: "Diagnóstico probable: Infección respiratoria"
        )


# ═════════════════════════════════════════════════════════════════
# 5️⃣ MEMORIA PROCEDURAL
# ═════════════════════════════════════════════════════════════════

class ProceduralMemory:
    """
    CONOCIMIENTO DE CÓMO HACER COSAS

    DURACIÓN: Años
    CONTENIDO: "Habilidades, scripts, políticas"
    AUTOMÁTICO: Se mejora con práctica

    ANALOGÍA HUMANA:
    - Sabes CÓMO conducir (sin pensar cada paso)
    - Sabes CÓMO atarte los zapatos
    - Sabes CÓMO hablar (reglas de gramática aplicadas)

    EN AGENTES:
    - Algoritmos
    - Políticas de decisión
    - Procedimientos
    - Estrategias de resolución
    """

    def __init__(self):
        self.procedures = {}

    def learn_procedure(self, name, procedure_func):
        """
        Aprende un procedimiento
        """
        self.procedures[name] = procedure_func

    def execute_procedure(self, name, inputs):
        """
        Ejecuta un procedimiento aprendido
        """
        if name in self.procedures:
            return self.procedures[name](inputs)
        return None

    def example_negotiation_skill(self):
        """
        Ejemplo: Agente que aprendió a negociar
        """

        def negotiation_procedure(params):
            """
            Procedimiento: Cómo negociar

            (Se ejecuta automáticamente, sin pensar cada paso)
            """
            offer = params['initial_offer']
            target = params['target_price']
            opponent_offer = params['opponent_offer']

            # Paso 1: Evaluar oferta
            if opponent_offer > target:
                # Paso 2: Contraoferta
                new_offer = (offer + opponent_offer) / 2
            else:
                new_offer = target

            # Paso 3: Enviar
            return {'counter_offer': new_offer}

        # Agente aprende el procedimiento
        self.learn_procedure('negotiate', negotiation_procedure)

        # Más tarde, ejecuta sin pensar
        result = self.execute_procedure('negotiate', {
            'initial_offer': 100,
            'target_price': 80,
            'opponent_offer': 90
        })

        print(f"Contraoferta automática: ${result['counter_offer']}")
        # → Contraoferta automática: $85

    def example_pathfinding_skill(self):
        """
        Ejemplo: Robot que aprendió a navegar
        """

        def pathfinding(params):
            """
            Procedimiento: Encontrar ruta
            (Basado en A*, Dijkstra, etc.)
            """
            import math
            start = params['start']
            goal = params['goal']

            # Algoritmo aprendido (simplificado)
            distance = math.sqrt(
                (goal[0] - start[0])**2 +
                (goal[1] - start[1])**2
            )

            return {'distance': distance, 'direction': 'northeast'}

        self.learn_procedure('navigate', pathfinding)

        result = self.execute_procedure('navigate', {
            'start': (0, 0),
            'goal': (10, 10)
        })

        print(f"Navegación: {result}")
        # → Navegación: {'distance': 14.14, 'direction': 'northeast'}


# ═════════════════════════════════════════════════════════════════
# INTEGRACIÓN: Sistema Completo de Memoria
# ═════════════════════════════════════════════════════════════════

class CompleteMemorySystem:
    """
    Integra TODOS los tipos de memoria
    """

    def __init__(self, name):
        self.name = name
        self.sensory = SensoryMemory()
        self.working = WorkingMemory()
        self.episodic = EpisodicMemory()
        self.semantic = SemanticMemory()
        self.procedural = ProceduralMemory()

    def perceive_and_remember(self, event):
        """
        Percibe evento → Procesa → Guarda
        """
        # 1. Llega a memoria sensorial
        self.sensory.add_sensation({'event': event})

        # 2. Procesa en memoria de trabajo
        self.working.store('current_event', event)

        # 3. Guarda en memoria episódica
        self.episodic.record_episode(event)

    def think_with_knowledge(self, query):
        """
        Piensa usando conocimiento adquirido
        """
        # Accede a memoria semántica
        fact = self.semantic.retrieve_fact('Paris', 'capital_of')

        # Usa memoria procedural
        result = self.procedural.execute_procedure('negotiate', {})

        return f"Basado en lo que sé: {fact}, y mi habilidad para {result}"

# RESUMEN VISUAL:

print("""
JERARQUÍA DE MEMORIA COMPLETA:

    SENSORIAL (ms)
         ↓ [Atención]
    TRABAJO (s-min)
         ↓ [Consolidación]
    ┌────────────┬──────────────┬────────────┐
    ↓            ↓              ↓            ↓
 EPISÓDICA   SEMÁNTICA    PROCEDURAL   (Otras)
 (Eventos)   (Hechos)     (Habilidades)
   ↓            ↓              ↓
"Hoy..."   "Sé que..."   "Puedo..."

USO:
- SENSORIAL: Percepción inmediata
- TRABAJO: Procesamiento actual
- EPISÓDICA: Contexto específico temporal
- SEMÁNTICA: Conocimiento compartible
- PROCEDURAL: Automatismos aprendidos

EN AGENTES IA:
- SENSORIAL: Buffer de entrada
- TRABAJO: Variables de sesión
- EPISÓDICA: Historial de conversación
- SEMÁNTICA: Base de conocimiento
- PROCEDURAL: Algoritmos y políticas
""")
```

---

## <a name="módulo-2"></a>Módulo 2: Gestión de Estado en Agentes

### 2.1 Qué es Estado

```python
class AgentState:
    """
    ESTADO = Información que define completamente al agente

    ANALOGÍA HUMANA:
    Tu "estado" en este momento es:
    - Tu ubicación: En casa
    - Tu energía: Cansado
    - Tu objetivo: Dormir
    - Tu dinero: $100
    - Tus relaciones: Amigo de Juan
    - Tu conocimiento: Ingeniero
    """

    def __init__(self, agent_name):
        self.agent_name = agent_name

        # COMPONENTES DE ESTADO:

        # 1. IDENTIDAD
        self.id = agent_name
        self.type = 'robot'
        self.version = '2.1'

        # 2. POSICIÓN / CONTEXTO
        self.location = (0, 0)  # Coordenadas
        self.environment = 'warehouse'

        # 3. RECURSOS
        self.energy = 100
        self.battery = 95
        self.memory_used = 45  # %

        # 4. OBJETIVOS
        self.primary_goal = 'deliver_package'
        self.secondary_goals = ['optimize_route', 'avoid_obstacles']

        # 5. CREENCIAS / MODELO DEL MUNDO
        self.beliefs = {
            'weather': 'sunny',
            'traffic_light': 'green',
            'obstacle_ahead': False
        }

        # 6. RELACIONES CON OTROS
        self.relationships = {
            'robot_2': 'teammate',
            'supervisor': 'authority'
        }

        # 7. HISTÓRICO
        self.actions_completed = 0
        self.errors = 0
        self.last_update = datetime.now()

    def snapshot(self):
        """
        Captura completa del estado (para guardar/restaurar)
        """
        return {
            'agent': self.agent_name,
            'location': self.location,
            'energy': self.energy,
            'goals': {
                'primary': self.primary_goal,
                'secondary': self.secondary_goals
            },
            'beliefs': self.beliefs,
            'timestamp': datetime.now()
        }

# DIAGRAMA DE ESTADO:

print("""
AGENTE EN TIEMPO T=0:
┌─────────────────────────────────┐
│ Robot-A                         │
├─────────────────────────────────┤
│ Ubicación: (0, 0)               │
│ Energía: 100%                   │
│ Objetivo: Entregar paquete      │
│ Creencias:                      │
│   - Ruta despejada: Sí          │
│   - Obstáculos: No              │
│ Relaciones:                     │
│   - Supervisor: Conectado       │
│   - Robot-B: En línea           │
└─────────────────────────────────┘
         ↓ [Acción: Mover]
         ↓ [Tiempo: 5 segundos]
         ↓
AGENTE EN TIEMPO T=5:
┌─────────────────────────────────┐
│ Robot-A                         │
├─────────────────────────────────┤
│ Ubicación: (5, 0)   ← CAMBIÓ    │
│ Energía: 98%        ← CAMBIÓ    │
│ Objetivo: Entregar paquete      │
│ Creencias:                      │
│   - Ruta despejada: Sí          │
│   - Obstáculos: No              │
│ Relaciones:                     │
│   - Supervisor: Conectado       │
│   - Robot-B: En línea           │
└─────────────────────────────────┘

CONCLUSIÓN:
El ESTADO CAMBIÓ gracias a la ACCIÓN
""")
```

### 2.2 Estado Local vs Compartido

```python
class StateSharingExample:
    """
    ESTADO LOCAL: Privado del agente
    ESTADO COMPARTIDO: Visible a otros
    """

    def __init__(self):
        self.agents = {}

    def example_local_state(self):
        """
        Ejemplo: Cada agente tiene su almacén local
        """
        print("ESTADO LOCAL\n")

        class Agent:
            def __init__(self, name):
                self.name = name
                # ✓ Local: Solo yo lo sé
                self.private_thoughts = "Tengo hambre"
                self.internal_battery = 100
                self.secret_goal = "Terminar pronto y descansar"

            def reveal_public_state(self):
                # ✗ No revelo estado privado
                return {
                    'name': self.name,
                    'status': 'working'
                }

        robot1 = Agent('Robot-1')
        robot2 = Agent('Robot-2')

        print(f"Robot-1 sabe sobre sí mismo: {robot1.private_thoughts}")
        print(f"Robot-2 sabe sobre sí mismo: {robot2.private_thoughts}")

        # Pero no saben lo del otro
        print(f"Robot-1 sabe sobre Robot-2: {robot2.reveal_public_state()}")
        # → No sabe que Robot-2 tiene hambre

    def example_shared_state(self):
        """
        Ejemplo: Tablero compartido con información global
        """
        print("\nESTADO COMPARTIDO\n")

        class SharedBoard:
            def __init__(self):
                self.state = {}

            def update(self, agent_name, info):
                """Actualiza estado visible"""
                self.state[agent_name] = info

            def read(self, agent_name):
                """Lee estado de otro"""
                return self.state.get(agent_name)

        board = SharedBoard()

        # Robot-1 publica su posición
        board.update('robot-1', {
            'position': (5, 5),
            'task': 'picking',
            'status': 'busy'
        })

        # Robot-2 lee posición de Robot-1
        r1_info = board.read('robot-1')
        print(f"Robot-2 sabe: Robot-1 está en {r1_info['position']}")

    def example_conflict(self):
        """
        Ejemplo: Conflicto cuando dos actualizan mismo estado
        """
        print("\nCONFLICTO DE ESTADO COMPARTIDO\n")

        class Counter:
            def __init__(self):
                self.value = 0

        counter = Counter()

        # Robot-1 intenta incrementar
        print(f"Valor inicial: {counter.value}")

        # Robot-1: Lee
        temp1 = counter.value  # → 0

        # Robot-2: Lee (mientras Robot-1 está procesando)
        temp2 = counter.value  # → 0

        # Robot-1: Suma y escribe
        counter.value = temp1 + 1  # 0 + 1 = 1

        # Robot-2: Suma y escribe (sin saber que Robot-1 cambió)
        counter.value = temp2 + 1  # 0 + 1 = 1 (¡Ignoró cambio de Robot-1!)

        print(f"Valor final: {counter.value}")
        print("❌ PROBLEMA: Debería ser 2, pero es 1!")
        print("   Robot-2 no vio el cambio de Robot-1")


# TABLA COMPARATIVA:
print("""
PROPIEDAD           LOCAL               COMPARTIDO
─────────────────────────────────────────────────────
Visibilidad         Solo el agente      Todos los agentes
Modificación        Sin sincronización  Requiere sincronización
Conflictos          Imposibles          Posibles
Performance         Rápido              Lento (coordinación)
Privacidad          Total               Expuesto
Secretos            ✓ Posible           ✗ Imposible
─────────────────────────────────────────────────────
""")
```

### 2.3 Persistencia de Estado

```python
import json
import pickle
from datetime import datetime

class PersistentState:
    """
    ¿Cómo guardar estado para recuperar después?

    CASOS DE USO:
    1. Recuperación de fallos: "Vuelvo a dónde estaba"
    2. Auditoría: "Quién hizo qué, cuándo"
    3. Debugging: "Qué pasó justo antes del error"
    4. Machine learning: "Aprendimiento entre sesiones"
    """

    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.state = {
            'position': (0, 0),
            'energy': 100,
            'tasks_completed': 0,
            'timestamp': datetime.now().isoformat()
        }

    # ───────────────────────────────────────────────────────────
    # OPCIÓN 1: Guardar en Archivo (JSON)
    # ───────────────────────────────────────────────────────────
    def save_to_json(self, filename):
        """
        Guarda estado en JSON
        VENTAJA: Legible, portable
        DESVENTAJA: Más lento
        """
        with open(filename, 'w') as f:
            json.dump(self.state, f, indent=2)
        print(f"✓ Estado guardado en {filename}")

    def load_from_json(self, filename):
        """
        Carga estado desde JSON
        """
        with open(filename, 'r') as f:
            self.state = json.load(f)
        print(f"✓ Estado restaurado desde {filename}")

    # ───────────────────────────────────────────────────────────
    # OPCIÓN 2: Guardar en Binario (Pickle)
    # ───────────────────────────────────────────────────────────
    def save_to_binary(self, filename):
        """
        Guarda estado binario
        VENTAJA: Muy rápido, objetos complejos
        DESVENTAJA: No legible, Python-only
        """
        with open(filename, 'wb') as f:
            pickle.dump(self.state, f)
        print(f"✓ Estado guardado (binario) en {filename}")

    def load_from_binary(self, filename):
        """Carga desde binario"""
        with open(filename, 'rb') as f:
            self.state = pickle.load(f)
        print(f"✓ Estado restaurado (binario) desde {filename}")

    # ───────────────────────────────────────────────────────────
    # OPCIÓN 3: Guardar en Base de Datos
    # ───────────────────────────────────────────────────────────
    def save_to_database(self, db_connection):
        """
        Guarda en BD (por ejemplo SQLite)
        """
        import sqlite3

        conn = sqlite3.connect('agents.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_states (
                id INTEGER PRIMARY KEY,
                agent_name TEXT,
                state TEXT,
                timestamp DATETIME
            )
        ''')

        cursor.execute(
            'INSERT INTO agent_states (agent_name, state, timestamp) VALUES (?, ?, ?)',
            (self.agent_name, json.dumps(self.state), datetime.now())
        )

        conn.commit()
        conn.close()
        print(f"✓ Estado guardado en BD")

    # ───────────────────────────────────────────────────────────
    # OPCIÓN 4: Event Sourcing
    # ───────────────────────────────────────────────────────────

    def event_sourcing_example(self):
        """
        Event Sourcing: Guardar EVENTOS, no estado

        IDEA:
        En vez de guardar: "Energía = 80"
        Guardamos evento: "Energía decreció 20 unidades"

        VENTAJA: Reconstruir cualquier momento
        DESVENTAJA: Más complejidad
        """

        events = []

        # Evento 1: Agente se crea
        events.append({
            'type': 'agent_created',
            'timestamp': datetime.now(),
            'agent_name': self.agent_name,
            'initial_energy': 100
        })

        # Evento 2: Agente se mueve
        events.append({
            'type': 'agent_moved',
            'timestamp': datetime.now(),
            'from': (0, 0),
            'to': (5, 5)
        })

        # Evento 3: Agente usa energía
        events.append({
            'type': 'energy_used',
            'timestamp': datetime.now(),
            'amount': 20
        })

        # RECONSTRUIR ESTADO en T=3:
        # 1. Energía inicial: 100
        # 2. Usar energía: -20
        # 3. Energía actual: 80

        reconstructed_energy = 100
        for event in events:
            if event['type'] == 'energy_used':
                reconstructed_energy -= event['amount']

        print(f"Energía reconstruida: {reconstructed_energy}")


# COMPARACIÓN DE OPCIONES:
print("""
MÉTODO            VELOCIDAD   TAMAÑO   LEGIBLE   COMPLEJO   IDEAL
──────────────────────────────────────────────────────────────────
JSON              Lento       Grande   Sí        Bajo       Desarrollo
Binario (Pickle)  Rápido      Pequeño  No        Bajo       Producción
Base de Datos     Medio       Pequeño  Parcial   Alto       Datos grandes
Event Sourcing    Rápido      Grande   Sí        Alto       Auditoría
──────────────────────────────────────────────────────────────────
""")
```

Continuará en la siguiente parte...

