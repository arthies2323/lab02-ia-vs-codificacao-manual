def calcular_fatura(consumo, faixas, bonus_limite=None):
    if consumo == 0:
        return {
            "total": 0,
            "detalhe": [],
            "retroativo": False
        }

    if bonus_limite is not None and consumo > bonus_limite:
        preco = faixas[0][1]
        total = round(consumo * preco, 2)

        return {
            "total": total,
            "detalhe": [(0, consumo, total)],
            "retroativo": True
        }

    total = 0
    detalhe = []
    consumido = 0

    for indice, (limite, preco) in enumerate(faixas):
        if consumido >= consumo:
            break

        if limite is None:
            quantidade = consumo - consumido
        else:
            espaco_na_faixa = limite - consumido
            quantidade = min(
                consumo - consumido,
                espaco_na_faixa
            )

        subtotal = round(quantidade * preco, 2)

        detalhe.append(
            (indice, quantidade, subtotal)
        )

        total += subtotal
        consumido += quantidade

    return {
        "total": round(total, 2),
        "detalhe": detalhe,
        "retroativo": False
    }
