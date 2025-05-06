import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
import powerlaw

def geraBarabasi(numV, numA, tipo=0, seed=None):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    # Estimativa inicial de "m" para gerar número aproximado de arestas
    m = max(1, numA // numV)
    G = nx.barabasi_albert_graph(n=numV, m=m, seed=seed)

    # Ajustar o número de arestas
    arestas_atuais = G.number_of_edges()
    faltam = numA - arestas_atuais

    if faltam > 0:
        while faltam > 0:
            u = random.randint(0, numV - 1)
            v = random.randint(0, numV - 1)
            if u != v:
                if tipo in [20, 30]:  # Permite múltiplas arestas
                    G.add_edge(u, v)
                    faltam -= 1
                elif tipo in [0]:  # Não permite múltiplas
                    if not G.has_edge(u, v):
                        G.add_edge(u, v)
                        faltam -= 1
    elif faltam < 0:
        G.remove_edges_from(random.sample(list(G.edges()), abs(faltam)))

    # Para pseudografo, adiciona laços se necessário
    if tipo == 30:
        for _ in range(numA - G.number_of_edges()):
            u = random.randint(0, numV - 1)
            G.add_edge(u, u)

    return G

def validaDistribuicao(G):
    graus = [d for _, d in G.degree() if d > 0]
    fit = powerlaw.Fit(graus, xmin=2, discrete=True)
    alpha = fit.power_law.alpha
    ks = fit.power_law.KS()
    R, p = fit.distribution_compare('power_law', 'lognormal')
    print("Ajuste Power Law:")
    print("  alpha:", alpha)
    print("  KS:", ks)
    print("  Comparacao com Lognormal: R =", R, ", p =", p)
    fit.plot_pdf(label='Empirical')
    fit.power_law.plot_pdf(label='Power Law', color='r', linestyle='--')
    plt.legend()
    plt.title("Distribuicao de Graus")
    plt.show()

if __name__ == "__main__":
    tipos = {
        0: "Simples",
        20: "Multigrafo",
        30: "Pseudografo"
    }
    print(tipos)
    tipo = int(input("Tipo de grafo: "))
    numV = int(input("Número de Vértices: "))
    numA = int(input("Número de Arestas: "))
    seed_input = input("Semente (opcional): ")
    seed = int(seed_input) if seed_input.strip() != "" else None

    G = geraBarabasi(numV, numA, tipo=tipo, seed=seed)
    print(f"Grafo gerado: {G.number_of_nodes()} vértices, {G.number_of_edges()} arestas")
    validaDistribuicao(G)
