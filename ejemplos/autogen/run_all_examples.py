#!/usr/bin/env python3
"""
Script maestro para ejecutar todos los ejemplos de Módulos 6-11
Verifica que Ollama esté disponible y ejecuta ejemplos de forma secuencial
"""

import os
import sys
import subprocess
import json
from datetime import datetime
from pathlib import Path


class ExampleRunner:
    """Ejecutor de ejemplos con validación de Ollama"""

    def __init__(self, base_dir="/home/rojaldo/cursos/agents/ejemplos/autogen"):
        self.base_dir = Path(base_dir)
        self.ollama_url = "http://localhost:11434"
        self.results = {
            "total": 0,
            "successful": 0,
            "failed": 0,
            "modules": {},
            "timestamp": datetime.now().isoformat()
        }

    def check_ollama_available(self):
        """Verificar si Ollama está disponible"""
        try:
            import requests
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

    def get_available_modules(self):
        """Obtener módulos disponibles"""
        modules = []
        for item in self.base_dir.iterdir():
            if item.is_dir() and item.name.startswith("modulo_"):
                module_num = item.name.replace("modulo_", "")
                modules.append((int(module_num), item))

        return sorted(modules, key=lambda x: x[0])

    def get_module_examples(self, module_dir):
        """Obtener ejemplos de un módulo"""
        examples = []
        for file in sorted(module_dir.glob("*.py")):
            if not file.name.startswith("__"):
                examples.append(file)

        return examples

    def run_example(self, example_file):
        """Ejecutar un ejemplo Python"""
        try:
            # Cambiar a directorio del ejemplo
            original_dir = os.getcwd()
            os.chdir(example_file.parent)

            result = subprocess.run(
                [sys.executable, example_file.name],
                capture_output=True,
                text=True,
                timeout=30
            )

            os.chdir(original_dir)

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout[:500],  # Limitar output
                "stderr": result.stderr[:500],
                "returncode": result.returncode
            }

        except subprocess.TimeoutExpired:
            os.chdir(original_dir)
            return {
                "success": False,
                "error": "Timeout - ejecución tardó más de 30 segundos",
                "returncode": -1
            }
        except Exception as e:
            os.chdir(original_dir)
            return {
                "success": False,
                "error": str(e),
                "returncode": -1
            }

    def print_banner(self):
        """Imprimir encabezado"""
        print("\n" + "="*70)
        print(" EJECUTOR DE EJEMPLOS AUTOGEN - MÓDULOS 6-11")
        print("="*70)

    def print_section(self, title):
        """Imprimir sección"""
        print(f"\n{'='*70}")
        print(f" {title}")
        print("="*70)

    def print_example_header(self, module_num, example_file):
        """Imprimir encabezado de ejemplo"""
        print(f"\n[Módulo {module_num}] {example_file.stem}")
        print("-" * 70)

    def run_all(self):
        """Ejecutar todos los ejemplos"""
        self.print_banner()

        # Verificar Ollama
        print("\n🔍 Verificando disponibilidad de Ollama...")
        if not self.check_ollama_available():
            print("⚠️  ADVERTENCIA: Ollama no está disponible")
            print("    Los ejemplos requerirán Ollama ejecutándose")
            print("    Ejecuta: ollama serve")
            print()

        # Obtener módulos
        modules = self.get_available_modules()

        if not modules:
            print("\n❌ No se encontraron módulos")
            return

        print(f"\n✓ {len(modules)} módulos encontrados")

        # Ejecutar ejemplos
        for module_num, module_dir in modules:
            self.print_section(f"MÓDULO {module_num}")

            examples = self.get_module_examples(module_dir)

            if not examples:
                print(f"⚠️  No hay ejemplos en módulo {module_num}")
                continue

            self.results["modules"][f"modulo_{module_num}"] = {
                "total": len(examples),
                "successful": 0,
                "failed": 0,
                "examples": []
            }

            for example_file in examples:
                self.print_example_header(module_num, example_file)

                self.results["total"] += 1

                # Ejecutar ejemplo
                result = self.run_example(example_file)

                if result["success"]:
                    print(f"✅ ÉXITO")
                    if "stdout" in result and result["stdout"]:
                        print(f"Output (primeras líneas):")
                        print(result["stdout"][:200])
                    self.results["successful"] += 1
                    self.results["modules"][f"modulo_{module_num}"]["successful"] += 1
                else:
                    print(f"❌ ERROR")
                    if "error" in result:
                        print(f"Error: {result['error']}")
                    elif "stderr" in result and result["stderr"]:
                        print(f"Stderr: {result['stderr'][:200]}")
                    self.results["failed"] += 1
                    self.results["modules"][f"modulo_{module_num}"]["failed"] += 1

                self.results["modules"][f"modulo_{module_num}"]["examples"].append({
                    "name": example_file.name,
                    "success": result["success"]
                })

        # Imprimir resumen final
        self.print_summary()

    def print_summary(self):
        """Imprimir resumen de resultados"""
        self.print_section("RESUMEN FINAL")

        print(f"\n📊 Estadísticas Generales:")
        print(f"   Total de ejemplos: {self.results['total']}")
        print(f"   Exitosos: {self.results['successful']} ✅")
        print(f"   Fallidos: {self.results['failed']} ❌")

        if self.results['total'] > 0:
            success_rate = (self.results['successful'] / self.results['total']) * 100
            print(f"   Tasa de éxito: {success_rate:.1f}%")

        print(f"\n📋 Desglose por Módulo:")
        for module_name, module_data in sorted(self.results['modules'].items()):
            module_num = module_name.replace("modulo_", "")
            total = module_data['total']
            successful = module_data['successful']
            print(f"   Módulo {module_num}: {successful}/{total} ejemplos exitosos")

        print(f"\n⏱️  Timestamp: {self.results['timestamp']}")
        print("="*70 + "\n")

        # Guardar resultados
        self.save_results()

    def save_results(self):
        """Guardar resultados en archivo JSON"""
        results_file = self.base_dir / "execution_results.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"✓ Resultados guardados en: {results_file}")


def main():
    """Función principal"""
    runner = ExampleRunner()

    try:
        runner.run_all()
    except KeyboardInterrupt:
        print("\n\n⚠️  Ejecución interrumpida por el usuario")
        runner.print_summary()
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
