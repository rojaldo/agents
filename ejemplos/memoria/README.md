# Ejemplos Didácticos: Memoria y Contexto en Agentes de IA

Sistema completo de ejemplos funcionales sobre memoria y contexto en agentes, basados en LangChain + Ollama ejecutable localmente.

## 📚 Contenidos

Este directorio contiene 7 ejemplos progresivos que cubren el temario del módulo `02-memoria-contexto.adoc`:

### 1. **01_tipos_memoria.py** - Tipos de Memoria en Agentes
**Conceptos**: Inspiración neurobiológica, taxonomía de memoria

Implementa los 5 tipos principales de memoria humana aplicados a agentes:

- **Memoria Sensorial**: Buffer muy breve (milisegundos), gran capacidad
- **Memoria de Trabajo**: Limitada (4-7 items), consciente, actualmente procesada
- **Memoria Episódica**: Eventos ordenados cronológicamente con contexto
- **Memoria Semántica**: Conocimiento abstracto descontextualizado
- **Memoria Procedural**: Habilidades que mejoran con la práctica

**Detalles técnicos**:
- Clase `MemoriaSensorial`: Simula buffer con expiración temporal
- Clase `MemoriaTrabajoLimitada`: Implementa limitación de capacidad y envejecimiento
- Clase `MemoriaEpisodica`: Timeline de eventos con recuperación temporal
- Clase `MemoriaSemantica`: Grafo de conocimiento simple (hechos + relaciones)
- Clase `MemoriaProcedural`: Registro de habilidades con mejora de tasa de éxito

```bash
python 01_tipos_memoria.py
```

**Salida esperada**: Demostración de todos los 5 tipos funcionando simultáneamente

---

### 2. **02_gestion_estado.py** - Gestión de Estado en Agentes
**Conceptos**: Identidad, posición, recursos, objetivos, creencias, event sourcing

Demuestra cómo un agente mantiene y persiste su estado completo:

- **Identidad**: ID, nombre, tipo de agente, versión
- **Posición**: Ubicación (x, y, z) en el ambiente
- **Recursos**: Items que posee (CPU, memoria, energía)
- **Objetivos**: Metas con prioridad y progreso
- **Creencias**: Conocimiento del mundo con confianza
- **Relaciones**: Vínculos con otros agentes

**Detalles técnicos**:
- Clase `EstadoAgenteLLM`: Estado completo del agente
- **Event Sourcing**: Registro inmutable de todos los cambios
- **Persistencia**: Guardado a JSON (snapshot + event log)
- **Recuperación**: Carga de estado desde archivos

```bash
python 02_gestion_estado.py
```

**Características especiales**:
- Snapshots para recuperación rápida
- Event log para auditoría completa
- Versionado de estado
- Historial de cambios

---

### 3. **03_buffer_contexto.py** - Buffer de Contexto y Límites en LLMs
**Conceptos**: Ventana de contexto, compresión, limitaciones de tokens

Maneja la restricción crítica de los LLMs: contexto limitado.

- **Buffer de contexto**: Ventana móvil de información reciente
- **Gestión de tokens**: Tracking de uso y disponibilidad
- **Estrategias de eliminación**: FIFO, LRU, importancia, relevancia
- **Compresión**: Resumen extractivo y abstractivo

**Detalles técnicos**:
- Clase `BufferContexto`: Buffer circular con límite de tokens
- Clase `CompresorContexto`: Compresión y resumen de contenido
- Estrategia `FIFO`: Descarta lo más antiguo
- Estrategia `LRU`: Descarta lo menos recientemente usado
- Estrategia `RELEVANCIA`: Descarta lo menos importante vs recency

```bash
python 03_buffer_contexto.py
```

**Parámetros personalizables**:
- `max_tokens`: Límite total (por defecto 2048)
- `margen_seguridad`: Reserva de seguridad (90%)
- `estrategia`: Método de eliminación

---

### 4. **04_embeddings_busqueda.py** - Embeddings y Búsqueda Semántica
**Conceptos**: Representación vectorial, similitud coseno, búsqueda híbrida

