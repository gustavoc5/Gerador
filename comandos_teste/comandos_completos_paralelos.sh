#!/bin/bash

# SCRIPT COMPLETO PARA EXECUÇÃO PARALELA DE TODOS OS EXPERIMENTOS
# Gera comandos para executar TODOS os 2.700 testes (1.800 Simples + 900 Power-Law)
# Total: 135.000 grafos (90.000 Simples + 45.000 Power-Law)
# IMPORTANTE: Cada execução gera 1 arquivo CSV por grafo para paralelização REAL

# CONFIGURAÇÕES PRINCIPAIS
# Usar caminho relativo para compatibilidade com Windows/Linux
MAIN_DIR="$(pwd)"
PYTHON_EXE="python"
EXPERIMENTO_SIMPLES="$MAIN_DIR/src/experimentos/simples.py"
EXPERIMENTO_POWERLAW="$MAIN_DIR/src/experimentos/powerlaw.py"
RESULTS_DIR="$MAIN_DIR/resultados_experimentos"

# TODAS AS SEEDS (10 seeds para reprodutibilidade completa)
SEEDS=(1000 2000 3000 4000 5000 6000 7000 8000 9000 10000)

# PARÂMETROS DOS EXPERIMENTOS
# Simples: 6 tipos × 5 tamanhos × 3 densidades × 2 componentes × 10 seeds = 1.800 testes
# Power-Law: 6 tipos × 5 tamanhos × 3 gammas × 10 seeds = 900 testes
# Total: 2.700 testes × 50 grafos = 135.000 grafos

echo "# COMANDOS PARA EXECUÇÃO PARALELA COMPLETA - TODOS OS EXPERIMENTOS"
echo "# IMPORTANTE: Cada execução gera 1 arquivo CSV por grafo (135.000 arquivos individuais)"
echo "# Total de seeds: ${#SEEDS[@]}"
echo "# Total de comandos: $(( ${#SEEDS[@]} * 2 ))"
echo "# Simples tests per seed: 1.800"
echo "# Power-Law tests per seed: 900"
echo "# Simples graphs per seed: 90.000"
echo "# Power-Law graphs per seed: 45.000"
echo "# Total de testes: 2.700"
echo "# Total de grafos: 135.000"
echo "# ESTRUTURA: 1 arquivo CSV por grafo com nomes descritivos"
echo ""

