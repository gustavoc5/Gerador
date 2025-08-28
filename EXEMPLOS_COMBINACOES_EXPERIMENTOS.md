# 🔍 EXEMPLOS DE COMBINAÇÕES DOS EXPERIMENTOS

## 🎯 EXEMPLOS PRÁTICOS DE TESTES

### **EXPERIMENTO SIMPLES COMPLETO**

#### **Exemplo 1: Grafo Simples Pequeno Esparso**
```
Teste: teste_t0_v100_p1_c0_s1000
Parâmetros:
- Tipo: 0 (Simples)
- Vértices: 100
- Preferência: 1 (Esparso)
- Componentes: 0 (Aleatório)
- Seed: 1000
- Grafos gerados: 50
```

#### **Exemplo 2: Digrafo Médio Denso Conexo**
```
Teste: teste_t1_v1000_p2_c1_s2000
Parâmetros:
- Tipo: 1 (Digrafo)
- Vértices: 1000
- Preferência: 2 (Denso)
- Componentes: 1 (Conexo)
- Seed: 2000
- Grafos gerados: 50
```

#### **Exemplo 3: Multigrafo Grande Sem Preferência**
```
Teste: teste_t20_v10000_p0_c0_s3000
Parâmetros:
- Tipo: 20 (Multigrafo)
- Vértices: 10000
- Preferência: 0 (Sem preferência)
- Componentes: 0 (Aleatório)
- Seed: 3000
- Grafos gerados: 50
```

### **EXPERIMENTO POWER-LAW COMPLETO**

#### **Exemplo 1: Grafo Simples Pequeno Denso**
```
Teste: teste_t0_v100_cdenso_s1000
Parâmetros:
- Tipo: 0 (Simples)
- Vértices: 100
- Categoria: denso (γ ∈ [2.0, 2.3))
- Seed: 1000
- Gamma gerado: 2.156 (exemplo)
- Grafos gerados: 50
```

#### **Exemplo 2: Digrafo Médio Moderado**
```
Teste: teste_t1_v1000_cmoderado_s2000
Parâmetros:
- Tipo: 1 (Digrafo)
- Vértices: 1000
- Categoria: moderado (γ ∈ [2.3, 2.7))
- Seed: 2000
- Gamma gerado: 2.534 (exemplo)
- Grafos gerados: 50
```

#### **Exemplo 3: Pseudografo Grande Esparso**
```
Teste: teste_t30_v10000_cesparso_s3000
Parâmetros:
- Tipo: 30 (Pseudografo)
- Vértices: 10000
- Categoria: esparso (γ ∈ [2.7, 3.0])
- Seed: 3000
- Gamma gerado: 2.891 (exemplo)
- Grafos gerados: 50
```

---

## 📊 TABELA DE EXEMPLOS COMPLETOS

### **Experimento Simples - Primeiros 10 Testes:**

| **Teste** | **Tipo** | **Vértices** | **Preferência** | **Componentes** | **Seed** | **Descrição** |
|-----------|----------|--------------|-----------------|-----------------|----------|---------------|
| 1 | 0 | 100 | 0 | 0 | 1000 | Simples pequeno sem preferência, aleatório |
| 2 | 0 | 100 | 0 | 1 | 1000 | Simples pequeno sem preferência, conexo |
| 3 | 0 | 100 | 1 | 0 | 1000 | Simples pequeno esparso, aleatório |
| 4 | 0 | 100 | 1 | 1 | 1000 | Simples pequeno esparso, conexo |
| 5 | 0 | 100 | 2 | 0 | 1000 | Simples pequeno denso, aleatório |
| 6 | 0 | 100 | 2 | 1 | 1000 | Simples pequeno denso, conexo |
| 7 | 0 | 100 | 0 | 0 | 2000 | Simples pequeno sem preferência, aleatório |
| 8 | 0 | 100 | 0 | 1 | 2000 | Simples pequeno sem preferência, conexo |
| 9 | 0 | 100 | 1 | 0 | 2000 | Simples pequeno esparso, aleatório |
| 10 | 0 | 100 | 1 | 1 | 2000 | Simples pequeno esparso, conexo |

### **Experimento Power-Law - Primeiros 10 Testes:**

