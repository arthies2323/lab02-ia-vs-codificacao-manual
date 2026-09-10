# Kata: torre-blocos

Validação de uma torre de blocos delimitados, com um bloco autopareado que
alterna entre abrir e fechar.

## Função a implementar

```python
analisar_torre(torre) -> dict
```

- `torre`: string.

## Regras

1. **Blocos pareados.** `(`/`)`, `[`/`]` e `{`/`}` funcionam como delimitadores
   normais, com fechamento na ordem inversa da abertura (o último aberto é o
   primeiro a fechar).
2. **Bloco autopareado.** O caractere `|` não tem par distinto. Ao encontrá-lo:
   - se o bloco **no topo** da pilha for um `|`, ele **fecha** esse bloco;
   - caso contrário, ele **abre** um novo bloco.
3. **Outros caracteres** são ignorados e não afetam a torre.
4. **Saída.** Um dicionário com:
   - `"valida"`: `True` se a torre está completa e bem formada.
   - `"profundidade_maxima"`: maior número de blocos abertos simultaneamente
     alcançado durante a leitura, **inclusive quando a torre é inválida**
     (conta-se o que foi atingido até o ponto do erro).
   - `"erro_posicao"`: índice (base 0) do primeiro caractere problemático, ou
     `None` se a torre é válida. Para um fechamento indevido, é a posição do
     caractere que fecha errado; para blocos que nunca fecham, é a posição do
     **primeiro** bloco que ficou aberto.

String vazia é válida, com profundidade `0` e `erro_posicao` `None`.

## Exemplos

```python
analisar_torre("([{}])")
# {"valida": True, "profundidade_maxima": 3, "erro_posicao": None}

analisar_torre("||")
# {"valida": True, "profundidade_maxima": 1, "erro_posicao": None}

analisar_torre("|()|")
# {"valida": True, "profundidade_maxima": 2, "erro_posicao": None}

analisar_torre("(|)")
# {"valida": False, "profundidade_maxima": 2, "erro_posicao": 2}

analisar_torre("((")
# {"valida": False, "profundidade_maxima": 2, "erro_posicao": 0}
```

## Procedência e adaptação

- **Exercício-base:** validação de parênteses balanceados com pilha
  ("valid parentheses"), um dos exercícios mais indexados que existem.
- **O que foi alterado:** (a) o delimitador autopareado `|` quebra o mapa
  fixo abre→fecha da solução canônica, porque o mesmo caractere muda de papel
  conforme o topo da pilha; (b) a saída deixa de ser booleana e passa a exigir
  profundidade máxima e localização do erro; (c) a profundidade precisa ser
  reportada mesmo em torres inválidas, o que impede o retorno antecipado puro.

A solução canônica devolve apenas `True`/`False` e usa um dicionário de pares
fixo — ela falha em todos os casos com `|` e em toda a parte de diagnóstico.
