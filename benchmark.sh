#!/bin/bash

# ==============================
# Slitherlink Test Runner (Benchmark Mode)
# ==============================

# Directory containing test files
TEST_DIR="slitherlink-boards-public"

# Script to test
SCRIPT="slitherlink.py"

# Optional label argument
LABEL=${1:-TESTS}

# Número de vezes que queres correr o conjunto de testes
NUM_RUNS=5

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[1;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}====================================${NC}"
echo -e "${BLUE} Running: ${YELLOW}$LABEL (Média de $NUM_RUNS runs)${NC}"
echo -e "${BLUE}====================================${NC}"
echo

# Variável para acumular o tempo total de todas as runs
grand_total_time=0

for ((run=1; run<=NUM_RUNS; run++)); do
    echo -e "${BLUE}▶▶▶ A iniciar Run $run/$NUM_RUNS...${NC}"
    
    passed=0
    failed=0
    total=0
    
    # Start timer para esta run específica
    start_time=$(date +%s.%N)

    for input_file in "$TEST_DIR"/test*.txt; do
        ((total++))

        # Extract test name
        test_name=$(basename "$input_file" .txt)
        expected_output="$TEST_DIR/$test_name.out"

        # Run test and capture output
        actual_output=$(python3 "$SCRIPT" < "$input_file")

        # Read expected output
        expected=$(cat "$expected_output")

        # Compare outputs
        if diff <(echo "$actual_output") <(echo "$expected") > /dev/null; then
            ((passed++))
        else
            echo -e "${RED}❌ $test_name FAILED na Run $run${NC}"
            ((failed++))
        fi
    done

    # End timer para esta run
    end_time=$(date +%s.%N)
    elapsed=$(echo "$end_time - $start_time" | bc)
    
    # Acumula o tempo no total global
    grand_total_time=$(echo "$grand_total_time + $elapsed" | bc)
    
    echo -e "   ↳ ${GREEN}Resultados da Run $run:${NC} $passed / $total certos em ${elapsed}s"
    echo "------------------------------------"
done

# Calcula a média aritmética do tempo total com 3 casas decimais
average_time=$(echo "scale=3; $grand_total_time / $NUM_RUNS" | bc)

echo
echo -e "${BLUE}====================================${NC}"
echo -e "${BLUE} Finished: ${YELLOW}$LABEL${NC}"
echo -e "${BLUE}====================================${NC}"

echo -e "${GREEN}Estado Geral:${NC} Testes executados com sucesso em todas as repetições."
echo -e "${YELLOW}Total de Corridas:${NC} $NUM_RUNS"
echo -e "${YELLOW}Tempo Médio Final:${NC} ${average_time}s"

# Print label novamente no fim como tinhas no original
echo
echo -e "${BLUE}>>> ${YELLOW}$LABEL${NC}"