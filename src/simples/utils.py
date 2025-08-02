import numpy as np
import random



def dfs(matriz, inicio, visitados):
    pilha = [inicio]
    while pilha:
        vertice = pilha.pop()
        if vertice not in visitados:
            visitados.add(vertice)
            for vizinho in range(len(matriz)):
                cell = matriz[vertice][vizinho]
                if isinstance(cell, list):
                    cond = len(cell) >= 1
                else:
                    cond = cell >= 1
                if cond and vizinho not in visitados:
                    pilha.append(vizinho)

def compConexas(matriz):
    visitados = set()
    componentes = 0
    for vertice in range(len(matriz)):
        if vertice not in visitados:
            dfs(matriz, vertice, visitados)
            componentes += 1
    return componentes



def atribuiPesos(matriz, minPeso, maxPeso):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] > 0:
                matriz[i][j] = sum(
                    [random.randint(minPeso, maxPeso) for _ in range(matriz[i][j])]
                )
    return matriz


def tipoGrafo(matriz):
    """Detecta o tipo de grafo baseado na matriz de adjacências."""
    laco = False
    multipla = False
    vert = len(matriz)
    
    for i in range(vert):
        for j in range(vert):
            cell = matriz[i][j]
            
            # Verifica se é uma lista (para grafos valorados)
            if isinstance(cell, list):
                if len(cell) > 1:
                    multipla = True
                if len(cell) > 0 and i == j:
                    laco = True
            # Verifica se é um número inteiro
            elif isinstance(cell, (int, float, np.integer)):
                if cell > 1:
                    multipla = True
                if cell > 0 and i == j:
                    laco = True
    
    # Verifica se é dirigido (matriz != transposta)
    dirigido = not (np.transpose(matriz) == matriz).all()
    
    # Determina o tipo baseado nas características
    if dirigido and multipla and laco:
        tipo = 31  # Pseudografo-Dirigido
    elif dirigido and multipla:
        tipo = 21  # Multigrafo-Dirigido
    elif dirigido:
        tipo = 1   # Digrafo
    elif laco:
        tipo = 30  # Pseudografo
    elif multipla:
        tipo = 20  # Multigrafo
    else:
        tipo = 0   # Simples
    
    return tipo

def criaListaAdjacencias(matriz):
    n = len(matriz)
    lista = {}
    for u in range(n):
        adj = []
        for v, cell in enumerate(matriz[u]):
            if isinstance(cell, list):
                for peso in cell:
                    adj.append((v, peso))
            else:
                if cell > 0:
                    adj.append((v, cell))
        lista[u] = adj
    return lista


def criaMatrizAdjacencias(arestas, numV, tipo):
    """Cria matriz de adjacências preservando arestas múltiplas e laços."""
    matriz = np.array([[0] * numV for _ in range(numV)])
    
    # Conta as ocorrências de cada aresta
    from collections import defaultdict
    arestas_count = defaultdict(int)
    
    for u, v in arestas:
        arestas_count[(u, v)] += 1
    
    # Aplica as arestas na matriz
    for (u, v), count in arestas_count.items():
        matriz[u][v] = count
        # Para grafos não dirigidos, adiciona na direção oposta
        if tipo in [0, 20, 30] and u != v:
            matriz[v][u] = count
    
    return matriz


def criaMatrizAdjacenciasValorada(arestas, numV, tipo, minPeso, maxPeso):
    matriz = [[[] for _ in range(numV)] for _ in range(numV)]
    for u, v in arestas:
        peso = random.randint(minPeso, maxPeso)
        matriz[u][v].append(peso)
        if tipo in (0, 20, 30) and u != v:
            matriz[v][u].append(peso)
    return matriz


def escreveMatrizParaArquivo(matriz, listaAdj, nomeArq, numV, numA, seed, n):
    with open(nomeArq, "w") as arquivo:
        arquivo.write(f"numV: {numV}, numA: {numA}, seed: {seed}, n: {n}\n")
        for linha in matriz:
            linha_formatada = " ".join(map(str, linha))
            arquivo.write(f"{linha_formatada}\n")
        arquivo.write(f"{matriz}\n")
        for vertice, adjacencias in listaAdj.items():
            arquivo.write(f"{vertice}: {adjacencias}\n")
