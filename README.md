# Curso de Agentes de IA

Un curso completo y práctico sobre el desarrollo de agentes inteligentes utilizando las tecnologías y frameworks más modernos del ecosistema de Inteligencia Artificial.

## 📋 Descripción General

Este repositorio contiene un curso estructurado de 12 módulos que cubre desde los fundamentos de los agentes de IA hasta temas avanzados como sistemas multi-agente, bases de datos vectoriales, recuperación aumentada por generación (RAG) y evaluación de agentes.

El curso está diseñado para proporcionar tanto conocimiento teórico como práctico, con presentaciones interactivas en RevealJS y documentación detallada en AsciiDoc.

## 🎯 Objetivos del Curso

- Comprender qué son los agentes de IA y cómo funcionan
- Aprender a utilizar frameworks populares (AutoGen, CrewAI, LangChain, Langflow, n8n)
- Implementar sistemas de memoria y contexto efectivos
- Dominar técnicas de RAG (Retrieval-Augmented Generation)
- Trabajar con bases de datos vectoriales y de grafos
- Diseñar y orquestar sistemas multi-agente
- Evaluar y probar la calidad de los agentes
- Integrar protocolos MCP (Model Context Protocol)

## 📚 Módulos del Curso

### 1. **Fundamentos de Agentes de IA** (Documentación Base)
- Conceptos básicos de agentes
- Arquitectura de un agente
- Ciclos de decisión y acción
- Casos de uso principales

### 2. **AutoGen**
- Framework de Microsoft para agentes conversacionales
- Comunicación multi-agente
- Configuración y personalización
- Ejemplos prácticos
- **Presentación**: `docs/reveal/autogen.html` (106 slides)

### 3. **CrewAI**
- Framework para crear equipos de agentes
- Roles y tareas
- Colaboración entre agentes
- Casos de uso empresariales
- **Presentación**: `docs/reveal/crewai.html` (disponible)

### 4. **Langflow**
- Interfaz visual para construcción de flujos
- Drag-and-drop workflow automation
- Integración con LangChain
- Deployment de flujos
- **Presentación**: `docs/reveal/langflow.html` (101 slides)

### 5. **LangChain**
- Framework principal para construir aplicaciones con LLMs
- Chains y Agents
- Prompts y templates
- Tools y utilities
- **Presentación**: `docs/reveal/langchain.html` (disponible)

### 6. **MCP (Model Context Protocol)**
- Protocolo estándar de Anthropic para contexto
- Integración con Claude
- Servidores MCP
- Casos de uso
- **Presentación**: `docs/reveal/mcp.html` (disponible)

### 7. **Memoria y Contexto**
- Tipos de memoria (corto/largo plazo)
- Persistencia de estado
- Gestión de contexto en conversaciones
- Estrategias de summarización
- **Presentación**: `docs/reveal/memoria-contexto.html` (disponible)

### 8. **RAG (Retrieval-Augmented Generation)**
- Recuperación de información
- Augmentación de prompts
- Mejora de respuestas con contexto externo
- Pipelines RAG completos
- **Presentación**: `docs/reveal/RAG.html` (disponible)

### 9. **Bases de Datos Vectoriales y Grafos**
- ChromaDB, Weaviate, Qdrant, Milvus
- Embeddings y búsqueda semántica
- Bases de datos de grafos: Neo4j, ArangoDB
- Integración con agentes
- **Presentación**: `docs/reveal/bases_datos_vectoriales_grafos.html` (63 slides)

### 10. **Evaluación y Testing de Agentes**
- Métricas de calidad
- Unit tests y integration tests
- Evaluación de respuestas
- Monitoreo en producción
- **Presentación**: `docs/reveal/evaluacion-testing.html` (75 slides)

### 11. **Sistemas Multi-Agente y Coordinación**
- Comunicación entre agentes
- Protocolos de coordinación
- Negociación y resolución de conflictos
- Teoría de juegos aplicada
- **Presentación**: `docs/reveal/multi-agentes-coordinacion.html` (64 slides)

### 12. **n8n - Automatización Empresarial**
- Plataforma de automatización visual
- Workflows complejos
- Integraciones con múltiples servicios
- Deployment y escalado
- **Presentación**: `docs/reveal/n8n.html` (141 slides)

## 📁 Estructura del Repositorio

