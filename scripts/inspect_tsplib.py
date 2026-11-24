
from pathlib import Path
import tsplib95


INSTANCES_DIR = Path(__file__).resolve().parents[1] / "data" / "instances"

NAMES = [
    "ulysses16",
    "gr24",
    "fri26",
    "bays29",
    "swiss42",
    "att48",
    "gr48",
    "hk48",
    "brazil58",
    "berlin52",
    "st70",
    "eil101",
]


for name in NAMES:
    filepath = INSTANCES_DIR / f"{name}.tsp"

    print(f"\n{'=' * 50}")
    print(f"Instância: {name}")

    try:
        problem = tsplib95.load(str(filepath))

        nodes = list(problem.get_nodes())

        print("Dimensão:", problem.dimension)
        print("Tipo:", problem.edge_weight_type)
        print("Formato:", problem.edge_weight_format)
        print("Quantidade de nós:", len(nodes))
        print("Primeiros nós:", nodes[:10])
        print("Últimos nós:", nodes[-5:])
        print("Coordenadas disponíveis:", bool(problem.node_coords))

        if nodes:
            print(
                "Peso do primeiro nó para ele mesmo:",
                problem.get_weight(nodes[0], nodes[0])
            )

    except Exception as error:
        print("ERRO:", repr(error))


# Inspeciona o arquivo eil51 separadamente
filepath = INSTANCES_DIR / "eil51.tsp"

print(f"\n{'=' * 50}")
print("Inspeção do arquivo eil51.tsp")

with open(filepath, "r", encoding="utf-8-sig") as file:
    lines = file.readlines()

print("\nPrimeiras 12 linhas:")
for line in lines[:12]:
    print(repr(line))

print("\nÚltimas 8 linhas:")
for line in lines[-8:]:
    print(repr(line))
