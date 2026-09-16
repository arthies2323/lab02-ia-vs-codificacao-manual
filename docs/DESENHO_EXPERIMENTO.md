# Desenho do Experimento — Lab02S01

## Goal (GQM)

Analisar o uso de assistentes de IA generativa na resolução de tarefas de
programação, com o propósito de comparar seu efeito frente à codificação
manual, com respeito a tempo de resolução, qualidade funcional (defeitos) e
qualidade estrutural do código produzido, do ponto de vista do grupo
pesquisador, no contexto de katas de dificuldade equivalente resolvidos por
estudantes de graduação sob condições controladas (crossover within-subject,
time-boxed).

## (A) Hipóteses

- **RQ1 — Tempo**
  - H0: não há diferença na mediana do tempo até passar todos os testes de
    aceitação (time-to-green) entre trials com e sem assistente de IA.
  - H1: o tempo até passar todos os testes de aceitação é menor com
    assistente de IA.
- **RQ2 — Defeitos**
  - H0: não há diferença na taxa de sucesso (% de testes de aceitação
    passando ao final do time-box) entre trials com e sem assistente de IA.
  - H1: a taxa de sucesso é maior com assistente de IA.
- **RQ3 — Estrutura do código**
  - H0: não há diferença na complexidade ciclomática média e/ou na
    duplicação de código (normalizadas por LOC) entre trials com e sem
    assistente de IA.
  - H1: a complexidade ciclomática média e/ou a duplicação de código diferem
    entre trials com e sem assistente de IA.

## (B) Variáveis dependentes

| RQ  | Variável            | Métrica                                                                                    |
|-----|----------------------|----------------------------------------------------------------------------------------------|
| RQ1 | Tempo de resolução   | Time-to-green (min), coletado por [`scripts/timer.py`](../scripts/timer.py); censurado em 35 min se não passar. Agregação: mediana por tratamento. |
| RQ2 | Defeitos             | Taxa de sucesso (% testes passando); nº absoluto de testes falhando ao final do time-box.    |
| RQ3 | Estrutura do código  | Complexidade ciclomática média e LOC/SLOC (Radon), duplicação (jscpd), coletados por [`scripts/collect_static_metrics.py`](../scripts/collect_static_metrics.py); MI (Radon `mi`) como métrica composta opcional. |

## (C) Variável independente

Uso ou não de assistente de IA generativa durante a resolução do kata
(binária: com IA / sem IA).

## (D) Tratamentos

1. **Com IA** — assistente de IA habilitado durante todo o trial. Conforme
   registrado no protocolo anti-contaminação
   ([`katas/README.md`](../katas/README.md)), o assistente em uso é o
   **GitHub Copilot**, mesmo assistente em todos os trials do experimento.
   Essa escolha pode ainda ser revisitada pelo grupo antes do início da
   execução (Sprint 2); qualquer mudança deve ser registrada aqui e no
   relatório final.
2. **Sem IA** — codificação manual, sem qualquer assistente de IA.

## (E) Objetos experimentais

6 katas em Python, de dificuldade comparável, listados e documentados em
[`katas/README.md`](../katas/README.md): `agenda-turnos`, `cifra-alternada`,
`compactar-serie`, `fatura-progressiva`, `ranking-liga`, `torre-blocos`. Cada
um é uma adaptação de um exercício clássico, alterada de forma a invalidar a
solução canônica (mitigação de memorização — ver ameaças à validade). Todos
têm testes de aceitação automatizados (pytest) e uma validação objetiva de
dificuldade equivalente (SLOC e complexidade ciclomática de uma solução de
referência), documentada no mesmo arquivo.

## (F) Tipo de projeto experimental

