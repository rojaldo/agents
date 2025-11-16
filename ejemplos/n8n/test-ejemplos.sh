#!/bin/bash

# Script de prueba para verificar que los ejemplos n8n funcionan

echo "=========================================="
echo "Pruebas de Ejemplos n8n"
echo "=========================================="
echo ""

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contador de pruebas
PRUEBAS_TOTAL=0
PRUEBAS_EXITOSAS=0
PRUEBAS_FALLIDAS=0

# Función para verificar JSON válido
verificar_json() {
    local archivo=$1
    local nombre=$2

    echo -n "Verificando $nombre... "
    PRUEBAS_TOTAL=$((PRUEBAS_TOTAL + 1))

    if python3 -m json.tool "$archivo" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ JSON válido${NC}"
        PRUEBAS_EXITOSAS=$((PRUEBAS_EXITOSAS + 1))
    else
        echo -e "${RED}✗ JSON inválido${NC}"
        PRUEBAS_FALLIDAS=$((PRUEBAS_FALLIDAS + 1))
    fi
}

# Función para verificar Ollama
verificar_ollama() {
    echo -n "Verificando Ollama en localhost:11434... "

    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Ollama disponible${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠ Ollama no disponible (opcional)${NC}"
        return 1
    fi
}

# Función para verificar n8n
verificar_n8n() {
    echo -n "Verificando n8n en localhost:5678... "

    if curl -s http://localhost:5678 > /dev/null 2>&1; then
        echo -e "${GREEN}✓ n8n disponible${NC}"
        return 0
    else
        echo -e "${RED}✗ n8n no disponible${NC}"
        echo "  Inicia n8n con: n8n"
        return 1
    fi
}

# Función para listar archivos JSON
listar_ejemplos() {
    echo ""
    echo "=========================================="
    echo "Ejemplos disponibles por módulo"
    echo "=========================================="

    for modulo in modulo*; do
        if [ -d "$modulo" ]; then
            echo ""
            echo "${YELLOW}$modulo:${NC}"
            ls -1 "$modulo"/*.json 2>/dev/null | while read archivo; do
                nombre=$(basename "$archivo" .json)
                echo "  - $nombre"
            done
        fi
    done
}

# INICIO DE PRUEBAS
echo "1. Verificación de Servicios"
echo "----------------------------"
verificar_n8n
N8N_OK=$?

verificar_ollama
OLLAMA_OK=$?

echo ""
echo "2. Verificación de Archivos JSON"
echo "--------------------------------"

# Verificar todos los archivos JSON
for archivo in modulo*/*.json; do
    if [ -f "$archivo" ]; then
        nombre=$(basename "$archivo" .json)
        verificar_json "$archivo" "$nombre"
    fi
done

echo ""
echo "3. Ejemplos Disponibles"
echo "---------------------"
listar_ejemplos

echo ""
echo "=========================================="
echo "RESUMEN DE PRUEBAS"
echo "=========================================="
echo "Total de archivos JSON verificados: $PRUEBAS_TOTAL"
echo -e "Archivos válidos: ${GREEN}$PRUEBAS_EXITOSAS${NC}"
echo -e "Archivos con errores: ${RED}$PRUEBAS_FALLIDAS${NC}"
echo ""

if [ $PRUEBAS_FALLIDAS -eq 0 ]; then
    echo -e "${GREEN}✓ Todos los archivos JSON son válidos${NC}"
else
    echo -e "${RED}✗ Hay archivos JSON con problemas${NC}"
fi

echo ""
echo "=========================================="
echo "INSTRUCCIONES PARA USAR LOS EJEMPLOS"
echo "=========================================="
echo ""
echo "1. Instala n8n:"
echo "   npm install -g n8n"
echo ""
echo "2. Inicia n8n:"
echo "   n8n"
echo ""
echo "3. Abre n8n en el navegador:"
echo "   http://localhost:5678"
echo ""
echo "4. Importa los archivos JSON:"
echo "   Click en el menú → Workflows → Importar desde JSON"
echo ""
echo "5. Para ejemplos con Ollama, instala:"
echo "   # En macOS:"
echo "   brew install ollama"
echo "   # En Linux/Windows: descarga desde ollama.ai"
echo ""
echo "6. Inicia Ollama en una terminal separada:"
echo "   ollama serve"
echo ""
echo "7. Descarga un modelo (ej. llama2):"
echo "   ollama pull llama2"
echo ""
echo "=========================================="

exit $PRUEBAS_FALLIDAS
