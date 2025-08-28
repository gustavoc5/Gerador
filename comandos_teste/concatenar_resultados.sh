#!/bin/bash
# SCRIPT PARA CONCATENAR RESULTADOS DE TODAS AS SEEDS

MAIN_DIR="C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador"
echo "Concatenando resultados..."

# CONCATENAÇÃO EXPERIMENTO SIMPLES
echo "Concatenando experimento Simples..."
cat > ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv << 'EOF'
gerador,tipo,numV,numA,seed,estrategia_arestas,preferencia_densidade,numC,num_grafos_gerados
EOF

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/1000/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/1000/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 1000 (Simples): OK"
else
    echo "Seed 1000 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/2000/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/2000/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 2000 (Simples): OK"
else
    echo "Seed 2000 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/3000/resultados_simples_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/3000/resultados_simples_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
    echo "Seed 3000 (Simples): OK"
else
    echo "Seed 3000 (Simples): ARQUIVO NÃO ENCONTRADO"
fi

# CONCATENAÇÃO EXPERIMENTO POWER-LAW
echo "Concatenando experimento Power-Law..."
cat > ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv << 'EOF'
gerador,tipo,numV,gamma,seed,num_grafos_gerados
EOF

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/1000/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/1000/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 1000 (Power-Law): OK"
else
    echo "Seed 1000 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/2000/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/2000/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 2000 (Power-Law): OK"
else
    echo "Seed 2000 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

if [ -f ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/3000/resultados_powerlaw_completo.csv ]; then
    tail -n +2 ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/3000/resultados_powerlaw_completo.csv >> ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv
    echo "Seed 3000 (Power-Law): OK"
else
    echo "Seed 3000 (Power-Law): ARQUIVO NÃO ENCONTRADO"
fi

echo "Concatenação concluída!"
echo "Arquivos finais:"
echo "  - ${MAIN_DIR}/resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv"
echo "  - ${MAIN_DIR}/resultados_experimentos/exp_powerlaw_completo/resultados_powerlaw_completo.csv"
