# CrewAI Multi-Agent Exercises

Este proyecto contiene tres ejercicios que demuestran cómo usar **CrewAI** para crear sistemas multi-agentes que resuelven tareas complejas de análisis de datos.

## Características

✅ **Tres ejercicios completos con CrewAI**:
- Titanic Dataset Analysis
- RestCountries API Analysis
- APOD (Astronomy Picture of the Day) Analysis

✅ **Arquitectura de multi-agentes**:
- Cada ejercicio usa 3 agentes especializados
- Los agentes colaboran a través de tareas (Tasks) con dependencias
- Las herramientas (Tools) son reutilizables

✅ **Integración con Ollama**:
- Todos los ejercicios están configurados para usar Mistral vía Ollama
- Soporte para LLMs locales

## Estructura

```
crewai/
├── crew_tools.py              # Herramientas reutilizables para agentes
├── tools.py                   # Módulo genérico de funcionalidades
│
├── titanic/
│   ├── titanic.py             # Ejercicio 1: Análisis Titanic con CrewAI
│   └── data/                  # Datos generados
│
├── restcountries/
│   ├── restcountries.py       # Ejercicio 2: API RestCountries con CrewAI
│   └── data/                  # Datos generados
│
└── apod/
    ├── apod.py                # Ejercicio 3: NASA APOD con CrewAI
    └── data/                  # Datos generados
```

## Componentes Principales

### 1. **Agents** (Agentes)
Cada ejercicio define 3 agentes especializados:

**Titanic:**
- Data Engineer: Descarga y valida datos
- Data Analyst: Limpia y analiza datos
- Statistician: Realiza análisis estadísticos

**RestCountries:**
- API Developer: Obtiene datos de API
- Data Processor: Procesa datos JSON
- Data Analyst: Análisis estadísticos

**APOD:**
- API Developer: Obtiene datos de NASA
- Image Processor: Procesa metadatos
- Image Analyst: Análisis de contenido

### 2. **Tools** (Herramientas)
Las herramientas en `crew_tools.py` están decoradas con `@tool` de crewai y disponibles para todos los agentes:

- **DataDownloader**: Descarga CSV/JSON desde URLs
- **DataProcessor**: Carga, limpia y filtra datos
- **DataAnalyzer**: Estadísticas y correlaciones
- **APIClient**: Peticiones GET y guardado de respuestas

### 3. **Tasks** (Tareas)
Cada ejercicio define tareas que:
- Tienen un agente asignado
- Pueden tener dependencias en otras tareas
- Especifican descripción y salida esperada

**Ejemplo de estructura de tareas:**
```
task_download → task_validate → task_clean → task_analysis
```

### 4. **Crew** (Equipo)
Orquesta los agentes y tareas para ejecutarlas en orden respetando dependencias.

## Requisitos

### Sistema Operativo
- Linux/macOS/Windows con Docker o acceso local

### Python
- Python 3.9+
- Virtual environment (incluido)

### Dependencias Principales
```
crewai==1.5.0
langchain-community
pandas>=1.5.0
requests>=2.28.0
pillow>=9.0.0
numpy>=1.20.0
```

### Ollama (Requerido)
Para ejecutar con Mistral LLM localmente:

1. **Instalar Ollama**:
   - Descarga desde https://ollama.ai

2. **Descargar modelo Mistral**:
   ```bash
   ollama pull mistral
   ```

3. **Iniciar servicio**:
   ```bash
   ollama serve
   ```

   El servicio estará disponible en: `http://localhost:11434`

## Instalación

### 1. Crear Virtual Environment
```bash
uv venv
```

### 2. Instalar Dependencias
```bash
uv sync
```

O instalar manualmente:
```bash
pip install -r requirements.txt
```

## Ejecución

Asegúrate de que Ollama está corriendo antes de ejecutar los ejercicios.

### Ejecutar Titanic Analysis
```bash
python titanic/titanic.py
```

