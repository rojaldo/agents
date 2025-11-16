#!/usr/bin/env python3
"""
test_syntax.py - Verificar la sintaxis de todos los ejemplos

Este script verifica que todos los ejemplos son sintácticamente correctos
sin necesidad de que Ollama esté ejecutándose.
"""

import ast
import sys
from pathlib import Path


def check_syntax(filepath):
    """Verificar sintaxis de un archivo Python"""
    try:
        with open(filepath, 'r') as f:
            ast.parse(f.read())
        return True, None
    except SyntaxError as e:
        return False, str(e)


def main():
    print("\n" + "=" * 60)
    print("VERIFICACIÓN DE SINTAXIS - EJEMPLOS LANGCHAIN")
    print("=" * 60 + "\n")

    ejemplos = [
        "01_basic_llm.py",
        "02_chains_basics.py",
        "03_memory.py",
        "04_agents.py",
        "05_embeddings_vectorstore.py",
        "06_rag_system.py",
        "07_debugging.py",
        "09_patterns.py",
        "11_chatbot.py",
        "15_production.py",
        "16_project_final.py",
    ]

    directorio = Path(__file__).parent
    resultados = []

    for ejemplo in ejemplos:
        filepath = directorio / ejemplo
        if not filepath.exists():
            print(f"❌ {ejemplo:40} - ARCHIVO NO ENCONTRADO")
            resultados.append((ejemplo, False, "Archivo no encontrado"))
            continue

        valido, error = check_syntax(filepath)
        if valido:
            print(f"✅ {ejemplo:40} - VÁLIDO")
            resultados.append((ejemplo, True, None))
        else:
            print(f"❌ {ejemplo:40} - ERROR SINTAXIS")
            print(f"   {error}")
            resultados.append((ejemplo, False, error))

    # Resumen
    print("\n" + "=" * 60)
    validos = sum(1 for _, v, _ in resultados if v)
    invalidos = sum(1 for _, v, _ in resultados if not v)

    print(f"RESULTADO: {validos} archivos válidos, {invalidos} con errores")
    print("=" * 60)

    if invalidos == 0:
        print("\n✅ Todos los ejemplos son sintácticamente correctos\n")
        print("PRÓXIMOS PASOS:")
        print("1. Asegúrate de que Ollama está ejecutándose:")
        print("   ollama serve")
        print("\n2. Descarga un modelo:")
        print("   ollama pull mistral")
        print("\n3. Ejecuta los ejemplos:")
        print("   python 01_basic_llm.py")
        print("   python 02_chains_basics.py")
        print("   ...\n")
        return 0
    else:
        print(f"\n❌ {invalidos} archivos tienen errores de sintaxis\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
