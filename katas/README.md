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
(48 SLOC, CC total 18, ~2x o mais leve). Como o desenho é contrabalanceado e
cada kata é resolvido nos dois tratamentos ao longo do trio, uma diferença de
dificuldade entre katas adiciona **variância**, não viés na comparação entre
tratamentos — desde que a ordem de contrabalanceamento garanta que cada kata
apareça sob os dois tratamentos. Isso é uma restrição para o desenho do
experimento (issue #1).

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
   árvore, a solução `sem-ia` de um kata fica ao lado da `com-ia` do mesmo
   integrante. Se o trial manual vier primeiro, o assistente indexa a resposta
   pronta no trial seguinte — e o tratamento deixa de medir assistência e passa
   a medir cópia.

**Regras para a S02:**

- Cada integrante roda seus trials a partir da tag `katas-v1` (estado limpo dos
  katas), em uma branch própria: `trials-<nome>`.
- Nenhum integrante faz merge/rebase da branch de outro antes de terminar todos
  os seus trials.
- Os testes de aceitação (`test_*.py`) não podem ser editados durante o trial.
- O merge das branches de trials para a `main` só acontece quando todos os
  trials estiverem concluídos.
- **Se o mesmo integrante resolver o mesmo kata nos dois tratamentos**, o trial
  `com-ia` vem **antes** do `sem-ia` e os slots do outro tratamento ficam fora
  do workspace aberto na IDE (abra a pasta do slot, não a raiz do repositório).
  A ordem inversa contamina o `com-ia`; nenhuma ordem elimina o efeito de
  aprendizado — ver a ressalva abaixo.

### Decisão de desenho: o mesmo kata nos dois tratamentos

A estrutura de 6 slots por kata comporta dois desenhos possíveis
(contrabalanceado ou repetido); o grupo avaliou os dois e **decidiu pelo
repetido**, formalizado em
[`docs/DESENHO_EXPERIMENTO.md`](../docs/DESENHO_EXPERIMENTO.md#f-tipo-de-projeto-experimental):

- **Repetido (24 trials) — escolhido.** Cada integrante resolve os 4 katas
  duas vezes, uma em cada tratamento (8 trials por integrante). Dobra o N em
  relação ao contrabalanceado, mas introduz **efeito de aprendizado**: a
  segunda passagem pelo mesmo kata é mais rápida por já conhecer o problema,
  não necessariamente pelo tratamento. O ganho medido em RQ1 fica confundido
  com a ordem, e o time-box de 35 min não protege contra isso — por isso é
  **obrigatório** declarar essa ameaça na leitura de RQ1 no relatório final.
- **Contrabalanceado (12 trials) — não usado.** Cada integrante resolveria
  cada kata uma única vez (metade com IA, metade sem), com cada kata
  aparecendo nos dois tratamentos ao longo do trio. Evitaria o efeito de
  aprendizado, ao custo de menos dados por integrante.

**Regra obrigatória por causa da escolha acima:** a ordem é sempre `com-ia`
primeiro, depois `sem-ia`, igual para todo mundo — é a regra já listada
acima em "Regras para a S02".
