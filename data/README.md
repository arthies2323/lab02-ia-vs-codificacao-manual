# Dados coletados

Datasets gerados durante a Sprint 2 (execução do experimento) e consumidos
na Sprint 3 (análise).

## `timings.csv` (gerado por `scripts/timer.py`, issue de cronometragem)

Uma linha por trial:

| coluna           | descrição                                                     |
|------------------|---------------------------------------------------------------|
| integrante       | nome de quem resolveu o trial                                  |
| kata             | identificador do kata                                          |
| tratamento       | `com-ia` ou `sem-ia`                                           |
| tempo_min        | **variável da RQ1**: tempo total de resolução em minutos; `35.0000` quando censurado |
| censurado        | `true` quando não houve green dentro do time-box de 35 min     |
| testes_passando  | testes passando **no encerramento do trial** (RQ2); vazio = não capturado |

### O que `tempo_min` inclui

`tempo_min` é o ciclo completo de resolução: compreensão do enunciado, projeto
da solução (a spec), implementação e verificação.

Nos trials `sem-ia` tudo isso acontece dentro do trial cronometrado, então o
valor gravado pelo `timer.py` já é o total.

Nos trials `com-ia` a spec é escrita **antes** de o agente ser acionado, isto é,
antes de o cronômetro iniciar — o `timer.py` não a enxerga. O participante
cronometra essa etapa à parte e **soma** o valor ao `tempo_min` da linha
correspondente. Sem essa soma, o campo mediria apenas a latência do agente, que
não descreve esforço humano algum.

### `testes_passando` e o time-box

O trial termina no minuto 35, então `testes_passando` descreve a suíte **naquele
instante** — não o estado da solução depois, se o participante continuou
trabalhando fora do time-box. Em trial com green, é a suíte inteira. Em trial
censurado, é a última contagem observada pelo `timer.py` antes do corte.

Célula vazia significa **não capturado**, que é diferente de zero: nos dois
trials censurados do `arthur` o cronômetro não estava rodando, então o número no
minuto 35 não existe. Preencher isso com `0` seria inventar medição.

A `RQ2` deve ser lida como **"atingiu green dentro do time-box?"** (`censurado ==
false`), que está definida para todos os trials. O `9/9 ao final` que aparece em
alguns `TEMPOS.md` descreve código produzido **depois** do corte e não é
resultado de trial.

> ⚠️ A mesma ressalva vale para o `metrics.csv`: nas linhas de trial censurado, as
> métricas foram coletadas sobre o código final, não sobre o código no minuto 35.
> Na RQ3, reporte os resultados com e sem essas linhas.

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
