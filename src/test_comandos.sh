#!/bin/bash
# Comandos gerados automaticamente para execução paralela
# Total de comandos: 10
# Módulo: simples
# Seeds: [123, 456]
# Vértices: [10, 15]
# Tipos: [0, 1]
# Execuções por combinação: 1

# Comando 1
mkdir -p ./test_results\simples\123

# Comando 2
python src/simples/test_simples.py --seed 123 --output_txt ./test_results\simples\123\simples_t0_v10_a21_s123_e0.txt &> ./test_results\simples\123\simples_t0_v10_a21_s123_e0.txt

# Comando 3
python src/simples/test_simples.py --seed 123 --output_txt ./test_results\simples\123\simples_t1_v10_a33_s123_e0.txt &> ./test_results\simples\123\simples_t1_v10_a33_s123_e0.txt

# Comando 4
python src/simples/test_simples.py --seed 123 --output_txt ./test_results\simples\123\simples_t0_v15_a64_s123_e0.txt &> ./test_results\simples\123\simples_t0_v15_a64_s123_e0.txt

# Comando 5
python src/simples/test_simples.py --seed 123 --output_txt ./test_results\simples\123\simples_t1_v15_a65_s123_e0.txt &> ./test_results\simples\123\simples_t1_v15_a65_s123_e0.txt

# Comando 6
mkdir -p ./test_results\simples\456

# Comando 7
python src/simples/test_simples.py --seed 456 --output_txt ./test_results\simples\456\simples_t0_v10_a15_s456_e0.txt &> ./test_results\simples\456\simples_t0_v10_a15_s456_e0.txt

# Comando 8
python src/simples/test_simples.py --seed 456 --output_txt ./test_results\simples\456\simples_t1_v10_a36_s456_e0.txt &> ./test_results\simples\456\simples_t1_v10_a36_s456_e0.txt

# Comando 9
python src/simples/test_simples.py --seed 456 --output_txt ./test_results\simples\456\simples_t0_v15_a33_s456_e0.txt &> ./test_results\simples\456\simples_t0_v15_a33_s456_e0.txt

# Comando 10
python src/simples/test_simples.py --seed 456 --output_txt ./test_results\simples\456\simples_t1_v15_a16_s456_e0.txt &> ./test_results\simples\456\simples_t1_v15_a16_s456_e0.txt

