# Laboratório 02 — Assistentes de IA vs. Codificação Manual

Experimento controlado (crossover, within-subject, time-boxed) para avaliar o
efeito do uso de assistente de IA generativa na resolução de katas de
programação, com respeito a **tempo de resolução** (RQ1), **defeitos**
(RQ2) e **qualidade estrutural do código** (RQ3).

Disciplina: Laboratório de Experimentação de Software — PUC Minas (2026/2).

## Stack do experimento

- **Linguagem dos katas:** Python 3.
- **Testes de aceitação:** pytest.
- **Métricas estáticas:** [Radon](https://radon.readthedocs.io/) (complexidade
  ciclomática, LOC, Maintainability Index) + [jscpd](https://github.com/kucherenko/jscpd)
  (duplicação de código).
- **Assistente de IA (tratamento):** a definir/confirmar com o grupo — candidato
  atual: GitHub Copilot (mesmo assistente em todos os trials).
- **Board:** GitHub Projects (v2), uma Issue por kata/tratamento/integrante.

## Estrutura do repositório

- `docs/DESENHO_EXPERIMENTO.md`: hipóteses, variáveis, tratamentos, objetos
  experimentais, desenho, ameaças à validade (Passo 1).
- `katas/`: os 6 katas escolhidos, cada um com enunciado e testes de aceitação
  (Passo 2). Ver [`katas/README.md`](katas/README.md) para a validação de
  dificuldade equivalente e o protocolo anti-contaminação da S02.
- `scripts/`: scripts de cronometragem (time-to-green) e de coleta das
  métricas estáticas (Radon/jscpd) sobre o código final de cada trial.
- `data/`: dados brutos coletados por trial (tempo, testes passando,
  métricas estáticas) — um registro por kata/tratamento/integrante.
- `Relatorios/`: relatório final consolidado (Passo 5) e dashboard de
  visualização (Passo 6).

## Execução rápida

```bash
python -m pip install -r scripts/requirements.txt
```

Testes de aceitação de um kata:

```bash
python -m pytest katas/<nome-do-kata>
```

Cronometragem de um trial:

```bash
python scripts/timer.py --kata <nome-do-kata> --tratamento com-ia --integrante <nome>
```

Coleta de métricas estáticas sobre a solução final de um trial:

```bash
python scripts/collect_static_metrics.py --path katas/<nome-do-kata>/solucao --out data/metrics.csv
```

## Time-box

Cada trial tem **35 minutos**. Ao final do tempo, o trial é encerrado
independentemente do resultado (censurado em 35 min, não descartado).
