# Índice de Ejemplos MCP con LangChain y Ollama

Este directorio contiene ejemplos prácticos completos para aprender a implementar el **Model Context Protocol (MCP)** usando **LangChain** y **Ollama** para ejecutar modelos de lenguaje localmente.

## 📁 Estructura de Archivos

### 🔧 Scripts de Configuración

| Archivo | Descripción | Tamaño |
|---------|-------------|--------|
| `00_verificar_setup.py` | Script de verificación de configuración | 7.0K |
| `setup_modelos.sh` | Script para descargar modelos de Ollama | 2.5K |
| `test_ejemplos.sh` | Script para probar todos los ejemplos | 2.9K |
| `requirements.txt` | Dependencias Python necesarias | 490B |

### 📚 Ejemplos Principales (Nuevos - LangChain + Ollama)

| Archivo | Descripción | Tamaño | Nivel |
|---------|-------------|--------|-------|
| `01_servidor_basico_langchain.py` | Servidor MCP básico con herramientas de NLP | 9.7K | Básico |
| `02_cliente_mcp_langchain.py` | Cliente MCP con flujos de trabajo | 9.8K | Intermedio |
| `03_servidor_rag_langchain.py` | Servidor MCP con RAG y embeddings | 16K | Avanzado |

### 📖 Documentación

| Archivo | Descripción | Tamaño |
|---------|-------------|--------|
| `README_LANGCHAIN_OLLAMA.md` | Guía completa de uso de ejemplos LangChain | 9.8K |
| `GUIA_REFERENCIA_RAPIDA.md` | Referencia rápida de MCP | 5.8K |
| `EJERCICIOS_PRACTICOS.md` | Ejercicios prácticos adicionales | 7.7K |
| `INDICE_Y_NAVEGACION.md` | Índice general del curso MCP | 11K |

### 📦 Ejemplos Previos (Referencia)

| Archivo | Descripción | Tamaño |
|---------|-------------|--------|
| `cliente_ejemplo.py` | Cliente MCP de ejemplo básico | 14K |
| `servidor_gestor_archivos.py` | Servidor de gestión de archivos | 17K |

## 🚀 Inicio Rápido

### 1. Verificar Configuración

Ejecuta primero el script de verificación:

```bash
python3 00_verificar_setup.py
```

Este script verificará:
- ✅ Versión de Python (3.8+)
- ✅ Paquetes Python instalados
- ✅ Ollama instalado y corriendo
- ✅ Modelos disponibles

### 2. Instalar Dependencias

Si usas un sistema con entorno Python gestionado (como Arch Linux):

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

Para otros sistemas:

```bash
pip install -r requirements.txt
```

### 3. Configurar Ollama

Si Ollama no está instalado:

```bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh

# macOS
brew install ollama

# Windows
# Descargar desde https://ollama.com/download
```

### 4. Descargar Modelos

Ejecuta el script de setup automático:

```bash
bash setup_modelos.sh
```

O descarga manualmente:

```bash
ollama pull llama3.2          # Modelo principal (~2GB)
ollama pull nomic-embed-text  # Embeddings (~274MB)
```

### 5. Ejecutar Ejemplos

Una vez configurado todo:

```bash
# Ejemplo básico
python3 01_servidor_basico_langchain.py

# Cliente MCP
python3 02_cliente_mcp_langchain.py

# Servidor RAG avanzado
python3 03_servidor_rag_langchain.py
```

O ejecuta todos con el script de prueba:

```bash
bash test_ejemplos.sh
```

## 📖 Progresión de Aprendizaje Recomendada

### Nivel 1: Fundamentos (Día 1)
1. Lee `README_LANGCHAIN_OLLAMA.md`
2. Ejecuta `00_verificar_setup.py`
3. Configura el entorno con `setup_modelos.sh`
4. Estudia y ejecuta `01_servidor_basico_langchain.py`

**Objetivos:**
- Entender qué es MCP
- Conocer las herramientas básicas de NLP
- Ejecutar tu primer servidor MCP

### Nivel 2: Interacción Cliente-Servidor (Día 2)
1. Estudia `02_cliente_mcp_langchain.py`
2. Experimenta con los flujos de trabajo
3. Crea tus propios flujos personalizados

