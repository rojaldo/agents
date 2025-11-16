"""
Ejemplo 0: Verificar Setup y Configuración

Este script verifica que todo esté correctamente configurado
para ejecutar los ejemplos de MCP con LangChain y Ollama.
"""

import sys
import subprocess
from typing import Tuple, List


def verificar_python() -> Tuple[bool, str]:
    """Verifica la versión de Python."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        return True, f"Python {version.major}.{version.minor}.{version.micro}"
    return False, f"Python {version.major}.{version.minor} (se requiere 3.8+)"


def verificar_paquete(paquete: str) -> Tuple[bool, str]:
    """Verifica que un paquete de Python esté instalado."""
    try:
        __import__(paquete)
        # Intentar obtener versión
        try:
            mod = __import__(paquete)
            version = getattr(mod, '__version__', 'instalado')
        except:
            version = 'instalado'
        return True, version
    except ImportError:
        return False, "no instalado"


def verificar_ollama() -> Tuple[bool, str]:
    """Verifica que Ollama esté instalado."""
    try:
        result = subprocess.run(
            ['ollama', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return True, result.stdout.strip()
        return False, "comando no funciona"
    except FileNotFoundError:
        return False, "no instalado"
    except Exception as e:
        return False, f"error: {str(e)}"


def verificar_ollama_corriendo() -> Tuple[bool, str]:
    """Verifica que Ollama esté corriendo."""
    try:
        import requests
        response = requests.get('http://localhost:11434', timeout=2)
        if response.status_code == 200 or 'Ollama' in response.text:
            return True, "corriendo"
        return False, "no responde"
    except:
        return False, "no está corriendo"


def listar_modelos_ollama() -> List[str]:
    """Lista los modelos de Ollama disponibles."""
    try:
        result = subprocess.run(
            ['ollama', 'list'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            modelos = [line.split()[0] for line in lines if line.strip()]
            return modelos
        return []
    except:
        return []


def main():
    print("=" * 70)
    print("Verificación de Setup para Ejemplos MCP + LangChain + Ollama")
    print("=" * 70)
    print()

    problemas = []

    # Verificar Python
    print("1. Verificando Python...")
    ok, info = verificar_python()
    print(f"   {'✓' if ok else '✗'} {info}")
    if not ok:
        problemas.append("Python 3.8+ es requerido")
    print()

    # Verificar paquetes Python
    print("2. Verificando paquetes Python...")
    paquetes_requeridos = {
        'langchain': 'LangChain',
        'langchain_ollama': 'LangChain Ollama',
        'langchain_community': 'LangChain Community',
        'faiss': 'FAISS (vector store)',
        'numpy': 'NumPy',
    }

    for paquete, nombre in paquetes_requeridos.items():
        ok, info = verificar_paquete(paquete)
        print(f"   {'✓' if ok else '✗'} {nombre}: {info}")
        if not ok:
            problemas.append(f"{nombre} no está instalado")

    print()

    # Verificar Ollama
    print("3. Verificando Ollama...")
    ok, info = verificar_ollama()
    print(f"   {'✓' if ok else '✗'} Ollama: {info}")
    if not ok:
        problemas.append("Ollama no está instalado")
    print()

    # Verificar que Ollama esté corriendo
    if ok:  # Solo si Ollama está instalado
        print("4. Verificando servicio Ollama...")
        ok, info = verificar_ollama_corriendo()
        print(f"   {'✓' if ok else '✗'} Servicio: {info}")
        if not ok:
            problemas.append("Ollama no está corriendo (ejecuta: ollama serve)")
        print()

        # Listar modelos disponibles
        print("5. Verificando modelos Ollama...")
        modelos = listar_modelos_ollama()
        if modelos:
            print(f"   ✓ Modelos disponibles ({len(modelos)}):")
            for modelo in modelos:
                print(f"     - {modelo}")
        else:
            print("   ⚠ No hay modelos instalados")
            problemas.append("Se requiere al menos llama3.2 y nomic-embed-text")
            print()
            print("   Descarga los modelos necesarios con:")
            print("     ollama pull llama3.2")
            print("     ollama pull nomic-embed-text")
            print()
            print("   O ejecuta el script de setup:")
            print("     bash setup_modelos.sh")

        # Verificar modelos específicos
        modelos_requeridos = ['llama3.2', 'nomic-embed-text']
        print()
        print("6. Verificando modelos requeridos...")
        for modelo in modelos_requeridos:
            # Verificar si algún modelo disponible contiene el nombre requerido
            encontrado = any(modelo in m for m in modelos)
            print(f"   {'✓' if encontrado else '✗'} {modelo}")
            if not encontrado:
                problemas.append(f"Modelo {modelo} no disponible")

    print()
    print("=" * 70)

    if problemas:
        print("❌ PROBLEMAS ENCONTRADOS:")
        print("=" * 70)
        for i, problema in enumerate(problemas, 1):
            print(f"{i}. {problema}")
        print()
        print("SOLUCIONES:")
        print()

        if any("Python" in p for p in problemas):
            print("• Instala Python 3.8 o superior desde python.org")
            print()

        if any("no está instalado" in p and "Ollama" not in p for p in problemas):
            print("• Instala las dependencias Python:")
            print("  pip install -r requirements.txt")
            print()

        if any("Ollama no está instalado" in p for p in problemas):
            print("• Instala Ollama:")
            print("  Linux: curl -fsSL https://ollama.com/install.sh | sh")
            print("  macOS: brew install ollama")
            print("  Windows: https://ollama.com/download")
            print()

        if any("no está corriendo" in p for p in problemas):
            print("• Inicia Ollama:")
            print("  ollama serve")
            print()

        if any("Modelo" in p for p in problemas):
            print("• Descarga los modelos:")
            print("  bash setup_modelos.sh")
            print("  (o manualmente: ollama pull llama3.2 && ollama pull nomic-embed-text)")
            print()

        sys.exit(1)
    else:
        print("✅ TODO ESTÁ CORRECTAMENTE CONFIGURADO!")
        print("=" * 70)
        print()
        print("Puedes ejecutar los ejemplos:")
        print()
        print("  python3 01_servidor_basico_langchain.py")
        print("  python3 02_cliente_mcp_langchain.py")
        print("  python3 03_servidor_rag_langchain.py")
        print()
        sys.exit(0)


if __name__ == "__main__":
    main()
