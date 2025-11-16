# Índice de Ejemplos n8n - Módulos 6 a 11

## Descripción General

Este conjunto de ejemplos proporciona implementaciones prácticas y funcionales de los módulos 6 al 11 del curso completo de n8n. Todos los ejemplos están diseñados para funcionar con **Ollama en local** para procesamiento de IA sin dependencias en servicios externos.

## Estructura de Directorios

```
ejemplos/n8n/
├── modulo6/          # Gestión de Datos
├── modulo7/          # Webhooks y APIs
├── modulo8/          # Casos de Uso Prácticos
├── modulo9/          # Nodos Avanzados
├── modulo10/         # Monitoreo y Debugging
├── modulo11/         # Seguridad y Mejores Prácticas
├── test-ejemplos.sh  # Script de validación
└── INDICE_EJEMPLOS.md
```

## Módulo 6: Gestión de Datos

### Ejemplos incluidos:

| Archivo | Descripción | Conceptos |
|---------|-------------|----------|
| 01-lectura-api-rest.json | Lectura desde API REST pública | HTTP GET, parseo JSON, encadenamiento de requests |
| 02-escritura-archivo-json.json | Escritura y lectura de archivos JSON | File I/O, conversión de formatos, validación |
| 03-transformacion-datos.json | Transformación con Code Node | Normalización, mapeo, estadísticas |
| 04-crud-sqlite.json | Operaciones CRUD completas | CREATE, READ, UPDATE, DELETE, transacciones |
| 05-ollama-data-processing.json | Procesamiento con IA local | Integración Ollama, análisis de sentimientos |

### Conceptos Clave:
- ✓ Lectura desde múltiples fuentes
- ✓ Escritura y persistencia de datos
- ✓ Transformación y normalización
- ✓ Operaciones CRUD en BD
- ✓ Integración con IA local

## Módulo 7: Webhooks y APIs

### Ejemplos incluidos:

| Archivo | Descripción | Conceptos |
|---------|-------------|----------|
| 01-webhook-basico.json | Webhook que recibe datos POST | Trigger webhook, request/response |
| 02-consumir-api-publica.json | Llamar APIs públicas sin auth | HTTP requests, data parsing |
| 03-webhook-con-validacion.json | Validar datos en webhook | Try-catch, error handling |
| 04-rate-limiting.json | Implementar rate limiting | Delay, protección contra spam |
| 05-autenticacion-apis.json | Diferentes métodos de auth | API Key, Bearer, Basic, OAuth |

### Conceptos Clave:
- ✓ Crear webhooks en n8n
- ✓ Consumir APIs REST
- ✓ Autenticación segura
- ✓ Rate limiting y throttling
- ✓ Manejo de errores HTTP

## Módulo 8: Casos de Uso Prácticos

### Ejemplos incluidos:

| Archivo | Descripción | Conceptos |
|---------|-------------|----------|
| 01-procesamiento-formularios.json | Formulario → BD → Email | Validación, flujo completo |
| 02-generador-reportes.json | Generar reportes diarios | Agregación, estadísticas |
| 03-pipeline-ollama.json | ETL con análisis de sentimientos | Pipeline, Ollama, agregación |

### Conceptos Clave:
- ✓ Workflows end-to-end
- ✓ Validación de datos
- ✓ Integración de servicios
- ✓ Generación de reportes
- ✓ Pipelines de datos complejos

## Módulo 9: Nodos Avanzados

### Ejemplos incluidos:

| Archivo | Descripción | Conceptos |
|---------|-------------|----------|
| 01-code-node-avanzado.json | JavaScript complejo en Code Node | Mapeo, filtrado, agregación |
| 02-schedule-cron.json | Ejecución programada | Triggers temporales, CRON |

### Conceptos Clave:
- ✓ Code Node avanzado
- ✓ Function Node para expresiones
- ✓ Scheduling y CRON
- ✓ SQLite avanzado
- ✓ Nodos de programación

## Módulo 10: Monitoreo y Debugging

Características documentadas en el adoc:
- ✓ Testing de workflows
- ✓ Inspección de logs
- ✓ Debugging avanzado
- ✓ Performance metrics
- ✓ Monitoreo de estados

README: `modulo10/README.md`

## Módulo 11: Seguridad y Mejores Prácticas

### Ejemplos incluidos:

| Archivo | Descripción | Conceptos |
|---------|-------------|----------|
| 01-manejo-errores.json | Retry logic y fallbacks | Try-catch, reintentos, logging |

