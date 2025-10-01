# GERADOR DE GRAFOS - TCC

Sistema completo de geração e análise de grafos para estudos de redes complexas, desenvolvido como trabalho de conclusão de curso na Universidade Federal de Itajubá.

## Estrutura do Projeto

```
Gerador/
├── src/                           # Código fonte principal
│   ├── simples/                   # Gerador de grafos simples
│   │   ├── gerador.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── utils.py
│   │   ├── main.py
│   │   └── test_simples.py
│   ├── pwl/                      # Gerador de grafos power-law
│   │   ├── pwl.py
│   │   ├── constants.py
│   │   └── test_pwl.py
│   └── experimentos/             # Sistema de experimentos
│       ├── simples.py            # Experimento simples completo
│       ├── power_law.py          # Experimento power-law completo
│       ├── similaridade.py       # Métricas de equivalência estrutural
│       ├── paralelizacao.py      # Gerador de comandos para GNU parallel
│       └── executar-tudo.py      # Executor geral (opcional)
├── comandos_teste/               # Documentação de execução
│   ├── README_TESTES.md          # Guia de níveis de teste
│   ├── README_ORIENTADOR.md      # Guia geral de execução paralela
│   └── LIMITES_OTIMIZADOS.md     # Notas sobre limites de recursos
├── comandos_paralelos/           # Saída gerada por paralelizacao.py (auto)
│   ├── comandos_todos.sh
│   ├── comandos_todos_mkdir.sh
│   ├── comandos_todos_python.sh
│   └── concatenar_resultados.sh
├── requirements.txt
└── README.md
```

## Características Principais

### Geradores Implementados

**Gerador Simples:**
- Grafos aleatórios com diferentes densidades
- Suporte a 6 tipos de grafos (Simples, Dirigido, Multigrafo, etc.)
- Configuração de componentes conexos
- Estratégias de densidade (Esparso, Denso, Sem preferência)

**Gerador Power-Law:**
- Redes livre de escala com distribuição power-law
- Categorias de densidade (Denso, Moderado, Esparso)
- Validação da qualidade do ajuste power-law
- Teste Kolmogorov-Smirnov para verificação

### Sistema de Experimentos

**Configuração Completa:**
- 2.700 testes experimentais
- 135.000 grafos gerados
- 80+ métricas coletadas por grafo
- Execução paralela otimizada para clusters

**Paralelização:**
- Estratégia baseada em seeds
- Independência total entre execuções
- Sistema de logs detalhados
- Concatenação automática de resultados

## Instalação e Configuração

### 1. Instalação das Dependências

**Opção A: Instalação Manual (Recomendada)**
```bash
pip install -r requirements.txt
```

**Opção B: Instalação Individual**
```bash
pip install numpy>=1.21.0 networkx>=2.8.0 pandas>=1.3.0
pip install scipy>=1.7.0 python-igraph>=0.10.0
pip install powerlaw>=1.5 matplotlib>=3.5.0 pytest>=6.0.0
```

### 2. Verificação da Instalação
```bash
# Teste do gerador simples
python src/simples/main.py --help

# Teste do gerador power-law
python src/pwl/pwl.py --help
```

## Uso Básico

### Gerador Simples
```bash
# Geração básica
python src/simples/main.py --numV 100 --numA 200 --seed 123

# Com preferência de densidade
python src/simples/main.py --numV 1000 --preferencia_densidade 1 --seed 456

# Grafo conexo
python src/simples/main.py --numV 500 --numC 1 --seed 789
```

### Gerador Power-Law
```bash
# Geração básica
python src/pwl/pwl.py --numV 100 --gamma 2.5 --seed 123

# Categoria de densidade
python src/pwl/pwl.py --numV 1000 --categoria denso --seed 456
```

## Sistema de Experimentos

### Execução Individual
```bash
# Experimento simples completo
python src/experimentos/simples.py --seeds 1000 2000

# Experimento power-law completo
python src/experimentos/power_law.py --seeds 1000 2000

# Executar ambos os experimentos
python src/experimentos/executar-tudo.py --teste_rapido
```

