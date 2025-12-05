import random
from terreno import *

#______________________________Mapa______________________________

class Mapa:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.matriz = []

        self.crear_matriz_vacia()   #llamada al método para crear la matriz

    def crear_matriz_vacia(self):
        self.matriz = []

        for f in range(self.filas):
            fila = []

            for c in range(self.columnas):
                fila.append(None)

            self.matriz.append(fila)

    def generar_mapa(self):
        # 1. Crear todo como muro inicialmente
        for f in range(self.filas):
            for c in range(self.columnas):
                self.matriz[f][c] = Muro()

        # 2. Generar un camino aleatorio desde (0,0)
        camino = []
        visitado = set()
        pila = [(0, 0)]

        while pila:
            x, y = pila.pop()

            if (x, y) in visitado:
                continue
            visitado.add((x, y))
            camino.append((x, y))

            # si llegamos a la última fila → fin del camino
            if y == self.filas - 1:
                break

            # movimientos posibles: derecha, izquierda, arriba, abajo
            vecinos = []
            if x + 1 < self.columnas: vecinos.append((x + 1, y))
            if x - 1 >= 0: vecinos.append((x - 1, y))
            if y + 1 < self.filas: vecinos.append((x, y + 1))
            if y - 1 >= 0: vecinos.append((x, y - 1))

            random.shuffle(vecinos)
            for nx, ny in vecinos:
                if (nx, ny) not in visitado:
                    pila.append((nx, ny))

        # 3. Marcar el camino encontrado como Camino()
        for x, y in camino:
            self.matriz[y][x] = Camino()

        # 4. La última celda del camino es la salida
        salida_x, salida_y = camino[-1]
        self.matriz[salida_y][salida_x] = Salida()

        # 5. Rellenar el resto del mapa con terreno aleatorio
        for f in range(self.filas):
            for c in range(self.columnas):

                if isinstance(self.matriz[f][c], (Camino, Salida)):
                    continue

                opcion = random.randint(1, 4)

                if opcion == 1:
                    self.matriz[f][c] = Camino()
                elif opcion == 2:
                    self.matriz[f][c] = Muro()
                elif opcion == 3:
                    self.matriz[f][c] = Tunel()
                else:
                    self.matriz[f][c] = Liana()


    def obtener_casilla(self, x, y):
        if 0 <= y < self.filas and 0 <= x < self.columnas:
            return self.matriz[y][x]
        return None

    def es_camino_valido_para_jugador(self, x, y):
        #Devuelve True si el jugador puede entrar en esa casilla.
        casilla = self.obtener_casilla(x, y)
        if casilla is None:
            return False
        return not casilla.bloquea_jugador

    def es_camino_valido_para_enemigo(self, x, y):
        #Devuelve True si un cazador puede entrar en esa casilla.
        casilla = self.obtener_casilla(x, y)
        if casilla is None:
            return False
        return not casilla.bloquea_enemigo

    def mostrar_mapa(self):
        #Imprime el mapa en texto (para revision) #puede quitarse
        for fila in self.matriz:
            print(" ".join(t.nombre[0].upper() for t in fila))
