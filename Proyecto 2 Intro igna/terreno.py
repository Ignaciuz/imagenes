import random

#___________________________Terreno______________________________

class TerrenoBase:
    #Clase base para todos los tipos de terrenoS
    nombre = "terreno"
    color = "white"    
    bloquea_jugador = False
    bloquea_enemigo = False

class Camino(TerrenoBase):
    nombre = "camino"
    color = "#ecf0f1"
    bloquea_jugador = False
    bloquea_enemigo = False

class Muro(TerrenoBase):
    nombre = "muro"
    color = "#2c3e50"
    bloquea_jugador = True
    bloquea_enemigo = True

class Tunel(TerrenoBase):
    nombre = "tunel"
    color = "#C0C0C0"
    bloquea_jugador = False
    bloquea_enemigo = True  #solo el jugador puede entrar

class Liana(TerrenoBase):
    nombre = "liana"
    color = "#90EE90"
    bloquea_jugador = True   #ugador NO puede entrar
    bloquea_enemigo = False  #cazadores sí pueden entrar

class Salida(TerrenoBase):
    nombre = "salida"
    color = "green"
    bloquea_jugador = False
    bloquea_enemigo = False
