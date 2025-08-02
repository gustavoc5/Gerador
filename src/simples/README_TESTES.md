# 🧪 Sistema de Testes - Módulo Simples

## 📋 Visão Geral

O módulo `simples` agora suporta execução de testes via linha de comando, permitindo executar milhares de testes de forma automatizada.

## 🚀 Como Usar

### 1. Teste Básico via Linha de Comando

```bash
# Sintaxe básica
python test_simples.py [execuções] [vértices] [arquivo_saída]

# Exemplos:
python test_simples.py                    # Usa valores padrão (3 exec, [100,200])
python test_simples.py 5                  # 5 execuções por tipo
python test_simples.py 10 50,100,200      # 10 exec, vértices 50,100,200
python test_simples.py 20 1000 meus_resultados.csv  # Arquivo personalizado
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
python test_simples.py 10 20,50

# Testes médios
python test_simples.py 20 100,200

# Testes grandes (mais demorados)
python test_simples.py 15 500,1000
```

## 📊 Parâmetros

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `execuções` | int | 3 | Número de execuções por tipo de grafo |
| `vértices` | string | "100,200" | Lista de tamanhos de vértices (separados por vírgula) |
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
python test_simples.py 5 20,50
# Resultado: 5 × 6 tipos × 2 tamanhos = 60 testes
# Tempo estimado: ~30 segundos
```

### Teste Médio
```bash
python test_simples.py 20 100,200
# Resultado: 20 × 6 tipos × 2 tamanhos = 240 testes
# Tempo estimado: ~5 minutos
```

### Teste Massivo
```bash
python test_simples.py 100 50,100,200,500
# Resultado: 100 × 6 tipos × 4 tamanhos = 2.400 testes
# Tempo estimado: ~2-3 horas
```

### Teste Extremo
```bash
python test_simples.py 500 100,200,500,1000
# Resultado: 500 × 6 tipos × 4 tamanhos = 12.000 testes
# Tempo estimado: ~12-15 horas
```

## 📁 Arquivos de Saída

Os arquivos CSV gerados contêm:
- **Métricas básicas**: grau médio, grau máximo, número de arestas
- **Centralidades**: degree centrality, PageRank
- **Distâncias**: média e diâmetro de hop
- **Comunidades**: número de comunidades detectadas
- **Validações**: tipo detectado, correção de tipo, componentes

## 🔧 Configurações Avançadas

### Execução em Lote
```bash
# Script para múltiplas execuções
for exec in 10 20 50; do
    for vert in "50,100" "200,500" "1000"; do
        python test_simples.py $exec $vert
    done
done
```

### Monitoramento
```bash
# Com timestamp e log
python test_simples.py 100 200,500 2>&1 | tee log_$(date +%Y%m%d_%H%M%S).txt
```

## ⚠️ Considerações

1. **Memória**: Testes com grafos grandes (1000+ vértices) podem usar mais memória
2. **Tempo**: Grafos densos demoram mais para gerar
3. **Disco**: Arquivos CSV podem ficar grandes (milhares de linhas)
4. **Interrupção**: Use Ctrl+C para parar execuções longas

## 🎉 Resultados

O sistema está otimizado para:
- ✅ **Escalabilidade**: Milhares de testes
- ✅ **Robustez**: Tratamento de erros
- ✅ **Flexibilidade**: Parâmetros configuráveis
- ✅ **Reprodutibilidade**: Seeds fixos
- ✅ **Análise**: Dados estruturados em CSV 