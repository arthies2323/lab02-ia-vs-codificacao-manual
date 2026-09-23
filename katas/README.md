# Katas — objetos experimentais

Quatro katas em Python, de dificuldade comparável, usados como objetos
experimentais do experimento (Passo 2). Número par, para permitir a divisão
exata entre trials **com-ia** e **sem-ia**.

## Os 4 katas

| kata | tema | funções | testes |
|---|---|---|---|
| [agenda-turnos](agenda-turnos/) | intervalos circulares com folga mínima | 1 | 9 |
| [fatura-progressiva](fatura-progressiva/) | faixas progressivas com bônus retroativo | 1 | 9 |
| [ranking-liga](ranking-liga/) | cascata de desempate com confronto direto | 1 | 9 |
| [compactar-serie](compactar-serie/) | RLE com limiar e escape | 2 | 14 |

Total: **41 testes de aceitação**.

## Estrutura de cada kata

Cada kata hospeda **6 slots de solução independentes** — um por integrante x
tratamento — para que os 3 integrantes resolvam o mesmo kata com e sem IA sem
sobrescrever o trabalho uns dos outros:

```
katas/<slug>/
  README.md            enunciado, regras, exemplos, procedência da adaptação
  TEMPOS.md            tabela de time-to-green dos 6 trials deste kata
  test_<modulo>.py     testes de aceitação (pytest) — NÃO editar durante o trial
  solucoes/
    arthur/
      sem-ia/<modulo>.py    stub com a assinatura; é aqui que o participante escreve
      com-ia/<modulo>.py
    gabriel/
      sem-ia/<modulo>.py
      com-ia/<modulo>.py
    pedro/
      sem-ia/<modulo>.py
      com-ia/<modulo>.py
```

O arquivo de teste é **um só** para os 6 slots e não é duplicado. Quem decide
qual slot ele importa é o [`conftest.py`](conftest.py) na raiz de `katas/`:
antes da coleta, ele publica `solucoes/<integrante>/<tratamento>/` no
`sys.path`, a partir de `--integrante`/`--tratamento` (ou das variáveis
`KATA_INTEGRANTE`/`KATA_TRATAMENTO`). Sem essa seleção o pytest para com uma
mensagem explícita, em vez de falhar com um `ModuleNotFoundError` obscuro.

O slot é também o alvo da coleta de métricas estáticas:

```bash
python scripts/collect_static_metrics.py \
    --path katas/<slug>/solucoes/<integrante>/<tratamento> \
    --kata <slug> --integrante <integrante> --tratamento com-ia
```

## Execução

```bash
python -m pip install -r scripts/requirements.txt

# um kata, um trial
python -m pytest katas/<slug> --integrante pedro --tratamento sem-ia

# todos os katas do mesmo trial (deve falhar: stubs)
python -m pytest katas --integrante pedro --tratamento sem-ia
```

Em trials reais, prefira o cronômetro — ele roda o pytest no slot certo
sozinho e grava o tempo em `data/timings.csv`:

```bash
python scripts/timer.py --kata <slug> --tratamento sem-ia --integrante pedro
```

## Registro de tempo

Cada kata tem um [`TEMPOS.md`](agenda-turnos/TEMPOS.md) na raiz, com uma linha
por integrante x tratamento. É a versão legível e revisável do time-to-green;
a fonte da análise da RQ1 continua sendo `data/timings.csv`, gerado pelo
`scripts/timer.py`. Em caso de divergência, o CSV prevalece.

## Baixa indexação: como as adaptações foram feitas

A ameaça de validade central deste experimento é a **memorização**: se o kata
for um exercício clássico, o assistente de IA reproduz uma solução vista no
treinamento em vez de efetivamente ajudar, e o tratamento deixa de medir o que
se propõe a medir.

Todos os 4 katas partem de exercícios conhecidos, mas foram adaptados segundo
uma regra fixa: **a alteração precisa invalidar a solução canônica**, não apenas
renomear variáveis ou trocar o domínio. Em cada kata, a seção "Procedência e
adaptação" do README registra o exercício-base, o que foi mudado e por que a
solução canônica falha nos testes de aceitação.

Os mecanismos usados foram:

- **Inverter o invariante** — o limiar de 3 em `compactar-serie` quebra a
  premissa do RLE de que toda sequência vira contagem+caractere.
- **Quebrar a estrutura de dados da solução** — o confronto direto em
  `ranking-liga` não cabe em uma única chave de `sorted()`.
- **Adicionar uma regra que contradiz o caso geral** — o bônus retroativo em
  `fatura-progressiva` faz a solução progressiva correta errar justamente nos
  consumos altos.
- **Mudar o escopo do estado** — a divisão na meia-noite em `agenda-turnos`.
- **Exigir saída diagnóstica** — cobertura e lacunas em `agenda-turnos`, em vez
  da lista que o exercício-base devolve.

## Validação de dificuldade equivalente

Além da revisão cruzada do trio, a equivalência foi ancorada em métricas
objetivas: uma solução de referência foi escrita para cada kata e medida com o
mesmo [`collect_static_metrics.py`](../scripts/collect_static_metrics.py) que
será usado na RQ3.

| kata | testes | SLOC | CC média | CC máx | CC total | funções |
|---|---|---|---|---|---|---|
| agenda-turnos | 9 | 32 | 4.33 | 11 | 13 | 3 |
| fatura-progressiva | 9 | 21 | 9.0 | 9 | 9 | 1 |
| ranking-liga | 9 | 48 | 6.0 | 10 | 18 | 3 |
| compactar-serie | 14 | 36 | 6.0 | 7 | 12 | 2 |

Faixas obtidas: SLOC 21–48 (mediana 34), CC total 9–18, testes 9–14. As
soluções de referência usam apenas a biblioteca padrão e nenhuma estrutura de
dados além de listas e dicionários.