| **Teste** | **Tipo** | **Vértices** | **Categoria** | **Seed** | **Gamma Exemplo** | **Descrição** |
|-----------|----------|--------------|---------------|----------|-------------------|---------------|
| 1 | 0 | 100 | denso | 1000 | 2.156 | Simples pequeno denso |
| 2 | 0 | 100 | moderado | 1000 | 2.534 | Simples pequeno moderado |
| 3 | 0 | 100 | esparso | 1000 | 2.891 | Simples pequeno esparso |
| 4 | 0 | 100 | denso | 2000 | 2.123 | Simples pequeno denso |
| 5 | 0 | 100 | moderado | 2000 | 2.567 | Simples pequeno moderado |
| 6 | 0 | 100 | esparso | 2000 | 2.834 | Simples pequeno esparso |
| 7 | 0 | 100 | denso | 3000 | 2.189 | Simples pequeno denso |
| 8 | 0 | 100 | moderado | 3000 | 2.478 | Simples pequeno moderado |
| 9 | 0 | 100 | esparso | 3000 | 2.756 | Simples pequeno esparso |
| 10 | 0 | 100 | denso | 4000 | 2.234 | Simples pequeno denso |

---

## 🔄 SEQUÊNCIA DE EXECUÇÃO

### **Ordem dos Loops (Experimento Simples):**
```python
for tipo in [0, 1, 20, 21, 30, 31]:           # 6 tipos
    for numV in [100, 1000, 10000, 100000, 1000000]:  # 5 tamanhos
        for pref_dens in [0, 1, 2]:           # 3 preferências
            for numC in [0, 1]:               # 2 componentes
                for seed in [1000, 2000, ..., 10000]:  # 10 seeds
                    # Executa teste
```

### **Ordem dos Loops (Experimento Power-Law):**
```python
for tipo in [0, 1, 20, 21, 30, 31]:           # 6 tipos
    for numV in [100, 1000, 10000, 100000, 1000000]:  # 5 tamanhos
        for categoria in ['denso', 'moderado', 'esparso']:  # 3 categorias
            for seed in [1000, 2000, ..., 10000]:  # 10 seeds
                gamma = gera_gamma_aleatorio(categoria, seed)
                # Executa teste
```

---

## 📁 EXEMPLOS DE ARQUIVOS GERADOS

### **Estrutura de Diretórios (Exemplo):**

```
resultados_experimentos/
├── exp_simples_completo/
│   ├── resultados_simples_completo.csv
│   ├── resumo_simples_completo.csv
│   ├── teste_t0_v100_p0_c0_s1000/
│   │   ├── dados_individuais.csv      # 50 linhas (uma por grafo)
│   │   ├── grafo_1_arestas.txt        # Lista de arestas do grafo 1
│   │   ├── grafo_2_arestas.txt        # Lista de arestas do grafo 2
│   │   ├── ...
│   │   ├── grafo_50_arestas.txt       # Lista de arestas do grafo 50
│   │   ├── resumo_teste.csv           # Médias das 50 execuções
│   │   └── info_teste.txt             # Parâmetros do teste
│   ├── teste_t0_v100_p0_c1_s1000/
│   ├── teste_t0_v100_p1_c0_s1000/
│   └── ...
└── exp_powerlaw_completo/
    ├── resultados_powerlaw_completo.csv
    ├── resumo_powerlaw_completo.csv
    ├── teste_t0_v100_cdenso_s1000/
    │   ├── dados_individuais.csv      # 50 linhas (uma por grafo)
    │   ├── grafo_1_arestas.txt        # Lista de arestas do grafo 1
    │   ├── grafo_2_arestas.txt        # Lista de arestas do grafo 2
    │   ├── ...
    │   ├── grafo_50_arestas.txt       # Lista de arestas do grafo 50
    │   ├── resumo_teste.csv           # Médias das 50 execuções
    │   └── info_teste.txt             # Parâmetros do teste
    ├── teste_t0_v100_cmoderado_s1000/
    ├── teste_t0_v100_cesparso_s1000/
    └── ...
```

### **Conteúdo dos Arquivos (Exemplo):**

