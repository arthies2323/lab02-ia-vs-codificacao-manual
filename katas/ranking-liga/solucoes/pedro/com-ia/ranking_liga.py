from itertools import groupby

PONTOS_VITORIA = 3
PONTOS_EMPATE = 1


def _tabela(times, partidas):
    """Acumula pontos e gols de cada time a partir das partidas."""
    tabela = {
        time: {"time": time, "pontos": 0, "gols_pro": 0, "gols_contra": 0, "saldo": 0}
        for time in times
    }

    for casa, fora, gols_casa, gols_fora in partidas:
        for time, marcados, sofridos in (
            (casa, gols_casa, gols_fora),
            (fora, gols_fora, gols_casa),
        ):
            registro = tabela[time]
            registro["gols_pro"] += marcados
            registro["gols_contra"] += sofridos
            registro["saldo"] = registro["gols_pro"] - registro["gols_contra"]
            if marcados > sofridos:
                registro["pontos"] += PONTOS_VITORIA
            elif marcados == sofridos:
                registro["pontos"] += PONTOS_EMPATE

    return tabela


def _saldo_confronto(partidas, um, outro):
    """Saldo de gols de ``um`` contra ``outro`` somando só os jogos entre eles."""
    saldo = 0
    for casa, fora, gols_casa, gols_fora in partidas:
        if casa == um and fora == outro:
            saldo += gols_casa - gols_fora
        elif casa == outro and fora == um:
            saldo += gols_fora - gols_casa
    return saldo


def classificar(times, partidas):
    """Classifica os times da liga. Ver README.md do kata."""
    tabela = _tabela(times, partidas)

    # Ordena pelos três primeiros critérios; o nome entra como desempate final
    # e já deixa cada grupo de empatados em ordem alfabética.
    ordenado = sorted(
        tabela.values(),
        key=lambda r: (-r["pontos"], -r["saldo"], -r["gols_pro"], r["time"]),
    )

    classificacao = []
    for _, empatados in groupby(
        ordenado, key=lambda r: (r["pontos"], r["saldo"], r["gols_pro"])
    ):
        grupo = list(empatados)
        # Confronto direto só vale para grupos de exatamente dois times; nos
        # demais casos a ordem alfabética do sorted acima já é a resposta.
        if len(grupo) == 2:
            if _saldo_confronto(partidas, grupo[0]["time"], grupo[1]["time"]) < 0:
                grupo.reverse()
        classificacao.extend(grupo)

    return classificacao
