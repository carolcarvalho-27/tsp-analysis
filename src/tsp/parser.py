
import numpy as np
import tsplib95

from src.tsp.instance import TSPInstance
from pathlib import Path

SUPPORTED_WEIGHT_TYPES = {
    "EUC_2D",
    "GEO",
    "ATT",
    "EXPLICIT",
}


def load_tsplib(filepath: str) -> TSPInstance:
    """
    Carrega uma instância TSP no formato TSPLIB.

    Tipos de distância aceitos:
    - EUC_2D: distância euclidiana arredondada.
    - GEO: distância geográfica.
    - ATT: distância pseudo-euclidiana.
    - EXPLICIT: pesos fornecidos diretamente no arquivo.

    Retorna um objeto TSPInstance.
    """

    # Carrega o arquivo utilizando a biblioteca tsplib95
    try:
        problem = tsplib95.load(filepath)
    except Exception as error:
        raise ValueError(
            f"Não foi possível carregar a instância TSPLIB: {filepath}"
        ) from error

    # Validação do tipo de problema
    if problem.type != "TSP":
        raise ValueError(
            "Somente instâncias TYPE: TSP são aceitas."
        )

    # Validação do tipo de distância
    edge_weight_type = problem.edge_weight_type

    if edge_weight_type not in SUPPORTED_WEIGHT_TYPES:
        raise ValueError(
            f"Tipo de distância não suportado: {edge_weight_type}"
        )

    # Validação da dimensão
    dimension = problem.dimension

    if dimension is None or dimension <= 0:
        raise ValueError("DIMENSION inválida ou ausente.")

    # Obtém os identificadores dos vértices conforme a biblioteca
    nodes = list(problem.get_nodes())

    if len(nodes) != dimension or len(set(nodes)) != dimension:
        raise ValueError(
            f"Esperados {dimension} vértices distintos, "
            f"mas encontrados {len(nodes)}."
        )

    # Obtém as coordenadas, quando disponíveis
    coordinates = None
    node_coords = problem.node_coords

    if node_coords:
        if set(node_coords.keys()) != set(nodes):
            raise ValueError(
                "Os identificadores das coordenadas "
                "não correspondem aos vértices da instância."
            )

        coordinates = np.array(
            [node_coords[node] for node in nodes],
            dtype=np.float64
        )

        if coordinates.shape != (dimension, 2):
            raise ValueError(
                "As coordenadas devem possuir duas dimensões."
            )

    # Constrói a matriz de distâncias utilizando os identificadores
    # originais e preservando a ordem definida por nodes
    distances = np.zeros(
        (dimension, dimension),
        dtype=np.int64
    )

    try:
        for i in range(dimension):
            for j in range(dimension):
                distances[i, j] = problem.get_weight(
                    nodes[i],
                    nodes[j]
                )
    except Exception as error:
        raise ValueError(
            "Não foi possível construir a matriz de distâncias."
        ) from error

    # Normaliza a diagonal
    np.fill_diagonal(distances, 0)

    # Validação dos pesos
    if np.any(distances < 0):
        raise ValueError(
            "A matriz de distâncias não pode conter pesos negativos."
        )

    if not np.array_equal(distances, distances.T):
        raise ValueError(
            "A matriz de distâncias deve ser simétrica."
        )

    if np.any(np.diag(distances) != 0):
        raise ValueError(
            "A diagonal da matriz de distâncias deve conter zeros."
        )

    return TSPInstance(
        name=Path(problem.name or filepath).stem,
        coordinates=coordinates,
        distances=distances,
        edge_weight_type=edge_weight_type
    )
