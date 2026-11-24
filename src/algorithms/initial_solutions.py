
from src.tsp.instance import TSPInstance

from src.algorithms.nearest_neighbor import nearest_neighbor
from src.algorithms.convex_hull_insertion import convex_hull_insertion
from src.algorithms.twice_around_tree import twice_around_tree
from src.algorithms.christofides import christofides


def generate_initial_routes(
    instance: TSPInstance,
) -> dict[str, list[int]]:
    """
    Gera soluções iniciais para as estratégias de warm-start.

    Estratégias:
        cold_start:
            Rota trivial na ordem dos índices.

        nearest_neighbor:
            Algoritmo do vizinho mais próximo.

        convex_hull_insertion:
            Inserção baseada no fecho convexo.
            Disponível somente quando existem coordenadas.

        twice_around_tree:
            Algoritmo Twice-around-the-tree.

        christofides:
            Algoritmo de Christofides.

    Todas as rotas começam no vértice 0.
    """

    if instance.n < 1:
        raise ValueError("A instância deve ter pelo menos um vértice.")

    routes = {
        "cold_start": list(range(instance.n)),
        "nearest_neighbor": nearest_neighbor(instance, start=0),
        "twice_around_tree": twice_around_tree(
            instance,
            start=0,
        ),
        "christofides": christofides(
            instance,
            start=0,
        ),
    }

    # O fecho convexo depende da existência de coordenadas.
    if instance.coordinates is not None:
        routes["convex_hull_insertion"] = convex_hull_insertion(
            instance,
            start=0,
        )

    return routes
