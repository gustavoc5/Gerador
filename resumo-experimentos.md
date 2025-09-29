# DOCUMENTO TÉCNICO - SISTEMA DE EXPERIMENTOS

---

## RESUMO

Este documento apresenta a metodologia completa desenvolvida para análise comparativa de dois geradores de grafos: o gerador Simples (baseado em grafos aleatórios) e o gerador Power-Law (baseado em redes livre de escala). O sistema foi projetado para execução em ambientes computacionais de alto desempenho, com foco na paralelização eficiente e robustez estatística.

A implementação contempla a geração de 135.000 grafos distribuídos em 2.700 testes experimentais, com coleta de mais de 80 métricas por grafo, totalizando aproximadamente 10.800.000 observações métricas. O sistema foi otimizado para execução em clusters computacionais, permitindo máxima utilização dos recursos disponíveis.

---

## 1. INTRODUÇÃO

### 1.1 Contexto e Objetivos

O estudo de geradores de grafos é fundamental para compreensão de estruturas de dados complexas e suas aplicações em diversas áreas da computação. Este projeto visa estabelecer uma comparação sistemática entre dois paradigmas distintos de geração de grafos, analisando suas características estruturais, propriedades topológicas e comportamento computacional.

### 1.2 Escopo do Sistema

O sistema desenvolvido abrange:
- Dois geradores distintos (Simples e Power-Law)
- Seis tipos diferentes de grafos
- Cinco escalas de tamanho (100 a 1.000.000 vértices)
- Múltiplas configurações de parâmetros
- Sistema de execução paralela otimizado
- Coleta abrangente de métricas estruturais e computacionais

---

## 2. METODOLOGIA EXPERIMENTAL

### 2.1 Configuração dos Experimentos

#### 2.1.1 Gerador Simples

**Parâmetros de Configuração:**
- **Tipos de Grafo**: 6 (Simples, Dirigido, Multigrafo, Multigrafo-Dirigido, Pseudografo, Pseudografo-Dirigido)
- **Tamanhos**: 5 escalas (100, 1.000, 10.000, 100.000, 1.000.000 vértices)
- **Preferência de Densidade**: 3 níveis (Sem preferência, Esparso, Denso)
- **Componentes**: 2 estratégias (Aleatório, Conexo)
- **Seeds**: 10 valores distintos para reprodutibilidade
- **Replicações**: 50 grafos por configuração

**Cálculo de Combinações:**
```
Total de Testes = 6 × 5 × 3 × 2 × 10 = 1.800 testes
Total de Grafos = 1.800 × 50 = 90.000 grafos
```

#### 2.1.2 Gerador Power-Law

**Parâmetros de Configuração:**
- **Tipos de Grafo**: 6 (mesmos tipos do gerador Simples)
- **Tamanhos**: 5 escalas (100, 1.000, 10.000, 100.000, 1.000.000 vértices)
- **Categorias Gamma**: 3 intervalos (Denso: 2.0-2.3, Moderado: 2.3-2.7, Esparso: 2.7-3.0)
- **Seeds**: 10 valores distintos para reprodutibilidade
- **Replicações**: 50 grafos por configuração

**Cálculo de Combinações:**
```
Total de Testes = 6 × 5 × 3 × 10 = 900 testes
Total de Grafos = 900 × 50 = 45.000 grafos
```

### 2.2 Métricas Coletadas

#### 2.2.1 Métricas Estruturais (25+ métricas)

**Propriedades Básicas:**
- Número de vértices e arestas
- Densidade do grafo
- Distribuição de graus (média, máximo, mínimo, desvio padrão, mediana)
- Assimetria e curtose da distribuição de graus

**Propriedades Topológicas:**
- Diâmetro e raio do grafo
- Distância média entre vértices
- Conectividade do grafo
- Número de componentes conexos

#### 2.2.2 Métricas de Centralidade (15+ métricas)

**PageRank:**
- Média, máximo, mínimo, desvio padrão, mediana

**Closeness Centrality:**
- Média, máximo, mínimo, desvio padrão, mediana

**Betweenness Centrality:**
- Média, máximo, mínimo, desvio padrão, mediana

#### 2.2.3 Métricas de Comunidade (4 métricas)

**Algoritmo Greedy:**
- Modularidade
- Número de comunidades

**Label Propagation:**
- Modularidade
- Número de comunidades

#### 2.2.4 Métricas Específicas por Gerador

**Gerador Simples:**
- Eficiência de geração (tempo por grafo)
- Razão vértices/arestas

