import random
import numpy as np
from igraph import Graph, plot

def verGrafo(matriz, nomeArq):
    # Verifica se o grafo é direcionado
    dirigido = True
    if (np.transpose(matriz) == matriz).all():
        dirigido = False

    # Cria o grafo
    if dirigido:
        g = Graph.Adjacency(matriz.tolist(), mode="directed")
    else:
        g = Graph.Adjacency(matriz.tolist(), mode="undirected")

    # Adiciona os valores das arestas como pesos (talvez em uma próxima versão que lide grafos valorados)
    # weights = matriz[matriz.nonzero()]
    # if len(weights) > 1:
    #     g.es['weight'] = weights

    # Visualiza o grafo
    g.vs['label'] = g.vs.indices
    # g.es['label'] = g.es['weight']
    layout = g.layout("kk")  # Layout Kamada-Kawai
    plot(g, bbox=(600, 600), layout=layout, edge_arrow_size=0.8, vertex_label_size=14, target= f'C:\\Users\\Gustavo\\OneDrive\\GUSTAVO\\Unifei\\Monitoria\\Imagens-Instancias\\{nomeArq}.png')

def tipoGrafo(matriz):
    laco = False
    multipla = False
    vert = len(matriz)
    for i in range(vert):
        for j in range(vert):
            if matriz[i][j] > 1:
                multipla = True
            if matriz[i][j] > 0 and i == j:
                laco = True
    if (np.transpose(matriz) == matriz).all():
        dirigido = False
    else:
        dirigido = True
    if dirigido and multipla and laco:
        tipo = 31
    elif dirigido and multipla:
        tipo = 21
    elif dirigido:
        tipo = 1
    elif laco:
        tipo = 30
    elif multipla:
        tipo = 20
    else:
        tipo = 0
    print(tipo)
    return tipo

def geraComponente(tipo, numV, numA, seed, numC):
    random.seed(seed)
    datasets = []
    tentativas = 0
    max_att = 50
    if numA < numV - numC:
            raise ValueError("Os valores fornecidos para vértices, arestas e componentes conexas não são consistentes")
        
    while tentativas < max_att:
        print(f'TENTATIVA-{tentativas}')
        matriz = np.array([[0] * numV for _ in range(numV)])
        verticesComp = [0] * numC
        arestasComp = [0] * numC
        
        # aloca a quantidade de vértices para cada componente
        for _ in range(numV):
            component = random.randint(0, numC - 1)
            verticesComp[component] += 1

        arestas_adicionadas = 0
        # aloca a quantidade de arestas para cada componente
        while arestas_adicionadas < numA:
            component = random.randint(0, numC - 1)
            # Garantir que uma componente com um vértice não receba uma aresta se o grafo for simples
            if (tipo != 30 and tipo != 31 and verticesComp[component] == 1):
                continue
            arestasComp[component] += 1
            arestas_adicionadas += 1
        
        print(verticesComp)
        print(arestasComp)
        
        tam = [0] * (numC + 1)
        tam[0] = 0
        for j in range(numC-1):
            tam[j+1] = verticesComp[j]
        tam[numC] = numV
        # 0 8 15
        
        # Criar matriz de adjacências para cada componente conexa
        # compConexas = []
        x = 0 #numero de arestas alocadas
        attemp = 0
        for i in range(numC):
            arestas = []
            if tipo == 0:
                if arestasComp[i] > verticesComp[i] * (verticesComp[i] - 1) / 2:
                    return
                while x < arestasComp[i] and attemp < 50:
                    attemp += 1
                    u = random.randint(tam[i], tam[i+1]-1)
                    v = random.randint(tam[i], tam[i+1]-1)
                    if u != v and (u, v) not in arestas and (v, u) not in arestas:
                        aresta = (min(u, v), max(u, v))
                        arestas.append(aresta)
                        matriz[u][v] += 1
                        matriz[v][u] += 1
                        x += 1
                        attemp = 0
                        
            elif tipo == 1:
                if arestasComp[i] > verticesComp[i] * (verticesComp[i] - 1) / 2:
                    return
                while x < arestasComp[i] and attemp < 50:
                    attemp += 1
                    u = random.randint(tam[i], tam[i+1]-1)
                    v = random.randint(tam[i], tam[i+1]-1)
                    if u != v and (u, v) not in arestas:
                        arestas.append((u, v))
                        matriz[u][v] += 1
                        x += 1
                        attemp = 0
            
            elif tipo == 20:
                while x < arestasComp[i] and attemp < 50:
                    attemp += 1
                    u = random.randint(tam[i], tam[i+1]-1)
                    v = random.randint(tam[i], tam[i+1]-1)
                    if u != v:
                        aresta = (min(u, v), max(u, v))
                        arestas.append(aresta)
                        matriz[u][v] += 1
                        matriz[v][u] += 1
                        x += 1
                        attemp = 0
            
            elif tipo == 21:
                while x < arestasComp[i] and attemp < 50:
                    attemp += 1
                    u = random.randint(tam[i], tam[i+1]-1)
                    v = random.randint(tam[i], tam[i+1]-1)
                    if u != v:
                        aresta = (u, v)
                        arestas.append(aresta)
                        x += 1
                        attemp = 0
                        
            elif tipo == 30:
                while x < arestasComp[i]:
                    x += 1
                    loop = False
                    u = random.randint(tam[i], tam[i+1]-1)
                    v = random.randint(tam[i], tam[i+1]-1)
                    aresta = (min(u, v), max(u, v))
                    arestas.append(aresta)
                    if u == v:
                        loop = True
                        matriz[u][v] += 1
                    else:
                        loop = False
                        matriz[u][v] += 1
                        matriz[v][u] += 1
        
            elif tipo == 31:
                while x < arestasComp[i]:
                    x += 1
                    loop = False
                    u = random.randint(tam[i], tam[i+1]-1)
                    v = random.randint(tam[i], tam[i+1]-1)
                    arestas.append((u, v))
                    if u == v:
                        loop = True
                    matriz[u][v] += 1
            if attemp == 50:
                print("Os parâmetros não foram aceitos após 50 tentativas.")
        #     else:
        #         compConexas.append(matriz)
        # print(matriz)
        # if tipoGrafo(matriz) != tipo:
        #         break
        # else:
        #     compConexas.append(matriz)
                
        # Se a união das componentes conexas forma o tipo de grafo especificado, retorna o dataset
        # if len(compConexas) == numC:
        #     grafo = np.block(compConexas)
        #     print(f'{tentativas}-{grafo}')
        #     if tipoGrafo(grafo) == tipo:
        #         datasets.append(grafo)
        #         max_att -= 1
        #         if max_att == 0:
        #             return datasets
        if tipoGrafo(matriz) == tipo and i == numC - 1:
            return matriz
        else:
            tentativas += 1
    print("Os parâmetros não foram aceitos após 50 tentativas.")
    return

