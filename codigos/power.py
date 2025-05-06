import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt
import powerlaw as plw

# Gera sequência de graus com power law
def geraGrausPwl(n, gamma, kMin=1, kMax=None):
    if kMax is None:
        kMax = n - 1
    graus = []
    while len(graus) < n:
        k = np.random.zipf(gamma)
        if kMin <= k <= kMax:
            graus.append(k)
    return graus

def constroiGrafo(graus, tipo):
    n = len(graus)
    dirigido = tipo in [1, 21, 31]
    multigrafo = tipo in [20, 21, 30, 31]
    laco = tipo in [30, 31]

    if dirigido:
        G = nx.MultiDiGraph() if multigrafo else nx.DiGraph()
    else:
        G = nx.MultiGraph() if multigrafo else nx.Graph()

    G.add_nodes_from(range(n))

    # Emparelhamento de stubs (graus -> arestas)
    stubs = []

    if dirigido:
        # Para grafos dirigidos, gera out-degree e in-degree separadamente
        out_stubs = []
        in_stubs = []
        for node, grau in enumerate(graus):
            out_stubs.extend([node] * grau)
            in_stubs.extend([node] * grau)
        random.shuffle(out_stubs)
        random.shuffle(in_stubs)

        while out_stubs and in_stubs:
            u = out_stubs.pop()
            v = in_stubs.pop()
            if not laco and u == v:
                continue
            if not multigrafo and G.has_edge(u, v):
                continue
            G.add_edge(u, v)
    else:
        # Para não-dirigidos, emparelha pares de vértices
        for node, grau in enumerate(graus):
            stubs.extend([node] * grau)
        random.shuffle(stubs)

        while len(stubs) > 1:
            u = stubs.pop()
            v = stubs.pop()
            if not laco and u == v:
                continue
            if not multigrafo and G.has_edge(u, v):
                continue
            G.add_edge(u, v)
    if laco and not any(u == v for u, v in G.edges()):
        v = random.choice(list(G.nodes()))
        G.add_edge(v, v)
    return G

def geraGrafoPwl(numV, numA, gamma=2.5, dirigido=False, tipo=0, seed=None):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    graus = geraGrausPwl(numV, gamma)

    G = constroiGrafo(graus, tipo)

    arestas = list(G.edges())[:numA]
    return arestas, G

def tipoGrafo(G):
    dirigido = G.is_directed()
    multigrafo = G.is_multigraph()
    laco = any(u == v for u, v in G.edges())
    multipla = any(G.number_of_edges(u, v) > 1 for u, v in G.edges()) if multigrafo else False

    if dirigido and multipla and laco:
        return 31
    elif dirigido and multipla:
        return 21
    elif dirigido:
        return 1
    elif laco:
        return 30
    elif multipla:
        return 20
    else:
        return 0

def validaDistribuicao(graus, gamma):
    graus = [g for g in graus if g >= 1]  # ignora graus < 1

    fit = plw.Fit(graus, xmin=2, discrete=True)
    alpha = fit.power_law.alpha
    ks_stat = fit.power_law.KS()

    print("Ajuste Power Law:")
    print("  α (alpha):", alpha)
    print("  KS Statistic:", ks_stat)

    valores, contagens = np.unique(graus, return_counts=True)
    valores = valores[valores >= 1]
    contagens = contagens[:len(valores)]

    # Criação dos dois subplots
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))

    # Subplot 1: Escala log-log
    axs[0].bar(valores, contagens, width=0.8, color='skyblue', edgecolor='black', label='Frequência Empírica')
    x = np.array(valores)
    y = x ** (-gamma)
    y = y * (max(contagens) / max(y))
    axs[0].plot(x, y, 'r--', linewidth=2, label=f'k^-{gamma:.2f} (Power Law)')
    axs[0].set_xscale('log')
    axs[0].set_yscale('log')
    axs[0].set_xlim(left=1)
    axs[0].set_ylim(bottom=1)
    axs[0].set_xlabel('Grau (log)', fontsize=11)
    axs[0].set_ylabel('Frequência (log)', fontsize=11)
    axs[0].set_title('Escala Log-Log', fontsize=13)
    axs[0].legend()
    axs[0].grid(True, which='both', ls='--', linewidth=0.5)

    # Subplot 2: Escala linear
    axs[1].bar(valores, contagens, width=0.8, color='skyblue', edgecolor='black', label='Frequência Empírica')
    x_lin = np.linspace(min(valores), max(valores), 200)
    y_lin = x_lin ** (-gamma)
    y_lin = y_lin * (max(contagens) / max(y_lin))
    axs[1].plot(x_lin, y_lin, 'r--', linewidth=2, label=f'k^-{gamma:.2f} (Power Law)')
    axs[1].set_xlabel('Grau', fontsize=11)
    axs[1].set_ylabel('Frequência', fontsize=11)
    axs[1].set_title('Escala Linear', fontsize=13)
    axs[1].legend()
    axs[1].grid(True, ls='--', linewidth=0.5)

    plt.suptitle('Distribuição de Graus: Power Law Empírica vs Teórica', fontsize=15)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

def visualizaGrafo(G, dirigido=False):
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)
    nx.draw_networkx_nodes(G, pos, node_size=50, node_color='skyblue')
    nx.draw_networkx_edges(G, pos, alpha=0.4, arrows=dirigido)
    plt.title("Visualização do Grafo Gerado")
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    print("Tipo de grafo:")
    print("0: Simples, 1: Digrafo, 20: Multigrafo, 21: Multigrafo-Dirigido, 30: Pseudografo, 31: Pseudografo-Dirigido")
    tipo = int(input("Tipo: "))
    dirigido = tipo in [1, 21, 31]

    numV = int(input("Número de Vértices: "))

    if tipo == 0:
        minA = numV - 1
        maxA = int(numV * (numV - 1) / 2)
    elif tipo == 1:
        minA = numV - 1
        maxA = numV * (numV - 1)
    elif tipo == 30:
        minA = numV - 1
        maxA = int(numV * (numV - 1) / 2 + numV)
    elif tipo == 31:
        minA = numV - 1
        maxA = numV * (numV - 1) + numV
    else:
        minA = numV - 1
        maxA = float('inf')

    if maxA == float('inf'):
        print(f"O número de arestas deve ser no mínimo {minA}.")
    else:
        print(f"O número de arestas deve estar entre {minA} e {maxA}.")

    numA = int(input("Número de Arestas: "))
    gamma = float(input("Expoente (gamma) da distribuição (padrão aleatório entre 2.00 e 3.00): ") or round(random.uniform(2, 3), 2))
    seed = input("Semente (opcional): ")
    seed = int(seed) if seed.strip() != "" else None
    
    arestas, G = geraGrafoPwl(numV, numA, gamma, dirigido, tipo, seed)

    graus = [d for _, d in (G.out_degree() if G.is_directed() else G.degree())]

    print("Número de arestas no grafo final:", G.number_of_edges())
    
    tipo_detectado = tipoGrafo(G)
    print("Tipo solicitado:", tipo)
    print("Tipo detectado:", tipo_detectado)
    if tipo_detectado != tipo:
        print("⚠️ Atenção: O grafo gerado NÃO corresponde ao tipo solicitado!")
    else:
        print("✅ O grafo gerado corresponde ao tipo solicitado.")

    validaDistribuicao(graus, gamma)
    
    visualizaGrafo(G, dirigido)