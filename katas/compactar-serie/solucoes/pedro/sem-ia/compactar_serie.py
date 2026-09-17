LITERAIS = ["0","1","2","3","4","5","6","7","8","9","*","\\"]

def compactar(serie):
   lista =  list(serie)         
   index = 0
   lista_compactada = []
   while index <len(lista):
      count = 1
      while index + 1 < len(lista) and lista[index] == lista[index + 1]:
         count += 1
         index += 1
      if count >= 3:
         lista_compactada.append(f"{count}*{lista[index]}")
         index += 1
      else:
            if lista[index] in LITERAIS:
                lista_compactada.append(f"\\{lista[index]}" * count)
                index += 1
            else:
                lista_compactada.append(lista[index] * count)
                index += 1
   return "".join(lista_compactada)


def expandir(codigo):
    """Inversa de compactar. Ver README.md do kata."""
    index = 0
    expandido = []
    while index < len(codigo):
        if codigo[index] == "\\":
            expandido.append(codigo[index + 1])
            index += 2
        elif codigo[index].isdigit():
            fim = index
            while codigo[fim].isdigit():
                fim += 1
            expandido.append(codigo[fim + 1] * int(codigo[index:fim]))
            index = fim + 2
        else:
            expandido.append(codigo[index])
            index += 1
    return "".join(expandido)
