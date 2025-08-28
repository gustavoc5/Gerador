# 📊 TABELAS COMPLETAS DOS EXPERIMENTOS

## 🎯 VISÃO GERAL DOS EXPERIMENTOS

| **Experimento** | **Gerador** | **Testes** | **Grafos por Teste** | **Total de Grafos** | **Arquivo** |
|-----------------|-------------|------------|---------------------|-------------------|-------------|
| **Simples Completo** | Simples | 1.800 | 50 | **90.000** | `experimento_simples_completo.py` |
| **Power-Law Completo** | Power-Law | 900 | 50 | **45.000** | `experimento_powerlaw_completo.py` |
| **TOTAL** | - | **2.700** | - | **135.000** | - |

---

## 🔢 EXPERIMENTO SIMPLES COMPLETO

### **Parâmetros do Experimento:**

| **Parâmetro** | **Valores** | **Descrição** |
|---------------|-------------|---------------|
| **Tipos de Grafo** | 0, 1, 20, 21, 30, 31 | 6 tipos diferentes |
| **Vértices (numV)** | 100, 1000, 10000, 100000, 1000000 | 5 tamanhos |
| **Preferência Densidade** | 0, 1, 2 | 0=Sem preferência, 1=Esparso, 2=Denso |
| **Componentes (numC)** | 0, 1 | 0=Aleatório, 1=Conexo |
| **Seeds** | 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000 | 10 seeds |
| **Grafos por Teste** | 50 | Valor fixo |

### **Cálculo de Combinações:**
```
6 tipos × 5 vértices × 3 preferências × 2 componentes × 10 seeds = 1.800 testes
1.800 testes × 50 grafos = 90.000 grafos
```

### **Tabela de Tipos de Grafos:**

| **Código** | **Nome** | **Dirigido** | **Laços** | **Arestas Múltiplas** |
|------------|----------|--------------|-----------|----------------------|
| **0** | Simples | ❌ | ❌ | ❌ |
| **1** | Digrafo | ✅ | ❌ | ❌ |
| **20** | Multigrafo | ❌ | ❌ | ✅ |
| **21** | Multigrafo-Dirigido | ✅ | ❌ | ✅ |
| **30** | Pseudografo | ❌ | ✅ | ✅ |
| **31** | Pseudografo-Dirigido | ✅ | ✅ | ✅ |

### **Tabela de Preferências de Densidade:**

| **Código** | **Nome** | **Densidade** | **Característica** |
|------------|----------|---------------|-------------------|
| **0** | Sem preferência | Aleatória | Qualquer densidade válida |
| **1** | Esparso | d ≤ 0.2 | Poucas arestas |
| **2** | Denso | d ≥ 0.8 | Muitas arestas |

### **Tabela de Componentes:**

| **Código** | **Nome** | **Descrição** |
|------------|----------|---------------|
| **0** | Aleatório | Número de componentes gerado aleatoriamente |
| **1** | Conexo | Grafo sempre conexo (1 componente) |

---

## 🔢 EXPERIMENTO POWER-LAW COMPLETO

### **Parâmetros do Experimento:**

| **Parâmetro** | **Valores** | **Descrição** |
|---------------|-------------|---------------|
| **Tipos de Grafo** | 0, 1, 20, 21, 30, 31 | 6 tipos diferentes |
| **Vértices (numV)** | 100, 1000, 10000, 100000, 1000000 | 5 tamanhos |
| **Gamma (γ)** | Denso, Moderado, Esparso | 3 categorias com intervalos |
| **Seeds** | 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000 | 10 seeds |
| **Grafos por Teste** | 50 | Valor fixo |

### **Cálculo de Combinações:**
```
6 tipos × 5 vértices × 3 categorias × 10 seeds = 900 testes
900 testes × 50 grafos = 45.000 grafos
```

### **Tabela de Categorias Gamma:**

| **Categoria** | **Intervalo γ** | **Característica** | **Exemplo de Rede Real** |
|---------------|-----------------|-------------------|--------------------------|
| **Denso** | [2.0, 2.3) | Muitos hubs, muito centralizado | Internet backbone |
| **Moderado** | [2.3, 2.7) | Balanceamento entre hubs e vértices normais | Redes sociais |
| **Esparso** | [2.7, 3.0] | Menos hubs, distribuição mais uniforme | Redes de proteínas |

### **Geração de Gamma por Categoria:**
```python
def gera_gamma_aleatorio(categoria, seed):
    if categoria == 'denso':
        return np.random.uniform(2.0, 2.3)
    elif categoria == 'moderado':
        return np.random.uniform(2.3, 2.7)
    elif categoria == 'esparso':
        return np.random.uniform(2.7, 3.0)
```

---

## 📊 MÉTRICAS COLETADAS

### **Métricas Gerais (Ambos os Geradores):**

| **Categoria** | **Métricas** | **Descrição** |
|---------------|--------------|---------------|
| **Básicas** | num_vertices, num_arestas, densidade, tempo_geracao | Propriedades fundamentais |
| **Conectividade** | num_componentes, conectividade | Estrutura de conectividade |
| **Grau** | grau_medio, grau_mediana, grau_max, grau_min, grau_desvio, grau_skewness, grau_kurtosis | Distribuição de graus |
| **Distância** | diametro, raio, distancia_media | Propriedades de distância |
| **Centralidade** | PageRank (média, mediana, máximo, mínimo, desvio), Closeness (média, mediana, máximo, mínimo, desvio), Betweenness (média, mediana, máximo, mínimo, desvio) | Medidas de centralidade |
| **Comunidades** | num_comunidades, modularidade_greedy, modularidade_label_propagation | Detecção de comunidades |

