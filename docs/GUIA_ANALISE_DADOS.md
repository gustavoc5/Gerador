# Guia de Análise dos Dados Experimentais

## 📊 Estrutura dos Dados

### Organização
```
resultados_experimentos/
├── exp_simples_completo/
│   ├── {seed}/
│   │   └── dados_consolidados.csv
│   └── ...
└── exp_powerlaw_completo/
    ├── {seed}/
    │   └── dados_consolidados.csv
    └── ...
```

### Campos Importantes

**Identificação:**
- `num_vertices` / `numV`: Tamanho do grafo (100, 1000, 10000, 100000, 1000000)
- `seed`: Seed do experimento
- `tipo`: Tipo de grafo (0-31 para Simples, 0-31 para Power-Law)
- `gamma`: Parâmetro gamma (Power-Law)
- `preferencia_densidade`: Preferência de densidade (Simples)

**Métricas Básicas:**
- `densidade`: Densidade do grafo
- `grau_medio`, `grau_max`, `grau_min`, `grau_desvio`: Estatísticas de grau
- `num_componentes`, `conectividade`: Conectividade

**Centralidades:**
- `pagerank_medio`, `closeness_medio`, `betweenness_medio`: Centralidades médias
- `closeness_amostrado`: Se closeness foi amostrado (1.0 = sim)

**Comunidades:**
- `num_comunidades_greedy`, `modularidade_greedy`: Greedy Modularity
- `num_comunidades_label`, `modularidade_label`: Label Propagation

**Power-Law Específico:**
- `qualidade_powerlaw_R`, `qualidade_powerlaw_p_value`: Qualidade do ajuste
- `powerlaw_alpha`, `powerlaw_xmin`: Parâmetros do ajuste

**Controle:**
- `taxa_sucesso`: Taxa de sucesso (0.0 a 1.0)
- `limite_atingido`: Se atingiu timeout (True/False)
- `tempo_geracao_s`: Tempo de geração em segundos
- `arquivo_origem`, `diretorio_origem`: Rastreabilidade

## ⚠️ Cuidados Importantes

### 1. Valores Especiais
- **`inf`**: Aparece em `diametro`, `raio`, `distancia_media` quando o grafo não é conectado
- **Valores vazios**: Algumas linhas podem ter campos vazios (timeouts parciais)
- **`limite_atingido=True`**: Indica que houve timeout durante cálculo de métricas

### 2. Filtragem Recomendada
```python
# Filtrar apenas experimentos completos
df_completos = df[df['taxa_sucesso'] > 0]
df_sem_timeout = df[df['limite_atingido'] != True]
```

### 3. Tratamento de `inf`
```python
# Substituir inf por NaN ou valor máximo
import numpy as np
df['diametro'] = df['diametro'].replace([np.inf, -np.inf], np.nan)
```

## 🛠️ Ferramentas Recomendadas

### Python (Recomendado)
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar todos os dados
def carregar_todos_dados():
    import glob
    dfs = []
    for csv in glob.glob('resultados_experimentos/**/dados_consolidados.csv'):
        df = pd.read_csv(csv)
        df['seed'] = csv.split('/')[-2]  # Extrair seed do caminho
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)
```

### R
```r
library(dplyr)
library(ggplot2)

# Carregar dados
files <- list.files("resultados_experimentos", 
                    pattern = "dados_consolidados.csv", 
                    recursive = TRUE, 
                    full.names = TRUE)
df <- bind_rows(lapply(files, read.csv))
```

### Excel/Power BI
- Use "Get Data" → "From Folder" para importar todos os CSVs
- Combine em uma única tabela
- Use Power Query para limpeza

## 📈 Análises Sugeridas

### 1. Taxa de Sucesso por Tamanho
```python
df.groupby(['num_vertices', 'gerador'])['taxa_sucesso'].mean()
```

### 2. Comparação Simples vs Power-Law
- Densidade média por tamanho
- Distribuição de graus
- Modularidade média
- Tempo de geração

### 3. Escalabilidade
- Como métricas variam com tamanho do grafo
- Tempo de geração vs número de vértices
- Taxa de sucesso vs tamanho

### 4. Análise de Power-Law
- Distribuição de `powerlaw_alpha` por gamma
- Qualidade do ajuste (`qualidade_powerlaw_R`, `p_value`)
- Relação entre `gamma` e `powerlaw_alpha`

### 5. Análise de Comunidades
- Comparação entre Greedy e Label Propagation
- Modularidade por tipo de grafo
- Número de comunidades vs tamanho

### 6. Centralidades
- Correlação entre diferentes centralidades
- Distribuição de centralidades por tipo
- Impacto do amostragem (`closeness_amostrado`)

## 📊 Visualizações Úteis

### 1. Heatmap de Taxa de Sucesso
```python
pivot = df.pivot_table(values='taxa_sucesso', 
                       index='num_vertices', 
                       columns='gerador')
