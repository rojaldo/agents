# En este directorio hay un coleccion ede ejemplos y ejercicios para crear agentes con CrewAI.

## Especificaciones generales

- Cada ejercicio debe tener su propio subdirectorio.
- Cada ejercicio debe usar agentes, tasks, tools y crew de CrewAI.
- Cada ejercicio usa un llm en local (Mistral) para evitar dependencias externas.
- Guarda las configuraciones de LLM en variables de entorno declaradas en un archivo `.env`.
- Hay que conseguir hacer las tools mas genericas posibles para que se puedan reutilizar en otros ejercicios.

## Ejercicios 

### Titanic
- Objetivo: Crear un crew que descargue, limpie y analice el dataset del Titanic.
- Subdirectorio de datos: `data/`
- Archivo principal: `titanic.py`
- Herramientas:
  - Descargar dataset desde URL
  - Cargar y limpiar datos con pandas
  - Analizar datos con pandas
- Agentes:
  - Ingeniero de Datos: Descarga y valida los datos
  - Analista de Datos: Filtra y analiza los datos
  - Estadístico: Calcula estadísticas descriptivas
- Crew: Coordina las tareas entre los agentes para completar el análisis del Titanic.

### RestCountries API
- Objetivo: Crear un crew que consulte la API de RestCountries y analice los datos obtenidos.
- Subdirectorio de datos: `data/`
- Archivo principal: `restcountries.py`
- Herramientas:
  - Consultar API RESTCountries
  - Procesar datos JSON
  - Analizar datos con pandas
- Agentes:
  - Desarrollador API: Consulta la API y obtiene los datos
  - Procesador de Datos: Procesa y limpia los datos JSON
  - Analista de Datos: Realiza análisis estadísticos
- Crew: Coordina las tareas entre los agentes para completar el análisis de los países.

### Apod API
- Objetivo: Crear un crew que consulte la API de Astronomy Picture of the Day (APOD) y analice las imágenes obtenidas.
- Subdirectorio de datos: `data/`
- Archivo principal: `apod.py`
- Herramientas:
  - Consultar API APOD
  - Descargar y procesar imágenes
  - Analizar imágenes con PIL y numpy
- Agentes:
  - Desarrollador API: Consulta la API y obtiene las imágenes
  - Procesador de Imágenes: Descarga y procesa las imágenes
  - Analista de Imágenes: Realiza análisis estadísticos de las imágenes
- Crew: Coordina las tareas entre los agentes para completar el análisis de las imágenes APOD.

## Despliegue
- Hay que crear un entorno virtual con uv
- Instalar las dependencias del proyecto
- guardar los requisitos en requirements.txt
- Cada ejercicio debe poder ejecutarse de forma independiente.
- Incluir instrucciones claras en un README.md en cada subdirectorio de ejercicio.