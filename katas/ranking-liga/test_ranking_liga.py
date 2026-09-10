from ranking_liga import classificar


def nomes(tabela):
    return [linha["time"] for linha in tabela]


def test_pontuacao_por_vitoria_empate_e_derrota():
    tabela = classificar(
        ["A", "B", "C"],
        [("A", "B", 1, 0), ("B", "C", 2, 2)],
    )
    pontos = {linha["time"]: linha["pontos"] for linha in tabela}
    assert pontos == {"A": 3, "B": 1, "C": 1}


def test_linha_completa_do_time():
    tabela = classificar(["A", "B"], [("A", "B", 3, 1)])
    assert tabela[0] == {
        "time": "A",
        "pontos": 3,
        "gols_pro": 3,
        "gols_contra": 1,
        "saldo": 2,
    }


def test_desempate_por_saldo_de_gols():
    tabela = classificar(
        ["A", "B", "C"],
        [("A", "C", 5, 0), ("B", "C", 1, 0)],
    )
    assert nomes(tabela) == ["A", "B", "C"]


def test_desempate_por_gols_pro_com_saldo_igual():
    tabela = classificar(
        ["A", "B", "C", "D"],
        [("A", "C", 3, 2), ("B", "D", 1, 0)],
    )
    assert nomes(tabela)[:2] == ["A", "B"]


def test_confronto_direto_decide_entre_dois_empatados():
    # Zebras e Antas empatam em pontos (3), saldo (0) e gols pro (2).
    # O confronto direto (Zebras 2 x 1 Antas) coloca Zebras na frente,
    # contrariando a ordem alfabetica.
    tabela = classificar(
        ["Zebras", "Antas", "Cinzas", "Dourados"],
        [
            ("Zebras", "Antas", 2, 1),
            ("Antas", "Cinzas", 1, 0),
            ("Zebras", "Dourados", 0, 1),
        ],
    )
    assert nomes(tabela) == ["Dourados", "Zebras", "Antas", "Cinzas"]


def test_confronto_direto_empatado_cai_na_ordem_alfabetica():
    tabela = classificar(
        ["Zebras", "Antas"],
        [("Zebras", "Antas", 1, 1)],
    )
    assert nomes(tabela) == ["Antas", "Zebras"]


def test_grupo_de_tres_empatados_usa_ordem_alfabetica():
    tabela = classificar(
        ["Cs", "As", "Bs"],
        [("As", "Bs", 1, 1), ("Bs", "Cs", 1, 1), ("Cs", "As", 1, 1)],
    )
    assert nomes(tabela) == ["As", "Bs", "Cs"]


def test_time_sem_partidas_fica_zerado():
    tabela = classificar(["A", "B"], [])
    assert tabela == [
        {"time": "A", "pontos": 0, "gols_pro": 0, "gols_contra": 0, "saldo": 0},
        {"time": "B", "pontos": 0, "gols_pro": 0, "gols_contra": 0, "saldo": 0},
    ]


def test_confronto_direto_nao_se_aplica_quando_ha_diferenca_de_pontos():
    tabela = classificar(
        ["A", "B"],
        [("A", "B", 0, 1), ("A", "B", 0, 1)],
    )
    assert nomes(tabela) == ["B", "A"]
