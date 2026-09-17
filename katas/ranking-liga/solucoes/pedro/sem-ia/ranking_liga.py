PONTOS_VITORIA = 3
PONTOS_EMPATE = 1


def vem_antes(a, b):
    if a["pontos"] != b["pontos"]:
        return a["pontos"] > b["pontos"]
    if a["saldo"] != b["saldo"]:
        return a["saldo"] > b["saldo"]
    if a["gols_pro"] != b["gols_pro"]:
        return a["gols_pro"] > b["gols_pro"]
    return a["time"] < b["time"]


def empatados(a, b):
    return a["pontos"] == b["pontos"] and a["saldo"] == b["saldo"] and a["gols_pro"] == b["gols_pro"]


def confronto_direto(partidas, casa, fora):
    saldo = 0
    index = 0
    while index < len(partidas):
        if partidas[index][0] == casa and partidas[index][1] == fora:
            saldo += partidas[index][2] - partidas[index][3]
        elif partidas[index][0] == fora and partidas[index][1] == casa:
            saldo += partidas[index][3] - partidas[index][2]
        index += 1
    return saldo


def classificar(times, partidas):
    tabela = []
    index = 0
    while index < len(times):
        tabela.append({"time": times[index], "pontos": 0, "gols_pro": 0, "gols_contra": 0, "saldo": 0})
        index += 1

    index = 0
    while index < len(partidas):
        casa = None
        fora = None
        pos = 0
        while pos < len(tabela):
            if tabela[pos]["time"] == partidas[index][0]:
                casa = tabela[pos]
            if tabela[pos]["time"] == partidas[index][1]:
                fora = tabela[pos]
            pos += 1
        gols_casa = partidas[index][2]
        gols_fora = partidas[index][3]
        casa["gols_pro"] += gols_casa
        casa["gols_contra"] += gols_fora
        fora["gols_pro"] += gols_fora
        fora["gols_contra"] += gols_casa
        if gols_casa > gols_fora:
            casa["pontos"] += PONTOS_VITORIA
        elif gols_fora > gols_casa:
            fora["pontos"] += PONTOS_VITORIA
        else:
            casa["pontos"] += PONTOS_EMPATE
            fora["pontos"] += PONTOS_EMPATE
        index += 1

    index = 0
    while index < len(tabela):
        tabela[index]["saldo"] = tabela[index]["gols_pro"] - tabela[index]["gols_contra"]
        index += 1

    index = 0
    while index < len(tabela):
        melhor = index
        pos = index + 1
        while pos < len(tabela):
            if vem_antes(tabela[pos], tabela[melhor]):
                melhor = pos
            pos += 1
        tabela[index], tabela[melhor] = tabela[melhor], tabela[index]
        index += 1

    index = 0
    while index < len(tabela):
        fim = index
        while fim + 1 < len(tabela) and empatados(tabela[fim + 1], tabela[index]):
            fim += 1
        if fim - index == 1:
            saldo = confronto_direto(partidas, tabela[index]["time"], tabela[fim]["time"])
            if saldo < 0:
                tabela[index], tabela[fim] = tabela[fim], tabela[index]
        index = fim + 1
    return tabela