#!/bin/bash

# Script para probar todos los ejemplos de bases de datos vectoriales y grafos
# Uso: ./test-ejemplos.sh [opcion]
#
# Opciones:
#   chromadb  - Solo ejemplos de ChromaDB
#   neo4j     - Solo ejemplos de Neo4j
#   hibrido   - Solo ejemplos híbridos
#   all       - Todos los ejemplos (default)

set -e  # Salir si hay errores

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  TESTING EJEMPLOS BBDD VECTORIALES    ${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Función para mostrar encabezado
print_header() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

# Función para ejecutar ejemplo
run_example() {
    local file=$1
    local name=$2

    echo -e "\n${YELLOW}► Ejecutando: ${name}${NC}"
    echo -e "${YELLOW}  Archivo: ${file}${NC}\n"

    if python3 "$file"; then
        echo -e "\n${GREEN}✓ ${name} completado exitosamente${NC}"
        return 0
    else
        echo -e "\n${RED}✗ ${name} falló${NC}"
        return 1
    fi
}

# Verificar dependencias
check_dependencies() {
    print_header "VERIFICANDO DEPENDENCIAS"

    echo -e "${YELLOW}Verificando Python...${NC}"
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}✗ Python3 no encontrado${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Python3 disponible: $(python3 --version)${NC}"

    echo -e "\n${YELLOW}Verificando paquetes Python...${NC}"
    python3 -c "import chromadb" 2>/dev/null && echo -e "${GREEN}✓ chromadb${NC}" || echo -e "${YELLOW}⚠ chromadb no instalado${NC}"
    python3 -c "import langchain" 2>/dev/null && echo -e "${GREEN}✓ langchain${NC}" || echo -e "${YELLOW}⚠ langchain no instalado${NC}"
    python3 -c "import neo4j" 2>/dev/null && echo -e "${GREEN}✓ neo4j${NC}" || echo -e "${YELLOW}⚠ neo4j no instalado${NC}"

    echo -e "\n${YELLOW}Verificando Ollama...${NC}"
    if curl -s http://localhost:11434/api/tags &> /dev/null; then
        echo -e "${GREEN}✓ Ollama disponible${NC}"
    else
        echo -e "${YELLOW}⚠ Ollama no disponible en localhost:11434${NC}"
        echo -e "${YELLOW}  Los ejemplos con Ollama pueden fallar${NC}"
    fi

    echo -e "\n${YELLOW}Verificando Neo4j...${NC}"
    if timeout 2 bash -c "</dev/tcp/localhost/7687" 2>/dev/null; then
        echo -e "${GREEN}✓ Neo4j disponible en puerto 7687${NC}"
    else
        echo -e "${YELLOW}⚠ Neo4j no disponible en localhost:7687${NC}"
        echo -e "${YELLOW}  Los ejemplos de Neo4j pueden fallar${NC}"
    fi
}

# Determinar qué ejemplos ejecutar
OPTION=${1:-all}

# Arrays de ejemplos
declare -a CHROMADB_EXAMPLES=(
    "01_chromadb_basico.py:ChromaDB Básico"
    "02_chromadb_con_ollama.py:ChromaDB con Ollama"
    "04_rag_avanzado_chromadb.py:RAG Avanzado"
)

declare -a NEO4J_EXAMPLES=(
    "neo4j/01_neo4j_basico.py:Neo4j Básico"
    "neo4j/02_neo4j_con_langchain.py:Neo4j con LangChain"
)

declare -a HIBRIDO_EXAMPLES=(
    "hibrido/01_busqueda_hibrida.py:Búsqueda Híbrida"
)

declare -a OTROS_EXAMPLES=(
    "03_grafos_conceptos_basicos.py:Grafos - Conceptos Básicos"
)

# Verificar dependencias primero
check_dependencies

# Contadores
TOTAL=0
PASSED=0
FAILED=0

# Función para ejecutar grupo de ejemplos
run_examples() {
    local -n examples=$1
    local category=$2

    if [ ${#examples[@]} -eq 0 ]; then
        echo -e "${YELLOW}No hay ejemplos en la categoría: ${category}${NC}"
        return
    fi

    print_header "$category"

    for example in "${examples[@]}"; do
        IFS=':' read -r file name <<< "$example"
        TOTAL=$((TOTAL + 1))

        if run_example "$file" "$name"; then
            PASSED=$((PASSED + 1))
        else
            FAILED=$((FAILED + 1))
        fi
    done
}

# Ejecutar según opción
case $OPTION in
    chromadb)
        run_examples CHROMADB_EXAMPLES "EJEMPLOS CHROMADB"
        ;;
    neo4j)
        run_examples NEO4J_EXAMPLES "EJEMPLOS NEO4J"
        ;;
    hibrido)
        run_examples HIBRIDO_EXAMPLES "EJEMPLOS HÍBRIDOS"
        ;;
    all)
        run_examples CHROMADB_EXAMPLES "EJEMPLOS CHROMADB"
        run_examples OTROS_EXAMPLES "EJEMPLOS DE GRAFOS (SIN BD)"
        run_examples NEO4J_EXAMPLES "EJEMPLOS NEO4J"
        run_examples HIBRIDO_EXAMPLES "EJEMPLOS HÍBRIDOS"
        ;;
    *)
        echo -e "${RED}Opción no válida: $OPTION${NC}"
        echo "Uso: ./test-ejemplos.sh [chromadb|neo4j|hibrido|all]"
        exit 1
        ;;
esac

# Resumen final
print_header "RESUMEN"

echo -e "Total de ejemplos ejecutados: ${TOTAL}"
echo -e "${GREEN}✓ Pasaron: ${PASSED}${NC}"
echo -e "${RED}✗ Fallaron: ${FAILED}${NC}"

if [ $FAILED -eq 0 ]; then
    echo -e "\n${GREEN}🎉 ¡Todos los ejemplos completados exitosamente!${NC}\n"
    exit 0
else
    echo -e "\n${YELLOW}⚠ Algunos ejemplos fallaron. Revisa los logs arriba.${NC}\n"
    exit 1
fi
