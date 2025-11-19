# Plan de Aprendizaje: RAG con Python

Este plan detalla una serie progresiva de ejemplos para dominar la creación de sistemas RAG (Retrieval-Augmented Generation) utilizando Python, LangChain, ChromaDB y Ollama.

## Tecnologías Clave

*   **Orquestación**: LangChain (Estándar de la industria, flexible).
*   **Base de Datos Vectorial**: ChromaDB (Open-source, local, fácil de usar).
*   **LLM y Embeddings**: Ollama (Ejecución local de modelos como `llama3.2` y `nomic-embed-text`).

## Listado de Ejemplos

### 1. Configuración del Entorno
*   **Objetivo**: Preparar las dependencias necesarias.
*   **Archivos**: `requirements.txt`

### 2. "Hello World" RAG (En Memoria)
*   **Concepto**: Entender el flujo básico `Input -> Embedding -> Búsqueda -> Output` sin persistencia.
*   **Stack**: LangChain + Ollama + FAISS (o Chroma en memoria).
*   **Descripción**: Script que define una lista de textos hardcodeados, los vectoriza en RAM y responde una pregunta basada solo en esos textos.

### 3. Base de Conocimiento Persistente
*   **Concepto**: Ingesta de documentos y persistencia de datos.
*   **Stack**: LangChain + ChromaDB (Persistente) + DirectoryLoader.
*   **Descripción**: Cargar documentos (Markdown/PDF) desde una carpeta, dividirlos en chunks y guardarlos en una base de datos ChromaDB local. Evita re-procesar si la DB ya existe.

### 4. RAG Conversacional (Chat con Memoria)
*   **Concepto**: Mantener el contexto de la conversación.
*   **Stack**: LangChain (`create_history_aware_retriever`) + ChromaDB.
*   **Descripción**: Un loop de chat en consola donde el usuario puede hacer preguntas de seguimiento (ej: "¿Y cuánto cuesta?" después de preguntar por un producto). El sistema reformula la pregunta antes de buscar.

### 5. Búsqueda Híbrida (Semántica + Palabras Clave)
*   **Concepto**: Mejorar la precisión combinando búsqueda vectorial con búsqueda por palabras clave (BM25).
*   **Stack**: LangChain (`EnsembleRetriever`) + BM25Retriever + ChromaDB.
*   **Descripción**: Sistema que recupera documentos usando ambos métodos, combina los resultados y elimina duplicados para pasar el mejor contexto al LLM.

### 6. RAG Agéntico (Router)
*   **Concepto**: Decidir *cuándo* buscar información y cuándo responder directamente.
*   **Stack**: LangChain (Agents) + Custom Tools.
*   **Descripción**: Un agente con acceso a una herramienta de búsqueda. Si el usuario saluda, responde normal. Si pregunta por información específica del curso, invoca la herramienta de búsqueda.

### 7. Evaluación de RAG (RAGAS)
*   **Concepto**: Medir la calidad de las respuestas (Fidelidad y Relevancia).
*   **Stack**: RAGAS + LangChain.
*   **Descripción**: Script que toma un dataset de prueba `(Pregunta, Respuesta_Esperada)`, ejecuta el pipeline RAG y calcula métricas de calidad.

### 8. RAG con CrewAI
*   **Concepto**: Agentes especializados colaborando con acceso a herramientas de búsqueda.
*   **Stack**: CrewAI + LangChain Tool (Chroma).
*   **Descripción**: Un equipo de agentes (Investigador y Redactor). El investigador usa una herramienta para buscar en la base de datos vectorial y el redactor compila la respuesta.

### 9. RAG con AutoGen
*   **Concepto**: Conversación multi-agente con capacidades de recuperación.
*   **Stack**: AutoGen + Function Calling (Tool).
*   **Descripción**: Un sistema donde un `UserProxy` y un `Assistant` colaboran. El `Assistant` puede invocar una función `search_docs` para recuperar contexto antes de responder.
