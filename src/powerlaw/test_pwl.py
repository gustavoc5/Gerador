import csv
import time
import random
import numpy as np
import networkx as nx
import powerlaw as plw
from networkx.algorithms import community as nx_comm

from pwl import geraGrafoPwl, tipoGrafo


def calcula_metricas(G, graus, gamma, tipo, tipo_nome, seed, numV, tempo_geracao):
    dirigido = G.is_directed()

    # Fit Power Law
    g_filtrados = [g for g in graus if g >= 1]
    fit = plw.Fit(g_filtrados, xmin=2, discrete=True)
    ks_stat = fit.power_law.KS()
    alpha = fit.power_law.alpha

    G_und = G.to_undirected() if dirigido else G

    # Comunidades via Label Propagation
    try:
        lp_coms = list(nx_comm.label_propagation_communities(G_und))
        n_lp = len(lp_coms)
    except:
        n_lp = -1

    # Centralidades
    deg_cent = nx.degree_centrality(G_und)
    pr_cent = nx.pagerank(G, alpha=0.85)

    avg_deg = np.mean(list(deg_cent.values()))
    max_deg = np.max(list(deg_cent.values()))
    avg_pr = np.mean(list(pr_cent.values()))
    max_pr = np.max(list(pr_cent.values()))

    # Hop plot (amostragem aleatória)
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

    tipo_detectado = tipoGrafo(G)
    tipo_ok = (tipo_detectado == tipo)

    return {
        'tipo': tipo,
        'descricao': tipo_nome,
        'seed': seed,
        'gamma': round(gamma, 4),
        'powerlaw_ok': ks_stat < 0.1,
        'num_vertices': numV,
        'num_arestas': G.number_of_edges(),
        'grau_medio': round(2 * G.number_of_edges() / G.number_of_nodes(), 4),
        'grau_max': round(max(graus), 4),
        'ks_stat': round(ks_stat, 4),
        'alpha_powerlaw': round(alpha, 4),
        'n_communities_lp': n_lp,
        'avg_degree_centrality': round(avg_deg, 4),
        'max_degree_centrality': round(max_deg, 4),
        'avg_pagerank': round(avg_pr, 4),
        'max_pagerank': round(max_pr, 4),
        'media_hop': round(media_hop, 4) if media_hop != -1 else -1,
        'diametro_hop': round(diametro_hop, 4) if diametro_hop != -1 else -1,
        'tipo_detectado': tipo_detectado,
        'tipo_correto': tipo_ok,
        'tempo_geracao_s': round(tempo_geracao, 4)
    }


def executa_testes_pwl(n_execucoes=3, vertices_lista=[1000, 5000]):
    tipos = {
        0: 'Simples',
        1: 'Digrafo',
        20: 'Multigrafo',
        21: 'Multigrafo-Dirigido',
        30: 'Pseudografo',
        31: 'Pseudografo-Dirigido'
    }

    resultados = []

    for numV in vertices_lista:
        for tipo in tipos:
            for _ in range(n_execucoes):
                gamma = round(random.uniform(2.0, 3.0), 2)
                seed = random.randint(0, 10000)
                dirigido = tipo in [1, 21, 31]
                desequilibrado = dirigido  # ativa desequilíbrio apenas se for dirigido

                print(f"🔄 V={numV}, Tipo={tipo} ({tipos[tipo]}), Seed={seed}, γ={gamma}")
                start_time = time.time()
                arestas, G, graus = geraGrafoPwl(
                    numV, gamma, dirigido, tipo, seed, desequilibrado=desequilibrado
                )
                tempo_geracao = time.time() - start_time

                dados = calcula_metricas(G, graus, gamma, tipo, tipos[tipo], seed, numV, tempo_geracao)
                resultados.append(dados)

    return resultados


def salva_resultados_csv(resultados, arquivo='resultados_powerlaw.csv'):
    if not resultados:
        return
    chaves = list(resultados[0].keys())
    with open(arquivo, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=chaves)
        writer.writeheader()
        writer.writerows(resultados)


# Executar testes
resultados = executa_testes_pwl(n_execucoes=5, vertices_lista=[10000, 50000])
salva_resultados_csv(resultados)
