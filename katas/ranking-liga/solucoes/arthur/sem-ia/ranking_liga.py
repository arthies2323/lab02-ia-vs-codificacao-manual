def classificar(times, partidas):
    tabela = {}

    for time in times:
        tabela[time] = {
            "time": time,
            "pontos": 0,
            "gols_pro": 0,
            "gols_contra": 0,
            "saldo": 0
        }

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

    for time in times:
        tabela[time]["saldo"] = (
            tabela[time]["gols_pro"] - tabela[time]["gols_contra"]
        )

    classificacao = list(tabela.values())

    classificacao.sort(
        key=lambda time: (
            -time["pontos"],
            -time["saldo"],
            -time["gols_pro"],
            time["time"]
        )
    )

    resultado = []
    i = 0

    while i < len(classificacao):
        grupo = [classificacao[i]]
        j = i + 1

        while j < len(classificacao):
            atual = classificacao[i]
            proximo = classificacao[j]

            if (
                atual["pontos"] == proximo["pontos"]
                and atual["saldo"] == proximo["saldo"]
                and atual["gols_pro"] == proximo["gols_pro"]
            ):
                grupo.append(proximo)
                j += 1
            else:
                break

        if len(grupo) == 2:
            time1 = grupo[0]
            time2 = grupo[1]

            saldo_confronto = 0
            se_enfrentaram = False

            for casa, fora, gols_casa, gols_fora in partidas:
                if casa == time1["time"] and fora == time2["time"]:
                    saldo_confronto += gols_casa - gols_fora
                    se_enfrentaram = True
                elif casa == time2["time"] and fora == time1["time"]:
                    saldo_confronto += gols_fora - gols_casa
                    se_enfrentaram = True

            if se_enfrentaram and saldo_confronto < 0:
                grupo[0], grupo[1] = grupo[1], grupo[0]

        resultado.extend(grupo)
        i = j

    return resultado
