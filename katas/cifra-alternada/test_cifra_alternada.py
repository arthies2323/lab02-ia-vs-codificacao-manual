import pytest

from cifra_alternada import cifrar, decifrar


def test_deslocamento_simples_primeira_palavra():
    assert cifrar("abc", [1]) == "bcd"


def test_segunda_palavra_desloca_para_tras():
    assert cifrar("ab cd", [1]) == "bc bc"


def test_chave_cicla_dentro_da_palavra():
    assert cifrar("az", [1, 2]) == "bb"


def test_separador_encerra_a_palavra():
    assert cifrar("a-b", [1]) == "b-a"


def test_contador_reinicia_a_cada_palavra():
    assert cifrar("ax ax ax", [1, 5]) == "bc zs bc"


def test_caixa_preservada():
    assert cifrar("AbZ", [1]) == "BcA"


def test_caracteres_nao_alfabeticos_passam_intactos():
    assert cifrar("a1! b", [2]) == "c1! z"


def test_texto_vazio():
    assert cifrar("", [1]) == ""
    assert decifrar("", [1]) == ""


@pytest.mark.parametrize(
    "texto, chave",
    [
        ("Ola Mundo", [3, 1]),
        ("teste com varias palavras", [7]),
        ("Ha 2 casos-limite, aqui!", [5, 11, 2]),
    ],
)
def test_decifrar_inverte_cifrar(texto, chave):
    assert decifrar(cifrar(texto, chave), chave) == texto
