# 📑 Índice Completo - Langflow Course

## 🎓 Guías de Inicio

| Documento | Propósito | Audiencia |
|-----------|----------|-----------|
| [QUICKSTART.md](QUICKSTART.md) | Comenzar en 5 minutos | Todos |
| [README.md](README.md) | Documentación completa | Aprendices |
| [SUMMARY.md](SUMMARY.md) | Resumen de completitud | Referencia |
| [INDEX.md](INDEX.md) | Este archivo | Navegación |

---

## 💻 Ejemplos de Código

### Módulo 1: Chatbot Simple
**Archivo:** [`01_chatbot_simple.py`](01_chatbot_simple.py)
- **Líneas:** 207
- **Ejemplos:** 4
- **Tiempo:** 15-20 minutos

**Contenido:**
1. Chat simple sin memoria
2. Chat con ConversationBufferMemory
3. Personalidades dinámicas (profesor, pirata, poeta)
4. Conversación multi-turno sobre viajes

**Conceptos:**
- ChatPromptTemplate
- ConversationBufferMemory
- LLM chaining
- Historial de sesión

**Usa:** `Ollama`, `langchain-core`

---

### Módulo 2: Componentes e Integraciones
**Archivo:** [`02_componentes_integracion.py`](02_componentes_integracion.py)
- **Líneas:** 247
- **Ejemplos:** 5
- **Tiempo:** 20-25 minutos

**Contenido:**
1. Web Search (DuckDuckGoSearchRun)
2. HTTP Requests a APIs externas
3. Prompt Templates con variables
4. Text Processing (length, case, reverse)
5. JSON Parsing con LLM

**Conceptos:**
- DuckDuckGoSearchRun
- requests library
- PromptTemplate
- JSON parsing

**Usa:** `Ollama`, `requests`, `langchain-community`

---

### Módulo 3: RAG Document Processing
**Archivo:** [`03_rag_document_processing.py`](03_rag_document_processing.py)
- **Líneas:** 294
- **Ejemplos:** 5
- **Tiempo:** 25-30 minutos

**Contenido:**
1. Text Splitting (CharacterTextSplitter)
2. Embeddings (OllamaEmbeddings)
3. Vector Store (FAISS)
4. RAG básico (retrieval + generation)
5. RAG avanzado (relevance scores)

**Conceptos:**
- CharacterTextSplitter
- OllamaEmbeddings
- FAISS vector store
- Similarity search
- RAG pipeline

**Usa:** `Ollama`, `langchain-community`, `FAISS`

---

### Módulo 4: Patrones Avanzados
**Archivo:** [`04_patrones_avanzados.py`](04_patrones_avanzados.py)
- **Líneas:** 296
- **Ejemplos:** 5
- **Tiempo:** 25-30 minutos

**Contenido:**
1. Conditional Routing (RunnableBranch)
2. Fallback Pattern
3. Error Handling (completo)
4. Custom Components
5. Complex Composition Pipeline

**Conceptos:**
- RunnableBranch
- Fallbacks
- Exception handling
- Custom components
- Pipeline composition

**Usa:** `Ollama`, `langchain-core`

---

### Módulo 5: Exportación a API
**Archivo:** [`05_exportacion_api.py`](05_exportacion_api.py)
- **Líneas:** 359
- **Ejemplos:** 5
- **Tiempo:** 30-35 minutos

**Contenido:**
1. FastAPI Server simple
2. Autenticación por tokens
3. Rate Limiting
4. Monitoring y Métricas
5. Configuración de Producción

**Conceptos:**
- FastAPI
- Pydantic BaseModel
- Authentication
- Rate limiting
- Metrics monitoring

**Usa:** `Ollama`, `fastapi`, `pydantic`

---

### Módulo 6: Proyecto Final Integrado
**Archivo:** [`06_proyecto_final.py`](06_proyecto_final.py)
- **Líneas:** 456
- **Ejemplos:** 4 asistentes + export
- **Tiempo:** 35-40 minutos

