
from itertools import permutations

import numpy as np
import pytest

from src.algorithms.branch_and_bound import branch_and_bound
from src.tsp.instance import TSPInstance
from src.tsp.solution import tour_cost


@pytest.fixture
def square_instance():
    coordinates = np.array([
        [0, 0],
        [3, 0],
        [3, 4],
        [0, 4],
    ])

    distances = np.array([
        [0, 3, 5, 4],
        [3, 0, 4, 5],
        [5, 4, 0, 3],
        [4, 5, 3, 0],
    ])

    return TSPInstance(
        name="square",
        coordinates=coordinates,
        distances=distances,
    )


def brute_force(instance):
    """Calcula a solução ótima por força bruta."""

    best_cost = float("inf")

    for ordering in permutations(range(1, instance.n)):
        route = [0] + list(ordering)
        cost = tour_cost(instance, route)

        if cost < best_cost:
            best_cost = cost

    return best_cost


def test_branch_and_bound_finds_optimal_solution(square_instance):
    result = branch_and_bound(square_instance)

    assert result.cost == 14
    assert tour_cost(square_instance, result.route) == 14
    assert result.route[0] == 0
    assert result.timed_out is False


def test_branch_and_bound_matches_brute_force(square_instance):
    result = branch_and_bound(square_instance)

    optimal_cost = brute_force(square_instance)

    assert result.cost == optimal_cost


def test_branch_and_bound_improves_initial_route(square_instance):
    initial_route = [0, 2, 1, 3]

    result = branch_and_bound(
        square_instance,
        initial_route=initial_route,
    )

    assert result.cost == 14
    assert result.cost <= tour_cost(
        square_instance,
        initial_route,
    )


def test_branch_and_bound_accepts_rotated_initial_route(square_instance):
    initial_route = [2, 1, 3, 0]

    result = branch_and_bound(
        square_instance,
        initial_route=initial_route,
    )

    assert result.route[0] == 0
    assert result.cost == 14


def test_branch_and_bound_timeout(square_instance):
    result = branch_and_bound(
        square_instance,
        time_limit_seconds=0,
    )

    assert result.timed_out is True
    assert result.cost == tour_cost(
        square_instance,
        result.route,
    )
    assert result.route[0] == 0


def test_branch_and_bound_invalid_initial_route(square_instance):
    with pytest.raises(ValueError):
        branch_and_bound(
            square_instance,
            initial_route=[0, 1, 2],
        )


def test_branch_and_bound_repeated_initial_vertex(square_instance):
    with pytest.raises(ValueError):
        branch_and_bound(
            square_instance,
            initial_route=[0, 1, 1, 3],
        )


def test_branch_and_bound_invalid_time_limit(square_instance):
    with pytest.raises(ValueError):
        branch_and_bound(
            square_instance,
            time_limit_seconds=-1,
        )
