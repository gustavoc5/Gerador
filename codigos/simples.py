import random
import numpy as np
from igraph import Graph, plot
import math
import sys


def verGrafo(matriz, nomeArq):
    # número de vértices
    n = len(matriz)

    # 1) Detectar se é dirigido:
    #    basta comparar o número de arcos (ou lista de pesos) em (i,j) vs (j,i)
    dirigido = False
    for i in range(n):
        for j in range(n):
            c_ij = matriz[i][j]
            c_ji = matriz[j][i]
            cnt_ij = len(c_ij) if isinstance(c_ij, list) else c_ij
            cnt_ji = len(c_ji) if isinstance(c_ji, list) else c_ji
            if cnt_ij != cnt_ji:
                dirigido = True
                break
        if dirigido:
            break

    # 2) Construir as listas de arestas e pesos
    edges = []
    weights = []
    for i in range(n):
        for j in range(n):
            cell = matriz[i][j]
            if isinstance(cell, list):
                # em cada lista, cada elemento é um arco paralelo
                for peso in cell:
                    edges.append((i, j))
                    weights.append(peso)
            elif cell > 0:
                # cell é um inteiro: multiplicidade ou peso único
                edges.append((i, j))
                weights.append(cell)

    # 3) Montar o grafo no igraph
    g = Graph(directed=dirigido)
    g.add_vertices(n)
    g.add_edges(edges)
    g.es["weight"] = weights
    g.es["label"] = weights  # exibe o peso de cada arco
    g.vs["label"] = g.vs.indices

    # 4) Layout e plotagem
    layout = g.layout("kk")  # Kamada-Kawai
    plot(
        g,
        bbox=(600, 600),
        layout=layout,
        edge_arrow_size=0.8,
        vertex_label_size=14,
        edge_label=g.es["label"],
        target=f"{nomeArq}.png",
    )


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
    return tipo


# função que relaciona o número de vértices, arestas e componentes conexas
def verificaAresta(tipo, numV, numC):
    if numV - (numC - 1) <= 0:
        raise ValueError("Número de vértices e componentes conexas inválido")

    if tipo == 0:
        minimo = (numV - (numC - 1)) - 1
        maximo = ((numV - (numC - 1)) * (numV - numC)) / 2
    elif tipo == 1:
        minimo = (numV - (numC - 1)) - 1
        maximo = (numV - (numC - 1)) * (numV - numC)
    elif "2" in str(tipo):
        minimo = numV - (numC - 1)
        maximo = math.inf
    elif "3" in str(tipo):
        minimo = numV - (numC - 1)
        maximo = math.inf
    return minimo, maximo


