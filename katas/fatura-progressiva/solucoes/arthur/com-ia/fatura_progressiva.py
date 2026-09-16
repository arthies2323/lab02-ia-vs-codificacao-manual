def calcular_fatura(consumo, faixas, bonus_limite=None):
    """Calcula a fatura por faixas progressivas. Ver README.md do kata."""
    if consumo == 0:
        return {"total": 0, "detalhe": [], "retroativo": False}

    if bonus_limite is not None and consumo > bonus_limite:
        preco_primeira_faixa = faixas[0][1]
        total = round(consumo * preco_primeira_faixa, 2)
        return {"total": total, "detalhe": [(0, consumo, total)], "retroativo": True}

    detalhe = []
    total = 0.0
    restante = consumo
    limite_anterior = 0
    for indice, (limite_superior, preco) in enumerate(faixas):
        if restante <= 0:
            break
        capacidade = restante if limite_superior is None else limite_superior - limite_anterior
        quantidade = min(restante, capacidade)
        if quantidade > 0:
            subtotal = round(quantidade * preco, 2)
            detalhe.append((indice, quantidade, subtotal))
            total += quantidade * preco
            restante -= quantidade
        if limite_superior is not None:
            limite_anterior = limite_superior

    return {"total": round(total, 2), "detalhe": detalhe, "retroativo": False}
