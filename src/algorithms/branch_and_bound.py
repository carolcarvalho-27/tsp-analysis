
from collections.abc import Sequence
from dataclasses import dataclass
from math import isfinite
from time import monotonic

from src.tsp.instance import TSPInstance
from src.tsp.solution import tour_cost
from src.algorithms.nearest_neighbor import nearest_neighbor


@dataclass
class BranchAndBoundResult:
    route: list[int]
    cost: int
    expanded_nodes: int
    pruned_nodes: int
    max_depth: int
    elapsed_seconds: float
    timed_out: bool


def mst_cost(
    instance: TSPInstance,
    vertices: Sequence[int]
) -> int:
    """
    Calcula o custo de uma MST sobre um subconjunto
    de vértices usando Prim.

    Complexidade: O(k²), sendo k a quantidade de vértices.
    """

    vertices = list(vertices)

    if len(set(vertices)) != len(vertices):
        raise ValueError("Existem vértices repetidos.")

    if any(v < 0 or v >= instance.n for v in vertices):
        raise ValueError("Vértice inválido.")

    if len(vertices) <= 1:
        return 0

    k = len(vertices)

    in_tree = [False] * k
    min_distance = [float("inf")] * k

    min_distance[0] = 0
    total_cost = 0

    for _ in range(k):
        current = -1

        for i in range(k):
            if not in_tree[i]:
                if (
                    current == -1
                    or min_distance[i] < min_distance[current]
                ):
                    current = i

        in_tree[current] = True
        total_cost += min_distance[current]

        for i in range(k):
            if not in_tree[i]:
                distance = instance.distance(
                    vertices[current],
                    vertices[i]
                )

                if distance < min_distance[i]:
                    min_distance[i] = distance

    return total_cost


def completion_lower_bound(
    instance: TSPInstance,
    route: Sequence[int],
    current_cost: int
) -> int:
    """
    Calcula um limite inferior para a conclusão
    de uma rota parcial do TSP.

    A rota parcial deve começar no vértice 0
    e não pode conter vértices repetidos.
    """

    route = list(route)

    if not route or route[0] != 0:
        raise ValueError("A rota parcial deve começar no vértice 0.")

    if len(set(route)) != len(route):
        raise ValueError("A rota parcial contém vértices repetidos.")

    if any(v < 0 or v >= instance.n for v in route):
        raise ValueError("A rota parcial contém vértices inválidos.")

    if current_cost < 0:
        raise ValueError("O custo atual não pode ser negativo.")

    visited = set(route)

    unvisited = [
        vertex
        for vertex in range(instance.n)
        if vertex not in visited
    ]

    current = route[-1]
    start = route[0]

    if not unvisited:
        return current_cost + instance.distance(current, start)

    remaining_mst_cost = mst_cost(instance, unvisited)

    min_current_connection = min(
        instance.distance(current, vertex)
        for vertex in unvisited
    )

    min_start_connection = min(
        instance.distance(start, vertex)
        for vertex in unvisited
    )

    return (
        current_cost
        + remaining_mst_cost
        + min_current_connection
        + min_start_connection
    )


def branch_and_bound(
    instance: TSPInstance,
    initial_route: Sequence[int] | None = None,
    time_limit_seconds: float = 1800.0,
) -> BranchAndBoundResult:
    """
    Resolve o TSP por Branch-and-Bound.

    Parâmetros:
        instance:
            Instância do TSP.

        initial_route:
            Rota completa usada como solução inicial.
            Se None, utiliza Nearest Neighbor.

        time_limit_seconds:
            Limite de execução em segundos.
            O padrão é 1800 segundos (30 minutos).

    Retorno:
        BranchAndBoundResult contendo a melhor rota
        encontrada, seu custo e as métricas da busca.

    A rota retornada é garantidamente válida.
    Se timed_out for True, não há garantia de otimalidade.
    """

    if instance.n < 1:
        raise ValueError("A instância deve ter pelo menos um vértice.")

    if (
        not isinstance(time_limit_seconds, (int, float))
        or not isfinite(time_limit_seconds)
        or time_limit_seconds < 0
    ):
        raise ValueError("O limite de tempo deve ser um número não negativo.")

    # Obtém a solução inicial.
    if initial_route is None:
        best_route = nearest_neighbor(instance, start=0)
    else:
        best_route = list(initial_route)

        if len(best_route) != instance.n:
            raise ValueError("A rota inicial deve conter n vértices.")

        if set(best_route) != set(range(instance.n)):
            raise ValueError(
                "A rota inicial deve conter todos os vértices exatamente uma vez."
            )

        # Rotaciona a rota para começar no vértice 0.
        start_position = best_route.index(0)
        best_route = (
            best_route[start_position:]
            + best_route[:start_position]
        )

    best_cost = tour_cost(instance, best_route)

    # Métricas da busca.
    expanded_nodes = 0
    pruned_nodes = 0
    max_depth = 0
    timed_out = False

    start_time = monotonic()

    # Controle dos vértices visitados.
    visited = [False] * instance.n
    visited[0] = True

    route = [0]

    def search(current: int, current_cost: int) -> None:
        nonlocal best_route
        nonlocal best_cost
        nonlocal expanded_nodes
        nonlocal pruned_nodes
        nonlocal max_depth
        nonlocal timed_out

        if timed_out:
            return

        # Verifica o limite de tempo.
        if monotonic() - start_time >= time_limit_seconds:
            timed_out = True
            return

        max_depth = max(max_depth, len(route))

        # Caso todos os vértices tenham sido visitados.
        if len(route) == instance.n:
            total_cost = (
                current_cost
                + instance.distance(current, 0)
            )

            if total_cost < best_cost:
                best_cost = total_cost
                best_route = route.copy()

            return

        # Calcula o limite inferior do ramo atual.
        lower_bound = completion_lower_bound(
            instance,
            route,
            current_cost,
        )

        # Verifica novamente o tempo após o cálculo do limite.
        if monotonic() - start_time >= time_limit_seconds:
            timed_out = True
            return

        # Poda por limite inferior.
        if lower_bound >= best_cost:
            pruned_nodes += 1
            return

        expanded_nodes += 1

        # Candidatos ordenados pela distância ao vértice atual.
        # Essa ordenação melhora a busca, mas não compromete
        # a exatidão do algoritmo.
        candidates = [
            vertex
            for vertex in range(instance.n)
            if not visited[vertex]
        ]

        candidates.sort(
            key=lambda vertex: instance.distance(current, vertex)
        )

        for next_vertex in candidates:

            if timed_out:
                return

            if monotonic() - start_time >= time_limit_seconds:
                timed_out = True
                return

            edge_cost = instance.distance(current, next_vertex)

            visited[next_vertex] = True
            route.append(next_vertex)

            search(
                next_vertex,
                current_cost + edge_cost,
            )

            # Desfaz a escolha para explorar outro ramo.
            route.pop()
            visited[next_vertex] = False

    search(current=0, current_cost=0)

    elapsed_seconds = monotonic() - start_time

    return BranchAndBoundResult(
        route=best_route,
        cost=best_cost,
        expanded_nodes=expanded_nodes,
        pruned_nodes=pruned_nodes,
        max_depth=max_depth,
        elapsed_seconds=elapsed_seconds,
        timed_out=timed_out,
    )
