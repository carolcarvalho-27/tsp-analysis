
import networkx as nx

from src.tsp.instance import TSPInstance


def build_complete_graph(instance: TSPInstance) -> nx.Graph:
    """
    Constrói o grafo completo ponderado da instância TSP.

    Cada vértice representa uma cidade e cada aresta
    possui como peso a distância entre duas cidades.
    """

    graph = nx.Graph()

    graph.add_nodes_from(range(instance.n))

    for i in range(instance.n):
        for j in range(i + 1, instance.n):
            graph.add_edge(
                i,
                j,
                weight=instance.distance(i, j)
            )

    return graph


def minimum_spanning_tree(instance: TSPInstance) -> nx.Graph:
    """
    Calcula uma Árvore Geradora Mínima usando Kruskal.
    """

    graph = build_complete_graph(instance)

    return nx.minimum_spanning_tree(
        graph,
        algorithm="kruskal",
        weight="weight"
    )