**Contenido:**
1. Asistente Simple (chat + memoria)
2. Asistente Web Search (detección inteligente)
3. Asistente RAG (consultas sobre documentos)
4. Asistente Completo (integración total)
5. Exportación a JSON

**Conceptos:**
- Arquitectura integrada
- Validación de entrada
- Clasificación de consultas
- Métricas de rendimiento
- JSON export

**Usa:** `Ollama`, `langchain-community`, `FAISS`

---

## 🔧 Herramientas

### Test & Validation
**Archivo:** [`test_syntax.py`](test_syntax.py)
- **Función:** Validar sintaxis de todos los ejemplos
- **Requisitos:** Python 3.8+ (nada más)
- **Uso:** `python test_syntax.py`
- **Resultado:** Reporte de validación

**Verifica:**
- ✅ Sintaxis Python válida
- ✅ Imports necesarios
- ✅ Dependencias disponibles

---

### Script Maestro
**Archivo:** [`run_all_examples.py`](run_all_examples.py)
- **Función:** Ejecutar todos los módulos
- **Requisitos:** Ollama + dependencias
- **Uso:** `python run_all_examples.py`
- **Genera:** `execution_results.json`

---

## 📚 Documentación Teórica

### Documentación Principal
**Ubicación:** `../../docs/langflow.adoc`
- **Líneas:** 1,870
- **Módulos:** 11 (Introducción a Mejores Prácticas)
- **Formato:** AsciiDoc

**Contenido:**
- Introducción a Langflow
- Conceptos fundamentales
- Conversaciones y memoria
- Integraciones
- Casos de uso
- Export y deployment
- Componentes personalizados
- Optimización
- Monitoreo
- Proyecto final
- Mejores prácticas

---

## 🗺️ Ruta de Aprendizaje Recomendada

### Principiante (6-9 horas)

**Día 1:**
1. Lee: [QUICKSTART.md](QUICKSTART.md)
2. Ejecuta: `python test_syntax.py`
3. Ejecuta: `01_chatbot_simple.py`
4. Ejecuta: `02_componentes_integracion.py`

**Día 2:**
1. Ejecuta: `03_rag_document_processing.py`
2. Lee: Secciones RAG en `docs/langflow.adoc`
3. Ejecuta: `04_patrones_avanzados.py`

**Día 3:**
1. Ejecuta: `05_exportacion_api.py`
2. Ejecuta: `06_proyecto_final.py`
3. Lee: [SUMMARY.md](SUMMARY.md)
4. Experimenta: Modifica ejemplos

---

## 📊 Mapa de Conceptos

```
Langflow Course
├── Fundamentos
│   ├── Prompts (01)
│   ├── Memoria (01)
│   └── LLM Chaining (01)
├── Integraciones
│   ├── Web Search (02)
│   ├── HTTP APIs (02)
│   └── JSON Parsing (02)
├── Procesamiento Avanzado
│   ├── Embeddings (03)
│   ├── Vector Stores (03)
│   └── RAG (03)
├── Patrones Productivos
│   ├── Routing (04)
│   ├── Fallbacks (04)
│   └── Error Handling (04)
├── Deployment
│   ├── FastAPI (05)
│   ├── Auth (05)
│   └── Monitoring (05)
└── Integración Total
    └── Asistentes Completos (06)
```

---

## 🎯 Objetivos de Aprendizaje

Después de completar este curso, serás capaz de:

### Básico
- ✅ Crear chatbots con memoria
- ✅ Usar prompts dinámicos
- ✅ Manejar conversaciones multi-turno

### Intermedio
- ✅ Integrar APIs externas
- ✅ Procesar documentos con RAG
- ✅ Implementar patrones avanzados

### Avanzado
- ✅ Exportar a APIs REST
- ✅ Implementar autenticación
- ✅ Monitorear aplicaciones
- ✅ Crear componentes personalizados

