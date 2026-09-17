def compactar(serie):
    """Compacta a série usando limiar 3 e escape para literais ambíguos."""
    saida = ""
    i = 0

    while i < len(serie):
        repeticoes = 1
        while i + repeticoes < len(serie) and serie[i + repeticoes] == serie[i]:
            repeticoes += 1

        caractere = serie[i]
        if repeticoes >= 3:
            saida += str(repeticoes) + "*" + caractere
        else:
            for _ in range(repeticoes):
                if caractere.isdigit() or caractere == "*" or caractere == "\\":
                    saida += "\\"
                saida += caractere

        i += repeticoes

    return saida


def expandir(codigo):
    """Reconstrói a string original a partir do código compactado."""
    saida = ""
    i = 0

    while i < len(codigo):
        if codigo[i] == "\\":
            if i + 1 < len(codigo):
                saida += codigo[i + 1]
                i += 2
            else:
                saida += "\\"
                i += 1
        elif codigo[i].isdigit():
            inicio_numero = i
            while i < len(codigo) and codigo[i].isdigit():
                i += 1

            if i < len(codigo) - 1 and codigo[i] == "*":
                quantidade = int(codigo[inicio_numero:i])
                saida += codigo[i + 1] * quantidade
                i += 2
            else:
                saida += codigo[inicio_numero:i]
        else:
            saida += codigo[i]
            i += 1

    return saida