```
cursos/agents/
   README.md                                    # Este archivo
   docs/
      REVEAL_CUSTOMIZATION_GUIDE.md           # Guía de personalización de RevealJS
      autogen.adoc                            # Fuente: AutoGen
      crewai.adoc                             # Fuente: CrewAI
      langflow.adoc                           # Fuente: Langflow
      langchain.adoc                          # Fuente: LangChain
      mcp.adoc                                # Fuente: MCP
      memoria-contexto.adoc                   # Fuente: Memoria
      multi-agentes-coordinacion.adoc         # Fuente: Multi-Agentes
      bases_datos_vectoriales_grafos.adoc     # Fuente: Bases de Datos
      evaluacion-testing.adoc                 # Fuente: Testing
      n8n.adoc                                # Fuente: n8n
      RAG.adoc                                # Fuente: RAG
      opencode.adoc                           # Fuente: Open Code
      reveal/
          autogen.html                        # Presentación RevealJS (106 slides)
          crewai.html                         # Presentación RevealJS
          langflow.html                       # Presentación RevealJS (101 slides)
          langchain.html                      # Presentación RevealJS
          mcp.html                            # Presentación RevealJS
          memoria-contexto.html               # Presentación RevealJS
          multi-agentes-coordinacion.html     # Presentación RevealJS (64 slides)
          bases_datos_vectoriales_grafos.html # Presentación RevealJS (63 slides)
          evaluacion-testing.html             # Presentación RevealJS (75 slides)
          n8n.html                            # Presentación RevealJS (141 slides)
          RAG.html                            # Presentación RevealJS
```

## 🚀 Cómo Usar Este Curso

### Acceder a las Presentaciones

1. **Opción A: Servir localmente**
   ```bash
   cd /home/rojaldo/cursos/agents/docs/reveal/
   python3 -m http.server 8000
   ```
   Luego abre tu navegador en `http://localhost:8000`

2. **Opción B: Abrir directamente en el navegador**
   - Navega a cualquier archivo `.html` en `docs/reveal/`
   - Abre con tu navegador preferido

### Navegar en las Presentaciones

- **Avanzar/Retroceder**: Flechas del teclado o clic
- **Vista general**: Presiona `Esc`
- **Pantalla completa**: Presiona `F`
- **Notas del orador**: Presiona `S`
- **Búsqueda**: Presiona `Ctrl+F` o `Cmd+F`

### Documentación Fuente (AsciiDoc)

Los archivos `.adoc` contienen la documentación detallada de cada módulo. Puedes:
- Leerlos en cualquier editor de texto
- Convertirlos a HTML/PDF usando AsciiDoctor
- Usarlos como referencia mientras visualizas las presentaciones

## 🎓 Ruta de Aprendizaje Recomendada

### Principiante
1. Fundamentos de Agentes de IA
2. AutoGen - Primeros pasos
3. LangChain - Conceptos básicos
4. Memoria y Contexto
5. Evaluación básica de agentes

### Intermedio
6. CrewAI - Equipos de agentes
7. Langflow - Automatización visual
8. RAG - Mejora con contexto externo
9. Bases de Datos Vectoriales

### Avanzado
10. Sistemas Multi-Agente
11. Coordinación y protocolos
12. MCP (Model Context Protocol)
13. Evaluación avanzada
14. n8n - Automatización empresarial

### Especializado
- Bases de Datos de Grafos
- Teoría de juegos en sistemas multi-agente
- Monitoreo en producción

## ⚙️ Requisitos Técnicos

### Software Requerido
- Python 3.8+
- Node.js 14+ (para algunas herramientas)
- Git
- Navegador web moderno (Chrome, Firefox, Safari, Edge)

### Librerías Python Principales
```
langchain>=0.1.0
autogen-agentchat>=0.2.0
crewai>=0.1.0
chromadb>=0.3.0
openai>=1.0.0
pydantic>=2.0.0
```

### Servicios Externos
- OpenAI API (o compatible)
- Hugging Face (para embeddings)
- Base de datos vectorial (ChromaDB, Weaviate, etc.)

## 📊 Contenido de las Presentaciones

### Estadísticas

| Módulo | Slides | Tamaño | Estado |
|--------|--------|--------|--------|
| AutoGen | 106 | 55K | ✓ |
| CrewAI | ~80 | 32K | ✓ |
| Langflow | 101 | 52K | ✓ |
| LangChain | ~110 | 66K | ✓ |
| MCP | ~95 | 70K | ✓ |
| Memoria | ~105 | 77K | ✓ |
| RAG | ~100 | 57K | ✓ |
| Vectorial/Grafos | 63 | 39K | ✓ |
| Testing | 75 | 59K | ✓ |
| Multi-Agentes | 64 | 52K | ✓ |
| n8n | 141 | 87K | ✓ |
| **TOTAL** | **~1,050** | **660K** | ✓ |

## 🔧 Temas Cubiertos

### Frameworks y Librerías
- **AutoGen** (Microsoft): Agentes conversacionales multi-agente
- **CrewAI**: Teams de agentes con roles y tareas
- **LangChain**: Framework principal para LLM applications
- **Langflow**: Interfaz visual para LangChain
- **n8n**: Plataforma de automatización empresarial
- **MCP**: Model Context Protocol de Anthropic

### Bases de Datos
- **Vectoriales**: ChromaDB, Weaviate, Qdrant, Milvus
- **Grafos**: Neo4j, ArangoDB
- **Búsqueda**: Elasticsearch, Algolia

