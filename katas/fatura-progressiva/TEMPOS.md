# Tempos — fatura-progressiva

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
| arthur | sem-ia | 2026-09-17 | 15.0883 | false | 9/9 testes |
| arthur | com-ia | 2026-09-16 | 0.0091 | false | Claude Code (Claude Opus 5); 9/9 testes, green na 1ª submissão |
| gabriel | sem-ia |  |  |  |  |
| gabriel | com-ia |  |  |  |  |
| pedro | sem-ia | 2026-09-17 | 28.9500 | false | cronometrado pelo próprio integrante (28:57); 9/9 testes |
| pedro | com-ia | 2026-09-16 | 0.4400 | false | agente autônomo (Claude Code); 9/9 testes, green na 1ª submissão |

## Métricas estáticas deste kata

Após o green (ou o time-box), colete as métricas da RQ3 apontando para o slot
do trial:

```bash
python scripts/collect_static_metrics.py \
  --path katas/fatura-progressiva/solucoes/<integrante>/<tratamento> \
  --kata fatura-progressiva \
  --integrante <integrante> \
  --tratamento <tratamento> \
  --out data/metrics.csv
```