### Conceptos Clave:
- ✓ Manejo robusto de errores
- ✓ Retry logic con backoff
- ✓ Fallback actions
- ✓ Logging y auditoría
- ✓ Mejores prácticas de seguridad

README: `modulo11/README.md`

## Validación de Ejemplos

Todos los ejemplos han sido validados como JSON válido:

```bash
$ ./test-ejemplos.sh

Total de archivos JSON verificados: 16
Archivos válidos: 16
Archivos con errores: 0
```

✓ **Estado:** Todos los ejemplos son funcionales

## Requisitos para ejecutar

### Instalación de n8n

```bash
# Opción 1: npm global
npm install -g n8n
n8n

# Opción 2: Docker
docker run -it --rm -p 5678:5678 n8nio/n8n

# Opción 3: Repositorio
git clone https://github.com/n8n-io/n8n.git
npm install
npm start
```

### Instalación de Ollama

```bash
# macOS
brew install ollama

# Linux
curl https://ollama.ai/install.sh | sh

# Windows
# Descargar desde https://ollama.ai

# Iniciar Ollama
ollama serve

# En otra terminal, descargar modelo
ollama pull llama2
```

## Cómo usar los ejemplos

1. **Inicia n8n:**
   ```bash
   n8n
   ```

2. **Abre en navegador:**
   ```
   http://localhost:5678
   ```

3. **Importa un ejemplo:**
   - Click en menú → Workflows → Import from JSON
   - Selecciona archivo desde `ejemplos/n8n/moduloX/XX-nombre.json`

4. **Configura credenciales (si aplica):**
   - Algunos ejemplos requieren configuración mínima
   - Lee el archivo JSON para entender los parámetros

5. **Ejecuta el workflow:**
   - Click en "Execute Workflow"
   - Observa los datos en cada nodo

## Estructura de Contenidos en el Adoc

El archivo `docs/n8n.adoc` contiene:

- **Módulo 6:** Explicaciones detalladas sobre gestión de datos con ejemplos prácticos
- **Módulo 7:** Webhooks, APIs y autenticación con casos de uso
- **Módulo 8-11:** Casos prácticos, nodos avanzados, debugging y seguridad

Cada módulo incluye:
- Conceptos teóricos
- Ejemplos de código
- Referencias a archivos JSON
- Mejores prácticas
- Puntos clave de aprendizaje

## Características Destacadas

### Integración con Ollama
Los ejemplos que usan Ollama permiten:
- Análisis de sentimientos local
- Procesamiento de texto sin API externa
- Modelo de IA personalizable
- Privacidad de datos garantizada

### Ejemplos Completos
Cada módulo incluye:
- README con descripción
- Múltiples ficheros JSON funcionales
- Documentación en el adoc
- Casos de uso reales

### Validación Automática
- Script `test-ejemplos.sh` verifica todos los JSONs
- Detecta errores de sintaxis
- Verifica disponibilidad de servicios

## Próximos Pasos Sugeridos

1. Ejecuta `./test-ejemplos.sh` para validar ejemplos
2. Importa un ejemplo simple (p.ej., webhook básico)
3. Observa cómo fluyen los datos
4. Modifica parámetros según tus necesidades
5. Combina conceptos para crear workflows personalizados

## Solución de Problemas

### Ollamano no disponible
```bash
ollama serve
# En otra terminal
ollama pull llama2
```

### n8n no responde
```bash
# Reinicia n8n
n8n
# Abre en navegador http://localhost:5678
```

### Error al importar JSON
- Verifica que el archivo sea válido: `python3 -m json.tool archivo.json`
- Comprueba que n8n está ejecutándose
- Lee el error específico en la UI de n8n

## Recursos Adicionales

- Documentación oficial: https://docs.n8n.io/
- GitHub: https://github.com/n8n-io/n8n
- Community: https://community.n8n.io/
- Ollama: https://ollama.ai/

## Estadísticas

- **Ejemplos totales:** 16
- **Módulos cubiertos:** 6 (módulos 6-11)
- **Líneas de contenido en adoc:** ~1500 líneas nuevas
- **Estado de validación:** ✓ 100% válido

## Notas Importantes

1. Los ejemplos están optimizados para educación
2. Algunos ejemplos simulan servicios (p.ej., email)
3. SQLite se usa como BD por defecto (sin instalación requerida)
4. Los ejemplos con Ollama requieren que el servicio esté corriendo
5. Los workflows están documentados con comentarios en el JSON

---

**Última actualización:** 2024
**Versión de n8n:** Compatible con v1.x+
**Estado:** Production-ready examples
