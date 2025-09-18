#!/usr/bin/env python3
"""
EXPERIMENTO POWER-LAW COMPLETO
Experimento unificado para o gerador Power-Law com todas as métricas possíveis.

FATORES:
- Tipo de Grafo: 0, 1, 20, 21, 30, 31 (6 tipos)
- Tamanho (numV): 100, 1000, 10000, 100000, 1000000
- Expoente Gamma (γ): 2.0, 2.2, 2.5, 2.8, 3.0
- Seed: 1000, 2000, 3000, 4000, 5000

MÉTRICAS COLETADAS:
- Todas as métricas básicas, de centralidade, distância, comunidades
- Métricas de performance e memória
- Métricas específicas do power-law (qualidade do ajuste)
"""

import os
import sys
import random
import time
import pandas as pd
import numpy as np
import networkx as nx
from datetime import datetime

# Adiciona o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pwl.pwl import geraGrafoPwl
from pwl.constants import GAMMA_MIN, GAMMA_MAX, GRAU_MIN_PADRAO

def gera_gamma_aleatorio(categoria):
    """
    Gera um valor gamma aleatório dentro da categoria especificada.
    
    Args:
        categoria (str): 'denso', 'moderado', ou 'esparso'
    
    Returns:
        float: Valor gamma aleatório no intervalo da categoria
    """
    if categoria == 'denso':
        return np.random.uniform(2.0, 2.3)
    elif categoria == 'moderado':
        return np.random.uniform(2.3, 2.7)
    elif categoria == 'esparso':
        return np.random.uniform(2.7, 3.0)
    else:
        raise ValueError(f"Categoria inválida: {categoria}")



def calcula_qualidade_powerlaw(graus):
    """Calcula a qualidade do ajuste power-law."""
    try:
        import powerlaw
        
        # Filtra graus > 0
        graus_positivos = [g for g in graus if g > 0]
        if len(graus_positivos) < 10:
            return 0.0, 0.0, 0.0, 0.0
        
        # Ajusta distribuição power-law
        fit = powerlaw.Fit(graus_positivos, discrete=True)
        
        # Teste de Kolmogorov-Smirnov
        R, p_value = fit.distribution_compare('power_law', 'exponential', normalized_ratio=True)
        
        # Parâmetros do ajuste
        alpha = fit.alpha
        xmin = fit.xmin
        
        return R, p_value, alpha, xmin
        
    except Exception as e:
        print(f"ERRO no cálculo power-law: {e}")
        return 0.0, 0.0, 0.0, 0.0

