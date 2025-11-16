# CrewAI - Curso Completo de Agentes Inteligentes

## 📚 Descripción General

Este directorio contiene ejemplos funcionales y documentación completa del framework **CrewAI**. Incluye 10 módulos progresivos que cubren desde conceptos fundamentales hasta un proyecto final completo de análisis de tendencias.

## 📁 Estructura del Proyecto

```
ejemplos/crewai/
├── README.md                          # Este archivo
├── run_all_examples.py               # Script maestro para ejecutar todos los ejemplos
├── crewai.adoc                       # Documentación completa (en raíz)
├── modulo_1/
│   └── 01_hello_crewai.py            # Introducción: Agentes, tareas y crews básicos
├── modulo_2/
│   └── 01_basic_agents.py            # Conceptos: Agentes con roles específicos
├── modulo_3/
│   └── 01_tools.py                   # Herramientas: Crear e integrar tools
├── modulo_4/
│   └── 01_yaml_config.py             # Configuración: Usar YAML para config
├── modulo_5/
│   └── 01_use_cases.py               # Casos prácticos: Market research pipeline
├── modulo_6/
│   └── 01_monitoring.py              # Monitoreo: Logging y debugging
├── modulo_7/
│   └── 01_best_practices.py          # Mejores prácticas: Patrones de diseño
├── modulo_8/
│   └── 01_scalability.py             # Escalabilidad: Multi-crew coordination
├── modulo_9/
│   └── 01_troubleshooting.py         # Troubleshooting: Diagnóstico de problemas
├── modulo_10/
│   └── 01_final_project.py           # Proyecto final: Sistema completo
└── output/
    └── (Resultados y reportes generados)
```

## 🚀 Quick Start

### Requisitos Previos

```bash
# Python 3.8+
python --version

# Crear entorno virtual
python -m venv crewai_env

# Activar entorno (Linux/macOS)
source crewai_env/bin/activate

# Activar entorno (Windows)
crewai_env\Scripts\activate
```

### Instalación

```bash
# Sin dependencias externas (los ejemplos usan simulaciones)
python modulo_1/01_hello_crewai.py

# Para usar CrewAI real (opcional)
pip install crewai crewai-tools
```

### Ejecutar Ejemplos Individuales

```bash
# Módulo 1: Introducción
python modulo_1/01_hello_crewai.py

# Módulo 2: Agentes básicos
python modulo_2/01_basic_agents.py

# Módulo 3: Herramientas
python modulo_3/01_tools.py

# ... y así sucesivamente
```

### Ejecutar Todos los Ejemplos

```bash
# Script maestro que ejecuta todos los módulos y genera reporte
python run_all_examples.py
```

Esto generará un archivo `execution_results.json` con los resultados de todas las pruebas.

## 📖 Contenido de Módulos

### Módulo 1: Introducción a CrewAI
**Archivo:** `modulo_1/01_hello_crewai.py`

Introduces conceptos básicos:
- **SimpleAgent**: Agentes con roles y goals
- **SimpleCrew**: Coordinación de múltiples agentes
- **Tareas secuenciales**: Flujo de trabajo simple

**Concepto clave:** CrewAI es un framework para orquestar "equipos" de agentes.

```bash
python modulo_1/01_hello_crewai.py
```

### Módulo 2: Conceptos Fundamentales
**Archivo:** `modulo_2/01_basic_agents.py`

Profundiza en conceptos:
- **Agent**: Estructura con role, goal, backstory
- **Task**: Unidades de trabajo asignadas a agentes
- **Think and Act**: Agentes razonan y actúan
- **Interactions**: Registro de interacciones

```bash
python modulo_2/01_basic_agents.py
```

### Módulo 3: Herramientas (Tools)
**Archivo:** `modulo_3/01_tools.py`

Demuestra creación de herramientas:
- **Tool base class**: Abstracción para herramientas
- **CalculatorTool**: Herramienta para operaciones matemáticas
- **DataAnalyzerTool**: Análisis estadístico
- **ToolBox**: Registro y gestión de herramientas

```bash
python modulo_3/01_tools.py
```

### Módulo 4: Configuración Avanzada
**Archivo:** `modulo_4/01_yaml_config.py`

Configuración declarativa:
- **Agentes en YAML**: Definición declarativa
- **Tareas en YAML**: Especificación de tareas
- **Dependencias**: Gestión de orden de ejecución
- **Validación**: Verificación de configuración

```bash
python modulo_4/01_yaml_config.py
```

### Módulo 5: Casos de Uso Prácticos
**Archivo:** `modulo_5/01_use_cases.py`

Proyecto realista:
- **ResearchCrew**: Investigación de mercado
- **Fases**: Research → Analysis → Reporting
- **Pipeline**: Flujo de datos entre agentes

```bash
python modulo_5/01_use_cases.py
```

### Módulo 6: Monitoreo y Debugging
**Archivo:** `modulo_6/01_monitoring.py`

Observabilidad y debugging:
- **CrewLogger**: Sistema de logging personalizado
- **Eventos**: task_start, task_end, tool_usage, errors
- **Exportación**: Guardar logs en JSON
- **Reportes**: Resumen de ejecución

```bash
python modulo_6/01_monitoring.py
```

### Módulo 7: Mejores Prácticas
**Archivo:** `modulo_7/01_best_practices.py`

Patrones de diseño:
- **Diseño de agentes**: Roles específicos y goals medibles
- **Estructuración de tareas**: Descripciones claras
- **Dependencias**: Orden lógico de ejecución
- **Optimización de costos**: Reducir uso de APIs

```bash
python modulo_7/01_best_practices.py
```

