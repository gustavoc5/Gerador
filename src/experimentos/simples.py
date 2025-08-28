#!/usr/bin/env python3
"""
EXPERIMENTO SIMPLES COMPLETO
Experimento unificado para o gerador Simples com todas as métricas possíveis.

FATORES:
- Tipo de Grafo: 0, 1, 20, 21, 30, 31 (6 tipos)
- Tamanho (numV): 100, 1000, 10000, 100000, 1000000
- Estratégia de Arestas: Proporcional, Aleatório
- Preferência de Densidade: 0 (Sem preferência), 1 (Esparso), 2 (Denso)
- Número de Componentes: 0, 1, 2, 5, 10
- Fator de Balanceamento: 0, 1, 2
- Seed: 1000, 2000, 3000, 4000, 5000
- Grafos: Sempre 10 grafos por configuração (valor fixo)

MÉTRICAS COLETADAS:
- Todas as métricas básicas, de centralidade, distância, comunidades
- Métricas de performance e memória
- Métricas específicas do gerador simples
- Médias de todas as métricas dos 10 grafos gerados
- Equivalência estrutural entre replicações
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
from simples.constants import TIPOS_GRAFOS, TIPOS_VALIDOS, DENSIDADE_ESPARSA_MAX, DENSIDADE_DENSA_MIN



def calcula_metricas_completas(matriz, tipo_grafo):
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
        graus = [d for n, d in G.degree()]
        metricas['grau_medio'] = np.mean(graus)
        metricas['grau_max'] = max(graus)
        metricas['grau_min'] = min(graus)
        metricas['grau_desvio'] = np.std(graus)
        metricas['grau_mediana'] = np.median(graus)
    else:
        metricas['grau_medio'] = metricas['grau_max'] = metricas['grau_min'] = 0
        metricas['grau_desvio'] = metricas['grau_mediana'] = 0
    
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
    
    # ===== MÉTRICAS ESPECÍFICAS DO SIMPLES =====
    # Razão vértices/arestas
    metricas['razao_vertices_arestas'] = metricas['num_vertices'] / metricas['num_arestas'] if metricas['num_arestas'] > 0 else 0
    
    return metricas

def executa_teste_simples_completo(tipo, numV, numA, seed, estrategia_arestas, preferencia_densidade, numC):
    """Executa teste completo do gerador simples com 50 grafos."""
    try:
        
        # Gera 50 grafos com os mesmos parâmetros
        NUM_GRAFOS_PADRAO = 50
        datasets = geraDataset(tipo, numV, numA, seed, n=NUM_GRAFOS_PADRAO, numC=numC, fator=0)
        
        if not datasets or len(datasets) == 0:
            return None
        
        # Analisa todos os grafos gerados
        todas_metricas = []
        grafos_networkx = []  # Lista para análise de equivalência estrutural
        
        for i, arestas in enumerate(datasets):
            matriz = criaMatrizAdjacencias(arestas, numV, tipo)
            tipo_detectado = tipoGrafo(matriz)
            metricas_grafo = calcula_metricas_completas(matriz, tipo_detectado)
            todas_metricas.append(metricas_grafo)
            
            # Converte para NetworkX para análise de equivalência estrutural
            import networkx as nx
            if tipo in [1, 21, 31]:  # Dirigidos
                G_nx = nx.DiGraph()
            else:
                G_nx = nx.Graph()
            
            for j in range(len(matriz)):
                G_nx.add_node(j)
                for k in range(len(matriz[j])):
                    if matriz[j][k] > 0:
                        G_nx.add_edge(j, k)
            
            grafos_networkx.append(G_nx)
        
        # Calcula médias de todas as métricas
        metricas_medias = {}
        for chave in todas_metricas[0].keys():
            if chave in ['num_vertices', 'tipo_detectado']:  # Valores fixos
                metricas_medias[chave] = todas_metricas[0][chave]
            else:  # Valores que devem ser calculados como média
                valores = [m[chave] for m in todas_metricas if m[chave] is not None and not np.isnan(m[chave])]
                if valores:
                    metricas_medias[chave] = np.mean(valores)
                else:
                    metricas_medias[chave] = 0.0
        

        
        # Analisa equivalência estrutural entre replicações
        try:
            from similaridade import analisar_equivalencia_replicacoes, detectar_outliers_estruturais
            
            metricas_equivalencia = analisar_equivalencia_replicacoes(grafos_networkx)
            outliers, metricas_outliers = detectar_outliers_estruturais(grafos_networkx)
            
            # Adiciona métricas de equivalência estrutural
            metricas_medias.update(metricas_equivalencia)
            metricas_medias.update(metricas_outliers)
            metricas_medias['n_outliers_estruturais'] = len(outliers)
            metricas_medias['indices_outliers'] = str(outliers) if outliers else "[]"
        except Exception as e:
            # Se não conseguir calcular equivalência estrutural, usa valores padrão
            metricas_medias.update({
                'similaridade_media': 0.0,
                'consistencia_estrutural': 0.0,
                'n_outliers_estruturais': 0,
                'indices_outliers': "[]"
            })
        
        # Adiciona métricas básicas
        metricas_medias.update({
            'taxa_sucesso': len(datasets) / NUM_GRAFOS_PADRAO,
            'limite_atingido': False
        })
        
        # Adiciona parâmetros do teste
        metricas_medias.update({
            'gerador': 'Simples',
            'tipo': tipo,
            'numV': numV,
            'numA': numA,
            'seed': seed,
            'estrategia_arestas': estrategia_arestas,
            'preferencia_densidade': preferencia_densidade,
            'numC': numC,
            'num_grafos_gerados': NUM_GRAFOS_PADRAO
        })
        
        return metricas_medias
        
    except MemoryError:
        return {
            'gerador': 'Simples',
            'tipo': tipo,
            'numV': numV,
            'numA': numA,
            'seed': seed,
            'estrategia_arestas': estrategia_arestas,
            'preferencia_densidade': preferencia_densidade,
            'numC': numC,
            'num_grafos_gerados': 50,
            'taxa_sucesso': 0.0,
            'limite_atingido': True,
            'erro': 'MemoryError'
        }
    except Exception as e:
        return {
            'gerador': 'Simples',
            'tipo': tipo,
            'numV': numV,
            'numA': numA,
            'seed': seed,
            'estrategia_arestas': estrategia_arestas,
            'preferencia_densidade': preferencia_densidade,
            'numC': numC,
            'num_grafos_gerados': 50,
            'taxa_sucesso': 0.0,
            'limite_atingido': True,
            'erro': str(e)
        }

def main():
    """Função principal do experimento."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Experimento Simples Completo - Todas as métricas')
    parser.add_argument('--output_dir', default='./resultados_experimentos/exp_simples_completo',
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
        PREFERENCIAS_DENSIDADE = [0, 1, 2]  # Sem preferência, Esparso, Denso
        NUM_COMPONENTES = [0, 1]  # Aleatório, Conexo
        SEEDS = [1000, 2000]
    else:
        TAMANHOS = [100, 1000, 10000]
        if args.max_vertices >= 100000:
            TAMANHOS.append(100000)
        if args.max_vertices >= 1000000:
            TAMANHOS.append(1000000)
        PREFERENCIAS_DENSIDADE = [0, 1, 2]  # Sem preferência, Esparso, Denso
        NUM_COMPONENTES = [0, 1]  # Aleatório, Conexo
        SEEDS = args.seeds
    
    # Cria diretório de saída
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("=" * 80)
    print("EXPERIMENTO SIMPLES COMPLETO - TODAS AS MÉTRICAS")
    print("=" * 80)
    print(f"Tipos de grafo: {len(TIPOS_GRAFOS)} tipos")
    print(f"Tamanhos: {TAMANHOS}")
    print(f"Preferências de densidade: {PREFERENCIAS_DENSIDADE} (0=Sem preferência, 1=Esparso, 2=Denso)")
    print(f"Número de componentes: {NUM_COMPONENTES} (0=Aleatório, 1=Conexo)")
    print(f"Grafos por teste: 50 (valor fixo)")
    print(f"Seeds: {SEEDS}")
    
    # Calcula total de combinações
    total_combinacoes = (len(TIPOS_GRAFOS) * len(TAMANHOS) * 
                        len(PREFERENCIAS_DENSIDADE) * len(NUM_COMPONENTES) * 
                        len(SEEDS))
    print(f"Total de combinações: {total_combinacoes}")
    print(f"Total de grafos gerados: {total_combinacoes * 50}")
    print(f"Diretório de saída: {args.output_dir}")
    print("=" * 80)
    
    resultados = []
    teste_atual = 0
    

    
    for tipo in TIPOS_GRAFOS:
        for numV in TAMANHOS:
            for pref_dens in PREFERENCIAS_DENSIDADE:
                for numC in NUM_COMPONENTES:
                    for seed in SEEDS:
                        teste_atual += 1
                        
                        # Calcula número de arestas baseado na preferência de densidade
                        max_arestas = numV * (numV - 1) // 2
                        min_arestas = max(1, numV-1)
                        
                        if pref_dens == 0:  # Sem preferência
                            numA = random.randint(min_arestas, max_arestas)
                        elif pref_dens == 1:  # Esparso (d ≤ 0.2)
                            numA = random.randint(min_arestas, int(max_arestas * DENSIDADE_ESPARSA_MAX))
                        else:  # Denso (d ≥ 0.8)
                            numA = random.randint(int(max_arestas * DENSIDADE_DENSA_MIN), max_arestas)
                        
                        # Mapeia preferência para texto
                        pref_texto = {0: "Sem preferência", 1: "Esparso", 2: "Denso"}[pref_dens]
                        comp_texto = {0: "Aleatório", 1: "Conexo"}[numC]
                        
                        print(f"[{teste_atual:6d}/{total_combinacoes}] Tipo {tipo} - V={numV} - {pref_texto} - {comp_texto} - Seed={seed}")
                        
                        resultado = executa_teste_simples_completo(
                            tipo, numV, numA, seed, "Proporcional", pref_dens, 
                            numC
                        )
                        
                        if resultado:
                            resultados.append(resultado)
                            if resultado['limite_atingido']:
                                print(f"  [LIMITE] {resultado.get('erro', 'Erro desconhecido')}")
                            else:
                                print(f"  [OK] Sucesso: {resultado['taxa_sucesso']:.1%} - Consistência: {resultado.get('consistencia_estrutural', 0):.3f}")
                        else:
                            print(f"  [ERRO] Falha")
    

    
    # Salva resultados
    if resultados:
        df = pd.DataFrame(resultados)
        
        # Arquivo CSV principal
        csv_file = os.path.join(args.output_dir, 'resultados_simples_completo.csv')
        df.to_csv(csv_file, index=False)
        
        # Arquivo de resumo
        resumo_file = os.path.join(args.output_dir, 'resumo_simples_completo.csv')
        
        # Cria resumo agrupado por tipo
        resumo_por_tipo = df.groupby('tipo').agg({
            'tempo_geracao': 'mean',
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
            'consistencia_estrutural': 'mean',
            'similaridade_media': 'mean',
            'n_outliers_estruturais': 'mean',
            'limite_atingido': 'sum'
        }).reset_index()
        
        resumo_por_tipo.to_csv(resumo_file, index=False)
        
        print("\n" + "=" * 80)
        print("[OK] EXPERIMENTO SIMPLES COMPLETO CONCLUIDO!")
        print(f"[RESULTADOS] Salvos em: {csv_file}")
        print(f"[RESUMO] Salvo em: {resumo_file}")
        print(f"[SUCESSO] Taxa: {len(resultados)/total_combinacoes*100:.1f}%")
        print(f"[GRAFOS] Total gerados: {len(resultados) * 50}")
        print(f"[CONSISTÊNCIA] Média: {df['consistencia_estrutural'].mean():.3f}")
        print("=" * 80)
    else:
        print("[ERRO] Nenhum resultado valido foi gerado!")

if __name__ == "__main__":
    main()
