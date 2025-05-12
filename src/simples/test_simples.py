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

def testa_simples(n_execucoes=5, vertices_lista=[1000, 5000], arquivo_csv="resultados_simples.csv"):
    tipos = {
        0: "Simples",
        1: "Digrafo",
        20: "Multigrafo",
        21: "Multigrafo-Dirigido",
        30: "Pseudografo",
        31: "Pseudografo-Dirigido",
    }
    geracao = {0: "Aleatório", 1: "Parcial", 2: "Balanceado"}
    resultados = []

    for numV in vertices_lista:
        for tipo in tipos:
            seed_base = random.randint(100, 9999)

            for execucao in range(n_execucoes):
                seed = seed_base + execucao
                numComp = random.choice([0, 1, 2])
                densPref = random.choice([0, 1, 2])
                valorado = random.choice([True, False])

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

                print(f"🔄 Tipo={tipo} Seed={seed} Geração={geracao[fator]} Arestas={numA} V={numV}")

                try:
                    start = time.time()
                    datasets = geraDataset(tipo, numV, numA, seed, n, numComp, fator)
                    tempo_geracao = time.time() - start

                    if not datasets:
                        continue

                    for dataset in datasets:
                        if valorado:
                            matriz = criaMatrizAdjacenciasValorada(dataset, numV, tipo, 1, 10)
                        else:
                            matriz = criaMatrizAdjacencias(dataset, numV, tipo)

                        G = nx.DiGraph() if tipo in [1, 21, 31] else nx.Graph()
                        for u in range(len(matriz)):
                            for v in range(len(matriz)):
                                cell = matriz[u][v]
                                if isinstance(cell, list):
                                    for _ in cell:
                                        G.add_edge(u, v)
                                elif cell > 0:
                                    for _ in range(cell):
                                        G.add_edge(u, v)

                        graus = [d for n, d in G.degree()]
                        grau_medio = np.mean(graus)
                        grau_max = max(graus)

                        G_und = G.to_undirected() if G.is_directed() else G

                        try:
                            lp_coms = list(nx_comm.label_propagation_communities(G_und))
                            n_lp = len(lp_coms)
                        except:
                            n_lp = -1

                        deg_cent = nx.degree_centrality(G_und)
                        pr_cent = nx.pagerank(G, alpha=0.85)

                        avg_deg = np.mean(list(deg_cent.values()))
                        max_deg = np.max(list(deg_cent.values()))
                        avg_pr = np.mean(list(pr_cent.values()))
                        max_pr = np.max(list(pr_cent.values()))

                        try:
                            nodes = list(G_und.nodes())
                            distancias = []
                            for _ in range(min(10000, len(nodes) ** 2)):
                                u, v = random.sample(nodes, 2)
                                try:
                                    d = nx.shortest_path_length(G_und, source=u, target=v)
                                    distancias.append(d)
                                except nx.NetworkXNoPath:
                                    continue
                            media_hop = np.mean(distancias) if distancias else -1
                            diametro_hop = np.max(distancias) if distancias else -1
                        except:
                            media_hop = diametro_hop = -1

                        tipo_detectado = tipoGrafo(matriz)
                        correto = tipo_detectado == tipo
                        comp = compConexas(matriz) if numComp > 1 else -1

                        resultados.append({
                            "vertices": numV,
                            "tipo": tipo,
                            "descricao": tipos[tipo],
                            "execucao": execucao + 1,
                            "seed": seed,
                            "num_arestas": len(dataset),
                            "num_componentes": comp,
                            "num_componentes_esperado": numComp,
                            "valorado": valorado,
                            "densidade_preferida": densPref,
                            "tipo_detectado": tipo_detectado,
                            "tipo_ok": correto,
                            "grau_medio": round(grau_medio, 4),
                            "grau_max": round(grau_max, 4),
                            "n_communities_lp": n_lp,
                            "avg_degree_centrality": round(avg_deg, 4),
                            "max_degree_centrality": round(max_deg, 4),
                            "avg_pagerank": round(avg_pr, 4),
                            "max_pagerank": round(max_pr, 4),
                            "media_hop": round(media_hop, 4) if media_hop != -1 else -1,
                            "diametro_hop": round(diametro_hop, 4) if diametro_hop != -1 else -1,
                            "tempo_geracao_s": round(tempo_geracao, 4)
                        })

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
    testa_simples(n_execucoes=5, vertices_lista=[100, 500])
