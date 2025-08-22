#!/bin/bash
# Comandos gerados automaticamente para execução paralela
# Total de comandos: 20
# Módulo: ambos
# Seeds: [123, 456]
# Vértices: [10, 15]
# Tipos: [0, 1]
# Execuções por combinação: 1

# Comando 1
mkdir -p ./exemplo_resultados\simples\123

# Comando 2
python src/simples/test_simples.py --seed 123 --output_txt ./exemplo_resultados\simples\123\simples_t0_v10_a36_s123_e0.txt &> ./exemplo_resultados\simples\123\simples_t0_v10_a36_s123_e0.txt

# Comando 3
python src/simples/test_simples.py --seed 123 --output_txt ./exemplo_resultados\simples\123\simples_t1_v10_a11_s123_e0.txt &> ./exemplo_resultados\simples\123\simples_t1_v10_a11_s123_e0.txt

# Comando 4
python src/simples/test_simples.py --seed 123 --output_txt ./exemplo_resultados\simples\123\simples_t0_v15_a83_s123_e0.txt &> ./exemplo_resultados\simples\123\simples_t0_v15_a83_s123_e0.txt

# Comando 5
python src/simples/test_simples.py --seed 123 --output_txt ./exemplo_resultados\simples\123\simples_t1_v15_a68_s123_e0.txt &> ./exemplo_resultados\simples\123\simples_t1_v15_a68_s123_e0.txt

# Comando 6
mkdir -p ./exemplo_resultados\simples\456

# Comando 7
python src/simples/test_simples.py --seed 456 --output_txt ./exemplo_resultados\simples\456\simples_t0_v10_a13_s456_e0.txt &> ./exemplo_resultados\simples\456\simples_t0_v10_a13_s456_e0.txt

# Comando 8
python src/simples/test_simples.py --seed 456 --output_txt ./exemplo_resultados\simples\456\simples_t1_v10_a37_s456_e0.txt &> ./exemplo_resultados\simples\456\simples_t1_v10_a37_s456_e0.txt

# Comando 9
python src/simples/test_simples.py --seed 456 --output_txt ./exemplo_resultados\simples\456\simples_t0_v15_a92_s456_e0.txt &> ./exemplo_resultados\simples\456\simples_t0_v15_a92_s456_e0.txt

# Comando 10
python src/simples/test_simples.py --seed 456 --output_txt ./exemplo_resultados\simples\456\simples_t1_v15_a45_s456_e0.txt &> ./exemplo_resultados\simples\456\simples_t1_v15_a45_s456_e0.txt

# Comando 11
mkdir -p ./exemplo_resultados\powerlaw\123

# Comando 12
python src/powerlaw/test_pwl.py --seed 123 --output_txt ./exemplo_resultados\powerlaw\123\powerlaw_t0_v10_g2.74_s123_e0.txt &> ./exemplo_resultados\powerlaw\123\powerlaw_t0_v10_g2.74_s123_e0.txt

# Comando 13
python src/powerlaw/test_pwl.py --seed 123 --output_txt ./exemplo_resultados\powerlaw\123\powerlaw_t1_v10_g3.04_s123_e0.txt &> ./exemplo_resultados\powerlaw\123\powerlaw_t1_v10_g3.04_s123_e0.txt

# Comando 14
python src/powerlaw/test_pwl.py --seed 123 --output_txt ./exemplo_resultados\powerlaw\123\powerlaw_t0_v15_g2.63_s123_e0.txt &> ./exemplo_resultados\powerlaw\123\powerlaw_t0_v15_g2.63_s123_e0.txt

# Comando 15
python src/powerlaw/test_pwl.py --seed 123 --output_txt ./exemplo_resultados\powerlaw\123\powerlaw_t1_v15_g3.19_s123_e0.txt &> ./exemplo_resultados\powerlaw\123\powerlaw_t1_v15_g3.19_s123_e0.txt

# Comando 16
mkdir -p ./exemplo_resultados\powerlaw\456

# Comando 17
python src/powerlaw/test_pwl.py --seed 456 --output_txt ./exemplo_resultados\powerlaw\456\powerlaw_t0_v10_g3.31_s456_e0.txt &> ./exemplo_resultados\powerlaw\456\powerlaw_t0_v10_g3.31_s456_e0.txt

# Comando 18
python src/powerlaw/test_pwl.py --seed 456 --output_txt ./exemplo_resultados\powerlaw\456\powerlaw_t1_v10_g2.65_s456_e0.txt &> ./exemplo_resultados\powerlaw\456\powerlaw_t1_v10_g2.65_s456_e0.txt

# Comando 19
python src/powerlaw/test_pwl.py --seed 456 --output_txt ./exemplo_resultados\powerlaw\456\powerlaw_t0_v15_g3.19_s456_e0.txt &> ./exemplo_resultados\powerlaw\456\powerlaw_t0_v15_g3.19_s456_e0.txt

# Comando 20
python src/powerlaw/test_pwl.py --seed 456 --output_txt ./exemplo_resultados\powerlaw\456\powerlaw_t1_v15_g2.06_s456_e0.txt &> ./exemplo_resultados\powerlaw\456\powerlaw_t1_v15_g2.06_s456_e0.txt

