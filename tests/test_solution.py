import numpy as np
import pytest

from src.tsp.instance import TSPInstance
from src.tsp.solution import tour_cost


def test_tour_cost():
    coordinates = np.array([
        [0, 0],
        [3, 0],
        [3, 4],
        [0, 4]
    ])

    distances = np.array([
        [0, 3, 5, 4],
        [3, 0, 4, 5],
        [5, 4, 0, 3],
        [4, 5, 3, 0]
    ])

    instance = TSPInstance(
        name="test",
        coordinates=coordinates,
        distances=distances
    )

    route = [0, 1, 2, 3]

    assert tour_cost(instance, route) == 14


def test_tour_cost_invalid_length():
    coordinates = np.array([
        [0, 0],
        [3, 0],
        [3, 4]
    ])

    distances = np.array([
        [0, 3, 5],
        [3, 0, 4],
        [5, 4, 0]
    ])

    instance = TSPInstance(
        name="test",
        coordinates=coordinates,
        distances=distances
    )

    with pytest.raises(ValueError):
        tour_cost(instance, [0, 1])


def test_tour_cost_repeated_vertex():
    coordinates = np.array([
        [0, 0],
        [3, 0],
        [3, 4]
    ])

    distances = np.array([
        [0, 3, 5],
        [3, 0, 4],
        [5, 4, 0]
    ])

    instance = TSPInstance(
        name="test",
        coordinates=coordinates,
        distances=distances
    )

    with pytest.raises(ValueError):
        tour_cost(instance, [0, 1, 1])