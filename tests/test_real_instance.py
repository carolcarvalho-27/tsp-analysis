import numpy as np
from src.tsp.parser import load_tsplib


def test_real_instance():
    filepath = "data/instances/eil101.tsp"

    instance = load_tsplib(filepath)

    print(f"Instância: {instance.name}")
    print(f"Número de vértices: {instance.n}")
    print(f"Dimensão da matriz: {instance.distances.shape}")
    print(f"Tipo da matriz: {instance.distances.dtype}")

    print("\nPrimeiras 5 coordenadas:")
    print(instance.coordinates[:5])

    print("\nPrimeiras 5 linhas da matriz:")
    print(instance.distances[:5, :5])

    print("\nValidações:")

    assert instance.n == 101
    print("Quantidade de vértices correta: True")

    assert instance.distances.shape == (101, 101)
    print("Dimensão da matriz correta: True")

    assert np.array_equal(
        instance.distances,
        instance.distances.T
    )
    print("Matriz simétrica: True")

    assert np.all(np.diag(instance.distances) == 0)
    print("Diagonal zerada: True")

    assert np.issubdtype(
        instance.distances.dtype,
        np.integer
    )
    print("Matriz inteira: True")