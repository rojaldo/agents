# Ejercicio: Análisis de APOD (Astronomy Picture of the Day)

## Objetivo
Crear un crew que consulte la API de NASA's APOD y analice las imágenes obtenidas.

## Descripción
Este ejercicio demuestra cómo crear un equipo de agentes que trabaja con imágenes y metadatos:
1. **APIDeveloper**: Consulta la API de NASA APOD
2. **ImageProcessor**: Descarga y procesa imágenes
3. **ImageAnalyst**: Analiza propiedades de las imágenes

## Estructura
```
apod/
├── apod.py             # Archivo principal del ejercicio
├── README.md           # Este archivo
└── data/               # Carpeta donde se guardan imágenes y datos
```

## Herramientas Implementadas
- `query_apod_api()`: Consulta la API de NASA APOD
- `download_images()`: Descarga imágenes de las URLs proporcionadas
- `process_apod_metadata()`: Procesa metadatos de APOD en formato tabular
- `analyze_images()`: Analiza propiedades de las imágenes (dimensiones, brillo, colores)

## Agentes
- **APIDeveloper**: Desarrollador especializado en APIs
- **ImageProcessor**: Procesador de imágenes y descargas
- **ImageAnalyst**: Analista especializado en imágenes

## Ejecución

### Requisitos
- Python 3.10+
- Mistral corriendo en localhost:8000
- Conexión a internet (para acceder a la API de NASA)
- Dependencias instaladas (`pip install -r requirements.txt`)
- API Key de NASA (obtén una gratis en https://api.nasa.gov/)

### Pasos
1. Obtén tu API key gratuita de NASA:
   - Ve a https://api.nasa.gov/
   - Completa el formulario y recibe tu key por correo

2. Actualiza el archivo `.env` con tu API key:
   ```
   NASA_API_KEY=tu_api_key_aqui
   ```

3. Asegúrate de tener Mistral ejecutándose:
   ```bash
   ollama run mistral
   ```

4. Desde la carpeta raíz del proyecto, ejecuta:
   ```bash
   python apod/apod.py
   ```

5. Los datos e imágenes se guardarán en `apod/data/`

## Salida Esperada
El crew generará:
- Metadatos brutos: `apod/data/apod_raw.json`
- Metadatos procesados: `apod/data/apod_metadata.csv`
- Imágenes descargadas: `apod/data/apod_YYYY-MM-DD.jpg`
- Análisis estadístico con:
  - Propiedades de imágenes (dimensiones, tamaño)
  - Estadísticas de brillo y color
  - Resumen de propiedades

## API Utilizada
**NASA APOD API**: https://api.nasa.gov/planetary/apod
- Requiere API key (gratuita)
- Devuelve datos en formato JSON
- Incluye metadatos e URLs de imágenes

## Conceptos Aprendidos
- Descarga de archivos con requests
- Procesamiento de imágenes con PIL
- Análisis de propiedades de imágenes (brillo, colores, dimensiones)
- Trabajo con numpy para análisis numérico
- Coordinación de agentes para flujos complejos de procesamiento de datos
- Manejo de archivos binarios (imágenes)
