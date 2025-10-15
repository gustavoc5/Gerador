#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwl import geraGrafoPwl, tipoGrafo
# from distribuicao import validaDistribuicao  # Arquivo não existe
from visualizacao import visualizaGrafo
# from analise import analisa_grafo  # Arquivo não existe
from constants import TIPOS_GRAFOS, GAMMA_MIN, GAMMA_MAX
import random


def main():
    print("Tipo de grafo:")
    for tipo, nome in TIPOS_GRAFOS.items():
        print(f"{tipo}: {nome}")
    
    tipo = int(input("Tipo: "))
    dirigido = tipo in [1, 21, 31]

    numV = int(input("Número de Vértices: "))
    
    seed = input("Semente (Opcional): ").strip()
    seed = int(seed) if seed else random.randint(0, 1000)
    
    gamma_input = input(f"Expoente (gamma) da distribuição (padrão aleatório entre {GAMMA_MIN} e {GAMMA_MAX}): ")
    gamma = float(gamma_input) if gamma_input else round(random.uniform(GAMMA_MIN, GAMMA_MAX), 2)
    
    arestas, G, graus = geraGrafoPwl(numV, gamma, dirigido, tipo, seed)

    print("Número de arestas no grafo final:", G.number_of_edges())
    tipo_detectado = tipoGrafo(G)
    print("Tipo solicitado:", tipo)
    print("Tipo detectado:", tipo_detectado)

    if tipo_detectado != tipo:
        print("⚠️ Atenção: O grafo gerado NÃO corresponde ao tipo solicitado!")
    else:
        print("✅ O grafo gerado corresponde ao tipo solicitado.")

    # validaDistribuicao(graus, gamma)  # Função não existe
    visualizaGrafo(G, dirigido)

    # analise = analisa_grafo(G)  # Função não existe

    # print("\n--- Comunidades ---")
    # print(f"Greedy: {analise['num_coms_greedy']} comunidades | Tam. médio: {analise['tam_medio_greedy']} | Maior: {analise['tam_maior_greedy']}")
    # print(f"LPA   : {analise['num_coms_lpa']} comunidades | Tam. médio: {analise['tam_medio_lpa']} | Maior: {analise['tam_maior_lpa']}")

    # print("\n--- Top‐5 nós por centralidade ---")
    # print(" Degree    :", analise["top5_degree"])
    # print(" PageRank  :", analise["top5_pagerank"])
    # print(" Closeness :", analise["top5_closeness"])


if __name__ == "__main__":
    main()
