
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error


CSV_PATH = Path("data/results/raw/experiments.csv")
OUTPUT_DIR = Path("reports/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(CSV_PATH)

# Converte colunas numéricas; campos vazios permanecem como NaN.
numeric_columns = [
    "n", "initial_cost", "best_cost", "bnb_elapsed_seconds",
    "expanded_nodes", "pruned_nodes", "max_depth",
    "peak_traced_memory_delta_mb"
]
for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Remove casos em que a estratégia não se aplica.
applicable = df[df["status"] != "not_applicable"].copy()

# ---------------------------------------------------------
# 1. Nós expandidos x N + regressão de potência
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 6))

for strategy, group in applicable.groupby("strategy"):
    group = group.dropna(subset=["n", "expanded_nodes"])
    ax.scatter(
        group["n"], group["expanded_nodes"],
        label=strategy, alpha=0.75
    )

    # Ajuste log-log: log10(nodes) = intercept + b*log10(N)
    # A curva é exploratória e descreve o esforço observado.
    if len(group) >= 3:
        x = np.log10(group[["n"]].to_numpy())
        y = np.log10(group["expanded_nodes"].to_numpy())

        model = LinearRegression()
        model.fit(x, y)
        prediction = model.predict(x)

        r2 = r2_score(y, prediction)
        rmse_log = np.sqrt(mean_squared_error(y, prediction))

        order = np.argsort(group["n"].to_numpy())
        x_curve = group["n"].to_numpy()[order]
        y_curve = 10 ** prediction[order]

        ax.plot(x_curve, y_curve, linestyle="--")

        print(
            f"{strategy}: "
            f"expoente b={model.coef_[0]:.3f}; "
            f"R²(log)={r2:.3f}; "
            f"RMSE(log10)={rmse_log:.3f}; "
            f"n_observações={len(group)}"
        )

ax.set_yscale("log")
ax.set_xlabel("Número de vértices (N)")
ax.set_ylabel("Nós expandidos (escala log)")
ax.set_title("Esforço de busca do B&B por estratégia")
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "nos_expandidos_regressao.png", dpi=300)
fig.savefig(OUTPUT_DIR / "nos_expandidos_regressao.pdf")
plt.close(fig)


# ---------------------------------------------------------
# 2. Proporção de nós podados
# ---------------------------------------------------------
valid = applicable.dropna(
    subset=["expanded_nodes", "pruned_nodes"]
).copy()

denominator = valid["expanded_nodes"] + valid["pruned_nodes"]
valid["pruning_ratio"] = np.where(
    denominator > 0,
    valid["pruned_nodes"] / denominator,
    np.nan
)

fig, ax = plt.subplots(figsize=(9, 6))

for strategy, group in valid.groupby("strategy"):
    ax.scatter(
        group["n"], group["pruning_ratio"] * 100,
        label=strategy, alpha=0.75
    )

ax.set_xlabel("Número de vértices (N)")
ax.set_ylabel("Nós podados (%)")
ax.set_title("Proporção de nós podados pelo B&B")
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "proporcao_poda.png", dpi=300)
fig.savefig(OUTPUT_DIR / "proporcao_poda.pdf")
plt.close(fig)


# ---------------------------------------------------------
# 3. Tempo observado: conclusão x timeout
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 6))

for status, group in applicable.groupby("status"):
    marker = "o" if status == "completed" else "x"
    ax.scatter(
        group["n"], group["bnb_elapsed_seconds"],
        label=status, marker=marker, alpha=0.8
    )

ax.axhline(1800, linestyle="--", label="Limite de 1800 s")
ax.set_xlabel("Número de vértices (N)")
ax.set_ylabel("Tempo observado do B&B (s)")
ax.set_title("Tempo de execução e interrupções por timeout")
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "tempo_bnb.png", dpi=300)
fig.savefig(OUTPUT_DIR / "tempo_bnb.pdf")
plt.close(fig)


# ---------------------------------------------------------
# 4. Gap da solução inicial, somente onde o ótimo foi provado
# ---------------------------------------------------------
completed = applicable[applicable["status"] == "completed"].copy()

# O custo final comum às estratégias de uma instância é usado
# como ótimo comprovado somente nas execuções completed.
optima = (
    completed.groupby("instance")["best_cost"]
    .min()
    .rename("optimal_cost")
)

completed = completed.join(optima, on="instance")
completed["initial_gap_percent"] = (
    (completed["initial_cost"] - completed["optimal_cost"])
    / completed["optimal_cost"] * 100
)

fig, ax = plt.subplots(figsize=(9, 6))

strategies = list(completed["strategy"].dropna().unique())
values = [
    completed.loc[
        completed["strategy"] == strategy,
        "initial_gap_percent"
    ].dropna().to_numpy()
    for strategy in strategies
]

ax.boxplot(values, tick_labels=strategies)
ax.set_ylabel("Gap da solução inicial em relação ao ótimo (%)")
ax.set_title("Qualidade das soluções iniciais nas instâncias resolvidas")
ax.tick_params(axis="x", rotation=20)
ax.grid(True, axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "gap_inicial.png", dpi=300)
fig.savefig(OUTPUT_DIR / "gap_inicial.pdf")
plt.close(fig)


# Tabela resumida de gaps para conferência e uso no artigo.
gap_summary = (
    completed.groupby("strategy")["initial_gap_percent"]
    .agg(["count", "mean", "median", "min", "max"])
    .round(2)
)
gap_summary.to_csv(OUTPUT_DIR / "resumo_gaps.csv")

print("\nResumo dos gaps iniciais:")
print(gap_summary)
print(f"\nFiguras salvas em: {OUTPUT_DIR}")
