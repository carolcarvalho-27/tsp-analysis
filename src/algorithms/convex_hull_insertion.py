
import numpy as np

from src.tsp.instance import TSPInstance


def _cross_product(origin, point_a, point_b):
    """Calcula o produto vetorial 2D entre OA e OB."""

    return (
        (point_a[0] - origin[0]) * (point_b[1] - origin[1])
        - (point_a[1] - origin[1]) * (point_b[0] - origin[0])
    )


def _convex_hull_vertices(instance: TSPInstance) -> list[int]:
    """
    Retorna os índices dos vértices do fecho convexo
    em ordem ao redor do contorno.

    Utiliza o algoritmo monotonic chain.
    """

    if instance.coordinates is None:
        raise ValueError(
            "O algoritmo de inserção pelo fecho convexo "
            "requer coordenadas dos vértices."
        )

    coordinates = np.asarray(
        instance.coordinates,
        dtype=np.float64,
    )

    if coordinates.ndim != 2 or coordinates.shape != (instance.n, 2):
        raise ValueError("As coordenadas devem ter formato (N, 2).")

    if not np.isfinite(coordinates).all():
        raise ValueError("As coordenadas devem ser valores finitos.")

    # Ordena por coordenadas e, em caso de empate,
    # pelo índice do vértice.
    points = sorted(
        (float(x), float(y), index)
        for index, (x, y) in enumerate(coordinates)
    )

    # Remove coordenadas duplicadas do fecho.
    # Os vértices duplicados serão inseridos posteriormente.
    unique_points = []
    previous_coordinate = None

    for x, y, index in points:
        coordinate = (x, y)

        if coordinate != previous_coordinate:
            unique_points.append((x, y, index))
            previous_coordinate = coordinate

    if len(unique_points) <= 2:
        return [point[2] for point in unique_points]

    lower = []

    for point in unique_points:
        while len(lower) >= 2:
            cross = _cross_product(
                lower[-2],
                lower[-1],
                point,
            )

            if cross > 0:
                break

            lower.pop()

        lower.append(point)

    upper = []

    for point in reversed(unique_points):
        while len(upper) >= 2:
            cross = _cross_product(
                upper[-2],
                upper[-1],
                point,
            )

            if cross > 0:
                break

            upper.pop()

        upper.append(point)

    hull = lower[:-1] + upper[:-1]

    return [point[2] for point in hull]


def convex_hull_insertion(
    instance: TSPInstance,
    start: int = 0,
) -> list[int]:
    """
    Constrói uma rota TSP usando inserção baseada
    no fecho convexo.

    Primeiro constrói o ciclo do fecho convexo.
    Depois insere os vértices restantes na posição
    que provoca o menor aumento de custo.

    Parâmetros:
        instance:
            Instância do TSP.

        start:
            Vértice em que a rota retornada deve começar.

    Retorno:
        Lista com todos os vértices exatamente uma vez,
        sem repetir o vértice inicial no final.
    """

    if instance.n < 1:
        raise ValueError("A instância deve ter pelo menos um vértice.")

    if not isinstance(start, int) or not 0 <= start < instance.n:
        raise ValueError("Vértice inicial inválido.")

    # Constrói o fecho convexo.
    route = _convex_hull_vertices(instance)

    # Identifica os vértices que ainda não pertencem ao ciclo.
    hull_vertices = set(route)

    remaining = [
        vertex
        for vertex in range(instance.n)
        if vertex not in hull_vertices
    ]

    # Insere um vértice por vez.
    while remaining:

        best_delta = float("inf")
        best_vertex = None
        best_position = None

        # Avalia todas as combinações de vértice e aresta.
        for vertex in remaining:

            for position in range(len(route)):

                current = route[position]
                next_vertex = route[
                    (position + 1) % len(route)
                ]

                delta = (
                    instance.distance(current, vertex)
                    + instance.distance(vertex, next_vertex)
                    - instance.distance(current, next_vertex)
                )

                # Desempate determinístico:
                # primeiro pelo vértice e depois pela posição.
                candidate = (delta, vertex, position)

                if best_vertex is None or candidate < (
                    best_delta,
                    best_vertex,
                    best_position,
                ):
                    best_delta = delta
                    best_vertex = vertex
                    best_position = position

        # Insere o vértice escolhido depois da posição avaliada.
        route.insert(best_position + 1, best_vertex)
        remaining.remove(best_vertex)

    # Rotaciona a rota para começar no vértice solicitado.
    start_position = route.index(start)

    route = (
        route[start_position:]
        + route[:start_position]
    )

    return route
