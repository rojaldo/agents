# Ejemplos MCP con LangChain y Ollama

Este directorio contiene ejemplos prácticos de implementación del **Model Context Protocol (MCP)** usando **LangChain** y **Ollama** para ejecutar modelos de lenguaje localmente.

## 📋 Contenido

1. **01_servidor_basico_langchain.py** - Servidor MCP básico con herramientas de procesamiento de lenguaje
2. **02_cliente_mcp_langchain.py** - Cliente MCP que se conecta e interactúa con servidores
3. **03_servidor_rag_langchain.py** - Servidor MCP con capacidades RAG (Retrieval Augmented Generation)

## 🚀 Requisitos Previos

### 1. Instalar Ollama

Ollama es necesario para ejecutar modelos de lenguaje localmente.

```bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh

# macOS
brew install ollama

# Windows
# Descargar desde https://ollama.com/download
```

### 2. Descargar Modelos

Descarga los modelos necesarios para los ejemplos:

```bash
# Modelo principal para generación de texto
ollama pull llama3.2

# Modelo para embeddings (necesario para RAG)
ollama pull nomic-embed-text
```

Verifica que los modelos estén instalados:

```bash
ollama list
```

### 3. Instalar Dependencias Python

```bash
# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## 📚 Ejemplos Detallados

### Ejemplo 1: Servidor MCP Básico

**Archivo:** `01_servidor_basico_langchain.py`

Este ejemplo implementa un servidor MCP con herramientas básicas de procesamiento de lenguaje:

**Herramientas disponibles:**
- `generar_texto` - Genera texto basado en un prompt
- `resumir_texto` - Resume textos largos
- `analizar_sentimiento` - Analiza el sentimiento de un texto
- `responder_pregunta` - Responde preguntas con contexto opcional

**Ejecución:**

```bash
python 01_servidor_basico_langchain.py
```

**Ejemplo de uso en código:**

```python
from servidor_basico_langchain import ServidorMCPLangChain

# Crear servidor
servidor = ServidorMCPLangChain(modelo="llama3.2")

# Usar herramientas
resultado = servidor.generar_texto("Explica qué es la IA")
print(resultado['texto_generado'])

# Resumir texto
resumen = servidor.resumir_texto("Texto largo aquí...")
print(resumen['resumen'])

# Analizar sentimiento
sentimiento = servidor.analizar_sentimiento("Me encanta este producto!")
print(sentimiento['sentimiento'])  # POSITIVO
```

**Salida esperada:**

```
✓ Servidor MCP inicializado con modelo: llama3.2
============================================================
Ejemplo 1: Generar texto
============================================================
Texto generado:
La inteligencia artificial (IA) es...
```

### Ejemplo 2: Cliente MCP

**Archivo:** `02_cliente_mcp_langchain.py`

Implementa un cliente que se conecta a un servidor MCP y utiliza sus herramientas de manera estructurada.

**Características:**
- Conexión y desconexión de servidores
- Descubrimiento de herramientas
- Flujos de trabajo automatizados
- Estadísticas de uso

**Ejecución:**

```bash
python 02_cliente_mcp_langchain.py
```

**Ejemplo de uso:**

```python
from cliente_mcp_langchain import ClienteMCPLangChain
from servidor_basico_langchain import ServidorMCPLangChain

# Crear servidor y cliente
servidor = ServidorMCPLangChain()
cliente = ClienteMCPLangChain("Mi Cliente")

# Conectar
await cliente.conectar(servidor)

# Listar herramientas
await cliente.listar_herramientas()

# Invocar herramienta
resultado = await cliente.invocar_herramienta(
    "generar_texto",
    prompt="Escribe sobre tecnología"
)

# Flujo completo
resultados = await cliente.flujo_generacion_contenido("IA en medicina")
```

**Flujos disponibles:**

1. **flujo_generacion_contenido** - Genera contenido, lo resume y analiza sentimiento
2. **flujo_qa_interactivo** - Responde múltiples preguntas con contexto

### Ejemplo 3: Servidor MCP con RAG

**Archivo:** `03_servidor_rag_langchain.py`

Implementa un servidor MCP con capacidades de RAG (Retrieval Augmented Generation) para consultas sobre documentos.

**Herramientas disponibles:**
- `crear_coleccion` - Crea una nueva colección de documentos
- `agregar_documentos` - Agrega documentos a una colección
- `consultar` - Realiza consultas RAG sobre documentos
- `buscar_similar` - Busca documentos similares
- `listar_colecciones` - Lista todas las colecciones

**Ejecución:**

```bash
python 03_servidor_rag_langchain.py
```

**Ejemplo de uso:**

```python
from servidor_rag_langchain import ServidorMCPRAG

# Crear servidor
servidor = ServidorMCPRAG(
    modelo_llm="llama3.2",
    modelo_embeddings="nomic-embed-text"
)

# Crear colección
servidor.crear_coleccion("mi_docs", "Mis documentos")

# Agregar documentos
documentos = [
    "Python es un lenguaje de programación...",
    "Machine Learning permite a las computadoras..."
]
servidor.agregar_documentos("mi_docs", documentos)

# Consultar
resultado = servidor.consultar(
    "mi_docs",
    "¿Qué es Python?",
    k=2  # Número de documentos relevantes
)
print(resultado['respuesta'])

