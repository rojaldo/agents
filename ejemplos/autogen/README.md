# Ejemplos AutoGen - Módulos 6-11

Colección completa de ejemplos de código funcionales para los módulos 6-11 del curso de AutoGen. Todos los ejemplos están diseñados para funcionar con **Ollama** como proveedor local de LLM.

## 📋 Requisitos Previos

### Obligatorio: Ollama
1. **Instalar Ollama**: https://ollama.ai
2. **Ejecutar servidor**: `ollama serve`
3. **Descargar modelo**: `ollama pull mistral` (u otro modelo)

### Python
- Python 3.8+
- Librerías: `requests` (instalado automáticamente en la mayoría de entornos)

```bash
pip install requests
```

## 📁 Estructura de Directorios

```
ejemplos/autogen/
├── modulo_6/          # Optimización y Costos
│   ├── 01_token_manager.py
│   ├── 02_prompt_optimizer.py
│   ├── 03_ollama_integration.py
│   ├── 04_cache_manager.py
│   ├── 05_semantic_cache.py
│   ├── 06_advanced_ollama_models.py
│   ├── 07_realtime_monitor.py
│   └── 08_cost_optimizer.py
│
├── modulo_7/          # Casos de Uso Prácticos
│   ├── 01_code_generator.py
│   ├── 02_code_reviewer.py
│   ├── 03_programming_team.py
│   └── 04_data_analyzer.py
│
├── modulo_8/          # Testing y Debugging
│   └── 01_unit_test_generator.py
│
├── modulo_9/          # Despliegue en Producción
│   └── 01_production_deployment.py
│
├── modulo_10/         # Integraciones
│   └── 01_framework_integration.py
│
├── modulo_11/         # Proyecto Final
│   └── 01_final_project.py
│
└── run_all_examples.py  # Script para ejecutar todos los ejemplos
```

## 🚀 Guía de Ejecución

### Opción 1: Ejecutar un ejemplo específico

```bash
# Ejemplo: Ejecutar Token Manager
cd modulo_6
python 01_token_manager.py

# Ejemplo: Ejecutar Code Generator con Ollama
cd modulo_7
python 01_code_generator.py
```

### Opción 2: Ejecutar todos los ejemplos

```bash
# Desde el directorio raíz ejemplos/autogen/
python run_all_examples.py
```

Este script:
- Verifica disponibilidad de Ollama
- Ejecuta todos los ejemplos secuencialmente
- Genera reporte de resultados en `execution_results.json`
- Muestra estadísticas de éxito/fallo

### Opción 3: Con variables de entorno

```bash
# Especificar URL de Ollama
export OLLAMA_URL="http://localhost:11434"

# Especificar modelo
export OLLAMA_MODEL="mistral"

# Especificar ambiente
export ENVIRONMENT="production"

python 01_token_manager.py
```

## 📚 Descripción de Módulos

### Módulo 6: Optimización y Costos

Enfoque en reducir costos y optimizar el uso de recursos:

| Ejemplo | Descripción |
|---------|-------------|
| `01_token_manager.py` | Gestión básica de tokens y cálculo de costos |
| `02_prompt_optimizer.py` | Optimización de prompts para reducir tokens |
| `03_ollama_integration.py` | Cliente avanzado de Ollama con fallback |
| `04_cache_manager.py` | Caché en memoria con estadísticas |
| `05_semantic_cache.py` | Caché inteligente con búsqueda de similitud |
| `06_advanced_ollama_models.py` | Gestor de múltiples modelos Ollama |
| `07_realtime_monitor.py` | Monitoreo en tiempo real de tokens |
| `08_cost_optimizer.py` | Optimización de costos con estrategia de caché |

**Conceptos Clave:**
- Estimación de tokens
- Control de presupuesto
- Caché para reutilización
- Selección automática de modelos
- Monitoreo de costos

### Módulo 7: Casos de Uso Prácticos

Aplicaciones reales de AutoGen:

| Ejemplo | Descripción |
|---------|-------------|
| `01_code_generator.py` | Generación automática de código |
| `02_code_reviewer.py` | Análisis y revisión de código |
| `03_programming_team.py` | Sistema colaborativo de desarrollo |
| `04_data_analyzer.py` | Análisis automático de datasets |

**Conceptos Clave:**
- Generación de código
- Revisión automática
- Análisis de datos
- Trabajo colaborativo entre agentes

### Módulo 8: Testing y Debugging

Automatización de testing y debugging:

| Ejemplo | Descripción |
|---------|-------------|
| `01_unit_test_generator.py` | Generación automática de tests unitarios |

**Conceptos Clave:**
- Generación de tests
- Cobertura de código
- Debugging colaborativo
- Análisis de errores

### Módulo 9: Despliegue en Producción

Configuración y despliegue en producción:

| Ejemplo | Descripción |
|---------|-------------|
| `01_production_deployment.py` | Configuración multiambiente para producción |

**Conceptos Clave:**
- Configuración por ambiente
- Health checks
- Rate limiting
- Seguridad en producción

