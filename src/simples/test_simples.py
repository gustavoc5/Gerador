import csv
import time
import random
import math
import numpy as np
import networkx as nx
from networkx.algorithms import community as nx_comm

from gerador import geraDataset, verificaAresta
from utils import (
    criaMatrizAdjacencias,
    criaMatrizAdjacenciasValorada,
    tipoGrafo,
    compConexas,
)
from constants import (
    TIPOS_GRAFOS, GERACAO, TIPOS_DIRIGIDOS, 
    NUM_EXECUCOES_PADRAO, VERTICES_LISTA_PADRAO, MAX_AMOSTRAS_HOP
)
from exceptions import GrafoGenerationError


def matrizParaNetworkX(matriz, tipo):
    """Converte matriz para NetworkX de forma eficiente."""
    G = nx.DiGraph() if tipo in TIPOS_DIRIGIDOS else nx.Graph()
    edges = []
    
    for u in range(len(matriz)):
        for v in range(len(matriz)):
            cell = matriz[u][v]
            if isinstance(cell, list):
                edges.extend([(u, v)] * len(cell))
            elif cell > 0:
                edges.extend([(u, v)] * cell)
    
    G.add_edges_from(edges)
    return G


def calcula_metricas_basicas(G, dataset):
    """Calcula métricas básicas do grafo."""
    graus = [d for n, d in G.degree()]
    return {
        'grau_medio': np.mean(graus),
        'grau_max': max(graus),
        'num_arestas': len(dataset)
    }


def calcula_metricas_centralidade(G):
    """Calcula métricas de centralidade."""
    try:
        G_und = G.to_undirected() if G.is_directed() else G
    except:
        G_und = nx.Graph()
        G_und.add_edges_from(G.edges())
    
    deg_cent = nx.degree_centrality(G_und)
    pr_cent = nx.pagerank(G, alpha=0.85)
    
    return {
        'avg_degree_centrality': np.mean(list(deg_cent.values())),
        'max_degree_centrality': np.max(list(deg_cent.values())),
        'avg_pagerank': np.mean(list(pr_cent.values())),
        'max_pagerank': np.max(list(pr_cent.values()))
    }


def calcula_metricas_hop(G):
    """Calcula métricas de distância (hop plot)."""
    try:
        G_und = G.to_undirected() if G.is_directed() else G
    except:
        G_und = nx.Graph()
        G_und.add_edges_from(G.edges())
    
    try:
        nodes = list(G_und.nodes())
        distancias = []
        for _ in range(min(MAX_AMOSTRAS_HOP, len(nodes) ** 2)):
            u, v = random.sample(nodes, 2)
            try:
                d = nx.shortest_path_length(G_und, source=u, target=v)
                distancias.append(d)
            except nx.NetworkXNoPath:
                continue
        
        if distancias:
            media_hop = np.mean(distancias)
            diametro_hop = np.max(distancias)
        else:
            media_hop = diametro_hop = -1
    except:
        media_hop = diametro_hop = -1
    
    return {
        'media_hop': media_hop,
        'diametro_hop': diametro_hop
    }


def calcula_metricas_comunidades(G):
    """Calcula métricas de comunidades."""
    try:
        G_und = G.to_undirected() if G.is_directed() else G
    except:
        G_und = nx.Graph()
        G_und.add_edges_from(G.edges())
    
    try:
        lp_coms = list(nx_comm.label_propagation_communities(G_und))
        n_lp = len(lp_coms)
    except:
        n_lp = -1
    
    return {
        'n_communities_lp': n_lp
    }


