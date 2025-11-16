#!/usr/bin/env python3
"""
SCRIPT DE PRUEBA - Validar todos los ejemplos de RAG
Comprueba que los ejemplos funcionan correctamente
"""

import sys
import subprocess
from pathlib import Path
import json
from datetime import datetime

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

MODULOS = {
    "modulo3": [
        "01_cargar_documentos.py",
        "02_chunking.py"
    ],
    "modulo4": [
        "01_embeddings.py"
    ],
    "modulo6": [
        "01_rag_basico_ollama.py"
    ],
    "modulo8": [
        "01_chat_con_memoria.py"
    ],
    "modulo10": [
        "01_qa_sobre_documentos.py"
    ]
}

# ============================================================================
# VERIFICACIONES
# ============================================================================

def verificar_python():
    """Verificar versión de Python"""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    return version.major >= 3 and version.minor >= 8


def verificar_archivos():
    """Verificar que todos los archivos existen"""
    print("\n📁 Verificando archivos...")
    base_path = Path(".")

    archivos_encontrados = 0
    archivos_faltantes = []

    for modulo, archivos in MODULOS.items():
        for archivo in archivos:
            ruta = base_path / modulo / archivo
            if ruta.exists():
                print(f"  ✓ {modulo}/{archivo}")
                archivos_encontrados += 1
            else:
                print(f"  ✗ {modulo}/{archivo} (NO ENCONTRADO)")
                archivos_faltantes.append(f"{modulo}/{archivo}")

    print(f"\nTotal: {archivos_encontrados} archivos encontrados")
    if archivos_faltantes:
        print(f"Faltantes: {len(archivos_faltantes)}")
        for archivo in archivos_faltantes:
            print(f"  - {archivo}")

    return len(archivos_faltantes) == 0


def verificar_ollama():
    """Verificar si Ollama está disponible"""
    print("\n🔍 Verificando Ollama...")
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            modelos = response.json().get("models", [])
            print(f"  ✓ Ollama disponible")
            print(f"  Modelos: {len(modelos)}")
            if modelos:
                for modelo in modelos[:3]:
                    print(f"    - {modelo.get('name', 'desconocido')}")
            return True
        else:
            print("  ✗ Ollama no responde")
            return False
    except Exception as e:
        print(f"  ⚠ Ollama no disponible: {e}")
        return False


def ejecutar_ejemplo(modulo: str, archivo: str) -> bool:
    """Ejecutar un ejemplo y validar que funciona"""
    ruta = Path(modulo) / archivo

    try:
        print(f"\n  ▶ {archivo}...", end=" ")

        # Ejecutar el script
        resultado = subprocess.run(
            [sys.executable, str(ruta)],
            capture_output=True,
            text=True,
            timeout=30
        )

        if resultado.returncode == 0:
            print("✓")
            return True
        else:
            print("✗")
            print(f"    Error: {resultado.stderr[:100]}")
            return False

    except subprocess.TimeoutExpired:
        print("✗ (Timeout)")
        return False
    except Exception as e:
        print(f"✗ ({e})")
        return False


# ============================================================================
# TESTS
# ============================================================================

def ejecutar_tests():
    """Ejecutar todos los ejemplos como tests"""
    print("\n" + "=" * 70)
    print("EJECUTANDO EJEMPLOS")
    print("=" * 70)

    resultados = {}
    total = 0
    exitosos = 0

    for modulo, archivos in MODULOS.items():
        print(f"\n{modulo.upper()}:")
        resultados[modulo] = []

        for archivo in archivos:
            total += 1
            exitoso = ejecutar_ejemplo(modulo, archivo)
            exitosos += exitoso
            resultados[modulo].append({
                "archivo": archivo,
                "exitoso": exitoso
            })

    # ========================================================================
    # RESUMEN
    # ========================================================================
    print("\n" + "=" * 70)
    print("RESUMEN DE PRUEBAS")
    print("=" * 70)

    print(f"\nTotal de ejemplos: {total}")
    print(f"Exitosos: {exitosos}")
    print(f"Fallidos: {total - exitosos}")
    print(f"Tasa de éxito: {(exitosos/total*100):.1f}%")

    # Detalles por módulo
    print("\nDetalles por módulo:")
    for modulo, tests in resultados.items():
        exitosos_modulo = sum(1 for t in tests if t["exitoso"])
        total_modulo = len(tests)
        print(f"  {modulo}: {exitosos_modulo}/{total_modulo}")

    return exitosos == total


# ============================================================================
# INFORMACIÓN DEL SISTEMA
# ============================================================================

