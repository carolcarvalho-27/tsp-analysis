
import csv

import numpy as np

from src.experiments.runner import (
    run_instance_experiments,
    save_results_csv,
)
from src.tsp.instance import TSPInstance


def create_square_instance():
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


def test_run_instance_experiments():
    instance = create_square_instance()

    results = run_instance_experiments(
        instance,
        time_limit_seconds=10,
    )

    assert len(results) == 5

    strategies = {
        result["strategy"]
        for result in results
    }

    assert strategies == {
        "cold_start",
        "nearest_neighbor",
        "convex_hull_insertion",
        "twice_around_tree",
        "christofides",
    }

    for result in results:
        assert result["instance"] == "square"
        assert result["n"] == 4
        assert result["best_cost"] == 14
        assert result["initial_cost"] >= 0
        assert result["warm_start_seconds"] >= 0
        assert result["bnb_elapsed_seconds"] >= 0
        assert result["expanded_nodes"] >= 0
        assert result["pruned_nodes"] >= 0
        assert result["timed_out"] is False


def test_save_results_csv(tmp_path):
    instance = create_square_instance()

    results = run_instance_experiments(
        instance,
        time_limit_seconds=10,
    )

    output_path = tmp_path / "results.csv"

    save_results_csv(results, output_path)

    assert output_path.exists()

    with output_path.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 5
    assert rows[0]["instance"] == "square"
