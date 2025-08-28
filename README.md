# 🎯 GERADOR DE GRAFOS - TCC

Sistema completo de geração de grafos para análise de redes, desenvolvido como trabalho de conclusão de curso.

## 📁 Estrutura do Projeto

```
Gerador/
├── src/                    # 🧠 Código fonte principal
│   ├── simples/           # Gerador de grafos simples
│   ├── pwl/               # Gerador de grafos power-law
│   ├── gerador_teste_automatico.py  # Gerador automático
│   ├── teste_rapido.py    # Testes rápidos
│   └── README.md          # Documentação do src/
├── resultados_teste/       # 📊 Resultados de testes
│   ├── testes_automaticos/
│   └── testes_rapidos/
├── visualizacoes/         # 📈 Gráficos e visualizações
├── backup_codigos_antigos/ # 📦 Códigos antigos (backup)
├── requirements.txt       # 📋 Dependências
└── README.md             # Este arquivo
```

## 🚀 Como Usar

### 1. Instalação
```bash
pip install -r requirements.txt
```

### 2. Teste Individual
```bash
# Teste simples
python src/simples/test_simples.py --seed 123 --output_txt resultado.txt

# Teste powerlaw
python src/pwl/test_pwl.py --seed 456 --output_txt resultado.txt
```

### 3. Teste Automático com Seed Incremental
```bash
# Gera 20 testes (seed 1000-1019)
python src/gerador_teste_automatico.py --num_testes 20 --base_seed 1000

# Apenas módulo simples
python src/gerador_teste_automatico.py --modulo simples --num_testes 10

# Apenas módulo powerlaw
python src/gerador_teste_automatico.py --modulo powerlaw --num_testes 10
```

### 4. Teste Rápido (Pré-configurado)
```bash
# Gera 60 arquivos (30 simples + 30 powerlaw)
python src/teste_rapido.py
```

## 📊 Tipos de Grafo Suportados

- **0**: Simples
- **1**: Digrafo
- **2**: Multigrafo
- **3**: Multigrafo-Dirigido
- **4**: Pseudografo
- **5**: Pseudografo-Dirigido

## 📈 Formato de Saída

Todos os testes geram arquivos CSV puros organizados por seed:

**Simples (30 campos):**
- Parâmetros: numV, numA, seed, n, numC, fator, tipo, tipo_detectado
- Métricas básicas: num_vertices, num_arestas, densidade, grau_medio, grau_max, grau_min, num_componentes
- Centralidade: pagerank_medio, pagerank_max, closeness_medio, closeness_max, betweenness_medio, betweenness_max
- Distâncias: diametro, raio, distancia_media
- Comunidades: num_comunidades_greedy, modularidade_greedy, num_comunidades_label, modularidade_label
- Tempo: tempo_geracao, timestamp

**Powerlaw (27 campos):**
- Parâmetros: numV, gamma, seed, tipo, tipo_detectado
- Métricas básicas: num_vertices, num_arestas, densidade, grau_medio, grau_max, grau_min, num_componentes
- Centralidade: pagerank_medio, pagerank_max, closeness_medio, closeness_max, betweenness_medio, betweenness_max
- Distâncias: diametro, raio, distancia_media
- Comunidades: num_comunidades_greedy, modularidade_greedy, num_comunidades_label, modularidade_label
- Tempo: tempo_geracao, timestamp

## ⚡ Performance

- **Teste individual**: ~0.1-0.5 segundos
- **Teste automático**: ~2-4 segundos por arquivo
- **Teste rápido**: ~4 minutos para 60 arquivos
- **Seed incremental**: Automático (seed + 1 a cada iteração)

## 🎯 Características

- ✅ **Organização por seed**: Cada seed em diretório separado
- ✅ **Sem condições de corrida**: Arquivos independentes
- ✅ **CSV puro**: Apenas valores, sem cabeçalhos
- ✅ **Tempo de geração**: Incluído em todos os resultados
- ✅ **Parâmetros aleatórios**: Vértices, arestas, gamma, tipo
- ✅ **Execução paralela**: Suporte para testes em massa

## 📝 Documentação Detalhada

Para mais informações sobre os módulos específicos, consulte:
- `src/README.md` - Documentação completa do código fonte
- `src/simples/` - Gerador de grafos simples
- `src/pwl/` - Gerador de grafos power-law

## 🔧 Desenvolvimento

Este projeto foi desenvolvido como parte do TCC em Ciência da Computação, focado na geração e análise de diferentes tipos de grafos para estudos de redes complexas.
