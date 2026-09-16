MINUTOS_NO_DIA = 24 * 60


def _para_minutos(hora):
    horas, minutos = hora.split(":")
    return int(horas) * 60 + int(minutos)


def _para_hora(minutos):
    return f"{minutos // 60:02d}:{minutos % 60:02d}"


def _expandir(turnos):
    """Converte turnos em intervalos lineares, dividindo os que cruzam a meia-noite."""
    intervalos = []
    for inicio, fim in turnos:
        inicio_min = _para_minutos(inicio)
        fim_min = _para_minutos(fim)

        if fim_min == inicio_min:
            intervalos.append((0, MINUTOS_NO_DIA))
        elif fim_min < inicio_min:
            intervalos.append((inicio_min, MINUTOS_NO_DIA))
            intervalos.append((0, fim_min))
        else:
            intervalos.append((inicio_min, fim_min))

    # A divisão na meia-noite pode gerar um trecho vazio (ex.: fim "00:00").
    return sorted(i for i in intervalos if i[0] < i[1])


def _consolidar(intervalos, folga_minima):
    """Funde intervalos sobrepostos, adjacentes ou separados por menos que a folga."""
    consolidados = []
    for inicio, fim in intervalos:
        if consolidados:
            inicio_anterior, fim_anterior = consolidados[-1]
            lacuna = inicio - fim_anterior
            if lacuna <= 0 or lacuna < folga_minima:
                consolidados[-1] = (inicio_anterior, max(fim_anterior, fim))
                continue
        consolidados.append((inicio, fim))
    return consolidados


def consolidar_turnos(turnos, folga_minima=0):
    """Consolida uma escala de turnos. Ver README.md do kata."""
    consolidados = _consolidar(_expandir(turnos), folga_minima)

    return {
        "intervalos": [(_para_hora(inicio), _para_hora(fim)) for inicio, fim in consolidados],
        "cobertura": sum(fim - inicio for inicio, fim in consolidados),
        "lacunas": [
            proximo[0] - atual[1]
            for atual, proximo in zip(consolidados, consolidados[1:])
        ],
    }
