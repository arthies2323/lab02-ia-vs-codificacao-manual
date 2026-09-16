"""Garante que os 4 katas mantenham os 6 slots de solução e o registro de tempo.

O desenho depende de cada kata ter exatamente um slot por integrante x
tratamento: é isso que permite os 3 integrantes resolverem o mesmo kata com e
sem IA sem colisão, e é o caminho que ``collect_static_metrics.py`` recebe em
``--path``. Um slot faltando só apareceria no meio de um trial cronometrado.

Estes testes olham só para a estrutura, nunca para o conteúdo das soluções —
continuam verdes antes, durante e depois dos trials.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
KATAS = ROOT / "katas"
INTEGRANTES = ("arthur", "gabriel", "pedro")
TRATAMENTOS = ("com-ia", "sem-ia")
SLUGS = (
    "agenda-turnos",
    "compactar-serie",
    "fatura-progressiva",
    "ranking-liga",
)
SLOTS = [(integrante, tratamento) for integrante in INTEGRANTES for tratamento in TRATAMENTOS]


def carregar_conftest():
    """Importa katas/conftest.py fora do pytest, só para testar a resolução."""
    spec = importlib.util.spec_from_file_location("lab02_katas_conftest", KATAS / "conftest.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def modulo_esperado(slug: str) -> str:
    """O módulo que o teste de aceitação importa, deduzido de test_<modulo>.py."""
    testes = list((KATAS / slug).glob("test_*.py"))
    assert len(testes) == 1, f"{slug} deveria ter exatamente um arquivo de teste"
    return testes[0].stem[len("test_") :] + ".py"


def test_os_quatro_katas_estao_presentes() -> None:
    encontrados = sorted(p.name for p in KATAS.iterdir() if p.is_dir() and p.name != "__pycache__")
    assert encontrados == sorted(SLUGS)


@pytest.mark.parametrize("slug", SLUGS)
def test_kata_tem_registro_de_tempo_na_raiz(slug: str) -> None:
    tempos = KATAS / slug / "TEMPOS.md"
    assert tempos.is_file(), f"{slug} sem TEMPOS.md na raiz"

    conteudo = tempos.read_text(encoding="utf-8")
    for integrante, tratamento in SLOTS:
        assert f"| {integrante} | {tratamento} |" in conteudo, (
            f"{slug}/TEMPOS.md sem linha para {integrante}/{tratamento}"
        )


@pytest.mark.parametrize("slug", SLUGS)
def test_kata_tem_um_slot_por_integrante_e_tratamento(slug: str) -> None:
    solucoes = KATAS / slug / "solucoes"
    assert solucoes.is_dir(), f"{slug} sem diretório solucoes/"

    # O arquivo de teste é um só para os 6 slots: o módulo importado tem de
    # existir em todos eles, independentemente de já estar implementado.
    modulo = modulo_esperado(slug)
    for integrante, tratamento in SLOTS:
        slot = solucoes / integrante / tratamento
        assert slot.is_dir(), f"slot ausente: {slot.relative_to(ROOT)}"
        assert (slot / modulo).is_file(), f"{slot.relative_to(ROOT)} sem {modulo}"


@pytest.mark.parametrize("slug", SLUGS)
def test_kata_nao_guarda_o_diretorio_solucao_antigo(slug: str) -> None:
    antigo = KATAS / slug / "solucao"
    assert not antigo.exists(), (
        f"{slug}/solucao/ foi substituído por solucoes/<integrante>/<tratamento>/"
    )


def test_conftest_lista_os_integrantes_dos_slots() -> None:
    conftest = carregar_conftest()
    assert conftest.integrantes_disponiveis() == sorted(INTEGRANTES)
    assert sorted(conftest.TRATAMENTOS) == sorted(TRATAMENTOS)
