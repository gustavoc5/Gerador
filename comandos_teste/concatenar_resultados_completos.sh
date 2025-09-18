#!/bin/bash
# SCRIPT PARA CONCATENAR RESULTADOS DE TODAS AS 10 SEEDS
# Concatena resultados dos experimentos Simples e Power-Law completos
# IMPORTANTE: Trabalha com 135.000 arquivos CSV individuais (1 por grafo)
# INCLUI TODAS AS MÉTRICAS: tempo, memória, skewness, kurtosis, etc.

# Usar caminho relativo para compatibilidade com Windows/Linux
MAIN_DIR="$(pwd)"
RESULTS_DIR="$MAIN_DIR/resultados_experimentos"

# TODAS AS SEEDS
SEEDS=(1000 2000 3000 4000 5000 6000 7000 8000 9000 10000)

echo "=========================================="
echo "CONCATENAÇÃO COMPLETA DE TODOS OS RESULTADOS"
echo "=========================================="
echo "IMPORTANTE: Sistema trabalha com 135.000 arquivos CSV individuais (1 por grafo)"
echo "INCLUI TODAS AS MÉTRICAS: tempo, memória, skewness, kurtosis, etc."
echo "Data: $(date)"
echo "Diretório: $RESULTS_DIR"
echo "Seeds: ${SEEDS[*]}"
echo ""

