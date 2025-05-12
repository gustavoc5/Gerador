import numpy as np
import random
import networkx as nx


def geraGrausPwl(n, gamma, kMin=1, kMax=None, desequilibrado=False):
    if kMax is None:
        kMax = n - 1

    def gerar_1():
        graus = []
        while len(graus) < n:
            k = np.random.zipf(gamma)
            if kMin <= k <= kMax:
                graus.append(k)
        return graus

    if desequilibrado:
        graus_out = gerar_1()
        graus_in = gerar_1()
        return graus_out, graus_in
    else:
        return gerar_1()



def constroiGrafo(graus, tipo):
    n = len(graus) if isinstance(graus, list) else len(graus[0])
    dirigido = tipo in [1, 21, 31]
    multigrafo = tipo in [20, 21, 30, 31]
    laco = tipo in [30, 31]

    if dirigido:
        G = nx.MultiDiGraph() if multigrafo else nx.DiGraph()
    else:
        G = nx.MultiGraph() if multigrafo else nx.Graph()

    G.add_nodes_from(range(n))

    if dirigido:
        if isinstance(graus, tuple):
            graus_out, graus_in = graus
        else:
            graus_out = graus_in = graus

        # Ajusta as somas para serem iguais
        soma_out = sum(graus_out)
        soma_in = sum(graus_in)
        diff = soma_out - soma_in

        if diff != 0:
            target = graus_in if diff > 0 else graus_out
            abs_diff = abs(diff)
            indices = np.random.choice(n, abs_diff, replace=True)
            for idx in indices:
                target[idx] += 1

        out_stubs, in_stubs = [], []
        for node, k in enumerate(graus_out):
            out_stubs.extend([node] * k)
        for node, k in enumerate(graus_in):
            in_stubs.extend([node] * k)

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
        stubs = []
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

    if multigrafo:
        edges = list(G.edges())
        for u, v in edges:
            G.add_edge(u, v)
            break

    if laco and not any(u == v for u, v in G.edges()):
        v = random.choice(list(G.nodes()))
        G.add_edge(v, v)

    return G



def geraGrafoPwl(numV, gamma=2.5, dirigido=False, tipo=0, seed=None, desequilibrado=False):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    graus = geraGrausPwl(numV, gamma, desequilibrado=desequilibrado)
    G = constroiGrafo(graus, tipo)

    if dirigido:
        numA = G.number_of_edges()
        graus_out = graus[0] if isinstance(graus, tuple) else graus  # <- aqui
        graus_resultado = graus_out
    else:
        numA = sum(dict(G.degree()).values()) // 2
        graus_resultado = graus

    arestas = list(G.edges())[:numA]
    return arestas, G, graus_resultado


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
