def _para_minutos(horario):
    horas, minutos = map(int, horario.split(":"))
    return horas * 60 + minutos


def _para_horario(total_minutos):
    if total_minutos == 24 * 60:
        return "24:00"
    horas, minutos = divmod(total_minutos, 60)
    return f"{horas:02d}:{minutos:02d}"


def consolidar_turnos(turnos, folga_minima=0):
    """Consolida turnos, inclusive os que atravessam a meia-noite."""
    if not turnos:
        return {"intervalos": [], "cobertura": 0, "lacunas": []}

    intervalos = []
    for inicio, fim in turnos:
        inicio_min = _para_minutos(inicio)
        fim_min = _para_minutos(fim)

        if fim_min == inicio_min:
            intervalos.append((0, 24 * 60))
        elif fim_min < inicio_min:
            intervalos.append((inicio_min, 24 * 60))
            if fim_min > 0:
                intervalos.append((0, fim_min))
        else:
            intervalos.append((inicio_min, fim_min))

    intervalos.sort(key=lambda item: (item[0], item[1]))

    consolidados = []
    inicio_atual, fim_atual = intervalos[0]

    for inicio, fim in intervalos[1:]:
        lacuna = inicio - fim_atual
        deve_fundir = inicio <= fim_atual or lacuna < folga_minima

        if deve_fundir:
            fim_atual = max(fim_atual, fim)
        else:
            consolidados.append((inicio_atual, fim_atual))
            inicio_atual, fim_atual = inicio, fim

    consolidados.append((inicio_atual, fim_atual))

    cobertura = sum(fim - inicio for inicio, fim in consolidados)
    lacunas = [
        consolidados[i + 1][0] - consolidados[i][1]
        for i in range(len(consolidados) - 1)
    ]

    return {
        "intervalos": [
            (_para_horario(inicio), _para_horario(fim))
            for inicio, fim in consolidados
        ],
        "cobertura": cobertura,
        "lacunas": lacunas,
    }
