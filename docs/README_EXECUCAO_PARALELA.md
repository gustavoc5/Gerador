# GUIA DE EXECUÇÃO PARALELA DOS EXPERIMENTOS

## 🎯 Objetivo
Este guia descreve como gerar e executar comandos para rodar os experimentos em paralelo, de forma reprodutível e compatível com GNU parallel.

## 🚀 Geração de comandos

Use o script `paralelizacao.py` para gerar os comandos (um comando por linha, sem quebras):
```bash
python src/experimentos/paralelizacao.py \
  --main_dir $(pwd) \
  --experimento todos \
  --seeds 2700001 3170702080 3548644859 1033592630 9263589860 1883634842 7648101510 1502014705 7214842310 2606453957 4194499680 2779365847 1094121244 1090525961 3310223418 604827988 1549035388 795578792 182649370 1127200130 332728275 1477598055 1157679575 3489403805 359655529 3107219804 911079554 1642444692 3959116112 2991474091
```

Serão gerados 3 arquivos:
- `comandos_paralelos/comandos_todos.sh` (comandos completos)
- `comandos_paralelos/comandos_todos_mkdir.sh` (apenas mkdir)
- `comandos_paralelos/comandos_todos_python.sh` (apenas python)

## 🧵 Limite de threads
Cada linha de execução Python já inclui: `export OMP_NUM_THREADS=24 && export MKL_NUM_THREADS=24`.
Isso limita cada processo a 24 threads para uso responsável dos recursos compartilhados.

## 🖥️ Execução com GNU parallel

Opção A — Comandos separados (recomendado):
```bash
# 1) Criar diretórios
cat comandos_paralelos/comandos_todos_mkdir.sh | parallel \
  --tmp /tmp --joblog progress.log --filter-hosts --sshloginfile my_servers.txt \
  --resume --resume-failed --jobs 1 'echo {}; eval {};'

# 2) Executar experimentos
cat comandos_paralelos/comandos_todos_python.sh | parallel \
  --tmp /tmp --joblog progress.log --filter-hosts --sshloginfile my_servers.txt \
  --resume --resume-failed --jobs 1 'echo {}; eval {};'
```

Opção B — Arquivo único:
```bash
cat comandos_paralelos/comandos_todos.sh | parallel \
  --tmp /tmp --joblog progress.log --filter-hosts --sshloginfile my_servers.txt \
  --resume --resume-failed --jobs 1 'echo {}; eval {};'
```

## 📎 Exemplo de conteúdo gerado
```bash
# COMANDOS PARA EXECUÇÃO PARALELA - AMBOS OS EXPERIMENTOS
# Total of seeds: 30
# Total of commands: 60
# Thread limit: 24 threads per process

mkdir -p /path/to/resultados_experimentos/exp_simples_completo/2700001
mkdir -p /path/to/resultados_experimentos/exp_powerlaw_completo/2700001
export OMP_NUM_THREADS=24 && export MKL_NUM_THREADS=24 && python /path/to/src/experimentos/simples.py --output_dir /path/to/resultados_experimentos/exp_simples_completo/2700001 --seeds 2700001 &> /path/to/resultados_experimentos/exp_simples_completo/2700001/log.txt
export OMP_NUM_THREADS=24 && export MKL_NUM_THREADS=24 && python /path/to/src/experimentos/power_law.py --output_dir /path/to/resultados_experimentos/exp_powerlaw_completo/2700001 --seeds 2700001 &> /path/to/resultados_experimentos/exp_powerlaw_completo/2700001/log.txt
```

Características:
- 60 comandos (30 seeds × 2 experimentos)
- Um comando por linha (sem barras de continuação)
- Limite de 24 threads por processo
- Caminhos absolutos e logs por seed

## 🧪 Teste rápido (5 minutos)
```bash
# Gerar comandos para um smoke test com 3 seeds
python src/experimentos/paralelizacao.py \
  --main_dir $(pwd) \
  --experimento todos \
  --seeds 2700001 3170702080 3548644859

# Executar
cat comandos_paralelos/comandos_todos.sh | parallel -j 6

# Verificar resultados
ls -la resultados_experimentos/exp_*_completo/*/
```

## 📈 Execução completa (30 seeds)
- 60 comandos executados em paralelo
- ~2.700 testes por experimento (Simples e Power-Law)
- ~135.000 grafos processados no total
- Tempo estimado: 2–3 horas (dependendo do cluster)

## ✅ Pós-execução
```bash
# Verificar erros
grep -r "ERRO\|ERROR\|Exitval" resultados_experimentos/

# Contar arquivos CSV
find resultados_experimentos/ -name "*.csv" | wc -l

# Verificar logs
find resultados_experimentos/ -name "log.txt" | wc -l

# Concatenação final (scrpit gerado automaticamente)
bash comandos_paralelos/concatenar_resultados.sh
```

## 📚 Notas
- O script correto para geração é `src/experimentos/paralelizacao.py`.
- Sementes usadas no exemplo possuem alta entropia e são adequadas para Mersenne Twister.
- Os comandos são compatíveis com GNU parallel e preparados para execução reentrante.

