# Tempos — compactar-serie

Registro do **time-to-green** de cada trial deste kata: uma linha por
integrante x tratamento. Preencha logo ao encerrar o trial.

`scripts/timer.py` grava o mesmo dado, já formatado, em `data/timings.csv`
(fonte da análise da RQ1). Esta tabela é a versão legível e revisável no
próprio kata — se houver divergência, `data/timings.csv` prevalece.

Regras de preenchimento:

- `tempo (min)`: tempo até todos os testes de aceitação passarem, com 4 casas
  decimais (ex.: `12.3456`), como no CSV.
- `censurado`: `true` quando o time-box de **35 min** foi atingido sem green —
  nesse caso registre `35.0000` e **não** descarte o trial. Caso contrário,
  `false`.
- `data`: `AAAA-MM-DD` do trial.
- Uma linha por slot de `solucoes/<integrante>/<tratamento>/`. Deixe em branco
  os trials ainda não executados.

| integrante | tratamento | data | tempo (min) | censurado | observações |
|---|---|---|---|---|---|
| arthur | sem-ia |  |  |  |  |
| arthur | com-ia |  |  |  |  |
| gabriel | sem-ia |  |  |  |  |
| gabriel | com-ia |  |  |  |  |
| pedro | sem-ia |  |  |  |  |
| pedro | com-ia | 2026-09-16 | 0.3148 | false | agente autônomo (Claude Code); 14/14 testes, green na 1ª submissão |

## Métricas estáticas deste kata

Após o green (ou o time-box), colete as métricas da RQ3 apontando para o slot
do trial:

```bash
python scripts/collect_static_metrics.py \
  --path katas/compactar-serie/solucoes/<integrante>/<tratamento> \
  --kata compactar-serie \
  --integrante <integrante> \
  --tratamento <tratamento> \
  --out data/metrics.csv
```
