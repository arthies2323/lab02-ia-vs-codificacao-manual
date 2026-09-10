# Kata: fatura-progressiva

Cálculo de fatura por faixas progressivas de consumo, com uma regra de bônus
retroativo que substitui o cálculo por faixas.

## Função a implementar

```python
calcular_fatura(consumo, faixas, bonus_limite=None) -> dict
```

- `consumo`: número (int ou float), sempre `>= 0`.
- `faixas`: lista de tuplas `(limite_superior, preco)`, em ordem crescente de
  `limite_superior`. A **última** faixa tem `limite_superior is None`,
  representando "daí em diante".
- `bonus_limite`: número ou `None`.

## Regras

1. **Cobrança progressiva.** O consumo é fatiado entre as faixas: a porção que
   cai em cada faixa é cobrada ao preço daquela faixa (como uma tabela de
   imposto de renda), e não ao preço da faixa mais alta atingida.
2. **Limite é exclusivo.** Um consumo exatamente igual ao `limite_superior` de
   uma faixa é cobrado inteiramente dentro dela e **não** abre a faixa seguinte.
3. **Bônus retroativo.** Se `bonus_limite` não é `None` e
   `consumo > bonus_limite` (estritamente), a regra progressiva é **descartada**
   e todo o consumo é cobrado ao preço da **primeira** faixa.
4. **Saída.** Um dicionário com:
   - `"total"`: valor final, arredondado com `round(valor, 2)`.
   - `"detalhe"`: lista de tuplas `(indice_da_faixa, quantidade, subtotal)`,
     apenas para as faixas efetivamente usadas, com cada `subtotal` arredondado
     com `round(valor, 2)`. Quando o bônus retroativo se aplica, o detalhe é uma
     única tupla `(0, consumo, total)`.
   - `"retroativo"`: `True` se a regra de bônus foi aplicada, `False` caso
     contrário.

Consumo `0` devolve `{"total": 0, "detalhe": [], "retroativo": False}`.

## Exemplos

Com `faixas = [(100, 0.5), (200, 0.8), (None, 1.2)]`:

```python
calcular_fatura(50, faixas)
# {"total": 25.0, "detalhe": [(0, 50, 25.0)], "retroativo": False}

calcular_fatura(150, faixas)
# {"total": 90.0, "detalhe": [(0, 100, 50.0), (1, 50, 40.0)], "retroativo": False}

calcular_fatura(250, faixas, bonus_limite=200)
# {"total": 125.0, "detalhe": [(0, 250, 125.0)], "retroativo": True}
```

## Procedência e adaptação

- **Exercício-base:** cálculo de faturamento por faixas / imposto progressivo,
  exercício comum em listas de lógica de negócio.
- **O que foi alterado:** (a) a regra de bônus retroativo inverte o resultado
  esperado justamente nos consumos altos, onde a solução progressiva canônica
  estaria correta; (b) a saída exige o rastro por faixa e não apenas o total;
  (c) a semântica exclusiva do limite muda o comportamento nos valores de borda.

Uma solução progressiva padrão passa nos casos baixos e falha em todos os casos
com bônus, o que torna o kata sensível à leitura completa do enunciado.
