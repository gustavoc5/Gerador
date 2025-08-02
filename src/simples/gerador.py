import random
import math
import numpy as np
from constants import (
    TIPOS_DIRIGIDOS, TIPOS_MULTIGRAFOS, TIPOS_PSEUDOGRAFOS,
    MAX_TENTATIVAS
)
from exceptions import (
    ParametrosInvalidosError, TentativasExcedidasError,
    ArestasInsuficientesError, ComponentesInvalidasError
)
from utils import tipoGrafo, compConexas


def verificaAresta(tipo, numV, numC):
    """Verifica se os parâmetros de arestas são válidos."""
    if numV - (numC - 1) <= 0:
        raise ComponentesInvalidasError("Número de vértices e componentes conexas inválido")

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
    else:
        raise ParametrosInvalidosError(f"Tipo de grafo inválido: {tipo}")
    
    return minimo, maximo


def alocaVertices(numV, numC, fator):
    """Aloca vértices para componentes baseado no fator."""
    verticesComp = [0] * numC
    
    if fator == 2:  # Balanceado
        resto = numV % numC
        vert = numV // numC
        verticesComp = [vert] * numC
        verticesComp[0] += resto
    else:  # Aleatório ou Parcialmente Balanceado
        for _ in range(numV):
            component = random.randint(0, numC - 1)
            verticesComp[component] += 1
    
    return verticesComp


def calculaLimitesArestas(verticesComp, tipo):
    """Calcula limites mínimo e máximo de arestas para cada componente."""
    minArestas = [0] * len(verticesComp)
    maxArestas = [0] * len(verticesComp)
    
    for i, numVertices in enumerate(verticesComp):
        if tipo == 0:  # Simples
            minArestas[i] = numVertices - 1
            maxArestas[i] = (numVertices * (numVertices - 1)) / 2
        elif tipo == 1:  # Dirigido
            minArestas[i] = numVertices - 1
            maxArestas[i] = numVertices * (numVertices - 1)
        elif "2" in str(tipo):  # Multigrafo
            if numVertices == 1:
                minArestas[i] = 0
                maxArestas[i] = 0
            else:
                minArestas[i] = numVertices
                maxArestas[i] = math.inf
        elif "3" in str(tipo):  # Pseudografo
            minArestas[i] = numVertices
            maxArestas[i] = math.inf
    
    return minArestas, maxArestas


def alocaArestasBalanceado(numA, numC, minArestas, maxArestas):
    """Aloca arestas de forma balanceada entre componentes."""
    resto = numA % numC
    arest = numA // numC
    arestasComp = [arest] * numC
    arestasComp[0] += resto
    
    # Valida se é possível
    for i in range(numC):
        if minArestas[i] > arestasComp[i]:
            raise ArestasInsuficientesError(
                "Não é possível gerar um grafo balanceado com esse número de arestas, considere aumentar"
            )
        elif maxArestas[i] < arestasComp[i]:
            raise ArestasInsuficientesError(
                "Não é possível gerar um grafo balanceado com esse número de arestas, considere diminuir"
            )
    
    return arestasComp


def alocaArestasAleatorio(numA, numC, minArestas, maxArestas):
    """Aloca arestas de forma aleatória entre componentes."""
    arestasComp = [0] * numC
    arestasRestantes = numA
    
    for i in range(numC - 1):
        if minArestas[i] < maxArestas[i]:
            try:
                max_possivel = min(
                    maxArestas[i],
                    arestasRestantes - sum(
                        min(minArestas[j], maxArestas[j])
                        for j in range(i + 1, numC)
                    )
                )
                arestasComp[i] = random.randint(minArestas[i], int(max_possivel))
            except ValueError as e:
                raise ArestasInsuficientesError(
                    f"Erro ao gerar valor aleatório para arestasComp[{i}]: {e}"
                )
        arestasRestantes -= arestasComp[i]
    
    # Última componente recebe o restante
    arestasComp[numC - 1] = numA - sum(arestasComp)
    
    # Valida última componente
    if (arestasComp[numC - 1] < minArestas[numC - 1] or 
        arestasComp[numC - 1] > maxArestas[numC - 1]):
        return None  # Indica que deve tentar novamente
    
    return arestasComp


def constroiComponentes(verticesComp, arestasComp, tipo, numV):
    """Constrói as componentes do grafo."""
    numC = len(verticesComp)
    
    # Calcula tamanhos acumulados
    tam = [0] * (numC + 1)
    for j in range(1, numC):
        tam[j] = tam[j - 1] + verticesComp[j - 1]
    tam[numC] = numV
    
    # Constrói matriz de adjacência
    matriz = np.array([[0] * numV for _ in range(numV)])
    arestas = []
    
    for i in range(numC):
        # Lista de vértices da componente atual
        vertices = list(range(tam[i], tam[i + 1]))
        random.shuffle(vertices)
        
        # Conecta vértices da componente
        for j in range(len(vertices) - 1):
            u, v = vertices[j], vertices[j + 1]
            if tipo in [0, 20, 30]:  # Grafo simples
                arestas.append((u, v))
                matriz[u][v] += 1
                matriz[v][u] += 1
            else:  # Grafo dirigido
                arestas.append((u, v))
                matriz[u][v] += 1
        
        # Adiciona arestas extras se necessário
        arestas_necessarias = arestasComp[i] - (len(vertices) - 1)
        for _ in range(arestas_necessarias):
            u = random.choice(vertices)
            v = random.choice(vertices)
            if u != v or tipo in TIPOS_PSEUDOGRAFOS:
                if tipo in [0, 20, 30]:  # Simples
                    arestas.append((min(u, v), max(u, v)))
                    matriz[u][v] += 1
                    matriz[v][u] += 1
                else:  # Dirigido
                    arestas.append((u, v))
                    matriz[u][v] += 1
    
    return arestas


