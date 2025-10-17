#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from igraph import Graph, plot


def verGrafo(matriz, nomeArq):
    n = len(matriz)

    # Detectar se é dirigido
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

    # Construir listas de arestas e pesos
    edges = []
    weights = []
    for i in range(n):
        for j in range(n):
            cell = matriz[i][j]
            if isinstance(cell, list):
                for peso in cell:
                    edges.append((i, j))
                    weights.append(peso)
            elif cell > 0:
                edges.append((i, j))
                weights.append(cell)

    # Criar o grafo no igraph
    g = Graph(directed=dirigido)
    g.add_vertices(n)
    g.add_edges(edges)
    g.es["weight"] = weights
    g.es["label"] = weights
    g.vs["label"] = g.vs.indices

    # Layout e plotagem
    layout = g.layout("kk")  # Kamada-Kawai
    plot(
        g,
        bbox=(600, 600),
        layout=layout,
        edge_arrow_size=0.8,
        vertex_label_size=14,
        edge_label=g.es["label"],
        target=f"../plots/{nomeArq}.png",
    )