**Salida esperada:**
- Descarga dataset Titanic
- Limpia datos
- Calcula estadísticas
- Analiza correlaciones
- Genera archivos: `titanic_raw.csv`, `titanic_cleaned.csv`

### Ejecutar RestCountries Analysis
```bash
python restcountries/restcountries.py
```

**Salida esperada:**
- Obtiene datos de países desde API
- Procesa JSON a CSV
- Analiza distribución regional
- Calcula densidad poblacional
- Genera archivos: `countries_raw.json`, `countries.csv`

### Ejecutar APOD Analysis
```bash
python apod/apod.py
```

**Salida esperada:**
- Obtiene últimos 10 días de APOD
- Procesa metadatos
- Analiza tipos de medios
- Genera informe
- Genera archivos: `apod_data.json`, `apod_metadata.csv`

## Conceptos de CrewAI Demostrados

### 1. **Specialization**
Cada agente tiene un rol específico con backstory y goals claros

### 2. **Collaboration**
Los agentes colaboran a través de tareas con dependencias

### 3. **Tool Usage**
Los agentes usan herramientas específicas para completar tareas

### 4. **Task Orchestration**
El Crew orquesta tareas respetando dependencias y asignaciones

### 5. **Verbose Mode**
Cada agente reporta sus acciones para transparencia

## Flujo de Ejecución

```
Crew.kickoff()
  ├─ Task 1 (Agent A)
  │   └─ Tool 1, Tool 2
  ├─ Task 2 (Agent B) [Depende Task 1]
  │   └─ Tool 3, Tool 4
  ├─ Task 3 (Agent C) [Depende Task 2]
  │   └─ Tool 5
  └─ Task 4 (Agent C) [Depende Task 3]
      └─ Tool 6
```

## Personalización

### Agregar nuevas herramientas
1. Añadir función en `tools.py`
2. Decorar con `@tool` en `crew_tools.py`
3. Añadir a los agentes que las necesiten

### Modificar agentes
Edita el rol, goal, backstory y tools en cada ejercicio

### Ajustar tareas
Modifica descripción, expected_output y dependencias

## Resolución de Problemas

### "Cannot connect to Ollama"
- Asegúrate de ejecutar `ollama serve` en otra terminal
- Verifica que Mistral está instalado: `ollama pull mistral`
- Confirma que el servicio está en `http://localhost:11434`

### "OPENAI_API_KEY is required"
- CrewAI intenta usar OpenAI por defecto
- Este error indica que Ollama no está siendo reconocido
- Asegúrate de que Ollama está corriendo y accesible

### Errores de archivo no encontrado
- Asegúrate de ejecutar el script desde el directorio correcto
- Verifica que el directorio `data/` existe
- Comprueba permisos de escritura en `data/`

## Notas Importantes

1. **LLM Local**: Los ejercicios están diseñados para usar Mistral vía Ollama, no requieren API keys
2. **Herramientas Reutilizables**: El módulo `crew_tools.py` puede ser usado en otros proyectos
3. **Datos Reales**: Descarga datos reales (Titanic) y consulta APIs reales (RestCountries, APOD)
4. **Transparencia**: Modo verbose mostrado para ver todos los pasos de los agentes

## Estructura de Archivos Generados

Después de ejecutar los ejercicios:

```
titanic/data/
├── titanic_raw.csv        # 891 filas, 12 columnas
└── titanic_cleaned.csv    # Datos limpios

restcountries/data/
├── countries_raw.json     # Respuesta API completa
└── countries.csv          # Datos procesados

apod/data/
├── apod_data.json         # Respuesta API de APOD
└── apod_metadata.csv      # Metadatos extraídos
```

## Referencias

- [CrewAI Documentation](https://docs.crewai.com/)
- [Ollama](https://ollama.ai/)
- [LangChain](https://python.langchain.com/)

## Licencia

Estos ejercicios son para propósitos educativos.
