
from pathlib import Path

import pytest

from src.tsp.parser import load_tsplib
from src.tsp.solution import tour_cost
from src.algorithms.initial_solutions import generate_initial_routes


INSTANCES_DIR = Path("data/instances")


@pytest.mark.parametrize(
    "instance_path",
    sorted(INSTANCES_DIR.glob("*.tsp")),
    ids=lambda path: path.stem,
)
def test_initial_solutions_are_valid(instance_path):
    instance = load_tsplib(instance_path)

    routes = generate_initial_routes(instance)

    assert routes, "Nenhuma solução inicial foi gerada."

    for strategy, route in routes.items():

        # A rota deve conter exatamente N vértices.
        assert len(route) == instance.n, (
            f"{strategy}: quantidade incorreta de vértices."
        )

        # Cada vértice deve aparecer exatamente uma vez.
        assert set(route) == set(range(instance.n)), (
            f"{strategy}: rota contém vértices inválidos ou repetidos."
        )

        # O custo da rota deve ser calculável e positivo.
        cost = tour_cost(instance, route)

        assert cost > 0, (
            f"{strategy}: custo inválido para a rota."
        )
