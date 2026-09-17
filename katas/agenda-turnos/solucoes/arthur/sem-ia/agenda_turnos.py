def _para_minutos(hhmm):
    horas, minutos = hhmm.split(":")
    return int(horas) * 60 + int(minutos)


def _para_hhmm(minutos):
    if minutos == 1440:
        return "24:00"

    horas = minutos // 60
    mins = minutos % 60

    return f"{horas:02d}:{mins:02d}"


def consolidar_turnos(turnos, folga_minima=0):
    if not turnos:
        return {
            "intervalos": [],
            "cobertura": 0,
            "lacunas": []
        }

    brutos = []

    for inicio, fim in turnos:
        s = _para_minutos(inicio)
        e = _para_minutos(fim)

        if e == s:
            brutos.append((0, 1440))
        elif e < s:
            brutos.append((s, 1440))
            brutos.append((0, e))
        else:
            brutos.append((s, e))

    brutos.sort()

    consolidados = []
    lacunas = []

    atual_s, atual_e = brutos[0]

    for s, e in brutos[1:]:
        gap = s - atual_e

        if gap <= 0 or gap < folga_minima:
            atual_e = max(atual_e, e)
        else:
            consolidados.append((atual_s, atual_e))
            lacunas.append(gap)
            atual_s, atual_e = s, e

    consolidados.append((atual_s, atual_e))

    cobertura = sum(e - s for s, e in consolidados)

    intervalos = []
    for s, e in consolidados:
        intervalos.append(
            (_para_hhmm(s), _para_hhmm(e))
        )

    return {
        "intervalos": intervalos,
        "cobertura": cobertura,
        "lacunas": lacunas
    }
