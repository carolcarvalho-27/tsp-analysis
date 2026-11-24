
import csv
import tracemalloc


from pathlib import Path
from time import perf_counter
from typing import Callable
from math import isclose

from src.algorithms.branch_and_bound import branch_and_bound
from src.algorithms.nearest_neighbor import nearest_neighbor
from src.algorithms.convex_hull_insertion import convex_hull_insertion
from src.algorithms.twice_around_tree import twice_around_tree
from src.algorithms.christofides import christofides
from src.tsp.metrics import check_triangle_inequality

from src.tsp.instance import TSPInstance
from src.tsp.solution import tour_cost


STRATEGIES = {
    "cold_start": lambda instance: list(range(instance.n)),
    "nearest_neighbor": lambda instance: nearest_neighbor(
        instance, start=0
    ),
    "convex_hull_insertion": lambda instance: convex_hull_insertion(
        instance, start=0
    ),
    "twice_around_tree": lambda instance: twice_around_tree(
        instance, start=0
    ),
    "christofides": lambda instance: christofides(
        instance, start=0
    ),
}


CSV_FIELDS = [
    "instance",
    "n",
    "is_metric",
    "max_triangle_violation",
    "triangle_violation_count",
    "strategy",
    "status",
    "not_applicable_reason",
    "initial_cost",
    "best_cost",
    "warm_start_seconds",
    "bnb_elapsed_seconds",
    "bnb_time_for_analysis",
    "total_seconds",
    "expanded_nodes",
    "pruned_nodes",
    "max_depth",
    "timed_out",
    "time_limit_seconds",
    "peak_traced_memory_delta_mb",
]


def run_instance_experiments(
    instance: TSPInstance,
    time_limit_seconds: float = 1800.0,
    on_result: Callable[[dict], None] | None = None,
    strategies: list[str] | None = None,
) -> list[dict]:
    """
    Executa o Branch-and-Bound com cada estratégia
    de solução inicial e coleta as métricas.

    Estratégias indisponíveis são registradas como
    not_applicable.

    O callback on_result, quando fornecido, é chamado
    imediatamente após cada estratégia ser registrada.

    Retorna uma lista de dicionários, um por estratégia.
    """

    results = []

    results = []

    # Verifica as propriedades métricas da instância.
    is_metric, max_violation, violation_count = (
        check_triangle_inequality(instance)
    )

    if strategies is None:
        selected_strategies = set(STRATEGIES)
    else:
        unknown_strategies = set(strategies) - set(STRATEGIES)

        if unknown_strategies:
            raise ValueError(
                f"Estratégias desconhecidas: {sorted(unknown_strategies)}"
            )

        selected_strategies = set(strategies)
    
    for strategy_name, generate_route in STRATEGIES.items():

        if strategy_name not in selected_strategies:
            continue
        # Verifica se a estratégia pode ser aplicada.
        if (
            strategy_name == "convex_hull_insertion"
            and instance.coordinates is None
        ):
            experiment_result = {
                "instance": instance.name,
                "n": instance.n,
                "is_metric": is_metric,
                "max_triangle_violation": max_violation,
                "triangle_violation_count": violation_count,
                "strategy": strategy_name,
                "status": "not_applicable",
                "not_applicable_reason": (
                    "A instância não possui coordenadas."
                ),
                "initial_cost": "",
                "best_cost": "",
                "warm_start_seconds": "",
                "bnb_elapsed_seconds": "",
                "bnb_time_for_analysis": "",
                "total_seconds": "",
                "expanded_nodes": "",
                "pruned_nodes": "",
                "max_depth": "",
                "timed_out": "",
                "time_limit_seconds": time_limit_seconds,
                "peak_traced_memory_delta_mb": "",
            }

            results.append(experiment_result)

            if on_result is not None:
                on_result(experiment_result)

            continue

        # Inicia a medição de memória.
        started_tracing_here = not tracemalloc.is_tracing()

        if started_tracing_here:
            tracemalloc.start()

        baseline_memory, _ = tracemalloc.get_traced_memory()
        tracemalloc.reset_peak()

        total_start = perf_counter()

        try:
            # Gera a solução inicial.
            warm_start_start = perf_counter()

            initial_route = generate_route(instance)

            warm_start_seconds = (
                perf_counter() - warm_start_start
            )

            initial_cost = tour_cost(instance, initial_route)

            # Executa o Branch-and-Bound.
            result = branch_and_bound(
                instance,
                initial_route=initial_route,
                time_limit_seconds=time_limit_seconds,
            )

            total_seconds = perf_counter() - total_start

            # Obtém o pico de memória rastreada.
            _, peak_memory = tracemalloc.get_traced_memory()

            memory_delta_mb = max(
                0,
                peak_memory - baseline_memory,
            ) / (1024 * 1024)

            experiment_result = {
                "instance": instance.name,
                "n": instance.n,
                "is_metric": is_metric,
                "max_triangle_violation": max_violation,
                "triangle_violation_count": violation_count,
                "strategy": strategy_name,
                "status": (
                    "timed_out"
                    if result.timed_out
                    else "completed"
                ),
                "not_applicable_reason": "",
                "initial_cost": initial_cost,
                "best_cost": result.cost,
                "warm_start_seconds": warm_start_seconds,
                "bnb_elapsed_seconds": result.elapsed_seconds,
                "bnb_time_for_analysis": (
                    ""
                    if result.timed_out
                    else result.elapsed_seconds
                ),
                "total_seconds": total_seconds,
                "expanded_nodes": result.expanded_nodes,
                "pruned_nodes": result.pruned_nodes,
                "max_depth": result.max_depth,
                "timed_out": result.timed_out,
                "time_limit_seconds": time_limit_seconds,
                "peak_traced_memory_delta_mb": memory_delta_mb,
            }

            results.append(experiment_result)

            if on_result is not None:
                on_result(experiment_result)

        finally:
            if started_tracing_here:
                tracemalloc.stop()

    return results


