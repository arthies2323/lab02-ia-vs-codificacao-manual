"""Coleta métricas estáticas (RQ3) sobre a solução final de um trial.

Roda Radon (complexidade ciclomática, LOC, Maintainability Index) e, se
disponível, jscpd (duplicação de código) sobre um diretório com o código de
um trial, e acrescenta uma linha em um CSV consolidado.

Uso:
    python scripts/collect_static_metrics.py \
        --path katas/fizzbuzz-variante/solucao \
        --kata fizzbuzz-variante \
        --integrante arthur \
        --tratamento com-ia \
        --out data/metrics.csv
"""
from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

CSV_COLUMNS = [
    "timestamp",
    "integrante",
    "kata",
    "tratamento",
    "loc",
    "sloc",
    "complexity_avg",
    "mi_avg",
    "duplication_pct",
]


def run_radon_raw(path: Path) -> dict:
    out = subprocess.run(
        [sys.executable, "-m", "radon", "raw", "-j", str(path)],
        capture_output=True, text=True, check=True,
    )
    data = json.loads(out.stdout)
    loc = sloc = 0
    for file_metrics in data.values():
        if isinstance(file_metrics, dict):
            loc += file_metrics.get("loc", 0)
            sloc += file_metrics.get("sloc", 0)
    return {"loc": loc, "sloc": sloc}


def run_radon_cc(path: Path) -> float | None:
    out = subprocess.run(
        [sys.executable, "-m", "radon", "cc", "-j", str(path)],
        capture_output=True, text=True, check=True,
    )
    data = json.loads(out.stdout)
    complexities = [
        block["complexity"]
        for blocks in data.values()
        for block in blocks
        if isinstance(block, dict) and "complexity" in block
    ]
    if not complexities:
        return None
    return sum(complexities) / len(complexities)


def run_radon_mi(path: Path) -> float | None:
    out = subprocess.run(
        [sys.executable, "-m", "radon", "mi", "-j", str(path)],
        capture_output=True, text=True, check=True,
    )
    data = json.loads(out.stdout)
    scores = []
    for value in data.values():
        if isinstance(value, dict) and "mi" in value:
            scores.append(value["mi"])
        elif isinstance(value, (int, float)):
            scores.append(value)
    if not scores:
        return None
    return sum(scores) / len(scores)


def run_jscpd(path: Path) -> float | None:
    """Retorna % de linhas duplicadas via jscpd, ou None se jscpd não estiver instalado."""
    jscpd_direct = shutil.which("jscpd")
    npx_bin = shutil.which("npx")
    if jscpd_direct is None and npx_bin is None:
        print("[aviso] jscpd não encontrado (npm install -g jscpd) — pulando duplicação.", file=sys.stderr)
        return None

    with tempfile.TemporaryDirectory() as tmp_dir:
        cmd = [jscpd_direct] if jscpd_direct else [npx_bin, "--yes", "jscpd"]
        cmd += [str(path), "--reporters", "json", "--output", tmp_dir, "--silent"]
        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as exc:
            print(f"[aviso] jscpd falhou: {exc}. Pulando duplicação.", file=sys.stderr)
            return None

        report_path = Path(tmp_dir) / "jscpd-report.json"
        if not report_path.exists():
            return None
        report = json.loads(report_path.read_text(encoding="utf-8"))
        return report.get("statistics", {}).get("total", {}).get("percentage")


def collect(path: Path) -> dict:
    raw = run_radon_raw(path)
    return {
        "loc": raw["loc"],
        "sloc": raw["sloc"],
        "complexity_avg": run_radon_cc(path),
        "mi_avg": run_radon_mi(path),
        "duplication_pct": run_jscpd(path),
    }


def append_row(out_path: Path, row: dict) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    file_exists = out_path.exists()
    with out_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", required=True, type=Path, help="Diretório com o código do trial")
    parser.add_argument("--kata", required=True, help="Nome/identificador do kata")
    parser.add_argument("--integrante", required=True, help="Nome do integrante que resolveu o trial")
    parser.add_argument("--tratamento", required=True, choices=["com-ia", "sem-ia"])
    parser.add_argument("--out", default=Path("data/metrics.csv"), type=Path, help="CSV consolidado de saída")
    args = parser.parse_args()

    if not args.path.exists():
        parser.error(f"path não existe: {args.path}")

    metrics = collect(args.path)
    row = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "integrante": args.integrante,
        "kata": args.kata,
        "tratamento": args.tratamento,
        **metrics,
    }
    append_row(args.out, row)
    print(f"Métricas registradas em {args.out}: {row}")


if __name__ == "__main__":
    main()
