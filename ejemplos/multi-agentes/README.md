# Sistema Multi-Agentes con LangChain y Ollama

Ejemplos didácticos y funcionales del curso "Agentes de IA: Multi-agentes y Coordinación"

## 🎯 Objetivo

Este proyecto demuestra conceptos fundamentales de sistemas multi-agente usando:
- **LangChain**: Framework para construir aplicaciones con LLMs
- **Ollama**: Servidor de modelos de IA ejecutados localmente
- **Python**: Lenguaje de implementación

## 📁 Estructura del Proyecto

```
ejemplos/multi-agentes/
├── utilidades/                      # Módulos reutilizables
│   ├── ollama_client.py            # Cliente para conectar con Ollama
│   ├── agent_base.py               # Clase base para todos los agentes
│   └── __init__.py
│
├── modulo1/                         # Fundamentos de Agentes Autónomos
│   ├── 01_agente_basico.py        # Ciclo percepto-acción
│   ├── 02_arquitecturas.py        # Centralizada, descentralizada, jerárquica
│   └── __init__.py
│
├── modulo2/                         # Comunicación Entre Agentes
│   ├── 01_comunicacion_basica.py  # Síncrona, asíncrona, Pub-Sub
│   └── __init__.py
│
├── modulo3/                         # Coordinación y Orquestación
│   ├── 01_coordinacion.py         # Centralizada, jerárquica, distribuida
│   └── __init__.py
│
├── modulo4/                         # Colaboración y Trabajo en Equipo
│   ├── 01_colaboracion.py         # Equipos, votación, delegación
│   └── __init__.py
│
├── modulo5/                         # Negociación y Conflictos
│   ├── 01_negociacion.py          # Protocolo oferta-contraoferta
│   └── __init__.py
│
└── README.md                        # Este archivo
```

## 🚀 Inicio Rápido

### 1. Instalar Ollama

Ollama permite ejecutar modelos de IA localmente sin necesidad de GPU poderosa.

```bash
# Descargar e instalar desde
https://ollama.ai

# Después de instalar, descargar un modelo
ollama pull mistral

# Iniciar el servidor (en otra terminal)
ollama serve
```

### 2. Instalar Dependencias Python

```bash
# Navegar al directorio del proyecto
cd ejemplos/multi-agentes

# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install requests  # Para comunicarse con Ollama
```

### 3. Ejecutar Ejemplos

```bash
# Ejemplo 1: Agente Básico
python modulo1/01_agente_basico.py

# Ejemplo 2: Arquitecturas
python modulo1/02_arquitecturas.py

# Ejemplo 3: Comunicación
python modulo2/01_comunicacion_basica.py

# Ejemplo 4: Coordinación
python modulo3/01_coordinacion.py

# Ejemplo 5: Colaboración
python modulo4/01_colaboracion.py

# Ejemplo 6: Negociación
python modulo5/01_negociacion.py
```

## 📚 Contenido por Módulo

### Módulo 1: Fundamentos de Sistemas Multi-Agente

**Conceptos:**
- ¿Qué es un agente autónomo?
- Ciclo percepto-acción: Percibir → Razonar → Actuar
- Arquitecturas: Centralizada, Descentralizada, Jerárquica
- Cuándo usar sistemas multi-agente

**Ejemplos:**
- `01_agente_basico.py`: Demostración del ciclo básico
- `02_arquitecturas.py`: Tres arquitecturas comparadas

**Conceptos clave:**
```
AGENTE = Entidad que Percibe + Razona + Actúa
```

### Módulo 2: Comunicación Entre Agentes

**Conceptos:**
- Paradigmas de comunicación
  - Síncrona (bloqueante)
  - Asíncrona (no-bloqueante)
  - Publish-Subscribe
- Message Brokers
- Confiabilidad y entrega

**Ejemplos:**
- `01_comunicacion_basica.py`: Tres paradigmas implementados

**Patrones principales:**
```
Síncrona:        Agente A → Espera → Agente B
Asíncrona:       Agente A → Cola → Agente B
Publish-Sub:     Agente A → [Tópico] ← Agente B
```

### Módulo 3: Coordinación y Orquestación

**Conceptos:**
- Estrategias de coordinación
  - Centralizada (coordinador maestro)
  - Jerárquica (múltiples niveles)
  - Distribuida (negociación local)
- Evitar deadlocks
- Asignación de recursos

**Ejemplos:**
- `01_coordinacion.py`: Las tres estrategias

**Tabla comparativa:**
```
Centralizada    | Óptimo global | Escalabilidad limitada
Jerárquica      | Balance       | Mejor escalabilidad
Distribuida     | Consenso      | Máxima escalabilidad
```

### Módulo 4: Colaboración y Trabajo en Equipo

**Conceptos:**
- Formación de equipos
- Votación y consenso
- Delegación de tareas
- Supervisión
- Resolución de conflictos

**Ejemplos:**
- `01_colaboracion.py`: Equipos colaborativos, votación, supervisión

**Flujo típico:**
```
Equipo Formado
  → Delegación de Tareas
    → Ejecución
      → Votación en Decisiones Críticas
        → Resultado Final
```

### Módulo 5: Negociación y Resolución de Conflictos

