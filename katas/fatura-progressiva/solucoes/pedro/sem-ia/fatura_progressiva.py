def calcular_fatura(consumo, faixas, bonus_limite=None):
    """Calcula a fatura por faixas progressivas. Ver README.md do kata."""
    if consumo == 0:
        return {"total": 0, "detalhe": [], "retroativo": False}

    if bonus_limite is not None and consumo > bonus_limite:
        total = consumo * faixas[0][1]
        return {"total": round(total, 2), "detalhe": [(0, consumo, round(total, 2))], "retroativo": True}

    detalhe = []
    total = 0
    restante = consumo
    anterior = 0
    index = 0
    while index < len(faixas) and restante > 0:
        limite = faixas[index][0]
        if limite is None:
            quantidade = restante
        else:
            quantidade = limite - anterior
            if quantidade > restante:
                quantidade = restante
        subtotal = quantidade * faixas[index][1]
        detalhe.append((index, quantidade, round(subtotal, 2)))
        total += subtotal
        restante -= quantidade
        anterior = limite
        index += 1
    return {"total": round(total, 2), "detalhe": detalhe, "retroativo": False}