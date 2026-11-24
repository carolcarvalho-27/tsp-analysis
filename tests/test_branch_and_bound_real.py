
from src.algorithms.branch_and_bound import branch_and_bound
from src.tsp.parser import load_tsplib
from src.tsp.solution import tour_cost


def test_branch_and_bound_eil101():
    instance = load_tsplib("data/instances/eil101.tsp")

    result = branch_and_bound(
        instance,
        time_limit_seconds=3,
    )

    # A rota retornada deve ser válida.
    assert len(result.route) == instance.n
    assert set(result.route) == set(range(instance.n))
    assert result.route[0] == 0

    # O custo informado deve corresponder à rota.
    assert result.cost == tour_cost(instance, result.route)

    # As métricas devem ter valores válidos.
    assert result.expanded_nodes >= 0
    assert result.pruned_nodes >= 0
    assert 1 <= result.max_depth <= instance.n
    assert result.elapsed_seconds >= 0

    # Exibe as métricas para análise.
    print("\nResultados do Branch-and-Bound em eil101:")
    print(f"Custo da rota: {result.cost}")
    print(f"Nós expandidos: {result.expanded_nodes}")
    print(f"Nós podados: {result.pruned_nodes}")
    print(f"Profundidade máxima: {result.max_depth}")
    print(f"Tempo decorrido: {result.elapsed_seconds:.4f} segundos")
    print(f"Timeout: {result.timed_out}")