**Ressalva a registrar no relatório:** `ranking-liga` é o kata mais pesado
(48 SLOC, CC total 18, ~2x o mais leve). Foi justamente essa dispersão que
motivou o desenho repetido: como cada integrante resolve o **mesmo** kata nos
dois tratamentos, a dificuldade do kata é constante dentro do par e some na
comparação pareada, em vez de entrar no contraste entre tratamentos. No
desenho contrabalanceado ela seria viés, não apenas variância.

A `CC média` é sensível ao número de funções extraídas, que é escolha de estilo
de quem resolve; para comparar katas, `CC total` e `SLOC` são os indicadores
mais estáveis.

## ⚠️ Protocolo anti-contaminação (obrigatório na S02)

O tratamento usa **Claude Code (Claude Opus 5)**, que indexa o workspace aberto. Sem
cuidado, o experimento se contamina de duas formas:

1. **Solução de referência no repositório.** Se existir um arquivo com a solução
   pronta dentro do workspace, o trial "com-ia" vira cópia. Por isso **as
   soluções de referência não estão versionadas neste repositório** — elas foram
   usadas apenas para a validação de dificuldade acima e são mantidas fora da
   árvore de trabalho.

2. **Soluções de um integrante contaminando os seguintes.** Se o integrante A
   commitar suas soluções e B fizer `pull` antes de rodar seus trials, o
   Claude Code de B indexa as soluções de A.

3. **O slot vizinho do próprio integrante.** Como os 6 slots convivem na mesma
   árvore e o trial manual vem primeiro, a solução `sem-ia` já existiria ao
   lado da `com-ia` quando o agente fosse acionado — e o assistente a indexaria,
   fazendo o tratamento medir cópia em vez de assistência.

   **Mitigação: os dois tratamentos são implementados em branches separadas.**
   O trial `com-ia` roda em uma branch onde a solução manual daquele kata
   simplesmente não existe na árvore de trabalho, de modo que não há o que
   indexar — a separação é garantida pelo versionamento, não pela disciplina de
   quais abas ficam abertas na IDE. Como reforço, a spec entregue ao agente
   traz instrução explícita de não procurar implementações prontas, no
   repositório ou fora dele.

**Regras para a S02:**

- Cada integrante roda seus trials a partir da tag `katas-v1` (estado limpo dos
  katas), em uma branch própria: `trials-<nome>`.
- Nenhum integrante faz merge/rebase da branch de outro antes de terminar todos
  os seus trials.
- Os testes de aceitação (`test_*.py`) não podem ser editados durante o trial.
- O merge das branches de trials para a `main` só acontece quando todos os
  trials estiverem concluídos.
- **Ordem dos tratamentos:** o trial `sem-ia` vem **antes** do `com-ia`. A
  revisão do código gerado pelo agente expõe decisões de implementação; fazê-la
  antes do trial manual daria pistas à condição de controle. Ver a decisão de
  desenho abaixo.
- **Uma branch por tratamento.** O trial `com-ia` roda em branch separada da do
  trial `sem-ia`, para que a solução manual do mesmo kata não esteja na árvore
  de trabalho enquanto o agente atua (ver item 3 acima). A spec entregue ao
  agente instrui explicitamente a não buscar implementações prontas.
- **Cada kata começa pela spec.** Antes de implementar, escreva um documento com
  design, abordagem, assinaturas e critérios de aceitação, cronometrando essa
  etapa. Ela é a entrada do agente no trial `com-ia` e entra no tempo dos dois
  tratamentos — no `sem-ia` já dentro do cronômetro, no `com-ia` somada depois,
  porque a spec precede o acionamento do agente.

### Decisão de desenho: o mesmo kata nos dois tratamentos

A estrutura de 6 slots por kata comporta dois desenhos possíveis
(contrabalanceado ou repetido); o grupo avaliou os dois e **decidiu pelo
repetido**, formalizado em
[`docs/DESENHO_EXPERIMENTO.md`](../docs/DESENHO_EXPERIMENTO.md#f-tipo-de-projeto-experimental):

- **Repetido (24 trials) — escolhido.** Cada integrante resolve os 4 katas
  duas vezes, uma em cada tratamento (8 trials por integrante). Dobra o N e,
  principalmente, neutraliza a diferença de dificuldade entre katas: como cada
  kata aparece nos **dois lados do par**, sua dificuldade intrínseca vira uma
  constante dentro do par. Isso importa porque katas de dificuldade
  classificada como equivalente custam tempos bem diferentes na prática — a
  descoberta de um invariante não óbvio ou acontece rápido ou consome o
  time-box inteiro, quase sem valores intermediários.
- **Contrabalanceado (12 trials) — não usado.** Cada integrante resolveria
  cada kata uma única vez (metade com IA, metade sem), com cada kata
  aparecendo nos dois tratamentos ao longo do trio. Evitaria o efeito de
  aprendizado, mas jogaria a diferença de dificuldade entre katas direto no
  contraste entre tratamentos, com direção dependente do sorteio.

**Por que o desenho repetido não invalida a RQ1.** O efeito de aprendizado é
atacado pelo protocolo, não ignorado: a spec é escrita uma vez e cobrada dos
dois tratamentos, então o segundo trial não herda de graça a etapa de
compreensão e projeto; e como a spec é congelada antes da implementação manual
e é a única entrada do agente, o que o participante aprendeu implementando à
mão não alcança o trial com IA. Some-se a ordem fixa `sem-ia` → `com-ia`, que
mantém a condição de controle livre de qualquer exposição a código gerado.

Resta uma parcela residual — familiaridade com o problema — que o grupo trata
como **ameaça aceita e declarada** na leitura de RQ1 do relatório final.
