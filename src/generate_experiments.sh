#!/bin/bash

# Script para gerar comandos de experimentos paralelos
# Baseado no exemplo fornecido pelo usuário

# Configurações
MAIN_DIR="/home/user/projects/graph_generation/results"
SEEDS=(123 456 789 101 202 303 404 505)
SIZES=(10 20 50 100)
EXECUCOES=1

# Função para gerar comandos simples
generate_simples() {
    echo "# Comandos para módulo simples"
    echo "# Gerado em: $(date)"
    echo ""
    
    for seed in "${SEEDS[@]}"; do
        for size in "${SIZES[@]}"; do
            for exec in $(seq 1 $EXECUCOES); do
                # Cria diretório baseado na seed
                echo "mkdir -p $MAIN_DIR/simples/$seed"
                
                # Comando de execução
                echo "python src/simples/test_simples.py --seed $seed --vertices_lista $size &> $MAIN_DIR/simples/$seed/size${size}_exec${exec}.txt"
                echo ""
            done
        done
    done
}

# Função para gerar comandos powerlaw
generate_powerlaw() {
    echo "# Comandos para módulo powerlaw"
    echo "# Gerado em: $(date)"
    echo ""
    
    for seed in "${SEEDS[@]}"; do
        for size in "${SIZES[@]}"; do
            for exec in $(seq 1 $EXECUCOES); do
                # Cria diretório baseado na seed
                echo "mkdir -p $MAIN_DIR/powerlaw/$seed"
                
                # Comando de execução
                echo "python src/powerlaw/test_pwl.py --seed $seed --vertices_lista $size &> $MAIN_DIR/powerlaw/$seed/size${size}_exec${exec}.txt"
                echo ""
            done
        done
    done
}

# Função para gerar comandos combinados
generate_combined() {
    echo "# Comandos para ambos os módulos"
    echo "# Gerado em: $(date)"
    echo ""
    
    for seed in "${SEEDS[@]}"; do
        for size in "${SIZES[@]}"; do
            for exec in $(seq 1 $EXECUCOES); do
                # Cria diretórios baseados na seed
                echo "mkdir -p $MAIN_DIR/simples/$seed"
                echo "mkdir -p $MAIN_DIR/powerlaw/$seed"
                
                # Comandos de execução
                echo "python src/simples/test_simples.py --seed $seed --vertices_lista $size &> $MAIN_DIR/simples/$seed/size${size}_exec${exec}.txt"
                echo "python src/powerlaw/test_pwl.py --seed $seed --vertices_lista $size &> $MAIN_DIR/powerlaw/$seed/size${size}_exec${exec}.txt"
                echo ""
            done
        done
    done
}

# Função principal
main() {
    local module=${1:-"both"}
    local output_file=${2:-"experiments_$(date +%Y%m%d_%H%M%S).sh"}
    
    echo "🚀 Gerando experimentos para módulo: $module"
    echo "📁 Diretório principal: $MAIN_DIR"
    echo "🌱 Seeds: ${SEEDS[*]}"
    echo "📊 Tamanhos: ${SIZES[*]}"
    echo "🔄 Execuções: $EXECUCOES"
    echo "📄 Arquivo de saída: $output_file"
    echo ""
    
    # Calcula total de experimentos
    local total_experiments=$((${#SEEDS[@]} * ${#SIZES[@]} * EXECUCOES))
    if [ "$module" = "both" ]; then
        total_experiments=$((total_experiments * 2))
    fi
    
    echo "🎯 Total de experimentos: $total_experiments"
    echo "============================================================"
    
    # Gera comandos baseado no módulo
    case $module in
        "simples")
            generate_simples > "$output_file"
            ;;
        "powerlaw")
            generate_powerlaw > "$output_file"
            ;;
        "both"|*)
            generate_combined > "$output_file"
            ;;
    esac
    
    # Torna o arquivo executável
    chmod +x "$output_file"
    
    echo "✅ Script gerado com sucesso: $output_file"
    echo "📋 Para executar: bash $output_file"
    echo "🔄 Para executar em paralelo: parallel -j <num_cores> < $output_file"
}

# Verifica argumentos
if [ $# -eq 0 ]; then
    echo "Uso: $0 [simples|powerlaw|both] [arquivo_saida]"
    echo ""
    echo "Exemplos:"
    echo "  $0 simples"
    echo "  $0 powerlaw"
    echo "  $0 both experiments.sh"
    echo ""
    echo "Configurações atuais:"
    echo "  MAIN_DIR: $MAIN_DIR"
    echo "  SEEDS: ${SEEDS[*]}"
    echo "  SIZES: ${SIZES[*]}"
    echo "  EXECUCOES: $EXECUCOES"
    exit 1
fi

# Executa função principal
main "$@" 