#!/usr/bin/env python3
"""
EXPERIMENTO 1: COMPARAÇÃO FUNDAMENTAL ENTRE GERADORES
Compara diretamente o comportamento dos geradores Simples e Power-Law em diferentes escalas.

FATORES:
- Gerador: Simples, Power-Law
- Tipo de Grafo: Simples (0), Digrafo (1), Multigrafo (20), Multigrafo-Dirigido (21), Pseudografo (30), Pseudografo-Dirigido (31)
- Tamanho (numV): 100, 1000, 10000, 100000, 1000000
- Seed: 1000, 2000, 3000, 4000, 5000

VARIÁVEIS DE RESPOSTA:
Tempo de geração, Número de arestas, Densidade, Grau médio, Grau máximo, Grau mínimo, 
Número de componentes, Modularidade, Diâmetro, Raio, Distância média, Taxa de sucesso.
"""

import os
import sys
import random
import time
import pandas as pd
import numpy as np
from datetime import datetime

# Adiciona o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from simples.gerador import geraDataset
from simples.utils import criaMatrizAdjacencias, tipoGrafo
from powerlaw.pwl import geraGrafoPwl
from simples.constants import TIPOS_GRAFOS, TIPOS_VALIDOS
from powerlaw.constants import GAMMA_MIN, GAMMA_MAX

def calcula_metricas_basicas(matriz, tipo_grafo):
    """Calcula métricas básicas do grafo."""
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
    
    # Informações básicas
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
    
    # Grau médio
    if G.number_of_nodes() > 0:
        graus = [d for n, d in G.degree()]
        metricas['grau_medio'] = np.mean(graus)
        metricas['grau_max'] = max(graus)
        metricas['grau_min'] = min(graus)
    else:
        metricas['grau_medio'] = metricas['grau_max'] = metricas['grau_min'] = 0
    
    # Componentes conexas
    if G.is_directed():
        metricas['num_componentes'] = nx.number_strongly_connected_components(G)
    else:
        metricas['num_componentes'] = nx.number_connected_components(G)
    
    # Métricas de centralidade (simplificadas)
    try:
        pagerank = nx.pagerank(G, max_iter=100)
        metricas['pagerank_medio'] = np.mean(list(pagerank.values()))
        metricas['pagerank_max'] = max(pagerank.values())
    except:
        metricas['pagerank_medio'] = metricas['pagerank_max'] = 0.0
    
    try:
        closeness = nx.closeness_centrality(G)
        metricas['closeness_medio'] = np.mean(list(closeness.values()))
        metricas['closeness_max'] = max(closeness.values())
    except:
        metricas['closeness_medio'] = metricas['closeness_max'] = 0.0
    
    try:
        betweenness = nx.betweenness_centrality(G, k=min(100, G.number_of_nodes()))
        metricas['betweenness_medio'] = np.mean(list(betweenness.values()))
        metricas['betweenness_max'] = max(betweenness.values())
    except:
        metricas['betweenness_medio'] = metricas['betweenness_max'] = 0.0
    
    # Métricas de distância
    try:
        if G.is_connected() or (G.is_directed() and nx.is_strongly_connected(G)):
            metricas['diametro'] = nx.diameter(G)
            metricas['raio'] = nx.radius(G)
            metricas['distancia_media'] = nx.average_shortest_path_length(G)
        else:
            metricas['diametro'] = metricas['raio'] = metricas['distancia_media'] = float('inf')
    except:
        metricas['diametro'] = metricas['raio'] = metricas['distancia_media'] = float('inf')
    
    # Métricas de comunidades
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
    
    return metricas

def executa_teste_simples(tipo, numV, numA, seed):
    """Executa teste do gerador simples."""
    try:
        start_time = time.time()
        
        # Gera o grafo
        datasets = geraDataset(tipo, numV, numA, seed, n=1, numC=0, fator=1.0)
        
        if not datasets:
            return None
        
        arestas = datasets[0]
        matriz = criaMatrizAdjacencias(arestas, numV, tipo)
        tipo_detectado = tipoGrafo(matriz)
        metricas = calcula_metricas_basicas(matriz, tipo_detectado)
        
        tempo_geracao = time.time() - start_time
        
        return {
            'gerador': 'Simples',
            'tipo': tipo,
            'numV': numV,
            'numA': numA,
            'seed': seed,
            'tipo_detectado': tipo_detectado,
            'tempo_geracao': tempo_geracao,
            'taxa_sucesso': 1.0,
            **metricas
        }
        
    except Exception as e:
        print(f"ERRO Simples: {e}")
        return None

def executa_teste_powerlaw(tipo, numV, gamma, seed):
    """Executa teste do gerador power-law."""
    try:
        start_time = time.time()
        
        # Gera o grafo
        dirigido = tipo in [1, 21, 31]
        resultado = geraGrafoPwl(numV, gamma, dirigido, tipo, seed, desequilibrado=False)
        
        if resultado is None:
            return None
        
        arestas, G, graus = resultado
        matriz = nx.to_numpy_array(G)
        tipo_detectado = tipo
        metricas = calcula_metricas_basicas(matriz, tipo_detectado)
        
        tempo_geracao = time.time() - start_time
        
        return {
            'gerador': 'Power-Law',
            'tipo': tipo,
            'numV': numV,
            'gamma': gamma,
            'seed': seed,
            'tipo_detectado': tipo_detectado,
            'tempo_geracao': tempo_geracao,
            'taxa_sucesso': 1.0,
            **metricas
        }
        
    except Exception as e:
        print(f"ERRO Power-Law: {e}")
        return None

