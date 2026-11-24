
import argparse
from pathlib import Path

from src.experiments.runner import (
    STRATEGIES,
    run_instance_experiments,
    save_results_csv,
    load_results_csv,
    get_completed_strategies,
)

from src.tsp.parser import load_tsplib


def main():
    parser = argparse.ArgumentParser(
        description="Executa experimentos de TSP com diferentes warm-starts."
    )

    parser.add_argument(
        "instances",
        nargs="+",
        help="Caminhos dos arquivos .tsp que serão utilizados.",
    )

    parser.add_argument(
        "--time-limit",
        type=float,
        default=1800.0,
        help="Limite de tempo do Branch-and-Bound por estratégia, em segundos.",
    )

    parser.add_argument(
        "--output",
        default="data/results/raw/experiments.csv",
        help="Caminho do arquivo CSV de saída.",
    )

    parser.add_argument(
        "--resume",
        action="store_true",
        help="Retoma os experimentos a partir dos resultados já registrados.",
    )

    args = parser.parse_args()

    if args.time_limit < 0:
        parser.error("--time-limit deve ser não negativo.")

    all_results = []
    output_path = Path(args.output)

    # Cria o diretório de saída, caso não exista.
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if args.resume:
        # Recupera os resultados já registrados.
        all_results = load_results_csv(output_path)

        print(
            f"Retomando experimentos: "
            f"{len(all_results)} registros carregados."
        )
    else:
        # Inicia uma campanha nova, substituindo resultados anteriores.
        save_results_csv([], output_path)

        print("Iniciando uma nova campanha de experimentos.")

    # Registra e salva cada resultado individualmente.
    def record_result(result):
        all_results.append(result)
        save_results_csv(all_results, output_path)

    print(f"Instâncias selecionadas: {len(args.instances)}")
    print(f"Limite por estratégia: {args.time_limit} segundos")
    print(f"Arquivo de saída: {output_path}")
    print()

    try:
        for index, instance_path in enumerate(args.instances, start=1):

            print(
                f"[{index}/{len(args.instances)}] "
                f"Carregando {instance_path}..."
            )

            instance = load_tsplib(instance_path)

            print(
                f"Instância: {instance.name} | "
                f"Vértices: {instance.n}"
            )

            # Identifica as estratégias já processadas para esta
            # instância e este limite de tempo.
            completed = get_completed_strategies(
                all_results,
                instance.name,
                args.time_limit,
            )

            # Seleciona somente as estratégias ainda pendentes.
            pending = [
                strategy
                for strategy in STRATEGIES
                if strategy not in completed
            ]

            if not pending:
                print(
                    "Todas as estratégias desta instância "
                    "já foram processadas."
                )
                print()
                continue

            print(
                f"Estratégias pendentes: {', '.join(pending)}"
            )

            results = run_instance_experiments(
                instance,
                time_limit_seconds=args.time_limit,
                on_result=record_result,
                strategies=pending,
            )

            print("Resultados:")

            for result in results:

                if result["status"] == "not_applicable":
                    print(
                        f"  {result['strategy']}: "
                        f"Não aplicável - "
                        f"{result['not_applicable_reason']}"
                    )
                    continue

                status = (
                    "TIMEOUT"
                    if result["timed_out"]
                    else "Concluído"
                )

                print(
                    f"  {result['strategy']}: "
                    f"custo inicial={result['initial_cost']}, "
                    f"melhor custo={result['best_cost']}, "
                    f"tempo B&B={result['bnb_elapsed_seconds']:.4f}s, "
                    f"nós expandidos={result['expanded_nodes']}, "
                    f"status={status}"
                )

            print()

    except KeyboardInterrupt:
        print("\nExecução interrompida pelo usuário.")
        print(
            f"Resultados registrados: {len(all_results)}"
        )
        print(f"Resultados disponíveis em: {output_path}")
        return

    print("Experimentos concluídos.")
    print(f"Total de registros: {len(all_results)}")
    print(f"Resultados salvos em: {output_path}")


if __name__ == "__main__":
    main()
