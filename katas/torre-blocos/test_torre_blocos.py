from torre_blocos import analisar_torre


def test_torre_aninhada_valida():
    assert analisar_torre("([{}])") == {
        "valida": True,
        "profundidade_maxima": 3,
        "erro_posicao": None,
    }


def test_blocos_autopareados_abrem_e_fecham():
    assert analisar_torre("||") == {
        "valida": True,
        "profundidade_maxima": 1,
        "erro_posicao": None,
    }


def test_autopareado_envolvendo_outro_bloco():
    assert analisar_torre("|()|") == {
        "valida": True,
        "profundidade_maxima": 2,
        "erro_posicao": None,
    }


def test_autopareado_abre_quando_topo_e_diferente():
    assert analisar_torre("(|)") == {
        "valida": False,
        "profundidade_maxima": 2,
        "erro_posicao": 2,
    }


def test_fechamento_de_tipo_trocado():
    assert analisar_torre("([)]") == {
        "valida": False,
        "profundidade_maxima": 2,
        "erro_posicao": 2,
    }


def test_fechamento_sem_bloco_aberto():
    assert analisar_torre(")") == {
        "valida": False,
        "profundidade_maxima": 0,
        "erro_posicao": 0,
    }


def test_blocos_que_nunca_fecham():
    assert analisar_torre("((") == {
        "valida": False,
        "profundidade_maxima": 2,
        "erro_posicao": 0,
    }


def test_caracteres_irrelevantes_sao_ignorados():
    assert analisar_torre("a(b)c") == {
        "valida": True,
        "profundidade_maxima": 1,
        "erro_posicao": None,
    }


def test_torre_vazia():
    assert analisar_torre("") == {
        "valida": True,
        "profundidade_maxima": 0,
        "erro_posicao": None,
    }


def test_sequencia_de_autopareados_lado_a_lado():
    assert analisar_torre("||||") == {
        "valida": True,
        "profundidade_maxima": 1,
        "erro_posicao": None,
    }