Implementa búsqueda semántica sin dependencias externas (demostración educativa):

- **Generación de embeddings**: Conversión de texto a vectores
- **Búsqueda vectorial**: Similitud coseno entre vectores
- **Búsqueda por palabras clave**: Full-text search
- **Búsqueda híbrida**: Combinación de ambas

**Detalles técnicos**:
- Clase `GeneradorEmbeddings`: TF-IDF simplificado (sin dependencias)
- Clase `IndiceVectorial`: Índice simple de búsqueda
- Clase `BuscadorHibrido`: Combina keyword + semantic
- Métrica: Similitud coseno (0.0 a 1.0)

```bash
python 04_embeddings_busqueda.py
```

**Métricas de similitud implementadas**:
- Coseno: Para búsqueda vectorial semántica
- Jaccard: Para conjuntos de palabras (keyword)
- Euclidiana: Distancia en espacio vectorial

**Nota sobre producción**: Para usar modelos reales de embeddings:
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
embedding = model.encode(texto)
```

---

### 5. **05_rag_retrieval.py** - RAG (Retrieval-Augmented Generation)
**Conceptos**: Pipeline completo de recuperación aumentada

Implementa el flujo completo de RAG:

1. **Recuperación**: Buscar documentos relevantes
2. **Construcción de contexto**: Ensamblar fragmentos de documentos
3. **Creación de prompt**: Enriquecer pregunta con contexto
4. **Generación**: LLM responde basándose en contexto
5. **Postprocesamiento**: Formatear respuesta

**Detalles técnicos**:
- Clase `BaseConocimiento`: Almacena documentos indexados
- Clase `PipelineRAG`: Orquesta el flujo completo
- Búsqueda por palabras clave simple
- Construcción inteligente de contexto (max_chars)
- Generación de respuestas simuladas

```bash
python 05_rag_retrieval.py
```

**Ventajas de RAG**:
- Información actualizada (basada en documentos)
- Cita de fuentes
- Menos alucinaciones
- Customizable por dominio

**Integración con Ollama** (pseudocódigo incluido):
```python
from langchain.llms import Ollama
ollama = Ollama(model="mistral")
response = ollama(prompt_enriquecido)
```

---

### 6. **06_memoria_conversacional.py** - Memoria en Agentes Conversacionales
**Conceptos**: Historial acumulativo, resolución de referencias, privacidad

Demuestra cómo agentes mantienen conversaciones coherentes:

- **Historial de conversación**: Contexto acumulativo de turnos
- **Seguimiento de entidades**: NER básica con tipos
- **Resolución de referencias anafóricas**: "él", "ella", "lo" -> entidad
- **Personalización**: Adaptar respuestas según usuario
- **Privacidad**: Filtrado de datos sensibles (GDPR)

**Detalles técnicos**:
- Clase `SeguimientoEntidades`: Extrae y rastrea entidades
- Clase `HistorialConversacion`: Gestiona turno a turno
- NER básica para: email, teléfono, productos, números
- Resolución heurística de pronombres
- Conformidad GDPR: marcar y limpiar datos sensibles

```bash
python 06_memoria_conversacional.py
```

**Características de privacidad**:
- Identificación de PII (Personally Identifiable Information)
- Filtrado de datos sensibles en contexto
- Método `limpiar_datos_sensibles()` para cumplimiento GDPR
- Redacción automática de información sensible

---

### 7. **07_memoria_jerarquica.py** - Sistema de Memoria Jerárquica Avanzada
**Conceptos**: Consolidación, compresión, interferencia, olvido adaptativo

Arquitectura escalable con tres niveles jerárquicos:

- **Nivel 1 (Episódico)**: Detalles específicos de eventos
- **Nivel 2 (Táctico)**: Patrones y regularidades
- **Nivel 3 (Estratégico)**: Reglas abstractas generales

**Flujo de consolidación** (como "sueño" en humanos):
1. Registrar episodios con detalles específicos
2. Extraer patrones (frecuencia >= 2)
3. Generar reglas desde patrones confiables
4. Envejecer episodios (olvido natural)
5. Eliminar información insignificante

**Detalles técnicos**:
- Clase `MemoriaJerarquica`: Gestiona 3 niveles
- `RegistroEpisodico`: Detalles + timestamp + importancia
- `PatronTactico`: Agrupa episodios similares
- `ReglaBstracia`: Generalización de patrones
- Olvido adaptativo: Score = importancia × exp(-edad/30)

```bash
python 07_memoria_jerarquica.py
```

**Beneficios del diseño jerárquico**:
- **Escalabilidad**: Millones de episodios -> pocos patrones -> reglas
- **Eficiencia**: 6 episodios -> 2 patrones -> 2 reglas (compresión)
- **Coherencia**: Recuperación comienza en nivel abstracto
- **Privacidad**: Olvido selectivo de episodios antiguos

---

## 🚀 Quickstart

### Requisitos Previos

```bash
# 1. Instalar Python 3.8+
python --version

