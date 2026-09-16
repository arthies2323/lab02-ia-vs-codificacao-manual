from itertools import groupby

_ESCAPAVEIS = set("0123456789*\\")


def _escapar(caractere):
    if caractere in _ESCAPAVEIS:
        return "\\" + caractere
    return caractere


def compactar(serie):
    """Compacta a serie. Ver README.md do kata."""
    partes = []
    for caractere, grupo in groupby(serie):
        quantidade = len(list(grupo))
        if quantidade >= 3:
            partes.append(f"{quantidade}*{caractere}")
        else:
            partes.append(_escapar(caractere) * quantidade)
    return "".join(partes)


def expandir(codigo):
    """Inversa de compactar. Ver README.md do kata."""
    resultado = []
    i = 0
    n = len(codigo)
    while i < n:
        c = codigo[i]
        if c == "\\":
            resultado.append(codigo[i + 1])
            i += 2
        elif c.isdigit():
            j = i
            while codigo[j].isdigit():
                j += 1
            quantidade = int(codigo[i:j])
            caractere = codigo[j + 1]
            resultado.append(caractere * quantidade)
            i = j + 2
        else:
            resultado.append(c)
            i += 1
    return "".join(resultado)