### Profesional
- ✅ Arquitectura de sistemas IA
- ✅ Patrones de producción
- ✅ Optimización y escalado

---

## 🔍 Búsqueda Rápida

### Por Concepto
- **Chat:** `01_chatbot_simple.py`
- **Memoria:** `01_chatbot_simple.py` (Ejemplo 2)
- **Web Search:** `02_componentes_integracion.py` (Ejemplo 1)
- **APIs:** `02_componentes_integracion.py` (Ejemplo 2)
- **Embeddings:** `03_rag_document_processing.py` (Ejemplo 2)
- **RAG:** `03_rag_document_processing.py` (Ejemplos 3-5)
- **Routing:** `04_patrones_avanzados.py` (Ejemplo 1)
- **Error Handling:** `04_patrones_avanzados.py` (Ejemplo 3)
- **FastAPI:** `05_exportacion_api.py` (Ejemplo 1)
- **Monitoreo:** `05_exportacion_api.py` (Ejemplos 3-4)

### Por Tecnología
- **Ollama:** Todos los ejemplos
- **LangChain:** Todos los ejemplos
- **FAISS:** `03_rag_document_processing.py`
- **FastAPI:** `05_exportacion_api.py`
- **DuckDuckGo:** `02_componentes_integracion.py`, `06_proyecto_final.py`

---

## 📈 Estadísticas

| Métrica | Valor |
|---------|-------|
| Total de archivos | 11 (6 ejemplos + 2 herramientas + 3 docs) |
| Líneas de código | 2,496 |
| Ejemplos prácticos | 28 |
| Conceptos cubiertos | 30+ |
| Validación sintaxis | 100% ✅ |
| Tiempo estimado | 8-12 horas |
| Dificultad | Progresivo: Básico → Avanzado |

---

## ✅ Validación

Todas los archivos han sido validados:
- ✅ Sintaxis Python válida
- ✅ Imports correctos
- ✅ Patrones profesionales
- ✅ Documentación completa
- ✅ Ejemplos funcionales

**Ejecuta:** `python test_syntax.py` para verificar

---

## 🚀 Comenzar Ahora

### Opción 1: Rápido (5 minutos)
```bash
python test_syntax.py
```

### Opción 2: Aprender (primer ejemplo)
```bash
ollama serve          # Terminal 1
python 01_chatbot_simple.py  # Terminal 2
```

### Opción 3: Leer primero
```bash
cat QUICKSTART.md
```

---

## 📖 Referencias Cruzadas

### Documentos Relacionados
- `../../docs/langflow.adoc` - Teoría completa
- `../../docs/langchain.adoc` - Fundamentos (LangChain)
- `../../docs/agentes.adoc` - Agentes IA avanzados

### Ejemplos Relacionados
- `../../ejemplos/langchain/` - Ejemplos de LangChain
- `../../ejemplos/agents/` - Ejemplos de agentes

---

## 🆘 Soporte

**¿Dónde encontrar ayuda?**
1. [QUICKSTART.md](QUICKSTART.md) - Problemas comunes
2. [README.md](README.md) - Troubleshooting section
3. [SUMMARY.md](SUMMARY.md) - Requisitos detallados
4. Código con comentarios en cada archivo

---

## 📝 Nota Legal

Este material educativo es de código abierto y puede ser usado libremente para propósitos de aprendizaje.

---

**Última actualización:** 2024-11-14
**Versión:** 1.0
**Estado:** ✅ Completado

---

## 🎓 Siguiente Nivel

Después de completar este curso, considera:
1. Explorar `../../docs/langflow.adoc` en profundidad
2. Modificar ejemplos para tus casos de uso
3. Integrar con APIs reales (OpenAI, Anthropic, etc.)
4. Explorar `../../ejemplos/agents/` para sistemas más complejos
5. Crear tu propio proyecto usando patrones aprendidos

---

**¡Felicidades por tu viaje de aprendizaje!** 🚀
