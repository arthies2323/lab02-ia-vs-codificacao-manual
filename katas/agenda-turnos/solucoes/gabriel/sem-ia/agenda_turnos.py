def consolidar_turnos(turnos, folga_minima=0):
    """Consolida uma escala de turnos seguindo as regras do kata."""
    if len(turnos) == 0:
        return {"intervalos": [], "cobertura": 0, "lacunas": []}

    partes = []

    for inicio, fim in turnos:
        hi, mi = [int(valor) for valor in inicio.split(":")]
        hf, mf = [int(valor) for valor in fim.split(":")]
        ini = hi * 60 + mi
        final = hf * 60 + mf

        if final == ini:
            partes.append([0, 1440])
        elif final < ini:
            partes.append([ini, 1440])
            if final > 0:
                partes.append([0, final])
        else:
            partes.append([ini, final])

    partes.sort()
    unidos = []

    for ini, final in partes:
        if not unidos:
            unidos.append([ini, final])
            continue

        ultimo = unidos[-1]
        distancia = ini - ultimo[1]
        if ini <= ultimo[1] or distancia < folga_minima:
            if final > ultimo[1]:
                ultimo[1] = final
        else:
            unidos.append([ini, final])

    intervalos = []
    cobertura = 0
    lacunas = []

    for indice, (ini, final) in enumerate(unidos):
        cobertura += final - ini

        def texto(minutos):
            if minutos == 1440:
                return "24:00"
            h = minutos // 60
            m = minutos % 60
            return f"{h:02d}:{m:02d}"

        intervalos.append((texto(ini), texto(final)))

        if indice > 0:
            lacunas.append(ini - unidos[indice - 1][1])

    return {
        "intervalos": intervalos,
        "cobertura": cobertura,
        "lacunas": lacunas,
    }