# 2. Instalar dependencias para ejemplos
pip install langchain ollama sentence-transformers pydantic

# 3. (Opcional) Instalar Ollama para integración real
# Ver: https://ollama.ai
```

### Ejecutar Ejemplos Individuales

```bash
# Cambiar al directorio
cd ejemplos/memoria

# Ejecutar ejemplo 1: Tipos de memoria
python 01_tipos_memoria.py

# Ejecutar ejemplo 2: Gestión de estado
python 02_gestion_estado.py

# ... etc
```

### Script de Ejecución Secuencial

```bash
# Ejecutar TODOS los ejemplos en orden
for i in {1..7}; do
    echo "=== Ejemplo $i ==="
    python 0${i}_*.py
    echo ""
done
```

---

## 📊 Comparativa de Ejemplos

| Ejemplo | Concepto | Complejidad | Tokens | Dependencias |
|---------|----------|-------------|--------|--------------|
| 01 | 5 tipos de memoria | ⭐ | ~100 | ninguna |
| 02 | Estado + Event sourcing | ⭐⭐ | ~300 | pydantic |
| 03 | Buffer + Compresión | ⭐⭐ | ~250 | ninguna |
| 04 | Embeddings + Búsqueda | ⭐⭐⭐ | ~400 | numpy |
| 05 | RAG completo | ⭐⭐⭐ | ~350 | langchain |
| 06 | Conversación + NER | ⭐⭐ | ~280 | ninguna |
| 07 | Jerarquía + Consolidación | ⭐⭐⭐ | ~320 | ninguna |

---

## 🔗 Integración con Ollama y LangChain

Cada ejemplo está diseñado para integración fácil con Ollama:

```python
# Instalación
pip install langchain ollama

# Ejecutar Ollama
ollama serve

# En otra terminal, descargar modelo
ollama pull mistral  # o neural-chat, orca-mini, etc

# Usar en código
from langchain.llms import Ollama
from langchain.memory import ConversationBufferWindowMemory

llm = Ollama(model="mistral")
memory = ConversationBufferWindowMemory(k=3)

# RAG + Memory + LLM
from langchain.chains import RetrievalQA
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,  # De ejemplo 04
    memory=memory
)
```

---

## 📖 Mapeo a Temario

Cada ejemplo cubre directamente secciones del temario:

```
02-memoria-contexto.adoc
├── Módulo 1: Tipos de Memoria
│   └── 01_tipos_memoria.py ✓
│
├── Módulo 2: Gestión de Estado
│   └── 02_gestion_estado.py ✓
│
├── Módulo 3: Memoria a Corto Plazo (Buffer)
│   └── 03_buffer_contexto.py ✓
│
├── Módulo 4: Memoria a Largo Plazo (Indexación)
│   ├── 04_embeddings_busqueda.py ✓
│   └── 05_rag_retrieval.py ✓
│
├── Módulo 5: Recuperación de Información
│   └── 04_embeddings_busqueda.py (híbrida) ✓
│
├── Módulo 6: Memoria Conversacional
│   └── 06_memoria_conversacional.py ✓
│
└── Módulo 7: Arquitecturas Avanzadas
    └── 07_memoria_jerarquica.py ✓
