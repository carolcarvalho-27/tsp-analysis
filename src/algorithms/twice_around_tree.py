
import networkx as nx

from src.tsp.instance import TSPInstance
from src.algorithms.mst import minimum_spanning_tree


def twice_around_tree(
    instance: TSPInstance,
    start: int = 0
) -> list[int]:
    """
    Constrói uma rota TSP utilizando a heurística
    Twice-around-the-tree.

    Etapas:
    1. Calcula a MST.
    2. Duplica suas arestas.
    3. Encontra um circuito euleriano.
    4. Remove as visitas repetidas (shortcutting).

    Retorna uma rota sem repetir o vértice inicial no final.
    """

    if not 0 <= start < instance.n:
        raise ValueError("Vértice inicial inválido.")

    if instance.n == 1:
        return [start]

    # 1. Construção da MST
    mst = minimum_spanning_tree(instance)

    # 2. Duplicação das arestas
    multigraph = nx.MultiGraph()
    multigraph.add_nodes_from(mst.nodes())

    for u, v, data in mst.edges(data=True):
        multigraph.add_edge(u, v, weight=data["weight"])
        multigraph.add_edge(u, v, weight=data["weight"])

    # 3. Construção do circuito euleriano
    eulerian_circuit = nx.eulerian_circuit(
        multigraph,
        source=start
    )

    eulerian_walk = [start]

    for u, v in eulerian_circuit:
        eulerian_walk.append(v)

    # 4. Shortcutting: manter somente a primeira visita
    route = []
    visited = set()

    for vertex in eulerian_walk:
        if vertex not in visited:
            route.append(vertex)
            visited.add(vertex)

    return route
