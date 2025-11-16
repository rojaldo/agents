"""
Módulo 9: Troubleshooting
Ejemplo 1: Diagnóstico y solución de problemas comunes
"""

import json
from datetime import datetime


class TroubleshootingGuide:
    """Guía completa de troubleshooting para CrewAI"""

    def __init__(self):
        self.problems = []
        self.solutions = []

    def problem_1_tool_selection(self):
        """Problema 1: Agente no selecciona la herramienta correcta"""
        print("\n" + "="*70)
        print("PROBLEMA 1: AGENTE NO SELECCIONA HERRAMIENTA CORRECTA")
        print("="*70)

        print("\n❌ PROBLEMA:")
        print("-" * 50)
        print("""
@tool
def search_web(query):
    \"\"\"Busca en la web\"\"\"  # Descripción muy vaga
    pass

# El agente no sabe cuándo usar esta herramienta
        """)

        print("\n✓ SOLUCIÓN:")
        print("-" * 50)
        print("""
@tool
def search_web(query: str) -> str:
    \"\"\"
    Busca información en internet usando Serper API.

    Útil para:
    - Investigación de mercado
    - Búsqueda de tendencias
    - Obtener información actualizada (últimas 24h)
    - Comparar precios de productos

    Retorna: Resultados relevantes con URLs y descripciones.
    \"\"\"
    # Implementación
    pass
        """)

        problem_data = {
            "problem": "Herramienta mal descrita",
            "root_cause": "Descripción vaga y sin contexto",
            "impact": "Agente no usa herramientas correctas",
            "solution": "Descripción clara con casos de uso"
        }

        self.problems.append(problem_data)
        return problem_data

    def problem_2_slow_execution(self):
        """Problema 2: Tareas que tardan demasiado"""
        print("\n" + "="*70)
        print("PROBLEMA 2: TAREAS QUE TARDAN DEMASIADO")
        print("="*70)

        print("\n❌ PROBLEMA:")
        print("-" * 50)
        print("""
task = Task(
    description="Analiza todo el internet sobre IA",
    expected_output="Análisis completo",
    agent=analyst
)

# Demasiado amplio - el agente intenta analizar demasiada información
        """)

        print("\n✓ SOLUCIÓN:")
        print("-" * 50)
        print("""
task = Task(
    description=\"\"\"
Analiza las 10 noticias más recientes sobre IA en los últimos 7 días.
Enfócate en:
1. Regulación y políticas
2. Avances tecnológicos
3. Adopción empresarial

Límite: máximo 20 minutos de búsqueda.
    \"\"\",
    expected_output="Resumen de 3-5 párrafos",
    agent=analyst
)

# Específico, acotado y con límites claros
        """)

        print("\nOtras estrategias:")
        strategies = [
            ("max_iterations", "Limitar intentos del agente: max_iterations=3"),
            ("timeout", "Establecer timeout: timeout_seconds=120"),
            ("streaming", "Usar streaming de resultados parciales"),
            ("async", "Ejecutar crews en paralelo con async/await")
        ]

        for strategy, description in strategies:
            print(f"  • {strategy}: {description}")

        problem_data = {
            "problem": "Tareas muy amplias",
            "root_cause": "Scope no definido",
            "impact": "Lentitud excesiva",
            "solutions": [
                "Ser específico y limitado",
                "Limitar iteraciones",
                "Establecer timeouts",
                "Usar streaming"
            ]
        }

        self.problems.append(problem_data)
        return problem_data

    def problem_3_output_format(self):
        """Problema 3: Output sin formato esperado"""
        print("\n" + "="*70)
        print("PROBLEMA 3: OUTPUT SIN FORMATO ESPERADO")
        print("="*70)

        print("\n❌ PROBLEMA:")
        print("-" * 50)
        print("""
task = Task(
    description="Analiza datos",
    expected_output="Reporte",
    agent=analyst
)

# Expected output muy vago - el agente puede devolver cualquier cosa
        """)

        print("\n✓ SOLUCIÓN:")
        print("-" * 50)
        print("""
task = Task(
    description="Analiza el dataset ventas_2024.csv",
    expected_output=\"\"\"
JSON Estruturado:
{
    "summary": "Resumen de 1 párrafo",
    "key_findings": ["finding1", "finding2", "finding3"],
    "statistics": {
        "total_sales": 0,
        "average_sale": 0,
        "growth_rate": 0
    },
    "recommendations": ["rec1", "rec2"],
    "confidence_score": 0-100
}\"\"\",
    agent=analyst
)

# Especifica exactamente el formato esperado
        """)

        print("\nValidación de formato:")
        print("""
def validate_json_output(output: str) -> bool:
    try:
        data = json.loads(output)
        required_keys = ["summary", "key_findings", "recommendations"]
        return all(key in data for key in required_keys)
    except json.JSONDecodeError:
        return False
        """)

        problem_data = {
            "problem": "Output con formato incorrecto",
            "root_cause": "Expected output mal definido",
            "impact": "Procesamiento de downstream falla",
            "solution": "Especificar exactamente el formato (JSON, markdown, etc)"
        }

        self.problems.append(problem_data)
        return problem_data

    def problem_4_memory_issues(self):
        """Problema 4: Problemas de memoria y contexto"""
        print("\n" + "="*70)
        print("PROBLEMA 4: PROBLEMAS DE MEMORIA Y CONTEXTO")
        print("="*70)

        print("\n❌ PROBLEMA:")
        print("-" * 50)
        print("""
agent = Agent(
    role="Investigador",
    goal="...",
    backstory="...",
    memory=False  # Sin memoria
)

# El agente no recuerda información de tareas anteriores
        """)

        print("\n✓ SOLUCIÓN:")
        print("-" * 50)
        print("""
agent = Agent(
    role="Investigador",
    goal="...",
    backstory="...",
    memory=True,  # Habilita memoria corta plazo
    long_term_memory=True  # Memoria persistente
)

# Acceder a memoria
context = agent.memory.get_memory()
agent.memory.save_memory(key="tendencies", value=data)
        """)

        print("\nTipos de memoria en CrewAI:")
        memory_types = [
            ("Short-term", "Conversación actual", "Se pierde al terminar"),
            ("Long-term", "Entre sesiones", "Se persiste"),
            ("Entity", "Información sobre entidades", "Reutilizable"),
            ("Context", "Contexto general", "Compartido entre agentes")
        ]

        for mem_type, description, behavior in memory_types:
            print(f"\n  {mem_type}:")
            print(f"    • Descripción: {description}")
            print(f"    • Comportamiento: {behavior}")

        return {"memory_enabled": True, "types": memory_types}

    def problem_5_dependency_errors(self):
        """Problema 5: Errores en dependencias entre tareas"""
        print("\n" + "="*70)
        print("PROBLEMA 5: ERRORES EN DEPENDENCIAS")
        print("="*70)

        print("\n❌ PROBLEMA:")
        print("-" * 50)
        print("""
task1 = Task(description="Tarea 1", agent=agent1)
task2 = Task(
    description="Tarea 2",
    agent=agent2,
    depends_on=[task1]
)
task3 = Task(
    description="Tarea 3",
    agent=agent3,
    depends_on=[task2]
)

# Task3 espera a Task2, pero Task2 falla
# → Task3 nunca se ejecuta (error cascada)
        """)

        print("\n✓ SOLUCIÓN:")
        print("-" * 50)
        print("""
# Opción 1: Manejo de errores explícito
task1 = Task(
    description="Tarea 1",
    agent=agent1,
    on_error_callback=handle_error_task1
)

# Opción 2: Tareas independientes paralelas
task2a = Task(description="Tarea 2a", agent=agent2)
task2b = Task(description="Tarea 2b", agent=agent3)
# Ambas dependen de task1, pero son independientes entre sí

# Opción 3: Validar resultados
def validate_task_output(output):
    if not output or len(output) < 10:
        raise ValueError("Output insuficiente")
    return True

task = Task(
    description="...",
    agent=agent,
    callback=lambda x: validate_task_output(x)
)
        """)

        return {
            "problem": "Fallo en cadena de dependencias",
            "solutions": [
                "Manejo de errores explícito",
                "Validación de outputs",
                "Pasos independientes cuando sea posible"
            ]
        }

    def demonstrate_debugging_techniques(self):
        """Demostrar técnicas de debugging avanzado"""
        print("\n" + "="*70)
        print("TÉCNICAS DE DEBUGGING AVANZADO")
        print("="*70)

        techniques = [
            {
                "technique": "1. Aumentar verbosidad",
                "code": """
crew = Crew(
    agents=agents,
    tasks=tasks,
    verbose=True,      # Mostrar cada paso
    log_file="debug.log"
)
"""
            },
            {
                "technique": "2. Ejecutar tasks independientemente",
                "code": """
result = task1.execute()
print(f"Task 1 output: {result}")
# Útil para aislar problemas
"""
            },
            {
                "technique": "3. Verificar agent memory",
                "code": """
memory_dump = agent.memory.get_memory()
print(json.dumps(memory_dump, indent=2))
"""
            },
            {
                "technique": "4. Probar herramientas aisladamente",
                "code": """
result = search_tool.execute("test query")
print(result)
# Validar que herramientas funcionan correctamente
"""
            },
            {
                "technique": "5. Usar try-except comprehensivo",
                "code": """
try:
    result = crew.kickoff()
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
"""
            }
        ]

        for item in techniques:
            print(f"\n{item['technique']}")
            print(item['code'])

        return techniques

    def print_checklist(self):
        """Imprimir checklist de troubleshooting"""
        print("\n" + "="*70)
        print("CHECKLIST DE TROUBLESHOOTING")
        print("="*70)

        checklist = [
            ("□", "Verificar que todas las API keys estén configuradas"),
            ("□", "Revisar descripciones de herramientas"),
            ("□", "Validar especificación de expected_output"),
            ("□", "Verificar dependencias entre tareas"),
            ("□", "Revisar logs de ejecución"),
            ("□", "Probar herramientas aisladamente"),
            ("□", "Aumentar verbosidad de logs"),
            ("□", "Validar formato de inputs/outputs"),
            ("□", "Verificar límites de iteraciones"),
            ("□", "Revisar uso de memoria"),
        ]

        print("\nAnte un problema:")
        for checkbox, item in checklist:
            print(f"  {checkbox} {item}")

        print("\n" + "="*70 + "\n")


def main():
    """Demostración completa de troubleshooting"""
    print("="*70)
    print(" MÓDULO 9: TROUBLESHOOTING Y DEBUGGING")
    print("="*70)

    guide = TroubleshootingGuide()

    # Mostrar problemas comunes y soluciones
    guide.problem_1_tool_selection()
    guide.problem_2_slow_execution()
    guide.problem_3_output_format()
    guide.problem_4_memory_issues()
    guide.problem_5_dependency_errors()

    # Técnicas de debugging
    guide.demonstrate_debugging_techniques()

    # Checklist
    guide.print_checklist()


if __name__ == "__main__":
    main()
