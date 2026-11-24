
import numpy as np
import networkx as nx
import pytest

from src.tsp.instance import TSPInstance
from src.tsp.solution import tour_cost
from src.algorithms.mst import minimum_spanning_tree
from src.algorithms.christofides import (
    find_odd_degree_vertices,
    minimum_weight_perfect_matching,
    christofides
)


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


def test_find_odd_degree_vertices(square_instance):
    mst = minimum_spanning_tree(square_instance)

    odd_vertices = find_odd_degree_vertices(mst)

    assert len(odd_vertices) % 2 == 0

    for vertex in odd_vertices:
        assert mst.degree(vertex) % 2 == 1


def test_minimum_weight_perfect_matching(square_instance):
    mst = minimum_spanning_tree(square_instance)

    odd_vertices = find_odd_degree_vertices(mst)

    matching = minimum_weight_perfect_matching(
        square_instance,
        odd_vertices
    )

    matched_vertices = {
        vertex
        for edge in matching
        for vertex in edge
    }

    assert len(matching) == len(odd_vertices) // 2
    assert matched_vertices == set(odd_vertices)


def test_matching_invalid_odd_quantity(square_instance):
    with pytest.raises(ValueError):
        minimum_weight_perfect_matching(
            square_instance,
            [0, 1, 2]
        )


def test_matching_repeated_vertex(square_instance):
    with pytest.raises(ValueError):
        minimum_weight_perfect_matching(
            square_instance,
            [0, 1, 1, 2]
        )


def test_matching_invalid_vertex(square_instance):
    with pytest.raises(ValueError):
        minimum_weight_perfect_matching(
            square_instance,
            [0, 4]
        )


def test_christofides_valid_route(square_instance):
    route = christofides(square_instance)

    assert len(route) == square_instance.n
    assert set(route) == set(range(square_instance.n))


def test_christofides_cost(square_instance):
    route = christofides(square_instance)

    assert tour_cost(square_instance, route) == 14


def test_christofides_different_start(square_instance):
    route = christofides(square_instance, start=2)

    assert route[0] == 2
    assert len(route) == square_instance.n
    assert set(route) == set(range(square_instance.n))


def test_christofides_invalid_start(square_instance):
    with pytest.raises(ValueError):
        christofides(square_instance, start=4)


def test_christofides_negative_start(square_instance):
    with pytest.raises(ValueError):
        christofides(square_instance, start=-1)
