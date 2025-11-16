"""
Módulo 4: Configuración Avanzada
Ejemplo 1: Configuración mediante YAML
"""

import yaml
from io import StringIO


class ConfigLoader:
    """Cargador de configuración desde YAML"""

    @staticmethod
    def load_agents_config(yaml_content):
        """Cargar configuración de agentes"""
        return yaml.safe_load(yaml_content)

    @staticmethod
    def load_tasks_config(yaml_content):
        """Cargar configuración de tareas"""
        return yaml.safe_load(yaml_content)

    @staticmethod
    def validate_config(config):
        """Validar estructura de configuración"""
        required_keys = ["role", "goal", "backstory"]
        for key in required_keys:
            if key not in config:
                return False, f"Falta clave requerida: {key}"
        return True, "Configuración válida"


def main():
    """Demostración de configuración con YAML"""
    print("="*70)
    print(" MÓDULO 4: CONFIGURACIÓN MEDIANTE YAML")
    print("="*70)

    # Configuración de agentes en YAML
    agents_yaml = """
researcher:
  role: "Investigador Senior"
  goal: "Recopilar información de alta calidad sobre tópicos específicos"
  backstory: |
    Eres un investigador experimentado con acceso a múltiples fuentes.
    Tu capacidad para encontrar información relevante es excepcional.
  tools:
    - search_tool
    - web_scraper

analyst:
  role: "Analista de Datos"
  goal: "Analizar información y generar insights accionables"
  backstory: |
    Eres un analista con experiencia en transformar datos en decisiones.
  tools:
    - data_analyzer
    - visualization_tool

reporter:
  role: "Reportero"
  goal: "Sintetizar hallazgos en reportes claros"
  backstory: |
    Eres un reportero con capacidad de comunicar información compleja.
  tools:
    - document_writer
"""

    # Configuración de tareas en YAML
    tasks_yaml = """
research_task:
  description: "Investiga el mercado de IA en 2024"
  expected_output: "Reporte comprensivo con 10 tendencias principales"
  agent: "researcher"

analysis_task:
  description: "Analiza los hallazgos de la investigación"
  expected_output: "Análisis con recomendaciones estratégicas"
  agent: "analyst"
  depends_on:
    - research_task

reporting_task:
  description: "Sintetiza todo en un reporte ejecutivo"
  expected_output: "Reporte de 1 página con conclusiones"
  agent: "reporter"
  depends_on:
    - analysis_task
"""

    print("\n📄 Cargando configuración desde YAML...\n")

    # Cargar configuración
    loader = ConfigLoader()

    agents_config = loader.load_agents_config(agents_yaml)
    print(f"✓ {len(agents_config)} agentes cargados:")
    for agent_name in agents_config.keys():
        print(f"   - {agent_name}")

    tasks_config = loader.load_tasks_config(tasks_yaml)
    print(f"\n✓ {len(tasks_config)} tareas cargadas:")
    for task_name in tasks_config.keys():
        print(f"   - {task_name}")

    # Mostrar detalles de agentes
    print("\n" + "="*70)
    print("DETALLES DE AGENTES")
    print("="*70)

    for agent_name, agent_config in agents_config.items():
        print(f"\n{agent_name}:")
        print(f"  Rol: {agent_config['role']}")
        print(f"  Goal: {agent_config['goal']}")
        print(f"  Herramientas: {', '.join(agent_config['tools'])}")

        # Validar
        valid, message = loader.validate_config(agent_config)
        print(f"  Validación: {'✓' if valid else '✗'} {message}")

    # Mostrar detalles de tareas
    print("\n" + "="*70)
    print("DETALLES DE TAREAS")
    print("="*70)

    for task_name, task_config in tasks_config.items():
        print(f"\n{task_name}:")
        print(f"  Descripción: {task_config['description']}")
        print(f"  Agente: {task_config['agent']}")
        print(f"  Output esperado: {task_config['expected_output']}")
        if 'depends_on' in task_config:
            print(f"  Depende de: {task_config['depends_on']}")

    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
