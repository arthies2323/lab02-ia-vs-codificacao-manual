def _estatisticas_iniciais(times):
    return {
        time: {"time": time, "pontos": 0, "gols_pro": 0, "gols_contra": 0, "saldo": 0}
        for time in times
    }


def _saldo_confronto(time_a, time_b, partidas):
    saldo = 0
    for casa, fora, gols_casa, gols_fora in partidas:
        if casa == time_a and fora == time_b:
            saldo += gols_casa - gols_fora
        elif casa == time_b and fora == time_a:
            saldo += gols_fora - gols_casa
    return saldo


def classificar(times, partidas):
    """Classifica os times usando os critérios definidos no README do kata."""
    tabela = _estatisticas_iniciais(times)

    for casa, fora, gols_casa, gols_fora in partidas:
        tabela[casa]["gols_pro"] += gols_casa
        tabela[casa]["gols_contra"] += gols_fora
        tabela[fora]["gols_pro"] += gols_fora
        tabela[fora]["gols_contra"] += gols_casa

        if gols_casa > gols_fora:
            tabela[casa]["pontos"] += 3
        elif gols_fora > gols_casa:
            tabela[fora]["pontos"] += 3
        else:
            tabela[casa]["pontos"] += 1
            tabela[fora]["pontos"] += 1

    for linha in tabela.values():
        linha["saldo"] = linha["gols_pro"] - linha["gols_contra"]

    linhas = sorted(
        tabela.values(),
        key=lambda linha: (-linha["pontos"], -linha["saldo"], -linha["gols_pro"]),
    )

    resultado = []
    indice = 0
    while indice < len(linhas):
        referencia = linhas[indice]
        chave = (referencia["pontos"], referencia["saldo"], referencia["gols_pro"])
        fim = indice + 1

        while fim < len(linhas):
            atual = linhas[fim]
            if (atual["pontos"], atual["saldo"], atual["gols_pro"]) != chave:
                break
            fim += 1

        grupo = linhas[indice:fim]
        if len(grupo) == 2:
            a, b = grupo
            confronto = _saldo_confronto(a["time"], b["time"], partidas)
            if confronto > 0:
                grupo = [a, b]
            elif confronto < 0:
                grupo = [b, a]
            else:
                grupo = sorted(grupo, key=lambda linha: linha["time"])
        else:
            grupo = sorted(grupo, key=lambda linha: linha["time"])

        resultado.extend(grupo)
        indice = fim

    return resultado
