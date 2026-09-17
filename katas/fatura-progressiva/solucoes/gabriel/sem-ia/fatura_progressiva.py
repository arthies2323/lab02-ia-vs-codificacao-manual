def calcular_fatura(consumo, faixas, bonus_limite=None):
    """Calcula a fatura conforme as faixas e o bônus retroativo."""
    if consumo == 0:
        return {"total": 0, "detalhe": [], "retroativo": False}

    if bonus_limite is not None:
        if consumo > bonus_limite:
            valor = round(consumo * faixas[0][1], 2)
            return {
                "total": valor,
                "detalhe": [(0, consumo, valor)],
                "retroativo": True,
            }

    restante = consumo
    inicio_faixa = 0
    valor_total = 0
    detalhe = []

    for numero, faixa in enumerate(faixas):
        limite, preco = faixa

        if limite is None:
            quantidade = restante
        else:
            tamanho_faixa = limite - inicio_faixa
            quantidade = min(restante, tamanho_faixa)

        if quantidade > 0:
            subtotal = round(quantidade * preco, 2)
            detalhe.append((numero, quantidade, subtotal))
            valor_total += quantidade * preco
            restante -= quantidade

        if restante <= 0:
            break

        if limite is not None:
            inicio_faixa = limite

    return {
        "total": round(valor_total, 2),
        "detalhe": detalhe,
        "retroativo": False,
    }
