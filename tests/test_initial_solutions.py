
import numpy as np
import pytest

from src.algorithms.initial_solutions import generate_initial_routes
from src.algorithms.branch_and_bound import branch_and_bound
from src.tsp.instance import TSPInstance
from src.tsp.distances import build_distance_matrix
from src.tsp.parser import load_tsplib
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


def validate_initial_routes(instance, routes):
    expected_strategies = {
        "cold_start",
        "nearest_neighbor",
        "convex_hull_insertion",
        "twice_around_tree",
        "christofides",
    }

    assert set(routes.keys()) == expected_strategies

    for strategy, route in routes.items():
        assert len(route) == instance.n, strategy
        assert set(route) == set(range(instance.n)), strategy
        assert route[0] == 0, strategy

        # Confirma que a rota possui um custo calculável.
        assert tour_cost(instance, route) >= 0, strategy


def test_generate_initial_routes_square(square_instance):
    routes = generate_initial_routes(square_instance)

    validate_initial_routes(square_instance, routes)


def test_all_warm_starts_are_accepted_by_branch_and_bound(
    square_instance,
):
    routes = generate_initial_routes(square_instance)

    for strategy, initial_route in routes.items():
        result = branch_and_bound(
            square_instance,
            initial_route=initial_route,
        )

        assert result.cost == 14, strategy
        assert result.cost <= tour_cost(
            square_instance,
            initial_route,
        ), strategy

        assert result.timed_out is False, strategy


def test_generate_initial_routes_eil101():
    instance = load_tsplib("data/instances/eil101.tsp")

    routes = generate_initial_routes(instance)

    validate_initial_routes(instance, routes)
