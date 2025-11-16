# Ejemplos de Bases de Datos Vectoriales y de Grafos

Este directorio contiene ejemplos prácticos del curso de Bases de Datos Vectoriales y de Grafos, enfocados en el uso de **LangChain** y **Ollama** en local.

## 📁 Estructura

```
bbdd/
├── 01_chromadb_basico.py          # ChromaDB básico (sin dependencias externas)
├── 02_chromadb_con_ollama.py      # ChromaDB con embeddings de Ollama
├── 03_grafos_conceptos_basicos.py # Grafos básicos en Python (sin BD)
├── 04_rag_avanzado_chromadb.py    # Sistema RAG completo con ChromaDB
├── neo4j/
│   ├── 01_neo4j_basico.py         # Neo4j básico con Python driver
│   └── 02_neo4j_con_langchain.py  # Neo4j + LangChain + Ollama
├── hibrido/
│   └── 01_busqueda_hibrida.py     # Sistema híbrido (vectores + grafos)
├── requirements.txt                # Dependencias Python
├── test-ejemplos.sh               # Script para ejecutar todos los ejemplos
└── README.md                      # Este archivo
```

## 🚀 Inicio Rápido

### 1. Instalar Dependencias

```bash
# Si puedes usar pip directamente
pip install -r requirements.txt

# Si necesitas un entorno virtual (recomendado en Arch Linux)
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Ejecutar Ejemplos

#### Ejemplos sin servicios externos (funcionan inmediatamente):

```bash
# Grafos básicos (solo Python)
python 03_grafos_conceptos_basicos.py

# ChromaDB básico (sin Ollama)
python 01_chromadb_basico.py
```

#### Ejemplos que requieren Ollama:

```bash
# 1. Instalar y ejecutar Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama serve

# 2. Descargar modelos necesarios
ollama pull mistral
ollama pull nomic-embed-text

# 3. Ejecutar ejemplos
python 02_chromadb_con_ollama.py
python 04_rag_avanzado_chromadb.py
```

#### Ejemplos que requieren Neo4j:

```bash
# 1. Ejecutar Neo4j en Docker
docker run --name neo4j \
  -p 7687:7687 \
  -p 7474:7474 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:latest

# 2. Ejecutar ejemplos
python neo4j/01_neo4j_basico.py
python neo4j/02_neo4j_con_langchain.py

# 3. Acceder a Neo4j Browser
# http://localhost:7474
# Usuario: neo4j, Password: password
```

#### Ejemplos híbridos (requieren Ollama + Neo4j):

```bash
python hibrido/01_busqueda_hibrida.py
```

### 3. Script de Prueba Automatizado

```bash
# Hacer ejecutable
chmod +x test-ejemplos.sh

# Ejecutar todos los ejemplos
./test-ejemplos.sh all

# Solo ejemplos de ChromaDB
./test-ejemplos.sh chromadb

# Solo ejemplos de Neo4j
./test-ejemplos.sh neo4j

