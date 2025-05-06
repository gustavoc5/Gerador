from testepwl import geraGrafoPwl, tipoGrafo
import random
import numpy as np
import networkx as nx
import powerlaw as plw

def testa_gerador(n_execucoes=5, numV=300):
    tipos = {
        0: 'Simples',
        1: 'Digrafo',
        20: 'Multigrafo',
        21: 'Multigrafo-Dirigido',
        30: 'Pseudografo',
        31: 'Pseudografo-Dirigido'
    }

    resultados = []

    for tipo in tipos:
        print(f"\n🧪 Testando tipo {tipo} – {tipos[tipo]}")
        for i in range(1, n_execucoes+1):
            gamma  = round(random.uniform(2.0, 3.0), 2)
            seed   = random.randint(0, 10000)
            dirigido = tipo in [1, 21, 31]

            # geração do grafo
            arestas, G, graus = geraGrafoPwl(numV, gamma, dirigido, tipo, seed)
            tipo_gerado = tipoGrafo(G)
            tipo_ok     = (tipo_gerado == tipo)

            # powerlaw KS
            g_filtrados = [g for g in graus if g >= 1]
            fit         = plw.Fit(g_filtrados, xmin=2, discrete=True)
            ks_stat     = fit.power_law.KS()
            pw_ok       = (ks_stat < 0.3)

            # comunidades
            G_und       = G.to_undirected() if G.is_directed() else G
            greedy_coms = list(nx.algorithms.community.greedy_modularity_communities(G_und))
            lp_coms     = list(nx.algorithms.community.label_propagation_communities(G_und))
            n_greedy    = len(greedy_coms)
            n_lp        = len(lp_coms)

            # centralidades
            deg_cent    = nx.degree_centrality(G_und)
            pr_cent     = nx.pagerank(G, alpha=0.85)
            cl_cent     = nx.closeness_centrality(G_und)

            avg_deg     = sum(deg_cent.values())/len(deg_cent)
            max_deg     = max(deg_cent.values())
            avg_pr      = sum(pr_cent.values())/len(pr_cent)
            max_pr      = max(pr_cent.values())
            avg_cl      = sum(cl_cent.values())/len(cl_cent)
            max_cl      = max(cl_cent.values())

            print(f" Exec {i:2d} | KS={ks_stat:.4f} | Tipo {'✅' if tipo_ok else '❌'} "
                  f"| GreedyComs={n_greedy:3d} | LPComs={n_lp:3d} "
                  f"| DC(avg/max)={avg_deg:.3f}/{max_deg:.3f} "
                  f"| PR(max)={max_pr:.3f} | CL(max)={max_cl:.3f}")

            resultados.append({
                'tipo': tipo,
                'descrição': tipos[tipo],
                'execução': i,
                'gamma': gamma,
                'seed': seed,
                'tipo_correto': tipo_ok,
                'ks_stat': round(ks_stat, 4),
                'powerlaw_ok': pw_ok,
                'arestas_geradas': G.number_of_edges(),
                'n_communities_greedy': n_greedy,
                'n_communities_label_prop': n_lp,
                'avg_degree_centrality': avg_deg,
                'max_degree_centrality': max_deg,
                'avg_pagerank': avg_pr,
                'max_pagerank': max_pr,
                'avg_closeness': avg_cl,
                'max_closeness': max_cl
            })

    return resultados


if __name__ == "__main__":
    testa_gerador(n_execucoes=5, numV=1000)
