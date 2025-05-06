import math
import random
import sys
from gerador import geraDataset
from utils import (
    criaMatrizAdjacencias,
    criaMatrizAdjacenciasValorada,
    criaListaAdjacencias,
    escreveMatrizParaArquivo,
    verGrafo,
)

def prompt_usuario():
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

        numComp = int(input("Número de componentes conexas (padrão 0): ") or 0)

        print("\nPreferência de densidade:")
        print("  0: Sem preferência")
        print("  1: Esparso (densidade ≤ 0.2)")
        print("  2: Denso   (densidade ≥ 0.8)")
        densPref = int(input("Escolha [0/1/2] (padrão 0): ") or 0)

        valorado = input("O grafo será valorado? (y/n): ").strip().lower() == "y"
        if valorado:
            minPeso = int(input("Peso mínimo das arestas (padrão = 1): ") or 1)
            maxPeso = int(input("Peso máximo das arestas (padrão = 10): ") or 10)

        from gerador import verificaAresta
        minA, maxA = verificaAresta(tipo, numV, numComp)

        if tipo in (0, 20):
            g_max = numV * (numV - 1) / 2
        elif tipo in (1, 21):
            g_max = numV * (numV - 1)
        elif tipo == 30:
            g_max = numV * (numV - 1) / 2 + numV
        elif tipo == 31:
            g_max = numV * (numV - 1) + numV

        if densPref == 1:
            lowA = minA
            highA = int(0.2 * g_max)
        elif densPref == 2:
            lowA = int(0.8 * g_max)
            highA = int(g_max)
        else:
            lowA = minA
            highA = None if math.isinf(maxA) else int(maxA)

        print(f"\nO número de arestas deve estar entre {lowA} e {highA or '∞'}.")
        numA = int(input("Número de Arestas: "))
        if numA < lowA or (highA is not None and numA > highA):
            raise ValueError(f"Valor inválido de arestas.")

        seed = int(input("Semente (opcional): ") or random.randint(0, 1000))
        n = int(input("Número de datasets: ") or 1)
        fator = int(input("0-Aleatório 1-Parcial 2-Balanceado: ") or random.randint(0, 2))

        datasets = geraDataset(tipo, numV, numA, seed, n, numComp, fator)

        for i, dataset in enumerate(datasets):
            nomeArq = f"{tipos[tipo]}-{geracao[fator][0]}-{numV}-{numA}-{seed}-{i+1}-{numComp}"
            arq = f"plots/{nomeArq}.txt"

            if valorado:
                matriz = criaMatrizAdjacenciasValorada(dataset, numV, tipo, minPeso, maxPeso)
            else:
                matriz = criaMatrizAdjacencias(dataset, numV, tipo)

            listaAdj = criaListaAdjacencias(matriz)

            totalArestas = len(dataset)
            densidade = totalArestas / g_max
            print(f"Densidade (|E|/g_max): {densidade:.3f}")

            escreveMatrizParaArquivo(matriz, listaAdj, arq, numV, numA, seed, i + 1)
            verGrafo(matriz, nomeArq)

        if input("\nDigite 'y' para gerar novamente, outra tecla para sair: ").lower() != "y":
            break
    print("Programa encerrado.")
    sys.exit(0)