sns.heatmap(pivot, annot=True, fmt='.2f')
```

### 2. Boxplot de Métricas por Tamanho
```python
sns.boxplot(data=df, x='num_vertices', y='densidade', hue='gerador')
```

### 3. Scatter: Tempo vs Tamanho
```python
plt.scatter(df['num_vertices'], df['tempo_geracao_s'], 
            c=df['gerador'].map({'Simples': 'blue', 'Power-Law': 'red'}))
plt.xscale('log')
plt.yscale('log')
```

### 4. Distribuição de Power-Law Alpha
```python
df_pwl = df[df['gerador'] == 'Power-Law']
sns.histplot(data=df_pwl, x='powerlaw_alpha', hue='gamma', kde=True)
```

## 🔍 Scripts de Exemplo

### Carregar e Limpar Dados
```python
import pandas as pd
import numpy as np
from pathlib import Path

def carregar_dados_consolidados():
    """Carrega todos os CSVs consolidados"""
    dfs = []
    base = Path('resultados_experimentos')
    
    for generator in ['exp_simples_completo', 'exp_powerlaw_completo']:
        gen_dir = base / generator
        for seed_dir in gen_dir.iterdir():
            if not seed_dir.is_dir():
                continue
            csv_file = seed_dir / 'dados_consolidados.csv'
            if csv_file.exists():
                df = pd.read_csv(csv_file)
                df['seed'] = seed_dir.name
                df['gerador'] = 'Simples' if 'simples' in generator else 'Power-Law'
                dfs.append(df)
    
    df_all = pd.concat(dfs, ignore_index=True)
    
    # Limpeza básica
    df_all['num_vertices'] = pd.to_numeric(df_all['num_vertices'], errors='coerce')
    df_all['taxa_sucesso'] = pd.to_numeric(df_all['taxa_sucesso'], errors='coerce')
    
    # Tratar inf
    numeric_cols = df_all.select_dtypes(include=[np.number]).columns
    df_all[numeric_cols] = df_all[numeric_cols].replace([np.inf, -np.inf], np.nan)
    
    return df_all

# Uso
df = carregar_dados_consolidados()
print(f"Total de registros: {len(df)}")
print(f"Seeds únicas: {df['seed'].nunique()}")
print(f"Tamanhos: {sorted(df['num_vertices'].dropna().unique())}")
```

### Análise Exploratória Básica
```python
# Estatísticas descritivas por gerador e tamanho
summary = df.groupby(['gerador', 'num_vertices']).agg({
    'taxa_sucesso': ['mean', 'std', 'count'],
    'densidade': 'mean',
    'tempo_geracao_s': 'mean',
    'modularidade_greedy': 'mean'
})
print(summary)

# Taxa de sucesso por tamanho
sucesso_por_tamanho = df.groupby(['num_vertices', 'gerador'])['taxa_sucesso'].mean()
print(sucesso_por_tamanho)
```

### Comparação Simples vs Power-Law
```python
# Filtrar apenas dados completos
df_completos = df[(df['taxa_sucesso'] > 0) & (df['limite_atingido'] != True)]

# Comparar métricas principais
metricas = ['densidade', 'grau_medio', 'modularidade_greedy', 
            'pagerank_medio', 'closeness_medio']

for metrica in metricas:
    if metrica in df_completos.columns:
        comparacao = df_completos.groupby(['gerador', 'num_vertices'])[metrica].mean()
        print(f"\n{metrica}:")
        print(comparacao)
```

## 📝 Perguntas de Pesquisa Sugeridas

1. **Escalabilidade**: Como os geradores se comportam com grafos maiores?
2. **Qualidade**: Qual gerador produz grafos com propriedades mais interessantes?
3. **Eficiência**: Qual gerador é mais rápido para diferentes tamanhos?
4. **Power-Law**: Os grafos Power-Law realmente seguem distribuição power-law?
5. **Comunidades**: Qual algoritmo de detecção de comunidades funciona melhor?
6. **Centralidades**: Como diferentes centralidades se correlacionam?

## 🎯 Próximos Passos

1. **Exploração Inicial**: Carregue os dados e faça estatísticas descritivas
2. **Limpeza**: Filtre dados incompletos e trate valores especiais
3. **Visualização**: Crie gráficos exploratórios
4. **Análise Comparativa**: Compare Simples vs Power-Law
5. **Análise de Escalabilidade**: Estude comportamento por tamanho
6. **Validação**: Verifique hipóteses sobre propriedades dos grafos

## 📚 Recursos Adicionais

- **Pandas**: Manipulação de dados
- **Seaborn/Matplotlib**: Visualizações
- **NetworkX**: Análise de redes (se precisar trabalhar com grafos individuais)
- **SciPy**: Testes estatísticos
- **Jupyter Notebook**: Ambiente interativo recomendado

---

**Dica Final**: Comece com análises simples e vá aprofundando conforme encontra padrões interessantes nos dados!



