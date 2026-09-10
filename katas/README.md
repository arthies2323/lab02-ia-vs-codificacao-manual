# Katas — objetos experimentais

Seis katas em Python, de dificuldade comparável, usados como objetos
experimentais do experimento (Passo 2). Número par, para permitir a divisão
exata entre trials **com-ia** e **sem-ia**.

## Os 6 katas

| kata | tema | funções | testes |
|---|---|---|---|
| [agenda-turnos](agenda-turnos/) | intervalos circulares com folga mínima | 1 | 9 |
| [cifra-alternada](cifra-alternada/) | cifra com chave por palavra e sentido alternado | 2 | 11 |
| [fatura-progressiva](fatura-progressiva/) | faixas progressivas com bônus retroativo | 1 | 9 |
| [torre-blocos](torre-blocos/) | pilha com delimitador autopareado | 1 | 10 |
| [ranking-liga](ranking-liga/) | cascata de desempate com confronto direto | 1 | 9 |
| [compactar-serie](compactar-serie/) | RLE com limiar e escape | 2 | 14 |

Total: **62 testes de aceitação**.

## Estrutura de cada kata

```
katas/<slug>/
  README.md            enunciado, regras, exemplos, procedência da adaptação
  conftest.py          põe solucao/ no sys.path
  test_<modulo>.py     testes de aceitação (pytest) — NÃO editar durante o trial
  solucao/
    <modulo>.py        stub com a assinatura; é aqui que o participante escreve
```

O diretório `solucao/` é também o alvo da coleta de métricas estáticas:

```bash
python scripts/collect_static_metrics.py --path katas/<slug>/solucao \
    --kata <slug> --integrante <nome> --tratamento com-ia
```

## Execução

```bash
python -m pip install -r scripts/requirements.txt
python -m pytest katas/<slug>          # um kata
python -m pytest katas                 # todos (deve falhar: stubs)
```

## Baixa indexação: como as adaptações foram feitas

A ameaça de validade central deste experimento é a **memorização**: se o kata
for um exercício clássico, o assistente de IA reproduz uma solução vista no
treinamento em vez de efetivamente ajudar, e o tratamento deixa de medir o que
se propõe a medir.

Todos os 6 katas partem de exercícios conhecidos, mas foram adaptados segundo
uma regra fixa: **a alteração precisa invalidar a solução canônica**, não apenas
renomear variáveis ou trocar o domínio. Em cada kata, a seção "Procedência e
adaptação" do README registra o exercício-base, o que foi mudado e por que a
solução canônica falha nos testes de aceitação.

Os mecanismos usados foram:

- **Inverter o invariante** — o limiar de 3 em `compactar-serie` quebra a
  premissa do RLE de que toda sequência vira contagem+caractere.
- **Quebrar a estrutura de dados da solução** — o `|` autopareado em
  `torre-blocos` impede o dicionário fixo abre→fecha; o confronto direto em
  `ranking-liga` não cabe em uma única chave de `sorted()`.
- **Adicionar uma regra que contradiz o caso geral** — o bônus retroativo em
  `fatura-progressiva` faz a solução progressiva correta errar justamente nos
  consumos altos.
- **Mudar o escopo do estado** — o índice da chave por palavra em
  `cifra-alternada`; a divisão na meia-noite em `agenda-turnos`.
- **Exigir saída diagnóstica** — profundidade máxima e posição do erro em
  `torre-blocos`, cobertura e lacunas em `agenda-turnos`, em vez do booleano ou
  da lista que o exercício-base devolve.

## Validação de dificuldade equivalente

Além da revisão cruzada do trio, a equivalência foi ancorada em métricas
objetivas: uma solução de referência foi escrita para cada kata e medida com o
mesmo [`collect_static_metrics.py`](../scripts/collect_static_metrics.py) que
será usado na RQ3.

| kata | testes | SLOC | CC média | CC máx | CC total | funções |
|---|---|---|---|---|---|---|
| agenda-turnos | 9 | 32 | 4.33 | 11 | 13 | 3 |
| cifra-alternada | 11 | 26 | 3.33 | 8 | 10 | 3 |
| fatura-progressiva | 9 | 21 | 9.0 | 9 | 9 | 1 |
| torre-blocos | 10 | 31 | 10.0 | 10 | 10 | 1 |
| ranking-liga | 9 | 48 | 6.0 | 10 | 18 | 3 |
| compactar-serie | 14 | 36 | 6.0 | 7 | 12 | 2 |

Faixas obtidas: SLOC 21–48 (mediana 31,5), CC total 9–18, testes 9–14. As
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

O tratamento usa **GitHub Copilot**, que indexa o workspace aberto. Sem
cuidado, o experimento se contamina de duas formas:

1. **Solução de referência no repositório.** Se existir um arquivo com a solução
   pronta dentro do workspace, o trial "com-ia" vira cópia. Por isso **as
   soluções de referência não estão versionadas neste repositório** — elas foram
   usadas apenas para a validação de dificuldade acima e são mantidas fora da
   árvore de trabalho.

2. **Soluções de um integrante contaminando os seguintes.** Se o integrante A
   commitar suas 6 soluções e B fizer `pull` antes de rodar seus trials, o
   Copilot de B indexa as soluções de A.

**Regras para a S02:**

- Cada integrante roda seus trials a partir da tag `katas-v1` (estado limpo dos
  katas), em uma branch própria: `trials-<nome>`.
- Nenhum integrante faz merge/rebase da branch de outro antes de terminar todos
  os seus 6 trials.
- Os testes de aceitação (`test_*.py`) não podem ser editados durante o trial.
- O merge das branches de trials para a `main` só acontece quando os 18 trials
  estiverem concluídos.
