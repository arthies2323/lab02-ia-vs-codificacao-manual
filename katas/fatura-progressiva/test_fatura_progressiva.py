import pytest

from fatura_progressiva import calcular_fatura

FAIXAS = [(100, 0.5), (200, 0.8), (None, 1.2)]


def test_consumo_dentro_da_primeira_faixa():
    assert calcular_fatura(50, FAIXAS) == {
        "total": 25.0,
        "detalhe": [(0, 50, 25.0)],
        "retroativo": False,
    }


def test_consumo_atravessa_duas_faixas():
    assert calcular_fatura(150, FAIXAS) == {
        "total": 90.0,
        "detalhe": [(0, 100, 50.0), (1, 50, 40.0)],
        "retroativo": False,
    }


def test_consumo_atravessa_todas_as_faixas():
    assert calcular_fatura(250, FAIXAS) == {
        "total": 190.0,
        "detalhe": [(0, 100, 50.0), (1, 100, 80.0), (2, 50, 60.0)],
        "retroativo": False,
    }


def test_limite_da_faixa_e_exclusivo():
    assert calcular_fatura(100, FAIXAS) == {
        "total": 50.0,
        "detalhe": [(0, 100, 50.0)],
        "retroativo": False,
    }


def test_consumo_zero():
    assert calcular_fatura(0, FAIXAS) == {
        "total": 0,
        "detalhe": [],
        "retroativo": False,
    }


def test_bonus_retroativo_substitui_o_calculo_progressivo():
    assert calcular_fatura(250, FAIXAS, bonus_limite=200) == {
        "total": 125.0,
        "detalhe": [(0, 250, 125.0)],
        "retroativo": True,
    }


def test_bonus_nao_dispara_no_limite_exato():
    assert calcular_fatura(200, FAIXAS, bonus_limite=200) == {
        "total": 130.0,
        "detalhe": [(0, 100, 50.0), (1, 100, 80.0)],
        "retroativo": False,
    }


def test_bonus_none_nunca_dispara():
    resultado = calcular_fatura(10_000, FAIXAS, bonus_limite=None)
    assert resultado["retroativo"] is False
    assert resultado["total"] == pytest.approx(50.0 + 80.0 + 9_800 * 1.2)


def test_faixa_unica_ilimitada():
    assert calcular_fatura(30, [(None, 2.0)]) == {
        "total": 60.0,
        "detalhe": [(0, 30, 60.0)],
        "retroativo": False,
    }
