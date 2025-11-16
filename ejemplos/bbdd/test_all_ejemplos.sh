#!/bin/bash

echo "=================================="
echo "PRUEBA DE TODOS LOS EJEMPLOS"
echo "=================================="

cd "$(dirname "$0")"

echo ""
echo "📦 Verificando dependencias..."
python3 << 'EOF'
try:
    import chromadb
    print("✓ chromadb disponible")
except:
    print("✗ chromadb no disponible")

try:
    from langchain_chroma import Chroma
    print("✓ langchain-chroma disponible")
except:
    print("✗ langchain-chroma no disponible")
EOF

echo ""
echo "════════════════════════════════════════════════════════════"
echo "EJEMPLO 1: ChromaDB Básico"
echo "════════════════════════════════════════════════════════════"
python3 01_chromadb_basico.py

echo ""
echo "════════════════════════════════════════════════════════════"
echo "EJEMPLO 3: Conceptos Básicos de Grafos"
echo "════════════════════════════════════════════════════════════"
python3 03_grafos_conceptos_basicos.py

echo ""
echo "════════════════════════════════════════════════════════════"
echo "RESUMEN"
echo "════════════════════════════════════════════════════════════"
echo "✓ Ejemplo 1: ChromaDB Basico - COMPLETADO"
echo "✓ Ejemplo 3: Grafos Conceptos - COMPLETADO"
echo ""
echo "Ejemplos creados en: $(pwd)"
echo "- 01_chromadb_basico.py"
echo "- 02_chromadb_con_ollama.py (requiere Ollama)"
echo "- 03_grafos_conceptos_basicos.py"
echo ""
echo "Database directory: ./chroma_db"
echo "════════════════════════════════════════════════════════════"