def mostrar_info_sistema():
    """Mostrar información del sistema"""
    print("\n" + "=" * 70)
    print("INFORMACIÓN DEL SISTEMA")
    print("=" * 70)

    # Python
    print(f"\n🐍 Python")
    print(f"  Versión: {sys.version}")
    print(f"  Ejecutable: {sys.executable}")

    # Sistema Operativo
    import platform
    print(f"\n💻 Sistema Operativo")
    print(f"  {platform.system()} {platform.release()}")
    print(f"  Máquina: {platform.machine()}")

    # Paquetes importantes
    print(f"\n📦 Paquetes Instalados")
    paquetes = ["langchain", "langchain-ollama", "chromadb", "requests"]
    for paquete in paquetes:
        try:
            __import__(paquete.replace("-", "_"))
            print(f"  ✓ {paquete}")
        except ImportError:
            print(f"  ✗ {paquete} (no instalado)")


# ============================================================================
# GENERADOR DE REPORTE
# ============================================================================

def generar_reporte(resultado_tests: bool, ollama_disponible: bool):
    """Generar reporte de pruebas"""
    reporte = {
        "timestamp": datetime.now().isoformat(),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
        "sistema": {
            "platform": sys.platform,
            "archivos": verificar_archivos(),
            "ollama": ollama_disponible,
            "tests": resultado_tests
        },
        "resumen": {
            "estado": "✅ EXITOSO" if resultado_tests else "❌ CON ERRORES",
            "todos_ejemplos_funcionan": resultado_tests,
            "ollama_disponible": ollama_disponible,
            "modulos_cubiertos": list(MODULOS.keys())
        }
    }

    # Guardar reporte
    with open("reporte_pruebas.json", "w", encoding="utf-8") as f:
        json.dump(reporte, f, ensure_ascii=False, indent=2)

    print("\n✓ Reporte guardado en reporte_pruebas.json")

    return reporte


# ============================================================================
# INSTRUCCIONES DE USO
# ============================================================================

def mostrar_instrucciones():
    """Mostrar instrucciones de uso"""
    instrucciones = """
┌─────────────────────────────────────────────────────────────────────────┐
│                   INSTRUCCIONES DE USO DE EJEMPLOS RAG                  │
└─────────────────────────────────────────────────────────────────────────┘

1. INSTALACIÓN DE DEPENDENCIAS:
   pip install langchain langchain-ollama chromadb requests

2. INSTALAR OLLAMA:
   - Descargar desde: https://ollama.ai
   - Ejecutar: ollama serve
   - Descargar modelo: ollama pull mistral

3. EJECUTAR EJEMPLOS INDIVIDUALES:
   cd modulo3
   python 01_cargar_documentos.py
   python 02_chunking.py

4. EJECUTAR TODOS LOS TESTS:
   python test_ejemplos_rag.py

5. MÓDULOS DISPONIBLES:
"""

    print(instrucciones)

    for modulo, archivos in MODULOS.items():
        print(f"   {modulo}:")
        for archivo in archivos:
            descripcion = archivo.replace("_", " ").replace(".py", "")
            print(f"      - {descripcion}")

    print("""
6. CONTENIDO POR MÓDULO:
   ✓ Módulo 3: Cargar documentos y chunking
   ✓ Módulo 4: Crear embeddings
   ✓ Módulo 6: RAG básico con Ollama
   ✓ Módulo 8: Chat con memoria
   ✓ Módulo 10: Q&A sobre documentos

7. PRÓXIMOS PASOS:
   - Revisar los archivos JSON generados
   - Personalizar ejemplos para tus documentos
   - Implementar en producción con Ollama real
    """)


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Función principal"""
    print("=" * 70)
    print("VALIDADOR DE EJEMPLOS RAG")
    print("=" * 70)

    # Verificaciones iniciales
    print("\n📋 VERIFICACIONES INICIALES")
    print("-" * 70)

    python_ok = verificar_python()
    archivos_ok = verificar_archivos()
    ollama_ok = verificar_ollama()

    # Ejecutar tests
    tests_ok = ejecutar_tests()

    # Mostrar información
    mostrar_info_sistema()

    # Generar reporte
    reporte = generar_reporte(tests_ok, ollama_ok)

    # Mostrar resumen final
    print("\n" + "=" * 70)
    print("RESULTADO FINAL")
    print("=" * 70)
    print(f"\n{reporte['resumen']['estado']}")
    print(f"  • Ejemplos funcionales: {reporte['resumen']['todos_ejemplos_funcionan']}")
    print(f"  • Ollama disponible: {reporte['resumen']['ollama_disponible']}")
    print(f"  • Módulos cubiertos: {len(MODULOS)}")

    # Mostrar instrucciones
    mostrar_instrucciones()

    # Retornar código de salida
    return 0 if tests_ok else 1


if __name__ == "__main__":
    sys.exit(main())
