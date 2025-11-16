# Índice de Contenidos - Módulo Memoria y Contexto

Índice completo de ejemplos y recursos educativos sobre memoria y contexto en agentes de IA.

---

## 📁 Estructura de Archivos

```
ejemplos/memoria/
├── 01_tipos_memoria.py            # 5 tipos de memoria (neurobiológicos)
├── 02_gestion_estado.py           # Estado + Event Sourcing + Persistencia
├── 03_buffer_contexto.py          # Buffer de contexto + Límites LLMs
├── 04_embeddings_busqueda.py      # Embeddings + Búsqueda Semántica
├── 05_rag_retrieval.py            # RAG (Retrieval-Augmented Generation)
├── 06_memoria_conversacional.py   # Conversación + NER + Privacidad
├── 07_memoria_jerarquica.py       # Arquitectura Jerárquica + Consolidación
├── README.md                        # Guía principal (100+ líneas)
└── INDICE_CONTENIDOS.md           # Este archivo
```

**Total**: 7 ejemplos funcionales + 156 KB de código educativo

---

## 🎓 Correlación con Temario

### Módulo 1: Tipos de Memoria en Agentes
**Archivo**: `01_tipos_memoria.py`

Implementa:
- ✓ Memoria sensorial (milisegundos, gran capacidad)
- ✓ Memoria de trabajo (4-7 items, limitada)
- ✓ Memoria episódica (eventos cronológicos)
- ✓ Memoria semántica (conocimiento abstracto)
- ✓ Memoria procedural (habilidades)

Clases principales:
- `MemoriaSensorial`: Buffer con expiración temporal
- `MemoriaTrabajoLimitada`: Capacidad limitada + envejecimiento
- `MemoriaEpisodica`: Timeline de eventos
- `MemoriaSemantica`: Grafo de conocimiento (hechos + relaciones)
- `MemoriaProcedural`: Habilidades con mejora

**Tiempo aprendizaje**: ~30 minutos
**Código**: ~400 líneas
**Conceptos**: 5 tipos neurobiológicos de memoria

---

### Módulo 2: Gestión de Estado en Agentes
**Archivo**: `02_gestion_estado.py`

Implementa:
- ✓ Representación de estado (identidad, posición, recursos, objetivos, creencias)
- ✓ Estado local vs compartido
- ✓ Persistencia y recuperación
- ✓ Serialización a JSON
- ✓ Event sourcing (registro inmutable)
- ✓ Versionado de estado

Clases principales:
- `Identidad`: ID, nombre, tipo, versión
- `EstadoAgenteLLM`: Estado completo multicomponente
- `Evento`: Para event sourcing
- `PersistenciaEstado`: Guardado/carga de snapshots

**Tiempo aprendizaje**: ~30 minutos
**Código**: ~450 líneas
**Conceptos**: State management, event sourcing, persistencia

---

### Módulo 3: Memoria a Corto Plazo y Contexto
**Archivo**: `03_buffer_contexto.py`

Implementa:
- ✓ Buffer de contexto (ventana móvil)
- ✓ Límites de contexto en LLMs
- ✓ Selección de información relevante
- ✓ 4 estrategias de eliminación (FIFO, LRU, importancia, relevancia)
- ✓ Compresión de contexto

Clases principales:
- `BufferContexto`: Buffer circular con límite de tokens
- `ItemContexto`: Item con importancia, accesos, envejecimiento
- `CompresorContexto`: Resumen y compresión
- Enums: `EstrategiaEliminacion`

**Tiempo aprendizaje**: ~25 minutos
**Código**: ~350 líneas
**Conceptos**: Context windows, token limits, compression strategies

---

### Módulo 4: Memoria a Largo Plazo
**Archivos**: `04_embeddings_busqueda.py`, `05_rag_retrieval.py`

#### 04 - Embeddings y Búsqueda Semántica
Implementa:
- ✓ Generación de embeddings (TF-IDF simplificado)
- ✓ Búsqueda vectorial (similitud coseno)
- ✓ Búsqueda por palabras clave (Jaccard)
- ✓ Búsqueda híbrida (combinada)
- ✓ Indexación de documentos