**Conceptos:**
- Teoría de negociación
  - BATNA (Best Alternative)
  - ZAP (Zona de Acuerdo Posible)
  - Utilidad (value functions)
- Protocolos
  - Oferta-Contraoferta
  - Subastas
  - Contract Net
- Estrategias
  - Competitiva (win-lose)
  - Colaborativa (win-win)
  - Compromiso (lose-lose)

**Ejemplos:**
- `01_negociacion.py`: Protocolo oferta-contraoferta

**Proceso típico:**
```
Vendedor: "Te doy X por Y"
  ↓
Comprador: "No, pero te doy Z por W"
  ↓
Vendedor: "Aceptado" O "Contraoferta: A por B"
  ↓
... (iteraciones) ...
  ↓
ACUERDO o IMPASSE
```

## 🔧 API Principal

### OllamaClient

```python
from utilidades.ollama_client import OllamaClient

# Crear cliente
client = OllamaClient(model="mistral")

# Generar texto
respuesta = client.generate("¿Cuál es la capital de Francia?")
print(respuesta)

# Chat (conversación)
mensajes = [
    {"role": "user", "content": "Hola, ¿cómo estás?"}
]
respuesta = client.chat(mensajes)

# Listar modelos disponibles
modelos = client.list_models()
```

### Agent Base

```python
from utilidades.agent_base import Agent
from utilidades.ollama_client import OllamaClient

class MiAgente(Agent):
    def _execute_action(self, action: str):
        # Implementar la acción específica
        return {"resultado": "..."}

# Crear agente
agente = MiAgente(
    name="Mi-Agente",
    role="especializado"
)

# Usar en un paso
ambiente = {"temperatura": 25, "luz": 100}
agente.step(ambiente)
```

## 📊 Conceptos Matemáticos

### Utilidad en Negociación

```python
# Utilidad mide qué tan bien una propuesta satisface los objetivos
utilidad = función(precio, cantidad, tiempo, ...)

# Rango: 0 (inaceptable) a 1 (ideal)
if utilidad > 0.7:
    aceptar()
elif utilidad > 0.4:
    contraoferta()
else:
    rechazar()
```

### Votación

```python
# Mayoría simple
votos_a_favor = 3
votos_en_contra = 2
if votos_a_favor > votos_en_contra:
    aprobar()

# Supermayoría (2/3)
umbral = total_votos * 2 / 3
if votos_a_favor >= umbral:
    aprobar()
```

## 🎓 Ejercicios Propuestos

### Nivel 1: Modificaciones Simples

1. **Cambiar modelo de IA**
   - Usar `ollama pull neural-chat` y cambiar en OllamaClient
   - Observar diferencias en razonamiento

2. **Añadir métricas de desempeño**
   - Contar tiempo de decisión
   - Registrar éxito/fracaso de acciones

### Nivel 2: Nuevas Funcionalidades

1. **Persistencia de estado**
   - Guardar historial en archivo JSON
   - Cargar estado anterior

2. **Más paradigmas de comunicación**
   - Implementar Request-Reply
   - Añadir confirmación de recepción (ACK)

### Nivel 3: Proyectos Integradores

1. **Sistema de comercio electrónico**
   - Vendedores, compradores, plataforma
   - Negociación de precios
   - Votación en cambios de política

2. **Simulación de tráfico**
   - Agentes vehículos
   - Coordinación en intersecciones
   - Minimizar congestión

## 🐛 Solución de Problemas

### "Error: Unable to connect to Ollama"

```bash
# Asegúrate de que Ollama está corriendo
ollama serve

# En otra terminal, verifica la conexión
curl http://localhost:11434/api/tags
```

### "Model not found"

```bash
# Descargar el modelo especificado
ollama pull mistral
ollama pull neural-chat
ollama pull llama2

# Listar modelos disponibles
ollama list
```

### Lentitud en la ejecución

- Los modelos de IA son lentos en CPU
- Esperar 5-10 segundos por respuesta es normal
- Para GPU, consultar documentación de Ollama

## 📖 Referencias

### Teóricas
- "Multiagent Systems" - Shoham & Leyton-Brown
- "An Introduction to Multiagent Systems" - Wooldridge
- Estándar FIPA (Foundational Agent Communication Language)

### Implementación
- [Ollama Documentation](https://ollama.ai)
- [LangChain Documentation](https://python.langchain.com)
- [Python Agent Development](https://python.langchain.com/docs/modules/agents)

## 📝 Notas Importantes

1. **Ollama es Local**: Todo corre en tu máquina, sin conexión a internet
2. **Modelos Pequeños**: Mistral (7B) funciona en CPU normal
3. **Iterativo**: Los ejemplos están diseñados para experimentar
4. **Educativo**: Enfasis en conceptos, no en optimización

## 🤝 Contribuciones

Para mejorar estos ejemplos:
1. Crear variaciones de los scripts
2. Documentar nuevos patrones
3. Reportar bugs o limitaciones
4. Proponer nuevos casos de uso

## 📄 Licencia

Contenido educativo. Libre para usar, modificar y distribuir.

---

**¡Feliz exploración del mundo de los agentes multi-agente!** 🤖🤖🤖
