# GERADOR DE GRAFOS - TCC

Sistema completo de geração e análise de grafos para estudos de redes complexas, desenvolvido como trabalho de conclusão de curso na Universidade Federal de Itajubá.

## Estrutura do Projeto

```
Gerador/
├── src/                           # Código fonte principal
│   ├── simples/                   # Gerador de grafos simples
│   │   ├── gerador.py            # Implementação principal
│   │   ├── constants.py          # Constantes e configurações
│   │   ├── exceptions.py         # Tratamento de exceções
│   │   ├── utils.py              # Utilitários
│   │   ├── main.py               # Interface de linha de comando
│   │   └── test_simples.py       # Testes unitários
│   ├── pwl/                      # Gerador de grafos power-law
│   │   ├── pwl.py                # Implementação principal
│   │   ├── constants.py          # Constantes e configurações
│   │   └── test_pwl.py           # Testes unitários
│   └── experimentos/             # Sistema de experimentos
│       ├── experimento_simples_completo.py    # Experimento simples
│       ├── experimento_powerlaw_completo.py   # Experimento power-law
│       ├── gerar_comandos_paralelos.py        # Gerador de comandos
│       ├── metrica_equivalencia_replicacoes.py # Métricas de equivalência
│       ├── executar_todos_experimentos.py     # Executor geral
│       └── README_experimentos.md             # Documentação dos experimentos
├── comandos_teste/               # Scripts de execução paralela
│   ├── comandos_todos.sh         # Comandos para execução
│   ├── concatenar_resultados.sh  # Script de concatenação
│   └── README.md                 # Instruções de uso
├── requirements.txt              # Dependências Python
├── .gitignore                    # Arquivos ignorados pelo Git
└── README.md                     # Este arquivo
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
```bash
pip install -r requirements.txt
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
python src/experimentos/experimento_simples_completo.py --seeds 1000 2000

# Experimento power-law completo
python src/experimentos/experimento_powerlaw_completo.py --seeds 1000 2000
```

### Execução Paralela
```bash
# 1. Gerar comandos de execução
python src/experimentos/gerar_comandos_paralelos.py \
    --main_dir "/path/to/project" \
    --experimento todos \
    --seeds 1000 2000 3000 4000 5000 \
    --output_dir ./comandos_teste

# 2. Executar em paralelo
cat comandos_teste/comandos_todos.sh | parallel -j 4

# 3. Concatenar resultados
./comandos_teste/concatenar_resultados.sh
```

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
- **Simples**: Eficiência de geração, razão vértices/arestas
- **Power-Law**: Qualidade do ajuste (R², p-valor), expoente alpha, xmin

### Métricas de Equivalência Estrutural
- Similaridade entre replicações
- Consistência estrutural
- Detecção de outliers

## Performance e Recursos

### Estimativas de Tempo
- **Gerador Simples**: 2-4 horas por seed (1.800 testes)
- **Gerador Power-Law**: 1-2 horas por seed (900 testes)
- **Total**: 20-40 horas para execução completa

### Requisitos de Memória
- **Gerador Simples**: 4-8 GB por execução
- **Gerador Power-Law**: 2-4 GB por execução
- **Total Paralelo**: 8-16 GB (dependendo do número de execuções)

### Armazenamento
- **Total**: 750 MB - 1.5 GB para todos os resultados
- **Formato**: CSV com métricas detalhadas
- **Estrutura**: Organização por seeds e experimentos

## Documentação Técnica

Para informações detalhadas sobre a metodologia experimental e estratégia de paralelização, consulte:

- `DOCUMENTO_TECNICO_EXPERIMENTOS.md` - Documentação técnica completa
- `src/experimentos/README_experimentos.md` - Documentação dos experimentos
- `comandos_teste/README.md` - Instruções de execução paralela

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
