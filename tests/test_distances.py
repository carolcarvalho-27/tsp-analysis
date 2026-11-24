
import numpy as np
import pytest

from src.tsp.parser import load_tsplib
from src.tsp.instance import TSPInstance
from src.tsp.distances import (
    euclidean_distance,
    build_distance_matrix
)


def test_tsp_instance():
    coordinates = np.array([
        [0, 0],
        [3, 4],
        [6, 8]
    ])

    distances = np.array([
        [0, 5, 10],
        [5, 0, 5],
        [10, 5, 0]
    ])

    instance = TSPInstance(
        name="test",
        coordinates=coordinates,
        distances=distances
    )

    assert instance.n == 3
    assert instance.distance(0, 1) == 5
    assert instance.distance(1, 2) == 5
    assert instance.distance(0, 2) == 10


def test_euclidean_distance():
    p1 = np.array([0, 0])
    p2 = np.array([3, 4])

    assert euclidean_distance(p1, p2) == 5


def test_build_distance_matrix():
    coordinates = np.array([
        [0, 0],
        [3, 4],
        [6, 8]
    ])

    expected = np.array([
        [0, 5, 10],
        [5, 0, 5],
        [10, 5, 0]
    ])

    result = build_distance_matrix(coordinates)

    assert np.array_equal(result, expected)


def test_distance_matrix_properties():
    coordinates = np.array([
        [0, 0],
        [3, 4],
        [6, 8]
    ])

    distances = build_distance_matrix(coordinates)

    assert np.all(distances == distances.T)
    assert np.all(np.diag(distances) == 0)
    assert np.issubdtype(distances.dtype, np.integer)


def test_load_tsplib(tmp_path):
    content = """NAME: test_instance
TYPE: TSP
DIMENSION: 3
EDGE_WEIGHT_TYPE: EUC_2D
NODE_COORD_SECTION
1 0 0
2 3 4
3 6 8
EOF
"""

    filepath = tmp_path / "test.tsp"
    filepath.write_text(content)

    instance = load_tsplib(str(filepath))

    assert instance.name == "test_instance"
    assert instance.n == 3
    assert instance.distance(0, 1) == 5
    assert instance.distance(1, 2) == 5
    assert instance.distance(0, 2) == 10


def test_reject_unsupported_weight_type(tmp_path):
    content = """NAME: invalid
TYPE: TSP
DIMENSION: 2
EDGE_WEIGHT_TYPE: CEIL_2D
NODE_COORD_SECTION
1 0 0
2 1 1
EOF
"""

    filepath = tmp_path / "invalid.tsp"
    filepath.write_text(content)

    with pytest.raises(ValueError):
        load_tsplib(str(filepath))


def test_reject_incorrect_dimension(tmp_path):
    content = """NAME: invalid
TYPE: TSP
DIMENSION: 3
EDGE_WEIGHT_TYPE: EUC_2D
NODE_COORD_SECTION
1 0 0
2 3 4
EOF
"""

    filepath = tmp_path / "invalid_dimension.tsp"
    filepath.write_text(content)

    with pytest.raises(ValueError):
        load_tsplib(str(filepath))
