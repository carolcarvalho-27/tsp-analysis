
import numpy as np

from src.tsp.instance import TSPInstance


def check_triangle_inequality(
    instance: TSPInstance,
    tolerance: float = 1e-9,
) -> tuple[bool, float, int]:
    """
    Verifica se a matriz de distâncias satisfaz a desigualdade triangular.

    Retorna:
        - bool: se a propriedade é satisfeita;
        - float: maior violação encontrada;
        - int: quantidade de violações.
    """
    distances = instance.distances

    # Formato dos arrays: (i, j, k)
    left = distances[:, :, np.newaxis]
    right = (
        distances[:, np.newaxis, :]
        + distances[np.newaxis, :, :]
    )

    violations = left - right

    max_violation = float(max(0.0, np.max(violations)))
    violation_count = int(np.count_nonzero(violations > tolerance))

    is_metric = violation_count == 0

    return is_metric, max_violation, violation_count