### Módulo 10: Integraciones

Integración con otros frameworks y servicios:

| Ejemplo | Descripción |
|---------|-------------|
| `01_framework_integration.py` | Integración con LangChain y otros frameworks |

**Conceptos Clave:**
- Integración con frameworks
- API Gateway
- Chain of prompts
- Cadenas de razonamiento

### Módulo 11: Proyecto Final

Sistema completo integrando todos los conceptos:

| Ejemplo | Descripción |
|---------|-------------|
| `01_final_project.py` | Sistema de análisis de código completo |

**Conceptos Clave:**
- Proyecto integral
- Múltiples agentes
- Flujos complejos
- Reportes y métricas

## ⚙️ Configuración de Ollama

### Instalación

```bash
# macOS
brew install ollama

# Linux
curl https://ollama.ai/install.sh | sh

# Windows
# Descargar desde https://ollama.ai/download

```

### Ejecutar servidor

```bash
ollama serve

# En otra terminal, descargar un modelo
ollama pull mistral
```

### Modelos recomendados

- **mistral**: Rápido, buena calidad (2.2 GB)
- **llama2**: Muy potente pero lento (3.8 GB)
- **neural-chat**: Muy rápido pero menor calidad (1.3 GB)

## 🔍 Verificar disponibilidad de Ollama

```bash
# Comprobar que Ollama está ejecutándose
curl http://localhost:11434/api/tags

# Debería devolver algo como:
# {"models":[{"name":"mistral:latest",...}]}
```

## 📊 Resultados de Ejecución

Después de ejecutar `run_all_examples.py`, se genera un archivo `execution_results.json`:

```json
{
  "total": 15,
  "successful": 14,
  "failed": 1,
  "modules": {
    "modulo_6": {
      "total": 8,
      "successful": 8,
      "failed": 0
    },
    ...
  },
  "timestamp": "2024-11-08T10:30:00"
}
```

## 🐛 Solución de Problemas

### Error: "No se puede conectar a Ollama"

**Problema**: Ollama no está ejecutándose o no está en `http://localhost:11434`

**Solución**:
```bash
# Terminal 1: Ejecutar Ollama
ollama serve

# Terminal 2: Ejecutar el ejemplo
python ejemplo.py

# O especificar URL diferente
export OLLAMA_URL="http://192.168.1.100:11434"
```

### Error: "Model not found"

**Problema**: El modelo no está descargado

**Solución**:
```bash
# Descargar el modelo
ollama pull mistral

# Listar modelos disponibles
ollama list
```

### Error: "Timeout"

**Problema**: Ollama tarda demasiado en responder

**Solución**:
- Usar un modelo más pequeño (neural-chat)
- Aumentar timeout en el código
- Verificar recursos de máquina

### Error: "CUDA out of memory"

**Problema**: GPU sin suficiente memoria

**Solución**:
```bash
# Ejecutar solo en CPU
CUDA_VISIBLE_DEVICES="" ollama serve

# O usar modelo más pequeño
ollama pull neural-chat
```

## 📝 Ejemplos de Uso

### Ejecutar un ejemplo simple

```bash
# 1. Asegúrate que Ollama está ejecutándose
ollama serve

# 2. En otra terminal, ejecuta el ejemplo
python modulo_6/01_token_manager.py
```

### Ejecutar con configuración personalizada

```python
# En el código
from modulo_6.codigo_ejemplo import ClienteOllama

client = ClienteOllama(
    base_url="http://mi-servidor:11434",
    model="llama2"
)
```

### Procesar múltiples ejemplos

```bash
#!/bin/bash

for modulo in modulo_6 modulo_7 modulo_8; do
    echo "Procesando $modulo..."
    cd $modulo
    for ejemplo in *.py; do
        echo "  - Ejecutando $ejemplo"
        python $ejemplo
    done
    cd ..
done
```

## 📈 Métricas y Monitoreo

### Monitorear rendimiento

```python
# Los ejemplos incluyen estadísticas automáticas:
manager = TokenManager()
# ... uso del manager ...
manager.print_summary()  # Muestra estadísticas

# Salida típica:
# ==================================================
# RESUMEN DE TOKENS Y COSTOS
# ==================================================
# Modelo: mistral
# Total de tokens usados: 450
# Total de costo: $0.0045
# ...
```

## 🔗 Referencias

- **AutoGen**: https://microsoft.github.io/autogen/
- **Ollama**: https://ollama.ai/
- **Mistral AI**: https://mistral.ai/
- **Documentación completa**: Ver `/home/rojaldo/cursos/agents/autogen.adoc`

## 📞 Soporte

Si encuentras problemas:

1. Verifica que Ollama está ejecutándose
2. Comprueba que tienes el modelo descargado
3. Revisa los logs del servidor Ollama
4. Intenta con otro modelo más simple

## 📄 Licencia

Ejemplos educativos para el curso de AutoGen.

---

**Última actualización**: 8 de Noviembre de 2024
**Estado**: ✅ Completo - Todos los módulos 6-11 incluidos
