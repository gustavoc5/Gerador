# Gerador de Grafos

Um sistema completo para geração, análise e teste de grafos com diferentes propriedades e distribuições.

## 📋 Visão Geral

Este projeto implementa dois geradores de grafos especializados:

- **Módulo Simples**: Gera grafos aleatórios simples com controle de densidade e conectividade
- **Módulo Power-Law**: Gera grafos com distribuição de graus seguindo lei de potência (power-law)

Ambos os módulos suportam 6 tipos de grafos: Simples, Digrafo, Multigrafo, Multigrafo-Dirigido, Pseudografo e Pseudografo-Dirigido.

## 🏗️ Estrutura do Projeto

```
src/
├── simples/                 # Gerador de grafos simples/aleatórios
│   ├── main.py             # Interface interativa
│   ├── gerador.py          # Lógica principal de geração
│   ├── utils.py            # Funções utilitárias
│   ├── visualizacao.py     # Visualização de grafos
│   ├── interface.py        # Interface adicional
│   ├── test_simples.py     # Testes automatizados
│   ├── mass_test.py        # Interface para testes em massa
│   ├── constants.py        # Constantes centralizadas
│   ├── exceptions.py       # Exceções customizadas
│   └── README_TESTES.md    # Documentação de testes
├── powerlaw/               # Gerador de grafos power-law
│   ├── main.py             # Interface interativa
│   ├── pwl.py              # Lógica principal de geração
│   ├── distribuicao.py     # Validação de distribuições
│   ├── analise.py          # Análise de comunidades e centralidade
│   ├── visualizacao.py     # Visualização de grafos
│   ├── test_pwl.py         # Testes automatizados
│   ├── mass_test.py        # Interface para testes em massa
│   ├── constants.py        # Constantes centralizadas
│   └── README_TESTES.md    # Documentação de testes
├── generate_experiments.py # Gerador de comandos para experimentos paralelos
├── generate_experiments.sh # Script bash para experimentos paralelos
├── concatenate_results.py  # Agregador de resultados
└── README_PARALLEL_EXPERIMENTS.md # Documentação do sistema paralelo
```

## 🚀 Funcionalidades Principais

### Módulo Simples
- **Geração de grafos aleatórios** com controle de densidade
- **Suporte a 6 tipos de grafos** (simples, dirigidos, múltiplas arestas, loops)
- **Controle de conectividade** (componentes conexas)
- **Validação automática** de parâmetros e propriedades
- **Detecção automática** do tipo de grafo gerado

### Módulo Power-Law
- **Geração de grafos com distribuição Zipf** (power-law)
- **Controle do expoente γ** (gamma) da distribuição
- **Validação de qualidade** da distribuição via teste KS
- **Análise de comunidades** (Greedy Modularity, Label Propagation)
- **Métricas de centralidade** (Degree, PageRank, Closeness)
- **Análise de hop plot** (distâncias de caminhos mínimos)

### Sistema de Experimentos Paralelos
- **Geração de comandos** para execução paralela
- **Evita condições de corrida** com arquivos de saída únicos
- **Escalabilidade** para milhares de experimentos
- **Agregação automática** de resultados

## 📦 Dependências

```bash
pip install numpy networkx powerlaw matplotlib pandas
```

## 🎯 Uso Rápido

### Interface Interativa

```bash
# Módulo Simples
cd src/simples
python main.py

# Módulo Power-Law
cd src/powerlaw
python main.py
```

### Testes Automatizados

```bash
# Teste simples com 10 execuções, 50 vértices
cd src/simples
python test_simples.py 10 50 resultados.csv

# Teste power-law com 10 execuções, 100 vértices
cd src/powerlaw
python test_pwl.py 10 100 resultados.csv
```

### Testes em Massa

```bash
# Interface menu-driven para testes
cd src/simples
python mass_test.py

cd src/powerlaw
python mass_test.py
```

### Experimentos Paralelos

```bash
# Gerar comandos para experimentos paralelos
python generate_experiments.py --main-dir /path/to/results --n-seeds 10

# Executar em paralelo (requer GNU parallel)
bash generate_experiments.sh | parallel

# Concatenar resultados
python concatenate_results.py --main-dir /path/to/results
```

## 🔧 Configuração

### Parâmetros Principais

**Módulo Simples:**
- `n_vertices`: Número de vértices
- `densidade`: Densidade desejada (0.0 a 1.0)
- `n_componentes`: Número de componentes conexas
- `tipo_grafo`: Tipo de grafo (1-6)