```

---

## 🎯 Propósitos Didácticos

Cada ejemplo demuestra:

### 01 - Fundamentos Biológicos
- Cómo la biología inspira arquitecturas de IA
- Importancia de múltiples escalas temporales

### 02 - Persistencia y Recuperabilidad
- Cómo guardar y recuperar estado completo
- Auditoría mediante event sourcing

### 03 - Restricciones Prácticas
- Cómo los LLMs tienen limitaciones de contexto
- Estrategias de compresión

### 04 - Búsqueda Inteligente
- De palabras clave a semántica
- Métricas de similitud

### 05 - Generación Fundamentada
- RAG reduce alucinaciones
- Cita de fuentes

### 06 - Interacción Natural
- Coherencia conversacional
- Privacidad en sistemas reales

### 07 - Escalabilidad
- Cómo escalar a millones de interacciones
- Consolidación de conocimiento

---

## 🔧 Personalización

### Aumentar Capacidad de Memoria

```python
# Cambiar límite de tokens en buffer
buffer = BufferContexto(max_tokens=4096)

# Aumentar capacidad de memoria de trabajo
mem_trabajo = MemoriaTrabajoLimitada(capacidad=10)

# Más documentos en base de conocimiento
for doc in documentos_adicionales:
    base.agregar_documento(doc)
```

### Usar Diferentes Estrategias

```python
# Cambiar estrategia de eliminación en buffer
buffer = BufferContexto(
    estrategia=EstrategiaEliminacion.IMPORTANCIA
)

# Cambiar pesos en búsqueda híbrida
resultados = buscador.busqueda_hibrida(
    query,
    peso_keyword=0.5,
    peso_semantica=0.5
)
```

### Integrar Modelos Reales

```python
# Usar embeddings reales
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

# Reemplazar GeneradorEmbeddings.generar_embedding()
def generar_embedding(self, texto):
    return model.encode(texto).tolist()
```

---

## 📋 Checklist de Aprendizaje

- [ ] Ejecuté todos los 7 ejemplos
- [ ] Entiendo cómo los 5 tipos de memoria funcionan
- [ ] Sé cómo persistir estado de agentes
- [ ] Entiendo el problema de límites de contexto
- [ ] Puedo explicar búsqueda semántica vs keywords
- [ ] Sé cómo funciona RAG
- [ ] Entiendo resolución de referencias anafóricas
- [ ] Conozco consolidación jerárquica de memoria
- [ ] Puedo integrar con Ollama en mis proyectos
- [ ] Considero privacidad en sistemas de memoria

---

## 🐛 Troubleshooting

**P: Los ejemplos son muy lentos**
R: Aumenta `margen_seguridad` en buffer o reduce documentos en RAG

**P: ¿Cómo uso esto con mi propio LLM?**
R: Reemplaza la función `_generar_respuesta()` en RAG para llamar a tu LLM

**P: ¿Cómo garantizo privacidad?**
R: Usa `limpiar_datos_sensibles()` en conversaciones y marca datos como sensibles

**P: ¿Debo usar todos los niveles de memoria?**
R: Depende de tu caso. Conversación simple = solo episódico. Agente complejo = todos.

---

## 📚 Recursos Adicionales

- **LangChain Docs**: https://python.langchain.com
- **Ollama**: https://ollama.ai
- **Sentence Transformers**: https://www.sbert.net
- **Paper RAG**: "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"

---

## 📝 Licencia

Ejemplos educativos para el Curso de Agentes de IA

---

## 💡 Tips para Instructores

Para usar estos ejemplos en clase:

1. **Semana 1**: Ejecutar ejemplos 1-3 (conceptos)
2. **Semana 2**: Ejecutar ejemplos 4-5 (búsqueda y RAG)
3. **Semana 3**: Ejecutar ejemplos 6-7 (avanzado)
4. **Proyecto**: Combinar todos en un agente conversacional

Cada ejemplo toma ~15 minutos para ejecutar y comprender.

---

**Creado**: Noviembre 2024
**Versión**: 1.0
**Compatibilidad**: Python 3.8+