Crossover / within-subject, contrabalanceado: cada integrante do trio
resolve os 6 katas, metade com IA e metade sem IA. Nenhum integrante resolve
o mesmo kata duas vezes (isso contaminaria o resultado por efeito de
aprendizado/memorização — ver seção H). Em vez disso, a ordem e a atribuição
de tratamento por kata são contrabalanceadas **entre os integrantes**, de
forma que cada um dos 6 katas seja resolvido sob os dois tratamentos ao
longo do trio (por pessoas diferentes). A comparação estatística (Sprint 3)
é pareada por integrante: mediana dos tempos/métricas desse integrante nos
katas com IA vs. nos katas sem IA — cada pessoa funciona como seu próprio
controle, o que neutraliza a variação individual de habilidade.

## (G) Quantidade de medições

3 integrantes × 6 katas = 18 trials no total (9 com IA / 9 sem IA), ou seja
6 trials por integrante (3 por tratamento) — dentro da faixa de 4–6 trials
recomendada pelo enunciado.

## (H) Ameaças à validade

- **Efeito de aprendizado entre katas.** Resolver vários katas em sequência
  pode enviesar os últimos trials (fadiga, ou familiaridade crescente com o
  padrão de teste do experimento). Mitigação: ordem contrabalanceada entre
  integrantes.
- **Repetição do mesmo kata pela mesma pessoa (memorização direta).** Se um
  integrante resolvesse o mesmo kata nos dois tratamentos, o segundo trial
  seria mais rápido apenas por já conhecer o problema — não pelo efeito da
  IA. Mitigação estrutural do desenho: cada kata é resolvido **uma única
  vez** por cada integrante (ver seção F).
- **Familiaridade prévia com a ferramenta de IA.** Integrantes com mais
  experiência prévia no assistente escolhido podem ter vantagem
  independente do tratamento. Mitigação: registrar a experiência prévia de
  cada integrante no relatório final.
- **Vazamento de solução já vista / memorização pelo modelo.** Katas muito
  conhecidos (clássicos de LeetCode/HackerRank) podem levar o assistente a
  reproduzir uma solução memorizada do treinamento, em vez de efetivamente
  ajudar. Mitigação: os 6 katas são adaptações que invalidam a solução
  canônica (detalhado em [`katas/README.md`](../katas/README.md)).
- **Contaminação via indexação do workspace pelo Copilot.** Ameaça
  identificada durante a preparação (Passo 2): como o Copilot indexa os
  arquivos abertos no editor, (i) soluções de referência não podem ficar
  versionadas no repositório, e (ii) um integrante não pode dar `pull` das
  soluções de outro antes de terminar seus próprios trials. Protocolo
  completo (branches por integrante, tag `katas-v1`) em
  [`katas/README.md`](../katas/README.md).
- **Variação individual de habilidade.** Mitigada pelo desenho
  within-subject: cada integrante passa pelos dois tratamentos, então é
  comparado contra si mesmo, não contra os outros dois integrantes.
- **Dificuldade não perfeitamente idêntica entre katas.** A validação por
  SLOC/complexidade ([`katas/README.md`](../katas/README.md)) aproxima os 6
  katas, mas não os iguala exatamente (`ranking-liga` é o mais pesado).
  Como o contrabalanceamento garante que cada kata apareça nos dois
  tratamentos, essa diferença adiciona variância à medição, não viés
  sistemático a favor de um tratamento.

## Métricas — justificativa da escolha

- **RQ1:** time-to-green como métrica primária (mais direta e comparável
  entre katas do que contagem de interações); mediana em vez de média dado
  N pequeno (6 trials/integrante) e sensibilidade da média a outliers.
- **RQ2:** taxa de sucesso como métrica primária (normaliza katas com
  números diferentes de testes de aceitação); nº absoluto de testes
  falhando como métrica complementar.
- **RQ3:** complexidade ciclomática (Radon `cc`) e duplicação (jscpd),
  sempre acompanhadas de LOC/SLOC (Radon `raw`) como controle, já que
  código gerado por IA pode ser mais verboso. MI (Radon `mi`) como métrica
  composta opcional.
- **Análise estatística (Sprint 3):** mediana e IQR nas tabelas
  descritivas; teste de Wilcoxon (pareado, não paramétrico) na análise
  inferencial, consistente com o desenho within-subject pareado por
  integrante.
