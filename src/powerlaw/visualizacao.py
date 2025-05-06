import matplotlib.pyplot as plt
import networkx as nx


def visualizaGrafo(G, dirigido=False):
    num_nos = G.number_of_nodes()

    if num_nos > 300:
        print("⚠️ Grafo muito grande — visualização ignorada.")
        return

    plt.figure(figsize=(10, 8))

    if num_nos <= 100:
        pos = nx.spring_layout(G, seed=42)
    else:
        pos = nx.kamada_kawai_layout(G)

    nx.draw_networkx_nodes(G, pos, node_size=50, node_color="skyblue")
    nx.draw_networkx_edges(G, pos, alpha=0.4, arrows=dirigido)

    plt.title("Visualização do Grafo Gerado")
    plt.axis("off")
    plt.show()