def geraComponente(tipo, numV, numA, numC, fator):
    tentativas = 0
    maximo = 100

    while tentativas < maximo:
        matriz = np.array([[0] * numV for _ in range(numV)])
        verticesComp = [0] * numC
        arestasComp = [0] * numC
        # divide os vértices em grupos iguais
        if fator == 2:
            resto = numV % numC
            vert = numV // numC
            verticesComp = [vert] * numC
            verticesComp[0] += resto
        else:
            # aloca a quantidade de vértices para cada componente
            for _ in range(numV):
                component = random.randint(0, numC - 1)
                verticesComp[component] += 1

            if not all(verticesComp):
                continue

        arestasRestantes = numA
        minArestas = [0] * numC
        maxArestas = [0] * numC

        # aloca a quantidade de arestas para cada componente
        for i in range(numC):
            if tipo == 0:
                minArestas[i] = verticesComp[i] - 1
                maxArestas[i] = (verticesComp[i] * (verticesComp[i] - 1)) / 2
            elif tipo == 1:
                minArestas[i] = verticesComp[i] - 1
                maxArestas[i] = verticesComp[i] * (verticesComp[i] - 1)
            elif "2" in str(tipo):
                if verticesComp[i] == 1:
                    minArestas[i] = 0
                    maxArestas[i] = 0
                else:
                    minArestas[i] = verticesComp[i]
                    maxArestas[i] = math.inf
            elif "3" in str(tipo):
                minArestas[i] = verticesComp[i]
                maxArestas[i] = math.inf

        if fator == 2:
            resto = numA % numC
            arest = numA // numC
            arestasComp = [arest] * numC
            arestasComp[0] += resto
            for i in range(numC):
                if minArestas[i] > arestasComp[i]:
                    raise ValueError(
                        "Não é possível gerar um grafo balanceado com esse número de arestas, considere aumentar"
                    )
                elif maxArestas[i] < arestasComp[i]:
                    raise ValueError(
                        "Não é possível gerar um grafo balanceado com esse número de arestas, considere diminuir"
                    )
        else:
            for i in range(numC - 1):
                if minArestas[i] < maxArestas[i]:
                    try:
                        arestasComp[i] = random.randint(
                            minArestas[i],
                            int(
                                min(
                                    maxArestas[i],
                                    arestasRestantes
                                    - sum(
                                        min(minArestas[j], maxArestas[j])
                                        for j in range(i + 1, numC)
                                    ),
                                )
                            ),
                        )
                    except ValueError as e:
                        print(
                            f"Erro ao gerar um valor aleatório para arestasComp[{i}], considere alterar o número de arestas: {e}"
                        )
                else:
                    continue
                arestasRestantes -= arestasComp[i]

            arestasComp[numC - 1] = numA - sum(arestasComp)
            if (
                arestasComp[numC - 1] < minArestas[numC - 1]
                or arestasComp[numC - 1] > maxArestas[numC - 1]
            ):
                tentativas += 1
                continue

        if fator == 1:
            verticesComp = sorted(verticesComp)
            arestasComp = sorted(arestasComp)

        tam = [0] * (numC + 1)
        tam[0] = 0
        for j in range(1, numC):
            tam[j] = tam[j - 1] + verticesComp[j - 1]
        tam[numC] = numV

        arestas = []
        for i in range(numC):
            x = 0
            # Cria uma lista de vértices para a componente atual
            vertices = list(range(tam[i], tam[i + 1]))

            # Embaralha a lista de vértices
            random.shuffle(vertices)

            # Conecta cada vértice ao próximo na lista
            for j in range(len(vertices) - 1):

                u, v = vertices[j], vertices[j + 1]
                if "0" in str(tipo):  # Grafo simples
                    arestas.append((u, v))
                    matriz[u][v] += 1
                    matriz[v][u] += 1
                    x += 1

                else:  # Grafo dirigido
                    arestas.append((u, v))
                    matriz[u][v] += 1
                    x += 1

            if tipo == 0:
                while x < arestasComp[i]:
                    u = random.randint(tam[i], tam[i + 1] - 1)
                    v = random.randint(tam[i], tam[i + 1] - 1)
                    if u != v and (u, v) not in arestas and (v, u) not in arestas:
                        aresta = (min(u, v), max(u, v))
                        arestas.append(aresta)
                        matriz[u][v] += 1
                        matriz[v][u] += 1
                        x += 1

            elif tipo == 1:
                while x < arestasComp[i]:
                    u = random.randint(tam[i], tam[i + 1] - 1)
                    v = random.randint(tam[i], tam[i + 1] - 1)
                    if u != v and (u, v) not in arestas:
                        arestas.append((u, v))
                        matriz[u][v] += 1
                        x += 1

            elif tipo == 20:
                multipla = False
                while x < arestasComp[i]:
                    u = random.randint(tam[i], tam[i + 1] - 1)
                    v = random.randint(tam[i], tam[i + 1] - 1)

                    if (
                        u != v
                        and i == numC - 1
                        and x == arestasComp[i] - 2
                        and not multipla
                    ):
                        aresta_existente = random.choice(arestas)
                        u, v = aresta_existente
                        arestas.append((u, v))
                        matriz[u][v] += 1
                        matriz[v][u] += 1
                        x += 1

                    elif u != v:
                        if (u, v) in arestas:
                            multipla = True
                        aresta = (min(u, v), max(u, v))
                        arestas.append(aresta)
                        matriz[u][v] += 1
                        matriz[v][u] += 1
                        x += 1

            elif tipo == 21:
                multipla = False
                while x < arestasComp[i]:
                    u = random.randint(tam[i], tam[i + 1] - 1)
                    v = random.randint(tam[i], tam[i + 1] - 1)

                    if (
                        u != v
                        and i == numC - 1
                        and x == arestasComp[i] - 2
                        and not multipla
                    ):
                        aresta_existente = random.choice(arestas)
                        u, v = aresta_existente
                        arestas.append((u, v))
                        matriz[u][v] += 1
                        x += 1

                    elif u != v:
                        if (u, v) in arestas:
                            multipla = True
                        aresta = (u, v)
                        arestas.append(aresta)
                        matriz[u][v] += 1
                        x += 1

            elif tipo == 30:
                loop = False
                while x < arestasComp[i]:
                    x += 1
                    u = random.randint(tam[i], tam[i + 1] - 1)
                    v = random.randint(tam[i], tam[i + 1] - 1)
                    if u == v:
                        loop = True
                        matriz[u][v] += 1

                    elif i == numC - 1 and x == arestasComp[i] - 1 and not loop:
                        aresta = (u, u)
                        arestas.append(aresta)
                        matriz[u][u] += 1
                        break

                    else:
                        matriz[u][v] += 1
                        matriz[v][u] += 1

                    aresta = (min(u, v), max(u, v))
                    arestas.append(aresta)

            elif tipo == 31:
                loop = False
                while x < arestasComp[i]:
                    x += 1
                    u = random.randint(tam[i], tam[i + 1] - 1)
                    v = random.randint(tam[i], tam[i + 1] - 1)

                    if u == v:
                        loop = True

                    elif i == numC - 1 and x == arestasComp[i] - 1 and not loop:
                        aresta = (u, u)
                        arestas.append(aresta)
                        matriz[u][u] += 1
                        break

                    matriz[u][v] += 1
                    arestas.append((u, v))

        if (
            tipoGrafo(matriz) == tipo
            and len(arestas) == numA
            and (numC == compConexas(matriz) or "1" in str(tipo))
        ):
            return arestas
        else:
            tentativas += 1
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


