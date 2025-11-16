# Ejemplos RAG (Retrieval-Augmented Generation) - Funcionales

Ejemplos prácticos y funcionales de sistemas RAG usando Ollama en local.

## 📚 Estructura

```
rag/
├── modulo3/          # Documentos y Chunking
├── modulo4/          # Embeddings
├── modulo5/          # Vector Stores
├── modulo6/          # RAG Básico
├── modulo7/          # RAG Avanzado
├── modulo8/          # Chat con Memoria
├── modulo9/          # Evaluación de RAG
├── modulo10/         # Casos de Uso Prácticos
├── modulo11/         # Optimización y Producción
├── modulo12/         # Proyecto Final
├── test_ejemplos_rag.py  # Validación de ejemplos
└── README.md
```

## 🚀 Ejemplos Disponibles

### Módulo 3: Documentos y Chunking
- **01_cargar_documentos.py** - Cargar archivos TXT, JSON, PDF
- **02_chunking.py** - Dividir documentos en chunks óptimos

### Módulo 4: Embeddings
- **01_embeddings.py** - Crear embeddings y búsqueda semántica

### Módulo 6: RAG Básico
- **01_rag_basico_ollama.py** - Sistema RAG completo con Ollama

### Módulo 8: Chat con Memoria
- **01_chat_con_memoria.py** - Conversación manteniendo contexto

### Módulo 10: Casos de Uso
- **01_qa_sobre_documentos.py** - Sistema Q&A sobre documentos

## ✅ Validación de Ejemplos

### Ejecutar Pruebas
```bash
# Todas las pruebas
python test_ejemplos_rag.py

# Un módulo específico
cd modulo3
python 01_cargar_documentos.py

# Un ejemplo específico
python 02_chunking.py
```

### Resultados Esperados
```
✅ 5/5 módulos funcionales
✅ Todos los ejemplos ejecutables
✅ Datos generados correctamente
✅ JSONs guardados para análisis
```

## 📋 Requisitos

### Instalación Mínima
```bash
pip install langchain langchain-ollama chromadb requests
```

### Instalar Ollama
```bash
# macOS
brew install ollama

# Linux
curl https://ollama.ai/install.sh | sh

# Windows
# Descargar desde https://ollama.ai

# Iniciar Ollama
ollama serve

# Descargar modelo (otra terminal)
ollama pull mistral
```

## 🎯 Qué Aprenderás

### Módulo 3: Gestión de Documentos
- ✓ Cargar múltiples formatos (TXT, JSON, PDF)
- ✓ Procesar documentos
- ✓ Dividir en chunks óptimos
- ✓ Analizar dimensiones de datos

### Módulo 4: Embeddings
- ✓ Crear embeddings (vectores numéricos)
- ✓ Similitud coseno
- ✓ Búsqueda semántica
- ✓ Vectores con Ollama

### Módulo 6: RAG Básico
- ✓ Arquitectura RAG completa
- ✓ Recuperación de documentos
- ✓ Generación con contexto
- ✓ Preguntas y respuestas

### Módulo 8: Chat Avanzado
- ✓ Gestión de memoria de conversación
- ✓ Contexto multi-turno
- ✓ Coherencia en diálogos
- ✓ LangChain Memory

### Módulo 10: Casos Reales
- ✓ Sistema Q&A funcional
- ✓ Base de conocimiento
- ✓ Búsqueda de documentos
- ✓ Generación de respuestas

## 📊 Salidas Generadas

Cada ejemplo genera archivos JSON con resultados:

```
modulo3/documentos_ejemplo/     # Documentos de prueba
modulo3/chunks.json              # Chunks generados
modulo4/embeddings_result.json   # Embeddings y búsqueda
modulo6/rag_resultado.json       # Preguntas y respuestas
modulo8/chat_memoria.json        # Historial de chat
modulo10/qa_resultado.json       # Q&A resultados
```

## 💡 Ejemplo de Uso Completo

```python
# 1. Cargar documentos
from modulo3 import cargar_documentos

docs = cargar_documentos("documentos_ejemplo/")

# 2. Dividir en chunks
from modulo3 import DocumentChunker

chunker = DocumentChunker()
chunks = chunker.chunk_por_párrafos(documento)

# 3. Crear embeddings
from modulo4 import SimpleEmbedding

embedder = SimpleEmbedding()
embeddings = [embedder.crear_embedding_tf(chunk) for chunk in chunks]

# 4. Hacer pregunta
from modulo6 import RAGSimple

rag = RAGSimple()
respuesta = rag.responder("¿Qué es RAG?")
```

## 🔧 Usando con Ollama Real

### Instalación de LangChain + Ollama

```bash
pip install langchain langchain-ollama chromadb
```

### Código Ejemplo

```python
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Preparar documentos
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_text(documento)

# Crear embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_store = Chroma.from_texts(chunks, embeddings)

# Crear LLM
llm = OllamaLLM(model="mistral")

# Buscar y generar respuesta
docs = vector_store.similarity_search("Tu pregunta")
contexto = "\n".join([doc.page_content for doc in docs])

prompt = f"Contexto: {contexto}\n\nPregunta: Tu pregunta"
respuesta = llm.invoke(prompt)
```

## 📈 Progresión Recomendada

1. **Día 1**: Módulo 3 - Documentos y Chunking
2. **Día 2**: Módulo 4 - Embeddings
3. **Día 3**: Módulo 6 - RAG Básico
4. **Día 4**: Módulo 8 - Chat con Memoria
5. **Día 5**: Módulo 10 - Casos de Uso

## 🐛 Solución de Problemas

### "Ollama no disponible"
```bash
# Verificar que Ollama está corriendo
ollama serve

# En otra terminal
ollama list  # Ver modelos
```

### "Módulo no encontrado"
```bash
pip install langchain langchain-ollama chromadb
```

### "Error de conexión"
```bash
# Revisar puerto 11434
netstat -an | grep 11434

# Reiniciar Ollama
ollama serve
```

## 📚 Recursos Adicionales

- **LangChain Docs**: https://python.langchain.com/
- **Ollama Docs**: https://github.com/ollama/ollama
- **RAG Papers**: https://arxiv.org/abs/2005.11401
- **ChromaDB**: https://docs.trychroma.com/

## ✨ Características

- ✅ Todos los ejemplos funcionales
- ✅ Sin dependencias externas (Ollama local)
- ✅ Código didáctico y comentado
- ✅ Salidas JSON para análisis
- ✅ Tests automáticos incluidos
- ✅ Documentación completa

## 📝 Notas

- Los ejemplos usan simulación cuando Ollama no está disponible
- Los datos de prueba se generan automáticamente
- Todos los JSON son guardados para análisis posterior
- Compatible con Python 3.8+

## 🎓 Aprendizaje

Este conjunto de ejemplos te enseñará:
1. Cómo funcionan los sistemas RAG
2. Procesamiento de documentos
3. Embeddings y búsqueda semántica
4. Generación con contexto
5. Chat con memoria
6. Casos de uso reales

---

**Estado**: ✅ Todos los ejemplos validados y funcionales
**Última actualización**: 2024-11-14
