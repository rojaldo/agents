# Ejercicio: Análisis del Dataset Titanic

## Objetivo
Crear un crew que descargue, limpie y analice el dataset del Titanic utilizando Autogen.

## Descripción
Este ejercicio demuestra cómo crear un equipo de agentes que colaboran para:
1. **DataEngineer**: Descarga el dataset desde GitHub
2. **DataCleaner**: Limpia los datos (maneja valores faltantes, ajusta tipos de datos)
3. **DataAnalyst**: Realiza análisis estadísticos descriptivos

## Estructura
```
titanic/
├── titanic.py          # Archivo principal del ejercicio
├── README.md           # Este archivo
└── data/               # Carpeta donde se guardan los datos descargados
```

## Herramientas Implementadas
- `download_dataset()`: Descarga el dataset desde URL
- `load_and_validate_data()`: Carga y valida los datos
- `clean_data()`: Limpia datos (valores faltantes, tipos)
- `analyze_dataset()`: Calcula estadísticas descriptivas

## Agentes
- **DataEngineer**: Ingeniero de datos que maneja descargas y validación
- **DataCleaner**: Especialista en limpieza y preprocesamiento
- **DataAnalyst**: Analista estadístico

## Ejecución

### Requisitos
- Python 3.10+
- Mistral corriendo en localhost:8000
- Dependencias instaladas (`pip install -r requirements.txt`)

### Pasos
1. Asegúrate de tener Mistral ejecutándose:
   ```bash
   ollama run mistral
   ```

2. Desde la carpeta raíz del proyecto, ejecuta:
   ```bash
   python titanic/titanic.py
   ```

3. Los datos descargados se guardarán en `titanic/data/`

## Salida Esperada
El crew generará:
- Dataset descargado: `titanic/data/titanic.csv`
- Dataset limpio: `titanic/data/titanic_cleaned.csv`
- Análisis estadístico con:
  - Distribución de supervivencia
  - Estadísticas por género y clase de pasajero
  - Grupos de edad y tasas de supervivencia

## Conceptos Aprendidos
- Creación de agentes con Autogen
- Definición y uso de herramientas personalizadas
- Coordinación de tareas entre múltiples agentes
- Procesamiento de datos con pandas
- Análisis estadístico básico
