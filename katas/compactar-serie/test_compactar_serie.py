import pytest

from compactar_serie import compactar, expandir


def test_sequencia_de_tres_e_compactada():
    assert compactar("aaabb") == "3*abb"


def test_sequencia_de_dois_fica_literal():
    assert compactar("aa") == "aa"


def test_digitos_avulsos_sao_escapados():
    assert compactar("a11") == "a\\1\\1"


def test_sequencia_longa_de_digitos_e_compactada_sem_escape():
    assert compactar("1111") == "4*1"


def test_asterisco_avulso_e_escapado():
    assert compactar("**") == "\\*\\*"


def test_barra_invertida_avulsa_e_escapada():
    assert compactar("\\") == "\\\\"


def test_contagem_com_mais_de_um_digito():
    assert compactar("a" * 12) == "12*a"


def test_serie_vazia():
    assert compactar("") == ""
    assert expandir("") == ""


def test_expandir_casos_diretos():
    assert expandir("3*abb") == "aaabb"
    assert expandir("a\\1\\1") == "a11"
    assert expandir("12*a") == "a" * 12


@pytest.mark.parametrize(
    "serie",
    [
        "aaabb",
        "a11",
        "**",
        "aaa***111bb\\\\\\",
        "xxxxyz1122333",
    ],
)
def test_expandir_inverte_compactar(serie):
    assert expandir(compactar(serie)) == serie
