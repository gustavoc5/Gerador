import networkx as nx
from networkx.algorithms import community as nx_comm

def analisa_grafo(G):
    from statistics import mean

    G_und = G.to_undirected() if G.is_directed() else G

    greedy_sets = list(nx_comm.greedy_modularity_communities(G_und))
    lpa_sets = list(nx_comm.asyn_lpa_communities(G_und))

    deg_cent = nx.degree_centrality(G)
    pr_cent = nx.pagerank(G, alpha=0.85)
    cl_cent = nx.closeness_centrality(G)

    resumo = {
        "num_coms_greedy": len(greedy_sets),
        "tam_maior_greedy": max(len(c) for c in greedy_sets),
        "tam_medio_greedy": round(mean(len(c) for c in greedy_sets), 2),
        "num_coms_lpa": len(lpa_sets),
        "tam_maior_lpa": max(len(c) for c in lpa_sets),
        "tam_medio_lpa": round(mean(len(c) for c in lpa_sets), 2),
        "top5_degree": sorted(deg_cent.items(), key=lambda x: -x[1])[:5],
        "top5_pagerank": sorted(pr_cent.items(), key=lambda x: -x[1])[:5],
        "top5_closeness": sorted(cl_cent.items(), key=lambda x: -x[1])[:5],
    }

    return resumo
