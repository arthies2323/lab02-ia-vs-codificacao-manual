"""Verifica se o ambiente do Lab02S01 está pronto para as Issues #3 e #4.

Uso:
    python scripts/check_environment.py

Retorna código 0 quando os itens obrigatórios estão disponíveis e código 1
quando há alguma pendência. A presença de ``jscpd`` direto OU de ``npx`` é
aceita, pois ``collect_static_metrics.py`` suporta os dois caminhos.
"""
from __future__ import annotations

import importlib
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Check:
    name: str
    ok: bool
    detail: str


def check_python() -> Check:
    ok = sys.version_info >= (3, 10)
    return Check("Python >= 3.10", ok, sys.version.split()[0])


def check_module(module_name: str) -> Check:
    try:
        module = importlib.import_module(module_name)
        version = getattr(module, "__version__", "instalado")
        return Check(f"Python: {module_name}", True, str(version))
    except Exception as exc:  # diagnóstico de ambiente; exibe a causa real
        return Check(f"Python: {module_name}", False, str(exc))


def check_duplication_tool() -> Check:
    direct = shutil.which("jscpd")
    if direct:
        return Check("Duplicação: jscpd", True, direct)
    npx = shutil.which("npx")
    if npx:
        return Check("Duplicação: jscpd/npx", True, f"npx disponível em {npx}")
    return Check(
        "Duplicação: jscpd/npx",
        False,
        "instale Node.js/npm ou jscpd; collect_static_metrics.py precisa de jscpd ou npx",
    )


def check_project_layout(root: Path) -> list[Check]:
    required = [
        root / "katas",
        root / "scripts" / "timer.py",
        root / "scripts" / "collect_static_metrics.py",
        root / "scripts" / "requirements.txt",
        root / "data",
    ]
    return [Check(f"Projeto: {path.relative_to(root)}", path.exists(), str(path)) for path in required]


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    checks = [
        check_python(),
        check_module("pytest"),
        check_module("radon"),
        check_module("pandas"),
        check_duplication_tool(),
        *check_project_layout(root),
    ]

    print("LAB02S01 — validação do ambiente (#3 e #4)\n")
    for item in checks:
        status = "OK" if item.ok else "FALHA"
        print(f"[{status:5}] {item.name}: {item.detail}")

    failures = [item for item in checks if not item.ok]
    if failures:
        print("\nAmbiente incompleto. Corrija os itens marcados como FALHA.")
        return 1

    print("\nAmbiente pronto para cronometragem e coleta de métricas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
