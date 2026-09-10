# Kata: compactar-serie

Compactação de sequências com limiar mínimo de repetição e escape de caracteres
ambíguos.

## Funções a implementar

```python
compactar(serie) -> str
expandir(codigo) -> str
```

## Regras

1. **Limiar.** Uma sequência de `n` caracteres iguais só é compactada quando
   `n >= 3`, virando `"{n}*{caractere}"`. Sequências de 1 ou 2 caracteres são
   copiadas literalmente.
2. **Escape.** Ao copiar um caractere literalmente, se ele for um dígito
   (`0`-`9`), um asterisco (`*`) ou uma barra invertida (`\`), ele deve ser
   precedido por `\`. Dentro da forma compactada `"{n}*{caractere}"`, o
   caractere **não** é escapado — a posição já o torna inequívoco.
3. **Inversa.** `expandir` reconstrói exatamente a string original:
   `expandir(compactar(s)) == s` para qualquer `s`.
4. Contagens podem ter mais de um dígito (`"12*a"` são doze `a`).

String vazia devolve string vazia em ambas as funções.

## Exemplos

```python
compactar("aaabb")     # "3*abb"
compactar("aa")        # "aa"
compactar("a11")       # "a\\1\\1"     (dois digitos avulsos, escapados)
compactar("1111")      # "4*1"
compactar("**")        # "\\*\\*"
compactar("a" * 12)    # "12*a"

expandir("3*abb")      # "aaabb"
expandir("a\\1\\1")    # "a11"
```

> Nos exemplos acima a barra aparece dobrada por ser notação de string Python;
> a string real contém uma única barra.

## Procedência e adaptação

- **Exercício-base:** *run-length encoding* (RLE), exercício clássico e
  altamente indexado.
- **O que foi alterado:** (a) o limiar de 3 quebra o invariante do RLE canônico,
  em que toda sequência vira `contagem+caractere`; (b) a mistura de trechos
  compactados e literais no mesmo fluxo torna a decodificação ambígua sem o
  esquema de escape, que é a parte central do kata; (c) exige o par
  codificador/decodificador consistente, e não apenas o codificador.

O RLE canônico produz `"3a2b"` para `"aaabb"` e falha em todos os testes; o
esquema de escape não tem contrapartida no exercício original.
