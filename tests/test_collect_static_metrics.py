from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "collect_static_metrics", ROOT / "scripts" / "collect_static_metrics.py"
)
assert SPEC is not None and SPEC.loader is not None
metrics = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = metrics
SPEC.loader.exec_module(metrics)


def test_append_row_preserva_schema_da_issue_4(tmp_path: Path) -> None:
    out = tmp_path / "metrics.csv"
    row = {
        "timestamp": "2026-09-10T10:00:00+00:00",
        "integrante": "gabriel",
        "kata": "agenda-turnos",
        "tratamento": "com-ia",
        "loc": 20,
        "sloc": 16,
        "complexity_avg": 3.5,
        "mi_avg": 75.0,
        "duplication_pct": 0.0,
    }

    metrics.append_row(out, row)

    with out.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        saved = next(reader)

    assert reader.fieldnames == metrics.CSV_COLUMNS
    assert saved["integrante"] == "gabriel"
    assert saved["complexity_avg"] == "3.5"
    assert saved["duplication_pct"] == "0.0"


def test_collect_agrega_metricas_sem_dependencia_de_subprocess(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(metrics, "run_radon_raw", lambda _path: {"loc": 30, "sloc": 24})
    monkeypatch.setattr(metrics, "run_radon_cc", lambda _path: 4.25)
    monkeypatch.setattr(metrics, "run_radon_mi", lambda _path: 71.2)
    monkeypatch.setattr(metrics, "run_jscpd", lambda _path: 3.0)

    result = metrics.collect(tmp_path)

    assert result == {
        "loc": 30,
        "sloc": 24,
        "complexity_avg": 4.25,
        "mi_avg": 71.2,
        "duplication_pct": 3.0,
    }
