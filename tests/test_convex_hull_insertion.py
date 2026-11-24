
import numpy as np
import pytest

from src.algorithms.convex_hull_insertion import (
    convex_hull_insertion,
)
from src.tsp.instance import TSPInstance
from src.tsp.distances import build_distance_matrix
from src.tsp.solution import tour_cost


def create_instance(coordinates, name="test"):
    coordinates = np.array(coordinates, dtype=float)

    return TSPInstance(
        name=name,
        coordinates=coordinates,
        distances=build_distance_matrix(coordinates),
    )


@pytest.fixture
def square_instance():
    return create_instance([
        [0, 0],
        [3, 0],
        [3, 4],
        [0, 4],
    ], name="square")


def test_convex_hull_insertion_square(square_instance):
    route = convex_hull_insertion(square_instance)

    assert route == [0, 1, 2, 3]
    assert tour_cost(square_instance, route) == 14


def test_convex_hull_insertion_valid_route(square_instance):
    route = convex_hull_insertion(square_instance)

    assert len(route) == square_instance.n
    assert set(route) == set(range(square_instance.n))
    assert route[0] == 0


def test_convex_hull_insertion_with_interior_point():
    instance = create_instance([
        [0, 0],
        [4, 0],
        [4, 4],
        [0, 4],
        [2, 2],
    ])

    route = convex_hull_insertion(instance)

    assert len(route) == 5
    assert set(route) == set(range(5))
    assert route[0] == 0


def test_convex_hull_insertion_collinear_points():
    instance = create_instance([
        [0, 0],
        [1, 0],
        [2, 0],
        [3, 0],
        [4, 0],
    ])

    route = convex_hull_insertion(instance)

    assert len(route) == 5
    assert set(route) == set(range(5))
    assert route[0] == 0


def test_convex_hull_insertion_duplicate_coordinates():
    instance = create_instance([
        [0, 0],
        [4, 0],
        [4, 4],
        [0, 4],
        [2, 2],
        [2, 2],
    ])

    route = convex_hull_insertion(instance)

    assert len(route) == 6
    assert set(route) == set(range(6))
    assert route[0] == 0


def test_convex_hull_insertion_single_vertex():
    instance = create_instance([
        [0, 0],
    ])

    route = convex_hull_insertion(instance)

    assert route == [0]
    assert tour_cost(instance, route) == 0


def test_convex_hull_insertion_two_vertices():
    instance = create_instance([
        [0, 0],
        [3, 4],
    ])

    route = convex_hull_insertion(instance)

    assert len(route) == 2
    assert set(route) == {0, 1}


def test_convex_hull_insertion_custom_start(square_instance):
    route = convex_hull_insertion(
        square_instance,
        start=2,
    )

    assert route[0] == 2
    assert set(route) == set(range(4))
    assert tour_cost(square_instance, route) == 14


def test_convex_hull_insertion_invalid_start(square_instance):
    with pytest.raises(ValueError):
        convex_hull_insertion(square_instance, start=4)
