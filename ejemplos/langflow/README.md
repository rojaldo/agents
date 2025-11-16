# Langflow - Curso Completo de Plataforma Visual para IA

## 📚 Descripción General

Este directorio contiene ejemplos funcionales y documentación completa de **Langflow**, una plataforma visual para construir flujos de trabajo con LLMs sin necesidad de código. Incluye 10 módulos progresivos que cubren desde conceptos fundamentales hasta un sistema integral de asistente IA.

## 📁 Estructura del Proyecto

```
ejemplos/langflow/
├── README.md                          # Este archivo
├── test_syntax.py                    # Validador de sintaxis de ejemplos
├── run_all_examples.py               # Script maestro para ejecutar todos los ejemplos
├── ../../../docs/langflow.adoc       # Documentación completa (1870+ líneas)
│
├── 01_chatbot_simple.py              # Chat simple, con memoria, personalidades, multi-turno
├── 02_componentes_integracion.py     # Web search, HTTP requests, prompts, text processing
├── 03_rag_document_processing.py     # Text splitting, embeddings, vector stores, RAG
├── 04_patrones_avanzados.py          # Routing, fallbacks, error handling, custom components
├── 05_exportacion_api.py             # FastAPI, autenticación, rate limiting, monitoreo
├── 06_proyecto_final.py              # Asistente integrado combinando todos los conceptos
│
├── modulo_1/ ... modulo_10/          # Módulos antiguos (referencia)
└── output/                           # Resultados y reportes generados
```

## 🚀 Quick Start

### Requisitos Previos

```bash
# Python 3.8+
python --version

# Crear entorno virtual
python -m venv langflow_env

# Activar entorno (Linux/macOS)
source langflow_env/bin/activate

# Activar entorno (Windows)
langflow_env\Scripts\activate
```

### Validar Ejemplos

Antes de ejecutar, valida que la sintaxis es correcta:

```bash
# Validar sintaxis de todos los ejemplos
python test_syntax.py
```

### Ejecutar Ejemplos Individuales

**Nuevos ejemplos integrados (recomendado):**

```bash
# Ejemplo 1: Chat simple, con memoria y personalidades
python 01_chatbot_simple.py

# Ejemplo 2: Componentes e integraciones (web search, HTTP)
python 02_componentes_integracion.py

# Ejemplo 3: RAG - Procesamiento de documentos
python 03_rag_document_processing.py

# Ejemplo 4: Patrones avanzados (routing, fallbacks, error handling)
python 04_patrones_avanzados.py

# Ejemplo 5: Exportación a API (FastAPI, autenticación, monitoreo)
python 05_exportacion_api.py

# Ejemplo 6: Proyecto final integrado
python 06_proyecto_final.py
```

**Ejemplos por módulos (legado):**

```bash
python modulo_1/01_hello_langflow.py
python modulo_2/01_components.py
# ... y así sucesivamente
```

### Ejecutar Todos los Ejemplos

```bash
# Script maestro que ejecuta todos los módulos
python run_all_examples.py
```

## 📖 Nuevos Ejemplos Integrados

### 1️⃣ Chatbot Simple (`01_chatbot_simple.py`)
**4 ejemplos progresivos:**
1. **Chat simple**: Conversación sin memoria
2. **Chat con memoria**: Usa `ConversationBufferMemory` para contexto
3. **Personalidades dinámicas**: Diferentes roles (profesor, pirata, poeta)
4. **Multi-turno**: Conversación sobre planificación de viajes

**Conceptos:** Prompts, LLM chaining, Memory management

### 2️⃣ Componentes e Integraciones (`02_componentes_integracion.py`)
**5 ejemplos:**
1. **Web Search**: Búsqueda con DuckDuckGo
2. **HTTP Requests**: Llamadas a APIs externas (JSONPlaceholder, GitHub)
3. **Prompt Templates**: Plantillas con variables dinámicas
4. **Text Processing**: Procesamiento de textos (length, case conversion)
5. **JSON Parsing**: LLM generando JSON válido

**Conceptos:** APIs, Web search, JSON parsing, Prompt composition

### 3️⃣ RAG - Procesamiento de Documentos (`03_rag_document_processing.py`)
**5 ejemplos de RAG completo:**
1. **Text Splitting**: Dividir documentos en chunks (CharacterTextSplitter)
2. **Embeddings**: Crear vectores semánticos con OllamaEmbeddings
3. **Vector Store**: Indexar con FAISS
4. **RAG básico**: Retrieval + Generation
5. **RAG avanzado**: Con relevance scores

**Conceptos:** Embeddings, Vector stores, FAISS, Similarity search, RAG pipeline

