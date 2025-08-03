# 🚀 Sistema de Experimentos Paralelos

## 📋 Visão Geral

Este sistema permite executar milhares de experimentos de forma paralela, evitando condições de corrida e organizando os resultados por seed. Cada experimento tem sua própria saída independente.

## 🎯 Estrutura de Diretórios

```
src/
├── generate_experiments.py      # Script Python para gerar experimentos
├── generate_experiments.sh      # Script Bash para gerar experimentos
├── concatenate_results.py       # Script para concatenar resultados
├── simples/                     # Módulo de grafos simples
├── powerlaw/                    # Módulo de grafos power-law
└── results/                     # Resultados organizados por seed
    ├── simples/
    │   ├── 270001/
    │   │   ├── size100_exec0.txt
    │   │   ├── size100_exec1.txt
    │   │   └── ...
    │   └── 341099/
    │       └── ...
    └── powerlaw/
        └── ...
```

## 🚀 Como Usar

### 1. Gerar Experimentos (Python)

```bash
# Sintaxe básica
python generate_experiments.py [opções]

# Exemplos:
# Apenas módulo simples
python generate_experiments.py --module simples --sizes 100 500 --execucoes 5

# Apenas módulo powerlaw
python generate_experiments.py --module powerlaw --sizes 1000 5000 --execucoes 3

# Ambos os módulos
python generate_experiments.py --module both --sizes 100 500 1000 --execucoes 10

# Com seeds específicas
python generate_experiments.py --seeds 270001 341099 160812 --sizes 100 500
```

### 2. Gerar Experimentos (Bash)

```bash
# Executa o script bash
bash generate_experiments.sh > experiments.sh

# Ou modifica as variáveis no script:
# SEEDS=(270001 341099 160812)
# SIZES=(100 500 1000)
# EXECUCOES=5
# MODULE="both"
```

### 3. Executar Experimentos

```bash
# Execução sequencial
bash experiments.sh

# Execução paralela (recomendado)
parallel -j 8 < experiments.sh

# Execução paralela com progresso
parallel --bar -j 8 < experiments.sh

# Execução paralela com log
parallel -j 8 --joblog experimentos.log < experiments.sh
```

### 4. Concatenar Resultados

```bash
# Concatena todos os resultados
python concatenate_results.py

# Com resumo
python concatenate_results.py --summary

# Módulos específicos
python concatenate_results.py --modules simples powerlaw

# Seeds específicas
python concatenate_results.py --seeds 270001 341099
```

## 📊 Parâmetros dos Scripts

### generate_experiments.py

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `--module` | string | "both" | Módulo(s): simples, powerlaw, both |
| `--main_dir` | path | cwd | Diretório principal do projeto |
| `--seeds` | list | [30 seeds] | Lista de seeds para experimentos |
| `--sizes` | list | [100,500,1000] | Tamanhos dos grafos |
| `--execucoes` | int | 5 | Execuções por configuração |
| `--output` | path | auto | Arquivo de saída |

### concatenate_results.py

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `--results_dir` | path | "results" | Diretório com resultados |
| `--modules` | list | ["simples","powerlaw"] | Módulos a processar |
| `--seeds` | list | [30 seeds] | Seeds a processar |
| `--summary` | flag | False | Gera resumo dos experimentos |

## 🎯 Exemplos de Escala

### Experimento Pequeno
```bash
python generate_experiments.py --module simples --sizes 100 500 --execucoes 2 --seeds 270001 341099
# Resultado: 8 experimentos
# Tempo: ~2-3 minutos
```

### Experimento Médio
```bash
python generate_experiments.py --module both --sizes 100 500 1000 --execucoes 5 --seeds 270001 341099 160812
# Resultado: 90 experimentos (45 simples + 45 powerlaw)
# Tempo: ~15-20 minutos
```

### Experimento Massivo
```bash
python generate_experiments.py --module both --sizes 100 500 1000 5000 --execucoes 10
# Resultado: 1.200 experimentos (600 simples + 600 powerlaw)
# Tempo: ~4-6 horas
```

### Experimento Extremo
```bash
python generate_experiments.py --module both --sizes 100 500 1000 5000 10000 --execucoes 20
# Resultado: 3.000 experimentos (1.500 simples + 1.500 powerlaw)
# Tempo: ~12-18 horas
```

## 🔧 Configurações Avançadas

### Paralelização

```bash
# Usar todos os cores disponíveis
parallel -j $(nproc) < experiments.sh

# Usar metade dos cores
parallel -j $(( $(nproc) / 2 )) < experiments.sh

# Limitar a 4 cores
parallel -j 4 < experiments.sh

# Com timeout por experimento
parallel --timeout 300 -j 8 < experiments.sh
```

### Monitoramento

```bash
# Com log detalhado
parallel --joblog experimentos.log --bar -j 8 < experiments.sh

# Com progresso e estatísticas
parallel --bar --eta -j 8 < experiments.sh

# Com retry em caso de falha
parallel --retry-failed --joblog experimentos.log -j 8 < experiments.sh
```

### Execução em Lote

```bash
# Gerar múltiplos scripts
for size in 100 500 1000; do
    python generate_experiments.py --sizes $size --output experiments_${size}.sh
done

# Executar em paralelo
for script in experiments_*.sh; do
    parallel -j 4 < $script &
done
wait
```

## 📁 Estrutura de Saída

### Arquivos Gerados

```
experiments_simples_20250802_201518.sh    # Script de experimentos
concatenate_results.sh                    # Script de concatenação
results/
├── simples/
│   ├── 270001/
│   │   ├── size100_exec0.txt
│   │   ├── size100_exec1.txt
│   │   └── ...
│   └── 341099/
│       └── ...
├── powerlaw/
│   └── ...
├── simples_concatenated_270001.txt       # Resultados concatenados
├── powerlaw_concatenated_270001.txt
├── simples_summary.txt                   # Resumo dos experimentos
└── powerlaw_summary.txt
```

### Formato dos Arquivos

Cada arquivo de saída contém:
- **Configuração**: Parâmetros do experimento
- **Logs**: Saída completa do script
- **Métricas**: Resultados das análises
- **Erros**: Qualquer erro durante execução

## ⚠️ Considerações

1. **Memória**: Experimentos paralelos podem usar muita memória
2. **Disco**: Arquivos de saída podem ser grandes
3. **CPU**: Monitore o uso de CPU durante execução
4. **Rede**: Se executando em cluster, considere latência de rede
5. **Timeout**: Configure timeout adequado para experimentos longos

## 🎉 Vantagens do Sistema

- ✅ **Paralelismo**: Execução simultânea de experimentos
- ✅ **Independência**: Cada experimento tem saída única
- ✅ **Organização**: Resultados organizados por seed
- ✅ **Escalabilidade**: Suporta milhares de experimentos
- ✅ **Robustez**: Tratamento de erros e retry
- ✅ **Flexibilidade**: Configuração via linha de comando
- ✅ **Monitoramento**: Logs e estatísticas detalhadas 