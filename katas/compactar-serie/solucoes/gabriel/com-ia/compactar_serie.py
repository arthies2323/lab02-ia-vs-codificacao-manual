def _escapar_literal(caractere):
    if caractere.isdigit() or caractere in {"*", "\\"}:
        return "\\" + caractere
    return caractere


def compactar(serie):
    """Compacta sequências de três ou mais caracteres iguais."""
    if not serie:
        return ""

    partes = []
    indice = 0

    while indice < len(serie):
        caractere = serie[indice]
        fim = indice + 1

        while fim < len(serie) and serie[fim] == caractere:
            fim += 1

        quantidade = fim - indice
        if quantidade >= 3:
            partes.append(f"{quantidade}*{caractere}")
        else:
            partes.extend(_escapar_literal(caractere) for _ in range(quantidade))

        indice = fim

    return "".join(partes)


def expandir(codigo):
    """Expande um código produzido por :func:`compactar`."""
    if not codigo:
        return ""

    resultado = []
    indice = 0

    while indice < len(codigo):
        atual = codigo[indice]

        if atual == "\\":
            if indice + 1 >= len(codigo):
                resultado.append("\\")
                indice += 1
            else:
                resultado.append(codigo[indice + 1])
                indice += 2
            continue

        if atual.isdigit():
            fim_numero = indice
            while fim_numero < len(codigo) and codigo[fim_numero].isdigit():
                fim_numero += 1

            if fim_numero < len(codigo) and codigo[fim_numero] == "*" and fim_numero + 1 < len(codigo):
                quantidade = int(codigo[indice:fim_numero])
                resultado.append(codigo[fim_numero + 1] * quantidade)
                indice = fim_numero + 2
                continue

        resultado.append(atual)
        indice += 1

    return "".join(resultado)
