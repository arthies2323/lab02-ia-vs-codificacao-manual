from itertools import groupby


def classificar(times, partidas):
    """Classifica os times da liga. Ver README.md do kata."""
    stats = {
        nome: {"pontos": 0, "gols_pro": 0, "gols_contra": 0}
        for nome in times
    }

    for casa, fora, gols_casa, gols_fora in partidas:
        stats[casa]["gols_pro"] += gols_casa
        stats[casa]["gols_contra"] += gols_fora
        stats[fora]["gols_pro"] += gols_fora
        stats[fora]["gols_contra"] += gols_casa
        if gols_casa > gols_fora:
            stats[casa]["pontos"] += 3
        elif gols_fora > gols_casa:
            stats[fora]["pontos"] += 3
        else:
            stats[casa]["pontos"] += 1
            stats[fora]["pontos"] += 1

    def chave_principal(nome):
        s = stats[nome]
        saldo = s["gols_pro"] - s["gols_contra"]
        return (-s["pontos"], -saldo, -s["gols_pro"])

    def saldo_confronto(nome_a, nome_b):
        saldo = 0
        for casa, fora, gols_casa, gols_fora in partidas:
            if casa == nome_a and fora == nome_b:
                saldo += gols_casa - gols_fora
            elif casa == nome_b and fora == nome_a:
                saldo += gols_fora - gols_casa
        return saldo

    ordenados = sorted(times, key=chave_principal)

    resultado_ordem = []
    for _, grupo in groupby(ordenados, key=chave_principal):
        bloco = list(grupo)
        if len(bloco) == 2:
            a, b = bloco
            saldo = saldo_confronto(a, b)
            if saldo > 0:
                bloco = [a, b]
            elif saldo < 0:
                bloco = [b, a]
            else:
                bloco = sorted(bloco)
        else:
            bloco = sorted(bloco)
        resultado_ordem.extend(bloco)

    return [
        {
            "time": nome,
            "pontos": stats[nome]["pontos"],
            "gols_pro": stats[nome]["gols_pro"],
            "gols_contra": stats[nome]["gols_contra"],
            "saldo": stats[nome]["gols_pro"] - stats[nome]["gols_contra"],
        }
        for nome in resultado_ordem
    ]
