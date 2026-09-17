def classificar(times, partidas):
    """Monta e ordena a tabela da liga."""
    dados = {}
    for time in times:
        dados[time] = {
            "time": time,
            "pontos": 0,
            "gols_pro": 0,
            "gols_contra": 0,
            "saldo": 0,
        }

    for casa, fora, gols_casa, gols_fora in partidas:
        dados[casa]["gols_pro"] += gols_casa
        dados[casa]["gols_contra"] += gols_fora
        dados[fora]["gols_pro"] += gols_fora
        dados[fora]["gols_contra"] += gols_casa

        if gols_casa == gols_fora:
            dados[casa]["pontos"] += 1
            dados[fora]["pontos"] += 1
        elif gols_casa > gols_fora:
            dados[casa]["pontos"] += 3
        else:
            dados[fora]["pontos"] += 3

    for time in times:
        dados[time]["saldo"] = dados[time]["gols_pro"] - dados[time]["gols_contra"]

    tabela = list(dados.values())
    tabela.sort(key=lambda x: (-x["pontos"], -x["saldo"], -x["gols_pro"], x["time"]))

    resposta = []
    i = 0

    while i < len(tabela):
        j = i + 1
        while (
            j < len(tabela)
            and tabela[j]["pontos"] == tabela[i]["pontos"]
            and tabela[j]["saldo"] == tabela[i]["saldo"]
            and tabela[j]["gols_pro"] == tabela[i]["gols_pro"]
        ):
            j += 1

        grupo = tabela[i:j]

        if len(grupo) == 2:
            primeiro = grupo[0]
            segundo = grupo[1]
            saldo_direto = 0
            houve_confronto = False

            for casa, fora, gc, gf in partidas:
                if casa == primeiro["time"] and fora == segundo["time"]:
                    saldo_direto += gc - gf
                    houve_confronto = True
                elif casa == segundo["time"] and fora == primeiro["time"]:
                    saldo_direto += gf - gc
                    houve_confronto = True

            if houve_confronto and saldo_direto < 0:
                grupo = [segundo, primeiro]
            elif not houve_confronto or saldo_direto == 0:
                grupo.sort(key=lambda x: x["time"])
        else:
            grupo.sort(key=lambda x: x["time"])

        resposta.extend(grupo)
        i = j

    return resposta
