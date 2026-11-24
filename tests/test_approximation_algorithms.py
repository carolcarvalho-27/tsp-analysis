
import numpy as np
import pytest

from src.tsp.instance import TSPInstance
from src.tsp.solution import tour_cost
from src.algorithms.twice_around_tree import twice_around_tree
from src.algorithms.christofides import christofides


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


@pytest.mark.parametrize(
    "algorithm, approximation_factor",
    [
        (twice_around_tree, 2.0),
        (christofides, 1.5),
    ],
)
def test_approximation_algorithm_guarantee(
    square_instance,
    algorithm,
    approximation_factor,
):
    optimal_cost = 14

    route = algorithm(square_instance)

    assert len(route) == square_instance.n
    assert set(route) == set(range(square_instance.n))

    cost = tour_cost(square_instance, route)

    assert cost <= approximation_factor * optimal_cost
