
from pathlib import Path

import numpy as np
import pytest

from src.tsp.parser import load_tsplib


INSTANCES_DIR = Path(__file__).resolve().parents[1] / "data" / "instances"


# Instância, dimensão esperada e tipo de peso esperado
INSTANCES = [
    ("ulysses16", 16, "GEO"),
    ("gr24", 24, "EXPLICIT"),
    ("fri26", 26, "EXPLICIT"),
    ("bays29", 29, "EXPLICIT"),
    ("swiss42", 42, "EXPLICIT"),
    ("att48", 48, "ATT"),
    ("gr48", 48, "EXPLICIT"),
    ("hk48", 48, "EXPLICIT"),
    ("eil51", 51, "EUC_2D"),
    ("berlin52", 52, "EUC_2D"),
    ("brazil58", 58, "EXPLICIT"),
    ("st70", 70, "EUC_2D"),
    ("eil101", 101, "EUC_2D"),
]


@pytest.mark.parametrize(
    "name, expected_n, expected_type",
    INSTANCES
)
def test_parser_multiple_types(name, expected_n, expected_type):

    filepath = INSTANCES_DIR / f"{name}.tsp"

    assert filepath.exists(), (
        f"Arquivo da instância não encontrado: {filepath}"
    )

    instance = load_tsplib(str(filepath))

    # Verifica identificação da instância
    assert instance.name.lower() == name

    # Verifica dimensão
    assert instance.n == expected_n

    # Verifica tipo de peso
    assert instance.edge_weight_type == expected_type

    # Verifica dimensão da matriz
    assert instance.distances.shape == (
        expected_n,
        expected_n
    )

    # Verifica simetria
    assert np.array_equal(
        instance.distances,
        instance.distances.T
    )

    # Verifica diagonal nula
    assert np.all(np.diag(instance.distances) == 0)

    # Verifica pesos não negativos
    assert np.all(instance.distances >= 0)

    # Se houver coordenadas, verifica sua dimensão
    if instance.coordinates is not None:
        assert instance.coordinates.shape == (
            expected_n,
            2
        )

    # Métricas calculadas a partir de coordenadas
    if expected_type in {"EUC_2D", "GEO", "ATT"}:
        assert instance.coordinates is not None
