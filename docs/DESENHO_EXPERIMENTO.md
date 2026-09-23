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
| RQ1 | Tempo de resolução   | Tempo total do ciclo de resolução (min) = confecção da spec + time-to-green medido por [`scripts/timer.py`](../scripts/timer.py); censurado em 35 min se não passar. Agregação: mediana por tratamento. Ver "Protocolo de execução de um trial" abaixo. |
| RQ2 | Defeitos             | Taxa de sucesso (% testes passando); nº absoluto de testes falhando ao final do time-box.    |
| RQ3 | Estrutura do código  | Complexidade ciclomática média e LOC/SLOC (Radon), duplicação (jscpd), coletados por [`scripts/collect_static_metrics.py`](../scripts/collect_static_metrics.py); MI (Radon `mi`) como métrica composta opcional. |

## (C) Variável independente

Uso ou não de assistente de IA generativa durante a resolução do kata
(binária: com IA / sem IA).

## (D) Tratamentos

1. **Com IA** — assistente de IA habilitado durante todo o trial. O
   assistente em uso é o **Claude Code (Claude Opus 5)**, mesmo assistente
   em todos os trials do experimento — escolha permitida pelo enunciado do
   laboratório, que lista Claude entre os chatbots aceitos.
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
[`katas/README.md`](../katas/README.md) ("Decisão de desenho"). O grupo optou
pelo desenho repetido por duas razões: dobrar o N por integrante e, sobretudo,
neutralizar a diferença de dificuldade entre katas, que no desenho
contrabalanceado entraria diretamente no contraste entre tratamentos. No
desenho repetido cada kata aparece nos dois lados do par, e sua dificuldade
intrínseca é eliminada por construção.

### Protocolo de execução de um trial

A ordem e a separação de fases abaixo são parte do desenho, não detalhe
operacional: são elas que sustentam a validade do desenho repetido.

1. **Leitura** do enunciado e dos testes de aceitação.
2. **Confecção da spec (cronometrada):** o participante escreve um documento
   com design, abordagem, assinaturas das funções e critérios de aceitação.
3. **Execução:** é o único passo em que os tratamentos divergem. No `sem-ia`
   o participante implementa à mão; no `com-ia` a spec do passo 2 é a entrada
   do agente, que executa a implementação.
4. **Verificação:** green ou time-box de 35 min, o que vier primeiro.
5. **Revisão** do código produzido, sempre **após** a parada do cronômetro.

**Ordem dos tratamentos: `sem-ia` antes de `com-ia`**, igual para todos os
integrantes. A revisão do código gerado pelo agente (passo 5) expõe decisões
concretas de implementação; realizá-la antes do trial manual daria ao
participante pistas que a condição de controle deve não ter.

Como a ordem faz a solução manual já existir quando o agente é acionado, cada
tratamento é implementado em uma **branch separada**: no trial `com-ia` a
solução manual daquele kata não está na árvore de trabalho, então não há o que
o Claude Code indexe. A separação é garantida pelo versionamento, e não pela
disciplina de quais arquivos ficam abertos na IDE. Como reforço, a spec
entregue ao agente instrui explicitamente a não buscar implementações prontas.

**Como isso neutraliza o efeito de aprendizado.** A spec é escrita uma vez por
(integrante, kata) e seu tempo é cobrado dos **dois** tratamentos — embutido
no trial manual e somado explicitamente ao trial com IA. Duas consequências:
(i) o segundo trial não herda de graça a etapa de compreensão e projeto, que é
onde o aprendizado de fato ocorre; e (ii) como a spec é congelada antes da
implementação manual e é a única entrada do agente, o que o participante
aprendeu implementando à mão não alcança o trial seguinte. Resta uma parcela
residual de familiaridade com o problema, tratada na seção H como ameaça
aceita e declarada.

A comparação estatística (Sprint 3) é pareada por (integrante, kata): tempo
com IA vs. tempo sem IA do mesmo par pessoa+kata.

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
  cada integrante resolver o mesmo kata duas vezes; em tese o segundo trial
  tende a ser mais rápido só por já conhecer o problema, não necessariamente
  pelo efeito da IA. O protocolo da seção F reduz substancialmente esse
  efeito — spec cobrada dos dois tratamentos e congelada antes da
  implementação manual, ordem fixa `sem-ia` → `com-ia`, isolamento do slot do
  outro tratamento no workspace — mas **não o elimina**: resta a familiaridade
  do participante com o problema. Deve ser declarado explicitamente na leitura
  dos resultados de RQ1 no relatório final.
- **Familiaridade prévia com a ferramenta de IA.** Integrantes com mais
  experiência prévia no assistente escolhido podem ter vantagem
  independente do tratamento. Mitigação: registrar a experiência prévia de
  cada integrante no relatório final.
- **Vazamento de solução já vista / memorização pelo modelo.** Katas muito
  conhecidos (clássicos de LeetCode/HackerRank) podem levar o assistente a
  reproduzir uma solução memorizada do treinamento, em vez de efetivamente
  ajudar. Mitigação: os 4 katas são adaptações que invalidam a solução
  canônica (detalhado em [`katas/README.md`](../katas/README.md)).
- **Contaminação via indexação do workspace pelo Claude Code.** Ameaça
  identificada durante a preparação (Passo 2): como o Claude Code indexa os
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