def calcula_metricas_completas(G, dataset, matriz, tipo, numComp):
    """Calcula todas as métricas do grafo."""
    # Métricas básicas
    metricas_basicas = calcula_metricas_basicas(G, dataset)
    
    # Métricas de centralidade
    metricas_cent = calcula_metricas_centralidade(G)
    
    # Métricas de hop
    metricas_hop = calcula_metricas_hop(G)
    
    # Métricas de comunidades
    metricas_com = calcula_metricas_comunidades(G)
    
    # Validações
    tipo_detectado = tipoGrafo(matriz)
    correto = tipo_detectado == tipo
    comp = compConexas(matriz) if numComp > 1 else -1
    
    return {
        **metricas_basicas,
        **metricas_cent,
        **metricas_hop,
        **metricas_com,
        'tipo_detectado': tipo_detectado,
        'tipo_ok': correto,
        'num_componentes': comp
    }


def testa_simples(n_execucoes=NUM_EXECUCOES_PADRAO, vertices_lista=VERTICES_LISTA_PADRAO, arquivo_csv="resultados_simples.csv"):
    """Executa bateria de testes para diferentes tipos de grafos."""
    resultados = []

    for numV in vertices_lista:
        for tipo in TIPOS_GRAFOS:
            seed_base = random.randint(100, 9999)

            for execucao in range(n_execucoes):
                seed = seed_base + execucao
                numComp = random.choice([0, 1, 2])
                densPref = random.choice([0, 1, 2])

                try:
                    minA, maxA = verificaAresta(tipo, numV, numComp)
                except:
                    continue

                g_max = (
                    numV * (numV - 1) / 2 if tipo in [0, 20]
                    else numV * (numV - 1) if tipo in [1, 21]
                    else numV * (numV - 1) / 2 + numV if tipo == 30
                    else numV * (numV - 1) + numV
                )

                if densPref == 1:
                    lowA = max(minA, int(0.05 * g_max))
                    highA = max(minA, int(0.2 * g_max))
                elif densPref == 2:
                    lowA = max(minA, int(0.8 * g_max))
                    highA = min(int(g_max), int(maxA)) if not math.isinf(maxA) else int(g_max)
                else:
                    lowA = int(minA)
                    highA = int(maxA) if not math.isinf(maxA) else int(g_max)

                if highA < lowA:
                    continue

                numA = random.randint(lowA, highA)
                n = 1
                fator = random.choice([0, 1, 2]) if numComp > 1 else 0

                print(f"🔄 Tipo={tipo} Seed={seed} Geração={GERACAO[fator]} Arestas={numA} V={numV}")

                try:
                    start = time.time()
                    datasets = geraDataset(tipo, numV, numA, seed, n, numComp, fator)
                    tempo_geracao = time.time() - start

                    if not datasets:
                        continue

                    for dataset in datasets:
                        matriz = criaMatrizAdjacencias(dataset, numV, tipo)
                        G = matrizParaNetworkX(matriz, tipo)
                        
                        # Calcula todas as métricas
                        metricas = calcula_metricas_completas(G, dataset, matriz, tipo, numComp)
                        
                        # Adiciona informações básicas
                        resultado = {
                            "vertices": numV,
                            "tipo": tipo,
                            "descricao": TIPOS_GRAFOS[tipo],
                            "execucao": execucao + 1,
                            "seed": seed,
                            "num_componentes_esperado": numComp,
                            "densidade_preferida": densPref,
                            "tempo_geracao_s": round(tempo_geracao, 4),
                            **metricas
                        }
                        
                        # Arredonda valores numéricos
                        for key, value in resultado.items():
                            if isinstance(value, float) and key != 'tempo_geracao_s':
                                resultado[key] = round(value, 4)
                        
                        resultados.append(resultado)

                except GrafoGenerationError as e:
                    print(f"❌ Erro de geração: {e}")
                except Exception as e:
                    print(f"❌ Erro: {e}")

    if resultados:
        with open(arquivo_csv, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=resultados[0].keys())
            writer.writeheader()
            writer.writerows(resultados)
        print(f"\n✅ {len(resultados)} execuções finalizadas. Resultados salvos em: {arquivo_csv}")
    else:
        print("\n⚠️ Nenhum resultado válido foi gerado.")


if __name__ == "__main__":
    testa_simples(n_execucoes=3, vertices_lista=[100, 200])