def main():
    """Função principal do experimento."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Experimento 1: Comparação Fundamental entre Geradores')
    parser.add_argument('--output_dir', default='./resultados_experimentos/exp1_comparacao_geradores',
                       help='Diretório de saída')
    parser.add_argument('--max_vertices', type=int, default=10000,
                       help='Máximo de vértices para teste (padrão: 10000)')
    parser.add_argument('--seeds', nargs='+', type=int, default=[1000, 2000, 3000, 4000, 5000],
                       help='Lista de seeds para teste')
    
    args = parser.parse_args()
    
    # Configurações do experimento
    GERADORES = ['Simples', 'Power-Law']
    TIPOS_GRAFOS = [0, 1, 20, 21, 30, 31]  # Todos os tipos
    TAMANHOS = [100, 1000, 10000]
    if args.max_vertices >= 100000:
        TAMANHOS.append(100000)
    if args.max_vertices >= 1000000:
        TAMANHOS.append(1000000)
    
    SEEDS = args.seeds
    
    # Cria diretório de saída
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("=" * 80)
    print("EXPERIMENTO 1: COMPARAÇÃO FUNDAMENTAL ENTRE GERADORES")
    print("=" * 80)
    print(f"Geradores: {GERADORES}")
    print(f"Tipos de grafo: {len(TIPOS_GRAFOS)} tipos")
    print(f"Tamanhos: {TAMANHOS}")
    print(f"Seeds: {SEEDS}")
    print(f"Total de combinações: {len(GERADORES)} × {len(TIPOS_GRAFOS)} × {len(TAMANHOS)} × {len(SEEDS)} = {len(GERADORES) * len(TIPOS_GRAFOS) * len(TAMANHOS) * len(SEEDS)}")
    print(f"Diretório de saída: {args.output_dir}")
    print("=" * 80)
    
    resultados = []
    total_testes = len(GERADORES) * len(TIPOS_GRAFOS) * len(TAMANHOS) * len(SEEDS)
    teste_atual = 0
    
    start_time_experimento = time.time()
    
    for gerador in GERADORES:
        for tipo in TIPOS_GRAFOS:
            for numV in TAMANHOS:
                for seed in SEEDS:
                    teste_atual += 1
                    
                    print(f"[{teste_atual:4d}/{total_testes}] {gerador} - Tipo {tipo} - V={numV} - Seed={seed}")
                    
                    if gerador == 'Simples':
                        # Calcula número de arestas para simples
                        max_arestas = numV * (numV - 1) // 2
                        numA = random.randint(max(1, numV-1), max_arestas)
                        resultado = executa_teste_simples(tipo, numV, numA, seed)
                    else:  # Power-Law
                        # Gamma fixo para comparação
                        gamma = 2.5
                        resultado = executa_teste_powerlaw(tipo, numV, gamma, seed)
                    
                    if resultado:
                        resultados.append(resultado)
                        print(f"  ✅ Sucesso - Tempo: {resultado['tempo_geracao']:.3f}s")
                    else:
                        print(f"  ❌ Falha")
    
    end_time_experimento = time.time()
    tempo_total = end_time_experimento - start_time_experimento
    
    # Salva resultados
    if resultados:
        df = pd.DataFrame(resultados)
        
        # Arquivo CSV principal
        csv_file = os.path.join(args.output_dir, 'resultados_experimento1.csv')
        df.to_csv(csv_file, index=False)
        
        # Arquivo de resumo
        resumo_file = os.path.join(args.output_dir, 'resumo_experimento1.txt')
        with open(resumo_file, 'w', encoding='utf-8') as f:
            f.write("EXPERIMENTO 1: COMPARAÇÃO FUNDAMENTAL ENTRE GERADORES\n")
            f.write("=" * 60 + "\n")
            f.write(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total de testes: {len(resultados)}/{total_testes}\n")
            f.write(f"Taxa de sucesso: {len(resultados)/total_testes*100:.1f}%\n")
            f.write(f"Tempo total: {tempo_total:.2f} segundos\n")
            f.write(f"Tempo médio por teste: {tempo_total/len(resultados):.3f} segundos\n\n")
            
            # Estatísticas por gerador
            for gerador in GERADORES:
                df_gerador = df[df['gerador'] == gerador]
                f.write(f"GERADOR: {gerador}\n")
                f.write(f"  Testes: {len(df_gerador)}\n")
                f.write(f"  Tempo médio: {df_gerador['tempo_geracao'].mean():.3f}s\n")
                f.write(f"  Densidade média: {df_gerador['densidade'].mean():.4f}\n")
                f.write(f"  Grau médio: {df_gerador['grau_medio'].mean():.2f}\n\n")
        
        print("\n" + "=" * 80)
        print("✅ EXPERIMENTO CONCLUÍDO!")
        print(f"📊 Resultados salvos em: {csv_file}")
        print(f"📋 Resumo salvo em: {resumo_file}")
        print(f"⏱️  Tempo total: {tempo_total:.2f} segundos")
        print(f"🎯 Taxa de sucesso: {len(resultados)/total_testes*100:.1f}%")
        print("=" * 80)
    else:
        print("❌ Nenhum resultado válido foi gerado!")

if __name__ == "__main__":
    main()
