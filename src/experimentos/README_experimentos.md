# 🧪 EXPERIMENTOS DE GERAÇÃO DE GRAFOS

Sistema simples para testar os geradores de grafos "Simples" e "Power-Law".

## 📋 EXPERIMENTOS DISPONÍVEIS

| Exp | Arquivo | Descrição | Testes |
|-----|---------|-----------|--------|
| 1 | `experimento_1_comparacao_geradores.py` | Comparação básica entre geradores | 72 |
| 2 | `experimento_2_parametros_simples.py` | Parâmetros do gerador simples | 432 |
| 3 | `experimento_3_parametros_powerlaw.py` | Parâmetros do gerador power-law | 432 |
| 4 | `experimento_4_escalabilidade.py` | Testes de escalabilidade | 144 |
| 5 | `experimento_5_replicacoes.py` | Replicações para análise estatística | 576 |

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

# Experimento 5 - Replicações
python src/experimentos/experimento_5_replicacoes.py --teste_rapido
```

### Executar Todos
```bash
# Executa todos os experimentos
python src/experimentos/executar_todos_experimentos.py --teste_rapido

# Executa experimentos específicos
python src/experimentos/executar_todos_experimentos.py --experimentos 1 2 5 --teste_rapido
```

## 📊 ONDE OS RESULTADOS SÃO SALVOS

Cada experimento cria uma pasta `resultados_experimento_X/` com:
- `dados_completos.csv` - Todos os dados brutos
- `resumo_estatisticas.txt` - Resumo das métricas
- `log_execucao.txt` - Log da execução

## ⚙️ PARÂMETROS PRINCIPAIS

- `--teste_rapido`: Executa versão reduzida para teste
- `--max_vertices`: Limite máximo de vértices (padrão: 10000)
- `--output_dir`: Pasta de saída personalizada

## 📈 MÉTRICAS COLETADAS

- **Tempo**: Tempo de geração
- **Estrutura**: Vértices, arestas, densidade, graus
- **Conectividade**: Componentes, modularidade
- **Distância**: Diâmetro, raio, distância média
- **Centralidade**: PageRank, closeness, betweenness
- **Memória**: Uso de RAM em diferentes etapas
- **Qualidade**: Ajuste power-law (R², p-valor)
