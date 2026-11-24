
import numpy as np

from src.tsp.instance import TSPInstance
from src.tsp.metrics import check_triangle_inequality


def test_metric_instance():
    distances = np.array([
        [0, 3, 5, 4],
        [3, 0, 4, 5],
        [5, 4, 0, 3],
        [4, 5, 3, 0],
    ])

    instance = TSPInstance(
        name="square",
        coordinates=None,
        distances=distances,
    )

    is_metric, max_violation, count = check_triangle_inequality(instance)

    assert is_metric
    assert max_violation == 0
    assert count == 0


def test_non_metric_instance():
    distances = np.array([
        [0, 2, 9],
        [2, 0, 6],
        [9, 6, 0],
    ])

    instance = TSPInstance(
        name="non_metric",
        coordinates=None,
        distances=distances,
    )

    is_metric, max_violation, count = check_triangle_inequality(instance)

    assert not is_metric
    assert max_violation > 0
    assert count > 0
