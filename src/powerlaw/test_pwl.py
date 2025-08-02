import csv
import time
import random
import numpy as np
import networkx as nx
import powerlaw as plw
from networkx.algorithms import community as nx_comm
from collections import defaultdict
from pwl import geraGrafoPwl, tipoGrafo
from constants import (
    TIPOS_GRAFOS, TIPOS_DIRIGIDOS, GAMMA_MIN, GAMMA_MAX,
    XMIN_POWERLAW, KS_THRESHOLD, NUM_EXECUCOES_PADRAO, 
    VERTICES_LISTA_PADRAO, MAX_AMOSTRAS_HOP
)


def salva_resumo_csv(resultados, arquivo='resumo_powerlaw.csv'):
    if not resultados:
        return

    grupos = defaultdict(list)
    for r in resultados:
        chave = (r['descricao'], r['num_vertices'])
        grupos[chave].append(r)

    resumo = []
    for (descricao, num_vertices), grupo in grupos.items():
        media = {}
        media['descricao'] = descricao
        media['num_vertices'] = num_vertices

        # Campos numéricos exceto os de identificação
        campos_numericos = [
            k for k in grupo[0].keys()
            if isinstance(grupo[0][k], (int, float)) and k not in ['seed', 'num_vertices']
        ]

        for campo in campos_numericos:
            valores = [g[campo] for g in grupo]
            media[f"media_{campo}"] = round(np.mean(valores), 4)
            media[f"std_{campo}"] = round(np.std(valores), 4)

        # Cálculo da porcentagem de sucesso no teste de power law (KS)
        if 'powerlaw_ok' in grupo[0]:
            qtd_ok = sum(1 for g in grupo if g['powerlaw_ok'])
            media['pct_powerlaw_ok'] = round(100 * qtd_ok / len(grupo), 2)

        resumo.append(media)

    chaves = list(resumo[0].keys())
    with open(arquivo, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=chaves)
        writer.writeheader()
        writer.writerows(resumo)


def calcula_metricas_powerlaw(graus, gamma):
    """Calcula métricas específicas de power-law."""
    g_filtrados = [g for g in graus if g >= 1]
    fit = plw.Fit(g_filtrados, xmin=XMIN_POWERLAW, discrete=True)
    ks_stat = fit.power_law.KS()
    alpha = fit.power_law.alpha
    
    return {
        'powerlaw_ok': ks_stat < KS_THRESHOLD,
        'ks_stat': round(ks_stat, 4),
        'alpha_powerlaw': round(alpha, 4)
    }


def calcula_metricas_graus(graus, G):
    """Calcula métricas relacionadas aos graus dos nós."""
    grau_medio = 2 * G.number_of_edges() / G.number_of_nodes()
    
    return {
        'grau_min': round(min(graus), 4),
        'grau_medio': round(grau_medio, 4),
        'grau_max': round(max(graus), 4),
        'grau_std': round(np.std(graus), 4)
    }


def calcula_metricas_centralidade(G):
    """Calcula métricas de centralidade."""
    try:
        G_und = G.to_undirected() if G.is_directed() else G
    except:
        # Fallback para evitar erro de atributos dos nós
        G_und = nx.Graph()
        G_und.add_edges_from(G.edges())
    
    deg_cent_vals = list(nx.degree_centrality(G_und).values())
    pr_cent_vals = list(nx.pagerank(G, alpha=0.85).values())
    
    return {
        'min_degree_centrality': round(np.min(deg_cent_vals), 4),
        'avg_degree_centrality': round(np.mean(deg_cent_vals), 4),
        'max_degree_centrality': round(np.max(deg_cent_vals), 4),
        'std_degree_centrality': round(np.std(deg_cent_vals), 4),
        'min_pagerank': round(np.min(pr_cent_vals), 4),
        'avg_pagerank': round(np.mean(pr_cent_vals), 4),
        'max_pagerank': round(np.max(pr_cent_vals), 4),
        'std_pagerank': round(np.std(pr_cent_vals), 4)
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
            std_hop = np.std(distancias)
            diametro_hop = np.max(distancias)
        else:
            media_hop = std_hop = diametro_hop = -1
    except:
        media_hop = std_hop = diametro_hop = -1
    
    return {
        'media_hop': round(media_hop, 4) if media_hop != -1 else -1,
        'diametro_hop': round(diametro_hop, 4) if diametro_hop != -1 else -1,
        'std_hop': round(std_hop, 4) if std_hop != -1 else -1
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


def calcula_metricas(G, graus, gamma, tipo, tipo_nome, seed, numV, tempo_geracao):
    """Calcula todas as métricas do grafo."""
    # Métricas básicas
    metricas_basicas = {
        'descricao': tipo_nome,
        'seed': seed,
        'gamma': round(gamma, 4),
        'num_vertices': numV,
        'num_arestas': G.number_of_edges(),
        'tempo_geracao_s': round(tempo_geracao, 4)
    }
    
    # Métricas de power-law
    metricas_pwl = calcula_metricas_powerlaw(graus, gamma)
    
    # Métricas de graus
    metricas_graus = calcula_metricas_graus(graus, G)
    
    # Métricas de centralidade
    metricas_cent = calcula_metricas_centralidade(G)
    
    # Métricas de hop
    metricas_hop = calcula_metricas_hop(G)
    
    # Métricas de comunidades
    metricas_com = calcula_metricas_comunidades(G)
    
    # Combina todas as métricas
    return {**metricas_basicas, **metricas_pwl, **metricas_graus, 
            **metricas_cent, **metricas_hop, **metricas_com}


def executa_testes_pwl(n_execucoes=NUM_EXECUCOES_PADRAO, vertices_lista=VERTICES_LISTA_PADRAO):
    """Executa bateria de testes para diferentes tipos de grafos."""
    resultados = []

    for numV in vertices_lista:
        for tipo in TIPOS_GRAFOS:
            seed_inicial = random.randint(0, 10000)  # sorteia uma seed base
            for i in range(n_execucoes):
                seed = seed_inicial + i
                gamma = round(random.uniform(GAMMA_MIN, GAMMA_MAX), 2)
                dirigido = tipo in TIPOS_DIRIGIDOS
                desequilibrado = dirigido

                print(f"🔄 V={numV}, ({TIPOS_GRAFOS[tipo]}), Seed={seed}, γ={gamma}")
                start_time = time.time()
                arestas, G, graus = geraGrafoPwl(
                    numV, gamma, dirigido, tipo, seed, desequilibrado=desequilibrado
                )
                tempo_geracao = time.time() - start_time

                dados = calcula_metricas(G, graus, gamma, tipo, TIPOS_GRAFOS[tipo], seed, numV, tempo_geracao)
                resultados.append(dados)

    return resultados


def salva_resultados_csv(resultados, arquivo='resultados_powerlaw.csv'):
    """Salva resultados em arquivo CSV."""
    if not resultados:
        return
    chaves = list(resultados[0].keys())
    with open(arquivo, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=chaves)
        writer.writeheader()
        writer.writerows(resultados)


# Executar testes
if __name__ == "__main__":
    resultados = executa_testes_pwl(n_execucoes=2, vertices_lista=[100, 1000, 10000])
    salva_resultados_csv(resultados)
    salva_resumo_csv(resultados, arquivo='resumo_powerlaw.csv')
