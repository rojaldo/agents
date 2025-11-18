# Autogen Exercises Collection

Colección de ejercicios prácticos para aprender a crear agentes con **Autogen** (Microsoft's AutoGen framework).

## 📚 Descripción General

Este proyecto contiene ejemplos y ejercicios progresivos para dominar la creación de agentes que colaboran entre sí utilizando:
- **Autogen**: Framework para crear agentes de IA cooperativos
- **Mistral**: LLM local para evitar dependencias externas
- **Herramientas personalizadas**: Funciones que los agentes pueden invocar
- **Equipos de agentes**: Coordinación entre múltiples agentes especializados

## 🎯 Ejercicios Incluidos

### 1. **Titanic Dataset Analysis**
📂 Directorio: `titanic/`

Analiza el dataset del Titanic con un equipo de tres agentes especializados.

**Agentes:**
- **DataEngineer**: Descarga y valida datasets
- **DataCleaner**: Limpia y preprocesa datos
- **DataAnalyst**: Realiza análisis estadísticos

**Conceptos:**
- Descarga de datos desde URLs
- Limpieza de datos con pandas
- Análisis estadístico descriptivo
- Coordinación entre agentes

[Ver detalles →](titanic/README.md)

---

### 2. **RestCountries API Analysis**
📂 Directorio: `restcountries/`

Consulta la API de RestCountries y analiza datos geográficos y demográficos.

**Agentes:**
- **APIDeveloper**: Consume APIs REST
- **DataProcessor**: Procesa datos JSON
- **DataAnalyst**: Analiza datos tabulares

**Conceptos:**
- Consumo de APIs REST
- Transformación de JSON a CSV
- Análisis geográfico
- Estadísticas por región

[Ver detalles →](restcountries/README.md)

---

### 3. **APOD (Astronomy Picture of the Day) Analysis**
📂 Directorio: `apod/`

Descarga y analiza imágenes del espacio desde la API de NASA APOD.

**Agentes:**
- **APIDeveloper**: Consulta la API de NASA
- **ImageProcessor**: Descarga y procesa imágenes
- **ImageAnalyst**: Analiza propiedades de imágenes

**Conceptos:**
- Descarga de archivos binarios
- Procesamiento de imágenes con PIL
- Análisis numérico con numpy
- Estadísticas de imágenes (brillo, colores, dimensiones)

[Ver detalles →](apod/README.md)

---

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.10 o superior
- pip o uv
- Ollama (para ejecutar Mistral localmente)

### Paso 1: Clonar o descargar el proyecto
```bash
cd autogen
```

### Paso 2: Crear entorno virtual
```bash
# Con uv (recomendado)
uv venv
source .venv/bin/activate

# O con venv
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### Paso 3: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Configurar variables de entorno
El archivo `.env` ya está configurado con valores por defecto. Puedes personalizarlo:

```bash
# Editar .env si necesitas cambiar configuración
nano .env
```

**Variables principales:**
- `LLM_MODEL`: Modelo a usar (mistral por defecto)
- `LLM_BASE_URL`: URL del servidor LLM local
- `NASA_API_KEY`: Tu API key de NASA (necesaria para APOD)

### Paso 5: Iniciar Mistral (LLM local)
```bash
# Instalar ollama desde https://ollama.ai
ollama pull mistral
ollama run mistral
```

El servidor estará disponible en `http://localhost:8000/v1`

---

## ▶️ Ejecución

### Ejecutar un ejercicio específico

```bash
# Ejercicio Titanic
python titanic/titanic.py

# Ejercicio RestCountries
python restcountries/restcountries.py

# Ejercicio APOD
python apod/apod.py
```

### Ejecutar todos los ejercicios
```bash
# Crear un script que ejecute todos
for exercise in titanic restcountries apod; do
    echo "Running $exercise..."
    python $exercise/${exercise}.py
    echo "---"
done
```

---

## 📁 Estructura del Proyecto

```
autogen/
├── README.md                          # Este archivo
├── specs.md                           # Especificaciones técnicas
├── .env                               # Configuración (variables de entorno)
├── requirements.txt                   # Dependencias de Python
│
├── titanic/
│   ├── titanic.py                     # Código principal
│   ├── README.md                      # Documentación específica
│   └── data/                          # Datos descargados y procesados
│
├── restcountries/
│   ├── restcountries.py               # Código principal
│   ├── README.md                      # Documentación específica
│   └── data/                          # Datos descargados y procesados
│
└── apod/
    ├── apod.py                        # Código principal
    ├── README.md                      # Documentación específica
    └── data/                          # Imágenes y metadatos descargados
```

---

## 🛠️ Herramientas Reutilizables

Cada ejercicio implementa herramientas (tools) que pueden ser reutilizadas:

### Titanic
- `download_dataset(url, output_path)` → Descarga archivos CSV
- `load_and_validate_data(file_path)` → Valida estructuras de datos
- `clean_data(file_path, output_path)` → Limpia valores faltantes
- `analyze_dataset(file_path)` → Estadísticas descriptivas

### RestCountries
- `query_countries_api(endpoint)` → Consulta genérica de APIs
- `process_json_data(input_file, output_file)` → JSON a CSV
- `analyze_countries_data(file_path)` → Análisis geográfico

### APOD
- `query_apod_api(days, output_file)` → Consulta API NASA
- `download_images(input_file, output_dir)` → Descarga binaria
- `process_apod_metadata(input_file, output_file)` → Procesa metadatos
- `analyze_images(image_dir)` → Análisis de propiedades

---

## 📚 Conceptos de Autogen

### Agentes
Entidades autónomas que pueden:
- Decidir qué herramientas usar
- Colaborar con otros agentes
- Iterar hasta completar tareas

```python
agent = AssistantAgent(
    name="DataEngineer",
    model_client=client,
    tools=[download_dataset, load_and_validate_data],
)
```

### Herramientas (Tools)
Funciones que los agentes pueden invocar:
```python
@tool
def my_function(param: str) -> dict:
    """Descripción de la herramienta"""
    return {"result": "..."}
```

### Equipos (Teams)
Coordinan múltiples agentes:
```python
team = RoundRobinGroupChat(
    [agent1, agent2, agent3]
)
result = await team.run(task)
```

### Tareas (Tasks)
Definen qué necesita hacerse:
```python
task = Task(
    description="Analizar datos...",
    agents=[agent1, agent2]
)
```

---

## 🔧 Solución de Problemas

### Error: "Connection refused" al conectar con LLM
**Solución:** Asegúrate de que Mistral está ejecutándose
```bash
ollama run mistral
```

### Error: "NASA_API_KEY not found"
**Solución:** Obtén una API key gratuita en https://api.nasa.gov/ y actualiza `.env`

### Error: "Module not found"
**Solución:** Instala las dependencias
```bash
pip install -r requirements.txt
```

---

## 📖 Recursos Adicionales

- **Autogen Docs**: https://microsoft.github.io/autogen/
- **Ollama**: https://ollama.ai/
- **Mistral Model**: https://mistral.ai/
- **NASA APIs**: https://api.nasa.gov/
- **Pandas Documentation**: https://pandas.pydata.org/
- **PIL/Pillow**: https://pillow.readthedocs.io/

---

## 🎓 Curva de Aprendizaje Sugerida

1. Comienza con **Titanic** para entender los conceptos básicos
2. Continúa con **RestCountries** para aprender sobre APIs
3. Finaliza con **APOD** para procesamiento de imágenes

Cada ejercicio construye sobre conceptos anteriores.

---

## 📝 Notas Importantes

- Los archivos `.env` contienen configuración sensible - no los commits a git
- Las herramientas están diseñadas para ser genéricas y reutilizables
- Cada ejercicio es independiente y puede ejecutarse por separado
- Los datos descargados se guardan en carpetas `data/` específicas

---

## 🤝 Contribuciones

Para extender este proyecto:
1. Crea un nuevo subdirectorio para tu ejercicio
2. Implementa tus propios agentes y herramientas
3. Sigue la estructura y nombrado de los ejercicios existentes
4. Documenta bien con README.md

---

## 📄 Licencia

Este proyecto es educativo y de código abierto.

---

**Última actualización:** Noviembre 2024
