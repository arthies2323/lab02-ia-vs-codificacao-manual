MINUTOS_NO_DIA = 1440


def para_minutos(horario):
    return int(horario[0:2]) * 60 + int(horario[3:5])


def para_horario(minutos):
    return f"{minutos // 60:02d}:{minutos % 60:02d}"


def consolidar_turnos(turnos, folga_minima=0):
    """Consolida uma escala de turnos. Ver README.md do kata."""
    intervalos = []
    index = 0
    while index < len(turnos):
        inicio = para_minutos(turnos[index][0])
        fim = para_minutos(turnos[index][1])
        if fim <= inicio:
            intervalos.append((inicio, MINUTOS_NO_DIA))
            intervalos.append((0, fim))
        else:
            intervalos.append((inicio, fim))
        index += 1
    intervalos.sort()

    consolidados = []
    index = 0
    while index < len(intervalos):
        inicio = intervalos[index][0]
        fim = intervalos[index][1]
        while index + 1 < len(intervalos) and (intervalos[index + 1][0] - fim <= 0 or intervalos[index + 1][0] - fim < folga_minima):
            if intervalos[index + 1][1] > fim:
                fim = intervalos[index + 1][1]
            index += 1
        consolidados.append((inicio, fim))
        index += 1

    saida = []
    lacunas = []
    cobertura = 0
    index = 0
    while index < len(consolidados):
        saida.append((para_horario(consolidados[index][0]), para_horario(consolidados[index][1])))
        cobertura += consolidados[index][1] - consolidados[index][0]
        if index + 1 < len(consolidados):
            lacunas.append(consolidados[index + 1][0] - consolidados[index][1])
        index += 1
    return {"intervalos": saida, "cobertura": cobertura, "lacunas": lacunas}