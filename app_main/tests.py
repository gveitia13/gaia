import hashlib
import uuid

lista = [123, 233, 34, 23, 34, 12]
lista2 = []
diccionario = {}
cant = 0

for i in range(len(lista)):
    j = i + 1
    for j in range(len(lista)):
        if lista[i] == lista[j]:
            cant += 1
            lista2.append(lista[i])
        cant = 0

for i in lista:
    if diccionario.get(i) is not None:
        diccionario[i] += 1
    else:
        diccionario[i] = 1

x = 0
resultado = "x es positivo" if x > 0 else "x es negativo" if x < 0 else "x es cero"
asd = 500
cat = f'00{asd}' if asd < 10 else f'{asd}' if asd > 99 else f'0{asd}'