# FUNÇÃO PARA CONCATENAR EXPERIMENTO SIMPLES
concatenar_simples() {
    echo "Concatenando experimento Simples..."
    echo "Procurando 90.000 arquivos CSV individuais por seed..."
    echo "INCLUI TODAS AS MÉTRICAS: tempo, memória, skewness, kurtosis, etc."
    
    # Descobrir cabeçalho dinamicamente a partir do primeiro CSV encontrado
    primeiro_csv=""
    for seed in "${SEEDS[@]}"; do
        dir_seed="${RESULTS_DIR}/exp_simples_completo/${seed}"
        if [ -d "$dir_seed" ]; then
            mapfile -t arquivos_iniciais < <(find "$dir_seed" -type f -name "metricas_${seed}_*.csv" | sort)
            if [ ${#arquivos_iniciais[@]} -gt 0 ]; then
                primeiro_csv="${arquivos_iniciais[0]}"
                break
            fi
        fi
    done
    if [ -z "$primeiro_csv" ]; then
        echo "Nenhum CSV Simples encontrado para extrair cabeçalho."
        return
    fi
    # Escrever cabeçalho real no arquivo consolidado
    head -n 1 "$primeiro_csv" > "${RESULTS_DIR}/exp_simples_completo/resultados_simples_completo.csv"
    
    # Concatenação de todas as seeds
    for seed in "${SEEDS[@]}"; do
        diretorio_seed="${RESULTS_DIR}/exp_simples_completo/${seed}"
        
        if [ -d "$diretorio_seed" ]; then
            # Encontrar todos os arquivos CSV da seed
            arquivos_csv=($(find "$diretorio_seed" -name "metricas_${seed}_*.csv" -type f))
            
            if [ ${#arquivos_csv[@]} -gt 0 ]; then
                echo "Seed ${seed} (Simples): Encontrados ${#arquivos_csv[@]} arquivos CSV"
                
                # Concatenar todos os arquivos CSV da seed
                for arquivo in "${arquivos_csv[@]}"; do
                    if [ -f "$arquivo" ]; then
                        # Remove cabeçalho e adiciona dados
                        tail -n +2 "$arquivo" >> "${RESULTS_DIR}/exp_simples_completo/resultados_simples_completo.csv"
                    fi
                done
                
                echo "Seed ${seed} (Simples): OK - ${#arquivos_csv[@]} arquivos processados"
            else
                echo "Seed ${seed} (Simples): NENHUM ARQUIVO CSV ENCONTRADO"
            fi
        else
            echo "Seed ${seed} (Simples): DIRETÓRIO NÃO ENCONTRADO"
        fi
    done
    
    # Estatísticas finais
    total_linhas=$(wc -l < "${RESULTS_DIR}/exp_simples_completo/resultados_simples_completo.csv")
    echo "Total de linhas (Simples): $total_linhas (incluindo cabeçalho)"
    echo ""
}

# FUNÇÃO PARA CONCATENAR EXPERIMENTO POWER-LAW
concatenar_powerlaw() {
    echo "Concatenando experimento Power-Law..."
    echo "Procurando 45.000 arquivos CSV individuais por seed..."
    echo "INCLUI TODAS AS MÉTRICAS: tempo, memória, power-law, etc."
    
    # Descobrir cabeçalho dinamicamente a partir do primeiro CSV encontrado
    primeiro_csv=""
    for seed in "${SEEDS[@]}"; do
        dir_seed="${RESULTS_DIR}/exp_powerlaw_completo/${seed}"
        if [ -d "$dir_seed" ]; then
            mapfile -t arquivos_iniciais < <(find "$dir_seed" -type f -name "metricas_${seed}_*.csv" | sort)
            if [ ${#arquivos_iniciais[@]} -gt 0 ]; then
                primeiro_csv="${arquivos_iniciais[0]}"
                break
            fi
        fi
    done
    if [ -z "$primeiro_csv" ]; then
        echo "Nenhum CSV Power-Law encontrado para extrair cabeçalho."
        return
    fi
    # Escrever cabeçalho real no arquivo consolidado
    head -n 1 "$primeiro_csv" > "${RESULTS_DIR}/exp_powerlaw_completo/resultados_powerlaw_completo.csv"
    
    # Concatenação de todas as seeds
    for seed in "${SEEDS[@]}"; do
        diretorio_seed="${RESULTS_DIR}/exp_powerlaw_completo/${seed}"
        
        if [ -d "$diretorio_seed" ]; then
            # Encontrar todos os arquivos CSV da seed
            arquivos_csv=($(find "$diretorio_seed" -name "metricas_${seed}_*.csv" -type f))
            
            if [ ${#arquivos_csv[@]} -gt 0 ]; then
                echo "Seed ${seed} (Power-Law): Encontrados ${#arquivos_csv[@]} arquivos CSV"
                
                # Concatenar todos os arquivos CSV da seed
                for arquivo in "${arquivos_csv[@]}"; do
                    if [ -f "$arquivo" ]; then
                        # Remove cabeçalho e adiciona dados
                        tail -n +2 "$arquivo" >> "${RESULTS_DIR}/exp_powerlaw_completo/resultados_powerlaw_completo.csv"
                    fi
                done
                
                echo "Seed ${seed} (Power-Law): OK - ${#arquivos_csv[@]} arquivos processados"
            else
                echo "Seed ${seed} (Power-Law): NENHUM ARQUIVO CSV ENCONTRADO"
            fi
        else
            echo "Seed ${seed} (Power-Law): DIRETÓRIO NÃO ENCONTRADO"
        fi
    done
    
    # Estatísticas finais
    total_linhas=$(wc -l < "${RESULTS_DIR}/exp_powerlaw_completo/resultados_powerlaw_completo.csv")
    echo "Total de linhas (Power-Law): $total_linhas (incluindo cabeçalho)"
    echo ""
}

# FUNÇÃO PARA GERAR RESUMO FINAL
gerar_resumo_final() {
    echo "=========================================="
    echo "RESUMO FINAL DA CONCATENAÇÃO"
    echo "=========================================="
    echo "IMPORTANTE: Sistema trabalha com 135.000 arquivos CSV individuais (1 por grafo)"
    echo "INCLUI TODAS AS MÉTRICAS: tempo, memória, skewness, kurtosis, etc."
    echo ""
    
    # Estatísticas dos arquivos finais
    if [ -f "${RESULTS_DIR}/exp_simples_completo/resultados_simples_completo.csv" ]; then
        linhas_simples=$(wc -l < "${RESULTS_DIR}/exp_simples_completo/resultados_simples_completo.csv")
        echo "Simples: ${linhas_simples} linhas (incluindo cabeçalho)"
    fi
    
    if [ -f "${RESULTS_DIR}/exp_powerlaw_completo/resultados_powerlaw_completo.csv" ]; then
        linhas_powerlaw=$(wc -l < "${RESULTS_DIR}/exp_powerlaw_completo/resultados_powerlaw_completo.csv")
        echo "Power-Law: ${linhas_powerlaw} linhas (incluindo cabeçalho)"
    fi
    
    echo ""
    echo "Arquivos finais gerados:"
    echo "  - ${RESULTS_DIR}/exp_simples_completo/resultados_simples_completo.csv"
    echo "  - ${RESULTS_DIR}/exp_powerlaw_completo/resultados_powerlaw_completo.csv"
    echo ""
    echo "MÉTRICAS COMPLETAS INCLUÍDAS:"
    echo ""
    echo "  SIMPLES (${linhas_simples-1} grafos):"
    echo "    - Identificação: gerador, tipo, numV, numA, seed, estrategia_arestas, preferencia_densidade, numC"
    echo "    - Básicas: num_vertices, num_arestas, tipo_detectado, densidade"
    echo "    - Grau: medio, max, min, desvio, mediana, skewness, kurtosis"
    echo "    - Conectividade: num_componentes, conectividade"
    echo "    - Centralidade: PageRank, Closeness, Betweenness (medio, max, min, desvio, mediana)"
    echo "    - Distância: diametro, raio, distancia_media"
    echo "    - Comunidades: greedy e label propagation (numero, modularidade)"
    echo "    - Específicas: razao_vertices_arestas"
    echo "    - Performance: tempo_geracao, memoria_inicial, memoria_pico, memoria_final"
    echo "    - Controle: taxa_sucesso, limite_atingido"
    echo "    - Equivalência: similaridade_media, consistencia_estrutural, outliers"
    echo ""
    echo "  POWER-LAW (${linhas_powerlaw-1} grafos):"
    echo "    - Identificação: gerador, tipo, numV, gamma, seed"
    echo "    - Básicas: num_vertices, num_arestas, tipo_detectado, densidade"
    echo "    - Grau: medio, max, min, desvio, mediana, skewness, kurtosis"
    echo "    - Conectividade: num_componentes, conectividade"
    echo "    - Centralidade: PageRank, Closeness, Betweenness (medio, max, min, desvio, mediana)"
    echo "    - Distância: diametro, raio, distancia_media"
    echo "    - Comunidades: greedy e label propagation (numero, modularidade)"
    echo "    - Power-Law: qualidade_R, pvalue, alpha, xmin, ks_statistic, ks_pvalue"
    echo "    - Performance: tempo_geracao, memoria_inicial, memoria_pico, memoria_final"
    echo "    - Controle: taxa_sucesso, limite_atingido"
    echo ""
    echo "Estrutura de diretórios (1 arquivo CSV por grafo):"
    echo "  ${RESULTS_DIR}/"
    echo "  ├── exp_simples_completo/"
    echo "  │   ├── resultados_simples_completo.csv (arquivo consolidado final)"
    echo "  │   ├── 1000/ (90.000 arquivos CSV individuais)"
    echo "  │   │   ├── metricas_1000_tipo0_v100_dens0_comp0_1.csv"
    echo "  │   │   ├── metricas_1000_tipo0_v100_dens0_comp0_2.csv"
    echo "  │   │   ├── ... (90.000 arquivos CSV)"
    echo "    │   │   └── metricas_1000_tipo31_v1000000_dens2_comp1_50.csv"
    echo "  │   ├── 2000/ (90.000 arquivos CSV individuais)"
    echo "  │   ├── ..."
    echo "  │   └── 10000/ (90.000 arquivos CSV individuais)"
    echo "  └── exp_powerlaw_completo/"
    echo "      ├── resultados_powerlaw_completo.csv (arquivo consolidado final)"
    echo "      ├── 1000/ (45.000 arquivos CSV individuais)"
    echo "      │   ├── metricas_1000_tipo0_v100_gamma2.1_1.csv"
    echo "      │   ├── metricas_1000_tipo0_v100_gamma2.1_2.csv"
    echo "      │   ├── ... (45.000 arquivos CSV)"
    echo "      │   └── metricas_1000_tipo31_v1000000_gamma3.0_50.csv"
    echo "      ├── 2000/ (45.000 arquivos CSV individuais)"
    echo "      ├── ..."
    echo "      └── 10000/ (45.000 arquivos CSV individuais)"
    echo ""
    echo "VANTAGENS DA PARALELIZAÇÃO REAL:"
    echo "  - Cada execução gera arquivos CSV ÚNICOS"
    echo "  - NÃO há condições de corrida"
    echo "  - Execução verdadeiramente paralela"
    echo "  - 1 arquivo CSV por grafo = 135.000 arquivos individuais"
    echo "  - Nomes descritivos com parâmetros"
    echo "  - Fácil análise individual ou consolidada"
    echo "  - TODAS AS MÉTRICAS incluídas (tempo, memória, skewness, kurtosis, etc.)"
    echo ""
    echo "Concatenação concluída com sucesso!"
}

# FUNÇÃO PRINCIPAL
main() {
    echo "Iniciando processo de concatenação..."
    echo "IMPORTANTE: Sistema trabalha com 135.000 arquivos CSV individuais (1 por grafo)"
    echo "INCLUI TODAS AS MÉTRICAS: tempo, memória, skewness, kurtosis, etc."
    echo ""
    
    # Verificar se os diretórios existem
    if [ ! -d "${RESULTS_DIR}/exp_simples_completo" ]; then
        echo "ERRO: Diretório exp_simples_completo não encontrado!"
        exit 1
    fi
    
    if [ ! -d "${RESULTS_DIR}/exp_powerlaw_completo" ]; then
        echo "ERRO: Diretório exp_powerlaw_completo não encontrado!"
        exit 1
    fi
    
    # Executar concatenações
    concatenar_simples
    concatenar_powerlaw
    
    # Gerar resumo final
    gerar_resumo_final
}

# EXECUTAR FUNÇÃO PRINCIPAL
main
