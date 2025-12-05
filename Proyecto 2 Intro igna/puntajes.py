import os

archivo = "puntajes.txt"

# __________________ AGREGAR PUNTAJE __________________

def agregar_puntaje(modo, nombre, puntaje):
    linea = nombre + "," + modo + "," + str(puntaje) + "\n"

    with open(archivo, "a", encoding="utf-8") as f:
        f.write(linea)

# __________________ OBTENER TOP 5 __________________

def obtener_top5(modo):
    if not os.path.exists(archivo):
        return []

    lista = []

    with open(archivo, "r", encoding="utf-8") as f:
        for linea in f:
            partes = linea.strip().split(",")

            if len(partes) != 3:
                continue

            nombre_arch, modo_arch, puntaje_arch = partes

            if modo_arch.lower() == modo.lower():
                lista.append((nombre_arch, int(puntaje_arch)))

    #_____________________ORDENAR______________________
                
    n = len(lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            #orden descendente por puntaje
            if lista[j][1] < lista[j + 1][1]:
                temp = lista[j]
                lista[j] = lista[j + 1]
                lista[j + 1] = temp

    return lista[:5]
