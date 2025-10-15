#!/bin/bash
# SCRIPT PARA CONCATENAR RESULTADOS DE TODAS AS SEEDS

MAIN_DIR="/mnt/c/Users/gusta/OneDrive/GUSTAVO/Unifei/TCC/Gerador"
echo "Concatenando resultados..."

# CONCATENAÇÃO EXPERIMENTO SIMPLES
echo "Concatenando experimento Simples..."
cat > ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv << 'EOF'
gerador,tipo,numV,numA,seed,estrategia_arestas,preferencia_densidade,numC,num_grafos_gerados
EOF

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/2700001/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/2700001/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 2700001 (Simples): OK"
else
    echo "Seed 2700001 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/3170702080/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/3170702080/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 3170702080 (Simples): OK"
else
    echo "Seed 3170702080 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/3548644859/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/3548644859/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 3548644859 (Simples): OK"
else
    echo "Seed 3548644859 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/1033592630/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/1033592630/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 1033592630 (Simples): OK"
else
    echo "Seed 1033592630 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/9263589860/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/9263589860/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 9263589860 (Simples): OK"
else
    echo "Seed 9263589860 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/1883634842/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/1883634842/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 1883634842 (Simples): OK"
else
    echo "Seed 1883634842 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/7648101510/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/7648101510/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 7648101510 (Simples): OK"
else
    echo "Seed 7648101510 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/1502014705/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/1502014705/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 1502014705 (Simples): OK"
else
    echo "Seed 1502014705 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/7214842310/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/7214842310/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 7214842310 (Simples): OK"
else
    echo "Seed 7214842310 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/2606453957/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/2606453957/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 2606453957 (Simples): OK"
else
    echo "Seed 2606453957 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/4194499680/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/4194499680/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 4194499680 (Simples): OK"
else
    echo "Seed 4194499680 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/2779365847/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/2779365847/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 2779365847 (Simples): OK"
else
    echo "Seed 2779365847 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/1094121244/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/1094121244/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 1094121244 (Simples): OK"
else
    echo "Seed 1094121244 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/1090525961/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/1090525961/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 1090525961 (Simples): OK"
else
    echo "Seed 1090525961 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/3310223418/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/3310223418/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 3310223418 (Simples): OK"
else
    echo "Seed 3310223418 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/604827988/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/604827988/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 604827988 (Simples): OK"
else
    echo "Seed 604827988 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/1549035388/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/1549035388/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 1549035388 (Simples): OK"
else
    echo "Seed 1549035388 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/795578792/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/795578792/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 795578792 (Simples): OK"
else
    echo "Seed 795578792 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/182649370/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/182649370/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 182649370 (Simples): OK"
else
    echo "Seed 182649370 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/1127200130/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/1127200130/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 1127200130 (Simples): OK"
else
    echo "Seed 1127200130 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/332728275/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/332728275/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 332728275 (Simples): OK"
else
    echo "Seed 332728275 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/1477598055/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/1477598055/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 1477598055 (Simples): OK"
else
    echo "Seed 1477598055 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/1157679575/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/1157679575/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 1157679575 (Simples): OK"
else
    echo "Seed 1157679575 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/3489403805/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/3489403805/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 3489403805 (Simples): OK"
else
    echo "Seed 3489403805 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/359655529/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/359655529/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 359655529 (Simples): OK"
else
    echo "Seed 359655529 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/3107219804/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/3107219804/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 3107219804 (Simples): OK"
else
    echo "Seed 3107219804 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/911079554/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/911079554/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 911079554 (Simples): OK"
else
    echo "Seed 911079554 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/1642444692/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/1642444692/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 1642444692 (Simples): OK"
else
    echo "Seed 1642444692 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/3959116112/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/3959116112/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 3959116112 (Simples): OK"
else
    echo "Seed 3959116112 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/2991474091/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/2991474091/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 2991474091 (Simples): OK"
