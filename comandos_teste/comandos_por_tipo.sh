#!/bin/bash

# SCRIPT PARA EXECUÇÃO PARALELA POR TIPO DE GRAFO
# Gera comandos para executar experimentos com granularidade por tipo
# Total: 120 comandos (10 seeds × 6 tipos × 2 experimentos)
# Vantagem: Processos menores, menos falhas, melhor aproveitamento das máquinas

# CONFIGURAÇÕES PRINCIPAIS
MAIN_DIR="$(pwd)"
PYTHON_EXE="python"
EXPERIMENTO_SIMPLES="$MAIN_DIR/src/experimentos/simples.py"
EXPERIMENTO_POWERLAW="$MAIN_DIR/src/experimentos/power_law.py"
RESULTS_DIR="$MAIN_DIR/resultados_experimentos"

# TODAS AS SEEDS (10 seeds para reprodutibilidade completa)
SEEDS=(1000 2000 3000 4000 5000 6000 7000 8000 9000 10000)

# TODOS OS TIPOS (6 tipos de grafos)
TIPOS=(0 1 20 21 30 31)

# Modo SMOKE opcional: defina SMOKE=1 para reduzir parâmetros e grafos
SMOKE_FLAG=""
if [[ "${SMOKE}" == "1" ]]; then
    SMOKE_FLAG="--smoke --num_grafos 2"
fi

echo "# COMANDOS PARA EXECUÇÃO PARALELA POR TIPO - ESTRATÉGIA GRANULAR"
echo "# IMPORTANTE: Cada execução processa 1 tipo de grafo por seed"
echo "# Total de seeds: ${#SEEDS[@]}"
echo "# Total de tipos: ${#TIPOS[@]}"
echo "# Total de comandos: $(( ${#SEEDS[@]} * ${#TIPOS[@]} * 2 ))"
echo "# Simples: 10 seeds × 6 tipos = 60 comandos"
echo "# Power-Law: 10 seeds × 6 tipos = 60 comandos"
echo "# Total: 120 comandos"
echo "# VANTAGEM: Processos menores = menos falhas, melhor paralelização"
echo ""

# FUNÇÃO PARA GERAR COMANDOS DE UMA SEED E TIPO
gerar_comando_tipo() {
    local seed=$1
    local tipo=$2
    local experimento=$3
    local nome_experimento=$4
    
    echo "# ========================================="
    echo "# SEED: $seed | TIPO: $tipo | EXPERIMENTO: $nome_experimento"
    echo "# ========================================="
    echo ""
    
    # 1. CRIAR DIRETÓRIO PARA A COMBINAÇÃO
    echo "# Criando diretório para seed $seed, tipo $tipo, $nome_experimento"
    echo "mkdir -p \"$RESULTS_DIR/exp_${nome_experimento}_por_tipo/${seed}_tipo${tipo}\""
    echo ""
    
    # 2. EXECUTAR EXPERIMENTO ESPECÍFICO
    echo "# $nome_experimento - Seed $seed, Tipo $tipo"
    echo "# Processa apenas 1 tipo de grafo (granularidade alta)"
    echo "# ESTRUTURA: metricas_{seed}_tipo{tipo}_v{vertices}_dens{densidade}_comp{componentes}_{numero}.csv"
    echo "# LIMITES: Apenas timeout de 2h (threads e memória livres)"
    echo "timeout 7200 $PYTHON_EXE \"$EXPERIMENTO_SIMPLES\" \\
    --output_dir \"$RESULTS_DIR/exp_${nome_experimento}_por_tipo/${seed}_tipo${tipo}\" \\
    --seeds $seed \\
    --tipos $tipo \\
    --output_format individual_csv \\
    --naming_pattern 'metricas_{seed}_tipo{tipo}_v{vertices}_dens{densidade}_comp{componentes}_{numero}.csv' \\
    $SMOKE_FLAG \\
    &> \"$RESULTS_DIR/exp_${nome_experimento}_por_tipo/${seed}_tipo${tipo}/log_${seed}_tipo${tipo}_\$(date +%Y%m%d_%H%M%S).txt\""
    echo ""
    
    echo "# ========================================="
    echo ""
}

