
import numpy as np
import pytest

from src.tsp.instance import TSPInstance
from src.tsp.solution import tour_cost
from src.algorithms.nearest_neighbor import nearest_neighbor


@pytest.fixture
def square_instance():
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

    return TSPInstance(
        name="square",
        coordinates=coordinates,
        distances=distances
    )


def test_nearest_neighbor_route(square_instance):
    route = nearest_neighbor(square_instance)

    assert route == [0, 1, 2, 3]


def test_nearest_neighbor_valid_route(square_instance):
    route = nearest_neighbor(square_instance)

    assert len(route) == square_instance.n
    assert set(route) == set(range(square_instance.n))


def test_nearest_neighbor_cost(square_instance):
    route = nearest_neighbor(square_instance)

    assert tour_cost(square_instance, route) == 14


def test_nearest_neighbor_different_start(square_instance):
    route = nearest_neighbor(square_instance, start=2)

    assert route[0] == 2
    assert len(route) == square_instance.n
    assert set(route) == set(range(square_instance.n))


def test_nearest_neighbor_invalid_start(square_instance):
    with pytest.raises(ValueError):
        nearest_neighbor(square_instance, start=4)


def test_nearest_neighbor_negative_start(square_instance):
    with pytest.raises(ValueError):
        nearest_neighbor(square_instance, start=-1)