Clases principales:
- `GeneradorEmbeddings`: Conversión texto → vectores
- `IndiceVectorial`: Índice de búsqueda
- `BuscadorHibrido`: Combina keyword + semantic
- `CalculadorSimilitud`: Coseno, Jaccard, Euclidiana

**Tiempo aprendizaje**: ~40 minutos
**Código**: ~380 líneas
**Conceptos**: Embeddings, similarity search, hybrid search

#### 05 - RAG (Retrieval-Augmented Generation)
Implementa:
- ✓ Pipeline RAG completo (5 pasos)
- ✓ Base de conocimiento
- ✓ Recuperación de documentos
- ✓ Construcción de contexto
- ✓ Enriquecimiento de prompts
- ✓ Generación de respuestas

Clases principales:
- `BaseConocimiento`: Almacén de documentos
- `PipelineRAG`: Orquestación del flujo
- `DocumentoFuente`: Con metadata y tipo de fuente

**Tiempo aprendizaje**: ~35 minutos
**Código**: ~420 líneas
**Conceptos**: RAG pipeline, information retrieval, prompt engineering

---

### Módulo 5: Recuperación de Información Relevante
**Archivo**: `04_embeddings_busqueda.py` (sección búsqueda híbrida)

Implementa:
- ✓ Algoritmos de búsqueda (BM25 simulado, TF-IDF, vectorial)
- ✓ Ranking de relevancia
- ✓ Filtrado y pre-filtrado
- ✓ Consultas multi-criterio
- ✓ Métricas de similitud

---

### Módulo 6: Memoria en Agentes Conversacionales
**Archivo**: `06_memoria_conversacional.py`

Implementa:
- ✓ Historial de conversación
- ✓ Seguimiento de entidades (NER básica)
- ✓ Resolución de referencias anafóricas
- ✓ Personalización basada en memoria
- ✓ Cumplimiento de privacidad (GDPR)
- ✓ Filtrado de datos sensibles

Clases principales:
- `HistorialConversacion`: Gestión de turnos
- `SeguimientoEntidades`: NER y coreference resolution
- `Mensaje`: Con entidades y referencias resueltas
- Tipos: Email, teléfono, productos, fechas

**Tiempo aprendizaje**: ~30 minutos
**Código**: ~400 líneas
**Conceptos**: Conversational AI, NER, anaphora resolution, privacy

---

### Módulo 7: Arquitecturas de Memoria Avanzadas
**Archivo**: `07_memoria_jerarquica.py`

Implementa:
- ✓ Memoria jerárquica en 3 niveles
- ✓ Consolidación de memoria (episódico → táctico → estratégico)
- ✓ Olvido adaptativo
- ✓ Compresión automática
- ✓ Interferencia y recuperación
- ✓ Event-driven consolidation

Clases principales:
- `MemoriaJerarquica`: Gestor de 3 niveles
- `RegistroEpisodico`: Detalles específicos
- `PatronTactico`: Patrones frecuentes
- `ReglaBstracia`: Reglas generalizadas

**Tiempo aprendizaje**: ~40 minutos
**Código**: ~420 líneas
**Conceptos**: Hierarchical memory, consolidation, adaptive forgetting

---

## 🚀 Guía de Ejecución Recomendada

### Para Principiantes (Orden sugerido)

1. **Día 1**: Ejecutar `01_tipos_memoria.py`
   - Comprender fundamentos biológicos
   - Ejecutar: `python 01_tipos_memoria.py`
   - Tiempo: 20 minutos

2. **Día 2**: Ejecutar `02_gestion_estado.py`
   - Entender persistencia de estado
   - Ejecutar: `python 02_gestion_estado.py`
   - Tiempo: 25 minutos

3. **Día 3**: Ejecutar `03_buffer_contexto.py`
   - Problema práctico de límites
   - Ejecutar: `python 03_buffer_contexto.py`
   - Tiempo: 20 minutos

4. **Día 4**: Ejecutar `04_embeddings_busqueda.py`
   - Fundamentos de búsqueda semántica
   - Ejecutar: `python 04_embeddings_busqueda.py`
   - Tiempo: 25 minutos

5. **Día 5**: Ejecutar `05_rag_retrieval.py`
   - Aplicación práctica RAG
   - Ejecutar: `python 05_rag_retrieval.py`
   - Tiempo: 25 minutos

