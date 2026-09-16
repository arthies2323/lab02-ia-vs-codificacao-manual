def calcular_fatura(consumo, faixas, bonus_limite=None):
    """Calcula a fatura por faixas progressivas. Ver README.md do kata."""
    if bonus_limite is not None and consumo > bonus_limite:
        # Bônus retroativo: o rastro por faixa é descartado e tudo vai ao
        # preço da primeira faixa.
        total = round(consumo * faixas[0][1], 2)
        return {"total": total, "detalhe": [(0, consumo, total)], "retroativo": True}

    detalhe = []
    total = 0
    base = 0  # fim da faixa anterior já faturada

    for indice, (limite_superior, preco) in enumerate(faixas):
        if consumo <= base:
            break

        # Limite exclusivo: consumo igual ao teto cabe inteiro nesta faixa.
        teto = consumo if limite_superior is None else min(consumo, limite_superior)
        quantidade = teto - base
        if quantidade > 0:
            total += quantidade * preco
            detalhe.append((indice, quantidade, round(quantidade * preco, 2)))
        base = teto

    return {"total": round(total, 2), "detalhe": detalhe, "retroativo": False}
