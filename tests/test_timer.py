from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("lab02_timer", ROOT / "scripts" / "timer.py")
assert SPEC is not None and SPEC.loader is not None
timer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = timer
SPEC.loader.exec_module(timer)


class FakeClock:
    def __init__(self) -> None:
        self.value = 0.0

    def now(self) -> float:
        return self.value

    def sleep(self, seconds: float) -> None:
        self.value += seconds


def test_green_registra_tempo_real() -> None:
    clock = FakeClock()
    calls = 0

    def runner(_target: Path, _remaining: float | None) -> bool:
        nonlocal calls
        calls += 1
        clock.value += 1.0  # custo da execução dos testes
        return calls == 3

    result = timer.run_trial(
        integrante="gabriel",
        kata="kata-x",
        tratamento="com-ia",
        test_target=Path("."),
        timebox_seconds=30,
        interval_seconds=2,
        now=clock.now,
        sleep=clock.sleep,
        test_runner=runner,
    )

    assert result.censurado is False
    assert result.elapsed_seconds == 7.0


def test_timebox_registra_censura_no_limite_exato() -> None:
    clock = FakeClock()

    def runner(_target: Path, _remaining: float | None) -> bool:
        clock.value += 1.0
        return False

    result = timer.run_trial(
        integrante="gabriel",
        kata="kata-y",
        tratamento="sem-ia",
        test_target=Path("."),
        timebox_seconds=5,
        interval_seconds=2,
        now=clock.now,
        sleep=clock.sleep,
        test_runner=runner,
    )

    assert result.censurado is True
    assert result.elapsed_seconds == 5


def test_append_result_cria_csv_compativel_com_data_readme(tmp_path: Path) -> None:
    out = tmp_path / "timings.csv"
    result = timer.TrialResult("gabriel", "agenda-turnos", "com-ia", 90.0, False)
    timer.append_result(out, result)

    with out.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert list(rows[0].keys()) == timer.CSV_COLUMNS
    assert rows[0]["integrante"] == "gabriel"
    assert rows[0]["kata"] == "agenda-turnos"
    assert rows[0]["tratamento"] == "com-ia"
    assert rows[0]["tempo_min"] == "1.5000"
    assert rows[0]["censurado"] == "false"


def test_censurado_e_serializado_com_35_minutos() -> None:
    result = timer.TrialResult("gabriel", "agenda-turnos", "sem-ia", 2100.0, True)
    assert result.as_csv_row()["tempo_min"] == "35.0000"
    assert result.as_csv_row()["censurado"] == "true"
