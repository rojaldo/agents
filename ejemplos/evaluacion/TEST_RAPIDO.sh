#!/bin/bash

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     TEST RÁPIDO: Verifica que todos los ejemplos funcionan ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

cd /home/rojaldo/cursos/agents/ejemplos/evaluacion/

tests_passed=0
tests_failed=0

# Función para ejecutar un test
run_test() {
    local name=$1
    local file=$2
    
    echo "▶ Probando: $name..."
    
    if python "$file" > /dev/null 2>&1; then
        echo "  ✅ PASS: $name"
        ((tests_passed++))
    else
        echo "  ❌ FAIL: $name"
        ((tests_failed++))
    fi
    echo ""
}

# Ejecutar tests
run_test "Módulo 1: Métricas" "01_metricas_desempeno.py"
run_test "Módulo 2: Benchmarks" "02_benchmarks_datasets.py"
run_test "Módulo 3: Testing" "03_testing_agentes.py"
run_test "Módulo 4: Comportamiento" "04_testing_comportamiento.py"
run_test "Módulo 5: Debugging" "05_debugging_agentes.py"
run_test "Módulo 6: LLM Juez" "06_llm_como_juez.py"

# Resumen
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                        RESULTADO                          ║"
echo "╠════════════════════════════════════════════════════════════╣"
echo "║ Tests pasados:  $tests_passed/6 ✅                        "
echo "║ Tests fallidos: $tests_failed/6 ❌                        "
echo "╚════════════════════════════════════════════════════════════╝"

if [ $tests_failed -eq 0 ]; then
    echo ""
    echo "🎉 ¡TODOS LOS EJEMPLOS FUNCIONAN CORRECTAMENTE!"
    echo ""
    echo "Próximos pasos:"
    echo "  1. Lee: README.md"
    echo "  2. Lee: GUIA_EVALUACION_AGENTES.md"
    echo "  3. Ejecuta uno a uno: python 0X_*.py"
    echo ""
    exit 0
else
    echo ""
    echo "⚠️  Algunos ejemplos fallaron."
    echo "Verifica la instalación de dependencias."
    echo ""
    exit 1
fi
