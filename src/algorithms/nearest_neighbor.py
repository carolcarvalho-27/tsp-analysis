
from src.tsp.instance import TSPInstance


def nearest_neighbor(
    instance: TSPInstance,
    start: int = 0
) -> list[int]:
    """
    Constrói uma rota TSP utilizando a heurística
    Nearest Neighbor.

    Parâmetros:
        instance: instância do problema TSP.
        start: índice do vértice inicial (0 até n-1).

    Retorna:
        Lista com os índices dos vértices visitados,
        sem repetir o vértice inicial no final.
    """

    if not 0 <= start < instance.n:
        raise ValueError("Vértice inicial inválido.")

    route = [start]
    visited = [False] * instance.n
    visited[start] = True

    current = start

    while len(route) < instance.n:

        nearest = None
        min_distance = float("inf")

        for vertex in range(instance.n):

            if not visited[vertex]:

                distance = instance.distance(current, vertex)

                if distance < min_distance:
                    min_distance = distance
                    nearest = vertex

        route.append(nearest)
        visited[nearest] = True
        current = nearest

    return route