#### **dados_individuais.csv:**
```csv
grafo_id,num_vertices,num_arestas,densidade,tempo_geracao,grau_medio,grau_mediana,grau_max,grau_min,grau_desvio,grau_skewness,grau_kurtosis,num_componentes,conectividade,diametro,raio,distancia_media,modularidade_greedy,modularidade_label_propagation,pagerank_medio,pagerank_mediana,pagerank_max,pagerank_min,pagerank_desvio,closeness_medio,closeness_mediana,closeness_max,closeness_min,closeness_desvio,betweenness_medio,betweenness_mediana,betweenness_max,betweenness_min,betweenness_desvio,eficiencia_geracao,razao_vertices_arestas,gamma,qualidade_powerlaw_R,qualidade_powerlaw_p_value,powerlaw_alpha,powerlaw_xmin,eficiencia_geracao_powerlaw,n_grafos,n_pares,similaridade_media,similaridade_mediana,similaridade_desvio,similaridade_min,similaridade_max,similaridade_q25,similaridade_q75,pares_altamente_similares,pares_medianamente_similares,pares_pouco_similares,fracao_altamente_similares,fracao_medianamente_similares,fracao_pouco_similares,consistencia_estrutural,coeficiente_variacao,n_outliers_estruturais,indices_outliers,similaridade_media_outliers,similaridade_media_nao_outliers
1,100,245,0.0495,0.123,4.9,5.0,12,1,2.1,0.8,0.5,3,0.8,8,4,3.2,0.45,0.42,0.01,0.01,0.02,0.005,0.003,0.31,0.31,0.5,0.15,0.08,0.05,0.05,0.12,0.01,0.02,0.95,0.41,2.156,0.89,0.12,2.1,5,0.92,50,1225,0.78,0.79,0.12,0.45,0.95,0.72,0.84,245,612,368,0.20,0.50,0.30,0.85,0.15,3,"[12,34,67]",0.45,0.82
2,100,248,0.0501,0.118,5.0,5.0,11,1,2.0,0.7,0.4,2,0.9,7,3,3.1,0.44,0.41,0.01,0.01,0.02,0.005,0.003,0.32,0.32,0.51,0.16,0.08,0.05,0.05,0.11,0.01,0.02,0.94,0.40,2.156,0.88,0.13,2.1,5,0.91,50,1225,0.77,0.78,0.11,0.46,0.94,0.71,0.83,240,615,370,0.20,0.50,0.30,0.84,0.16,2,"[23,45]",0.47,0.81
...
```

#### **resumo_teste.csv:**
```csv
teste_id,tipo,num_vertices,num_arestas,densidade,tempo_geracao,grau_medio,grau_mediana,grau_max,grau_min,grau_desvio,grau_skewness,grau_kurtosis,num_componentes,conectividade,diametro,raio,distancia_media,modularidade_greedy,modularidade_label_propagation,pagerank_medio,pagerank_mediana,pagerank_max,pagerank_min,pagerank_desvio,closeness_medio,closeness_mediana,closeness_max,closeness_min,closeness_desvio,betweenness_medio,betweenness_mediana,betweenness_max,betweenness_min,betweenness_desvio,eficiencia_geracao,razao_vertices_arestas,gamma,qualidade_powerlaw_R,qualidade_powerlaw_p_value,powerlaw_alpha,powerlaw_xmin,eficiencia_geracao_powerlaw,n_grafos,n_pares,similaridade_media,similaridade_mediana,similaridade_desvio,similaridade_min,similaridade_max,similaridade_q25,similaridade_q75,pares_altamente_similares,pares_medianamente_similares,pares_pouco_similares,fracao_altamente_similares,fracao_medianamente_similares,fracao_pouco_similares,consistencia_estrutural,coeficiente_variacao,n_outliers_estruturais,indices_outliers,similaridade_media_outliers,similaridade_media_nao_outliers
teste_t0_v100_p0_c0_s1000,0,100,246.5,0.0498,0.1205,4.95,5.0,11.5,1.0,2.05,0.75,0.45,2.5,0.85,7.5,3.5,3.15,0.445,0.415,0.01,0.01,0.02,0.005,0.003,0.315,0.315,0.505,0.155,0.08,0.05,0.05,0.115,0.01,0.02,0.945,0.405,2.156,0.885,0.125,2.1,5,0.915,50,1225,0.775,0.785,0.115,0.455,0.945,0.715,0.835,242.5,613.5,369,0.198,0.501,0.301,0.845,0.148,2.5,"[12,23,34,45,67]",0.46,0.815
```

#### **info_teste.txt:**
```
TESTE: teste_t0_v100_p0_c0_s1000
DATA/HORA: 2024-01-15 14:30:25
PARÂMETROS:
- Tipo: 0 (Simples)
- Vértices: 100
- Preferência densidade: 0 (Sem preferência)
- Componentes: 0 (Aleatório)
- Seed: 1000
- Grafos gerados: 50
- Tempo total: 6.025 segundos
- Tempo médio por grafo: 0.1205 segundos
- Taxa de sucesso: 100.0%
```

---

## 🎯 RESUMO DOS EXEMPLOS

### **Características dos Exemplos:**

1. **Reprodutibilidade**: Mesmo seed = mesmos resultados
2. **Variação**: Diferentes seeds = diferentes grafos
3. **Consistência**: 50 grafos por configuração
4. **Completude**: Todas as métricas coletadas
5. **Organização**: Estrutura clara de arquivos

### **Benefícios da Estrutura:**

1. **Análise Individual**: Cada grafo pode ser analisado separadamente
2. **Análise Agregada**: Médias e estatísticas por teste
3. **Análise Comparativa**: Comparação entre diferentes configurações
4. **Reprodutibilidade**: Seeds permitem reproduzir resultados
5. **Escalabilidade**: Estrutura suporta grandes volumes de dados
