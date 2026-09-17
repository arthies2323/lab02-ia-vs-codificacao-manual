def compactar(serie):
    if not serie:
        return ""

    resultado = ""
    i = 0

    while i < len(serie):
        caractere = serie[i]
        quantidade = 1

        while (
            i + quantidade < len(serie)
            and serie[i + quantidade] == caractere
        ):
            quantidade += 1

        if quantidade >= 3:
            resultado += str(quantidade) + "*" + caractere
        else:
            for _ in range(quantidade):
                if caractere.isdigit() or caractere == "*" or caractere == "\\":
                    resultado += "\\" + caractere
                else:
                    resultado += caractere

        i += quantidade

    return resultado


def expandir(codigo):
    if not codigo:
        return ""

    resultado = ""
    i = 0

    while i < len(codigo):
        if codigo[i] == "\\":
            resultado += codigo[i + 1]
            i += 2
        elif codigo[i].isdigit():
            numero = ""

            while i < len(codigo) and codigo[i].isdigit():
                numero += codigo[i]
                i += 1

            i += 1
            caractere = codigo[i]

            resultado += caractere * int(numero)
            i += 1
        else:
            resultado += codigo[i]
            i += 1

    return resultado
