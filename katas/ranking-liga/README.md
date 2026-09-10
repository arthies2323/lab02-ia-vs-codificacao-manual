# Kata: ranking-liga

Classificação de uma liga com cascata de critérios de desempate, terminando em
confronto direto.

## Função a implementar

```python
classificar(times, partidas) -> list[dict]
```

- `times`: lista de nomes (strings).
- `partidas`: lista de tuplas `(casa, fora, gols_casa, gols_fora)`.

## Regras

1. **Pontuação.** Vitória vale 3 pontos, empate 1, derrota 0.
2. **Ordem de classificação**, aplicada em cascata:
   1. mais pontos;
   2. maior saldo de gols (`gols_pro - gols_contra`);
   3. mais gols pró;
   4. **confronto direto** — ver regra 3;
   5. ordem alfabética do nome.
3. **Confronto direto.** Aplica-se **apenas** quando o grupo de times empatados
   nos três primeiros critérios tem **exatamente dois** times. Nesse caso, soma-se
   o saldo de gols das partidas entre os dois; quem tiver saldo maior fica à
   frente. Se esse saldo for zero, ou se eles não se enfrentaram, vale a ordem
   alfabética. Grupos empatados com três ou mais times vão direto para a ordem
   alfabética.
4. **Saída.** Lista de dicionários, na ordem da classificação, cada um com as
   chaves `"time"`, `"pontos"`, `"gols_pro"`, `"gols_contra"` e `"saldo"`.

Times sem partidas aparecem com tudo zerado.

## Exemplo

```python
times = ["Azuis", "Verdes"]
partidas = [("Azuis", "Verdes", 2, 0), ("Verdes", "Azuis", 1, 0)]
classificar(times, partidas)
# [{"time": "Azuis", "pontos": 3, "gols_pro": 2, "gols_contra": 1, "saldo": 1},
#  {"time": "Verdes", "pontos": 3, "gols_pro": 1, "gols_contra": 2, "saldo": -1}]
```

## Procedência e adaptação

- **Exercício-base:** tabela de classificação de liga / ordenação por múltiplas
  chaves, exercício comum (variações aparecem em listas de "league table").
- **O que foi alterado:** (a) o confronto direto **não é uma chave de ordenação**
  — depende do par de times empatados, então não pode ser expresso em um único
  `sorted(key=...)`, que é exatamente como a solução canônica resolve; (b) o
  critério só vale para grupos de tamanho dois, o que exige agrupar os empatados
  antes de desempatar; (c) o desempate final alfabético é ascendente enquanto os
  demais são descendentes.

A solução canônica com uma única chave de ordenação passa nos casos sem empate
triplo e falha em todos os que exercitam o confronto direto.