# Solo ejemplos híbridos
./test-ejemplos.sh hibrido
```

## 📚 Descripción de los Ejemplos

### ChromaDB

#### `01_chromadb_basico.py`
- **Requisitos**: Ninguno (ChromaDB standalone)
- **Conceptos**:
  - Crear colecciones
  - Agregar documentos
  - Búsqueda básica
  - Operaciones CRUD
  - Filtrado por metadata
- **Duración**: ~30 segundos

#### `02_chromadb_con_ollama.py`
- **Requisitos**: Ollama + nomic-embed-text
- **Conceptos**:
  - Embeddings con Ollama
  - Búsqueda semántica real
  - Scores de similitud
  - Comparación de vectores
- **Duración**: ~2-3 minutos

#### `04_rag_avanzado_chromadb.py`
- **Requisitos**: Ollama + mistral + nomic-embed-text
- **Conceptos**:
  - Sistema RAG completo
  - Text splitting
  - Retrieval y generation
  - Clase RAG reutilizable
  - Mejores prácticas
- **Duración**: ~3-4 minutos

### Grafos

#### `03_grafos_conceptos_basicos.py`
- **Requisitos**: Ninguno (solo Python)
- **Conceptos**:
  - Grafos dirigidos y no dirigidos
  - Grafos ponderados
  - Búsqueda DFS
  - Análisis de centralidad
  - Casos de uso
- **Duración**: ~20 segundos

### Neo4j

#### `neo4j/01_neo4j_basico.py`
- **Requisitos**: Neo4j en Docker
- **Conceptos**:
  - Conexión con Python driver
  - Crear nodos y relaciones
  - Consultas Cypher básicas
  - Agregaciones
  - Operaciones CRUD
- **Duración**: ~1 minuto

#### `neo4j/02_neo4j_con_langchain.py`
- **Requisitos**: Neo4j + Ollama + mistral
- **Conceptos**:
  - Neo4j con LangChain
  - Extracción de entidades con LLM
  - Knowledge Graphs automáticos
  - Consultas en lenguaje natural
  - GraphCypherQAChain
- **Duración**: ~3-5 minutos

### Híbridos

#### `hibrido/01_busqueda_hibrida.py`
- **Requisitos**: ChromaDB + Neo4j + Ollama
- **Conceptos**:
  - Arquitectura híbrida
  - Búsqueda vectorial + grafos
  - RAG híbrido
  - Clase HybridRAG
  - Ventajas del enfoque híbrido
- **Duración**: ~4-6 minutos

## 🔧 Requisitos del Sistema

### Software

- **Python**: 3.10 o superior
- **Docker**: Para Neo4j (opcional)
- **Ollama**: Para embeddings y LLMs locales (opcional)

### Hardware Recomendado

- **RAM**: 8GB mínimo, 16GB recomendado
- **CPU**: 4 cores mínimo
- **Disco**: 10GB libres (para modelos de Ollama)
- **GPU**: Opcional (Ollama funciona sin GPU)

## 📦 Dependencias

```
chromadb>=0.4.0           # Base de datos vectorial
langchain>=0.1.0          # Framework de orquestación
langchain-chroma>=0.1.0   # Integración ChromaDB
langchain-ollama>=0.1.0   # Integración Ollama
langchain-core>=0.1.0     # Core de LangChain
langchain-community>=0.1.0 # Integraciones comunitarias
langchain-experimental>=0.1.0 # Características experimentales
ollama>=0.1.0             # Cliente Python de Ollama
numpy>=1.21.0             # Operaciones numéricas
requests>=2.28.0          # HTTP requests
neo4j>=5.0.0              # Driver de Neo4j
```

## 🎯 Niveles de Dificultad

| Ejemplo | Nivel | Servicios Externos | Tiempo |
|---------|-------|-------------------|--------|
| `03_grafos_conceptos_basicos.py` | ⭐ Básico | Ninguno | 20s |
| `01_chromadb_basico.py` | ⭐ Básico | Ninguno | 30s |
| `02_chromadb_con_ollama.py` | ⭐⭐ Intermedio | Ollama | 2-3m |
| `neo4j/01_neo4j_basico.py` | ⭐⭐ Intermedio | Neo4j | 1m |
| `04_rag_avanzado_chromadb.py` | ⭐⭐⭐ Avanzado | Ollama | 3-4m |
| `neo4j/02_neo4j_con_langchain.py` | ⭐⭐⭐ Avanzado | Neo4j + Ollama | 3-5m |
| `hibrido/01_busqueda_hibrida.py` | ⭐⭐⭐⭐ Experto | Todo | 4-6m |

## 🐛 Resolución de Problemas

### Error: "Collection already exists"

```bash
# Eliminar directorios de ChromaDB
rm -rf chroma_db/ chromadb/ hibrido_chroma/ rag_chromadb/

# Ejecutar nuevamente el ejemplo
python 01_chromadb_basico.py
```

### Error: "Ollama no disponible"

```bash
# Verificar que Ollama está ejecutándose
curl http://localhost:11434/api/tags

# Si no está ejecutándose
ollama serve

# Verificar modelos instalados
ollama list

# Instalar modelos necesarios
ollama pull mistral
ollama pull nomic-embed-text
```

### Error: "Neo4j no disponible"

```bash
# Verificar contenedor Docker
docker ps | grep neo4j

# Si no está ejecutándose
docker start neo4j

# O crear nuevo contenedor
docker run --name neo4j \
  -p 7687:7687 -p 7474:7474 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:latest
```

### Error: "Module not found"

```bash
# Verificar instalación de dependencias
python -c "import chromadb, langchain, neo4j"

# Si falla, reinstalar
pip install -r requirements.txt
```

## 📖 Recursos Adicionales

- **ChromaDB**: https://docs.trychroma.com/
- **LangChain**: https://python.langchain.com/
- **Ollama**: https://ollama.com/
- **Neo4j**: https://neo4j.com/developer/
- **Documento del curso**: `../docs/bases_datos_vectoriales_grafos.adoc`

## 💡 Consejos

1. **Empieza por los ejemplos básicos** (sin servicios externos)
2. **Instala servicios gradualmente** (primero Ollama, luego Neo4j)
3. **Lee los comentarios** en cada ejemplo
4. **Experimenta modificando** los parámetros
5. **Usa el Neo4j Browser** para visualizar grafos (http://localhost:7474)
6. **Revisa los logs** si algo falla

## 🤝 Contribuir

Si encuentras errores o mejoras:

1. Reporta issues
2. Propón mejoras en los ejemplos
3. Comparte tus propios ejemplos

## 📝 Licencia

Ejemplos educativos del Curso de Agentes IA.

---

**¿Dudas?** Revisa el documento completo del curso en `docs/bases_datos_vectoriales_grafos.adoc`
