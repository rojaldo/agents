# Ejercicio: Análisis de RestCountries API

## Objetivo
Crear un crew que consulte la API de RestCountries y analice los datos obtenidos.

## Descripción
Este ejercicio demuestra cómo crear un equipo de agentes que trabajan con APIs externas:
1. **APIDeveloper**: Consulta la API de RestCountries
2. **DataProcessor**: Procesa y limpia datos JSON
3. **DataAnalyst**: Realiza análisis estadísticos

## Estructura
```
restcountries/
├── restcountries.py    # Archivo principal del ejercicio
├── README.md           # Este archivo
└── data/               # Carpeta donde se guardan los datos descargados
```

## Herramientas Implementadas
- `query_countries_api()`: Consulta la API de RestCountries
- `process_json_data()`: Procesa datos JSON en formato tabular (CSV)
- `analyze_countries_data()`: Calcula estadísticas sobre países

## Agentes
- **APIDeveloper**: Desarrollador especializado en APIs
- **DataProcessor**: Procesador de datos JSON
- **DataAnalyst**: Analista estadístico

## Ejecución

### Requisitos
- Python 3.10+
- Mistral corriendo en localhost:8000
- Conexión a internet (para acceder a la API)
- Dependencias instaladas (`pip install -r requirements.txt`)

### Pasos
1. Asegúrate de tener Mistral ejecutándose:
   ```bash
   ollama run mistral
   ```

2. Desde la carpeta raíz del proyecto, ejecuta:
   ```bash
   python restcountries/restcountries.py
   ```

3. Los datos descargados y procesados se guardarán en `restcountries/data/`

## Salida Esperada
El crew generará:
- Datos brutos: `restcountries/data/countries_raw.json`
- Datos procesados: `restcountries/data/countries_processed.csv`
- Análisis estadístico con:
  - Distribución de países por región
  - Estadísticas de población
  - Estadísticas de área geográfica
  - Idiomas más comunes
  - Rankings de países

## API Utilizada
**RestCountries API v3.1**: https://restcountries.com/v3.1
- No requiere autenticación
- Acceso público sin restricciones
- Devuelve datos en formato JSON

## Conceptos Aprendidos
- Integración con APIs REST
- Consumo de datos JSON
- Transformación de JSON a formatos tabulares
- Análisis de datos geográficos
- Coordinación de agentes para flujos de datos complejos
