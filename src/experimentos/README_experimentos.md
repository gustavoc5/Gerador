# SISTEMA DE EXPERIMENTOS

Sistema simplificado e otimizado para execução de experimentos com geradores de grafos.

## EXPERIMENTOS DISPONÍVEIS

| **ID** | **Arquivo** | **Descrição** | **Testes** | **Grafos por Teste** | **Total de Grafos** |
|--------|-------------|---------------|------------|---------------------|-------------------|
| **S** | `simples.py` | **Simples completo** - Todas as métricas | 1.800 | 50 | **90.000** |
| **P** | `powerlaw.py` | **Power-Law completo** - Todas as métricas | 900 | 50 | **45.000** |

## EXECUÇÃO RÁPIDA

### Teste Rápido (Pequena Amostra)
```bash
# Simples completo
python src/experimentos/simples.py --teste_rapido

# Power-Law completo  
python src/experimentos/powerlaw.py --teste_rapido
```

### Execução Completa
```bash
# Simples completo
python src/experimentos/simples.py

# Power-Law completo
python src/experimentos/powerlaw.py
```

### Executar Todos os Experimentos
```bash
python src/experimentos/executar-tudo.py
```

## MÉTRICAS COLETADAS

### Métricas Gerais (Ambos os Geradores)
- **Básicas**: Vértices, arestas, densidade
- **Conectividade**: Número de componentes, conectividade
- **Grau**: Médio, mediana, máximo, mínimo, desvio, skewness, kurtosis
- **Distância**: Diâmetro, raio, distância média
- **Centralidade**: PageRank, Closeness, Betweenness (média, mediana, máximo, mínimo, desvio)
- **Comunidades**: Número de comunidades e modularidade (greedy e label propagation)

### Métricas Específicas do Simples
- Razão vértices/arestas

### Métricas Específicas do Power-Law
- Qualidade do ajuste power-law (R, p-value)
- Expoente alpha
- Valor xmin

### Métricas de Equivalência Estrutural (Entre Replicações)
- Similaridade média, mediana, desvio
- Consistência estrutural
- Frações de pares altamente/medianamente/pouco similares
- Detecção de outliers estruturais

## ESTRUTURA DE SAÍDA

Cada experimento gera:

```
resultados_experimentos/
├── exp_simples_completo/
│   ├── resultados_simples_completo.csv      # Dados agregados
│   └── resumo_simples_completo.csv          # Resumo estatístico
└── exp_powerlaw_completo/
    ├── resultados_powerlaw_completo.csv     # Dados agregados
    └── resumo_powerlaw_completo.csv         # Resumo estatístico
```

### Arquivos de Saída Detalhados

| **Arquivo** | **Formato** | **Conteúdo** | **Linhas** | **Colunas** |
|-------------|-------------|--------------|------------|-------------|
| `resultados_simples_completo.csv` | CSV | Dados de todos os testes (1.800 linhas) | ~1.800 | ~50 |
| `resumo_simples_completo.csv` | CSV | Médias agrupadas por tipo de grafo | 6 | ~50 |
| `resultados_powerlaw_completo.csv` | CSV | Dados de todos os testes (900 linhas) | ~900 | ~50 |
| `resumo_powerlaw_completo.csv` | CSV | Médias agrupadas por tipo de grafo | 6 | ~50 |

### Exemplo de Estrutura dos Dados CSV

**Colunas Principais (Ambos os Experimentos):**
- `gerador`, `tipo`, `numV`, `seed` (parâmetros)
- `num_vertices`, `num_arestas`, `densidade` (básicas)
- `grau_medio`, `grau_max`, `grau_min`, `grau_desvio` (grau)
- `num_componentes`, `conectividade` (conectividade)
- `pagerank_medio`, `closeness_medio`, `betweenness_medio` (centralidade)
- `diametro`, `raio`, `distancia_media` (distância)
- `num_comunidades_greedy`, `modularidade_greedy` (comunidades)
- `similaridade_media`, `consistencia_estrutural` (equivalência)
- `taxa_sucesso`, `limite_atingido` (controle)

**Colunas Específicas:**
- **Simples**: `preferencia_densidade`, `numC`, `razao_vertices_arestas`
- **Power-Law**: `gamma`, `qualidade_powerlaw_R`, `powerlaw_alpha`, `powerlaw_xmin`

## PARÂMETROS DOS EXPERIMENTOS

