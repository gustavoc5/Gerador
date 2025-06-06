from gerador import geraDataset, verificaAresta
from utils import (
    criaMatrizAdjacencias,
    criaMatrizAdjacenciasValorada,
    criaListaAdjacencias,
    escreveMatrizParaArquivo,
)
from visualizacao import verGrafo
import random
import math
import sys

def main():
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

        numComp = input("Número de componentes conexas (padrão 0): ").strip()
        numComp = int(numComp) if numComp else 0

        print("\nPreferência de densidade:")
        print("  0: Sem preferência")
        print("  1: Esparso (densidade ≤ 0.2)")
        print("  2: Denso   (densidade ≥ 0.8)")
        densPref = int(input("Escolha [0/1/2] (padrão 0): ") or 0)

        valorado = input("O grafo será valorado? (y/n): ").strip().lower() == "y"
        if valorado:
            minPeso = input("Peso mínimo das arestas (padrão = 1): ").strip()
            maxPeso = input("Peso máximo das arestas (padrão = 10): ").strip()
            minPeso = int(minPeso) if minPeso.isdigit() else 1
            maxPeso = int(maxPeso) if maxPeso.isdigit() else 10

        minA, maxA = verificaAresta(tipo, numV, numComp)

        if tipo == 0 or tipo == 20:
            g_max = numV * (numV - 1) / 2
        elif tipo == 1 or tipo == 21:
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

        if highA is None:
            print(f"\nO número de arestas deve ser ≥ {lowA}.")
        else:
            print(f"\nO número de arestas deve estar entre {lowA} e {highA}.")

        numA = int(input("Número de Arestas: "))
        if numA < lowA or (highA is not None and numA > highA):
            raise ValueError(f"Número de arestas {numA} fora do intervalo [{lowA},{highA or '∞'}]")

        seed = input("Semente (Não obrigatório): ").strip()
        seed = int(seed) if seed else random.randint(0, 1000)
        n = input("Número de datasets: ").strip()
        n = int(n) if n else 1
        if numComp > 1:
            fator = input("0-Aleatório 1-Parcial 2-Balanceado: ").strip()
            fator = int(fator) if fator else random.randint(0, 2)
        else:
            fator = 0

        datasets = geraDataset(tipo, numV, numA, seed, n, numComp, fator)
        
        for i, dataset in enumerate(datasets):
            nomeArq = f"{tipos[tipo]}-{geracao[fator][0]}-{numV}-{numA}-{seed}-{i+1}-{numComp}"
            arq = f"../plots/{nomeArq}.txt"

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

        if input("\nDigite 'y' para gerar novamente, qualquer outra tecla para sair: ").strip().lower() != "y":
            break

    print("\nPrograma encerrado.")
    sys.exit(0)

if __name__ == "__main__":
    main()
