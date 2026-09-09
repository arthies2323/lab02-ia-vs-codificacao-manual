# Dados coletados

Datasets gerados durante a Sprint 2 (execução do experimento) e consumidos
na Sprint 3 (análise).

## `timings.csv` (gerado por `scripts/timer.py`, issue de cronometragem)

Uma linha por trial: `integrante, kata, tratamento, tempo_min, censurado`.

## `metrics.csv` (gerado por `scripts/collect_static_metrics.py`)

Uma linha por trial, com as métricas estáticas (RQ3) do código final:

| coluna           | descrição                                            |
|-------------------|-------------------------------------------------------|
| timestamp         | data/hora UTC da coleta                                |
| integrante        | nome de quem resolveu o trial                          |
| kata              | identificador do kata                                  |
| tratamento        | `com-ia` ou `sem-ia`                                   |
| loc               | linhas de código (Radon `raw`), métrica de controle    |
| sloc              | linhas de código sem comentários/brancos (Radon `raw`) |
| complexity_avg    | complexidade ciclomática média (Radon `cc`)             |
| mi_avg            | Maintainability Index médio (Radon `mi`)                |
| duplication_pct   | % de linhas duplicadas (jscpd)                          |
