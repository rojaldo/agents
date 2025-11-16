# 🚀 QuickStart - Comienza en 5 minutos

## ⏱️ Pasos Rápidos

### Paso 1: Preparar Ollama (5 minutos)

```bash
# En MACOS/WINDOWS: Descarga desde https://ollama.ai y ejecuta

# En LINUX:
curl https://ollama.ai/install.sh | sh
ollama serve  # En terminal 1
```

### Paso 2: Descargar Modelo (3-5 minutos)

```bash
# En terminal 2
ollama pull mistral
# O más rápido:
ollama pull neural-chat
```

### Paso 3: Verificar Instalación (1 minuto)

```bash
# En terminal 3
cd ejemplos/langchain
python test_imports.py   # Debería mostrar ✅
python test_syntax.py    # Debería mostrar ✅
```

### Paso 4: Ejecutar tu Primer Ejemplo (2-5 minutos)

```bash
python 01_basic_llm.py
```

¡Listo! Deberías ver respuestas del LLM.

## 📖 Orden Recomendado para Aprender

```
1️⃣  Ejecuta 01_basic_llm.py
    Aprende: LLMs, prompts, parsers, LCEL

2️⃣  Lee Módulo 2 en docs/langchain.adoc
    (5 minutos)

3️⃣  Ejecuta 02_chains_basics.py
    Aprende: Cadenas, composición, streaming

4️⃣  Lee Módulo 3-4 en docs/langchain.adoc
    (10 minutos)

5️⃣  Ejecuta 03_memory.py
    Aprende: Memoria conversacional

6️⃣  Lee Módulo 5-6 en docs/langchain.adoc
    (10 minutos)

7️⃣  Ejecuta 04_agents.py
    Aprende: Agentes autónomos y herramientas

8️⃣  Lee Módulo 7-8 en docs/langchain.adoc
    (10 minutos)

9️⃣  Ejecuta 05_embeddings_vectorstore.py
    Aprende: Embeddings y búsqueda semántica

🔟  Ejecuta 06_rag_system.py
    Aprende: Sistema RAG completo
```

**Tiempo total estimado: 1.5-2 horas para entender todo**

## 🆘 Troubleshooting Rápido

| Problema | Solución |
|----------|----------|
| "No puedo conectar a Ollama" | Ejecuta `ollama serve` en otra terminal |
| "ModuleNotFoundError: langchain" | Ejecuta `python test_imports.py` |
| "Respuesta muy lenta" | Usa modelo más rápido: `ollama pull neural-chat` |
| "Modelo no encontrado" | Descarga: `ollama pull mistral` |
| "Código no funciona" | Ejecuta `python test_syntax.py` para verificar |

## 💡 Ejemplos Clave en Cada Archivo

### 01_basic_llm.py
```
✓ Crear LLM con Ollama
✓ Prompts simples y con variables
✓ Output parsers
✓ Composición LCEL
```

### 02_chains_basics.py
```
✓ Cadenas: prompt → LLM → parser
✓ RunnableLambda: funciones personalizadas
✓ RunnableParallel: procesamiento paralelo
✓ Stream: respuestas en tiempo real
✓ Lógica condicional
```

### 03_memory.py
```
✓ Memoria simple
✓ Memoria de ventana
✓ Chatbot interactivo (descomenta para probar)
✓ Memoria personalizada
```

### 04_agents.py
```
✓ Herramientas simples (@tool)
✓ Herramientas personalizadas
✓ Agente ReAct
✓ Razonamiento del agente (verbose)
```

### 05_embeddings_vectorstore.py
```
✓ Generar embeddings
✓ Vector store (FAISS)
✓ Búsqueda por similitud
✓ Guardando/cargando vector stores
```

### 06_rag_system.py
```
✓ RAG simple
✓ RAG mejorado
✓ Filtrado por relevancia
✓ RAG iterativo
```

## 📚 Recursos Rápidos

- **Documentación oficial**: https://docs.langchain.com
- **Ollama**: https://ollama.ai
- **Temario completo**: Ver `docs/langchain.adoc`
- **Guía de instalación**: Ver `SETUP.md`
- **Preguntas frecuentes**: Ver `README.md`

## 🎯 Próximos Pasos Después de Aprender

1. **Personaliza los ejemplos** para tu caso de uso
2. **Combina módulos**: Usa agentes con memoria
3. **Integra con tu aplicación**: FastAPI, Flask, etc.
4. **Cambia modelos**: Experimenta con neural-chat, llama2, etc.
5. **Explora integraciones**: Wikipedia, APIs externas, etc.

## ⚡ Cheat Sheet

```python
# LLM básico
from langchain_community.llms import Ollama
llm = Ollama(model="mistral")
respuesta = llm.invoke("Tu pregunta")

# Cadena simple
from langchain_core.prompts import PromptTemplate
prompt = PromptTemplate.from_template("Responde: {pregunta}")
cadena = prompt | llm
resultado = cadena.invoke({"pregunta": "¿Qué es Python?"})

# Memoria
from langchain.memory import ConversationBufferMemory
memoria = ConversationBufferMemory()
memoria.save_context(
    {"input": "Hola"},
    {"output": "¿Qué tal?"}
)

# Agente
from langchain.agents import create_react_agent, AgentExecutor
agente = create_react_agent(llm, herramientas, prompt)
executor = AgentExecutor(agent=agente, tools=herramientas)
resultado = executor.invoke({"input": "Tu pregunta"})

# Vector store
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
embeddings = OllamaEmbeddings(model="mistral")
vector_store = FAISS.from_documents(docs, embeddings)
resultados = vector_store.similarity_search("Tu pregunta")
```

## ✨ Tips Pro

1. **Usa streaming para UI**: `cadena.stream({"pregunta": "..."})`
2. **Batch para múltiples inputs**: `cadena.batch([...])`
3. **Verbose para debugging**: `executor = AgentExecutor(..., verbose=True)`
4. **Modelos pequeños para desarrollo rápido**: `neural-chat` es 10x más rápido
5. **Caching automático**: LangChain cachea respuestas por defecto

---

**¿Preguntas?** Consulta `README.md` o `SETUP.md`