### 4️⃣ Patrones Avanzados (`04_patrones_avanzados.py`)
**5 ejemplos de patrones productivos:**
1. **Conditional Routing**: RunnableBranch para detectar tipo de pregunta
2. **Fallback Pattern**: Cadena principal + fallback
3. **Error Handling**: Gestión completa de TimeoutError, ValueError, ConnectionError
4. **Custom Components**: Clase PersonalizadoComponent con procesamiento
5. **Complex Composition**: Pipeline: validación → clasificación → respuesta → formateo

**Conceptos:** RunnableBranch, Fallbacks, Error handling, Custom components

### 5️⃣ Exportación a API (`05_exportacion_api.py`)
**5 ejemplos de producción:**
1. **FastAPI Simple**: Servidor con endpoints /chat y /health
2. **Autenticación**: Token-based auth (expandible a JWT)
3. **Rate Limiting**: Control de requests por usuario
4. **Monitoring**: Métricas de performance (tiempo, tasa de éxito)
5. **Configuración Producción**: Settings para despliegue

**Conceptos:** FastAPI, Authentication, Rate limiting, Monitoring

### 6️⃣ Proyecto Final Integrado (`06_proyecto_final.py`)
**4 asistentes completos:**
1. **Asistente Simple**: Chat con memoria y historial
2. **Asistente Web Search**: Detección inteligente de necesidad de búsqueda
3. **Asistente RAG**: Consultas sobre documentos cargados
4. **Asistente Completo**: Integra todo - validación, clasificación, procesamiento, métricas

**Plus:** Exportación a configuración JSON para despliegue

**Conceptos:** Arquitectura integrada, Validación, Clasificación, Composición

---

## 📖 Contenido de Módulos (Legado)

### Módulo 1: Introducción a Langflow
**Archivo:** `modulo_1/01_hello_langflow.py`

Introduce conceptos básicos:
- **LangflowComponent**: Componentes base
- **InputComponent**: Entrada de usuario
- **ChatOpenAIComponent**: Componente de LLM
- **OutputComponent**: Salida de resultados
- **SimpleFlow**: Orquestación de componentes

**Concepto clave:** Langflow es una plataforma visual para orquestar componentes conectando inputs y outputs.

### Módulo 2: Conceptos Fundamentales
**Archivo:** `modulo_2/01_components.py`

Profundiza en:
- **ComponentLibrary**: Librería disponible de componentes
- **Connection**: Conexiones entre componentes
- **FlowValidator**: Validación de flujos
- **FlowAnalyzer**: Análisis de complejidad

### Módulo 3: Conversaciones y Chat
**Archivo:** `modulo_3/01_conversation.py`

Manejo de conversaciones:
- **Message**: Estructura de mensajes
- **ConversationMemory**: Historial y contexto
- **ChatInterface**: Interfaz de chat mejorada
- Multi-turn interactions con memoria

### Módulo 4: Integraciones y Herramientas
**Archivo:** `modulo_4/01_integrations.py`

Integración con sistemas externos:
- **APIComponent**: Llamadas a APIs REST
- **SearchTool**: Búsqueda en web
- **DatabaseComponent**: Conexión a bases de datos
- **ToolIntegrationFlow**: Coordinar herramientas

### Módulo 5: Casos de Uso Prácticos
**Archivo:** `modulo_5/01_usecases.py`

Chatbot de atención al cliente:
- **CustomerServiceBot**: Sistema completo de soporte
- Intent classification (clasificación de intenciones)
- Knowledge base integration
- Escalación a agentes humanos

### Módulo 6: Exportación y Deployment
**Archivo:** `modulo_6/01_deployment.py`

Exportar flujos en múltiples formatos:
- **FlowExporter**: Exporta como JSON, Python API, Docker
- **DeploymentManager**: Gestiona deployments en cloud
- APIs REST automáticas
- Webhooks y embeddings

### Módulo 7: Componentes Personalizados
**Archivo:** `modulo_7/01_custom_components.py`

Crear componentes propios:
- **CustomComponent**: Clase base para extensión
- **ComponentRegistry**: Registro de componentes
- Ejemplos: TextToUpper, TextLength, SentimentAnalysis

### Módulo 8: Optimización y Performance
**Archivo:** `modulo_8/01_optimization.py`

Estrategias de optimización:
- **RequestCache**: Caching de requests
- **BatchProcessor**: Procesamiento en lotes
- **TokenOptimizer**: Reducción de tokens
- **PerformanceMonitor**: Monitoreo de métricas

### Módulo 9: Monitoreo y Debugging
**Archivo:** `modulo_9/01_monitoring.py`

Observabilidad y debugging:
- **FlowLogger**: Logging detallado de ejecución
- **FlowDebugger**: Herramientas de debugging
- **ExecutionAnalyzer**: Análisis de performance
- Stack traces e inspección de variables

### Módulo 10: Proyecto Final
**Archivo:** `modulo_10/01_final_project.py`