def calcula_metricas_completas(matriz, tipo_grafo, graus=None):
    """Calcula todas as métricas possíveis do grafo."""
    import networkx as nx
    
    # Converte matriz para NetworkX
    if tipo_grafo in [1, 21, 31]:  # Dirigidos
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    
    for i in range(len(matriz)):
        G.add_node(i)
        for j in range(len(matriz[i])):
            if matriz[i][j] > 0:
                G.add_edge(i, j)
    
    metricas = {}
    
    # ===== MÉTRICAS BÁSICAS =====
    metricas['num_vertices'] = G.number_of_nodes()
    metricas['num_arestas'] = G.number_of_edges()
    metricas['tipo_detectado'] = tipo_grafo
    
    # Densidade
    if G.number_of_nodes() > 1:
        max_arestas = G.number_of_nodes() * (G.number_of_nodes() - 1)
        if not G.is_directed():
            max_arestas //= 2
        metricas['densidade'] = G.number_of_edges() / max_arestas
    else:
        metricas['densidade'] = 0.0
    
    # ===== MÉTRICAS DE GRAU =====
    if G.number_of_nodes() > 0:
        graus_grafo = [d for n, d in G.degree()]
        metricas['grau_medio'] = np.mean(graus_grafo)
        metricas['grau_max'] = max(graus_grafo)
        metricas['grau_min'] = min(graus_grafo)
        metricas['grau_desvio'] = np.std(graus_grafo)
        metricas['grau_mediana'] = np.median(graus_grafo)
        
        # Distribuição de graus
        metricas['grau_skewness'] = pd.Series(graus_grafo).skew()
        metricas['grau_kurtosis'] = pd.Series(graus_grafo).kurtosis()
    else:
        metricas['grau_medio'] = metricas['grau_max'] = metricas['grau_min'] = 0
        metricas['grau_desvio'] = metricas['grau_mediana'] = 0
        metricas['grau_skewness'] = metricas['grau_kurtosis'] = 0
    
    # ===== MÉTRICAS DE CONECTIVIDADE =====
    try:
        if G.is_directed():
            metricas['num_componentes'] = nx.number_strongly_connected_components(G)
            metricas['conectividade'] = 1.0 if nx.is_strongly_connected(G) else 0.0
        else:
            metricas['num_componentes'] = nx.number_connected_components(G)
            metricas['conectividade'] = 1.0 if nx.is_connected(G) else 0.0
    except:
        metricas['num_componentes'] = 1
        metricas['conectividade'] = 0.0
    
    # ===== MÉTRICAS DE CENTRALIDADE =====
    try:
        pagerank = nx.pagerank(G, max_iter=100)
        metricas['pagerank_medio'] = np.mean(list(pagerank.values()))
        metricas['pagerank_max'] = max(pagerank.values())
        metricas['pagerank_min'] = min(pagerank.values())
        metricas['pagerank_desvio'] = np.std(list(pagerank.values()))
        metricas['pagerank_mediana'] = np.median(list(pagerank.values()))
    except:
        metricas['pagerank_medio'] = metricas['pagerank_max'] = metricas['pagerank_min'] = 0.0
        metricas['pagerank_desvio'] = metricas['pagerank_mediana'] = 0.0
    
    try:
        closeness = nx.closeness_centrality(G)
        metricas['closeness_medio'] = np.mean(list(closeness.values()))
        metricas['closeness_max'] = max(closeness.values())
        metricas['closeness_min'] = min(closeness.values())
        metricas['closeness_desvio'] = np.std(list(closeness.values()))
        metricas['closeness_mediana'] = np.median(list(closeness.values()))
    except:
        metricas['closeness_medio'] = metricas['closeness_max'] = metricas['closeness_min'] = 0.0
        metricas['closeness_desvio'] = metricas['closeness_mediana'] = 0.0
    
    try:
        betweenness = nx.betweenness_centrality(G, k=min(100, G.number_of_nodes()))
        metricas['betweenness_medio'] = np.mean(list(betweenness.values()))
        metricas['betweenness_max'] = max(betweenness.values())
        metricas['betweenness_min'] = min(betweenness.values())
        metricas['betweenness_desvio'] = np.std(list(betweenness.values()))
        metricas['betweenness_mediana'] = np.median(list(betweenness.values()))
    except:
        metricas['betweenness_medio'] = metricas['betweenness_max'] = metricas['betweenness_min'] = 0.0
        metricas['betweenness_desvio'] = metricas['betweenness_mediana'] = 0.0
    
    # ===== MÉTRICAS DE DISTÂNCIA =====
    try:
        if G.is_connected() or (G.is_directed() and nx.is_strongly_connected(G)):
            metricas['diametro'] = nx.diameter(G)
            metricas['raio'] = nx.radius(G)
            metricas['distancia_media'] = nx.average_shortest_path_length(G)
        else:
            metricas['diametro'] = metricas['raio'] = metricas['distancia_media'] = float('inf')
    except:
        metricas['diametro'] = metricas['raio'] = metricas['distancia_media'] = float('inf')
    
    # ===== MÉTRICAS DE COMUNIDADES =====
    try:
        communities_greedy = nx.community.greedy_modularity_communities(G.to_undirected())
        metricas['num_comunidades_greedy'] = len(communities_greedy)
        metricas['modularidade_greedy'] = nx.community.modularity(G.to_undirected(), communities_greedy)
    except:
        metricas['num_comunidades_greedy'] = 1
        metricas['modularidade_greedy'] = 0.0
    
    try:
        communities_label = nx.community.label_propagation_communities(G.to_undirected())
        metricas['num_comunidades_label'] = len(communities_label)
        metricas['modularidade_label'] = nx.community.modularity(G.to_undirected(), communities_label)
    except:
        metricas['num_comunidades_label'] = 1
        metricas['modularidade_label'] = 0.0
    
    # ===== MÉTRICAS ESPECÍFICAS DO POWER-LAW =====
    if graus is not None:
        # Calcula qualidade do power-law
        R, p_value, alpha, xmin = calcula_qualidade_powerlaw(graus)
        metricas['qualidade_powerlaw_R'] = R
        metricas['qualidade_powerlaw_p_value'] = p_value
        metricas['powerlaw_alpha'] = alpha
        metricas['powerlaw_xmin'] = xmin
        

        
        # Razão vértices/arestas
        metricas['razao_vertices_arestas'] = metricas['num_vertices'] / metricas['num_arestas'] if metricas['num_arestas'] > 0 else 0
    else:
        metricas['qualidade_powerlaw_R'] = 0.0
        metricas['qualidade_powerlaw_p_value'] = 1.0
        metricas['powerlaw_alpha'] = 0.0
        metricas['powerlaw_xmin'] = 0.0

        metricas['razao_vertices_arestas'] = 0.0
    
    return metricas

