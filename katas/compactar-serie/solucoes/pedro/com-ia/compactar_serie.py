from itertools import groupby

LIMIAR = 3
DIGITOS = "0123456789"
ESCAPAR = set(DIGITOS) | {"*", "\\"}


def _literal(caractere):
    """Copia um caractere fora de trecho compactado, escapando o que é ambíguo."""
    return "\\" + caractere if caractere in ESCAPAR else caractere


def compactar(serie):
    """Compacta a serie. Ver README.md do kata."""
    partes = []
    for caractere, grupo in groupby(serie):
        repeticoes = len(list(grupo))
        if repeticoes >= LIMIAR:
            # Dentro de "{n}*{c}" a posição já desambigua o caractere.
            partes.append(f"{repeticoes}*{caractere}")
        else:
            partes.append(_literal(caractere) * repeticoes)
    return "".join(partes)


def expandir(codigo):
    """Inversa de compactar. Ver README.md do kata."""
    partes = []
    posicao = 0

    while posicao < len(codigo):
        caractere = codigo[posicao]

        if caractere == "\\":
            partes.append(codigo[posicao + 1])
            posicao += 2
        elif caractere in DIGITOS:
            # Dígito sem escape só aparece como contagem: leia até o "*".
            fim = posicao
            while codigo[fim] in DIGITOS:
                fim += 1
            partes.append(codigo[fim + 1] * int(codigo[posicao:fim]))
            posicao = fim + 2
        else:
            partes.append(caractere)
            posicao += 1

    return "".join(partes)
