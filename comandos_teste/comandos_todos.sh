# COMANDOS PARA EXECUÇÃO PARALELA - AMBOS OS EXPERIMENTOS
# Total of seeds: 3
# Total of commands: 6
# Simples tests per seed: 180
# Power-Law tests per seed: 90
# Simples graphs per seed: 9000
# Power-Law graphs per seed: 4500

mkdir -p C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_simples_completo/1000
mkdir -p C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_powerlaw_completo/1000
python C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\src/experimentos/experimento_simples_completo.py --output_dir C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_simples_completo/1000 --seeds 1000 &> C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_simples_completo/1000/log.txt
python C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\src/experimentos/experimento_powerlaw_completo.py --output_dir C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_powerlaw_completo/1000 --seeds 1000 &> C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_powerlaw_completo/1000/log.txt
mkdir -p C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_simples_completo/2000
mkdir -p C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_powerlaw_completo/2000
python C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\src/experimentos/experimento_simples_completo.py --output_dir C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_simples_completo/2000 --seeds 2000 &> C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_simples_completo/2000/log.txt
python C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\src/experimentos/experimento_powerlaw_completo.py --output_dir C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_powerlaw_completo/2000 --seeds 2000 &> C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_powerlaw_completo/2000/log.txt
mkdir -p C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_simples_completo/3000
mkdir -p C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_powerlaw_completo/3000
python C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\src/experimentos/experimento_simples_completo.py --output_dir C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_simples_completo/3000 --seeds 3000 &> C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_simples_completo/3000/log.txt
python C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\src/experimentos/experimento_powerlaw_completo.py --output_dir C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_powerlaw_completo/3000 --seeds 3000 &> C:\Users\gusta\OneDrive\GUSTAVO\Unifei\TCC\Gerador\resultados_experimentos/exp_powerlaw_completo/3000/log.txt