def executa_teste_powerlaw_completo(tipo, numV, gamma, seed):
    """Executa teste do gerador power-law com todas as métricas."""
    try:
        
        # Gera o grafo (desequilibrado e grau_min são intrínsecos ao gerador)
        dirigido = tipo in [1, 21, 31]
        resultado = geraGrafoPwl(numV, gamma, dirigido, tipo, seed)
        
        if resultado is None:
            return None
        
        arestas, G, graus = resultado
        matriz = nx.to_numpy_array(G)
        tipo_detectado = tipo
        
        # Calcula métricas completas
        metricas = calcula_metricas_completas(matriz, tipo_detectado, graus)
        
        # Adiciona métricas básicas
        metricas.update({
            'taxa_sucesso': 1.0,
            'limite_atingido': False
        })
        
        # Adiciona parâmetros do teste
        metricas.update({
            'gerador': 'Power-Law',
            'tipo': tipo,
            'numV': numV,
            'gamma': gamma,
            'seed': seed
        })
        
        return metricas
        
    except MemoryError:
        return {
            'gerador': 'Power-Law',
            'tipo': tipo,
            'numV': numV,
            'gamma': gamma,
            'seed': seed,
            'taxa_sucesso': 0.0,
            'limite_atingido': True,
            'erro': 'MemoryError'
        }
    except Exception as e:
        return {
            'gerador': 'Power-Law',
            'tipo': tipo,
            'numV': numV,
            'gamma': gamma,
            'seed': seed,

            'taxa_sucesso': 0.0,
            'limite_atingido': True,
            'erro': str(e)
        }

