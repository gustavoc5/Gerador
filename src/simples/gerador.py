import random
import math
import numpy as np
import sys
from utils import tipoGrafo, compConexas

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