### Execução Paralela
```bash
# 1. Gerar comandos de execução (um por linha, sem quebras)
python src/experimentos/paralelizacao.py \
  --main_dir $(pwd) \
  --experimento todos \
  --seeds 2700001 3170702080 3548644859 1033592630 9263589860 \
         1883634842 7648101510 1502014705 7214842310 2606453957 \
         4194499680 2779365847 1094121244 1090525961 3310223418 \
         604827988 1549035388 795578792 182649370 1127200130 \
         332728275 1477598055 1157679575 3489403805 359655529 \
         3107219804 911079554 1642444692 3959116112 2991474091

# 2. Executar em paralelo (GNU parallel)
cat comandos_paralelos/comandos_todos.sh | parallel -j 60

# 3. Concatenação final
bash comandos_paralelos/concatenar_resultados.sh
```

### Estrutura de Arquivos Gerados

**Cada gerador produz seus próprios arquivos de saída:**

```
resultados_experimentos/
├── exp_simples_completo/                    # Gerador Simples
│   ├── resultados_simples_completo.csv      # Dados completos (1.800 testes)
│   └── resumo_simples_completo.csv          # Resumo estatístico (6 linhas)
└── exp_powerlaw_completo/                   # Gerador Power-Law
    ├── resultados_powerlaw_completo.csv     # Dados completos (900 testes)
    └── resumo_powerlaw_completo.csv         # Resumo estatístico (6 linhas)
```

**Execução Paralela (por seed):**
```
resultados_experimentos/
├── exp_simples_completo/
│   ├── 1000/                              # Seed 1000
│   │   ├── resultados_simples_completo.csv
│   │   └── log.txt
│   ├── 2000/                              # Seed 2000
│   │   ├── resultados_simples_completo.csv
│   │   └── log.txt
│   └── ...                                # Outras seeds
└── exp_powerlaw_completo/
    ├── 1000/                              # Seed 1000
    │   ├── resultados_powerlaw_completo.csv
    │   └── log.txt
    ├── 2000/                              # Seed 2000
    │   ├── resultados_powerlaw_completo.csv
    │   └── log.txt
    └── ...                                # Outras seeds
```

**Após concatenação:**
- **`resultados_simples_completo.csv`** - Todos os dados do gerador Simples
- **`resultados_powerlaw_completo.csv`** - Todos os dados do gerador Power-Law

## Tipos de Grafo Suportados

| Código | Tipo | Descrição |
|--------|------|-----------|
| 0 | Simples | Grafo não dirigido sem loops ou múltiplas arestas |
| 1 | Digrafo | Grafo dirigido sem loops ou múltiplas arestas |
| 20 | Multigrafo | Grafo não dirigido com múltiplas arestas |
| 21 | Multigrafo-Dirigido | Grafo dirigido com múltiplas arestas |
| 30 | Pseudografo | Grafo não dirigido com loops |
| 31 | Pseudografo-Dirigido | Grafo dirigido com loops |

## Métricas Coletadas

### Métricas Estruturais
- Número de vértices e arestas
- Densidade do grafo
- Distribuição de graus (média, máximo, mínimo, desvio padrão)
- Assimetria e curtose da distribuição

### Métricas de Centralidade
- PageRank (média, máximo, mínimo, desvio padrão)
- Closeness Centrality (média, máximo, mínimo, desvio padrão)
- Betweenness Centrality (média, máximo, mínimo, desvio padrão)

### Métricas de Comunidade
- Modularidade (algoritmos Greedy e Label Propagation)
- Número de comunidades detectadas

### Métricas Específicas
- **Simples**: Razão vértices/arestas
- **Power-Law**: Qualidade do ajuste (R², p-valor), expoente alpha, xmin

### Métricas de Equivalência Estrutural
- Similaridade entre replicações
- Consistência estrutural
- Detecção de outliers

## Documentação Técnica

Para detalhes:
- `src/experimentos/README_experimentos.md` — Documentação dos experimentos
- `docs/README_TESTES.md` — Guia de níveis de teste
- `docs/README_EXECUCAO_PARALELA.md` — Guia de execução paralela (GNU parallel)

## Desenvolvimento

Este projeto foi desenvolvido como parte do TCC em Ciência da Computação na Universidade Federal de Itajubá, focado na análise comparativa de geradores de grafos e suas aplicações em redes complexas.

### Contribuições
- Sistema completo de experimentos
- Metodologia robusta para análise comparativa
- Paralelização otimizada para clusters
- Base de dados única com 135.000 grafos analisados

### Próximos Passos
1. Execução completa em ambiente de cluster
2. Análise estatística dos resultados
3. Publicação de artigos científicos
4. Disponibilização de código e dados