def atribuiPesos(matriz, minPeso, maxPeso):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] > 0:
                matriz[i][j] = sum(
                    [random.randint(minPeso, maxPeso) for _ in range(matriz[i][j])]
                )
    return matriz


def geraDataset(tipo, numV, numA, seed, n, numC, fator):
    random.seed(seed)
    datasets = []
    tentativas = 0
    maximo = 100

    if numC > 0:
        while len(datasets) != n and tentativas < maximo:
            tentativas += 1
            grafo = geraComponente(tipo, numV, numA, numC, fator)
            if grafo != None:
                datasets.append(sorted(list(grafo)))
                tentativas = 0
            else:
                continue
        if tentativas == maximo:
            sys.exit(
                "\nNúmero máximo de tentativas, considere alterar o número de arestas ou deixar grafo aleatório\nErro crítico: encerrando o programa."
            )

    else:
        for _ in range(n):
            arestas = []
            if tipo == 0:
                # Grafo Simples
                if numA > numV * (numV - 1) / 2:
                    raise ValueError(
                        "Número de arestas excede o máximo permitido para um grafo simples."
                    )
                while len(arestas) < numA:
                    u = random.randint(0, numV - 1)
                    v = random.randint(0, numV - 1)
                    if u != v and (u, v) not in arestas and (v, u) not in arestas:
                        aresta = (min(u, v), max(u, v))
                        arestas.append(aresta)

            elif tipo == 1:
                # Grafo Dirigido
                if numA > numV * (numV - 1):
                    raise ValueError(
                        "Número de arestas excede o máximo permitido para um digrafo."
                    )

                while len(arestas) < numA:
                    u = random.randint(0, numV - 1)
                    v = random.randint(0, numV - 1)
                    if u != v and (u, v) not in arestas:
                        aresta = (u, v)
                        arestas.append(aresta)

            elif tipo == 20:
                # Multigrafo Simples
                while len(arestas) < numA - 1:
                    u = random.randint(0, numV - 1)
                    v = random.randint(0, numV - 1)
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
                        u = random.randint(0, numV - 1)
                        v = random.randint(0, numV - 1)
                        if u == v:
                            continue
                        aresta = (min(u, v), max(u, v))
                        arestas.append(aresta)
                        break

            elif tipo == 21:
                # Multigrafo Dirigido
                while len(arestas) < numA - 1:
                    u = random.randint(0, numV - 1)
                    v = random.randint(0, numV - 1)
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
                        u = random.randint(0, numV - 1)
                        v = random.randint(0, numV - 1)
                        if u == v:
                            continue
                        aresta = (u, v)
                        arestas.append(aresta)
                        break

            elif tipo == 30:
                # Pseudografo Simples
                loop = False
                while len(arestas) < numA - 1:
                    u = random.randint(0, numV - 1)
                    v = random.randint(0, numV - 1)
                    aresta = (min(u, v), max(u, v))
                    arestas.append(aresta)
                    if u == v:
                        loop = True

                # Adicionar um laço se necessário
                if loop:
                    u = random.randint(0, numV - 1)
                    v = random.randint(0, numV - 1)
                    aresta = (min(u, v), max(u, v))
                    arestas.append(aresta)

                else:
                    u = random.randint(0, numV - 1)
                    v = u
                    arestas.append((u, v))

            elif tipo == 31:
                # Pseudografo Dirigido
                loop = False
                while len(arestas) < numA - 1:
                    u = random.randint(0, numV - 1)
                    v = random.randint(0, numV - 1)
                    aresta = (u, v)
                    arestas.append((u, v))
                    if u == v:
                        loop = True

                # Adicionar um laço se necessário
                if loop:
                    u = random.randint(0, numV - 1)
                    v = random.randint(0, numV - 1)
                    aresta = (u, v)
                    arestas.append((u, v))

                else:
                    u = random.randint(0, numV - 1)
                    v = u
                    arestas.append((u, v))

            else:
                raise ValueError("Tipo de grafo inválido.")

            datasets.append(sorted(list(arestas)))

    return datasets


