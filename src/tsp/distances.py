
import numpy as np


def euclidean_distance(p1: np.ndarray, p2: np.ndarray) -> int:
    """
    Calcula a distância EUC_2D entre dois pontos,
    seguindo o arredondamento da TSPLIB.
    """
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]

    return int(np.floor(np.sqrt(dx**2 + dy**2) + 0.5))


def build_distance_matrix(coordinates: np.ndarray) -> np.ndarray:
    """
    Constrói a matriz completa de distâncias EUC_2D.

    Retorna uma matriz simétrica de inteiros.
    """
    coordinates = np.asarray(coordinates, dtype=np.float64)

    if coordinates.ndim != 2 or coordinates.shape[1] != 2:
        raise ValueError("As coordenadas devem ter formato (N, 2).")

    n = len(coordinates)

    dx = coordinates[:, 0][:, None] - coordinates[:, 0][None, :]
    dy = coordinates[:, 1][:, None] - coordinates[:, 1][None, :]

    distances = np.floor(np.sqrt(dx**2 + dy**2) + 0.5)

    return distances.astype(np.int64)