def geraComponente(tipo, numV, numA, numC, fator):
    """Gera uma componente do grafo."""
    tentativas = 0
    
    while tentativas < MAX_TENTATIVAS:
        # Aloca vértices
        verticesComp = alocaVertices(numV, numC, fator)
        if not all(verticesComp):
            tentativas += 1
            continue
        
        # Calcula limites de arestas
        minArestas, maxArestas = calculaLimitesArestas(verticesComp, tipo)
        
        # Aloca arestas
        if fator == 2:  # Balanceado
            try:
                arestasComp = alocaArestasBalanceado(numA, numC, minArestas, maxArestas)
            except ArestasInsuficientesError:
                tentativas += 1
                continue
        else:  # Aleatório ou Parcialmente Balanceado
            arestasComp = alocaArestasAleatorio(numA, numC, minArestas, maxArestas)
            if arestasComp is None:
                tentativas += 1
                continue
        
        # Ordena se parcialmente balanceado
        if fator == 1:
            verticesComp = sorted(verticesComp)
            arestasComp = sorted(arestasComp)
        
        # Constrói componentes
        try:
            arestas = constroiComponentes(verticesComp, arestasComp, tipo, numV)
            return arestas
        except Exception:
            tentativas += 1
            continue
    
    return None


def geraGrafoSimples(numV, numA):
    """Gera grafo simples."""
    if numA > numV * (numV - 1) / 2:
        raise ArestasInsuficientesError(
            "Número de arestas excede o máximo permitido para um grafo simples."
        )
    
    arestas = []
    while len(arestas) < numA:
        u = random.randint(0, numV - 1)
        v = random.randint(0, numV - 1)
        if u != v and (u, v) not in arestas and (v, u) not in arestas:
            aresta = (min(u, v), max(u, v))
            arestas.append(aresta)
    
    return arestas


def geraGrafoDirigido(numV, numA):
    """Gera grafo dirigido."""
    if numA > numV * (numV - 1):
        raise ArestasInsuficientesError(
            "Número de arestas excede o máximo permitido para um digrafo."
        )
    
    arestas = []
    while len(arestas) < numA:
        u = random.randint(0, numV - 1)
        v = random.randint(0, numV - 1)
        if u != v and (u, v) not in arestas:
            aresta = (u, v)
            arestas.append(aresta)
    
    return arestas


def geraMultigrafo(numV, numA, dirigido=False):
    """Gera multigrafo simples ou dirigido."""
    arestas = []
    
    # Gera arestas normais
    while len(arestas) < numA - 1:
        u = random.randint(0, numV - 1)
        v = random.randint(0, numV - 1)
        if u != v:
            if dirigido:
                aresta = (u, v)
            else:
                aresta = (min(u, v), max(u, v))
            arestas.append(aresta)
    
    # Garante que há pelo menos uma aresta múltipla
    if len(set(arestas)) == len(arestas):
        aresta_existente = random.choice(arestas)
        arestas.append(aresta_existente)
    
    return arestas


def geraPseudografo(numV, numA, dirigido=False):
    """Gera pseudografo simples ou dirigido."""
    arestas = []
    loop = False
    
    # Gera arestas normais
    while len(arestas) < numA - 1:
        u = random.randint(0, numV - 1)
        v = random.randint(0, numV - 1)
        if dirigido:
            aresta = (u, v)
        else:
            aresta = (min(u, v), max(u, v))
        arestas.append(aresta)
        if u == v:
            loop = True
    
    # Garante que há pelo menos um laço
    if not loop:
        u = random.randint(0, numV - 1)
        arestas.append((u, u))
    
    return arestas


def geraDataset(tipo, numV, numA, seed, n, numC, fator):
    """Função principal para gerar datasets de grafos."""
    random.seed(seed)
    datasets = []
    
    if numC > 0:
        # Geração com múltiplas componentes
        tentativas = 0
        while len(datasets) != n and tentativas < MAX_TENTATIVAS:
            tentativas += 1
            grafo = geraComponente(tipo, numV, numA, numC, fator)
            if grafo is not None:
                datasets.append(sorted(list(grafo)))
                tentativas = 0
            else:
                continue
        
        if tentativas >= MAX_TENTATIVAS:
            raise TentativasExcedidasError(
                "Número máximo de tentativas atingido. Considere alterar parâmetros."
            )
    else:
        # Geração de grafo conexo
        for _ in range(n):
            if tipo == 0:
                arestas = geraGrafoSimples(numV, numA)
            elif tipo == 1:
                arestas = geraGrafoDirigido(numV, numA)
            elif tipo == 20:
                arestas = geraMultigrafo(numV, numA, dirigido=False)
            elif tipo == 21:
                arestas = geraMultigrafo(numV, numA, dirigido=True)
            elif tipo == 30:
                arestas = geraPseudografo(numV, numA, dirigido=False)
            elif tipo == 31:
                arestas = geraPseudografo(numV, numA, dirigido=True)
            else:
                raise ParametrosInvalidosError(f"Tipo de grafo inválido: {tipo}")
            
            datasets.append(sorted(list(arestas)))
    
    return datasets