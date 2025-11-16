# Contenidos Didácticos: Multi-Agentes y Coordinación

## 📚 Índice
1. [Módulo 1: Fundamentos de Sistemas Multi-Agente](#módulo-1)
2. [Módulo 2: Comunicación Entre Agentes](#módulo-2)
3. [Módulo 3: Coordinación y Orquestación](#módulo-3)
4. [Módulo 4: Colaboración y Trabajo en Equipo](#módulo-4)
5. [Módulo 5: Negociación](#módulo-5)

---

## <a name="módulo-1"></a>Módulo 1: Fundamentos de Sistemas Multi-Agente

### ¿Qué es un Sistema Multi-Agente?

Un **sistema multi-agente (MAS)** es un conjunto de múltiples agentes autónomos que interactúan entre sí para resolver problemas complejos. Cada agente:

- **Percibe** su ambiente mediante sensores
- **Razona** sobre la información percibida
- **Actúa** tomando decisiones
- **Interactúa** con otros agentes

```
┌─────────────────────────────────────────┐
│         AMBIENTE / MUNDO                │
│                                         │
│  ┌──────────┐        ┌──────────┐     │
│  │  AGENTE  │◄─────►│  AGENTE  │     │
│  │    1     │        │    2     │     │
│  └──────────┘        └──────────┘     │
│       ▲                      ▲         │
│       │                      │         │
│       └──────────┬───────────┘         │
│                  │                     │
│         ┌────────▼────────┐            │
│         │  AGENTE 3       │            │
│         │  (Coordinador)  │            │
│         └─────────────────┘            │
│                                         │
└─────────────────────────────────────────┘
```

### 1.1 Conceptos Fundamentales

#### **El Ciclo Percepto-Acción**

Todo agente funciona en un ciclo:

```python
class Agent:
    """
    Ciclo fundamental de un agente:
    1. Percibir el ambiente
    2. Razonar sobre la situación
    3. Decidir qué hacer
    4. Actuar
    5. Repetir
    """

    def __init__(self, name, objective):
        self.name = name
        self.objective = objective
        self.state = {}
        self.beliefs = {}
        self.knowledge_base = {}

    def perceive(self, environment):
        """
        PERCEPCIÓN: El agente obtiene información del ambiente

        ¿QUÉ PERCIBE?
        - Variables del ambiente
        - Mensajes de otros agentes
        - Cambios en estado del mundo
        """
        percepts = {
            'temperature': environment.get('temp'),
            'light': environment.get('light'),
            'messages': self.get_messages(),
            'time': environment.get('time'),
            'resources': environment.get('resources')
        }
        return percepts

    def reason(self, percepts):
        """
        RAZONAMIENTO: El agente procesa información

        ¿QUÉ HACE?
        - Actualiza creencias sobre el mundo
        - Usa reglas de lógica
        - Consulta base de conocimiento
        - Usa IA/ML para decisiones
        """
        # Actualizar creencias
        if percepts['temperature'] > 25:
            self.beliefs['is_hot'] = True

        # Razonar sobre objetivos
        if self.objective == 'maintain_comfort':
            if self.beliefs['is_hot']:
                decision = 'turn_on_ac'
            else:
                decision = 'maintain_current'

        return decision

    def act(self, decision):
        """
        ACCIÓN: El agente ejecuta decisiones

        ¿QUÉ ACCIONES?
        - Cambiar estado del ambiente
        - Enviar mensajes
        - Actualizar estado local
        """
        result = self._execute_action(decision)

        # Log para auditoría
        self._log_action(decision, result)

        return result

    def step(self, environment):
        """
        UN PASO COMPLETO DEL CICLO
        """
        # 1. Percibir
        percepts = self.perceive(environment)

        # 2. Razonar
        decision = self.reason(percepts)

        # 3. Actuar
        result = self.act(decision)

        return {
            'percepts': percepts,
            'decision': decision,
            'result': result
        }
```

**Ejemplo en acción:**

```python
# Escenario: Agente termostato
env = {
    'temp': 28,
    'light': 'day',
    'time': '14:00',
    'resources': {'energy': 100}
}

agent = Agent('Thermostat-1', 'maintain_comfort')

# Ejecutar un paso
log = agent.step(env)

print(f"Temperatura percibida: {log['percepts']['temperature']}°C")
print(f"Decisión: {log['decision']}")
print(f"Resultado: {log['result']}")

# SALIDA:
# Temperatura percibida: 28°C
# Decisión: turn_on_ac
# Resultado: AC encendido (consume 5 de energía)
```

#### **Autonomía vs Control**

```python
# Agente AUTÓNOMO: Toma decisiones propias
class AutonomousRobot:
    """El robot decide qué hacer basado en su objetivo"""

    def step(self, environment):
        # El robot ELIGE qué hacer
        if environment['battery'] < 20:
            # DECISIÓN PROPIA: buscar cargador
            action = 'search_charger'
        elif environment['obstacle']:
            # DECISIÓN PROPIA: evitar obstáculo
            action = 'avoid_obstacle'
        else:
            # DECISIÓN PROPIA: continuar con tarea
            action = 'continue_task'

        return self.execute(action)

# Agente HETERÓNOMO: Espera órdenes
class ControlledRobot:
    """El robot ejecuta lo que le dicen"""

    def step(self, instruction):
        # El robot OBEDECE instrucciones
        return self.execute(instruction)

# ¿Cuál es más inteligente?
# El autónomo puede adaptarse a cambios
# El heterónomo es predecible y seguro
```

### 1.2 Propiedades del Ambiente

Los agentes actúan en ambientes con diferentes características:

```python
from enum import Enum

class EnvironmentProperty:
    """Clasifica ambientes según sus propiedades"""

    @staticmethod
    def example_deterministic():
        """
        DETERMINÍSTICO: Mismo input → Siempre mismo output
        Ejemplo: Ajedrez
        """
        # Si sé exactamente dónde está todo, puedo predecir el futuro
        return "Si muevo peón a e4, la posición es SIEMPRE la misma"

    @staticmethod
    def example_stochastic():
        """
        ESTOCÁSTICO: Mismo input → Múltiples posibles outputs
        Ejemplo: Conducción con tráfico
        """
        # Aunque vea un semáforo verde, otros autos pueden sorprenderme
        return "Aunque acelere, el auto de adelante podría frenar"

    @staticmethod
    def example_static():
        """
        ESTÁTICO: El ambiente no cambia sin el agente
        Ejemplo: Puzzle
        """
        # Las piezas solo se mueven si YO las muevo
        return "El puzzle no cambia si no lo toco"

    @staticmethod
    def example_dynamic():
        """
        DINÁMICO: El ambiente cambia sin el agente
        Ejemplo: Tráfico
        """
        # Aunque no haga nada, otros autos siguen moviéndose
        return "El tráfico avanza aunque espere"

    @staticmethod
    def example_discrete():
        """
        DISCRETO: Cantidad finita de estados/acciones
        Ejemplo: Ajedrez
        """
        # Solo hay posiciones permitidas en el tablero
        return "Solo 64 cuadrados posibles"

    @staticmethod
    def example_continuous():
        """
        CONTINUO: Infinitas posibilidades
        Ejemplo: Control de temperatura
        """
        # La temperatura puede ser 20.1, 20.11, 20.111...
        return "Infinitos valores posibles"

# TABLA DE AMBIENTES COMUNES:
ambientes = {
    'Ajedrez': {
        'determinístico': True,
        'estático': True,
        'discreto': True,
        'totalmente observable': True,
        'dificultad': 'Media (10^120 posiciones)'
    },
    'Conducción': {
        'determinístico': False,  # Impredecible
        'estático': False,         # El tráfico cambia
        'discreto': False,         # Infinitas posiciones
        'totalmente observable': False,  # Puntos ciegos
        'dificultad': 'Muy alta'
    },
    'Ajedrez vs Aleatorio': {
        'determinístico': True,
        'estático': True,
        'discreto': True,
        'totalmente observable': True,
        'dificultad': 'Imposible (3x10^48 posiciones)'
    },
    'Diagnóstico Médico': {
        'determinístico': False,   # Síntomas varían
        'estático': False,          # Paciente evoluciona
        'discreto': True,           # Enfermedades discretas
        'totalmente observable': False,  # No vemos órganos
        'dificultad': 'Muy alta'
    }
}
```

### 1.3 Arquitecturas: Comparativa Detallada

#### **1. Arquitectura Centralizada**

```python
class CentralizedArchitecture:
    """
    CARACTERÍSTICAS:
    - Un COORDINADOR maestro controla todo
    - Los demás agentes son WORKERS que obedecen
    - El coordinador conoce TODA la información
    - El coordinador toma TODAS las decisiones

    DIAGRAMA:
                    [COORDINADOR]
                          ↑
            ┌─────────────┼─────────────┐
            ↓             ↓             ↓
         [Worker1]    [Worker2]    [Worker3]
    """

    def __init__(self):
        self.coordinator = Coordinator('main')
        self.workers = [
            Worker(f'worker_{i}')
            for i in range(1, 4)
        ]
        self.global_state = {}

    def step(self):
        # 1. El coordinador RECOPILA información
        world_state = self._collect_info()

        # 2. El coordinador ANALIZA
        decisions = self.coordinator.plan(world_state)

        # 3. El coordinador ASIGNA tareas
        for worker, task in zip(self.workers, decisions):
            worker.execute(task)

    def _collect_info(self):
        """Coordinador recopila todo"""
        info = {}
        for worker in self.workers:
            info[worker.name] = {
                'resources': worker.resources,
                'status': worker.status,
                'completed_tasks': worker.completed_tasks
            }
        return info

class Coordinator:
    def plan(self, world_state):
        """
        EJEMPLO: Coordinador decide cómo procesar 3 tareas
        con 3 workers
        """
        tasks = ['process_A', 'process_B', 'process_C']

        # Usa algoritmo de optimización
        assignment = self._optimize_assignment(
            tasks,
            world_state
        )
        # Resultado: Worker1 → Task A, Worker2 → Task B, etc.

        return assignment

    def _optimize_assignment(self, tasks, state):
        """Encuenta asignación óptima"""
        # Aquí iría algoritmo húngaro u otro
        return ['process_A', 'process_B', 'process_C']

# ANÁLISIS CENTRALIZADO:
print("""
VENTAJAS:
✓ Coordinación perfecta
✓ Sin conflictos
✓ Óptimo global

DESVENTAJAS:
✗ Cuello de botella: coordinador procesando
✗ Punto único de fallo: si falla coordinador, ¡colapso!
✗ Escalabilidad limitada: coordinador se abruma
✗ No adapta a cambios: decisiones previas

IDEAL PARA:
- Sistemas pequeños (3-5 agentes)
- Problemas bien definidos
- Entornos estables
""")
```

#### **2. Arquitectura Descentralizada (P2P)**

```python
class DecentralizedArchitecture:
    """
    CARACTERÍSTICAS:
    - TODOS los agentes son iguales
    - SIN autoridad central
    - Cada agente es AUTÓNOMO
    - Coordinación emerge de INTERACCIONES locales

    DIAGRAMA:
         [Agent1] ←→ [Agent2]
            ↕            ↕
         [Agent4] ←→ [Agent3]

    Cada agente negocia con sus vecinos
    """

    def __init__(self):
        self.agents = [
            PeerAgent(f'peer_{i}')
            for i in range(1, 5)
        ]
        # Conectar en topología de anillo
        for i in range(len(self.agents)):
            next_agent = self.agents[(i + 1) % len(self.agents)]
            self.agents[i].set_neighbor(next_agent)

    def step(self):
        # Cada agente actúa INDEPENDIENTEMENTE
        for agent in self.agents:
            # Negocia con vecinos
            neighbors_state = agent.get_neighbors_state()

            # Toma decisión PROPIA
            decision = agent.decide(neighbors_state)

            # Ejecuta acción
            agent.execute(decision)

class PeerAgent:
    """Agente que negocia localmente"""

    def __init__(self, name):
        self.name = name
        self.resources = 10
        self.objective = 'maximize_own_resources'
        self.neighbor = None

    def set_neighbor(self, neighbor):
        self.neighbor = neighbor

    def get_neighbors_state(self):
        if self.neighbor:
            return {
                'name': self.neighbor.name,
                'resources': self.neighbor.resources
            }
        return None

    def decide(self, neighbor_state):
        """
        ESTRATEGIA LOCAL:
        - Si vecino tiene mucho, negocia
        - Si vecino tiene poco, coopera
        - Si yo tengo poco, pido ayuda
        """
        if neighbor_state is None:
            return 'wait'

        if neighbor_state['resources'] > 15:
            # Vecino tiene mucho, negocia
            return 'request_resources'
        elif neighbor_state['resources'] < 5:
            # Vecino tiene poco, coopera
            return 'share_resources'
        else:
            # Equilibrio, coopera
            return 'exchange'

    def execute(self, decision):
        if decision == 'request_resources':
            # Negocia con vecino
            self.neighbor.receive_request(self)
        elif decision == 'share_resources':
            # Comparte con vecino
            self.neighbor.receive_offer(self)

# ANÁLISIS DESCENTRALIZADO:
print("""
VENTAJAS:
✓ Sin punto de fallo único
✓ Escalable: agrega agentes fácilmente
✓ Robusto: si un agente falla, otros continúan
✓ Adaptativo: responde a cambios locales

DESVENTAJAS:
✗ Coordinación compleja: emerge de caos
✗ Convergencia no garantizada
✗ Difícil de debuggear
✗ Puede ser subóptimo globalmente

IDEAL PARA:
- Sistemas grandes (100+ agentes)
- Entornos dinámicos
- Requisito de robustez
- Redes P2P (blockchain, BitTorrent)
""")
```

#### **3. Arquitectura Jerárquica**

```python
class HierarchicalArchitecture:
    """
    CARACTERÍSTICAS:
    - MÚLTIPLES NIVELES de coordinadores
    - Cada nivel coordina su subgrupo
    - Balance entre centralización y distribución

    DIAGRAMA:
                [Director General]
                        ↑
            ┌───────────┼───────────┐
            ↓           ↓           ↓
         [Manager1]  [Manager2]  [Manager3]
            ↑           ↑           ↑
        ┌───┴───┐   ┌───┴───┐   ┌───┴───┐
        ↓       ↓   ↓       ↓   ↓       ↓
      [W1]   [W2] [W3]   [W4] [W5]   [W6]
    """

    def __init__(self):
        # Nivel 0: Director
        self.director = Coordinator('director')

        # Nivel 1: Managers
        self.managers = [
            Coordinator(f'manager_{i}')
            for i in range(1, 4)
        ]

        # Nivel 2: Workers
        self.workers = [
            Worker(f'worker_{i}')
            for i in range(1, 7)
        ]

        # Asignar workers a managers
        workers_per_manager = 2
        for i, mgr in enumerate(self.managers):
            start = i * workers_per_manager
            end = start + workers_per_manager
            mgr.set_team(self.workers[start:end])

    def step(self):
        """
        FLUJO JERÁRQUICO:
        1. Director define ESTRATEGIA global
        2. Managers adaptan estrategia a su grupo
        3. Workers ejecutan tareas
        """
        # Nivel 0
        global_strategy = self.director.define_strategy()

        # Nivel 1
        for manager in self.managers:
            # Manager adapta estrategia
            local_plan = manager.adapt_strategy(global_strategy)

            # Manager coordina su equipo
            for worker in manager.team:
                worker.execute(local_plan)

class Manager(Coordinator):
    def __init__(self, name):
        super().__init__(name)
        self.team = []
        self.parent = None
        self.children = []

    def set_team(self, workers):
        self.team = workers

    def adapt_strategy(self, global_strategy):
        """
        Manager ADAPTA estrategia global
        a recursos y capacidades locales

        EJEMPLO:
        Global: "Procesar 100 registros"
        Local (5 workers): "Cada uno procesa 20"
        """
        team_capacity = len(self.team) * 20  # Cada worker: 20 registros

        local_strategy = {
            'global_goal': global_strategy,
            'team_size': len(self.team),
            'work_per_agent': global_strategy.get('work', 0) // len(self.team)
        }

        return local_strategy

# ANÁLISIS JERÁRQUICO:
print("""
VENTAJAS:
✓ Escalabilidad controlada
✓ Distribución de responsabilidad
✓ Fácil de entender
✓ Balance entre control y autonomía

DESVENTAJAS:
✗ Más complejo que centralizado
✗ Latencia: decisiones suben y bajan
✗ Puntos de fallo en managers

IDEAL PARA:
- Sistemas medianos (20-200 agentes)
- Estructuras organizacionales
- Equipos con líderes naturales
""")
```

### 1.4 Cuándo Usar Sistemas Multi-Agente

```python
class SelectArchitecture:
    """
    ÁRBOL DE DECISIÓN: ¿Uso Multi-Agente?
    """

    @staticmethod
    def should_use_multiagent(problem):
        """
        Factores para decidir:
        """
        factors = {
            'multiple_goals': problem.get('num_objectives', 1) > 1,
            'distributed': problem.get('distributed', False),
            'dynamic': problem.get('dynamic', False),
            'scalable': problem.get('needs_scaling', False),
            'robust': problem.get('needs_robustness', False)
        }

        # Contar factores
        score = sum(1 for v in factors.values() if v)

        return {
            'recommendation': 'USE MULTIAGENT' if score >= 2 else 'USE MONOLITIC',
            'score': f'{score}/5 factors',
            'factors': factors
        }

# EJEMPLOS:

# ❌ NO usar multi-agente
problem_simple = {
    'description': 'Convertir temperaturas Celsius a Fahrenheit',
    'num_objectives': 1,
    'distributed': False,
    'dynamic': False,
    'needs_scaling': False,
    'needs_robustness': False
}
print(SelectArchitecture.should_use_multiagent(problem_simple))
# → MONOLITIC es mejor

# ✅ SÍ usar multi-agente
problem_complex = {
    'description': 'Sistema de tráfico inteligente para ciudad',
    'num_objectives': 5,  # Seguridad, velocidad, consumo, etc.
    'distributed': True,
    'dynamic': True,
    'needs_scaling': True,
    'needs_robustness': True
}
print(SelectArchitecture.should_use_multiagent(problem_complex))
# → MULTIAGENT es mejor

# TABLA DE DECISIÓN:
print("""
CRITERIO                          → MONOLITIC        → MULTIAGENT
─────────────────────────────────────────────────────────────────
Número de objetivos              1                  ≥2
Complejidad del problema         Baja               Alta
Distribución geográfica          Centralizado       Distribuido
Dinamismo del ambiente           Estático           Dinámico
Necesidad de escalabilidad       Baja               Alta
Necesidad de robustez            Baja               Alta
Facilidad de desarrollo          Más fácil          Más difícil
Facilidad de debugging           Más fácil          Difícil
─────────────────────────────────────────────────────────────────
""")
```

### 1.5 Casos de Uso Reales

```python
class RealWorldCases:
    """
    Ejemplos de sistemas multi-agente en el mundo real
    """

    @staticmethod
    def smart_grid():
        """
        ⚡ RED ELÉCTRICA INTELIGENTE

        AGENTES:
        - Productores (paneles solares, plantas)
        - Consumidores (casas, fábricas)
        - Distribuidores (subestaciones)
        - Reguladores (autoridad)

        COORDINACIÓN:
        - Sin coordinador central (descentralizado)
        - Cada productor negocia precio
        - Cada consumidor compra al mejor precio
        - Precio emerge del mercado

        OBJETIVO GLOBAL:
        - Equilibrio oferta-demanda
        - Minimizar pérdidas
        - Máxima eficiencia
        """

        class Producer:
            def __init__(self, name, capacity):
                self.name = name
                self.capacity = capacity  # MW
                self.price = 50  # $/MWh

            def negotiate(self, buyers):
                """Aumenta precio si demanda > oferta"""
                total_demand = sum(b.demand for b in buyers)
                if total_demand > self.capacity:
                    self.price *= 1.1  # Sube 10%

        class Consumer:
            def __init__(self, name, demand):
                self.name = name
                self.demand = demand  # MW
                self.max_price = 150  # $/MWh

            def buy(self, producers):
                """Compra del productor más barato"""
                cheapest = min(producers, key=lambda p: p.price)
                if cheapest.price <= self.max_price:
                    return cheapest
                return None

    @staticmethod
    def autonomous_vehicles():
        """
        🚗 VEHÍCULOS AUTÓNOMOS EN CIUDAD

        AGENTES:
        - Cada vehículo es un agente
        - Semáforos inteligentes
        - Central de tráfico

        COORDINACIÓN:
        - Jerárquica: Central → Semáforos → Vehículos
        - Distribuida: Vehículos comunican entre sí

        EJEMPLO:
        - Auto A detecta congestión
        - Comunica a autos cercanos
        - Todos recalculan rutas
        - Se distribuye tráfico
        """

        class Vehicle:
            def __init__(self, vehicle_id):
                self.id = vehicle_id
                self.position = (0, 0)
                self.destination = None
                self.neighbors = []

            def broadcast_congestion(self):
                """Avisa a vecinos de tráfico"""
                message = {
                    'sender': self.id,
                    'type': 'congestion_alert',
                    'position': self.position
                }
                for neighbor in self.neighbors:
                    neighbor.receive_message(message)

            def reroute(self):
                """Cambia ruta para evitar congestión"""
                # Usar algoritmo de routing
                self.destination = self.calculate_alternate_route()

    @staticmethod
    def swarm_robotics():
        """
        🤖 ENJAMBRES DE ROBOTS

        AGENTES:
        - Cientos de robots pequeños
        - Cada uno con capacidades limitadas
        - Inteligencia colectiva sin centralizador

        EJEMPLO:
        - Robots colaborativos construyen estructura
        - Sin planos detallados
        - Siguen reglas locales simples:
          * Si ves un gap, rellénalo
          * Si alguien construye cerca, ayuda

        RESULTADO:
        - Estructuras complejas emergen
        - Adaptación automática
        - Robustez extrema
        """

        class SwarmRobot:
            def __init__(self, robot_id):
                self.id = robot_id
                self.position = (0, 0)
                self.local_view = []  # Lo que ve

            def sense(self):
                """Percibe 1m a la redonda"""
                self.local_view = self.get_nearby_positions()

            def decide(self):
                """Reglas simples locales"""
                # Si hay gap cercano
                if self.find_gap_nearby():
                    return 'move_to_gap'
                # Si hay robot cercano construyendo
                elif self.find_building_neighbor():
                    return 'help_build'
                else:
                    return 'explore'

            def act(self, decision):
                """Ejecuta decisión"""
                if decision == 'move_to_gap':
                    self.position = self.find_gap_nearby()
```

---

## <a name="módulo-2"></a>Módulo 2: Comunicación Entre Agentes

### ¿Por qué Comunicación?

Dos agentes sin comunicación:

```
┌─────────────┐          ┌─────────────┐
│  Agente A   │ ┼┼┼┼┼┼┼┼ │  Agente B   │
│             │ SIN INFO │             │
│ Objetivo:   │          │ Objetivo:   │
│ Pintar muro │          │ Traer agua  │
│ SOLO        │          │ SOLO        │
└─────────────┘          └─────────────┘

RESULTADO:
- A pinta solo (lentamente)
- B trae agua solo (ineficiente)
- ❌ Ninguno sabe qué hace el otro
- ❌ No pueden colaborar
```

Con comunicación:

```
┌─────────────┐          ┌─────────────┐
│  Agente A   │ ←────→  │  Agente B   │
│             │ COMU    │             │
│ "Necesito   │ NICAC.  │ "Tengo agua │
│  agua para  │ ←────→  │  disponible"│
│  pintar"    │         │             │
└─────────────┘          └─────────────┘

RESULTADO:
- A y B colaboran
- ✅ Muro pintado rápido
- ✅ Recurso usado eficientemente
```

### 2.1 Paradigmas de Comunicación

```python
# ═══════════════════════════════════════════════════════════════
# 1️⃣ COMUNICACIÓN SÍNCRONA (Bloqueante)
# ═══════════════════════════════════════════════════════════════

class SynchronousCommunication:
    """
    EL EMISOR ESPERA RESPUESTA INMEDIATA

    DIAGRAMA:

    Agent A                        Agent B
    │
    ├─ Envía "¿Tienes datos?"
    │  (ESPERA ────────────────────────→ Recibe
    │                                    Procesa
    │                                    RESPONDE)
    │
    ├─ Recibe "Sí, aquí"
    │
    ├─ Continúa con el siguiente paso
    │
    """

    def __init__(self):
        self.agent_a = Agent('A')
        self.agent_b = Agent('B')

    def example_request_response(self):
        """
        Ejemplo: A pide datos a B
        """
        print("COMUNICACIÓN SÍNCRONA\n")

        # Agente A BLOQUEA esperando respuesta
        print("Agent A: 'Enviando petición...'")
        print("Agent A: [ESPERANDO...]")

        # Agente B RESPONDE
        print("Agent B: 'Recibida petición'")
        print("Agent B: 'Procesando...'")
        print("Agent B: 'Enviando respuesta'")

        # Agente A desbloquea
        print("Agent A: '¡Respuesta recibida!'")
        print("Agent A: 'Continuando con siguiente paso'\n")

    def code_example(self):
        """
        Implementación en código
        """

        class SyncAgent:
            def request_data(self, other_agent, key):
                """
                Requiere información BLOQUEANTE
                """
                # BLOQUEA AQUÍ (no continúa)
                response = other_agent.get_data(key)

                # Solo continúa después de respuesta
                return self.process_data(response)

            def process_data(self, data):
                return f"Procesado: {data}"

        # Uso
        agent_a = SyncAgent()
        agent_b = SyncAgent()

        # BLOQUEANTE: A espera
        result = agent_a.request_data(agent_b, 'sensor_data')
        # A NO PUEDE hacer nada mientras espera

# ANÁLISIS:
print("""
SÍNCRONO
Ventajas:
  ✓ Simple: emisor sabe cuándo llegó respuesta
  ✓ Confirmación inmediata

Desventajas:
  ✗ Bloquea: emisor no puede hacer nada
  ✗ Ambos deben estar activos
  ✗ Timeout si uno no responde
  ✗ No escalable: muchos esperandos

IDEAL: Comunicación directa 1-a-1, baja latencia
""")


# ═══════════════════════════════════════════════════════════════
# 2️⃣ COMUNICACIÓN ASÍNCRONA (No-bloqueante)
# ═══════════════════════════════════════════════════════════════

class AsynchronousCommunication:
    """
    EL EMISOR NO ESPERA, CONTINÚA SU TRABAJO

    DIAGRAMA:

    Agent A                Queue                Agent B
    │
    ├─ Envía "¿Datos?"
    │  (NO ESPERA) ──────────→ [Cola de mensajes]
    │                                ↓
    │  ├─ Continúa               Procesa cuando
    │  │ trabajando                puede
    │  │                                ↓
    │  └─ Recibe respuesta más tarde  ←─ "Aquí"
    │
    """

    def __init__(self):
        self.message_queue = []

    def example_async(self):
        """
        Ejemplo: A pide datos, continúa sin esperar
        """
        print("COMUNICACIÓN ASÍNCRONA\n")

        print("Agent A: 'Enviando petición...'")
        print("Agent A: [Mensaje en cola]")
        print("Agent A: 'No espero! Continuando con otra tarea...'")

        # A CONTINÚA TRABAJANDO mientras B procesa
        print("Agent A: [Haciendo tarea 2]")
        print("Agent A: [Haciendo tarea 3]")

        # Mientras, B procesa
        print("\nAgent B: 'Procesando cuando estoy libre'")
        print("Agent B: 'Enviando respuesta a la cola'")

        # A recibe cuando quiera
        print("\nAgent A: 'Oh! Respuesta disponible!'")
        print("Agent A: 'Procesando respuesta ahora'")

    def code_example(self):
        """
        Implementación
        """
        import queue
        from threading import Thread
        import time

        class AsyncAgent:
            def __init__(self, name):
                self.name = name
                self.inbox = queue.Queue()
                self.outbox = {}

            def send_async(self, recipient_queue, message):
                """
                Envía sin esperar (no-bloqueante)
                """
                # Solo pone en cola y continúa
                recipient_queue.put(message)
                print(f"{self.name}: Mensaje enviado (no espero)")

            def receive_async(self):
                """
                Procesa cuando hay tiempo
                """
                try:
                    message = self.inbox.get_nowait()
                    print(f"{self.name}: Procesando: {message}")
                    return message
                except queue.Empty:
                    # Sin mensajes, continúo
                    return None

            def work(self):
                """
                Trabajo continuo
                """
                for i in range(3):
                    print(f"{self.name}: Trabajando en tarea {i}")

                    # Intenta procesar mensajes
                    msg = self.receive_async()

                    time.sleep(0.1)

# ANÁLISIS:
print("""
ASÍNCRONO
Ventajas:
  ✓ No-bloqueante: emisor continúa
  ✓ Escalable: muchos simultáneamente
  ✓ Desacoplamiento temporal

Desventajas:
  ✗ Más complejo: manejar cola
  ✗ Receptor no sabe si llegó
  ✗ Mensajes desordenados posible

IDEAL: Múltiples agentes, comunicación frecuente
""")


# ═══════════════════════════════════════════════════════════════
# 3️⃣ PUBLISH-SUBSCRIBE (Desacoplamiento Total)
# ═══════════════════════════════════════════════════════════════

class PublishSubscribe:
    """
    PRODUCTORES PUBLICAN EN TÓPICOS
    SUSCRIPTORES RECIBEN AUTOMÁTICAMENTE

    VENTAJA: Emisor no conoce receptores

    DIAGRAMA:

    Sensor Temp   ┐
    Sensor Luz    ├─→ [TÓPICO: ambiente]
    Sensor Humedad┘
                         ↓
                    [EVENT BUS]
                         ↓
                   ┌─────┴─────┐
                   ↓           ↓
              [Logger]   [Dashboard]

    Sensor publica sin saber quién escucha
    Logger y Dashboard escuchan sin conocer sensor
    """

    def __init__(self):
        self.topics = {}  # tópico → [suscriptores]

    def subscribe(self, topic, subscriber):
        """
        Un agente se suscribe a un tópico
        """
        if topic not in self.topics:
            self.topics[topic] = []

        self.topics[topic].append(subscriber)

    def publish(self, topic, message):
        """
        Un agente publica en un tópico
        """
        if topic in self.topics:
            # TODOS los suscriptores reciben
            for subscriber in self.topics[topic]:
                subscriber.on_message(message)

    def example_smart_home(self):
        """
        Ejemplo: Casa inteligente
        """

        class Sensor:
            def __init__(self, name, bus):
                self.name = name
                self.bus = bus

            def measure(self, value):
                """
                Sensor PUBLICA (no sabe quién escucha)
                """
                self.bus.publish(
                    topic='sensors/temperature',
                    message={'sensor': self.name, 'value': value}
                )

        class Device:
            def __init__(self, name):
                self.name = name

            def on_message(self, message):
                """
                Device RECIBE (no conoce emisor)
                """
                print(f"{self.name} recibió: {message}")

        # Crear bus
        bus = PublishSubscribe()

        # Crear sensor
        sensor = Sensor('TempSensor1', bus)

        # Crear devices
        logger = Device('Logger')
        dashboard = Device('Dashboard')
        ac = Device('AirConditioner')

        # Devices se SUSCRIBEN
        bus.subscribe('sensors/temperature', logger)
        bus.subscribe('sensors/temperature', dashboard)
        bus.subscribe('sensors/temperature', ac)

        # Sensor PUBLICA (sin conocer subscribers)
        print("Sensor mide 28°C")
        sensor.measure(28)

        # RESULTADO: Todos reciben automáticamente
        # Logger:  "Temp: 28"
        # Dashboard: "Temp: 28"
        # AC: "Temp: 28, encendiendo"

# ANÁLISIS:
print("""
PUBLISH-SUBSCRIBE
Ventajas:
  ✓ Desacoplamiento total: productor no conoce consumidores
  ✓ Escalable: add/remove suscriptores sin cambiar código
  ✓ Flexible: mismo dato a múltiples destinos

Desventajas:
  ✗ Más complejidad
  ✗ Difícil debuggear
  ✗ Orden de mensajes no garantizado

IDEAL: Sistemas eventos, broadcasting
""")
```

### 2.2 Formatos de Mensajes

```python
# ═══════════════════════════════════════════════════════════════
# FORMATOS ESTÁNDAR
# ═══════════════════════════════════════════════════════════════

class MessageFormats:
    """
    ¿Cómo estructura agentes sus mensajes?
    """

    # 1️⃣ JSON (Simple, legible, estándar)
    @staticmethod
    def json_format():
        """
        JSON: Flexible, legible humano
        """
        message = {
            'from': 'Agent-A',
            'to': 'Agent-B',
            'type': 'request',
            'timestamp': '2025-11-13T14:30:00Z',
            'content': {
                'action': 'compute',
                'data': [1, 2, 3, 4, 5],
                'options': {'method': 'sum'}
            }
        }

        import json
        json_str = json.dumps(message)
        print(f"JSON: {json_str}")

        return message

    # 2️⃣ FIPA ACL (Estándar IEEE para agentes)
    @staticmethod
    def fipa_acl_format():
        """
        FIPA ACL: Estándar de IEEE para agentes
        """
        fipa_message = {
            'performative': 'request',  # Tipo de acto comunicativo
            'sender': 'buyer-agent',
            'receiver': 'seller-agent',
            'language': 'FIPA-SL',
            'ontology': 'commerce',
            'content': 'buy(item(name=laptop, quantity=2))',
            'reply-with': 'order-123',
            'in-reply-to': None
        }

        return fipa_message

    # 3️⃣ Protocol Buffers (Eficiente, tipado)
    @staticmethod
    def protobuf_example():
        """
        Protocol Buffers: Binario, eficiente, tipado

        Definición (proto file):

        message AgentMessage {
            string from = 1;
            string to = 2;
            int32 timestamp = 3;
            bytes payload = 4;
        }
        """

        # En código Python (después compilar .proto)
        message = {
            'from': 'agent-1',
            'to': 'agent-2',
            'timestamp': 1699860600,
            'payload': b'binary data'
        }

        return message

# Comparación de formatos:
print("""
FORMATO       TAMAÑO    VELOCIDAD   LEGIBLE   TIPADO    IDEAL
─────────────────────────────────────────────────────────────────
JSON          Grande    Lento       Sí        No        Desarrollo
FIPA ACL      Medio     Medio       Sí        No        Estándar
Protocol Buff Pequeño   Rápido      No        Sí        Producción
MQTT          Pequeño   Rápido      Parcial   No        IoT/Mobile
─────────────────────────────────────────────────────────────────
""")
```

### 2.3 Confiabilidad y Entrega

```python
class ReliableDelivery:
    """
    ¿CÓMO garantizar que el mensaje LLEGUE?
    """

    def __init__(self):
        self.messages_sent = {}
        self.messages_received = {}

    # ───────────────────────────────────────────────────────────
    # GARANTÍA 1: At-Most-Once
    # ───────────────────────────────────────────────────────────
    def at_most_once(self, sender, receiver, message):
        """
        ENVÍO Y OLVIDA

        Características:
        - Mensaje se envía UNA VEZ
        - Si se pierde, se pierde (no se reintenta)
        - Sin confirmación

        Riesgo: Puede no llegar
        Ventaja: Rápido, simple

        Uso: Datos no-críticos (telemetría)
        """
        msg_id = len(self.messages_sent) + 1

        try:
            receiver.receive(message)  # Intenta enviar
            self.messages_sent[msg_id] = 'sent'
            print(f"✓ Mensaje {msg_id}: Envío y olvida")
        except:
            self.messages_sent[msg_id] = 'lost'
            print(f"✗ Mensaje {msg_id}: Perdido (no se reintenta)")

    # ───────────────────────────────────────────────────────────
    # GARANTÍA 2: At-Least-Once
    # ───────────────────────────────────────────────────────────
    def at_least_once(self, sender, receiver, message, timeout=5):
        """
        ENVÍO CON REINTENTO

        Características:
        - Envía, espera ACK
        - Si no ACK → Reintenta
        - Puede llegar MÚLTIPLES VECES

        Garantía: NO SE PIERDE
        Riesgo: Puede duplicarse
        Ventaja: Confiable

        Uso: Datos importantes (pagos)
        """
        msg_id = len(self.messages_sent) + 1
        attempts = 0
        max_attempts = 3

        while attempts < max_attempts:
            try:
                # Intenta enviar
                receiver.receive(message)

                # Espera ACK
                ack = receiver.send_ack(msg_id, timeout=timeout)

                if ack:
                    self.messages_sent[msg_id] = 'delivered'
                    print(f"✓ Mensaje {msg_id}: Entregado (intento {attempts+1})")
                    return True

            except TimeoutError:
                attempts += 1
                print(f"⚠ Reintentando envío {attempts+1}/{max_attempts}")

        self.messages_sent[msg_id] = 'failed'
        print(f"✗ Mensaje {msg_id}: Falló después de {max_attempts} intentos")
        return False

    # ───────────────────────────────────────────────────────────
    # GARANTÍA 3: Exactly-Once
    # ───────────────────────────────────────────────────────────
    def exactly_once(self, sender, receiver, message):
        """
        ENVÍO EXACTAMENTE UNA VEZ

        Características:
        - Máxima garantía
        - Costoso (requiere BD distribuida)
        - Complejo de implementar

        Mecanismo:
        1. Envía mensaje con ID único
        2. Receiver verifica si ya vio ese ID
        3. Si ya vio → Rechaza duplicado
        4. Si nuevo → Procesa y guarda ID

        Uso: Transacciones críticas (dinero)
        """
        msg_id = str(hash(message))  # ID único del mensaje

        # Check: ¿Ya procesé este mensaje?
        if receiver.has_seen_message(msg_id):
            print(f"⚠ Mensaje {msg_id}: Duplicado detectado, rechazando")
            return False

        # Procesa solo si es nuevo
        receiver.receive(message)
        receiver.mark_message_seen(msg_id)

        self.messages_sent[msg_id] = 'exactly_once_delivered'
        print(f"✓ Mensaje {msg_id}: Entregado EXACTAMENTE UNA VEZ")
        return True

# COMPARACIÓN:
print("""
GARANTÍA            PÉRDIDA    DUPLICADOS    COMPLEJIDAD    USO
─────────────────────────────────────────────────────────────────
At-Most-Once         Posible   No            Baja           Telemetría
At-Least-Once        No        Posible       Media          Datos críticos
Exactly-Once         No        No            Alta           Transacciones
─────────────────────────────────────────────────────────────────
""")
```

---

Continuará en la siguiente parte...