# Buscar similares
similar = servidor.buscar_similar(
    "mi_docs",
    "programación",
    k=3
)
```

**Características técnicas:**

- **Embeddings locales** usando `nomic-embed-text`
- **Vector store** con FAISS (rápido y eficiente)
- **Text splitting** automático para documentos largos
- **Metadatos** para organizar documentos
- **Búsqueda semántica** por similitud

## 🔧 Configuración Avanzada

### Cambiar modelos

Puedes usar diferentes modelos de Ollama:

```python
# Modelos disponibles (descarga con: ollama pull <modelo>)
servidor = ServidorMCPLangChain(modelo="mistral")
servidor = ServidorMCPLangChain(modelo="llama2")
servidor = ServidorMCPLangChain(modelo="codellama")
```

### Ajustar parámetros del LLM

```python
from langchain_ollama import OllamaLLM

llm = OllamaLLM(
    model="llama3.2",
    temperature=0.7,  # Mayor = más creativo (0.0 - 1.0)
    top_p=0.9,
    num_ctx=4096,     # Tamaño del contexto
)
```

### Configurar RAG

```python
# Ajustar chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,   # Tamaño del chunk
    chunk_overlap=100, # Overlap entre chunks
)

# Ajustar retrieval
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}  # Número de documentos
)
```

## 🧪 Testing

### Verificar que Ollama está corriendo

```bash
# Debe devolver "Ollama is running"
curl http://localhost:11434
```

### Probar un modelo

```bash
ollama run llama3.2 "Hola, ¿cómo estás?"
```

### Ejecutar tests unitarios (si están disponibles)

```bash
pytest test_*.py -v
```

## 📊 Casos de Uso

### 1. Asistente de Documentación

```python
# Crear colección con documentación
servidor = ServidorMCPRAG()
servidor.crear_coleccion("docs_proyecto")

# Agregar archivos del proyecto
with open("README.md") as f:
    servidor.agregar_documentos("docs_proyecto", [f.read()])

# Consultar
resultado = servidor.consultar(
    "docs_proyecto",
    "¿Cómo instalar el proyecto?"
)
```

### 2. Análisis de Feedback

```python
servidor = ServidorMCPLangChain()

# Analizar múltiples comentarios
comentarios = [
    "Excelente producto!",
    "Muy malo, no funciona",
    "Está bien, podría mejorar"
]

for comentario in comentarios:
    resultado = servidor.analizar_sentimiento(comentario)
    print(f"{comentario}: {resultado['sentimiento']}")
```

### 3. Sistema de Q&A con Contexto

```python
cliente = ClienteMCPLangChain()
await cliente.conectar(servidor)

contexto = "LangChain es un framework para LLMs..."
preguntas = [
    "¿Qué es LangChain?",
    "¿Para qué sirve?"
]

resultados = await cliente.flujo_qa_interactivo(preguntas, contexto)
```

## ⚠️ Solución de Problemas

### Error: "Ollama not running"

```bash
# Iniciar Ollama
ollama serve
```

### Error: "Model not found"

```bash
# Descargar el modelo
ollama pull llama3.2
```

### Error: "Out of memory"

- Reduce el tamaño del contexto: `num_ctx=2048`
- Usa un modelo más pequeño
- Reduce `chunk_size` en RAG

### Error de importación de langchain

```bash
# Reinstalar dependencias
pip install --upgrade langchain langchain-ollama langchain-community
```

## 📈 Performance

### Benchmarks aproximados (en CPU i7)

| Operación | Tiempo | Tokens/s |
|-----------|--------|----------|
| Generar texto (100 tokens) | ~5-10s | 10-20 |
| Resumir texto | ~3-8s | 15-25 |
| RAG query | ~8-15s | 8-15 |
| Embeddings (1000 chars) | ~1-2s | - |

### Optimizaciones

1. **Usar GPU** si está disponible (mejora 5-10x)
2. **Cache de embeddings** para documentos frecuentes
3. **Batch processing** para múltiples operaciones
4. **Modelos cuantizados** para menor uso de memoria

## 🔐 Consideraciones de Seguridad

- ✅ Todo se ejecuta localmente (privacidad)
- ✅ No se envían datos a servidores externos
- ⚠️ Validar inputs en producción
- ⚠️ Limitar tamaño de documentos en RAG

## 📚 Recursos Adicionales

### Documentación

- [LangChain Docs](https://python.langchain.com/)
- [Ollama Docs](https://ollama.com/docs)
- [MCP Specification](https://spec.modelcontextprotocol.io/)

### Modelos recomendados para Ollama

| Modelo | Tamaño | Uso recomendado |
|--------|--------|-----------------|
| llama3.2 | 2GB | General, conversación |
| mistral | 4GB | Tareas complejas |
| codellama | 4GB | Código |
| nomic-embed-text | 274MB | Embeddings |

## 🤝 Contribuir

Para agregar nuevos ejemplos:

1. Crea un archivo numerado: `04_tu_ejemplo.py`
2. Sigue la estructura de los ejemplos existentes
3. Documenta las herramientas y casos de uso
4. Actualiza este README

## 📝 Licencia

Estos ejemplos son parte del material educativo del curso de Agentes de IA.

## ✨ Próximos Pasos

1. Explora los ejemplos en orden
2. Modifica los prompts y parámetros
3. Crea tus propias herramientas MCP
4. Integra con aplicaciones reales

¡Feliz aprendizaje! 🚀
