
from pathlib import Path

from src.tsp.parser import load_tsplib
from src.tsp.metrics import check_triangle_inequality


INSTANCE_DIR = Path("data/instances")


def main():
    print("Verificação da desigualdade triangular\n")

    for filepath in sorted(INSTANCE_DIR.glob("*.tsp")):
        instance = load_tsplib(str(filepath))

        is_metric, max_violation, count = check_triangle_inequality(instance)

        status = "Métrica" if is_metric else "Não métrica"

        print(
            f"{instance.name:12} | "
            f"N={instance.n:3} | "
            f"{status:12} | "
            f"Maior violação={max_violation:.6f} | "
            f"Quantidade={count}"
        )


if __name__ == "__main__":
    main()
