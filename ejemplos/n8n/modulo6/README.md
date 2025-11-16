# MÓDULO 6: Gestión de Datos - Ejemplos Funcionales

Este módulo contiene ejemplos prácticos de lectura, escritura y manipulación de datos en n8n usando Ollama como modelo local de IA.

## Estructura de Ejemplos

### 01-lectura-api-rest.json
- **Concepto**: Lectura de datos desde una API REST
- **Nodos**: HTTP Request → Table (visualización)
- **Uso**: Obtener datos de una API pública (JSONPlaceholder)
- **Aprendizaje**: Configurar requests GET, parsear JSON

### 02-escritura-archivo-json.json
- **Concepto**: Escritura de datos en archivos JSON
- **Nodos**: Manual trigger → Set data → Write file
- **Uso**: Guardar datos en formato JSON
- **Aprendizaje**: Crear estructuras JSON, guardar archivos

### 03-transform-datos.json
- **Concepto**: Transformación de datos con Code Node
- **Nodos**: Read file → Code (transformar) → Write transformed
- **Uso**: Procesar datos con lógica personalizada
- **Aprendizaje**: Usar Code Node para transformaciones complejas

### 04-crud-sqlite.json
- **Concepto**: Operaciones CRUD con SQLite
- **Nodos**: Manual → SQLite (CREATE, READ, UPDATE, DELETE)
- **Uso**: Gestión completa de base de datos SQLite
- **Aprendizaje**: Ejecutar queries SQL, manejar transacciones

### 05-ollama-data-processing.json
- **Concepto**: Procesar datos con Ollama (IA local)
- **Nodos**: Read data → Ollama API → Store results
- **Uso**: Usar IA para clasificar, analizar o generar texto
- **Aprendizaje**: Integrar modelos de IA con flujos de datos

## Requisitos

- n8n instalado
- Ollama instalado y corriendo en `http://localhost:11434`
- SQLite (incluido en n8n)
- curl (para pruebas manuales)

## Cómo Usar

1. Importa los archivos JSON en n8n
2. Configura las credenciales necesarias
3. Ejecuta los workflows paso a paso
4. Observa los datos en cada etapa del flujo

## Conceptos Clave

### Lectura de Datos
- **HTTP GET**: Obtener datos de APIs
- **File Reader**: Leer contenido de archivos
- **Database**: Consultar bases de datos
- **APIs**: Integración con servicios externos

### Escritura de Datos
- **HTTP POST**: Enviar datos a APIs
- **File Writer**: Guardar en archivos
- **Database**: Insertar en bases de datos
- **Transformación**: Convertir formato de datos

### Transformación
- **Code Node**: JavaScript personalizado
- **Function Node**: Expresiones simples
- **Set Node**: Asignar valores
- **Filter**: Seleccionar datos específicos

## Próximos Pasos
- Módulo 7: Webhooks y APIs
- Módulo 8: Casos de uso prácticos
- Módulo 9: Nodos avanzados
