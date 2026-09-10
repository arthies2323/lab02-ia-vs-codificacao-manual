"""Cronometra um trial do Lab02 e registra o time-to-green (RQ1).

O participante inicia este script no começo do trial e continua implementando a
solução na IDE. O script executa periodicamente o pytest do kata. Assim que todos
os testes de aceitação passam, o tempo decorrido é persistido em
``data/timings.csv``. Se o green não ocorrer em até 35 minutos, o trial é
encerrado e registrado como censurado exatamente em 35 minutos.

Uso:
    python scripts/timer.py \
        --kata agenda-turnos \
        --tratamento com-ia \
        --integrante gabriel

Por padrão, o alvo de testes é ``katas/<kata>`` e o time-box é fixado em 35
minutos. ``--interval-seconds`` e ``--timebox-seconds`` existem para testes do
próprio script; em trials reais, mantenha o time-box padrão de 2100 s.
"""
from __future__ import annotations

import argparse
import csv
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

TIMEBOX_SECONDS = 35 * 60
DEFAULT_INTERVAL_SECONDS = 5.0
CSV_COLUMNS = ["integrante", "kata", "tratamento", "tempo_min", "censurado"]


@dataclass(frozen=True)
class TrialResult:
    integrante: str
    kata: str
    tratamento: str
    elapsed_seconds: float
    censurado: bool

    def as_csv_row(self) -> dict[str, str]:
        tempo_min = self.elapsed_seconds / 60
        return {
            "integrante": self.integrante,
            "kata": self.kata,
            "tratamento": self.tratamento,
            "tempo_min": f"{tempo_min:.4f}",
            "censurado": "true" if self.censurado else "false",
        }


def run_pytest(test_target: Path, timeout_seconds: float | None = None) -> bool:
    """Executa pytest e retorna True somente quando toda a suíte passa."""
    cmd = [sys.executable, "-m", "pytest", str(test_target), "-q"]
    try:
        completed = subprocess.run(
            cmd,
            timeout=timeout_seconds,
            check=False,
            capture_output=True,
            text=True,
        )
    except subprocess.TimeoutExpired:
        return False

    output = "\n".join(part for part in (completed.stdout, completed.stderr) if part).strip()
    if completed.returncode != 0 and output:
        # Evita inundar o terminal a cada ciclo, mas preserva o resumo do pytest.
        tail = [line for line in output.splitlines() if line.strip()][-3:]
        print("[pytest] " + " | ".join(tail), flush=True)
    return completed.returncode == 0


def has_duplicate(out_path: Path, integrante: str, kata: str, tratamento: str) -> bool:
    """Detecta registro prévio da mesma combinação participante/kata/tratamento."""
    if not out_path.exists() or out_path.stat().st_size == 0:
        return False
    try:
        with out_path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                if (
                    row.get("integrante") == integrante
                    and row.get("kata") == kata
                    and row.get("tratamento") == tratamento
                ):
                    return True
    except (OSError, csv.Error):
        return False
    return False


def append_result(out_path: Path, result: TrialResult) -> None:
    """Acrescenta uma linha ao CSV consolidado, criando cabeçalho se necessário."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not out_path.exists() or out_path.stat().st_size == 0
    with out_path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        if write_header:
            writer.writeheader()
        writer.writerow(result.as_csv_row())


def run_trial(
    *,
    integrante: str,
    kata: str,
    tratamento: str,
    test_target: Path,
    timebox_seconds: float = TIMEBOX_SECONDS,
    interval_seconds: float = DEFAULT_INTERVAL_SECONDS,
    now: Callable[[], float] = time.monotonic,
    sleep: Callable[[float], None] = time.sleep,
    test_runner: Callable[[Path, float | None], bool] = run_pytest,
) -> TrialResult:
    """Executa o ciclo de medição até green ou até o limite do time-box."""
    started_at = now()
    attempt = 0

    while True:
        elapsed_before_test = now() - started_at
        remaining = timebox_seconds - elapsed_before_test
        if remaining <= 0:
            return TrialResult(integrante, kata, tratamento, timebox_seconds, True)

        attempt += 1
        print(
            f"[trial] tentativa {attempt} | decorrido: {elapsed_before_test / 60:.2f} min "
            f"| restante: {remaining / 60:.2f} min",
            flush=True,
        )

        green = test_runner(test_target, remaining)
        elapsed_after_test = now() - started_at

        # Green só é válido quando obtido dentro do limite experimental.
        if green and elapsed_after_test <= timebox_seconds:
            return TrialResult(integrante, kata, tratamento, elapsed_after_test, False)

        if elapsed_after_test >= timebox_seconds:
            return TrialResult(integrante, kata, tratamento, timebox_seconds, True)

        wait_for = min(interval_seconds, timebox_seconds - elapsed_after_test)
        if wait_for > 0:
            sleep(wait_for)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kata", required=True, help="Identificador do kata (ex.: agenda-turnos)")
    parser.add_argument("--tratamento", required=True, choices=["com-ia", "sem-ia"])
    parser.add_argument("--integrante", required=True, help="Nome/identificador do participante")
    parser.add_argument(
        "--tests",
        type=Path,
        help="Alvo pytest. Padrão: katas/<kata>",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("data/timings.csv"),
        help="CSV consolidado de saída (padrão: data/timings.csv)",
    )
    parser.add_argument(
        "--interval-seconds",
        type=float,
        default=DEFAULT_INTERVAL_SECONDS,
        help="Intervalo entre execuções do pytest (padrão: 5 s)",
    )
    parser.add_argument(
        "--timebox-seconds",
        type=float,
        default=TIMEBOX_SECONDS,
        help="Limite do trial. Em execução real, mantenha 2100 s (35 min).",
    )
    parser.add_argument(
        "--allow-duplicate",
        action="store_true",
        help="Permite registrar novamente a mesma combinação integrante/kata/tratamento.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.interval_seconds < 0:
        parser.error("--interval-seconds deve ser >= 0")
    if args.timebox_seconds <= 0:
        parser.error("--timebox-seconds deve ser > 0")

    test_target = args.tests or Path("katas") / args.kata
    if not test_target.exists():
        parser.error(f"alvo de testes não existe: {test_target}")

    if (
        not args.allow_duplicate
        and has_duplicate(args.out, args.integrante, args.kata, args.tratamento)
    ):
        parser.error(
            "já existe um registro para esta combinação integrante/kata/tratamento em "
            f"{args.out}. Use --allow-duplicate somente se a repetição for intencional."
        )

    print("=" * 72)
    print("LAB02 — trial iniciado")
    print(f"Integrante : {args.integrante}")
    print(f"Kata       : {args.kata}")
    print(f"Tratamento : {args.tratamento}")
    print(f"Testes     : {test_target}")
    print(f"Time-box   : {args.timebox_seconds / 60:.2f} min")
    print("=" * 72, flush=True)

    try:
        result = run_trial(
            integrante=args.integrante,
            kata=args.kata,
            tratamento=args.tratamento,
            test_target=test_target,
            timebox_seconds=args.timebox_seconds,
            interval_seconds=args.interval_seconds,
        )
    except KeyboardInterrupt:
        print("\n[trial] interrompido manualmente; nenhum dado foi gravado.", file=sys.stderr)
        return 130

    append_result(args.out, result)

    if result.censurado:
        print(f"[trial] time-box atingido. Registrado como censurado em {args.timebox_seconds / 60:.2f} min.")
    else:
        print(f"[trial] GREEN em {result.elapsed_seconds / 60:.4f} min.")
    print(f"[trial] resultado salvo em: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
