# Lab02S01 — Issues #3 e #4

Este documento complementa os artefatos já existentes do repositório. Nenhum
arquivo anterior foi substituído para esta entrega.

## Issue #3 — Script de cronometragem (time-to-green)

Artefato: `scripts/timer.py`.

O cronômetro inicia junto com o trial, roda automaticamente o `pytest` do kata e
encerra em uma das duas condições:

1. **Green:** todos os testes passam antes do limite; grava o tempo real até o
   green.
2. **Time-box:** não houve green em até 35 minutos; grava `35.0000` minutos e
   `censurado=true`. O trial não é descartado.

Formato de `data/timings.csv`:

```text
integrante,kata,tratamento,tempo_min,censurado
```

### Execução real

Na raiz do repositório:

```bash
python scripts/timer.py --kata agenda-turnos --tratamento com-ia --integrante gabriel
```

Para o tratamento manual:

```bash
python scripts/timer.py --kata agenda-turnos --tratamento sem-ia --integrante gabriel
```

O alvo padrão dos testes é `katas/<kata>`. O script impede, por padrão, que a
mesma combinação integrante/kata/tratamento seja registrada duas vezes.

> Em trials reais, não altere `--timebox-seconds`: o padrão é 2100 segundos
> (35 minutos), conforme o enunciado do laboratório.

## Issue #4 — Ambiente + métricas estáticas

Os artefatos principais da Issue #4 já estavam presentes no ZIP recebido:

- `scripts/requirements.txt`
- `scripts/collect_static_metrics.py`

Foram **mantidos sem alteração**. Esta complementação adiciona
`scripts/check_environment.py` e testes automatizados para validar a preparação
do ambiente e o contrato do CSV de métricas.

### Preparar Python

```bash
python -m pip install -r scripts/requirements.txt
```

O projeto utiliza Python 3.10+ (a sintaxe do coletor existente usa union types
com `|`).

### Preparar duplicação (jscpd)

Foi adicionado um `package.json` com a versão do `jscpd` fixada para tornar a
preparação do ambiente reproduzível. Com Node.js/npm instalado, execute:

```bash
npm install
```

O `collect_static_metrics.py` existente aceita `jscpd` instalado diretamente ou
usa `npx` quando disponível. Como alternativa à instalação local acima, também
é possível instalar o jscpd globalmente:

```bash
npm install -g jscpd
```

### Verificar ambiente

```bash
python scripts/check_environment.py
```

O diagnóstico confere Python, pytest, Radon, Pandas, jscpd/npx e a estrutura
mínima das Issues #3 e #4.

### Coletar métricas finais de um trial

```bash
python scripts/collect_static_metrics.py \
  --path katas/agenda-turnos/solucao \
  --kata agenda-turnos \
  --integrante gabriel \
  --tratamento com-ia \
  --out data/metrics.csv
```

O CSV produzido contém as métricas previstas para a RQ3:

- LOC e SLOC (controle de tamanho);
- complexidade ciclomática média;
- Maintainability Index;
- percentual de duplicação via jscpd.

## Testes dos artefatos

Os testes adicionados ficam em `tests/` e não executam os trials reais:

```bash
python -m pytest tests -q
```

Eles validam, entre outros pontos, que:

- um green é registrado com o tempo efetivo;
- um trial sem green é censurado exatamente no time-box;
- o `timings.csv` mantém o formato esperado pela Sprint 3;
- o coletor de métricas mantém o esquema definido na Issue #4.

## Sugestões de commits para rastreabilidade no GitHub Projects

Como a correção exige referência à Issue correspondente, uma separação simples
é:

```text
feat: implementar cronometro time-to-green dos trials (#3)
test: validar ambiente e coleta de metricas estaticas (#4)
```

A Sprint 1 não inclui a execução dos 18 trials nem a análise estatística. Esses
dados devem ser produzidos apenas nas sprints posteriores, conforme o protocolo
do laboratório.
