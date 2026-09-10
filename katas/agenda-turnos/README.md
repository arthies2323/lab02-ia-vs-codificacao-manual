# Kata: agenda-turnos

Consolidar uma escala de turnos que pode atravessar a meia-noite, aplicando uma
folga mínima entre turnos.

## Função a implementar

```python
consolidar_turnos(turnos, folga_minima=0) -> dict
```

- `turnos`: lista de tuplas `(inicio, fim)`, cada valor no formato `"HH:MM"`.
- `folga_minima`: inteiro, em minutos (padrão `0`).

## Regras

1. **Turno que atravessa a meia-noite.** Se `fim <= inicio`, o turno é dividido
   em dois: `(inicio, "24:00")` e `("00:00", fim)`. Se `fim == inicio`, o turno
   cobre as 24 horas.
2. **Consolidação.** Dois intervalos são fundidos quando se sobrepõem, quando
   são adjacentes, ou quando a lacuna entre eles é **estritamente menor** que
   `folga_minima`. Uma lacuna exatamente igual a `folga_minima` **não** funde.
3. **Saída.** Um dicionário com:
   - `"intervalos"`: lista de tuplas `("HH:MM", "HH:MM")` já consolidadas e em
     ordem crescente. O fim do dia é representado como `"24:00"`.
   - `"cobertura"`: total de minutos cobertos (inteiro).
   - `"lacunas"`: lista de inteiros com as lacunas, em minutos, **entre**
     intervalos consecutivos consolidados. Não inclui o tempo antes do primeiro
     nem depois do último intervalo.

A lista de entrada pode vir fora de ordem. Lista vazia devolve
`{"intervalos": [], "cobertura": 0, "lacunas": []}`.

## Exemplos

```python
consolidar_turnos([("08:00", "12:00"), ("14:00", "18:00")])
# {"intervalos": [("08:00", "12:00"), ("14:00", "18:00")],
#  "cobertura": 480, "lacunas": [120]}

consolidar_turnos([("22:00", "06:00")])
# {"intervalos": [("00:00", "06:00"), ("22:00", "24:00")],
#  "cobertura": 480, "lacunas": [960]}

consolidar_turnos([("08:00", "12:00"), ("14:00", "18:00")], folga_minima=180)
# {"intervalos": [("08:00", "18:00")], "cobertura": 600, "lacunas": []}
```

## Procedência e adaptação

- **Exercício-base:** consolidação de intervalos sobrepostos ("merge
  intervals"), padrão clássico de manipulação de intervalos.
- **O que foi alterado:** (a) intervalos circulares — turnos que cruzam a
  meia-noite precisam ser divididos antes da consolidação; (b) critério de fusão
  por *folga mínima* com comparação estrita, e não apenas por sobreposição;
  (c) saída agregada (`cobertura` e `lacunas`) em vez da lista de intervalos.

A solução canônica de *merge intervals* não passa nos testes de aceitação sem
reescrita das três partes.
