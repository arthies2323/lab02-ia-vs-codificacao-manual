from agenda_turnos import consolidar_turnos


def test_intervalos_separados_mantem_lacuna():
    assert consolidar_turnos([("08:00", "12:00"), ("14:00", "18:00")]) == {
        "intervalos": [("08:00", "12:00"), ("14:00", "18:00")],
        "cobertura": 480,
        "lacunas": [120],
    }


def test_intervalos_sobrepostos_sao_fundidos():
    assert consolidar_turnos([("08:00", "12:00"), ("10:00", "15:00")]) == {
        "intervalos": [("08:00", "15:00")],
        "cobertura": 420,
        "lacunas": [],
    }


def test_intervalos_adjacentes_fundem_com_folga_zero():
    assert consolidar_turnos([("08:00", "12:00"), ("12:00", "15:00")]) == {
        "intervalos": [("08:00", "15:00")],
        "cobertura": 420,
        "lacunas": [],
    }


def test_turno_atravessa_meia_noite_e_dividido():
    assert consolidar_turnos([("22:00", "06:00")]) == {
        "intervalos": [("00:00", "06:00"), ("22:00", "24:00")],
        "cobertura": 480,
        "lacunas": [960],
    }


def test_turno_com_fim_igual_ao_inicio_cobre_24h():
    assert consolidar_turnos([("08:00", "08:00")]) == {
        "intervalos": [("00:00", "24:00")],
        "cobertura": 1440,
        "lacunas": [],
    }


def test_folga_minima_funde_intervalos_proximos():
    assert consolidar_turnos(
        [("08:00", "12:00"), ("14:00", "18:00")], folga_minima=180
    ) == {
        "intervalos": [("08:00", "18:00")],
        "cobertura": 600,
        "lacunas": [],
    }


def test_lacuna_igual_a_folga_minima_nao_funde():
    assert consolidar_turnos(
        [("08:00", "12:00"), ("14:00", "18:00")], folga_minima=120
    ) == {
        "intervalos": [("08:00", "12:00"), ("14:00", "18:00")],
        "cobertura": 480,
        "lacunas": [120],
    }


def test_entrada_fora_de_ordem():
    assert consolidar_turnos([("14:00", "18:00"), ("08:00", "12:00")]) == {
        "intervalos": [("08:00", "12:00"), ("14:00", "18:00")],
        "cobertura": 480,
        "lacunas": [120],
    }


def test_lista_vazia():
    assert consolidar_turnos([]) == {
        "intervalos": [],
        "cobertura": 0,
        "lacunas": [],
    }