# FUNÇÃO PARA GERAR RESUMO FINAL
gerar_resumo() {
    echo "# ========================================="
    echo "# RESUMO DOS COMANDOS GERADOS"
    echo "# ========================================="
    echo "#"
    echo "# ESTRATÉGIA: Granularidade por tipo de grafo"
    echo "# VANTAGENS:"
    echo "# - Processos menores (20min vs 2h)"
    echo "# - Menos falhas (Exitval 0)"
    echo "# - Melhor aproveitamento (120/200 máquinas = 60%)"
    echo "# - Fácil debug (1 tipo por processo)"
    echo "#"
    echo "# Para executar TODOS os experimentos em paralelo:"
    echo "#"
    echo "# 1. Salvar este script como 'comandos_por_tipo.sh'"
    echo "# 2. Executar: bash comandos_por_tipo.sh > comandos_execucao.sh"
    echo "# 3. Executar em paralelo:"
    echo "#    - Com 120 threads: cat comandos_execucao.sh | parallel -j 120"
    echo "#    - Com 200 threads: cat comandos_execucao.sh | parallel -j 200"
    echo "#    - Com GNU parallel: parallel -j 120 < comandos_execucao.sh"
    echo "#"
    echo "# 4. Após execução, concatenar resultados:"
    echo "#    bash \"$MAIN_DIR/comandos_teste/concatenar_resultados_por_tipo.sh\""
    echo "#"
    echo "# ESTRUTURA FINAL DE DIRETÓRIOS:"
    echo "# $RESULTS_DIR/"
    echo "# ├── exp_simples_por_tipo/"
    echo "# │   ├── 1000_tipo0/  (30 combinações: 5 tamanhos × 3 densidades × 2 componentes)"
    echo "# │   ├── 1000_tipo1/  (30 combinações)"
    echo "# │   ├── 1000_tipo20/ (30 combinações)"
    echo "# │   ├── 1000_tipo21/ (30 combinações)"
    echo "# │   ├── 1000_tipo30/ (30 combinações)"
    echo "# │   ├── 1000_tipo31/ (30 combinações)"
    echo "# │   ├── 2000_tipo0/  (30 combinações)"
    echo "# │   └── ... (até 10000_tipo31)"
    echo "# └── exp_powerlaw_por_tipo/"
    echo "#     ├── 1000_tipo0/  (15 combinações: 5 tamanhos × 3 gammas)"
    echo "#     ├── 1000_tipo1/  (15 combinações)"
    echo "#     └── ... (até 10000_tipo31)"
    echo "#"
    echo "# VANTAGENS DA GRANULARIDADE POR TIPO:"
    echo "# - 120 comandos vs 20 comandos (6x mais granularidade)"
    echo "# - Processos menores = menos chance de falha"
    echo "# - Melhor distribuição entre máquinas"
    echo "# - Debug mais fácil (1 tipo por processo)"
    echo "# - Aproveitamento de 60% das máquinas (120/200)"
    echo "#"
    echo "# TOTAL: 120 comandos para 2.700 testes (mesmo número de testes!)"
    echo "#"
    echo "# Smoke test mínimo (rápido):"
    echo "#   export SMOKE=1; bash comandos_por_tipo.sh > comandos_execucao.sh; parallel -j 12 < comandos_execucao.sh"
    echo "# ========================================="
}

# FUNÇÃO PRINCIPAL
main() {
    echo "# SISTEMA DE EXPERIMENTOS POR TIPO - GERAÇÃO DE COMANDOS"
    echo "# IMPORTANTE: Cada execução processa 1 tipo de grafo por seed"
    echo "# Data: $(date)"
    echo "# Diretório principal: $MAIN_DIR"
    echo "# Resultados: $RESULTS_DIR"
    echo "# Seeds: ${SEEDS[*]}"
    echo "# Tipos: ${TIPOS[*]}"
    echo "#"
    
    # Gerar comandos para cada combinação (seed, tipo, experimento)
    for seed in "${SEEDS[@]}"; do
        for tipo in "${TIPOS[@]}"; do
            # Simples
            gerar_comando_tipo "$seed" "$tipo" "$EXPERIMENTO_SIMPLES" "simples"
        done
    done
    
    for seed in "${SEEDS[@]}"; do
        for tipo in "${TIPOS[@]}"; do
            # Power-Law
            gerar_comando_tipo "$seed" "$tipo" "$EXPERIMENTO_POWERLAW" "powerlaw"
        done
    done
    
    # Gerar resumo final
    gerar_resumo
}

# EXECUTAR FUNÇÃO PRINCIPAL
main

echo "# Script de geração de comandos por tipo concluído!"
echo "# IMPORTANTE: Cada execução processa 1 tipo de grafo por seed"
echo "# Execute: bash $0 > comandos_execucao.sh"
echo "# Depois execute: cat comandos_execucao.sh | parallel -j 120"
