# COMANDOS PARA EXECUÇÃO PARALELA - AMBOS OS EXPERIMENTOS
# Total of seeds: 2
# Total of commands: 8
# Commands per seed: 4 (2 mkdir + 2 python)
# Simples tests per seed: 180
# Power-Law tests per seed: 90
# Simples graphs per seed: 9000
# Power-Law graphs per seed: 4500
# Thread limit: 24 threads per process

mkdir -p C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_simples_completo/2700001
mkdir -p C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_powerlaw_completo/2700001
mkdir -p C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_simples_completo/2700001 && timeout --signal=SIGKILL 2h bash -lc 'export PYTHONIOENCODING=UTF-8; export OMP_NUM_THREADS=24; export MKL_NUM_THREADS=24; python3 -u C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\src/experimentos/simples.py --output_dir C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_simples_completo/2700001 --seeds 2700001 --max_vertices 1000000 &> C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_simples_completo/2700001/log.txt'
mkdir -p C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_powerlaw_completo/2700001 && timeout --signal=SIGKILL 2h bash -lc 'export PYTHONIOENCODING=UTF-8; export OMP_NUM_THREADS=24; export MKL_NUM_THREADS=24; python3 -u C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\src/experimentos/power_law.py --output_dir C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_powerlaw_completo/2700001 --seeds 2700001 --max_vertices 1000000 &> C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_powerlaw_completo/2700001/log.txt'
mkdir -p C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_simples_completo/3170702080
mkdir -p C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_powerlaw_completo/3170702080
mkdir -p C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_simples_completo/3170702080 && timeout --signal=SIGKILL 2h bash -lc 'export PYTHONIOENCODING=UTF-8; export OMP_NUM_THREADS=24; export MKL_NUM_THREADS=24; python3 -u C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\src/experimentos/simples.py --output_dir C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_simples_completo/3170702080 --seeds 3170702080 --max_vertices 1000000 &> C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_simples_completo/3170702080/log.txt'
mkdir -p C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_powerlaw_completo/3170702080 && timeout --signal=SIGKILL 2h bash -lc 'export PYTHONIOENCODING=UTF-8; export OMP_NUM_THREADS=24; export MKL_NUM_THREADS=24; python3 -u C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\src/experimentos/power_law.py --output_dir C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_powerlaw_completo/3170702080 --seeds 3170702080 --max_vertices 1000000 &> C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_powerlaw_completo/3170702080/log.txt'
