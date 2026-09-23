"""Analise estatistica das RQ1-RQ3 (Lab02S03, Passo 4).

Le data/timings.csv e data/metrics.csv, monta as tabelas descritivas
(mediana/IQR por tratamento) e roda o teste de Wilcoxon pareado por
(integrante, kata) para cada RQ.

Uso:
    python scripts/analyze_results.py
    python scripts/analyze_results.py --timings data/timings.csv --metrics data/metrics.csv
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from scipy.stats import wilcoxon

TOTAL_TESTES = {
    "agenda-turnos": 9,
    "compactar-serie": 14,
    "fatura-progressiva": 9,
    "ranking-liga": 9,
}


def carregar_timings(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["total_testes"] = df["kata"].map(TOTAL_TESTES)
    df["taxa_sucesso"] = df["testes_passando"] / df["total_testes"]
    return df


def carregar_metrics(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Uma coleta por (integrante, kata, tratamento); se houver mais de uma
    # (reexecucao), fica a mais recente.
    df = df.sort_values("timestamp").drop_duplicates(
        subset=["integrante", "kata", "tratamento"], keep="last"
    )
    return df


def parear(df: pd.DataFrame, coluna: str) -> pd.DataFrame:
    """Pivota (integrante, kata) x tratamento para a coluna dada.

    Devolve só as linhas com os dois tratamentos presentes -- e' o
    pareamento que sustenta o Wilcoxon.
    """
    largo = df.pivot_table(
        index=["integrante", "kata"], columns="tratamento", values=coluna
    )
    completos = largo.dropna(subset=["com-ia", "sem-ia"])
    return completos


def iqr(serie: pd.Series) -> tuple[float, float, float]:
    q1, q3 = serie.quantile(0.25), serie.quantile(0.75)
    return serie.median(), q1, q3


def identificar_outliers(serie: pd.Series, rotulos: pd.Series) -> list[str]:
    """Regra do IQR (1.5x): valores fora de [Q1-1.5*IQR, Q3+1.5*IQR]."""
    q1, q3 = serie.quantile(0.25), serie.quantile(0.75)
    largura = q3 - q1
    baixo, alto = q1 - 1.5 * largura, q3 + 1.5 * largura
    fora = (serie < baixo) | (serie > alto)
    return [f"{r} ({v:.4f})" for r, v, f in zip(rotulos, serie, fora) if f]


def resumo_e_wilcoxon(pares: pd.DataFrame, nome: str, unidade: str = "") -> None:
    n = len(pares)
    print(f"\n--- {nome} (N pares = {n}) ---")
    if n == 0:
        print("sem pares completos (integrante,kata) ainda -- nada a reportar.")
        return

    for tratamento in ("com-ia", "sem-ia"):
        mediana, q1, q3 = iqr(pares[tratamento])
        print(f"{tratamento:7s}: mediana={mediana:.4f}{unidade}  IQR=[{q1:.4f}, {q3:.4f}]")

    rotulos = pares.index.map(lambda idx: f"{idx[0]}/{idx[1]}")
    for tratamento in ("com-ia", "sem-ia"):
        outliers = identificar_outliers(pares[tratamento], rotulos)
        if outliers:
            print(f"outliers ({tratamento}): {', '.join(outliers)}")

    diffs = pares["com-ia"] - pares["sem-ia"]
    if (diffs == 0).all():
        print("todas as diferencas sao zero -- Wilcoxon nao aplicavel (estatistica trivial).")
        return

    estatistica, p_valor = wilcoxon(pares["com-ia"], pares["sem-ia"])
    print(f"Wilcoxon: estatistica={estatistica:.4f}  p-valor={p_valor:.4f}")
    if p_valor < 0.05:
        direcao = "menor" if diffs.median() < 0 else "maior"
        print(f"=> diferenca estatisticamente significativa (com-ia {direcao} que sem-ia).")
    else:
        print("=> sem diferenca estatisticamente significativa (p >= 0.05).")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timings", type=Path, default=Path("data/timings.csv"))
    parser.add_argument("--metrics", type=Path, default=Path("data/metrics.csv"))
    args = parser.parse_args()

    timings = carregar_timings(args.timings)
    metrics = carregar_metrics(args.metrics)

    integrantes = sorted(set(timings["integrante"]) | set(metrics["integrante"]))
    print(f"Integrantes com dados: {', '.join(integrantes)} (esperado: arthur, gabriel, pedro)")

    print("\n=========== RQ1 -- Tempo de resolucao ===========")
    resumo_e_wilcoxon(parear(timings, "tempo_min"), "time-to-green (min)", " min")

    print("\n=========== RQ2 -- Defeitos (taxa de sucesso) ===========")
    resumo_e_wilcoxon(parear(timings, "taxa_sucesso"), "taxa de sucesso")

    print("\n=========== RQ3 -- Estrutura do codigo ===========")
    resumo_e_wilcoxon(parear(metrics, "complexity_avg"), "complexidade ciclomatica media")
    resumo_e_wilcoxon(parear(metrics, "duplication_pct"), "duplicacao (%)", "%")
    resumo_e_wilcoxon(parear(metrics, "mi_avg"), "Maintainability Index")
    resumo_e_wilcoxon(parear(metrics, "sloc"), "SLOC (controle)")


if __name__ == "__main__":
    main()