### **Métricas Específicas do Simples:**

| **Métrica** | **Descrição** |
|-------------|---------------|
| eficiencia_geracao | Eficiência do processo de geração |
| razao_vertices_arestas | Razão entre vértices e arestas |

### **Métricas Específicas do Power-Law:**

| **Métrica** | **Descrição** |
|-------------|---------------|
| qualidade_powerlaw_R | Qualidade do ajuste power-law (R²) |
| qualidade_powerlaw_p_value | P-value do teste Kolmogorov-Smirnov |
| powerlaw_alpha | Expoente alpha da distribuição |
| powerlaw_xmin | Valor mínimo para ajuste |
| eficiencia_geracao_powerlaw | Eficiência da geração power-law |

### **Métricas de Equivalência Estrutural (Entre Replicações):**

| **Métrica** | **Descrição** |
|-------------|---------------|
| n_grafos | Número de grafos replicados |
| n_pares | Número de pares de grafos comparados |
| similaridade_media | Similaridade média entre pares |
| similaridade_mediana | Similaridade mediana entre pares |
| similaridade_desvio | Desvio padrão da similaridade |
| similaridade_min, similaridade_max | Valores mínimo e máximo |
| similaridade_q25, similaridade_q75 | Quartis da distribuição |
| pares_altamente_similares | Número de pares com alta similaridade |
| pares_medianamente_similares | Número de pares com similaridade média |
| pares_pouco_similares | Número de pares com baixa similaridade |
| fracao_altamente_similares | Fração de pares altamente similares |
| fracao_medianamente_similares | Fração de pares medianamente similares |
| fracao_pouco_similares | Fração de pares pouco similares |
| consistencia_estrutural | Medida de consistência estrutural |
| coeficiente_variacao | Coeficiente de variação da similaridade |
| n_outliers_estruturais | Número de outliers estruturais |
| indices_outliers | Índices dos outliers |
| similaridade_media_outliers | Similaridade média dos outliers |
| similaridade_media_nao_outliers | Similaridade média dos não-outliers |

---

## 📁 ESTRUTURA DE SAÍDA

### **Organização dos Arquivos:**

```
resultados_experimentos/
├── exp_simples_completo/
│   ├── resultados_simples_completo.csv      # Dados agregados de todos os testes
│   ├── resumo_simples_completo.csv          # Resumo estatístico
│   └── teste_tX_vY_pP_cC_sW/               # Dados individuais por teste
│       ├── dados_individuais.csv            # Métricas de cada grafo (50 grafos)
│       ├── grafo_X_arestas.txt              # Lista de arestas do grafo X
│       ├── resumo_teste.csv                 # Médias do teste
│       └── info_teste.txt                   # Informações do teste
└── exp_powerlaw_completo/
    ├── resultados_powerlaw_completo.csv     # Dados agregados de todos os testes
    ├── resumo_powerlaw_completo.csv         # Resumo estatístico
    └── teste_tX_vY_cG_sW/                   # Dados individuais por teste
        ├── dados_individuais.csv            # Métricas de cada grafo (50 grafos)
        ├── grafo_X_arestas.txt              # Lista de arestas do grafo X
        ├── resumo_teste.csv                 # Médias do teste
        └── info_teste.txt                   # Informações do teste
```

### **Convenção de Nomenclatura:**

| **Experimento** | **Formato** | **Exemplo** | **Significado** |
|-----------------|-------------|-------------|-----------------|
| **Simples** | `teste_tX_vY_pP_cC_sW` | `teste_t0_v1000_p1_c0_s1000` | Tipo 0, V=1000, Pref=1, Comp=0, Seed=1000 |
| **Power-Law** | `teste_tX_vY_cG_sW` | `teste_t1_v1000_cdenso_s2000` | Tipo 1, V=1000, Cat=denso, Seed=2000 |

---

## 🎯 EXECUÇÃO DOS EXPERIMENTOS

### **Comandos de Execução:**

```bash
# Teste Rápido (versão reduzida)
python src/experimentos/experimento_simples_completo.py --teste_rapido
python src/experimentos/experimento_powerlaw_completo.py --teste_rapido

# Execução Completa
python src/experimentos/experimento_simples_completo.py
python src/experimentos/experimento_powerlaw_completo.py

# Executar Todos
python src/experimentos/executar_todos_experimentos.py
```

### **Parâmetros de Linha de Comando:**

| **Parâmetro** | **Padrão** | **Descrição** |
|---------------|------------|---------------|
| `--output_dir` | `./resultados_experimentos/exp_*_completo` | Diretório de saída |
| `--max_vertices` | 10000 | Máximo de vértices para teste |
| `--seeds` | [1000, 2000, ..., 10000] | Lista de seeds |
| `--teste_rapido` | False | Executa versão reduzida |

---

## 📈 ANÁLISE DOS RESULTADOS

### **Tipos de Análise:**

1. **Análise Descritiva**: Estatísticas básicas por parâmetro
2. **Análise Comparativa**: Comparação entre geradores
3. **Análise de Consistência**: Equivalência estrutural entre replicações
4. **Análise de Escalabilidade**: Comportamento com diferentes tamanhos
5. **Análise de Validação**: Confirmação de que os parâmetros são respeitados

### **Objetivos dos Experimentos:**

1. **Caracterização**: Entender propriedades dos grafos gerados
2. **Comparação**: Diferenças entre geradores Simples e Power-Law
3. **Consistência**: Verificar reprodutibilidade dos resultados
4. **Escalabilidade**: Comportamento com grafos grandes
5. **Validação**: Confirmar que os parâmetros são respeitados
