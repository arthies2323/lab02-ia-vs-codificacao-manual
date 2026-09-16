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

4 katas em Python, de dificuldade comparável, listados e documentados em
[`katas/README.md`](../katas/README.md): `agenda-turnos`, `compactar-serie`,
`fatura-progressiva`, `ranking-liga` (reduzido de 6 para 4 durante a
preparação, para viabilizar o desenho repetido descrito em F sem estourar o
tempo de execução da S02). Cada um é uma adaptação de um exercício clássico,
alterada de forma a invalidar a solução canônica (mitigação de memorização —
ver ameaças à validade). Todos têm testes de aceitação automatizados
(pytest) e uma validação objetiva de dificuldade equivalente (SLOC e
complexidade ciclomática de uma solução de referência), documentada no
mesmo arquivo.

## (F) Tipo de projeto experimental

Crossover / within-subject, **repetido**: cada integrante do trio resolve os
4 katas **duas vezes cada**, uma vez com IA e uma vez sem IA (8 trials por
integrante). Essa é uma revisão do desenho original — a alternativa
contrabalanceada (cada kata resolvido uma única vez por pessoa, com a
atribuição de tratamento combinada entre os três) foi considerada e está
descrita, junto com o trade-off entre as duas, em
[`katas/README.md`](../katas/README.md#L174) ("Ressalva de desenho"). O
grupo optou pelo desenho repetido para dobrar o N por integrante; a
contrapartida é o efeito de aprendizado descrito na seção H, que passa a ser
uma ameaça **aceita e declarada**, não eliminada pelo desenho.

Mitigação parcial obrigatória (protocolo em
[`katas/README.md`](../katas/README.md)): a ordem é sempre **com-ia antes de
sem-ia** para todos os integrantes, e o slot do outro tratamento fica fora
do workspace aberto na IDE durante o trial, para não contaminar via
indexação do Copilot. Isso não remove o efeito de aprendizado sobre o
tempo (RQ1) — só evita que o assistente "veja" a resposta pronta do outro
tratamento.

A comparação estatística (Sprint 3) é pareada por (integrante, kata): tempo
com IA vs. tempo sem IA do mesmo par pessoa+kata. É um pareamento mais
direto que o do desenho contrabalanceado, mas o resultado da RQ1
especificamente precisa ser lido com a ressalva do efeito de aprendizado
registrada no relatório final.

## (G) Quantidade de medições

3 integrantes × 4 katas × 2 tratamentos = 24 trials no total (12 com IA / 12
sem IA), ou seja 8 trials por integrante (4 por tratamento).

## (H) Ameaças à validade

- **Efeito de aprendizado entre katas.** Resolver vários katas em sequência
  pode enviesar os últimos trials (fadiga, ou familiaridade crescente com o
  padrão de teste do experimento). Mitigação: ordem contrabalanceada entre
  integrantes.
- **Repetição do mesmo kata pela mesma pessoa (efeito de aprendizado /
  memorização direta) — ameaça aceita.** O desenho escolhido (seção F) faz
  cada integrante resolver o mesmo kata duas vezes; o segundo trial tende a
  ser mais rápido só por já conhecer o problema, não necessariamente pelo
  efeito da IA. **Isso não é eliminado pelo desenho** — é mitigado apenas
  parcialmente (ordem fixa com-ia → sem-ia, isolamento do slot do outro
  tratamento no workspace) e deve ser declarado explicitamente na leitura
  dos resultados de RQ1 no relatório final, especialmente se `sem-ia` for
  sistematicamente mais rápido que o esperado.
- **Familiaridade prévia com a ferramenta de IA.** Integrantes com mais
  experiência prévia no assistente escolhido podem ter vantagem
  independente do tratamento. Mitigação: registrar a experiência prévia de
  cada integrante no relatório final.
- **Vazamento de solução já vista / memorização pelo modelo.** Katas muito
  conhecidos (clássicos de LeetCode/HackerRank) podem levar o assistente a
  reproduzir uma solução memorizada do treinamento, em vez de efetivamente
  ajudar. Mitigação: os 4 katas são adaptações que invalidam a solução
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
  SLOC/complexidade ([`katas/README.md`](../katas/README.md)) aproxima os 4
  katas, mas não os iguala exatamente (`ranking-liga` é o mais pesado). No
  desenho repetido isso pesa menos que no contrabalanceado, porque todo
  integrante passa pelos 4 katas nos dois tratamentos — a diferença de
  dificuldade entre katas afeta os dois lados do par igualmente.

## Métricas — justificativa da escolha

- **RQ1:** time-to-green como métrica primária (mais direta e comparável
  entre katas do que contagem de interações); mediana em vez de média dado
  N pequeno (8 trials/integrante) e sensibilidade da média a outliers. Ao
  reportar RQ1, registrar também a ressalva do efeito de aprendizado
  (seções F e H) — o resultado mede "com IA vs. sem IA na segunda
  passagem pelo kata", não um contraste limpo entre tratamentos.
- **RQ2:** taxa de sucesso como métrica primária (normaliza katas com
  números diferentes de testes de aceitação); nº absoluto de testes
  falhando como métrica complementar.
- **RQ3:** complexidade ciclomática (Radon `cc`) e duplicação (jscpd),
  sempre acompanhadas de LOC/SLOC (Radon `raw`) como controle, já que
  código gerado por IA pode ser mais verboso. MI (Radon `mi`) como métrica
  composta opcional. RQ3 não sofre o mesmo viés de aprendizado que RQ1: a
  estrutura do código final não é obviamente mais simples só por ser a
  segunda tentativa.
- **Análise estatística (Sprint 3):** mediana e IQR nas tabelas
  descritivas; teste de Wilcoxon (pareado, não paramétrico) na análise
  inferencial, pareado por (integrante, kata) — 12 pares no total,
  consistente com o desenho within-subject repetido.
