# Kata: cifra-alternada

Cifra de deslocamento em que a chave se reinicia a cada palavra e o sentido do
deslocamento alterna entre palavras.

## Funções a implementar

```python
cifrar(texto, chave) -> str
decifrar(texto, chave) -> str
```

- `texto`: string qualquer.
- `chave`: lista não vazia de inteiros.

## Regras

1. **Palavra** é uma sequência máxima de letras ASCII (`a-z`, `A-Z`). Qualquer
   caractere que não seja letra ASCII é copiado sem alteração e encerra a
   palavra corrente.
2. **Deslocamento.** A i-ésima letra **dentro da palavra corrente** (contando a
   partir de 0) é deslocada por `chave[i % len(chave)]`. O contador `i` reinicia
   em 0 a cada nova palavra.
3. **Alternância.** As palavras são numeradas a partir de 0 na ordem em que
   aparecem. Palavras de índice **par** deslocam para frente; palavras de índice
   **ímpar** deslocam para trás.
4. **Caixa preservada.** Maiúsculas continuam maiúsculas, minúsculas continuam
   minúsculas. O alfabeto é circular (`z` + 1 = `a`).
5. `decifrar` é a inversa exata de `cifrar` para a mesma chave.

## Exemplos

```python
cifrar("abc", [1])           # "bcd"
cifrar("ab cd", [1])         # "bc bc"   (2ª palavra desloca para trás)
cifrar("az", [1, 2])         # "bb"
cifrar("a-b", [1])           # "b-a"     (o hífen encerra a palavra)
decifrar(cifrar("Ola Mundo", [3, 1]), [3, 1])   # "Ola Mundo"
```

## Procedência e adaptação

- **Exercício-base:** cifra de César / cifra de Vigenère, exercícios amplamente
  indexados.
- **O que foi alterado:** (a) o índice da chave é relativo à palavra e não ao
  texto, reiniciando a cada separador; (b) o sentido do deslocamento alterna por
  paridade do índice da palavra; (c) exige a função inversa consistente com as
  duas regras acima.

A solução canônica de César/Vigenère falha nos testes de aceitação porque
mantém um único contador global e um único sentido de deslocamento.
