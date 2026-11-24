import numpy as np
import pytest

from src.tsp.instance import TSPInstance
from src.experiments.runner import (
    STRATEGIES,
    run_instance_experiments,
    CSV_FIELDS,
    load_results_csv,
    save_results_csv,
    get_completed_strategies,
)


def test_load_results_csv_nonexistent_file(tmp_path):
    path = tmp_path / "results.csv"

    results = load_results_csv(path)

    assert results == []


def test_load_results_csv_empty_file(tmp_path):
    path = tmp_path / "results.csv"

    save_results_csv([], path)

    results = load_results_csv(path)

    assert results == []


def test_load_results_csv_with_records(tmp_path):
    path = tmp_path / "results.csv"

    original_results = [
        {
            "instance": "ulysses16",
            "n": 16,
            "strategy": "cold_start",
            "status": "timed_out",
            "not_applicable_reason": "",
            "initial_cost": 9665,
            "best_cost": 7004,
            "warm_start_seconds": 0.01,
            "bnb_elapsed_seconds": 10.0,
            "bnb_time_for_analysis": "",
            "total_seconds": 10.01,
            "expanded_nodes": 8366,
            "pruned_nodes": 100,
            "max_depth": 15,
            "timed_out": True,
            "time_limit_seconds": 10.0,
            "peak_traced_memory_delta_mb": 1.5,
        }
    ]

    save_results_csv(original_results, path)

    loaded_results = load_results_csv(path)

    assert len(loaded_results) == 1
    assert loaded_results[0]["instance"] == "ulysses16"
    assert loaded_results[0]["strategy"] == "cold_start"
    assert loaded_results[0]["status"] == "timed_out"


def test_load_results_csv_missing_columns(tmp_path):
    path = tmp_path / "invalid.csv"
    path.write_text("instance,strategy\n", encoding="utf-8")

    try:
        load_results_csv(path)
        assert False, "Era esperada uma exceção ValueError."
    except ValueError:
        pass


def test_get_completed_strategies_same_instance_and_time_limit():
    existing_results = [
        {
            "instance": "ulysses16",
            "strategy": "cold_start",
            "status": "timed_out",
            "time_limit_seconds": "10.0",
        },
        {
            "instance": "ulysses16",
            "strategy": "nearest_neighbor",
            "status": "completed",
            "time_limit_seconds": "10.0",
        },
        {
            "instance": "ulysses16",
            "strategy": "convex_hull_insertion",
            "status": "not_applicable",
            "time_limit_seconds": "10.0",
        },
    ]

    completed = get_completed_strategies(
        existing_results,
        "ulysses16",
        10.0,
    )

    assert completed == {
        "cold_start",
        "nearest_neighbor",
        "convex_hull_insertion",
    }


def test_get_completed_strategies_ignores_other_instances():
    existing_results = [
        {
            "instance": "ulysses16",
            "strategy": "cold_start",
            "status": "completed",
            "time_limit_seconds": "10.0",
        },
    ]

    completed = get_completed_strategies(
        existing_results,
        "eil51",
        10.0,
    )

    assert completed == set()


def test_get_completed_strategies_ignores_different_time_limit():
    existing_results = [
        {
            "instance": "ulysses16",
            "strategy": "cold_start",
            "status": "timed_out",
            "time_limit_seconds": "10.0",
        },
    ]

    completed = get_completed_strategies(
        existing_results,
        "ulysses16",
        1800.0,
    )

    assert completed == set()


def test_get_completed_strategies_ignores_invalid_status():
    existing_results = [
        {
            "instance": "ulysses16",
            "strategy": "cold_start",
            "status": "running",
            "time_limit_seconds": "10.0",
        },
    ]

    completed = get_completed_strategies(
        existing_results,
        "ulysses16",
        10.0,
    )

    assert completed == set()

def create_test_instance():
    coordinates = np.array([
        [0, 0],
        [1, 0],
        [1, 1],
        [0, 1],
    ])

    distances = np.array([
        [0, 1, 1, 1],
        [1, 0, 1, 1],
        [1, 1, 0, 1],
        [1, 1, 1, 0],
    ])

    return TSPInstance(
        name="test_instance",
        coordinates=coordinates,
        distances=distances,
    )

def test_run_instance_experiments_executes_all_strategies_by_default():
    instance = create_test_instance()

    results = run_instance_experiments(
        instance,
        time_limit_seconds=0,
    )

    executed_strategies = {
        result["strategy"] for result in results
    }

    assert executed_strategies == set(STRATEGIES)


def test_run_instance_experiments_executes_only_selected_strategies():
    instance = create_test_instance()

    selected = ["nearest_neighbor", "christofides"]

    results = run_instance_experiments(
        instance,
        time_limit_seconds=0,
        strategies=selected,
    )

    executed_strategies = {
        result["strategy"] for result in results
    }

    assert executed_strategies == set(selected)


def test_run_instance_experiments_with_empty_strategy_list():
    instance = create_test_instance()

    results = run_instance_experiments(
        instance,
        time_limit_seconds=0,
        strategies=[],
    )

    assert results == []


def test_run_instance_experiments_rejects_unknown_strategy():
    instance = create_test_instance()

    with pytest.raises(
        ValueError,
        match="Estratégias desconhecidas",
    ):
        run_instance_experiments(
            instance,
            time_limit_seconds=0,
            strategies=["invalid_strategy"],
        )