# 🚀 Langflow - Quick Start Guide

## En 5 Minutos

### Paso 1: Validar (sin instalar nada)
```bash
cd /home/rojaldo/cursos/agents/ejemplos/langflow
python test_syntax.py
```
**Resultado esperado:** ✅ Todos los archivos son válidos

### Paso 2: Instalar dependencias mínimas
```bash
pip install langchain-core langchain-community
```

### Paso 3: Instalar Ollama (una sola vez)
```bash
# Linux/macOS
curl https://ollama.ai/install.sh | sh

# Descargar modelo
ollama pull mistral
```

### Paso 4: Ejecutar ejemplo
```bash
# Terminal 1: Iniciar Ollama
ollama serve

# Terminal 2: Ejecutar ejemplo
python 01_chatbot_simple.py
```

---

## 📚 Ejemplos Quick Reference

### Ejemplo 1: Chat Simple
```bash
python 01_chatbot_simple.py
```
**Aprenderás:** Prompts, memoria, conversaciones

### Ejemplo 2: Integraciones
```bash
python 02_componentes_integracion.py
```
**Aprenderás:** Web search, APIs, JSON parsing

### Ejemplo 3: RAG
```bash
python 03_rag_document_processing.py
```
**Aprenderás:** Embeddings, vector stores, RAG

### Ejemplo 4: Patrones
```bash
python 04_patrones_avanzados.py
```
**Aprenderás:** Routing, fallbacks, error handling

### Ejemplo 5: API
```bash
python 05_exportacion_api.py
```
**Aprenderás:** FastAPI, autenticación, monitoreo

### Ejemplo 6: Proyecto Final
```bash
python 06_proyecto_final.py
```
**Aprenderás:** Arquitectura integrada

---

## 🎯 Ruta de Aprendizaje (Recomendada)

**Día 1 (2-3 horas):**
1. ✅ Validar con `test_syntax.py`
2. ✅ Ejecutar `01_chatbot_simple.py`
3. ✅ Ejecutar `02_componentes_integracion.py`

**Día 2 (2-3 horas):**
1. ✅ Ejecutar `03_rag_document_processing.py`
2. ✅ Ejecutar `04_patrones_avanzados.py`

**Día 3 (2-3 horas):**
1. ✅ Ejecutar `05_exportacion_api.py`
2. ✅ Ejecutar `06_proyecto_final.py`

**Total:** 6-9 horas

---

## 🔍 Conceptos Clave

### 1. Prompts
```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente útil"),
    ("user", "{input}")
])
cadena = prompt | llm
respuesta = cadena.invoke({"input": "¿Hola?"})
```

### 2. Memoria
```python
memoria = ConversationBufferMemory(return_messages=True)
historial = memoria.load_memory_variables({})
# ... usar historial
memoria.save_context({"input": entrada}, {"output": respuesta})
```

### 3. Web Search
```python
search = DuckDuckGoSearchRun()
resultados = search.run("¿Qué tiempo hace?")
```

### 4. RAG
```python
from langchain_community.vectorstores import FAISS
vector_store = FAISS.from_documents(documentos, embeddings)
docs = vector_store.similarity_search(query, k=2)
```

### 5. Error Handling
```python
try:
    respuesta = cadena.invoke({...})
except TimeoutError:
    respuesta = "Timeout"
except Exception as e:
    respuesta = f"Error: {e}"
```

---

## 📊 Estructura de Archivos

```
ejemplos/langflow/
├── 01_chatbot_simple.py          ← Comienza aquí
├── 02_componentes_integracion.py
├── 03_rag_document_processing.py
├── 04_patrones_avanzados.py
├── 05_exportacion_api.py
├── 06_proyecto_final.py
├── test_syntax.py                ← Valida primero
├── README.md                     ← Documentación completa
└── SUMMARY.md                    ← Resumen detallado
```

---

## ❓ Preguntas Frecuentes

**P: ¿Puedo ejecutar ejemplos sin Ollama?**
R: Sí, con `test_syntax.py`. Para los demás ejemplos necesitas Ollama.

**P: ¿Puedo usar ChatGPT en lugar de Ollama?**
R: Sí, modifica el LLM en los ejemplos:
```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(api_key="...", model="gpt-4")
```

**P: ¿Dónde está la documentación?**
R:
- Teoría: `docs/langflow.adoc` (1,870 líneas)
- Resumen: `SUMMARY.md` (este archivo)
- Completa: `README.md`

**P: ¿Cuánto tiempo toma completar?**
R: 6-9 horas (1-2 horas por módulo)

**P: ¿Hay certificado?**
R: No, pero aprenderás habilidades productivas.

---

## 🔧 Troubleshooting

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError` | `pip install langchain-core langchain-community` |
| Ollama no responde | Asegúrate que `ollama serve` está ejecutándose |
| Error de timeout | Aumenta timeout en código o espera más |
| Error de embedding | Descarga modelo: `ollama pull mistral` |

---

## 📖 Recursos Adicionales

- **Documentación oficial:** https://docs.langchain.com
- **Ollama:** https://ollama.ai
- **Langflow:** https://github.com/logspace-ai/langflow
- **LangChain:** https://github.com/langchain-ai/langchain

---

## ✨ Próximos Pasos

1. **Completar ejemplos** (1-3 días)
2. **Modificar ejemplos** para tus casos de uso
3. **Crear proyecto propio** usando patrones aprendidos
4. **Desplegar API** usando ejemplo 05 como base

---

## 📝 Notas

- Todos los ejemplos usan **Ollama local** (http://localhost:11434)
- Código con **patrones profesionales** (tipo hints, logging, error handling)
- **100% validado** - sintaxis correcta garantizada
- **Totalmente extensible** - personaliza según necesites

---

**¡Listo para empezar!** 🚀

Ejecuta: `python test_syntax.py` → `python 01_chatbot_simple.py`
