import numpy as np
import random
import networkx as nx


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

    if dirigido:
        out_stubs, in_stubs = [], []
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


def geraGrafoPwl(numV, gamma=2.5, dirigido=False, tipo=0, seed=None):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    graus = geraGrausPwl(numV, gamma)
    numA = sum(graus) if dirigido else sum(graus) // 2
    G = constroiGrafo(graus, tipo)
    arestas = list(G.edges())[:numA]
    return arestas, G, graus


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
