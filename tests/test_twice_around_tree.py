
import numpy as np
import networkx as nx
import pytest

from src.tsp.instance import TSPInstance
from src.tsp.solution import tour_cost
from src.algorithms.mst import (
    build_complete_graph,
    minimum_spanning_tree
)
from src.algorithms.twice_around_tree import twice_around_tree


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


def test_build_complete_graph(square_instance):
    graph = build_complete_graph(square_instance)

    assert graph.number_of_nodes() == 4
    assert graph.number_of_edges() == 6


def test_minimum_spanning_tree(square_instance):
    mst = minimum_spanning_tree(square_instance)

    assert mst.number_of_nodes() == 4
    assert mst.number_of_edges() == 3
    assert nx.is_tree(mst)

    mst_cost = sum(
        data["weight"]
        for _, _, data in mst.edges(data=True)
    )

    assert mst_cost == 10


def test_twice_around_tree_valid_route(square_instance):
    route = twice_around_tree(square_instance)

    assert len(route) == 4
    assert set(route) == {0, 1, 2, 3}


def test_twice_around_tree_start(square_instance):
    route = twice_around_tree(square_instance, start=2)

    assert route[0] == 2
    assert len(route) == 4
    assert set(route) == {0, 1, 2, 3}


def test_twice_around_tree_cost(square_instance):
    route = twice_around_tree(square_instance)

    cost = tour_cost(square_instance, route)

    assert cost == 14


def test_twice_around_tree_invalid_start(square_instance):
    with pytest.raises(ValueError):
        twice_around_tree(square_instance, start=4)


def test_twice_around_tree_negative_start(square_instance):
    with pytest.raises(ValueError):
        twice_around_tree(square_instance, start=-1)
