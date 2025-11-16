#!/usr/bin/env python3
"""
test_syntax.py - Validación de sintaxis de todos los ejemplos

Realiza validación de sintaxis Python en todos los archivos de ejemplos.
"""

import ast
import os
from pathlib import Path
import sys
from typing import Dict, List, Tuple


class ValidadorSintaxis:
    """Valida la sintaxis Python de los archivos"""

    def __init__(self):
        self.resultados = {
            "validos": [],
            "invalidos": [],
            "advertencias": []
        }
        self.total = 0

    def validar_archivo(self, ruta: Path) -> Tuple[bool, str]:
        """Valida un archivo Python"""
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                codigo = f.read()

            # Intentar parsear como AST
            ast.parse(codigo)

            # Validaciones adicionales
            advertencias = self._verificar_advertencias(codigo)

            return True, advertencias

        except SyntaxError as e:
            return False, f"Error de sintaxis en línea {e.lineno}: {e.msg}"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def _verificar_advertencias(self, codigo: str) -> str:
        """Verifica posibles advertencias"""
        advertencias = []

        # Verificar imports no utilizados (simple)
        lineas = codigo.split('\n')
        for i, linea in enumerate(lineas, 1):
            if linea.strip().startswith('import ') or linea.strip().startswith('from '):
                # Verificaciones básicas
                if 'json' in linea and 'json.' not in codigo:
                    advertencias.append(f"Línea {i}: 'json' importado pero no usado")

        return "; ".join(advertencias) if advertencias else ""

    def validar_directorio(self, directorio: Path) -> Dict:
        """Valida todos los archivos Python en un directorio"""
        archivos_py = list(directorio.glob("*.py"))

        if not archivos_py:
            print(f"⚠️  No se encontraron archivos Python en {directorio}")
            return self.resultados

        print(f"\n🔍 Validando {len(archivos_py)} archivos Python...\n")

        for archivo in sorted(archivos_py):
            self.total += 1

            # Saltar archivos de test
            if archivo.name.startswith('test_') or archivo.name.startswith('run_'):
                continue

            valido, mensaje = self.validar_archivo(archivo)

            if valido:
                self.resultados["validos"].append(archivo.name)
                estado = "✅"
                print(f"{estado} {archivo.name}")

                if mensaje:
                    print(f"   ⚠️  {mensaje}")
                    self.resultados["advertencias"].append({
                        "archivo": archivo.name,
                        "mensaje": mensaje
                    })
            else:
                self.resultados["invalidos"].append({
                    "archivo": archivo.name,
                    "error": mensaje
                })
                estado = "❌"
                print(f"{estado} {archivo.name}")
                print(f"   {mensaje}")

        return self.resultados

    def obtener_reporte(self) -> str:
        """Genera un reporte de validación"""
        reporte = []
        reporte.append("\n" + "=" * 60)
        reporte.append("REPORTE DE VALIDACIÓN DE SINTAXIS")
        reporte.append("=" * 60)

        # Resumen
        reporte.append(f"\n📊 RESUMEN:")
        reporte.append(f"   Total de archivos: {self.total}")
        reporte.append(f"   ✅ Válidos: {len(self.resultados['validos'])}")
        reporte.append(f"   ❌ Inválidos: {len(self.resultados['invalidos'])}")
        reporte.append(f"   ⚠️  Advertencias: {len(self.resultados['advertencias'])}")

        # Archivos válidos
        if self.resultados["validos"]:
            reporte.append(f"\n✅ ARCHIVOS VÁLIDOS ({len(self.resultados['validos'])}):")
            for archivo in sorted(self.resultados["validos"]):
                reporte.append(f"   - {archivo}")

        # Archivos inválidos
        if self.resultados["invalidos"]:
            reporte.append(f"\n❌ ARCHIVOS INVÁLIDOS ({len(self.resultados['invalidos'])}):")
            for item in self.resultados["invalidos"]:
                reporte.append(f"   - {item['archivo']}")
                reporte.append(f"     {item['error']}")

        # Advertencias
        if self.resultados["advertencias"]:
            reporte.append(f"\n⚠️  ADVERTENCIAS ({len(self.resultados['advertencias'])}):")
            for item in self.resultados["advertencias"]:
                reporte.append(f"   - {item['archivo']}")
                reporte.append(f"     {item['mensaje']}")

        # Resultado final
        if self.resultados["invalidos"]:
            reporte.append(f"\n❌ VALIDACIÓN FALLIDA")
            reporte.append("=" * 60)
            return "\n".join(reporte), False
        else:
            reporte.append(f"\n✅ TODOS LOS ARCHIVOS SON VÁLIDOS")
            reporte.append("=" * 60)
            return "\n".join(reporte), True

    def validar_imports(self, directorio: Path) -> Dict[str, List[str]]:
        """Verifica que todos los imports estén disponibles"""
        print("\n🔍 Verificando imports requeridos...\n")

        imports_requeridos = set()
        archivos_py = list(directorio.glob("*.py"))

        for archivo in archivos_py:
            if archivo.name.startswith('test_') or archivo.name.startswith('run_'):
                continue

            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    arbol = ast.parse(f.read())

                for nodo in ast.walk(arbol):
                    if isinstance(nodo, ast.Import):
                        for alias in nodo.names:
                            modulo = alias.name.split('.')[0]
                            imports_requeridos.add(modulo)
                    elif isinstance(nodo, ast.ImportFrom):
                        if nodo.module:
                            modulo = nodo.module.split('.')[0]
                            imports_requeridos.add(modulo)

            except Exception as e:
                print(f"   ⚠️  Error analizando {archivo.name}: {e}")

        # Verificar disponibilidad
        print(f"📦 Imports requeridos encontrados: {len(imports_requeridos)}\n")

        imports_disponibles = {}
        imports_faltantes = []

        for modulo in sorted(imports_requeridos):
            try:
                __import__(modulo)
                imports_disponibles[modulo] = "✅"
                print(f"   ✅ {modulo}")
            except ImportError:
                imports_faltantes.append(modulo)
                imports_disponibles[modulo] = "❌"
                print(f"   ❌ {modulo}")

        if imports_faltantes:
            print(f"\n⚠️  Módulos faltantes: {', '.join(imports_faltantes)}")
            print("   Instalar con: pip install -r requirements.txt")

        return imports_disponibles