**Módulo Power-Law:**
- `n_vertices`: Número de vértices
- `gamma`: Expoente da distribuição power-law
- `tipo_grafo`: Tipo de grafo (1-6)
- `n_arestas`: Número de arestas (opcional)

### Constantes Configuráveis

Ambos os módulos possuem arquivos `constants.py` com parâmetros ajustáveis:
- Limites de tentativas
- Configurações de teste
- Parâmetros de visualização
- Tipos de grafos suportados

## 📊 Saída e Resultados

### Arquivos CSV
- **Métricas de grafos**: Vértices, arestas, densidade, componentes
- **Propriedades**: Tipo detectado, conectividade, distribuição de graus
- **Análises**: Centralidade, comunidades, hop plot (power-law)
- **Validações**: Qualidade da distribuição power-law

### Visualizações
- **Grafos pequenos** (< 50 vértices): Visualização completa
- **Grafos grandes**: Histogramas de distribuição de graus
- **Análises**: Gráficos de centralidade e comunidades

## 🧪 Testes e Validação

### Testes Automatizados
- **Validação de parâmetros**: Verificação de entrada
- **Verificação de propriedades**: Confirmação de características
- **Testes de stress**: Grafos grandes e casos extremos
- **Reprodutibilidade**: Testes com sementes fixas

### Validação de Qualidade
- **Distribuição power-law**: Teste Kolmogorov-Smirnov
- **Detecção de tipo**: Identificação automática correta
- **Conectividade**: Verificação de componentes
- **Densidade**: Confirmação de valores calculados

## 🔄 Sistema de Experimentos Paralelos

### Geração de Comandos
```bash
# Python
python generate_experiments.py --main-dir /results --n-seeds 100 --module both

# Bash
bash generate_experiments.sh --main-dir /results --n-seeds 100
```

### Execução Paralela
```bash
# Usando GNU parallel
bash generate_experiments.sh | parallel -j 8

# Usando xargs
bash generate_experiments.sh | xargs -P 4 -I {} bash -c "{}"
```

### Estrutura de Resultados
```
results/
├── simples/
│   ├── seed_001/
│   │   ├── size50.txt
│   │   ├── size100.txt
│   │   └── ...
│   └── ...
├── powerlaw/
│   ├── seed_001/
│   │   ├── gamma2.0.txt
│   │   ├── gamma2.5.txt
│   │   └── ...
│   └── ...
└── concatenated/
    ├── simples_all.csv
    ├── powerlaw_all.csv
    └── summary.txt
```

## 📈 Escalabilidade

### Performance
- **Grafos pequenos** (< 100 vértices): < 1 segundo
- **Grafos médios** (100-1000 vértices): 1-10 segundos
- **Grafos grandes** (1000+ vértices): 10+ segundos
- **Paralelização**: Linear com número de cores

### Limites Práticos
- **Máximo testado**: 10.000 vértices
- **Experimentos paralelos**: 1000+ simultâneos
- **Armazenamento**: ~1MB por experimento

## 🛠️ Desenvolvimento

### Arquitetura
- **Modular**: Separação clara de responsabilidades
- **Extensível**: Fácil adição de novos tipos de grafos
- **Testável**: Cobertura completa de testes
- **Documentado**: Docstrings detalhadas e exemplos

### Boas Práticas
- **Tratamento de erros**: Exceções customizadas
- **Validação**: Verificação rigorosa de entrada
- **Logging**: Rastreabilidade completa
- **Constantes**: Centralização de parâmetros

## 📚 Documentação Adicional

- `src/simples/README_TESTES.md`: Documentação completa dos testes do módulo simples
- `src/powerlaw/README_TESTES.md`: Documentação completa dos testes do módulo power-law
- `src/README_PARALLEL_EXPERIMENTS.md`: Guia completo do sistema de experimentos paralelos

## 🤝 Contribuição

O projeto está estruturado para facilitar contribuições:
1. **Módulos independentes**: Cada módulo pode ser desenvolvido separadamente
2. **Interfaces padronizadas**: APIs consistentes entre módulos
3. **Testes automatizados**: Validação automática de mudanças
4. **Documentação**: Guias detalhados para novos desenvolvedores

## 📄 Licença

Este projeto é parte de um trabalho de conclusão de curso (TCC) da Universidade Federal de Itajubá (UNIFEI).
