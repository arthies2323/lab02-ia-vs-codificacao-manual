def calcular_fatura(consumo, faixas, bonus_limite=None):
    """Calcula a cobrança progressiva e o detalhe por faixa utilizada."""
    if consumo == 0:
        return {"total": 0, "detalhe": [], "retroativo": False}

    if bonus_limite is not None and consumo > bonus_limite:
        preco_primeira_faixa = faixas[0][1]
        total = round(consumo * preco_primeira_faixa, 2)
        return {
            "total": total,
            "detalhe": [(0, consumo, total)],
            "retroativo": True,
        }

    detalhe = []
    total = 0.0
    limite_anterior = 0

    for indice, (limite_superior, preco) in enumerate(faixas):
        if limite_superior is None:
            quantidade = consumo - limite_anterior
        else:
            quantidade = min(consumo, limite_superior) - limite_anterior

        if quantidade > 0:
            subtotal = round(quantidade * preco, 2)
            detalhe.append((indice, quantidade, subtotal))
            total += quantidade * preco

        if limite_superior is None or consumo <= limite_superior:
            break

        limite_anterior = limite_superior

    return {
        "total": round(total, 2),
        "detalhe": detalhe,
        "retroativo": False,
    }
