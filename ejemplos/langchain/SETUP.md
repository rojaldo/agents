# Guía de Configuración e Instalación

## Requisitos del Sistema

- **Python**: 3.10 o superior
- **Ollama**: Última versión
- **RAM**: Mínimo 4GB (recomendado 8GB)
- **Espacio en disco**: Mínimo 10GB para modelos

## 1. Instalar Ollama

### Windows/macOS
Descarga desde https://ollama.ai e instala el ejecutable.

### Linux (Arch)
```bash
sudo pacman -S ollama
```

### Linux (otras distribuciones)
```bash
curl https://ollama.ai/install.sh | sh
```

## 2. Descargar Modelos

Abre una terminal y ejecuta:

```bash
# Modelo recomendado (4.1GB, buena relación velocidad/calidad)
ollama pull mistral

# Alternativas más rápidas
ollama pull neural-chat      # 3.8GB, muy rápido
ollama pull openchat         # 3.5GB, ideal para producción

# Listar modelos disponibles
ollama list
```

## 3. Iniciar Ollama

```bash
# En macOS y Windows, la aplicación gráfica lo inicia automáticamente

# En Linux (en una terminal dedicada):
ollama serve

# Ollama estará disponible en http://localhost:11434
```

## 4. Instalar Dependencias de Python

```bash
# Opción 1: Con pip directamente (requiere permisos)
pip install langchain langchain-community langchain-core pydantic --break-system-packages

# Opción 2: Con entorno virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install langchain langchain-community langchain-core pydantic
```

## 5. Verificar la Instalación

```bash
# Verificar dependencias
python test_imports.py

# Verificar sintaxis de ejemplos
python test_syntax.py

# Ejecutar un ejemplo simple
python 01_basic_llm.py
```

## Solución de Problemas

### "Error: ModuleNotFoundError"
```bash
# Asegúrate de que las dependencias están instaladas
python test_imports.py

# Si faltan, instala:
pip install langchain langchain-community langchain-core pydantic --break-system-packages
```

### "Error: No puedo conectar a http://localhost:11434"
```bash
# Verifica que Ollama está ejecutándose
curl http://localhost:11434/api/tags

# Si no funciona, inicia Ollama en otra terminal
ollama serve
```

### "La respuesta es muy lenta"
- Usa un modelo más pequeño: `ollama pull neural-chat`
- Asegúrate de tener suficiente RAM disponible
- Los primeros ejemplos son lentos porque cargan el modelo por primera vez

### "El modelo no existe"
```bash
# Descarga el modelo
ollama pull mistral

# O elige otro disponible
ollama pull neural-chat
ollama pull llama2
ollama pull openchat
```

## Comando Rápido para Empezar

```bash
# 1. En terminal 1, inicia Ollama
ollama serve

# 2. En terminal 2, descarga el modelo
ollama pull mistral

# 3. En terminal 3, ejecuta un ejemplo
cd /home/rojaldo/cursos/agents/ejemplos/langchain
python 01_basic_llm.py
```

## Variables de Entorno (Opcional)

Crea un archivo `.env` en el directorio de ejemplos:

```env
# Configuración de Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# Otros modelos disponibles
# OLLAMA_MODEL=neural-chat
# OLLAMA_MODEL=llama2
# OLLAMA_MODEL=openchat
```

## Estructura Recomendada para Desarrollo

```
mi_proyecto_langchain/
├── venv/                    # Entorno virtual (opcional)
├── ejemplos/
│   └── langchain/          # Este directorio
├── datos/
│   └── documentos/         # Tus documentos para RAG
└── main.py                 # Tu aplicación
```

## Próximos Pasos

1. ✅ Instala Ollama y descarga un modelo
2. ✅ Instala las dependencias de Python
3. 🚀 Ejecuta los ejemplos en orden:
   - `python 01_basic_llm.py`
   - `python 02_chains_basics.py`
   - `python 03_memory.py`
   - `python 04_agents.py`
   - `python 05_embeddings_vectorstore.py`
   - `python 06_rag_system.py`

## Recursos Útiles

- [Documentación de LangChain](https://docs.langchain.com)
- [Documentación de Ollama](https://github.com/jmorganca/ollama)
- [Temario completo](../../docs/langchain.adoc)