def dfs(matriz, vertice, visitados):
    visitados.add(vertice)
    for vizinho in range(len(matriz)):
        if matriz[vertice][vizinho] >= 1 and vizinho not in visitados:
            dfs(matriz, vizinho, visitados)

def compConexas(matriz):
    visitados = set()
    componentes = 0
    for vertice in range(len(matriz)):
        if vertice not in visitados:
            dfs(matriz, vertice, visitados)
            componentes += 1
    return componentes

def geraDataset(tipo, numV, numA, seed, n, numC):
    random.seed(seed)
    datasets = []
    tentativas = 0
    maximo = 100
    while len(datasets) != n and tentativas < maximo:
        arestas = []
        if tipo == 0:
            # Grafo Simples
            if numA > numV * (numV - 1) / 2:
                raise ValueError("Número de arestas excede o máximo permitido para um grafo simples.")
            while len(arestas) < numA:
                u = random.randint(0, numV-1)
                v = random.randint(0, numV-1)
                if u != v and (u, v) not in arestas and (v, u) not in arestas:
                    aresta = (min(u, v), max(u, v))
                    arestas.append(aresta)
        
        elif tipo == 1:
            # Grafo Dirigido
            if numA > numV * (numV - 1):
                raise ValueError("Número de arestas excede o máximo permitido para um digrafo.")
            
            while len(arestas) < numA:
                u = random.randint(0, numV-1)
                v = random.randint(0, numV-1)
                if u != v and (u, v) not in arestas:
                    aresta = (u, v)
                    arestas.append(aresta)
        
        elif tipo == 20:
            # Multigrafo Simples
            while len(arestas) < numA - 1:
                u = random.randint(0, numV-1)
                v = random.randint(0, numV-1)
                if u != v:
                    aresta = (min(u, v), max(u, v))
                    arestas.append(aresta)
            
            # Adicionar uma aresta múltipla se necessário
            if len(set(arestas)) == len(arestas):
                aresta_existente = random.choice(arestas)
                u, v = aresta_existente
                arestas.append((u, v))
                
            else:
                while True:
                    u = random.randint(0, numV-1)
                    v = random.randint(0, numV-1)
                    if u == v:
                        continue
                    aresta = (min(u, v), max(u, v))
                    arestas.append(aresta)
                    break
        
        elif tipo == 21:
            # Multigrafo Dirigido
            while len(arestas) < numA - 1:
                u = random.randint(0, numV-1)
                v = random.randint(0, numV-1)
                if u != v:
                    aresta = (u, v)
                    arestas.append(aresta)
            
            # Adicionar uma aresta múltipla se necessário
            if len(set(arestas)) == len(arestas):
                aresta_existente = random.choice(arestas)
                u, v = aresta_existente
                arestas.append((u, v))
                
            else:
                while True:
                    u = random.randint(0, numV-1)
                    v = random.randint(0, numV-1)
                    if u == v:
                        continue
                    aresta = (u, v)
                    arestas.append(aresta)
                    break
                
        elif tipo == 30:
            # Pseudografo Simples
            loop = False
            while len(arestas) < numA -1:
                u = random.randint(0, numV-1)
                v = random.randint(0, numV-1)
                aresta = (min(u, v), max(u, v))
                arestas.append(aresta)
                if u == v:
                    loop = True
            
            # Adicionar um laço se necessário
            if loop:
                u = random.randint(0, numV-1)
                v = random.randint(0, numV-1)
                aresta = (min(u, v), max(u, v))
                arestas.append(aresta)
                
            else:
                u = random.randint(0, numV-1)
                v = u
                arestas.append((u, v))
                
        
        elif tipo == 31:
            # Pseudografo Dirigido
            loop = False
            while len(arestas) < numA -1:
                u = random.randint(0, numV-1)
                v = random.randint(0, numV-1)
                aresta = (u, v)
                arestas.append((u, v))
                if u == v:
                    loop = True
            
            # Adicionar um laço se necessário
            if loop:
                u = random.randint(0, numV-1)
                v = random.randint(0, numV-1)
                aresta = (u, v)
                arestas.append((u, v))
                
            else:
                u = random.randint(0, numV-1)
                v = u
                arestas.append((u, v))
                
        else:
            raise ValueError("Tipo de grafo inválido.")
        
        matriz = criaMatrizAdjacencias(arestas, numV, tipo)
        if (numC == compConexas(matriz) or numC == 0):
            datasets.append(sorted(list(arestas)))
            tentativas = 0
        else:
            tentativas += 1
            
    if tentativas == maximo:
        raise ValueError(f"Incapaz de gerar o grafo em {maximo} tentativas")
        
    return datasets

