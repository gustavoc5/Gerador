#!/bin/bash

# Configurações principais
MAIN_DIR="$(pwd)"
SIMPLES_EXE="$MAIN_DIR/simples/test_simples.py"
POWERLAW_EXE="$MAIN_DIR/powerlaw/test_pwl.py"
RESULTS_DIR="$MAIN_DIR/results"

# Seeds para os experimentos (mesmas do exemplo)
SEEDS=(270001 341099 160812 713978 705319 219373 255486 135848 142095 571618
2199149535 4178555405 2827217920 59891126 3373722980 2876174150 2287038545
3681872705 1896279216 3550610394 537193474 3500110090 2694679745 3512663495
3082165489 3077898063 464010461 1981280707 1053668570 3538661238)

# Tamanhos dos grafos
SIZES=(100 500 1000 5000)

# Número de execuções por configuração
EXECUCOES=5

# Módulo a executar (simples, powerlaw, ou both)
MODULE="both"

# Função para gerar experimentos do módulo simples
generate_simples() {
    echo "# Experimentos do módulo Simples"
    echo "# Gerado em: $(date)"
    echo "# Total de experimentos: $(( ${#SEEDS[@]} * ${#SIZES[@]} * EXECUCOES ))"
    echo ""
    
    for seed in "${SEEDS[@]}"
    do
        for size in "${SIZES[@]}"
        do
            for execucao in $(seq 1 $EXECUCOES)
            do
                # Cria diretório baseado na seed
                results="$RESULTS_DIR/simples/$seed"
                if [ ! -e "$results" ]
                then
                    echo "mkdir -p $results"
                fi
                
                # Gera comando com saída única
                echo "python $SIMPLES_EXE 1 $size &> $results/size${size}_exec${execucao}.txt"
            done
        done
    done
}

# Função para gerar experimentos do módulo powerlaw
generate_powerlaw() {
    echo "# Experimentos do módulo Power-Law"
    echo "# Gerado em: $(date)"
    echo "# Total de experimentos: $(( ${#SEEDS[@]} * ${#SIZES[@]} * EXECUCOES ))"
    echo ""
    
    for seed in "${SEEDS[@]}"
    do
        for size in "${SIZES[@]}"
        do
            for execucao in $(seq 1 $EXECUCOES)
            do
                # Cria diretório baseado na seed
                results="$RESULTS_DIR/powerlaw/$seed"
                if [ ! -e "$results" ]
                then
                    echo "mkdir -p $results"
                fi
                
                # Gera comando com saída única
                echo "python $POWERLAW_EXE 1 $size &> $results/size${size}_exec${execucao}.txt"
            done
        done
    done
}

# Função para gerar experimentos de ambos os módulos
generate_both() {
    echo "# Experimentos dos módulos Simples e Power-Law"
    echo "# Gerado em: $(date)"
    echo "# Total de experimentos: $(( ${#SEEDS[@]} * ${#SIZES[@]} * EXECUCOES * 2 ))"
    echo ""
    
    for seed in "${SEEDS[@]}"
    do
        for size in "${SIZES[@]}"
        do
            for execucao in $(seq 1 $EXECUCOES)
            do
                # Diretórios baseados na seed
                simples_results="$RESULTS_DIR/simples/$seed"
                powerlaw_results="$RESULTS_DIR/powerlaw/$seed"
                
                # Cria diretórios se não existirem
                if [ ! -e "$simples_results" ]
                then
                    echo "mkdir -p $simples_results"
                fi
                if [ ! -e "$powerlaw_results" ]
                then
                    echo "mkdir -p $powerlaw_results"
                fi
                
                # Comandos para ambos os módulos
                echo "python $SIMPLES_EXE 1 $size &> $simples_results/size${size}_exec${execucao}.txt"
                echo "python $POWERLAW_EXE 1 $size &> $powerlaw_results/size${size}_exec${execucao}.txt"
            done
        done
    done
}

# Função para concatenar resultados
concatenate_results() {
    echo "# Script para concatenar resultados"
    echo "# Gerado em: $(date)"
    echo ""
    
    echo "echo 'Concatenando resultados do módulo Simples...'"
    echo "for seed in ${SEEDS[@]}; do"
    echo "    if [ -d \"$RESULTS_DIR/simples/\$seed\" ]; then"
    echo "        cat $RESULTS_DIR/simples/\$seed/*.txt > $RESULTS_DIR/simples_concatenated_\$seed.txt"
    echo "    fi"
    echo "done"
    echo ""
    
    echo "echo 'Concatenando resultados do módulo Power-Law...'"
    echo "for seed in ${SEEDS[@]}; do"
    echo "    if [ -d \"$RESULTS_DIR/powerlaw/\$seed\" ]; then"
    echo "        cat $RESULTS_DIR/powerlaw/\$seed/*.txt > $RESULTS_DIR/powerlaw_concatenated_\$seed.txt"
    echo "    fi"
    echo "done"
    echo ""
    
    echo "echo 'Concatenação concluída!'"
}

# Função principal
main() {
    case $MODULE in
        "simples")
            generate_simples
            ;;
        "powerlaw")
            generate_powerlaw
            ;;
        "both")
            generate_both
            ;;
        *)
            echo "Módulo inválido: $MODULE"
            echo "Use: simples, powerlaw, ou both"
            exit 1
            ;;
    esac
}

# Executa função principal
main

# Gera script de concatenação separado
concatenate_results > concatenate_results.sh
chmod +x concatenate_results.sh

echo "# Script de concatenação gerado: concatenate_results.sh"
echo "# Para executar: bash concatenate_results.sh" 