### Módulo 8: Escalabilidad y Arquitectura
**Archivo:** `modulo_8/01_scalability.py`

Arquitecturas complejas:
- **Multi-crew coordination**: Múltiples crews trabajando juntos
- **Comunicación entre crews**: Paso de resultados
- **REST API integration**: Exponer crews como APIs
- **Escalabilidad**: Diseño para crecer

```bash
python modulo_8/01_scalability.py
```

### Módulo 9: Troubleshooting
**Archivo:** `modulo_9/01_troubleshooting.py`

Diagnóstico de problemas:
- **Problema 1**: Herramienta no seleccionada correctamente
- **Problema 2**: Tareas muy lentas
- **Problema 3**: Output en formato incorrecto
- **Problema 4**: Issues de memoria y contexto
- **Problema 5**: Errores en dependencias
- **Técnicas de debugging**: Verbosidad, tests aislados, etc.

```bash
python modulo_9/01_troubleshooting.py
```

### Módulo 10: Proyecto Final
**Archivo:** `modulo_10/01_final_project.py`

Sistema completo de análisis de tendencias:
- **Fase 1**: Investigación multi-fuente
- **Fase 2**: Análisis y extracción de insights
- **Fase 3**: Predicción y forecasting
- **Fase 4**: Generación de reportes ejecutivos
- **Exportación**: Reporte en JSON

```bash
python modulo_10/01_final_project.py
```

## 📊 Resultados Esperados

Al ejecutar todos los ejemplos correctamente:

```
✓ Módulo 1: 3 agentes, 3 tareas completadas
✓ Módulo 2: Rol-based agent execution
✓ Módulo 3: Calculadora y análisis de datos
✓ Módulo 4: 3 agentes + 3 tareas desde YAML
✓ Módulo 5: Pipeline research → analysis → reporting
✓ Módulo 6: Logging y monitoring completo
✓ Módulo 7: Patrones de diseño demostrados
✓ Módulo 8: Multi-crew coordination
✓ Módulo 9: Troubleshooting checklist
✓ Módulo 10: Sistema completo ejecutado

Tasa de éxito: 100%
```

## 🔧 Configuración Personalizada

### Cambiar Modelo LLM

Para usar CrewAI real con OpenAI:

```python
from crewai import Agent

agent = Agent(
    role="Investigador",
    goal="Investigar información",
    backstory="...",
    llm="gpt-4"  # Cambiar modelo
)
```

Para usar Ollama local:

```python
agent = Agent(
    role="Investigador",
    goal="Investigar información",
    backstory="...",
    llm="ollama:mistral"
)
```

### Variables de Entorno

```bash
# Para OpenAI
export OPENAI_API_KEY="sk-..."

# Para otras APIs
export SERPER_API_KEY="..."
export ANTHROPIC_API_KEY="..."
```

## 📚 Recursos Adicionales

### Documentación Completa
- **crewai.adoc**: Documentación detallada (1500+ líneas)
- **Módulos 1-10**: Teoría y código

### Referencias
- [CrewAI GitHub](https://github.com/joaomdmoura/crewai)
- [CrewAI Docs](https://crewai.me)
- [LangChain](https://python.langchain.com)

### Comunidad
- Discord: CrewAI Community
- GitHub Issues: Reportar problemas
- Discussions: Propuestas y preguntas

## 🛠️ Troubleshooting Rápido

### Error: "Módulo no encontrado"
```bash
# Asegurar que estás en el directorio correcto
cd /home/rojaldo/cursos/agents/ejemplos/crewai
python modulo_1/01_hello_crewai.py
```

### Error: "API Key no configurada"
```bash
# Configurar variable de entorno
export OPENAI_API_KEY="tu_clave_aqui"

# O crear .env
echo "OPENAI_API_KEY=tu_clave_aqui" > .env
```

### Error: "Timeout en ejecución"
- Aumentar el timeout en run_all_examples.py
- Ejecutar módulos individualmente
- Verificar conexión a internet

## 📈 Métricas de Aprendizaje

Después de completar este curso puedes:

✅ Entender conceptos de agentes inteligentes
✅ Crear crews de múltiples agentes
✅ Implementar herramientas personalizadas
✅ Diseñar sistemas escalables
✅ Diagnosticar y resolver problemas
✅ Optimizar costos de APIs
✅ Generar reportes automáticos
✅ Integrar con APIs REST

## 📝 Notas Importantes

1. **Los ejemplos no requieren API keys**: Usan simulaciones en lugar de LLMs reales
2. **Totalmente extensible**: Puedes reemplazar simulaciones con CrewAI real
3. **Código limpio**: Incluye best practices y patrones profesionales
4. **Documentado**: Cada ejemplo tiene comentarios explicativos
5. **Escalable**: La arquitectura soporta proyectos complejos

## 🎓 Recomendaciones de Estudio

1. **Semana 1**: Módulos 1-3 (Fundamentos)
2. **Semana 2**: Módulos 4-6 (Conceptos intermedios)
3. **Semana 3**: Módulos 7-9 (Técnicas avanzadas)
4. **Semana 4**: Módulo 10 (Proyecto capstone)

## 📞 Soporte

Para preguntas o problemas:
1. Revisar el módulo 9 (Troubleshooting)
2. Consultar la documentación en crewai.adoc
3. Revisar los logs de ejecución
4. Buscar en la comunidad de CrewAI

## 📜 Licencia

Este material educativo es de código abierto y puede ser usado libremente para propósitos de aprendizaje.

---

**Última actualización:** 2024-11-08
**Versión:** 1.0
**Autor:** Curso de Agentes IA
