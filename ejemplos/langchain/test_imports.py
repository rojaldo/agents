#!/usr/bin/env python3
"""
test_imports.py - Verificar que todos los imports necesarios están disponibles

Este script verifica que todas las dependencias están instaladas correctamente.
No requiere que Ollama esté ejecutándose.
"""

import sys


def test_imports():
    """Probar imports de todos los módulos necesarios"""
    print("=" * 60)
    print("VERIFICANDO DEPENDENCIAS")
    print("=" * 60)

    required_modules = {
        "langchain": "LangChain core",
        "langchain_community": "LangChain Community",
        "langchain_core": "LangChain Core",
        "langchain_text_splitters": "Text Splitters",
        "pydantic": "Pydantic",
    }

    failed = []
    success = []

    for module, description in required_modules.items():
        try:
            __import__(module)
            print(f"✅ {description:30} - OK")
            success.append(module)
        except ImportError as e:
            print(f"❌ {description:30} - FALTA")
            failed.append((module, str(e)))

    print("\n" + "=" * 60)
    print(f"RESULTADO: {len(success)} módulos encontrados, {len(failed)} faltantes")
    print("=" * 60)

    if failed:
        print("\n📦 Módulos faltantes. Instala con:")
        print("\n   pip install langchain langchain-community langchain-core pydantic python-dotenv")
        return False

    return True


def test_ollama_connection():
    """Verificar conexión a Ollama (opcional)"""
    print("\n" + "=" * 60)
    print("VERIFICANDO CONEXIÓN A OLLAMA")
    print("=" * 60)

    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        print(f"✅ Ollama está ejecutándose en http://localhost:11434")
        print(f"   Status: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print(f"⚠️  Ollama no está ejecutándose")
        print(f"   Para iniciar: ollama serve")
        return False
    except Exception as e:
        print(f"⚠️  Error al conectar con Ollama: {e}")
        return False


def test_ollama_models():
    """Listar modelos disponibles en Ollama"""
    print("\n" + "=" * 60)
    print("MODELOS DISPONIBLES EN OLLAMA")
    print("=" * 60)

    try:
        import requests
        import json

        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        data = response.json()

        if "models" in data and len(data["models"]) > 0:
            print("\nModelos disponibles:")
            for model in data["models"]:
                name = model.get("name", "desconocido")
                size = model.get("size", 0)
                size_gb = size / (1024**3)
                print(f"  • {name:30} ({size_gb:.2f} GB)")
        else:
            print("\n⚠️  No hay modelos descargados")
            print("\nPara descargar un modelo:")
            print("   ollama pull mistral")
            print("   ollama pull neural-chat")

    except Exception as e:
        print(f"No se pudo obtener información de modelos: {e}")


def main():
    print("\n🚀 VERIFICACIÓN DEL ENTORNO DE LANGCHAIN\n")

    # Test 1: Imports
    imports_ok = test_imports()

    if imports_ok:
        print("\n✅ Todas las dependencias están instaladas correctamente")
        print("\n📝 Ahora puedes ejecutar los ejemplos:")
        print("   python 01_basic_llm.py")
        print("   python 02_chains_basics.py")
        print("   ...")

        # Test 2: Ollama connection (opcional)
        ollama_ok = test_ollama_connection()

        if ollama_ok:
            test_ollama_models()
            print("\n✅ Sistema listo para ejecutar los ejemplos")
        else:
            print("\n⚠️  Asegúrate de ejecutar Ollama antes de correr los ejemplos:")
            print("   ollama serve")

    else:
        print("\n❌ Instala las dependencias faltantes y vuelve a intentar")
        sys.exit(1)


if __name__ == "__main__":
    main()
