#!/bin/bash

# Script para descargar los modelos necesarios de Ollama

echo "=========================================="
echo "Setup de Modelos para Ejemplos MCP"
echo "=========================================="
echo ""

# Verificar que Ollama esté instalado
if ! command -v ollama &> /dev/null; then
    echo "✗ Ollama no está instalado"
    echo ""
    echo "Instala Ollama según tu sistema operativo:"
    echo ""
    echo "Linux:"
    echo "  curl -fsSL https://ollama.com/install.sh | sh"
    echo ""
    echo "macOS:"
    echo "  brew install ollama"
    echo ""
    echo "Windows:"
    echo "  Descarga desde https://ollama.com/download"
    exit 1
fi

echo "✓ Ollama está instalado"
echo ""

# Verificar que Ollama esté corriendo
echo "Verificando que Ollama esté corriendo..."
if ! curl -s http://localhost:11434 &> /dev/null; then
    echo "Ollama no está corriendo. Iniciando..."
    ollama serve > /tmp/ollama.log 2>&1 &
    sleep 3

    if curl -s http://localhost:11434 &> /dev/null; then
        echo "✓ Ollama iniciado correctamente"
    else
        echo "✗ No se pudo iniciar Ollama"
        echo "Ejecuta manualmente: ollama serve"
        exit 1
    fi
else
    echo "✓ Ollama está corriendo"
fi

echo ""
echo "=========================================="
echo "Descargando modelos necesarios..."
echo "=========================================="
echo ""
echo "NOTA: Esto puede tomar varios minutos dependiendo de tu conexión"
echo ""

# Modelo principal para LLM
echo "1. Descargando llama3.2 (~2GB)..."
echo "   Este es el modelo principal para generación de texto"
ollama pull llama3.2

if [ $? -eq 0 ]; then
    echo "   ✓ llama3.2 descargado correctamente"
else
    echo "   ✗ Error descargando llama3.2"
    exit 1
fi

echo ""

# Modelo para embeddings
echo "2. Descargando nomic-embed-text (~274MB)..."
echo "   Este modelo se usa para embeddings en RAG"
ollama pull nomic-embed-text

if [ $? -eq 0 ]; then
    echo "   ✓ nomic-embed-text descargado correctamente"
else
    echo "   ✗ Error descargando nomic-embed-text"
    exit 1
fi

echo ""
echo "=========================================="
echo "✓ Todos los modelos descargados!"
echo "=========================================="
echo ""
echo "Modelos disponibles:"
ollama list

echo ""
echo "Ya puedes ejecutar los ejemplos con:"
echo "  python3 01_servidor_basico_langchain.py"
echo "  python3 02_cliente_mcp_langchain.py"
echo "  python3 03_servidor_rag_langchain.py"
echo ""
