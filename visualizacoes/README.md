# 📈 Visualizações

Este diretório contém gráficos e visualizações gerados pelos geradores de grafos.

## 📁 Conteúdo

- **Gráficos PNG**: Visualizações de grafos gerados
- **Arquivos TXT**: Dados detalhados das visualizações
- **Análises**: Gráficos de distribuição de graus e métricas

## 🎨 Tipos de Visualização

### Grafos Pequenos (< 50 vértices)
- **Visualização completa**: Mostra todos os vértices e arestas
- **Layout automático**: Posicionamento otimizado dos nós
- **Cores por tipo**: Diferenciação visual por tipo de grafo

### Grafos Grandes (≥ 50 vértices)
- **Histogramas**: Distribuição de graus
- **Gráficos de centralidade**: PageRank, Closeness, Betweenness
- **Análise de comunidades**: Estrutura modular

## 📊 Arquivos Incluídos

- `Simples-A-30-420-10-1-1.png` - Grafo simples com 30 vértices
- `Pseudografo-A-15-80-10-1-1.png` - Pseudografo com 15 vértices
- `Pseudografo-A-15-80-10-2-1.png` - Pseudografo com 15 vértices (execução 2)

## 🔧 Como Gerar Novas Visualizações

```bash
# Interface interativa para visualização
cd src/simples
python main.py

cd src/powerlaw
python main.py
```

## 📋 Formato dos Arquivos

- **PNG**: Imagens de alta qualidade para apresentações
- **TXT**: Dados estruturados para análise posterior
- **Resolução**: 1920x1080 (padrão)

## 🎯 Uso das Visualizações

1. **Análise visual**: Verificar estrutura dos grafos gerados
2. **Validação**: Confirmar propriedades esperadas
3. **Apresentações**: Usar em slides e relatórios
4. **Documentação**: Ilustrar diferentes tipos de grafos