6. **Día 6**: Ejecutar `06_memoria_conversacional.py`
   - Conversaciones coherentes
   - Ejecutar: `python 06_memoria_conversacional.py`
   - Tiempo: 20 minutos

7. **Día 7**: Ejecutar `07_memoria_jerarquica.py`
   - Arquitectura avanzada
   - Ejecutar: `python 07_memoria_jerarquica.py`
   - Tiempo: 25 minutos

**Total**: ~2 horas de ejecución + comprensión teórica

### Para Avanzados

Ejecutar en paralelo o modificar según necesidad:

```bash
# Crear agente que combine todos
python -c "
# Importar todas las clases
from 01_tipos_memoria import *
from 02_gestion_estado import *
# ... etc
# Crear agente complejo
"
```

---

## 📊 Estadísticas de Código

| Archivo | Líneas | Clases | Funciones | Complejidad |
|---------|--------|--------|-----------|-------------|
| 01_tipos_memoria.py | 410 | 5 | 35+ | ⭐⭐ |
| 02_gestion_estado.py | 450 | 10 | 40+ | ⭐⭐ |
| 03_buffer_contexto.py | 350 | 3 | 25+ | ⭐⭐ |
| 04_embeddings_busqueda.py | 380 | 4 | 30+ | ⭐⭐⭐ |
| 05_rag_retrieval.py | 420 | 4 | 28+ | ⭐⭐⭐ |
| 06_memoria_conversacional.py | 400 | 3 | 30+ | ⭐⭐ |
| 07_memoria_jerarquica.py | 420 | 4 | 35+ | ⭐⭐⭐ |
| **TOTAL** | **2,830** | **33** | **223+** | - |

---

## 🔧 Configuración Técnica

### Dependencias Mínimas
```bash
pip install pydantic  # Para dataclasses
```

### Dependencias Opcionales (para integración)
```bash
pip install langchain ollama sentence-transformers numpy scikit-learn
```

### Requisitos de Sistema
- Python 3.8+
- 50 MB de espacio en disco
- Sin dependencias externas para ejemplos 1-7

---

## 💻 Uso en Producción

Cada ejemplo es adaptable a producción:

### Reemplazar componentes:

1. **Embeddings**: GeneradorEmbeddings → SentenceTransformer
2. **Búsqueda**: IndiceVectorial → Pinecone/Weaviate/Chroma
3. **LLM**: Respuesta simulada → Ollama/OpenAI/Anthropic
4. **Storage**: JSON → PostgreSQL/MongoDB

Ejemplo de integración:
```python
# Reemplazar
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

# En GeneradorEmbeddings
def generar_embedding(self, texto):
    return model.encode(texto).tolist()
```

---

## 📚 Recursos de Referencia

### Conceptos Clave por Archivo

**01_tipos_memoria.py**:
- Inspiration from neuroscience (Baddeley, Atkinson-Shiffrin)
- Working memory limitation (Magic number 7±2)
- Episodic vs semantic memory distinction

**02_gestion_estado.py**:
- Event sourcing pattern
- CQRS (Command Query Responsibility Segregation)
- State machines and transitions

**03_buffer_contexto.py**:
- Sliding window algorithms
- LRU cache policies
- Context compression

**04_embeddings_busqueda.py**:
- TF-IDF (Term Frequency-Inverse Document Frequency)
- Vector similarity metrics
- Hybrid search combining signals

**05_rag_retrieval.py**:
- Information Retrieval (IR) basics
- Prompt engineering
- Knowledge augmentation

**06_memoria_conversacional.py**:
- Coreference resolution (anaphora)
- Named Entity Recognition (NER)
- Privacy-preserving techniques (GDPR)

**07_memoria_jerarquica.py**:
- Levels of abstraction
- Consolidation mechanisms
- Adaptive forgetting (importance-weighted)

---

## 🎯 Casos de Uso por Archivo

### 01 - Tipos de Memoria
**Usar para**:
- Entender arquitectura cognitiva
- Diseñar sistemas multi-escala
- Educación

**Casos reales**:
- Sistema de sensor → procesamiento → respuesta
- Web scraping → índice → queries
- Chat → context → generation

