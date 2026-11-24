
from src.tsp.parser import load_tsplib
from src.tsp.solution import tour_cost
from src.algorithms.mst import minimum_spanning_tree
from src.algorithms.christofides import (
    find_odd_degree_vertices,
    minimum_weight_perfect_matching,
    christofides
)


def test_christofides_eil101():

    instance = load_tsplib("data/instances/eil101.tsp")

    mst = minimum_spanning_tree(instance)

    odd_vertices = find_odd_degree_vertices(mst)

    matching = minimum_weight_perfect_matching(
        instance,
        odd_vertices
    )

    route = christofides(instance)

    mst_cost = sum(
        data["weight"]
        for _, _, data in mst.edges(data=True)
    )

    matching_cost = sum(
        instance.distance(u, v)
        for u, v in matching
    )

    route_cost = tour_cost(instance, route)

    print(f"\nInstância: {instance.name}")
    print(f"Quantidade de vértices: {instance.n}")
    print(f"Custo da MST: {mst_cost}")
    print(f"Quantidade de vértices ímpares: {len(odd_vertices)}")
    print(f"Custo do matching: {matching_cost}")
    print(f"Custo da rota: {route_cost}")
    print(f"Rota encontrada: {route}")

    assert len(odd_vertices) % 2 == 0
    assert len(matching) == len(odd_vertices) // 2
    assert len(route) == instance.n
    assert len(set(route)) == instance.n
    assert route[0] == 0
    assert route_cost > 0