Sistema integral de asistente IA:
- **IntegratedAssistant**: Asistente completo
- 5 fases: Understand → Search → Process → Generate → Integrate
- Base de conocimientos
- Logging y estadísticas

## ✅ Validación y Testing

### Validar Sintaxis (Sin requerimientos especiales)

```bash
# Valida que todos los archivos .py tienen sintaxis correcta
python test_syntax.py
```

**Resultado esperado:**
```
✅ 01_chatbot_simple.py
✅ 02_componentes_integracion.py
✅ 03_rag_document_processing.py
✅ 04_patrones_avanzados.py
✅ 05_exportacion_api.py
✅ 06_proyecto_final.py

✅ TODOS LOS ARCHIVOS SON VÁLIDOS
```

### Ejecutar Ejemplos (Requiere Ollama)

Para ejecutar los ejemplos con funcionalidad completa, necesitas Ollama:

```bash
# 1. Instalar Ollama: https://ollama.ai
# 2. Descargar modelo: ollama pull mistral
# 3. Ejecutar: ollama serve (en otra terminal)
# 4. Ejecutar ejemplos:
python 01_chatbot_simple.py
```

## 📊 Resultados Esperados

**Ejemplos nuevos:**

```
✓ 01_chatbot_simple.py: 4 ejemplos de chat
✓ 02_componentes_integracion.py: 5 ejemplos de integraciones
✓ 03_rag_document_processing.py: 5 ejemplos de RAG
✓ 04_patrones_avanzados.py: 5 ejemplos de patrones
✓ 05_exportacion_api.py: 5 ejemplos de API
✓ 06_proyecto_final.py: 4 asistentes integrados

Tasa de éxito: 100% (sintaxis)
```

**Ejemplos legado:**

```
✓ Módulo 1-10: Componentes, chat, integraciones, deployment, etc.
```

## 🔧 Configuración Personalizada

### Usar Langflow Real

Para integrar con Langflow instalado localmente:

```python
from langflow import Component

class MiComponente(Component):
    inputs = {"text": "string"}
    outputs = {"result": "string"}

    def run(self, text: str) -> str:
        return text.upper()
```

### Conectar a APIs Reales

```python
# Modificar APIComponent para usar credenciales reales
api = APIComponent(
    "OpenWeatherAPI",
    "https://api.openweathermap.org",
    api_key="tu_api_key"
)
```

## 📚 Recursos Adicionales

### Documentación Completa
- **Langflow.adoc**: Documentación detallada (1500+ líneas)
- **Módulos 1-10**: Teoría y código

### Referencias
- [Langflow GitHub](https://github.com/logspace-ai/langflow)
- [Langflow Docs](https://github.com/logspace-ai/langflow/wiki)
- [Langflow Community](https://discord.gg/langflow)

## 🛠️ Troubleshooting Rápido

### Error: "Módulo no encontrado"
```bash
# Asegurar que estás en el directorio correcto
cd /home/rojaldo/cursos/agents/ejemplos/langflow
python modulo_1/01_hello_langflow.py
```

### Error: "Componente no encontrado"
- Verificar que el componente está registrado
- Usar `registry.list_components()` para ver disponibles

### Error: "API no responde"
- Verificar conexión a internet
- Validar API keys si están configuradas
- Aumentar timeout en caso necesario

## 📈 Métricas de Aprendizaje

Después de completar este curso puedes:

✅ Entender plataformas visuales para IA
✅ Crear flujos con componentes
✅ Integrar herramientas y APIs
✅ Construir chatbots funcionales
✅ Exportar flujos como aplicaciones
✅ Optimizar performance
✅ Monitorear ejecuciones
✅ Crear componentes personalizados

## 📝 Notas Importantes

1. **Los ejemplos no requieren instalación de Langflow**: Usan simulaciones en lugar de la plataforma real
2. **Totalmente extensible**: Puedes reemplazar simulaciones con Langflow real
3. **Código limpio**: Incluye best practices y patrones profesionales
4. **Documentado**: Cada ejemplo tiene comentarios explicativos
5. **Escalable**: La arquitectura soporta proyectos complejos

## 🎓 Recomendaciones de Estudio

1. **Semana 1**: Módulos 1-3 (Fundamentos)
2. **Semana 2**: Módulos 4-6 (Integraciones y deployment)
3. **Semana 3**: Módulos 7-9 (Componentes y optimización)
4. **Semana 4**: Módulo 10 (Proyecto capstone)

## 📞 Soporte

Para preguntas o problemas:
1. Revisar la documentación en Langflow.adoc
2. Consultar el módulo de troubleshooting (si aplica)
3. Revisar los logs de ejecución
4. Buscar en la comunidad de Langflow

## 📜 Licencia

Este material educativo es de código abierto y puede ser usado libremente para propósitos de aprendizaje.

---

**Última actualización:** 2024-11-08
**Versión:** 1.0
**Autor:** Curso de Agentes IA
