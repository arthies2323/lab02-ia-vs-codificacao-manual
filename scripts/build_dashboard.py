"""Dashboard de visualizacao (Lab02S03, Passo 6).

Le data/timings.csv e data/metrics.csv e gera graficos comparando
com-ia vs sem-ia para as 3 RQs: tempo (RQ1), taxa de sucesso (RQ2) e
metricas estaticas (RQ3). Salva um painel unico e as figuras
individuais em Relatorios/graficos/.

Uso:
    python scripts/build_dashboard.py
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

TOTAL_TESTES = {
    "agenda-turnos": 9,
    "compactar-serie": 14,
    "fatura-progressiva": 9,
    "ranking-liga": 9,
}

# Paleta categorica fixa: com-ia = azul (slot 1), sem-ia = laranja (slot 2).
# Ordem sempre a mesma nos graficos -- ver skill de dataviz do projeto.
CORES = {"com-ia": "#2a78d6", "sem-ia": "#eb6834"}
ORDEM = ["com-ia", "sem-ia"]


def carregar_timings(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["total_testes"] = df["kata"].map(TOTAL_TESTES)
    df["taxa_sucesso"] = df["testes_passando"] / df["total_testes"]
    return df


def carregar_metrics(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df.sort_values("timestamp").drop_duplicates(
        subset=["integrante", "kata", "tratamento"], keep="last"
    )


def box_com_pontos(ax, df: pd.DataFrame, coluna: str, titulo: str, ylabel: str) -> None:
    sns.boxplot(
        data=df, x="tratamento", y=coluna, order=ORDEM,
        hue="tratamento", palette=CORES, legend=False,
        width=0.5, fliersize=0, ax=ax,
    )
    sns.stripplot(
        data=df, x="tratamento", y=coluna, order=ORDEM,
        color="#0b0b0b", size=5, alpha=0.6, jitter=0.15, ax=ax,
    )
    ax.set_title(titulo, fontsize=11, fontweight="bold")
    ax.set_xlabel("")
    ax.set_ylabel(ylabel)
    sns.despine(ax=ax)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timings", type=Path, default=Path("data/timings.csv"))
    parser.add_argument("--metrics", type=Path, default=Path("data/metrics.csv"))
    parser.add_argument("--out-dir", type=Path, default=Path("Relatorios/graficos"))
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)

    timings = carregar_timings(args.timings)
    metrics = carregar_metrics(args.metrics)

    sns.set_theme(style="white", font="sans-serif")
    plt.rcParams["axes.edgecolor"] = "#c3c2b7"
    plt.rcParams["text.color"] = "#0b0b0b"
    plt.rcParams["axes.labelcolor"] = "#52514e"
    plt.rcParams["xtick.color"] = "#52514e"
    plt.rcParams["ytick.color"] = "#52514e"

    paineis = [
        (timings, "tempo_min", "RQ1 — Tempo de resolução", "minutos"),
        (timings, "taxa_sucesso", "RQ2 — Taxa de sucesso", "% testes passando"),
        (metrics, "complexity_avg", "RQ3 — Complexidade ciclomática média", "CC média"),
        (metrics, "duplication_pct", "RQ3 — Duplicação de código", "% duplicado"),
        (metrics, "mi_avg", "RQ3 — Maintainability Index", "MI"),
        (metrics, "sloc", "RQ3 — SLOC (controle)", "linhas"),
    ]

    # Painel unico com os 6 graficos -- o "dashboard".
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    fig.suptitle(
        "Assistentes de IA vs. Codificação Manual — com-ia vs sem-ia (N=12 pares)",
        fontsize=14, fontweight="bold",
    )
    for ax, (df, coluna, titulo, ylabel) in zip(axes.flat, paineis):
        box_com_pontos(ax, df, coluna, titulo, ylabel)

    handles = [plt.Rectangle((0, 0), 1, 1, color=CORES[t]) for t in ORDEM]
    fig.legend(handles, ORDEM, loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, -0.02))
    fig.tight_layout(rect=(0, 0.03, 1, 0.95))
    painel_path = args.out_dir / "dashboard.png"
    fig.savefig(painel_path, dpi=150, facecolor="#fcfcfb")
    plt.close(fig)
    print(f"Painel salvo em {painel_path}")

    # Figuras individuais, uma por metrica -- uteis pra colar no relatorio.
    for df, coluna, titulo, ylabel in paineis:
        fig, ax = plt.subplots(figsize=(5, 4))
        box_com_pontos(ax, df, coluna, titulo, ylabel)
        handles = [plt.Rectangle((0, 0), 1, 1, color=CORES[t]) for t in ORDEM]
        ax.legend(handles, ORDEM, loc="best", frameon=False)
        fig.tight_layout()
        nome = coluna.replace("_", "-") + ".png"
        caminho = args.out_dir / nome
        fig.savefig(caminho, dpi=150, facecolor="#fcfcfb")
        plt.close(fig)
        print(f"Figura salva em {caminho}")


if __name__ == "__main__":
    main()