### Técnicas Principales
- Retrieval-Augmented Generation (RAG)
- Embedding y búsqueda semántica
- Memory systems (short/long-term)
- Multi-agent communication
- Prompt engineering
- Chain of Thought (CoT)
- Function calling
- Tool use

### Temas Avanzados
- Teoría de juegos
- Negociación entre agentes
- Coordinación distribuida
- Monitoreo y logging
- Testing y evaluación
- Métricas de calidad
- Calibración y sesgo

## ✨ Características Especiales

### Presentaciones Interactivas
- Todas las presentaciones usan **RevealJS 4.5.0**
- Tema profesional y legible
- Resaltado de código con Atom One Light
- Navegación fluida y responsiva
- Notas del orador disponibles

### Código Bien Formateado
- Ejemplos prácticos en Python
- Snippets de Cypher para Neo4j
- Queries SQL y pseudo-código
- Configuraciones JSON/YAML

### Documentación Completa
- Explicaciones detalladas
- Diagramas conceptuales
- Casos de uso reales
- Mejores prácticas

## 📖 Referencias y Recursos

### Sitios Oficiales
- [OpenAI API](https://platform.openai.com)
- [LangChain Docs](https://python.langchain.com)
- [AutoGen](https://microsoft.github.io/autogen/)
- [CrewAI](https://crewai.io)
- [Neo4j](https://neo4j.com)
- [Anthropic Claude](https://claude.ai)

### Comunidades
- OpenAI Community
- LangChain Discord
- AI Alignment Forum
- Stack Overflow (tag: langchain, autogen)

### Libros y Papers
- "Building LLM Applications" (various authors)
- "Agents as a Service" papers
- Multi-agent Systems literature
- Reinforcement Learning from Human Feedback (RLHF)

## 🎨 Personalización y Extensión

### Modificar Presentaciones
1. Edita los archivos `.adoc` en `docs/`
2. Regenera las presentaciones HTML usando el script de conversión
3. Las presentaciones usarán automáticamente la guía de estilos en `REVEAL_CUSTOMIZATION_GUIDE.md`

### Agregar Nuevos Módulos
1. Crea un nuevo archivo `.adoc` en `docs/`
2. Sigue el formato y estructura de los módulos existentes
3. Genera el archivo RevealJS correspondiente
4. Actualiza este README

### Estilos y Temas
- Todos los estilos están centralizados en `REVEAL_CUSTOMIZATION_GUIDE.md`
- Personaliza colores, tamaños y tipografía editando ese archivo
- Los cambios se aplican a todas las presentaciones

## 🎨 Guía de Estilos RevealJS

Las presentaciones siguen esta estructura:
- **Texto alineado a la izquierda** para mejor legibilidad
- **Tamaños de fuente escalados** para claridad
- **Código con fondo gris** y bordes definidos
- **Listas bien espaciadas** y legibles
- **Colores consistentes** (#555555 como principal)
- **Transiciones suaves** entre slides
- **Numeración de slides** visible

## ✅ Checklist de Verificación

Cada presentación ha sido:
- ✓ Generada desde fuente AsciiDoc verificada
- ✓ Validada para tag HTML balance
- ✓ Probada en navegadores modernos
- ✓ Formateada según REVEAL_CUSTOMIZATION_GUIDE.md
- ✓ Optimizada para presentación en aula
- ✓ Corregida de errores de maquetación y código

## 🛠️ Solución de Problemas

### Las presentaciones no cargan
- Verifica que todos los CDN (jsDelivr, cdnjs) sean accesibles
- Intenta servir localmente con `python3 -m http.server`
- Comprueba la consola del navegador (F12) para errores

### Código no se ve correctamente
- Asegúrate de que usas un navegador compatible con RevealJS
- Prueba en modo pantalla completa (F)
- Verifica que los archivos HTML están completos (no truncados)

### Problemas de rendimiento
- Cierra otras pestañas del navegador
- Desactiva extensiones del navegador
- Prueba en un navegador diferente

## 🤝 Soporte y Contribuciones

Para reportar problemas o sugerir mejoras:
1. Verifica que el problema no está documentado
2. Proporciona detalles específicos y capturas de pantalla si es posible
3. Incluye información del navegador y sistema operativo
4. Sugiere soluciones si las tienes

## 📜 Licencia

Este curso es material educativo. Respeta los términos de licencia de las librerías y frameworks utilizados.

## 🎓 Conclusión

Este curso proporciona una base sólida en el desarrollo de agentes de IA, desde conceptos fundamentales hasta sistemas complejos y distribuidos. Cada módulo construye sobre los anteriores, permitiéndote progresar de forma gradual y estructurada.

¡Buena suerte en tu aprendizaje de agentes de IA!

---

**Última actualización**: Noviembre 2024
**Versión del curso**: 1.0
**Presentaciones**: 11 módulos
**Total de slides**: ~1,050
