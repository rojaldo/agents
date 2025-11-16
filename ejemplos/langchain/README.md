# Ejemplos Funcionales de LangChain con Ollama

Este directorio contiene ejemplos funcionales y didácticos de LangChain configurados para funcionar con **Ollama en local**.

## Requisitos Previos

### 1. Instalar Ollama
Descarga e instala Ollama desde: https://ollama.ai

### 2. Descargar un modelo
```bash
ollama pull mistral
```

### 3. Iniciar Ollama
```bash
ollama serve
```
Ollama estará disponible en `http://localhost:11434`

### 4. Instalar dependencias de Python
```bash
pip install langchain langchain-community langchain-core ollama python-dotenv pydantic
```

## Ejemplos Disponibles

### 01_basic_llm.py - LLMs Básicos
**Conceptos**: Inicialización de modelos, prompts, output parsers, LCEL

```bash
python 01_basic_llm.py
```

**Qué aprenderás:**
- Crear un modelo Ollama
- Usar prompts simples y con templates
- Parsear salidas
- Composición con LCEL (operador |)
- Procesamiento en batch

---

### 02_chains_basics.py - Cadenas y LCEL
**Conceptos**: Composición de cadenas, RunnableLambda, procesamiento paralelo, streaming

```bash
python 02_chains_basics.py
```

**Qué aprenderás:**
- Construir cadenas simples
- Usar RunnableLambda para funciones personalizadas
- Procesamiento paralelo con RunnableParallel
- Streaming de respuestas
- Cadenas condicionales

---

### 03_memory.py - Gestión de Memoria
**Conceptos**: ConversationBufferMemory, ConversationWindowMemory, chatbots stateful

```bash
python 03_memory.py
```

**Qué aprenderás:**
- Almacenamiento de historial completo
- Memoria con ventana de últimos turnos
- Construcción de chatbots conversacionales
- Persistencia de memoria
- Crear memoria personalizada

---

### 04_agents.py - Agentes Autónomos
**Conceptos**: Herramientas, ReAct, AgentExecutor, razonamiento

```bash
python 04_agents.py
```

**Qué aprenderás:**
- Crear herramientas con decorador @tool
- Crear herramientas personalizadas con BaseTool
- Construir agentes ReAct
- Configurar AgentExecutor
- Razonamiento de agentes (Thought/Action/Observation)

---

### 05_embeddings_vectorstore.py - Embeddings y Vector Stores
**Conceptos**: Embeddings con Ollama, FAISS, búsqueda semántica

```bash
python 05_embeddings_vectorstore.py
```

**Qué aprenderás:**
- Generar embeddings de texto
- Crear vector stores con FAISS
- Búsqueda por similitud
- Text splitters para chunking
- Persistencia de vector stores

---

### 06_rag_system.py - Sistema RAG Completo
**Conceptos**: RAG, Retrieval, Augmentation, Generation

```bash
python 06_rag_system.py
```

**Qué aprenderás:**
- Sistema RAG simple (Retrieve + Generate)
- RAG con contexto mejorado
- Filtrado por relevancia
- Diferentes estrategias de retrieval
- RAG iterativo

---

## Estructura de los Ejemplos

Cada archivo sigue una estructura consistente:

```python
def ejemplo_1():
    """Descripción breve"""
    print("=" * 60)
    print("EJEMPLO 1: Título")
    print("=" * 60)
    # ... código ...

def ejemplo_2():
    # ... más ejemplos ...

if __name__ == "__main__":
    try:
        ejemplo_1()
        ejemplo_2()
        # ...
        print("✅ Completado")
    except Exception as e:
        print(f"❌ Error: {e}")
```

## Solución de Problemas

### "No puedo conectar a Ollama"
```bash
# Verifica que Ollama está ejecutándose
curl http://localhost:11434/api/tags

# Si no está corriendo, inicia Ollama en otra terminal:
ollama serve
```

### "El modelo no existe"
```bash
# Descarga el modelo
ollama pull mistral

# Lista modelos disponibles
ollama list
```

### "ModuleNotFoundError: No module named 'langchain'"
```bash
# Instala las dependencias
pip install langchain langchain-community langchain-core
```

### Respuestas lentas
- Los primeros ejemplos son lentos porque descargan el modelo a memoria
- Ejemplos posteriores son más rápidos
- Usa un modelo más pequeño: `ollama pull neural-chat`

## Flujo Recomendado de Aprendizaje

1. **01_basic_llm.py** - Comienza aquí, aprende los fundamentos
2. **02_chains_basics.py** - Composición de cadenas
3. **03_memory.py** - Agregar contexto conversacional
4. **04_agents.py** - Sistemas autónomos
5. **05_embeddings_vectorstore.py** - Búsqueda semántica
6. **06_rag_system.py** - Sistema completo RAG

## Notas sobre Ollama

### Modelos Recomendados

| Modelo | Tamaño | Velocidad | Calidad | Ideal para |
|--------|--------|-----------|---------|-----------|
| mistral | 4.1GB | Rápido | Buena | Desarrollo, testing |
| neural-chat | 3.8GB | Muy rápido | Aceptable | Prototipos rápidos |
| llama2 | 3.8GB | Rápido | Muy buena | Aplicaciones |
| openchat | 3.5GB | Muy rápido | Buena | Producción ligera |

### Cambiar modelo
```python
# En los ejemplos, cambia:
llm = Ollama(model="neural-chat", ...)  # Cambiar "mistral" por otro
```

## Recursos Adicionales

- [Documentación de LangChain](https://docs.langchain.com)
- [Documentación de Ollama](https://ollama.ai)
- [Repositorio de Ollama](https://github.com/jmorganca/ollama)
- [Ejemplos de LangChain](https://github.com/langchain-ai/langchain)

## Estructura Recomendada para Proyectos

```
mi_proyecto/
├── .env                    # Variables de entorno
├── requirements.txt        # Dependencias
├── src/
│   ├── config.py          # Configuración
│   ├── models.py          # Inicialización de LLMs
│   ├── chains.py          # Definición de cadenas
│   ├── agents.py          # Definición de agentes
│   ├── tools.py           # Herramientas personalizadas
│   └── memory.py          # Gestión de memoria
├── data/
│   ├── documents/         # Documentos para RAG
│   └── vectors/           # Vector stores
├── examples/              # Scripts de ejemplo
└── main.py               # Punto de entrada
```

## Tips de Optimización

1. **Caching**: LangChain cachea respuestas automáticamente
2. **Batch processing**: Usa `batch()` en lugar de `invoke()` múltiples veces
3. **Streaming**: Usa `stream()` para UI responsivas
4. **Modelos más pequeños**: Usa neural-chat para iteración rápida
5. **Async/await**: Para aplicaciones web, usa versiones async

## Contribuyendo

Para agregar nuevos ejemplos:

1. Crea un archivo `0X_nombre.py` siguiendo la estructura
2. Incluye docstring con descripción
3. Agrega al menos 3-5 ejemplos relacionados
4. Actualiza este README

## Licencia

Estos ejemplos son educativos y pueden usarse libremente con fines de aprendizaje.
