from src.tsp.parser import load_tsplib
from src.tsp.solution import tour_cost
from src.algorithms.nearest_neighbor import nearest_neighbor


def test_nearest_neighbor_eil101():

    instance = load_tsplib("data/instances/eil101.tsp")

    route = nearest_neighbor(instance)

    cost = tour_cost(instance, route)

    print(f"\nInstância: {instance.name}")
    print(f"Quantidade de vértices: {instance.n}")
    print(f"Rota encontrada: {route}")
    print(f"Custo da rota: {cost}")

    assert len(route) == 101
    assert len(set(route)) == 101
    assert 0 <= min(route)
    assert max(route) < 101
    assert cost > 0