def save_results_csv(
    results: list[dict],
    output_path: str | Path,
) -> None:
    """
    Salva os resultados em um arquivo CSV.

    Se o arquivo já existir, seu conteúdo será substituído.
    """

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=CSV_FIELDS,
        )

        writer.writeheader()
        writer.writerows(results)


def load_results_csv(
    input_path: str | Path,
) -> list[dict]:
    """
    Carrega os resultados de um arquivo CSV existente.

    Se o arquivo não existir, retorna uma lista vazia.
    Verifica se o arquivo possui todas as colunas esperadas.
    """

    input_path = Path(input_path)

    if not input_path.exists():
        return []

    with input_path.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            return []

        missing_fields = set(CSV_FIELDS) - set(reader.fieldnames)

        if missing_fields:
            raise ValueError(
                "O arquivo CSV não possui todas as colunas esperadas. "
                f"Colunas ausentes: {sorted(missing_fields)}"
            )

        return list(reader)


def get_completed_strategies(
    existing_results: list[dict],
    instance_name: str,
    time_limit_seconds: float,
) -> set[str]:
    """
    Identifica as estratégias já registradas para uma instância
    e um limite de tempo específico.

    São considerados processados os registros com status:
    completed, timed_out ou not_applicable.
    """

    completed_strategies = set()

    valid_statuses = {
        "completed",
        "timed_out",
        "not_applicable",
    }

    for result in existing_results:

        # Verifica se pertence à instância desejada.
        if result.get("instance") != instance_name:
            continue

        # Verifica se o registro possui uma estratégia.
        strategy = result.get("strategy")

        if not strategy:
            continue

        # Verifica se o status representa um resultado registrado.
        if result.get("status") not in valid_statuses:
            continue

        # Verifica se o limite de tempo é o mesmo.
        try:
            recorded_time_limit = float(
                result["time_limit_seconds"]
            )
        except (KeyError, TypeError, ValueError):
            continue

        if isclose(
            recorded_time_limit,
            time_limit_seconds,
            rel_tol=1e-9,
            abs_tol=1e-9,
        ):
            completed_strategies.add(strategy)

    return completed_strategies