def criaListaAdjacencias(matriz):
    n = len(matriz)
    lista = {}
    for u in range(n):
        adj = []
        for v, cell in enumerate(matriz[u]):
            if isinstance(cell, list):
                # cada elemento da lista é um peso de um arco paralelo
                for peso in cell:
                    adj.append((v, peso))
            else:
                # cell é um inteiro: 0 = sem aresta; >0 = peso ou multiplicidade
                if cell > 0:
                    adj.append((v, cell))
        lista[u] = adj
    return lista


def criaMatrizAdjacencias(arestas, numV, tipo):
    matriz = np.array(
        [[0] * numV for _ in range(numV)]
    )  # Inicializa uma matriz de adjacências com zeros

    for aresta in arestas:
        u, v = aresta
        matriz[u][v] += 1

        if "0" in str(tipo) and u != v:
            matriz[v][u] += 1

    return matriz


def criaMatrizAdjacenciasValorada(arestas, numV, tipo, minPeso, maxPeso):
    # Em vez de [[ ]], já crio matrix de listas
    matriz = [[[] for _ in range(numV)] for _ in range(numV)]

    for aresta in arestas:
        u, v = aresta
        # gera peso aleatório para esta instância de aresta
        peso = random.randint(minPeso, maxPeso)
        matriz[u][v].append(peso)

        # se for não-dirigido (as simples, multigrafos e pseudografos não-dirigidos)
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