def criaListaAdjacencias(matriz):
    listaAdj = {}
    for i, linha in enumerate(matriz):
        adjc = []
        for j, valor in enumerate(linha):
            if valor > 0:
                adjc.extend([j]*valor)
        listaAdj[i] = adjc
    return listaAdj

def criaMatrizAdjacencias(arestas, numV, tipo):
    matriz = np.array([[0] * numV for _ in range(numV)])  # Inicializa uma matriz de adjacências com zeros
    
    for aresta in arestas:
        u, v = aresta
        matriz[u][v] += 1
        
        if '0' in str(tipo) and u != v:
            matriz[v][u] += 1
    
    return matriz

def escreveMatrizParaArquivo(matriz, listaAdj, nomeArq, numV, numA, seed, n):
    with open(nomeArq, 'w') as arquivo:
        arquivo.write(f"numV: {numV}, numA: {numA}, seed: {seed}, n: {n}\n")
        
        for linha in matriz:
            linha_formatada = ' '.join(map(str, linha))
            arquivo.write(f"{linha_formatada}\n")  

        arquivo.write(f"{np.array(matriz).tolist()}\n")
        
        for vertice, adjacencias in listaAdj.items():
            arquivo.write(f"{vertice}: {adjacencias}\n")

if __name__ == '__main__':
    tipos = {
        0 : 'Simples',
        1 : 'Digrafo',
        20: 'Multigrafo',
        21: 'Multigrafo-Dirigido',
        30: 'Pseudografo',
        31: 'Pseudografo-Dirigido'
    }
    print(tipos)
    tipo = int(input('Tipo Grafo: '))
    numV = int(input('Número de Vértices: '))
    numA = int(input('Número de Arestas: '))
    seed = input('Semente (Não obrigatório): ')
    n = input('Número de datasets: ')
    numComp = input('Número de componentes conexas: ')
    
    if seed == "":
        seed = random.randint(0, 1000)
    else:
        seed = int(seed)
    
    if n == "":
        n = 1
    else:
        n = int(n)
        
    if numComp == "":
        numComp = 0
    else:
        numComp = int(numComp) 

    datasets = geraDataset(tipo, numV, numA, seed, n, numComp)
    # print(datasets)
    for i, dataset in enumerate(datasets):
        nomeArq = f"{tipos[tipo]}-{numV}-{numA}-{seed}-{i+1}-{numComp}"
        arq = f'C:\\Users\\Gustavo\\OneDrive\\GUSTAVO\\Unifei\\Monitoria\\Imagens-Instancias\\{nomeArq}.txt'
        matriz = criaMatrizAdjacencias(dataset, numV, tipo)
        listaAdj = criaListaAdjacencias(matriz)
        escreveMatrizParaArquivo(matriz, listaAdj, arq, numV, numA, seed, i+1)
        verGrafo(matriz, nomeArq)