### Simples Completo
- **Tipos**: 0, 1, 20, 21, 30, 31 (6 tipos)
- **Vértices**: 100, 1000, 10000, 100000, 1000000
- **Preferência densidade**: 0 (Sem preferência), 1 (Esparso), 2 (Denso)
- **Componentes**: 0 (Aleatório), 1 (Conexo)
- **Seeds**: 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000
- **Grafos por teste**: 50 (fixo)

### Power-Law Completo
- **Tipos**: 0, 1, 20, 21, 30, 31 (6 tipos)
- **Vértices**: 100, 1000, 10000, 100000, 1000000
- **Gamma**: Denso (2.0-2.3), Moderado (2.3-2.7), Esparso (2.7-3.0)
- **Seeds**: 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000
- **Grafos por teste**: 50 (fixo)

## CÁLCULO DETALHADO

### Experimento Simples Completo:
- **Tipos**: 6 (0, 1, 20, 21, 30, 31)
- **Vértices**: 5 (100, 1000, 10000, 100000, 1000000)
- **Preferência densidade**: 3 (0, 1, 2)
- **Componentes**: 2 (0=Aleatório, 1=Conexo)
- **Seeds**: 10 (1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000)
- **Total**: 6 × 5 × 3 × 2 × 10 = **1.800 testes**
- **Grafos por teste**: **50**
- **Total de grafos**: 1.800 × 50 = **90.000 grafos**

### Experimento Power-Law Completo:
- **Tipos**: 6 (0, 1, 20, 21, 30, 31)
- **Vértices**: 5 (100, 1000, 10000, 100000, 1000000)
- **Gamma**: 3 categorias (Denso, Moderado, Esparso)
- **Seeds**: 10 (1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000)
- **Total**: 6 × 5 × 3 × 10 = **900 testes**
- **Grafos por teste**: **50**
- **Total de grafos**: 900 × 50 = **45.000 grafos**

### Resumo Geral:
- **Total de testes**: 1.800 + 900 = **2.700 testes**
- **Total de grafos**: 90.000 + 45.000 = **135.000 grafos**

## FERRAMENTAS AUXILIARES

### `similaridade.py`
Módulo para análise de equivalência estrutural entre grafos replicados:
- Similaridade entre pares de grafos
- Consistência estrutural
- Detecção de outliers
- Comparação entre geradores

### `executar-tudo.py`
Script para execução automatizada de todos os experimentos:
- Execução sequencial
- Relatórios consolidados
- Análise comparativa

## ANÁLISE DOS RESULTADOS

Os experimentos geram dados estruturados para análise:
- **Análise descritiva**: Estatísticas básicas por parâmetro
- **Análise comparativa**: Comparação entre geradores
- **Análise de consistência**: Equivalência estrutural entre replicações
- **Análise de escalabilidade**: Comportamento com diferentes tamanhos

## OBJETIVOS DOS EXPERIMENTOS

1. **Caracterização**: Entender propriedades dos grafos gerados
2. **Comparação**: Diferenças entre geradores Simples e Power-Law
3. **Consistência**: Verificar reprodutibilidade dos resultados
4. **Escalabilidade**: Comportamento com grafos grandes
5. **Validação**: Confirmar que os parâmetros são respeitados

## TIPOS DE GRAFOS

### Códigos dos Tipos:
- **0**: Simples (Não dirigido, sem laços, sem arestas múltiplas)
- **1**: Digrafo (Dirigido, sem laços, sem arestas múltiplas)
- **20**: Multigrafo (Não dirigido, sem laços, com arestas múltiplas)
- **21**: Multigrafo-Dirigido (Dirigido, sem laços, com arestas múltiplas)
- **30**: Pseudografo (Não dirigido, com laços, com arestas múltiplas)
- **31**: Pseudografo-Dirigido (Dirigido, com laços, com arestas múltiplas)

## CATEGORIAS DE DENSIDADE (Power-Law)

### Gamma por Categoria:
- **Denso**: γ ∈ [2.0, 2.3) - Muitos hubs, muito centralizado
- **Moderado**: γ ∈ [2.3, 2.7) - Balanceamento entre hubs e vértices normais
- **Esparso**: γ ∈ [2.7, 3.0] - Menos hubs, distribuição mais uniforme

### Vantagens da Abordagem com Intervalos:
- **Mais realista**: Representa variação natural das redes reais
- **Cobertura ampla**: Qualquer valor dentro do intervalo é testado
- **Foco conceitual**: Concentra-se nas características da rede
- **Eficiência**: Reduz o número de testes mantendo a qualidade