if __name__ == "__main__":
    tipos = {
        0: "Simples",
        1: "Digrafo",
        20: "Multigrafo",
        21: "Multigrafo-Dirigido",
        30: "Pseudografo",
        31: "Pseudografo-Dirigido",
    }
    geracao = {0: "Aleatório", 1: "Parcialmente Balanceado", 2: "Balanceado"}

    while True:
        print("\nTipos de grafo disponíveis:")
        for k, v in tipos.items():
            print(f"  {k}: {v}")
        tipo = int(input("Tipo Grafo: "))
        numV = int(input("Número de Vértices: "))

        # 1) Componentes conexas
        numComp = input("Número de componentes conexas (padrão 0): ").strip()
        numComp = int(numComp) if numComp else 0

        # 2) Preferência de densidade
        print("\nPreferência de densidade:")
        print("  0: Sem preferência")
        print("  1: Esparso (densidade ≤ 0.2)")
        print("  2: Denso   (densidade ≥ 0.8)")
        densPref = int(input("Escolha [0/1/2] (padrão 0): ") or 0)

        # 3) Grafo valorado?
        valorado = input("O grafo será valorado? (y/n): ").strip().lower() == "y"
        if valorado:
            minPeso = input("Peso mínimo das arestas (padrão = 1): ").strip()
            maxPeso = input("Peso máximo das arestas (padrão = 10): ").strip()
            minPeso = int(minPeso) if minPeso.isdigit() else 1
            maxPeso = int(maxPeso) if maxPeso.isdigit() else 10

        # 4) intervalo básico de conectividade
        minA, maxA = verificaAresta(tipo, numV, numComp)

        # 5) máximo de posições distintas de arestas
        if tipo == 0 or tipo == 20:
            g_max = numV * (numV - 1) / 2
        elif tipo == 1 or tipo == 21:
            g_max = numV * (numV - 1)
        elif tipo == 30:
            g_max = numV * (numV - 1) / 2 + numV
        elif tipo == 31:
            g_max = numV * (numV - 1) + numV

        # 6) restrição adicional por densidade
        if densPref == 1:  # esparso
            lowA = max(minA, int(0.05 * g_max))  # esparsidade mínima viável
            highA = max(minA, int(0.2 * g_max))
        elif densPref == 2:  # denso
            lowA = max(minA, int(0.8 * g_max))
            highA = min(maxA, int(g_max))
        else:  # sem preferência
            lowA = minA
            highA = int(maxA) if not math.isinf(maxA) else int(g_max)

        # 7) prompt ao usuário
        if highA <= lowA:
            raise ValueError(f"Não há intervalo viável de arestas entre {lowA} e {highA}. Ajuste os parâmetros.")

        print(f"\nO número de arestas deve estar entre {lowA} e {highA}.")
        numA = int(input("Número de Arestas: "))
        if numA < lowA or numA > highA:
            raise ValueError(f"Número de arestas {numA} fora do intervalo [{lowA},{highA}]")


        seed = input("Semente (Não obrigatório): ").strip()
        seed = int(seed) if seed else random.randint(0, 1000)
        n = input("Número de datasets: ").strip()
        n = int(n) if n else 1
        fator = input("0-Aleatório 1-Parcial 2-Balanceado: ").strip()
        fator = int(fator) if fator else random.randint(0, 2)

        datasets = geraDataset(tipo, numV, numA, seed, n, numComp, fator)

        for i, dataset in enumerate(datasets):
            nomeArq = f"{tipos[tipo]}-{geracao[fator][0]}-{numV}-{numA}-{seed}-{i+1}-{numComp}"
            arq = f"{nomeArq}.txt"

            if valorado:
                matriz = criaMatrizAdjacenciasValorada(
                    dataset, numV, tipo, minPeso, maxPeso
                )
            else:
                matriz = criaMatrizAdjacencias(dataset, numV, tipo)

            listaAdj = criaListaAdjacencias(matriz)

            totalArestas = len(dataset)
            densidade = totalArestas / g_max
            print(f"Densidade (|E|/g_max): {densidade:.3f}")

            escreveMatrizParaArquivo(matriz, listaAdj, arq, numV, numA, seed, i + 1)
            verGrafo(matriz, nomeArq)

        if (
            input("\nDigite 'y' para gerar novamente, qualquer outra tecla para sair: ")
            .strip()
            .lower()
            != "y"
        ):
            break

    print("\nPrograma encerrado.")
    sys.exit(0)
