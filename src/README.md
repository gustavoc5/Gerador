# 📁 Diretório SRC - Geradores de Grafos

Este diretório contém os geradores de grafos e ferramentas de teste organizados de forma modular.

## 🏗️ Estrutura

```
src/
├── simples/                 # Gerador de grafos simples
│   ├── main.py             # Interface interativa
│   ├── gerador.py          # Lógica principal de geração
│   ├── test_simples.py     # Script de teste automatizado
│   ├── utils.py            # Funções utilitárias
│   ├── constants.py        # Constantes do módulo
│   └── exceptions.py       # Exceções customizadas
├── powerlaw/               # Gerador de grafos power-law
│   ├── main.py             # Interface interativa
│   ├── pwl.py              # Lógica principal de geração
│   ├── test_pwl.py         # Script de teste automatizado
│   ├── constants.py        # Constantes do módulo
│   └── visualizacao.py     # Visualizações (opcional)
├── gerador_teste_automatico.py  # Gerador automático com seed incremental
├── teste_rapido.py         # Gerador de testes rápidos
├── generate_experiments.py # Gerador de comandos para execução paralela
├── concatenate_results.py  # Concatenador de resultados
└── README.md               # Este arquivo
```

## 🚀 Como Usar

### 1. Teste Individual
```bash
# Teste simples
python src/simples/test_simples.py --seed 123 --output_txt resultado.txt

# Teste powerlaw
python src/powerlaw/test_pwl.py --seed 456 --output_txt resultado.txt
```

### 2. Teste Automático com Seed Incremental
```bash
# Gera 20 testes (seed 1000-1019)
python src/gerador_teste_automatico.py --num_testes 20 --base_seed 1000

# Apenas módulo simples
python src/gerador_teste_automatico.py --modulo simples --num_testes 10

# Apenas módulo powerlaw
python src/gerador_teste_automatico.py --modulo powerlaw --num_testes 10
```

### 3. Teste Rápido (Pré-configurado)
```bash
# Gera 60 arquivos (30 simples + 30 powerlaw)
python src/teste_rapido.py
```

### 4. Execução Paralela
```bash
# Gera comandos para execução paralela
python src/generate_experiments.py --main_dir ./resultados --seeds 100 200 300

# Executa os comandos gerados
bash comandos_experimentos.sh
```

## 📊 Formato de Saída

Todos os testes geram arquivos CSV puros com os seguintes campos:

**Simples (30 campos):**
1. numV, 2. numA, 3. seed, 4. n, 5. numC, 6. fator, 7. tipo, 8. tipo_detectado
9. num_vertices, 10. num_arestas, 11. densidade, 12. grau_medio, 13. grau_max, 14. grau_min, 15. num_componentes
16. pagerank_medio, 17. pagerank_max, 18. closeness_medio, 19. closeness_max, 20. betweenness_medio, 21. betweenness_max
22. diametro, 23. raio, 24. distancia_media, 25. num_comunidades_greedy, 26. modularidade_greedy
27. num_comunidades_label, 28. modularidade_label, 29. tempo_geracao, 30. timestamp

**Powerlaw (27 campos):**
1. numV, 2. gamma, 3. seed, 4. tipo, 5. tipo_detectado
6. num_vertices, 7. num_arestas, 8. densidade, 9. grau_medio, 10. grau_max, 11. grau_min, 12. num_componentes
13. pagerank_medio, 14. pagerank_max, 15. closeness_medio, 16. closeness_max, 17. betweenness_medio, 18. betweenness_max
19. diametro, 20. raio, 21. distancia_media, 22. num_comunidades_greedy, 23. modularidade_greedy
24. num_comunidades_label, 25. modularidade_label, 26. tempo_geracao, 27. timestamp

## 🎯 Tipos de Grafo

- **0**: Simples
- **1**: Digrafo
- **2**: Multigrafo
- **3**: Multigrafo-Dirigido
- **4**: Pseudografo
- **5**: Pseudografo-Dirigido

## ⚡ Performance

- **Teste individual**: ~0.1-0.5 segundos
- **Teste automático**: ~2-4 segundos por arquivo
- **Teste rápido**: ~4 minutos para 60 arquivos

## 📝 Notas

- Todos os arquivos são organizados por seed em diretórios separados
- Não há condições de corrida (cada arquivo é independente)
- Métricas são calculadas com valores simplificados para velocidade
- Tempo de geração é incluído em todos os resultados

