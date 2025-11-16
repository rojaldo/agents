"""
Módulo 4: Capacidades Avanzadas
Ejemplo 1: Code Execution - Ejecución de código con validación
"""

import subprocess
import tempfile
import os
from datetime import datetime


class CodeExecutor:
    """Ejecutor de código seguro"""

    def __init__(self):
        self.execution_history = []
        self.executed_code = []

    def execute_python(self, code):
        """Ejecutar código Python de forma segura"""
        try:
            # Crear archivo temporal
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name

            # Ejecutar código
            result = subprocess.run(
                ['python', temp_file],
                capture_output=True,
                text=True,
                timeout=10
            )

            # Limpiar archivo temporal
            os.unlink(temp_file)

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Timeout: ejecución tardó más de 10 segundos",
                "return_code": -1
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "return_code": -1
            }

    def validate_code(self, code):
        """Validar código Python"""
        try:
            compile(code, '<string>', 'exec')
            return {"valid": True, "message": "Código válido"}
        except SyntaxError as e:
            return {"valid": False, "message": f"Error de sintaxis: {e}"}
        except Exception as e:
            return {"valid": False, "message": f"Error: {e}"}

    def execute_and_log(self, code, description=""):
        """Ejecutar código y registrar en historial"""
        # Validar
        validation = self.validate_code(code)

        if not validation["valid"]:
            return {
                "success": False,
                "validation_error": validation["message"]
            }

        # Ejecutar
        result = self.execute_python(code)

        # Registrar
        self.execution_history.append({
            "timestamp": datetime.now().isoformat(),
            "description": description,
            "code": code,
            "result": result
        })

        self.executed_code.append(code)

        return result

    def get_execution_count(self):
        """Obtener cantidad de ejecuciones"""
        return len(self.execution_history)

    def print_execution_report(self):
        """Imprimir reporte de ejecuciones"""
        print(f"\n{'═'*70}")
        print("REPORTE DE EJECUCIONES")
        print("="*70)

        successful = sum(1 for e in self.execution_history if e['result'].get('success'))
        failed = self.get_execution_count() - successful

        print(f"Total de ejecuciones: {self.get_execution_count()}")
        print(f"Exitosas: {successful}")
        print(f"Fallidas: {failed}")

        if self.execution_history:
            print("\nÚltimas ejecuciones:")
            for i, execution in enumerate(self.execution_history[-3:], 1):
                print(f"\n{i}. {execution['description']}")
                print(f"   Resultado: {'✅ Éxito' if execution['result'].get('success') else '❌ Error'}")
                if execution['result'].get('stdout'):
                    print(f"   Output: {execution['result']['stdout'][:100]}")

        print("="*70 + "\n")


def main():
    """Demostración de ejecución de código"""
    print("="*70)
    print(" MÓDULO 4: EJECUCIÓN DE CÓDIGO")
    print("="*70)

    executor = CodeExecutor()

    # Ejemplo 1: Código simple
    print("\n[Ejemplo 1] Código Simple")
    print("-"*70)

    code1 = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)

print(f"Factorial de 5: {factorial(5)}")
"""

    print("Código:")
    print(code1)
    print("\nEjecutando...")

    result1 = executor.execute_and_log(code1, "Calcular factorial")

    if result1.get('success'):
        print(f"✅ Éxito")
        print(f"Output:\n{result1['stdout']}")
    else:
        print(f"❌ Error: {result1.get('error')}")

    # Ejemplo 2: Operaciones con listas
    print("\n[Ejemplo 2] Operaciones con Listas")
    print("-"*70)

    code2 = """
números = [1, 2, 3, 4, 5]
cuadrados = [n**2 for n in números]
suma = sum(cuadrados)

print(f"Números: {números}")
print(f"Cuadrados: {cuadrados}")
print(f"Suma de cuadrados: {suma}")
"""

    print("Código:")
    print(code2)
    print("\nEjecutando...")

    result2 = executor.execute_and_log(code2, "Operaciones con listas")

    if result2.get('success'):
        print(f"✅ Éxito")
        print(f"Output:\n{result2['stdout']}")
    else:
        print(f"❌ Error: {result2.get('error')}")

    # Ejemplo 3: Manejo de datos
    print("\n[Ejemplo 3] Procesamiento de Datos")
    print("-"*70)

    code3 = """
datos = {'name': 'Python', 'version': 3.11, 'year': 2024}

for key, value in datos.items():
    print(f"{key}: {value}")
"""

    print("Código:")
    print(code3)
    print("\nEjecutando...")

    result3 = executor.execute_and_log(code3, "Procesamiento de diccionarios")

    if result3.get('success'):
        print(f"✅ Éxito")
        print(f"Output:\n{result3['stdout']}")
    else:
        print(f"❌ Error: {result3.get('error')}")

    # Reporte
    executor.print_execution_report()


if __name__ == "__main__":
    main()
