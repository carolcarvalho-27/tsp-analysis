
from dataclasses import dataclass
import numpy as np


@dataclass
class TSPInstance:
    name: str
    coordinates: np.ndarray | None
    distances: np.ndarray
    edge_weight_type: str = "EUC_2D"

    @property
    def n(self) -> int:
        return len(self.distances)

    def distance(self, i: int, j: int) -> int:
        return int(self.distances[i, j])
