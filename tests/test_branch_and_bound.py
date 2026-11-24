
from itertools import permutations


import pytest

from src.algorithms.branch_and_bound import (
    mst_cost,
    completion_lower_bound,
    branch_and_bound,
)

from src.tsp.instance import TSPInstance
from src.tsp.solution import tour_cost

@pytest.fixture
def square_instance():
    coordinates = [
        [0, 0],
        [3, 0],
        [3, 4],
        [0, 4],
    ]

    distances = [
        [0, 3, 5, 4],
        [3, 0, 4, 5],
        [5, 4, 0, 3],
        [4, 5, 3, 0],
    ]

    import numpy as np

    return TSPInstance(
        name="square",
        coordinates=np.array(coordinates),
        distances=np.array(distances),
    )


def calculate_partial_path_cost(instance, route):
    """Calcula somente o custo das arestas já percorridas."""
    total = 0

    for i in range(len(route) - 1):
        total += instance.distance(route[i], route[i + 1])

    return total


def calculate_completion_cost(instance, route):
    """Calcula o custo de um ciclo completo."""
    total = calculate_partial_path_cost(instance, route)

    if len(route) > 0:
        total += instance.distance(route[-1], route[0])

    return total


def test_mst_cost(square_instance):
    assert mst_cost(square_instance, [1, 2, 3]) == 7


def test_mst_cost_empty_vertices(square_instance):
    assert mst_cost(square_instance, []) == 0


def test_mst_cost_single_vertex(square_instance):
    assert mst_cost(square_instance, [1]) == 0


def test_mst_cost_repeated_vertices(square_instance):
    with pytest.raises(ValueError):
        mst_cost(square_instance, [1, 1])


def test_mst_cost_invalid_vertex(square_instance):
    with pytest.raises(ValueError):
        mst_cost(square_instance, [1, 4])


def test_lower_bound_initial_route(square_instance):
    assert completion_lower_bound(square_instance, [0], 0) == 13


def test_lower_bound_partial_route(square_instance):
    assert completion_lower_bound(square_instance, [0, 1], 3) == 14


def test_lower_bound_complete_route(square_instance):
    assert completion_lower_bound(
        square_instance,
        [0, 1, 2, 3],
        10,
    ) == 14


def test_lower_bound_admissibility(square_instance):
    """
    Verifica se o limite inferior nunca ultrapassa
    o custo da melhor conclusão possível.

    São examinados todos os prefixos possíveis
    das rotas que começam no vértice 0.
    """

    vertices = [1, 2, 3]

    for ordering in permutations(vertices):

        complete_route = [0] + list(ordering)

        for prefix_length in range(1, 5):

            partial_route = complete_route[:prefix_length]

            current_cost = calculate_partial_path_cost(
                square_instance,
                partial_route,
            )

            bound = completion_lower_bound(
                square_instance,
                partial_route,
                current_cost,
            )

            remaining = [
                vertex
                for vertex in range(square_instance.n)
                if vertex not in partial_route
            ]

            possible_completion_costs = []

            for ordering_remaining in permutations(remaining):

                completed_route = (
                    partial_route + list(ordering_remaining)
                )

                possible_completion_costs.append(
                    calculate_completion_cost(
                        square_instance,
                        completed_route,
                    )
                )

            best_completion = min(possible_completion_costs)

            assert bound <= best_completion


def test_lower_bound_invalid_empty_route(square_instance):
    with pytest.raises(ValueError):
        completion_lower_bound(square_instance, [], 0)


def test_lower_bound_invalid_start(square_instance):
    with pytest.raises(ValueError):
        completion_lower_bound(square_instance, [1, 2], 3)


def test_lower_bound_repeated_vertices(square_instance):
    with pytest.raises(ValueError):
        completion_lower_bound(square_instance, [0, 1, 1], 6)


def test_lower_bound_invalid_vertex(square_instance):
    with pytest.raises(ValueError):
        completion_lower_bound(square_instance, [0, 4], 3)


def test_lower_bound_negative_cost(square_instance):
    with pytest.raises(ValueError):
        completion_lower_bound(square_instance, [0], -1)

def test_branch_and_bound_finds_optimal_solution(square_instance):
    # Rota inicial que utiliza as duas diagonais.
    initial_route = [0, 2, 1, 3]

    initial_cost = tour_cost(square_instance, initial_route)

    assert initial_cost == 18

    result = branch_and_bound(
        square_instance,
        initial_route=initial_route,
        time_limit_seconds=5,
    )

    assert not result.timed_out
    assert result.cost == 14
    assert result.cost <= initial_cost


def test_branch_and_bound_returns_valid_route(square_instance):
    result = branch_and_bound(
        square_instance,
        time_limit_seconds=5,
    )

    assert len(result.route) == square_instance.n
    assert set(result.route) == set(range(square_instance.n))

    calculated_cost = tour_cost(
        square_instance,
        result.route,
    )

    assert calculated_cost == result.cost


def test_branch_and_bound_does_not_worsen_initial_solution(
    square_instance,
):
    initial_route = [0, 2, 1, 3]
    initial_cost = tour_cost(square_instance, initial_route)

    result = branch_and_bound(
        square_instance,
        initial_route=initial_route,
        time_limit_seconds=5,
    )

    assert result.cost <= initial_cost

def test_branch_and_bound_matches_brute_force():
    import numpy as np

    distances = np.array([
        [0, 2, 9, 10, 7],
        [2, 0, 6, 4, 3],
        [9, 6, 0, 8, 5],
        [10, 4, 8, 0, 6],
        [7, 3, 5, 6, 0],
    ])

    instance = TSPInstance(
        name="non_metric_test",
        coordinates=None,
        distances=distances,
    )

    # Calcula o ótimo por busca exaustiva.
    possible_costs = []

    for ordering in permutations(range(1, instance.n)):
        route = [0] + list(ordering)
        possible_costs.append(
            calculate_completion_cost(instance, route)
        )

    brute_force_optimum = min(possible_costs)

    # Executa o Branch-and-Bound.
    result = branch_and_bound(
        instance,
        time_limit_seconds=5,
    )

    assert not result.timed_out
    assert result.cost == brute_force_optimum