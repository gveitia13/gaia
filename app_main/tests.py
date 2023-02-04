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

print(lista2)

for i in lista:
    if diccionario.get(i) is not None:
        diccionario[i] += 1
    else:
        diccionario[i] = 1