else
    echo "Seed 2991474091 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

# CONCATENAÇÃO EXPERIMENTO POWER-LAW
echo "Concatenando experimento Power-Law..."
cat > ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv << 'EOF'
gerador,tipo,numV,gamma,seed,num_grafos_gerados
EOF

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/2700001/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/2700001/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 2700001 (Power-Law): OK"
else
    echo "Seed 2700001 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/3170702080/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/3170702080/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 3170702080 (Power-Law): OK"
else
    echo "Seed 3170702080 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/3548644859/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/3548644859/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 3548644859 (Power-Law): OK"
else
    echo "Seed 3548644859 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/1033592630/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/1033592630/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 1033592630 (Power-Law): OK"
else
    echo "Seed 1033592630 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/9263589860/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/9263589860/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 9263589860 (Power-Law): OK"
else
    echo "Seed 9263589860 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/1883634842/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/1883634842/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 1883634842 (Power-Law): OK"
else
    echo "Seed 1883634842 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/7648101510/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/7648101510/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 7648101510 (Power-Law): OK"
else
    echo "Seed 7648101510 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/1502014705/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/1502014705/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 1502014705 (Power-Law): OK"
else
    echo "Seed 1502014705 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/7214842310/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/7214842310/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 7214842310 (Power-Law): OK"
else
    echo "Seed 7214842310 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/2606453957/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/2606453957/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 2606453957 (Power-Law): OK"
else
    echo "Seed 2606453957 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/4194499680/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/4194499680/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 4194499680 (Power-Law): OK"
else
    echo "Seed 4194499680 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/2779365847/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/2779365847/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 2779365847 (Power-Law): OK"
else
    echo "Seed 2779365847 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/1094121244/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/1094121244/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 1094121244 (Power-Law): OK"
else
    echo "Seed 1094121244 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/1090525961/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/1090525961/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 1090525961 (Power-Law): OK"
else
    echo "Seed 1090525961 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/3310223418/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/3310223418/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 3310223418 (Power-Law): OK"
else
    echo "Seed 3310223418 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/604827988/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/604827988/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 604827988 (Power-Law): OK"
else
    echo "Seed 604827988 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/1549035388/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/1549035388/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 1549035388 (Power-Law): OK"
else
    echo "Seed 1549035388 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/795578792/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/795578792/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 795578792 (Power-Law): OK"
else
    echo "Seed 795578792 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/182649370/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/182649370/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 182649370 (Power-Law): OK"
else
    echo "Seed 182649370 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/1127200130/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/1127200130/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 1127200130 (Power-Law): OK"
else
    echo "Seed 1127200130 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/332728275/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/332728275/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 332728275 (Power-Law): OK"
else
    echo "Seed 332728275 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/1477598055/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/1477598055/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 1477598055 (Power-Law): OK"
else
    echo "Seed 1477598055 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/1157679575/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/1157679575/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 1157679575 (Power-Law): OK"
else
    echo "Seed 1157679575 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/3489403805/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/3489403805/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 3489403805 (Power-Law): OK"
else
    echo "Seed 3489403805 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/359655529/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/359655529/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 359655529 (Power-Law): OK"
else
    echo "Seed 359655529 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/3107219804/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/3107219804/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 3107219804 (Power-Law): OK"
else
    echo "Seed 3107219804 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/911079554/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/911079554/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 911079554 (Power-Law): OK"
else
    echo "Seed 911079554 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/1642444692/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/1642444692/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 1642444692 (Power-Law): OK"
else
    echo "Seed 1642444692 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/3959116112/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/3959116112/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 3959116112 (Power-Law): OK"
else
    echo "Seed 3959116112 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/2991474091/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/2991474091/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 2991474091 (Power-Law): OK"
else
    echo "Seed 2991474091 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

echo "Concatenação concluída!"
echo "Arquivos finais:"
echo "  - ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv"
echo "  - ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv"
