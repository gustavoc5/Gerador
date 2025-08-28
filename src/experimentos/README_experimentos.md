# 📊 EXPERIMENTOS DE GERAÇÃO DE GRAFOS

Este diretório contém scripts para execução de experimentos sistemáticos dos geradores de grafos, seguindo o planejamento experimental definido.

## 🎯 VISÃO GERAL

Os experimentos foram projetados para analisar sistematicamente o comportamento dos geradores de grafos **Simples** e **Power-Law** em diferentes cenários e configurações.

## 📋 EXPERIMENTOS DISPONÍVEIS

### 1. **EXPERIMENTO 1: Comparação Fundamental entre Geradores**
- **Arquivo:** `experimento_1_comparacao_geradores.py`
- **Objetivo:** Comparar diretamente o comportamento dos geradores Simples e Power-Law
- **Fatores:** Gerador, Tipo de Grafo, Tamanho, Seed
- **Combinações:** 2 × 6 × 5 × 5 = 300 testes

### 2. **EXPERIMENTO 2: Parâmetros Críticos do Gerador Simples**
- **Arquivo:** `experimento_2_parametros_simples.py`
- **Objetivo:** Analisar todos os parâmetros do gerador simples
- **Fatores:** Tipo, Tamanho, Estratégia de Arestas, Componentes, Balanceamento, Número de Grafos, Seed
- **Combinações:** 6 × 5 × 2 × 5 × 5 × 3 × 3 × 3 = 40.500 testes (com teste rápido: 2.160)

### 3. **EXPERIMENTO 3: Parâmetros Críticos do Gerador Power-Law**
- **Arquivo:** `experimento_3_parametros_powerlaw.py`
- **Objetivo:** Analisar todos os parâmetros do gerador power-law
- **Fatores:** Tipo, Tamanho, Gamma, Distribuição, Grau Mínimo, Seed
- **Combinações:** 6 × 5 × 5 × 2 × 3 × 3 = 2.700 testes (com teste rápido: 432)

### 4. **EXPERIMENTO 4: Análise de Escalabilidade e Limitações**
- **Arquivo:** `experimento_4_escalabilidade.py`
- **Objetivo:** Avaliar comportamento com tamanhos extremos
- **Fatores:** Tamanho, Gerador, Tipo, Estratégia de Memória, Seed
- **Combinações:** 3 × 2 × 6 × 2 × 2 = 144 testes (com teste rápido: 6)

## 🚀 COMO EXECUTAR

### Execução Individual

```bash
# Experimento 1 - Comparação básica
python src/experimentos/experimento_1_comparacao_geradores.py --teste_rapido

# Experimento 2 - Parâmetros simples
python src/experimentos/experimento_2_parametros_simples.py --teste_rapido

# Experimento 3 - Parâmetros power-law
python src/experimentos/experimento_3_parametros_powerlaw.py --teste_rapido

# Experimento 4 - Escalabilidade
python src/experimentos/experimento_4_escalabilidade.py --teste_rapido
```

### Execução com Script Principal

```bash
# Executa todos os experimentos sequencialmente
python src/experimentos/executar_todos_experimentos.py --experimentos 1,2,3,4 --modo sequencial

# Executa experimentos específicos em paralelo
python src/experimentos/executar_todos_experimentos.py --experimentos 1,2 --modo paralelo --cores 4

# Executa apenas um experimento em modo teste rápido
python src/experimentos/executar_todos_experimentos.py --experimentos 1 --teste_rapido
```

## ⚙️ PARÂMETROS DE CONFIGURAÇÃO

### Parâmetros Globais
- `--output_dir`: Diretório de saída (padrão: `./resultados_experimentos`)
- `--max_vertices`: Máximo de vértices para teste (padrão: 10000)
- `--seeds`: Lista de seeds para teste (padrão: [1000, 2000, 3000])
- `--teste_rapido`: Executa versões reduzidas dos experimentos

### Parâmetros Específicos por Experimento

#### Experimento 1
- Comparação direta entre geradores
- Tamanhos: 100, 1000, 10000, 100000, 1000000
- Seeds: 1000, 2000, 3000, 4000, 5000

#### Experimento 2
- Análise completa dos parâmetros do gerador simples
- Estratégias de arestas: Proporcional, Aleatório
- Fatores de densidade: 0.1, 0.3, 0.5, 0.7, 0.9
- Componentes: 0, 1, 2, 5, 10
- Balanceamento: 0, 1, 2
- Número de grafos: 1, 5, 10

#### Experimento 3
- Análise completa dos parâmetros do gerador power-law
- Expoentes gamma: 2.0, 2.2, 2.5, 2.8, 3.0
- Distribuições: Balanceado, Desequilibrado
- Graus mínimos: 1, 2, 3

#### Experimento 4
- Análise de escalabilidade
- Tamanhos grandes: 10000, 100000, 1000000
- Monitoramento de memória e tempo
- Detecção de limitações de hardware

## 📊 SAÍDAS DOS EXPERIMENTOS