# FUNÇÃO PARA GERAR COMANDOS DE UMA SEED
gerar_comandos_seed() {
    local seed=$1
    
    echo "# ========================================="
    echo "# SEED: $seed"
    echo "# ========================================="
    echo ""
    
    # 1. CRIAR DIRETÓRIOS PARA A SEED
    echo "# Criando diretórios para seed $seed"
    echo "mkdir -p \"$RESULTS_DIR/exp_simples_completo/$seed\""
    echo "mkdir -p \"$RESULTS_DIR/exp_powerlaw_completo/$seed\""
    echo ""
    
    # 2. EXECUTAR EXPERIMENTO SIMPLES COMPLETO
    echo "# Experimento Simples Completo - Seed $seed"
    echo "# 1.800 testes × 50 grafos = 90.000 arquivos CSV individuais"
    echo "# ESTRUTURA: metricas_{seed}_tipo{tipo}_v{vertices}_dens{densidade}_comp{componentes}_{numero}.csv"
    echo "$PYTHON_EXE \"$EXPERIMENTO_SIMPLES\" \\"
    echo "    --output_dir \"$RESULTS_DIR/exp_simples_completo/$seed\" \\"
    echo "    --seeds $seed \\"
    echo "    --output_format individual_csv \\"
    echo "    --naming_pattern 'metricas_{seed}_tipo{tipo}_v{vertices}_dens{densidade}_comp{componentes}_{numero}.csv' \\"
    echo "    &> \"$RESULTS_DIR/exp_simples_completo/$seed/log_${seed}_\$(date +%Y%m%d_%H%M%S).txt\""
    echo ""
    
    # 3. EXECUTAR EXPERIMENTO POWER-LAW COMPLETO
    echo "# Experimento Power-Law Completo - Seed $seed"
    echo "# 900 testes × 50 grafos = 45.000 arquivos CSV individuais"
    echo "# ESTRUTURA: metricas_{seed}_tipo{tipo}_v{vertices}_gamma{gamma}_{numero}.csv"
    echo "$PYTHON_EXE \"$EXPERIMENTO_POWERLAW\" \\"
    echo "    --output_dir \"$RESULTS_DIR/exp_powerlaw_completo/$seed\" \\"
    echo "    --seeds $seed \\"
    echo "    --output_format individual_csv \\"
    echo "    --naming_pattern 'metricas_{seed}_tipo{tipo}_v{vertices}_gamma{gamma}_{numero}.csv' \\"
    echo "    &> \"$RESULTS_DIR/exp_powerlaw_completo/$seed/log_${seed}_\$(date +%Y%m%d_%H%M%S).txt\""
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
    echo "# IMPORTANTE: Sistema gera 1 arquivo CSV por grafo (135.000 arquivos individuais)"
    echo "#"
    echo "# Para executar TODOS os experimentos em paralelo:"
    echo "#"
    echo "# 1. Salvar este script como 'comandos_completos.sh'"
    echo "# 2. Executar: bash comandos_completos.sh > comandos_execucao.sh"
    echo "# 3. Executar em paralelo:"
    echo "#    - Com 4 threads: cat comandos_execucao.sh | parallel -j 4"
    echo "#    - Com todos os cores: cat comandos_execucao.sh | parallel -j \$(nproc)"
    echo "#    - Com GNU parallel: parallel -j 4 < comandos_execucao.sh"
    echo "#"
    echo "# 4. Após execução, concatenar resultados:"
    echo "#    bash \"$MAIN_DIR/comandos_teste/concatenar_resultados_completos.sh\""
    echo "#"
    echo "# ESTRUTURA FINAL DE DIRETÓRIOS (1 arquivo CSV por grafo):"
    echo "# $RESULTS_DIR/"
    echo "# ├── exp_simples_completo/"
    echo "# │   ├── 1000/  (90.000 arquivos CSV individuais)"
    echo "# │   │   ├── metricas_1000_tipo0_v100_dens0_comp0_1.csv"
    echo "# │   │   ├── metricas_1000_tipo0_v100_dens0_comp0_2.csv"
    echo "# │   │   ├── ... (90.000 arquivos CSV)"
    echo "# │   │   └── metricas_1000_tipo31_v1000000_dens2_comp1_50.csv"
    echo "# │   ├── 2000/  (90.000 arquivos CSV individuais)"
    echo "# │   ├── ..."
    echo "# │   └── 10000/ (90.000 arquivos CSV individuais)"
    echo "# └── exp_powerlaw_completo/"
    echo "#     ├── 1000/  (45.000 arquivos CSV individuais)"
    echo "#     │   ├── metricas_1000_tipo0_v100_gamma2.1_1.csv"
    echo "#     │   ├── metricas_1000_tipo0_v100_gamma2.1_2.csv"
    echo "#     │   ├── ... (45.000 arquivos CSV)"
    echo "#     │   └── metricas_1000_tipo31_v1000000_gamma3.0_50.csv"
    echo "#     ├── 2000/  (45.000 arquivos CSV individuais)"
    echo "#     ├── ..."
    echo "#     └── 10000/ (45.000 arquivos CSV individuais)"
    echo "#"
    echo "# VANTAGENS DA PARALELIZAÇÃO REAL:"
    echo "# - Cada execução gera arquivos CSV ÚNICOS"
    echo "# - NÃO há condições de corrida"
    echo "# - Execução verdadeiramente paralela"
    echo "# - 1 arquivo CSV por grafo = 135.000 arquivos individuais"
    echo "# - Nomes descritivos com parâmetros"
    echo "#"
    echo "# TOTAL: 135.000 arquivos CSV individuais em 2.700 testes"
    echo "# ========================================="
}

# FUNÇÃO PRINCIPAL
main() {
    echo "# SISTEMA DE EXPERIMENTOS COMPLETO - GERAÇÃO DE COMANDOS"
    echo "# IMPORTANTE: Sistema gera 1 arquivo CSV por grafo (135.000 arquivos individuais)"
    echo "# Data: $(date)"
    echo "# Diretório principal: $MAIN_DIR"
    echo "# Resultados: $RESULTS_DIR"
    echo "# Seeds: ${SEEDS[*]}"
    echo "#"
    
    # Gerar comandos para cada seed
    for seed in "${SEEDS[@]}"; do
        gerar_comandos_seed "$seed"
    done
    
    # Gerar resumo final
    gerar_resumo
}

# EXECUTAR FUNÇÃO PRINCIPAL
main

echo "# Script de geração de comandos concluído!"
echo "# IMPORTANTE: Sistema gera 1 arquivo CSV por grafo (135.000 arquivos individuais)"
echo "# Execute: bash $0 > comandos_execucao.sh"
echo "# Depois execute: cat comandos_execucao.sh | parallel -j 4"
