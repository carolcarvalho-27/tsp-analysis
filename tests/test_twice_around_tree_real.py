
from src.tsp.parser import load_tsplib
from src.tsp.solution import tour_cost
from src.algorithms.mst import minimum_spanning_tree
from src.algorithms.twice_around_tree import twice_around_tree


def test_twice_around_tree_eil101():

    instance = load_tsplib("data/instances/eil101.tsp")

    mst = minimum_spanning_tree(instance)
    route = twice_around_tree(instance)
    cost = tour_cost(instance, route)

    mst_cost = sum(
        data["weight"]
        for _, _, data in mst.edges(data=True)
    )

    print(f"\nInstância: {instance.name}")
    print(f"Quantidade de vértices: {instance.n}")
    print(f"Custo da MST: {mst_cost}")
    print(f"Custo da rota: {cost}")
    print(f"Rota encontrada: {route}")

    assert len(route) == instance.n
    assert len(set(route)) == instance.n
    assert route[0] == 0
    assert cost > 0