def main():
    """Função principal do experimento."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Experimento Power-Law Completo - Todas as métricas')
    parser.add_argument('--output_dir', default='./resultados_experimentos/exp_powerlaw_completo',
                       help='Diretório de saída')
    parser.add_argument('--max_vertices', type=int, default=10000,
                       help='Máximo de vértices para teste (padrão: 10000)')
    parser.add_argument('--seeds', nargs='+', type=int, default=[1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000],
                       help='Lista de seeds para teste')
    parser.add_argument('--teste_rapido', action='store_true',
                       help='Executa versão reduzida para teste rápido')
    
    args = parser.parse_args()
    
    # Configurações do experimento
    TIPOS_GRAFOS = [0, 1, 20, 21, 30, 31]  # Todos os tipos
    
    if args.teste_rapido:
        TAMANHOS = [100, 1000]
        CATEGORIAS_GAMMA = ['denso', 'moderado']
        SEEDS = [1000, 2000]
    else:
        TAMANHOS = [100, 1000, 10000]
        if args.max_vertices >= 100000:
            TAMANHOS.append(100000)
        if args.max_vertices >= 1000000:
            TAMANHOS.append(1000000)
        CATEGORIAS_GAMMA = ['denso', 'moderado', 'esparso']
        SEEDS = args.seeds
    
    # Cria diretório de saída
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("=" * 80)
    print("EXPERIMENTO POWER-LAW COMPLETO - TODAS AS MÉTRICAS")
    print("=" * 80)
    print(f"Tipos de grafo: {len(TIPOS_GRAFOS)} tipos")
    print(f"Tamanhos: {TAMANHOS}")
    print(f"Categorias gamma: {CATEGORIAS_GAMMA}")
    print(f"Seeds: {SEEDS}")
    
    # Calcula total de combinações
    total_combinacoes = (len(TIPOS_GRAFOS) * len(TAMANHOS) * len(CATEGORIAS_GAMMA) * len(SEEDS))
    print(f"Total de combinações: {total_combinacoes}")
    print(f"Diretório de saída: {args.output_dir}")
    print("=" * 80)
    
    resultados = []
    teste_atual = 0
    

    
    for tipo in TIPOS_GRAFOS:
        for numV in TAMANHOS:
            for categoria_gamma in CATEGORIAS_GAMMA:
                for seed in SEEDS:
                    teste_atual += 1
                    
                    # Gera gamma aleatório dentro da categoria
                    np.random.seed(seed)  # Para reprodutibilidade
                    gamma = gera_gamma_aleatorio(categoria_gamma)
                    
                    print(f"[{teste_atual:6d}/{total_combinacoes}] Tipo {tipo} - V={numV} - {categoria_gamma} (γ={gamma:.3f}) - Seed={seed}")
                    
                    resultado = executa_teste_powerlaw_completo(
                        tipo, numV, gamma, seed
                    )
                    
                    if resultado:
                        resultados.append(resultado)
                        if resultado['limite_atingido']:
                            print(f"  [LIMITE] {resultado.get('erro', 'Erro desconhecido')}")
                        else:
                            print(f"  [OK] R={resultado['qualidade_powerlaw_R']:.3f}")
                    else:
                        print(f"  [ERRO] Falha")
    

    
    # Salva resultados
    if resultados:
        df = pd.DataFrame(resultados)
        
        # Arquivo CSV principal
        csv_file = os.path.join(args.output_dir, 'resultados_powerlaw_completo.csv')
        df.to_csv(csv_file, index=False)
        
        # Arquivo de resumo
        resumo_file = os.path.join(args.output_dir, 'resumo_powerlaw_completo.csv')
        
        # Cria resumo agrupado por tipo
        resumo_por_tipo = df.groupby('tipo').agg({

            'densidade': 'mean',
            'grau_medio': 'mean',
            'grau_max': 'mean',
            'grau_min': 'mean',
            'grau_desvio': 'mean',
            'grau_mediana': 'mean',
            'num_componentes': 'mean',
            'conectividade': 'mean',
            'pagerank_medio': 'mean',
            'pagerank_max': 'mean',
            'pagerank_min': 'mean',
            'pagerank_desvio': 'mean',
            'pagerank_mediana': 'mean',
            'closeness_medio': 'mean',
            'closeness_max': 'mean',
            'closeness_min': 'mean',
            'closeness_desvio': 'mean',
            'closeness_mediana': 'mean',
            'betweenness_medio': 'mean',
            'betweenness_max': 'mean',
            'betweenness_min': 'mean',
            'betweenness_desvio': 'mean',
            'betweenness_mediana': 'mean',
            'diametro': 'mean',
            'raio': 'mean',
            'distancia_media': 'mean',
            'num_comunidades_greedy': 'mean',
            'modularidade_greedy': 'mean',
            'num_comunidades_label': 'mean',
            'modularidade_label': 'mean',
            'razao_vertices_arestas': 'mean',
            'taxa_sucesso': 'mean',
            'qualidade_powerlaw_R': 'mean',
            'powerlaw_alpha': 'mean',
            'limite_atingido': 'sum'
        }).reset_index()
        
        resumo_por_tipo.to_csv(resumo_file, index=False)
        
        print("\n" + "=" * 80)
        print("[OK] EXPERIMENTO POWER-LAW COMPLETO CONCLUIDO!")
        print(f"[RESULTADOS] Salvos em: {csv_file}")
        print(f"[RESUMO] Salvo em: {resumo_file}")

        print(f"[SUCESSO] Taxa: {len(resultados)/total_combinacoes*100:.1f}%")
        print("=" * 80)
    else:
        print("[ERRO] Nenhum resultado valido foi gerado!")

if __name__ == "__main__":
    main()