**Gerador Power-Law:**
- Qualidade do ajuste power-law (R² e p-valor do teste Kolmogorov-Smirnov)
- Expoente alpha da distribuição
- Valor xmin para ajuste da distribuição
- Eficiência de geração power-law

#### 2.2.5 Métricas de Equivalência Estrutural (20+ métricas)

**Análise de Similaridade:**
- Similaridade média e mediana entre replicações
- Consistência estrutural
- Detecção de outliers estruturais
- Coeficiente de variação das replicações

#### 2.2.6 Métricas de Performance (8+ métricas)

**Recursos Computacionais:**
- Tempo de geração
- Uso de memória (inicial, pico, final)
- Taxa de sucesso
- Limitações de hardware

---

## 3. ESTRATÉGIA DE PARALELIZAÇÃO

### 3.1 Arquitetura do Sistema

O sistema foi projetado seguindo princípios de computação paralela distribuída, com foco na independência de execução e máxima utilização de recursos computacionais.

#### 3.1.1 Princípios de Design

**Independência Total:**
- Cada execução é completamente independente
- Não há dependências entre diferentes seeds
- Eliminação de condições de corrida

**Escalabilidade Linear:**
- Performance proporcional ao número de cores disponíveis
- Utilização eficiente de recursos computacionais
- Adaptabilidade a diferentes configurações de cluster

**Robustez Operacional:**
- Recuperação automática de falhas
- Monitoramento individual de execuções
- Logs detalhados para diagnóstico

### 3.2 Implementação da Paralelização

#### 3.2.1 Estratégia Baseada em Seeds

A paralelização é implementada através da divisão do trabalho por seeds, onde cada seed representa uma execução independente do experimento completo.

**Vantagens da Abordagem:**
- **Simplicidade**: Cada seed executa o experimento completo
- **Independência**: Não há comunicação entre execuções
- **Escalabilidade**: Número de execuções paralelas igual ao número de seeds
- **Recuperação**: Falhas isoladas não afetam outras execuções

#### 3.2.2 Estrutura de Diretórios

```
resultados_experimentos/
├── exp_simples_completo/
│   ├── resultados_simples_completo.csv
│   ├── resumo_simples_completo.csv
│   └── {seed}/
│       ├── resultados_simples_completo.csv
│       └── log.txt
└── exp_powerlaw_completo/
    ├── resultados_powerlaw_completo.csv
    ├── resumo_powerlaw_completo.csv
    └── {seed}/
        ├── resultados_powerlaw_completo.csv
        └── log.txt
```

#### 3.2.3 Geração de Comandos

O sistema inclui um gerador de comandos que cria scripts de execução para cada seed:

```bash
# Exemplo de comando gerado para seed 1000
python src/experimentos/experimento_simples_completo.py \
    --output_dir resultados_experimentos/exp_simples_completo/1000 \
    --seeds 1000 \
    &> resultados_experimentos/exp_simples_completo/1000/log.txt
```

### 3.3 Execução em Clusters

#### 3.3.1 Preparação para Execução

**Geração de Comandos:**
```bash
python src/experimentos/paralelizacao.py \
    --main_dir "/path/to/project" \
    --experimento todos \
    --seeds 1000 2000 3000 4000 5000 6000 7000 8000 9000 10000 \
    --output_dir ./comandos_paralelos
```

**Execução Paralela:**
```bash
# Execução com 4 threads
cat comandos_paralelos/comandos_todos.sh | parallel -j 4

# Execução com número de cores disponíveis
cat comandos_paralelos/comandos_todos.sh | parallel -j $(nproc)
```

#### 3.3.2 Submissão em Sistemas de Job

**Exemplo para SLURM:**
```bash
#!/bin/bash
#SBATCH --job-name=experimentos_grafos
#SBATCH --output=logs/exp_%A_%a.out
#SBATCH --error=logs/exp_%A_%a.err
#SBATCH --array=1-20
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --time=24:00:00

# Execução do experimento
python src/experimentos/experimento_simples_completo.py \
    --output_dir resultados_experimentos/exp_simples_completo/${SLURM_ARRAY_TASK_ID} \
    --seeds ${SLURM_ARRAY_TASK_ID}
```

### 3.4 Concatenação de Resultados

#### 3.4.1 Script de Concatenação

Após a conclusão de todas as execuções, um script automatizado concatena os resultados:

```bash
#!/bin/bash
# Script para concatenar resultados de todas as seeds

echo "Iniciando concatenação de resultados..."

# Concatenação do experimento Simples
cat > resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv << 'EOF'
gerador,tipo,numV,numA,seed,estrategia_arestas,preferencia_densidade,numC,num_grafos_gerados
EOF

for seed in 1000 2000 3000 4000 5000 6000 7000 8000 9000 10000; do
    if [ -f resultados_experimentos/exp_simples_completo/${seed}/resultados_simples_completo.csv ]; then
        tail -n +2 resultados_experimentos/exp_simples_completo/${seed}/resultados_simples_completo.csv \
            >> resultados_experimentos/exp_simples_completo/resultados_simples_completo.csv
        echo "Seed ${seed} (Simples): OK"
    else
        echo "Seed ${seed} (Simples): ARQUIVO NÃO ENCONTRADO"
    fi
done

# Concatenação do experimento Power-Law
# ... código similar para Power-Law ...

echo "Concatenação concluída."
```

---

## 4. CONTROLES DE QUALIDADE

### 4.1 Validação de Parâmetros

O sistema implementa verificações automáticas para garantir que os grafos gerados respeitem os parâmetros de entrada:

**Verificações Implementadas:**
- Confirmação do número de vértices
- Validação do número de arestas
- Verificação da conectividade (quando especificada)
- Análise da distribuição de graus (para Power-Law)

### 4.2 Reprodutibilidade

**Controle de Seeds:**
- Seeds fixas para reprodutibilidade
- Documentação completa dos valores utilizados
- Verificação de consistência entre execuções

### 4.3 Monitoramento de Performance

**Métricas de Monitoramento:**
- Tempo de execução por seed
- Uso de memória durante execução
- Taxa de sucesso por configuração
- Detecção de limitações de recursos

### 4.4 Detecção de Erros

**Sistema de Logs:**
- Logs detalhados por execução
- Identificação de falhas específicas
- Rastreamento de problemas de recursos
- Relatórios de status de execução

---

## 5. ESTIMATIVAS DE RECURSOS

### 5.1 Otimizações Implementadas

**Gerenciamento de Memória:**
- Monitoramento contínuo do uso de memória
- Limpeza automática de objetos temporários
- Alocação dinâmica baseada no tamanho do grafo

**Compressão de Dados:**
- Armazenamento otimizado de matrizes de adjacência
- Compressão de logs e arquivos temporários
- Estruturas de dados eficientes para grafos grandes

---

## 6. ANÁLISE ESTATÍSTICA

### 6.1 Robustez Estatística

**Justificativa das Replicações:**
- 50 replicações por configuração para análise estatística robusta
- Base sólida para inferência estatística
- Detecção de outliers e valores atípicos

**Diversidade de Parâmetros:**
- 15 combinações diferentes de parâmetros
- Cobertura ampla do espaço de parâmetros
- Análise de sensibilidade a diferentes configurações

### 6.2 Métricas de Qualidade

**Equivalência Estrutural:**
- Análise de similaridade entre replicações
- Medida de consistência estrutural
- Detecção de configurações problemáticas

**Qualidade de Ajuste (Power-Law):**
- Teste Kolmogorov-Smirnov para validação
- Coeficiente de determinação (R²)
- Análise de significância estatística

---

## 7. CONCLUSÕES

### 7.1 Contribuições do Sistema

**Metodologia Robusta:**
- Sistema completo para análise comparativa de geradores
- Metodologia replicável para estudos similares
- Documentação abrangente de procedimentos

**Eficiência Computacional:**
- Paralelização otimizada para clusters
- Utilização eficiente de recursos computacionais
- Sistema robusto a falhas e interrupções

**Análise Abrangente:**
- Coleta de mais de 80 métricas por grafo
- Cobertura completa de parâmetros relevantes
- Base sólida para inferência estatística

### 7.2 Impacto Esperado

**Contribuição Científica:**
- Base de dados única para análise de geradores
- Insights sobre comportamento de diferentes paradigmas
- Metodologia para estudos futuros

**Aplicabilidade:**
- Resultados úteis para pesquisas em teoria de grafos
- Metodologia aplicável a outros geradores
- Ferramentas para análise de redes complexas

### 7.3 Próximos Passos

**Execução e Análise:**
1. Execução completa em ambiente de cluster
2. Processamento estatístico dos resultados
3. Análise comparativa entre geradores
4. Identificação de padrões e insights

**Publicação e Disseminação:**
1. Preparação de artigos científicos
2. Documentação técnica completa
3. Disponibilização de código e dados
4. Apresentação em eventos científicos

---
