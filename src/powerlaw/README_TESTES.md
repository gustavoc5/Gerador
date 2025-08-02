# 🧪 Sistema de Testes - Módulo Power-Law

## 📋 Visão Geral

O módulo `powerlaw` agora suporta execução de testes via linha de comando, permitindo executar milhares de testes de forma automatizada para grafos com distribuição power-law.

## 🚀 Como Usar

### 1. Teste Básico via Linha de Comando

```bash
# Sintaxe básica
python test_pwl.py [execuções] [vértices] [arquivo_saída]

# Exemplos:
python test_pwl.py                    # Usa valores padrão (2 exec, [100,1000,10000])
python test_pwl.py 5                  # 5 execuções por tipo
python test_pwl.py 10 500,1000,5000   # 10 exec, vértices 500,1000,5000
python test_pwl.py 20 10000 meus_resultados.csv  # Arquivo personalizado
```

### 2. Script de Testes Massivos

```bash
# Executa o script interativo
python mass_test.py

# Opções disponíveis:
# 1. Bateria completa de testes (automático)
# 2. Teste específico (interativo)
# 3. Sair
```

### 3. Execução Direta de Bateria

```bash
# Testes pequenos (rápidos)
python test_pwl.py 5 100,500

# Testes médios
python test_pwl.py 10 1000,5000

# Testes grandes (mais demorados)
python test_pwl.py 8 10000,20000
```

## 📊 Parâmetros

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `execuções` | int | 2 | Número de execuções por tipo de grafo |
| `vértices` | string | "100,1000,10000" | Lista de tamanhos de vértices (separados por vírgula) |
| `arquivo_saída` | string | auto | Nome do arquivo CSV de saída |

## 🎯 Tipos de Grafos Testados

- **0**: Simples
- **1**: Digrafo  
- **20**: Multigrafo
- **21**: Multigrafo-Dirigido
- **30**: Pseudografo
- **31**: Pseudografo-Dirigido

## 📈 Exemplos de Escala

### Teste Pequeno (Rápido)
```bash
python test_pwl.py 5 100,500
# Resultado: 5 × 6 tipos × 2 tamanhos = 60 testes
# Tempo estimado: ~2-3 minutos
```

### Teste Médio
```bash
python test_pwl.py 10 1000,5000
# Resultado: 10 × 6 tipos × 2 tamanhos = 120 testes
# Tempo estimado: ~10-15 minutos
```

### Teste Massivo
```bash
python test_pwl.py 50 500,1000,5000,10000
# Resultado: 50 × 6 tipos × 4 tamanhos = 1.200 testes
# Tempo estimado: ~2-4 horas
```

### Teste Extremo
```bash
python test_pwl.py 100 1000,5000,10000,20000
# Resultado: 100 × 6 tipos × 4 tamanhos = 2.400 testes
# Tempo estimado: ~6-10 horas
```

## 📁 Arquivos de Saída

### Arquivo de Resultados Detalhados
O arquivo CSV principal contém:
- **Métricas básicas**: número de vértices, arestas, tempo de geração
- **Power-law**: gamma, xmin, KS statistic, p-value, R²
- **Graus**: grau médio, máximo, mínimo, desvio padrão
- **Centralidades**: degree centrality, PageRank, closeness
- **Distâncias**: média e diâmetro de hop
- **Comunidades**: número de comunidades (Label Propagation)

### Arquivo de Resumo
O arquivo de resumo contém:
- **Estatísticas agregadas** por tipo de grafo
- **Médias e desvios** das métricas principais
- **Análise de correlação** entre parâmetros

## 🔧 Configurações Avançadas

### Execução em Lote
```bash
# Script para múltiplas execuções
for exec in 5 10 20; do
    for vert in "500,1000" "5000,10000" "20000"; do
        python test_pwl.py $exec $vert
    done
done
```

### Monitoramento
```bash
# Com timestamp e log
python test_pwl.py 50 1000,5000 2>&1 | tee log_$(date +%Y%m%d_%H%M%S).txt
```

### Testes Específicos por Tipo
```bash
# Teste apenas grafos simples
python test_pwl.py 20 1000,5000  # Modificar código para filtrar tipos

# Teste apenas grafos dirigidos
python test_pwl.py 15 5000,10000  # Modificar código para filtrar tipos
```

## ⚠️ Considerações

1. **Memória**: Grafos power-law grandes (10000+ vértices) podem usar muita memória
2. **Tempo**: Cálculo de métricas de centralidade é O(n³) para grafos densos
3. **Disco**: Arquivos CSV podem ficar muito grandes (milhares de linhas)
4. **Power-Law**: Validação de distribuição pode falhar para grafos pequenos
5. **Interrupção**: Use Ctrl+C para parar execuções longas

## 🎯 Características Específicas do Power-Law

### Distribuição de Graus
- **Gamma**: Expoente da distribuição power-law (2.0-3.0)
- **Xmin**: Grau mínimo para ajuste da distribuição
- **KS Test**: Teste de Kolmogorov-Smirnov para qualidade do ajuste

### Validação
- **R²**: Coeficiente de determinação do ajuste
- **P-value**: Significância estatística do ajuste
- **KS Statistic**: Estatística do teste KS

## 🎉 Resultados

O sistema está otimizado para:
- ✅ **Escalabilidade**: Milhares de testes
- ✅ **Robustez**: Tratamento de erros de power-law
- ✅ **Flexibilidade**: Parâmetros configuráveis
- ✅ **Reprodutibilidade**: Seeds fixos
- ✅ **Análise**: Dados estruturados em CSV + resumo
- ✅ **Power-Law**: Validação estatística completa 