**Objetivos:**
- Conectar clientes a servidores
- Usar flujos de trabajo automatizados
- Entender el ciclo de vida de las conexiones

### Nivel 3: RAG y Embeddings (Día 3-4)
1. Estudia `03_servidor_rag_langchain.py`
2. Crea colecciones de documentos
3. Implementa búsquedas semánticas

**Objetivos:**
- Implementar RAG completo
- Usar embeddings locales
- Gestionar vectorstores

### Nivel 4: Proyectos Reales (Día 5+)
1. Revisa `EJERCICIOS_PRACTICOS.md`
2. Implementa casos de uso específicos
3. Crea tus propias herramientas MCP

## 🎯 Casos de Uso por Ejemplo

### 01_servidor_basico_langchain.py

**Casos de uso:**
- ✅ Generación de contenido
- ✅ Resumen de textos
- ✅ Análisis de sentimientos
- ✅ Sistema de Q&A

**Ideal para:**
- Chatbots básicos
- Procesamiento de feedback
- Generación de reportes
- Asistentes de escritura

### 02_cliente_mcp_langchain.py

**Casos de uso:**
- ✅ Automatización de flujos
- ✅ Orquestación de múltiples herramientas
- ✅ Procesamiento en pipeline
- ✅ Monitoreo y estadísticas

**Ideal para:**
- Aplicaciones cliente
- Integración con sistemas existentes
- Workflows complejos
- Testing de servidores

### 03_servidor_rag_langchain.py

**Casos de uso:**
- ✅ Búsqueda en documentación
- ✅ Asistente de base de conocimientos
- ✅ Q&A sobre documentos
- ✅ Análisis de similitud

**Ideal para:**
- Sistemas de documentación
- Asistentes técnicos
- Bases de conocimiento
- Chatbots con memoria

## 🔧 Troubleshooting

### Error: "Ollama is not running"

```bash
# Inicia Ollama
ollama serve
```

### Error: "Model not found"

```bash
# Descarga el modelo
ollama pull llama3.2
```

### Error: "Module not found"

```bash
# Reinstala dependencias
pip install -r requirements.txt
```

### Error: "externally-managed-environment"

```bash
# Usa entorno virtual
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📚 Recursos Adicionales

### Documentación Oficial
- [LangChain Docs](https://python.langchain.com/)
- [Ollama Docs](https://ollama.com/docs)
- [MCP Specification](https://spec.modelcontextprotocol.io/)

### Guías en este Directorio
- `README_LANGCHAIN_OLLAMA.md` - Guía completa y detallada
- `GUIA_REFERENCIA_RAPIDA.md` - Referencia rápida de comandos
- `EJERCICIOS_PRACTICOS.md` - Ejercicios adicionales

### Comunidad y Soporte
- GitHub Issues para reportar problemas
- Documentación del curso en `/docs/mcp.adoc`

## 💡 Próximos Pasos

Después de completar estos ejemplos:

1. **Personaliza las herramientas** - Agrega tus propias funciones
2. **Integra con APIs** - Conecta con servicios externos
3. **Optimiza el rendimiento** - Implementa caché y batching
4. **Crea aplicaciones** - Construye proyectos reales

## 🤝 Contribuir

Si tienes mejoras o nuevos ejemplos:

1. Sigue la nomenclatura: `0X_nombre_descriptivo.py`
2. Incluye docstrings completos
3. Agrega ejemplos de uso
4. Actualiza este índice

## ✨ Resumen

Este conjunto de ejemplos te proporciona:

- ✅ **3 ejemplos progresivos** de MCP con LangChain y Ollama
- ✅ **Scripts de configuración** automatizados
- ✅ **Documentación completa** y guías paso a paso
- ✅ **Casos de uso reales** listos para implementar
- ✅ **Todo ejecutable localmente** sin dependencias externas

**Total de archivos nuevos:** 8 (4 scripts Python + 3 scripts Bash + 1 requirements)
**Líneas de código:** ~1500+
**Documentación:** 4 archivos MD (~30KB)

¡Comienza con `00_verificar_setup.py` y sigue la progresión recomendada! 🚀
