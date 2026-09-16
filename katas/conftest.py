"""Seleciona qual slot de solução entra no ``sys.path`` durante um trial.

Cada kata guarda 6 slots independentes em
``solucoes/<integrante>/<tratamento>/``. Os testes de aceitação importam o
módulo pelo nome (``from agenda_turnos import consolidar_turnos``), então
exatamente um slot por kata é publicado no ``sys.path`` antes da coleta — é
isso que faz o mesmo arquivo de teste valer para os 6 trials sem ser editado.

Como escolher o slot (a opção de linha de comando tem precedência sobre a
variável de ambiente):

    python -m pytest katas/agenda-turnos --integrante pedro --tratamento sem-ia

    KATA_INTEGRANTE=pedro KATA_TRATAMENTO=sem-ia python -m pytest katas

``scripts/timer.py`` exporta as duas variáveis automaticamente a partir de
``--integrante``/``--tratamento``, então em trials reais não é preciso repetir
a seleção na mão.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

KATAS_DIR = Path(__file__).parent
TRATAMENTOS = ("com-ia", "sem-ia")


def pytest_addoption(parser: pytest.Parser) -> None:
    grupo = parser.getgroup("lab02", "seleção do trial (Lab02)")
    grupo.addoption(
        "--integrante",
        action="store",
        default=None,
        help="Integrante cujo slot de solução será testado (ou KATA_INTEGRANTE).",
    )
    grupo.addoption(
        "--tratamento",
        action="store",
        default=None,
        choices=TRATAMENTOS,
        help="Tratamento do trial: com-ia ou sem-ia (ou KATA_TRATAMENTO).",
    )


def integrantes_disponiveis() -> list[str]:
    """Nomes de integrante presentes em ``katas/*/solucoes/``."""
    nomes: set[str] = set()
    for kata_dir in KATAS_DIR.iterdir():
        solucoes = kata_dir / "solucoes"
        if solucoes.is_dir():
            nomes.update(slot.name for slot in solucoes.iterdir() if slot.is_dir())
    return sorted(nomes)


def _selecao(config: pytest.Config) -> tuple[str, str]:
    integrante = config.getoption("--integrante") or os.environ.get("KATA_INTEGRANTE", "")
    tratamento = config.getoption("--tratamento") or os.environ.get("KATA_TRATAMENTO", "")
    return integrante.strip().lower(), tratamento.strip().lower()


def pytest_configure(config: pytest.Config) -> None:
    integrante, tratamento = _selecao(config)
    conhecidos = integrantes_disponiveis()

    if not integrante or not tratamento:
        raise pytest.UsageError(
            "os testes dos katas precisam saber de quem é o trial. Informe "
            "--integrante e --tratamento (ou KATA_INTEGRANTE/KATA_TRATAMENTO). "
            f"Integrantes: {', '.join(conhecidos)}. Tratamentos: {', '.join(TRATAMENTOS)}."
        )
    if tratamento not in TRATAMENTOS:
        raise pytest.UsageError(
            f"tratamento inválido: {tratamento!r}. Use {' ou '.join(TRATAMENTOS)}."
        )
    if integrante not in conhecidos:
        raise pytest.UsageError(
            f"integrante sem slot de solução: {integrante!r}. "
            f"Disponíveis: {', '.join(conhecidos)}."
        )

    slots = []
    for kata_dir in sorted(KATAS_DIR.iterdir()):
        slot = kata_dir / "solucoes" / integrante / tratamento
        if slot.is_dir():
            sys.path.insert(0, str(slot))
            slots.append(slot)

    if not slots:
        raise pytest.UsageError(
            f"nenhum slot encontrado para {integrante}/{tratamento} em {KATAS_DIR}."
        )

    config.stash_lab02 = (integrante, tratamento, slots)  # type: ignore[attr-defined]


def pytest_report_header(config: pytest.Config) -> list[str]:
    selecao = getattr(config, "stash_lab02", None)
    if selecao is None:
        return []
    integrante, tratamento, slots = selecao
    return [f"lab02: trial de {integrante} / {tratamento} ({len(slots)} kata(s) no sys.path)"]
