# Tempos — ranking-liga

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
| arthur | sem-ia | 2026-09-17 | 35.0000 | true | sem green no time-box: 0 testes passando aos 35 min (relatado pelo grupo, sem captura do cronômetro — o timer não chegou a ser iniciado); duração real até o green estimada em ~1h30 |
| arthur | com-ia | 2026-09-16 | 0.0094 | false | Claude Code (Claude Opus 5); 9/9 testes, green na 1ª submissão |
| gabriel | sem-ia |  |  |  |  |
| gabriel | com-ia |  |  |  |  |
| pedro | sem-ia | 2026-09-17 | 35.0000 | true | sem green no time-box: 0 testes passando aos 35 min (código ainda não executável); duração real até o green 1:11:23 |
| pedro | com-ia | 2026-09-16 | 0.5321 | false | agente autônomo (Claude Code); 9/9 testes, green na 1ª submissão |

## Métricas estáticas deste kata

Após o green (ou o time-box), colete as métricas da RQ3 apontando para o slot
do trial:

```bash
python scripts/collect_static_metrics.py \
  --path katas/ranking-liga/solucoes/<integrante>/<tratamento> \
  --kata ranking-liga \
  --integrante <integrante> \
  --tratamento <tratamento> \
  --out data/metrics.csv
```
