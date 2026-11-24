from collections.abc import Sequence

from src.tsp.instance import TSPInstance


def tour_cost(instance: TSPInstance, route: Sequence[int]) -> int:
    """
    Calcula o custo total de uma rota, incluindo o retorno
    do último vértice ao primeiro.

    A rota deve conter cada vértice exatamente uma vez,
    utilizando índices de 0 até n-1.
    """

    if len(route) != instance.n:
        raise ValueError(
            "A rota deve conter exatamente n vértices."
        )

    if set(route) != set(range(instance.n)):
        raise ValueError(
            "A rota deve conter todos os vértices exatamente uma vez."
        )

    total_cost = 0

    for i in range(instance.n):
        current = route[i]
        next_vertex = route[(i + 1) % instance.n]

        total_cost += instance.distance(current, next_vertex)

    return total_cost