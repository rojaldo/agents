#!/bin/bash

# Script para probar los ejemplos de MCP con LangChain y Ollama

echo "=========================================="
echo "Test de Ejemplos MCP + LangChain + Ollama"
echo "=========================================="
echo ""

# Verificar que Ollama esté instalado
echo "1. Verificando instalación de Ollama..."
if command -v ollama &> /dev/null; then
    echo "   ✓ Ollama está instalado"
    ollama --version
else
    echo "   ✗ Ollama no está instalado"
    echo "   Instala Ollama desde: https://ollama.com"
    exit 1
fi

echo ""

# Verificar que Ollama esté corriendo
echo "2. Verificando que Ollama esté corriendo..."
if curl -s http://localhost:11434 &> /dev/null; then
    echo "   ✓ Ollama está corriendo"
else
    echo "   ✗ Ollama no está corriendo"
    echo "   Ejecuta: ollama serve"
    exit 1
fi

echo ""

# Verificar modelos necesarios
echo "3. Verificando modelos necesarios..."
REQUIRED_MODELS=("llama3.2" "nomic-embed-text")

for model in "${REQUIRED_MODELS[@]}"; do
    if ollama list | grep -q "$model"; then
        echo "   ✓ Modelo $model está disponible"
    else
        echo "   ✗ Modelo $model NO está disponible"
        echo "   Descarga con: ollama pull $model"
        exit 1
    fi
done

echo ""

# Verificar dependencias Python
echo "4. Verificando dependencias Python..."
if python3 -c "import langchain" 2>/dev/null; then
    echo "   ✓ langchain está instalado"
else
    echo "   ✗ langchain no está instalado"
    echo "   Ejecuta: pip install -r requirements.txt"
    exit 1
fi

if python3 -c "import langchain_ollama" 2>/dev/null; then
    echo "   ✓ langchain-ollama está instalado"
else
    echo "   ✗ langchain-ollama no está instalado"
    echo "   Ejecuta: pip install -r requirements.txt"
    exit 1
fi

echo ""
echo "=========================================="
echo "Todos los prerequisitos están OK!"
echo "=========================================="
echo ""

# Preguntar si ejecutar los ejemplos
read -p "¿Deseas ejecutar los ejemplos? (s/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo ""
    echo "=========================================="
    echo "Ejecutando Ejemplo 1: Servidor Básico"
    echo "=========================================="
    python3 01_servidor_basico_langchain.py

    echo ""
    echo "=========================================="
    echo "Ejecutando Ejemplo 2: Cliente MCP"
    echo "=========================================="
    python3 02_cliente_mcp_langchain.py

    echo ""
    echo "=========================================="
    echo "Ejecutando Ejemplo 3: Servidor RAG"
    echo "=========================================="
    python3 03_servidor_rag_langchain.py

    echo ""
    echo "=========================================="
    echo "Todos los ejemplos ejecutados!"
    echo "=========================================="
fi
