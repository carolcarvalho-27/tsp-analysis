
import networkx as nx

from src.tsp.instance import TSPInstance
from src.algorithms.mst import (
    build_complete_graph,
    minimum_spanning_tree
)


def find_odd_degree_vertices(mst: nx.Graph) -> list[int]:
    """
    Retorna os vértices de grau ímpar da MST.
    """

    return [
        vertex
        for vertex, degree in mst.degree()
        if degree % 2 == 1
    ]


def minimum_weight_perfect_matching(
    instance: TSPInstance,
    odd_vertices: list[int]
) -> set[tuple[int, int]]:
    """
    Calcula um matching perfeito de peso mínimo
    entre os vértices fornecidos.

    Cada vértice deve aparecer em exatamente uma aresta.
    """

    if len(odd_vertices) % 2 != 0:
        raise ValueError(
            "A quantidade de vértices deve ser par."
        )

    if len(set(odd_vertices)) != len(odd_vertices):
        raise ValueError(
            "A lista contém vértices repetidos."
        )

    if any(
        vertex < 0 or vertex >= instance.n
        for vertex in odd_vertices
    ):
        raise ValueError("Vértice inválido no matching.")

    if not odd_vertices:
        return set()

    complete_graph = build_complete_graph(instance)

    odd_graph = complete_graph.subgraph(odd_vertices).copy()

    matching = nx.min_weight_matching(
        odd_graph,
        weight="weight"
    )

    return matching


def christofides(
    instance: TSPInstance,
    start: int = 0
) -> list[int]:
    """
    Constrói uma rota TSP utilizando o algoritmo de Christofides.

    Etapas:
    1. Calcula a MST.
    2. Identifica os vértices de grau ímpar.
    3. Calcula um matching perfeito de peso mínimo.
    4. Constrói um multigrafo e encontra um circuito euleriano.
    5. Aplica shortcutting.

    Retorna uma rota sem repetir o vértice inicial no final.
    """

    if not 0 <= start < instance.n:
        raise ValueError("Vértice inicial inválido.")

    if instance.n == 1:
        return [start]

    # 1. Construção da MST
    mst = minimum_spanning_tree(instance)

    # 2. Identificação dos vértices de grau ímpar
    odd_vertices = find_odd_degree_vertices(mst)

    # 3. Matching perfeito de peso mínimo
    matching = minimum_weight_perfect_matching(
        instance,
        odd_vertices
    )

    # 4. Construção do multigrafo
    multigraph = nx.MultiGraph()
    multigraph.add_nodes_from(mst.nodes())

    # Adiciona as arestas da MST
    for u, v, data in mst.edges(data=True):
        multigraph.add_edge(u, v, weight=data["weight"])

    # Adiciona as arestas do matching
    for u, v in matching:
        multigraph.add_edge(
            u,
            v,
            weight=instance.distance(u, v)
        )

    # Verifica se o multigrafo é euleriano
    if not nx.is_eulerian(multigraph):
        raise RuntimeError(
            "O multigrafo construído não é euleriano."
        )

    eulerian_circuit = nx.eulerian_circuit(
        multigraph,
        source=start
    )

    eulerian_walk = [start]

    for u, v in eulerian_circuit:
        eulerian_walk.append(v)

    # 5. Shortcutting
    route = []
    visited = set()

    for vertex in eulerian_walk:
        if vertex not in visited:
            route.append(vertex)
            visited.add(vertex)

    return route
