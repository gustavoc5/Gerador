#!/bin/bash
# SCRIPT PARA CONCATENAR RESULTADOS DE TODAS AS SEEDS

MAIN_DIR="C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador"
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

echo "Concatenação concluída!"
echo "Arquivos finais:"
echo "  - ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv"
echo "  - ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv"