### Estrutura de Diretórios
```
resultados_experimentos/
├── exp1_comparacao_geradores/
│   ├── resultados_experimento1.csv
│   └── resumo_experimento1.txt
├── exp2_parametros_simples/
│   ├── resultados_experimento2.csv
│   └── resumo_experimento2.txt
├── exp3_parametros_powerlaw/
│   ├── resultados_experimento3.csv
│   └── resumo_experimento3.txt
├── exp4_escalabilidade/
│   ├── resultados_experimento4.csv
│   └── resumo_experimento4.txt
└── log_execucao_YYYYMMDD_HHMMSS.txt
```

### Arquivos de Saída

#### CSV Principal
- Contém todos os resultados em formato tabular
- Inclui parâmetros de entrada e métricas de saída
- Compatível com pandas, R, Excel, etc.

#### Resumo TXT
- Estatísticas resumidas por fator
- Tempos médios e taxas de sucesso
- Análise de tendências

#### Log de Execução
- Registro completo da execução
- Tempos e status de cada experimento
- Informações de debug

## 📈 MÉTRICAS COLETADAS

### Métricas Básicas
- `num_vertices`: Número de vértices
- `num_arestas`: Número de arestas
- `densidade`: Densidade do grafo
- `grau_medio`: Grau médio dos vértices
- `grau_max`: Grau máximo
- `grau_min`: Grau mínimo
- `num_componentes`: Número de componentes conexas

### Métricas de Centralidade
- `pagerank_medio`: PageRank médio
- `pagerank_max`: PageRank máximo
- `closeness_medio`: Closeness centrality médio
- `closeness_max`: Closeness centrality máximo
- `betweenness_medio`: Betweenness centrality médio
- `betweenness_max`: Betweenness centrality máximo

### Métricas de Distância
- `diametro`: Diâmetro do grafo
- `raio`: Raio do grafo
- `distancia_media`: Distância média

### Métricas de Comunidades
- `num_comunidades_greedy`: Número de comunidades (Greedy)
- `modularidade_greedy`: Modularidade (Greedy)
- `num_comunidades_label`: Número de comunidades (Label)
- `modularidade_label`: Modularidade (Label)

### Métricas de Performance
- `tempo_geracao`: Tempo de geração (segundos)
- `memoria_pico_mb`: Uso máximo de memória (MB)
- `taxa_sucesso`: Taxa de sucesso (0.0-1.0)
- `limite_atingido`: Se limite de hardware foi atingido

### Métricas Específicas
- `qualidade_powerlaw_R`: Qualidade do ajuste power-law (R)
- `qualidade_powerlaw_p_value`: P-value do teste power-law
- `conectividade`: Se o grafo é conexo (0.0-1.0)

## 🔧 CONFIGURAÇÕES AVANÇADAS

### Modo Teste Rápido
Reduz significativamente o número de combinações para validação rápida:
- Menos tamanhos de grafos
- Menos tipos de grafos
- Menos seeds
- Menos fatores de densidade

### Execução Paralela
- Utiliza múltiplos cores para acelerar execução
- Cada experimento roda em processo separado
- Monitoramento independente de recursos

### Monitoramento de Recursos
- Uso de memória em tempo real
- Detecção de limitações de hardware
- Timeout automático (1 hora por experimento)

## 📝 EXEMPLOS DE USO

### Validação Rápida
```bash
# Testa todos os experimentos rapidamente
python src/experimentos/executar_todos_experimentos.py --teste_rapido
```

### Análise Completa
```bash
# Executa experimento 2 completo (pode demorar horas)
python src/experimentos/experimento_2_parametros_simples.py --max_vertices 100000
```

### Execução em Cluster
```bash
# Executa em paralelo com 8 cores
python src/experimentos/executar_todos_experimentos.py --modo paralelo --cores 8
```

## ⚠️ CONSIDERAÇÕES IMPORTANTES

### Recursos Necessários
- **Memória:** Experimentos com 100k+ vértices podem requerer 8GB+ RAM
- **Tempo:** Experimentos completos podem demorar horas/dias
- **Armazenamento:** Resultados podem ocupar centenas de MB

### Recomendações
1. **Sempre teste primeiro** com `--teste_rapido`
2. **Monitore recursos** durante execução
3. **Use execução paralela** em clusters
4. **Faça backup** dos resultados importantes

### Limitações Conhecidas
- Grafos com 1M+ vértices podem exceder memória disponível
- Alguns tipos de grafos podem falhar com certas configurações
- Cálculo de métricas para grafos muito grandes pode ser lento

## 📚 ANÁLISE DOS RESULTADOS

### Ferramentas Recomendadas
- **Python:** pandas, matplotlib, seaborn
- **R:** ggplot2, dplyr
- **Excel:** Para análises básicas
- **Jupyter:** Para análises interativas

### Exemplos de Análise
```python
import pandas as pd
import matplotlib.pyplot as plt

# Carrega resultados
df = pd.read_csv('resultados_experimento1.csv')

# Análise por gerador
df.groupby('gerador')['tempo_geracao'].mean()

# Análise por tamanho
df.groupby('numV')['densidade'].mean().plot()
```

## 🤝 CONTRIBUIÇÕES

Para adicionar novos experimentos:
1. Crie script seguindo o padrão dos existentes
2. Adicione ao `executar_todos_experimentos.py`
3. Atualize esta documentação
4. Teste com `--teste_rapido` primeiro
