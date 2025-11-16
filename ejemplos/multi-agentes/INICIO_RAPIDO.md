# Guía de Inicio Rápido - Multi-Agentes con Ollama

**Tiempo estimado: 10 minutos**

## Paso 1: Verificar/Instalar Ollama (2 min)

### En Windows/Mac
```bash
# Descargar desde https://ollama.ai/download
# Instalar ejecutable
# Se abrirá automáticamente el servidor
```

### En Linux
```bash
curl https://ollama.ai/install.sh | sh
ollama serve  # Inicia el servidor
```

## Paso 2: Descargar Modelo (3-5 min)

```bash
# En nueva terminal
ollama pull mistral

# Verificar instalación
curl http://localhost:11434/api/tags
```

## Paso 3: Instalar Dependencias Python (1 min)

```bash
cd /home/rojaldo/cursos/agents/ejemplos/multi-agentes

# Opcional: crear entorno virtual
python -m venv venv
source venv/bin/activate

# Instalar dependencias (mínimas)
pip install requests
```

## Paso 4: Ejecutar tu Primer Ejemplo (2 min)

```bash
# El ejemplo más simple
python modulo1/01_agente_basico.py
```

## ✅ ¿Funcionó?

Si ves salida como esta:
```
════════════════════════════════════════════════════════════
      AGENTES AUTÓNOMOS - Ciclo Percepto-Acción
════════════════════════════════════════════════════════════

Agente creado: Agente-Explorador-1
Objetivo: Explorar y mapear el ambiente
...
```

**¡Felicidades! 🎉 Tu primer agente está funcionando**

## Próximos Pasos

### 1. Explorar Otros Ejemplos

```bash
# Arquitecturas
python modulo1/02_arquitecturas.py

# Comunicación entre agentes
python modulo2/01_comunicacion_basica.py

# Coordinación
python modulo3/01_coordinacion.py

# Colaboración
python modulo4/01_colaboracion.py

# Negociación
python modulo5/01_negociacion.py
```

### 2. Modificar los Ejemplos

Edita `modulo1/01_agente_basico.py`:

```python
# Línea ~130: Cambiar objetivo
objetivo="Tu nuevo objetivo aquí"

# Línea ~75: Cambiar número de ciclos
for i in range(5):  # Más ciclos
    agente.step(ambiente)
```

### 3. Crear Tu Propio Agente

```python
from utilidades.agent_base import Agent
from utilidades.ollama_client import OllamaClient

class MiAgentePersonalizado(Agent):
    def __init__(self, name, objetivo):
        client = OllamaClient(model="mistral")
        super().__init__(name=name, role="custom", model_client=client)
        self.objective = objetivo

    def _execute_action(self, action):
        # Tu lógica aquí
        return {"resultado": "done"}

# Usar
mi_agente = MiAgentePersonalizado("Mi-Agente", "Mi objetivo")
ambiente = {"param1": 100}
mi_agente.step(ambiente)
```

## Troubleshooting Rápido

| Problema | Solución |
|----------|----------|
| `Connection refused` | `ollama serve` en otra terminal |
| `Model not found` | `ollama pull mistral` |
| `Timeout` | Esperar, los modelos son lentos en CPU |
| `ImportError` | `pip install requests` |

## Conceptos Clave (30 segundos)

```
🤖 AGENTE = Entidad autónoma que:
   • Percibe el ambiente
   • Razona usando IA
   • Toma decisiones
   • Ejecuta acciones

📡 COMUNICACIÓN = Cómo hablan los agentes
   • Síncrona (esperando)
   • Asíncrona (en cola)
   • Pub-Sub (tópicos)

🎯 COORDINACIÓN = Cómo trabajan juntos
   • Centralizada (un jefe)
   • Jerárquica (jefes de equipos)
   • Distribuida (entre pares)

🤝 NEGOCIACIÓN = Cómo se ponen de acuerdo
   • Oferta-Contraoferta
   • BATNA (mejor alternativa)
   • Votación
```

## Preguntas Frecuentes

**P: ¿Necesito GPU?**
R: No, Ollama funciona en CPU. Mistral es pequeño (~3GB RAM).

**P: ¿Qué modelos puedo usar?**
R: `ollama list` muestra disponibles. Recomendado: mistral, neural-chat.

**P: ¿Puedo usar ChatGPT en lugar de Ollama?**
R: Sí, pero requiere API key. Ollama es local y gratuito.

**P: ¿Cuánto tardan los ejemplos?**
R: 5-30 segundos según tu CPU y número de ciclos.

**P: ¿Cómo modifico el número de agentes?**
R: En cada ejemplo, busca `for i in range(X)` y cambia X.

## Recursos

- 📖 [README Completo](README.md)
- 🎓 [Documentación del Temario](../01-multi-agentes-coordinacion.adoc)
- 🔧 [API de Utilidades](README.md#-api-principal)

---

**¡Ahora estás listo para aprender sobre sistemas multi-agente! 🚀**