### 02 - Gestión de Estado
**Usar para**:
- Persistencia de agentes
- Auditoría y cumplimiento
- Recuperación de fallos

**Casos reales**:
- Agentes de trading
- Bots conversacionales con memoria
- Sistemas de recomendación stateful

### 03 - Buffer de Contexto
**Usar para**:
- Aplicaciones con límites de contexto
- Gestión de memoria en embeddings
- Compresión de información

**Casos reales**:
- ChatGPT-like applications
- Long document processing
- Real-time monitoring systems

### 04 - Embeddings y Búsqueda
**Usar para**:
- Semantic search
- Document similarity
- Recommendation systems

**Casos reales**:
- E-commerce search
- Document repositories
- Content recommendation

### 05 - RAG
**Usar para**:
- Reducir alucinaciones
- Domain-specific QA
- Knowledge base integration

**Casos reales**:
- Customer support bots
- Technical documentation systems
- Internal knowledge bases

### 06 - Memoria Conversacional
**Usar para**:
- Multi-turn dialogues
- Personalized responses
- Privacy-compliant systems

**Casos reales**:
- Virtual assistants
- Chatbots
- Customer service systems

### 07 - Memoria Jerárquica
**Usar para**:
- Escalabilidad
- Pattern recognition
- Long-term learning

**Casos reales**:
- Learning systems
- Complex agent architectures
- Knowledge consolidation

---

## ✅ Checklist Completo de Aprendizaje

### Conceptual (Teoría)
- [ ] Entiendo 5 tipos de memoria humana
- [ ] Sé diferenciar episódico vs semántico
- [ ] Conozco limitaciones de transformers (O(n²))
- [ ] Entiendo RAG y por qué reduce alucinaciones
- [ ] Sé qué es coreference resolution

### Práctico (Código)
- [ ] Ejecuté todos los 7 ejemplos
- [ ] Modifiqué parámetros en cada ejemplo
- [ ] Entiendo cada clase principal
- [ ] Puedo explicar flujos de datos
- [ ] Combino ejemplos en código personalizado

### Aplicación (Producción)
- [ ] Adapté ejemplos a mi caso de uso
- [ ] Integré con Ollama/LangChain
- [ ] Consideré privacidad (GDPR)
- [ ] Optimicé para rendimiento
- [ ] Documenté mis cambios

---

## 📞 Preguntas Frecuentes

**P: ¿Cuál ejemplo debo aprender primero?**
R: Comienza con `01_tipos_memoria.py` para fundamentos

**P: ¿Puedo combinar múltiples ejemplos?**
R: Sí, la arquitectura es modular. Ver ejemplo 7 como referencia

**P: ¿Cómo integro con mi modelo LLM?**
R: Reemplaza la función `_generar_respuesta()` en ejemplo 5

**P: ¿Son estos ejemplos production-ready?**
R: Son educativos, pero estructurados para facilitar adaptación

**P: ¿Qué modelo de Ollama recomiendan?**
R: Comienza con `mistral` (rápido, buena relación) o `neural-chat` (optimizado)

---

## 📖 Referencias Bibliográficas

Consulta el archivo `02-memoria-contexto.adoc` (líneas 511-532) para:
- Libros recomendados (Russell & Norvig, Goodfellow et al., Baddeley)
- Papers académicos (Attention is All You Need, RAG papers, Memory Networks)
- Librerías específicas (sentence-transformers, pinecone, langchain)

---

## 🏆 Objetivos de Aprendizaje (Alcanzados)

Al completar estos 7 ejemplos, habrás alcanzado todos los objetivos de aprendizaje del módulo:

✅ Módulo 1: Entender taxonomía de memoria y distinguir tipos
✅ Módulo 2: Representar estado de agente y persistirlo
✅ Módulo 3: Diseñar buffers de contexto y manejar límites
✅ Módulo 4: Almacenar y recuperar información a largo plazo
✅ Módulo 5: Implementar algoritmos de ranking y búsqueda
✅ Módulo 6: Mantener coherencia conversacional
✅ Módulo 7: Diseñar arquitecturas jerárquicas

---

**Documento actualizado**: Noviembre 2024
**Versión**: 1.0
**Autores**: Ejemplos educativos del Curso de Agentes de IA
