import numpy as np
import random
import networkx as nx
from constants import (
    TIPOS_DIRIGIDOS, TIPOS_MULTIGRAFOS, TIPOS_PSEUDOGRAFOS,
    GRAU_MIN_PADRAO, GAMMA_MIN, GAMMA_MAX
)


def gerarGrausZipf(n, gamma, kMin=GRAU_MIN_PADRAO, kMax=None):
    """Gera uma lista de graus seguindo distribuição Zipf (power-law)."""
    if kMax is None:
        kMax = n - 1
    
    graus = []
    while len(graus) < n:
        k = np.random.zipf(gamma)
        if kMin <= k <= kMax:
            graus.append(k)
    return graus


def geraGrausPwl(n, gamma, kMin=GRAU_MIN_PADRAO, kMax=None, desequilibrado=False):
    """Gera graus para grafos power-law, com opção de graus desequilibrados para grafos dirigidos."""
    if desequilibrado:
        graus_out = gerarGrausZipf(n, gamma, kMin, kMax)
        graus_in = gerarGrausZipf(n, gamma, kMin, kMax)
        return graus_out, graus_in
    else:
        return gerarGrausZipf(n, gamma, kMin, kMax)


def ajustaGrausDirigidos(graus_out, graus_in):
    """Ajusta graus de entrada e saída para que tenham a mesma soma."""
    soma_out = sum(graus_out)
    soma_in = sum(graus_in)
    diff = soma_out - soma_in

    if diff != 0:
        target = graus_in if diff > 0 else graus_out
        abs_diff = abs(diff)
        indices = np.random.choice(len(target), abs_diff, replace=True)
        for idx in indices:
            target[idx] += 1
    
    return graus_out, graus_in


def constroiGrafoDirigido(graus, tipo, n):
    """Constrói grafo dirigido usando stub matching."""
    multigrafo = tipo in TIPOS_MULTIGRAFOS
    laco = tipo in TIPOS_PSEUDOGRAFOS
    
    G = nx.MultiDiGraph() if multigrafo else nx.DiGraph()
    G.add_nodes_from(range(n))

    if isinstance(graus, tuple):
        graus_out, graus_in = graus
    else:
        graus_out = graus_in = graus

    # Ajusta graus se necessário
    graus_out, graus_in = ajustaGrausDirigidos(graus_out, graus_in)

    # Cria stubs
    out_stubs, in_stubs = [], []
    for node, k in enumerate(graus_out):
        out_stubs.extend([node] * k)
    for node, k in enumerate(graus_in):
        in_stubs.extend([node] * k)

    random.shuffle(out_stubs)
    random.shuffle(in_stubs)

    # Conecta stubs
    while out_stubs and in_stubs:
        u = out_stubs.pop()
        v = in_stubs.pop()
        if not laco and u == v:
            continue
        if not multigrafo and G.has_edge(u, v):
            continue
        G.add_edge(u, v)

    return G


def constroiGrafoNaoDirigido(graus, tipo, n):
    """Constrói grafo não dirigido usando stub matching."""
    multigrafo = tipo in TIPOS_MULTIGRAFOS
    laco = tipo in TIPOS_PSEUDOGRAFOS
    
    G = nx.MultiGraph() if multigrafo else nx.Graph()
    G.add_nodes_from(range(n))

    # Cria stubs
    stubs = []
    for node, grau in enumerate(graus):
        stubs.extend([node] * grau)
    random.shuffle(stubs)

    # Conecta stubs
    while len(stubs) > 1:
        u = stubs.pop()
        v = stubs.pop()
        if not laco and u == v:
            continue
        if not multigrafo and G.has_edge(u, v):
            continue
        G.add_edge(u, v)

    return G


def adicionaCaracteristicasEspeciais(G, tipo):
    """Adiciona características especiais como multigrafos e laços."""
    multigrafo = tipo in TIPOS_MULTIGRAFOS
    laco = tipo in TIPOS_PSEUDOGRAFOS

    # Garante que multigrafos tenham pelo menos uma aresta múltipla
    if multigrafo:
        edges = list(G.edges())
        if edges:
            u, v = edges[0]
            G.add_edge(u, v)

    # Garante que pseudografos tenham pelo menos um laço
    if laco and not any(u == v for u, v in G.edges()):
        v = random.choice(list(G.nodes()))
        G.add_edge(v, v)

    return G


def constroiGrafo(graus, tipo):
    """Constrói grafo baseado no tipo especificado."""
    n = len(graus) if isinstance(graus, list) else len(graus[0])
    dirigido = tipo in TIPOS_DIRIGIDOS

    if dirigido:
        G = constroiGrafoDirigido(graus, tipo, n)
    else:
        G = constroiGrafoNaoDirigido(graus, tipo, n)

    G = adicionaCaracteristicasEspeciais(G, tipo)
    return G


def geraGrafoPwl(numV, gamma=2.5, dirigido=False, tipo=0, seed=None, desequilibrado=False):
    """Função principal para gerar grafos power-law."""
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    graus = geraGrausPwl(numV, gamma, desequilibrado=desequilibrado)
    G = constroiGrafo(graus, tipo)

    if dirigido:
        numA = G.number_of_edges()
        graus_out = graus[0] if isinstance(graus, tuple) else graus
        graus_resultado = graus_out
    else:
        numA = sum(dict(G.degree()).values()) // 2
        graus_resultado = graus

    arestas = list(G.edges())[:numA]
    return arestas, G, graus_resultado


def tipoGrafo(G):
    """Detecta automaticamente o tipo do grafo."""
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
