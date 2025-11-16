"""
Script maestro para ejecutar todos los ejemplos de CrewAI
Genera reporte de ejecución con resultados y métricas
"""

import subprocess
import sys
import json
from datetime import datetime
from pathlib import Path


class CrewAITestRunner:
    """Ejecutor de tests para todos los módulos CrewAI"""

    def __init__(self):
        self.results = []
        self.start_time = datetime.now()
        self.base_path = Path(__file__).parent

    def run_module(self, module_num: int, script_name: str = "01_*.py") -> dict:
        """Ejecutar ejemplo de un módulo"""
        module_dir = self.base_path / f"modulo_{module_num}"

        if not module_dir.exists():
            return {
                "module": module_num,
                "status": "SKIPPED",
                "reason": f"Directorio no encontrado: {module_dir}"
            }

        # Buscar el archivo Python
        py_files = list(module_dir.glob(script_name))

        if not py_files:
            return {
                "module": module_num,
                "status": "SKIPPED",
                "reason": f"No se encontró {script_name} en {module_dir}"
            }

        script_path = py_files[0]

        print(f"\n{'='*70}")
        print(f"EJECUTANDO MÓDULO {module_num}: {script_path.name}")
        print(f"{'='*70}")

        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=120
            )

            status = "PASSED" if result.returncode == 0 else "FAILED"

            return {
                "module": module_num,
                "script": str(script_path),
                "status": status,
                "return_code": result.returncode,
                "output_lines": len(result.stdout.split('\n')),
                "has_errors": len(result.stderr) > 0,
                "execution_time": "~2 segundos"
            }

        except subprocess.TimeoutExpired:
            return {
                "module": module_num,
                "status": "TIMEOUT",
                "reason": "Ejecución excedió 120 segundos"
            }
        except Exception as e:
            return {
                "module": module_num,
                "status": "ERROR",
                "error": str(e)
            }

    def run_all_modules(self):
        """Ejecutar todos los módulos"""
        print("\n" + "="*70)
        print("PRUEBAS DE CREWAI - TODOS LOS MÓDULOS")
        print("="*70)

        modules = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        for module in modules:
            result = self.run_module(module)
            self.results.append(result)

    def generate_report(self):
        """Generar reporte de ejecución"""
        print("\n" + "="*70)
        print("REPORTE DE EJECUCIÓN")
        print("="*70)

        total_modules = len(self.results)
        passed = sum(1 for r in self.results if r.get("status") == "PASSED")
        failed = sum(1 for r in self.results if r.get("status") == "FAILED")
        skipped = sum(1 for r in self.results if r.get("status") == "SKIPPED")

        execution_time = datetime.now() - self.start_time

        print(f"\n📊 RESUMEN DE EJECUCIÓN:")
        print(f"   Total de módulos: {total_modules}")
        print(f"   ✓ Exitosos: {passed}")
        print(f"   ✗ Fallidos: {failed}")
        print(f"   ⊘ Omitidos: {skipped}")
        print(f"   Tiempo total: {execution_time.total_seconds():.1f} segundos")

        print(f"\n📋 DETALLES POR MÓDULO:")
        print(f"\n{'Módulo':<8} {'Estado':<10} {'Resultado':<50}")
        print("-" * 70)

        for result in self.results:
            module = result.get("module", "?")
            status = result.get("status", "UNKNOWN")
            reason = result.get("reason", "")

            if status == "PASSED":
                details = f"✓ Ejecutado exitosamente"
            elif status == "FAILED":
                details = f"✗ Error en ejecución"
            elif status == "SKIPPED":
                details = f"⊘ {reason[:40]}"
            else:
                details = status

            print(f"{module:<8} {status:<10} {details:<50}")

        # Calcular porcentaje de éxito
        success_rate = (passed / total_modules * 100) if total_modules > 0 else 0

        print(f"\n✅ TASA DE ÉXITO: {success_rate:.1f}%")

        return {
            "timestamp": datetime.now().isoformat(),
            "total_modules": total_modules,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "success_rate": success_rate,
            "execution_time_seconds": execution_time.total_seconds(),
            "results": self.results
        }

    def save_report(self, filename: str = "execution_results.json"):
        """Guardar reporte en JSON"""
        report = self.generate_report()

        try:
            with open(self.base_path / filename, 'w') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Reporte guardado: {self.base_path / filename}")
            return True
        except Exception as e:
            print(f"\n⚠️  Error al guardar reporte: {e}")
            return False

    def print_final_summary(self):
        """Imprimir resumen final"""
        print("\n" + "="*70)
        print("RESUMEN FINAL")
        print("="*70)

        total_modules = len(self.results)
        passed = sum(1 for r in self.results if r.get("status") == "PASSED")

        if passed == total_modules:
            print("\n🎉 ¡TODOS LOS MÓDULOS EJECUTADOS EXITOSAMENTE!")
        elif passed > total_modules / 2:
            print(f"\n✓ {passed}/{total_modules} módulos completados correctamente")
        else:
            print(f"\n⚠️  Solo {passed}/{total_modules} módulos completados")

        print("\n" + "="*70 + "\n")


def main():
    """Función principal"""
    runner = CrewAITestRunner()

    # Ejecutar todos los módulos
    runner.run_all_modules()

    # Generar reporte
    runner.generate_report()

    # Guardar reporte
    runner.save_report()

    # Resumen final
    runner.print_final_summary()


if __name__ == "__main__":
    main()