def validar_dependencias_minimas():
    """Verifica dependencias mínimas"""
    print("\n🔧 Verificando dependencias mínimas...\n")

    dependencias = {
        "python": "3.8+",
        "langchain": "core",
        "ollama": "local"
    }

    requeridas = [
        ("langchain_core", "langchain-core"),
        ("langchain_community", "langchain-community"),
        ("fastapi", "fastapi"),
        ("pydantic", "pydantic"),
    ]

    disponibles = 0
    for modulo, paquete in requeridas:
        try:
            __import__(modulo)
            print(f"   ✅ {paquete}")
            disponibles += 1
        except ImportError:
            print(f"   ❌ {paquete}")

    print(f"\n   {disponibles}/{len(requeridas)} dependencias disponibles")

    if disponibles < len(requeridas):
        print("\n   ⚠️  Para ejecutar los ejemplos completamente, instala:")
        print("   pip install langchain-core langchain-community fastapi pydantic")


def main():
    """Función principal"""
    # Obtener directorio actual
    directorio_actual = Path(__file__).parent

    print("=" * 60)
    print("VALIDADOR DE EJEMPLOS LANGFLOW")
    print("=" * 60)

    # Validar sintaxis
    validador = ValidadorSintaxis()
    validador.validar_directorio(directorio_actual)

    # Reporte de sintaxis
    reporte, valido = validador.obtener_reporte()
    print(reporte)

    # Verificar imports
    validador.validar_imports(directorio_actual)

    # Verificar dependencias
    validar_dependencias_minimas()

    # Conclusión
    print("\n" + "=" * 60)
    if valido:
        print("✅ VALIDACIÓN COMPLETADA CON ÉXITO")
        print("\nTodos los archivos de ejemplo tienen sintaxis válida.")
        print("Para ejecutar los ejemplos:")
        print("   1. Asegúrate de tener Ollama ejecutándose en http://localhost:11434")
        print("   2. Ejecuta cualquier archivo: python 01_chatbot_simple.py")
        print("=" * 60)
        sys.exit(0)
    else:
        print("❌ VALIDACIÓN FALLIDA")
        print("Revisa los errores de sintaxis arriba.")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
