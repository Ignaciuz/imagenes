import tkinter as tk
from tkinter import messagebox

from mapa import Mapa
from terreno import Salida
from gui import *
from puntajes import agregar_puntaje

from PIL import Image, ImageTk

import time
import random

from sonido import *
from animaciones import *
#___________________________________________________________________________

class Enemigo:
    def __init__(self, enemigo_y, enemigo_x):
        # misma idea que el jugador: (x,columna) — (y,fila)
        self.enemigo_x = enemigo_x
        self.enemigo_y = enemigo_y

        self.ultima_pos = None      
        self.historial = [] 

    def mover(self, mov_y, mov_x, mapa):
        nueva_y = self.enemigo_y + mov_y
        nueva_x = self.enemigo_x + mov_x

        # validar destino primero (nota: mapa.es_camino_valido_para_enemigo espera (x,y))
        if not mapa.es_camino_valido_para_enemigo(nueva_x, nueva_y):
            return False

        self.enemigo_y = nueva_y
        self.enemigo_x = nueva_x
        return True

    def mover_aleatorio(self, mapa):
        movimientos = [(1,0),(-1,0),(0,1),(0,-1)]
        random.shuffle(movimientos)

        for dy, dx in movimientos:
            if self.mover(dy, dx, mapa):
                return True
        return False

    # Cambiado para recibir coordenadas en lugar de un objeto jugador
    def perseguir(self, jugador_x, jugador_y, mapa):
        movimientos = []

        # Diferencias
        dy = jugador_y - self.enemigo_y
        dx = jugador_x - self.enemigo_x

        # Elegir el eje principal (el que está más lejos)
        if abs(dy) > abs(dx):
            # primero vertical
            if dy < 0: movimientos.append((-1, 0))
            elif dy > 0: movimientos.append((1, 0))

            # luego horizontal
            if dx < 0: movimientos.append((0, -1))
            elif dx > 0: movimientos.append((0, 1))
        else:
            # primero horizontal
            if dx < 0: movimientos.append((0, -1))
            elif dx > 0: movimientos.append((0, 1))

            # luego vertical
            if dy < 0: movimientos.append((-1, 0))
            elif dy > 0: movimientos.append((1, 0))

        # Intentar movimientos calculados en orden
        for mov_y, mov_x in movimientos:
            if self.mover(mov_y, mov_x, mapa):
                return True

        # Último recurso: movimiento aleatorio
        return self.mover_aleatorio(mapa)

    def ir_a_salida(self, mapa):
        # (sin cambios; tu función es razonable)
        ex = self.enemigo_x
        ey = self.enemigo_y

        # localizar salida
        salida = None
        y = 0
        while y < mapa.filas:
            x = 0
            while x < mapa.columnas:
                if isinstance(mapa.matriz[y][x], Salida):
                    salida = (x, y)
                    break
                x += 1
            if salida is not None:
                break
            y += 1

        if salida is None:
            return False

        salida_x = salida[0]
        salida_y = salida[1]

        try:
            temp = self.historial
        except:
            self.historial = []

        movimientos = [(-1, 0), (1, 0), (0, -1),(0, 1)]

        opciones = []

        # evaluar movimientos
        i = 0
        while i < len(movimientos):
            dy = movimientos[i][0]
            dx = movimientos[i][1]

            ny = ey + dy
            nx = ex + dx

            # fuera del mapa
            if not (0 <= ny < mapa.filas and 0 <= nx < mapa.columnas):
                i += 1
                continue

            # no puede pasar
            if not mapa.es_camino_valido_para_enemigo(nx, ny):
                i += 1
                continue

            # evitar casilla recién visitada
            reciente = False
            j = 0
            while j < len(self.historial):
                if self.historial[j] == (nx, ny):
                    reciente = True
                    break
                j += 1

            if reciente:
                i += 1
                continue

            # calcular distancia Manhattan
            dist = abs(salida_x - nx) + abs(salida_y - ny)

            opciones.append([dist, dy, dx])
            i += 1

        # escoger la mejor opción
        if len(opciones) > 0:
            mejor = opciones[0]
            k = 1
            while k < len(opciones):
                if opciones[k][0] < mejor[0]:
                    mejor = opciones[k]
                k += 1

            dy = mejor[1]
            dx = mejor[2]

            # guardar posición actual antes de mover
            self.historial.append((ex, ey))
            if len(self.historial) > 6:
                self.historial.pop(0)

            return self.mover(dy, dx, mapa)

        i = 0
        while i < len(movimientos):
            dy = movimientos[i][0]
            dx = movimientos[i][1]

            ny = ey + dy
            nx = ex + dx

            if 0 <= ny < mapa.filas and 0 <= nx < mapa.columnas:
                if mapa.es_camino_valido_para_enemigo(nx, ny):
                    self.historial.append((ex, ey))
                    if len(self.historial) > 6:
                        self.historial.pop(0)
                    return self.mover(dy, dx, mapa)
            i += 1

        # último recurso, movimiento aleatorio
        self.historial.append((ex, ey))
        if len(self.historial) > 6:
            self.historial.pop(0)

        return self.mover_aleatorio(mapa)

    # corregido: usar las coordenadas pasadas (jugador_x, jugador_y)
    def huir(self, jugador_x, jugador_y, mapa):
        # movimientos posibles
        movimientos = [(-1,0), (1,0), (0,-1), (0,1)]

        mejor_opcion = None
        mejor_dist = -1  # queremos maximizar la distancia al jugador

        for dy, dx in movimientos:
            ny = self.enemigo_y + dy
            nx = self.enemigo_x + dx

            # validar límites
            if not (0 <= ny < mapa.filas and 0 <= nx < mapa.columnas):
                continue

            # validar terreno
            if not mapa.es_camino_valido_para_enemigo(nx, ny):
                continue

            # calcular distancia al jugador SI se mueve a esta casilla
            dist = abs(jugador_x - nx) + abs(jugador_y - ny)

            if dist > mejor_dist:
                mejor_dist = dist
                mejor_opcion = (dy, dx)

        # si encontramos una casilla que aumenta distancia, movernos
        if mejor_opcion is not None:
            dy, dx = mejor_opcion
            return self.mover(dy, dx, mapa)

        # si no hay forma de huir, usar movimiento aleatorio
        return self.mover_aleatorio(mapa)



#___________________________________________________________________________

class Juego:
    def __init__(self, modo, nombre_jugador, dificultad):

        self.modo = modo
        self.nombre_jugador = nombre_jugador
        self.dificultad = dificultad

        #dificultad
        if dificultad == "facil":
            self.velocidad_enemigos = 900
        elif dificultad == "medio":
            self.velocidad_enemigos = 550
        else:
            self.velocidad_enemigos = 300

        self.energia = 100
        self.energia_max = 100
        self.corriendo = False
        self.juego_terminado = False

        #respawn
        self.respawn_delay = 4000

        #trampas
        self.trampas = []
        self.max_trampas = 3
        self.trampa_disponible = True

        #estadísticas
        self.inicio_tiempo = time.time()
        self.puntaje = 0
        self.trampas_colocadas = 0
        self.enemigos_eliminados = 0
        self.enemigos_escapados = 0
        self.max_enemigos = 10

        print("Modo seleccionado:", self.modo)
        print("Dificultad seleccionada:", self.dificultad)

        #Interfaz
        (self.ventana, self.canvas, self.canvas_barra, self.barra_energia) = crear_interfaz_juego(self)

        #Tamaño de celda
        self.tam = 60

        #IMÁGENES 
        self.img_muro_raw = Image.open("imagenes/muro.png").resize((self.tam, self.tam))
        self.img_muro = ImageTk.PhotoImage(self.img_muro_raw)

        self.img_liana_raw = Image.open("imagenes/liana.png").resize((self.tam, self.tam))
        self.img_liana = ImageTk.PhotoImage(self.img_liana_raw)

        self.img_tunel_raw = Image.open("imagenes/tunel.png").resize((self.tam, self.tam))
        self.img_tunel = ImageTk.PhotoImage(self.img_tunel_raw)

        self.img_camino_raw = Image.open("imagenes/camino.png").resize((self.tam, self.tam))
        self.img_camino = ImageTk.PhotoImage(self.img_camino_raw)

        #tamaño del mapa
        self.mapa = Mapa(10, 10)
        self.mapa.generar_mapa()

        #enemigos iniciales
        self.enemigos = [Enemigo(5, 5), Enemigo(8, 2)]

        #spawn del jugador
        self.jugador_x = 0
        self.jugador_y = 0

        #dibujo
        self.dibujar_mapa()
        self.dibujar_jugador()
        self.dibujar_enemigos()

        #controles
        self.ventana.bind("<Up>", self.arriba)
        self.ventana.bind("<Down>", self.abajo)
        self.ventana.bind("<Left>", self.izquierda)
        self.ventana.bind("<Right>", self.derecha)

        self.ventana.bind("<KeyPress-Shift_L>", self.iniciar_correr)
        self.ventana.bind("<KeyRelease-Shift_L>", self.detener_correr)

        self.ventana.bind("<e>", self.colocar_trampa)

        self.recuperar_energia()#energía
        
        self.actualizar_enemigos()#movimiento de enemigos

        animacion_jugador(self)
        
        self.ventana.mainloop()
#___________________________________________________________________________
        
#                                  DIBUJAR
#___________________________________________________________________________
        
    #DIBUJAR MAPA COMPLETO
    def dibujar_mapa(self):
        for f in range(self.mapa.filas):
            for c in range(self.mapa.columnas):

                celda = self.mapa.matriz[f][c]
                x1 = c * self.tam
                y1 = f * self.tam

                if celda.nombre == "muro":
                    self.canvas.create_image(x1, y1, image=self.img_muro, anchor="nw")

                elif celda.nombre == "liana":
                    self.canvas.create_image(x1, y1, image=self.img_liana, anchor="nw")

                elif celda.nombre == "tunel":
                    self.canvas.create_image(x1, y1, image=self.img_tunel, anchor="nw")
                    
                elif celda.nombre == "camino":
                    self.canvas.create_image(x1, y1, image=self.img_camino, anchor="nw")

                else:
                    self.canvas.create_rectangle(x1, y1,x1 + self.tam, y1 + self.tam,fill=celda.color,outline="gray")
        
    #DIBUJAR JUGADOR
    def dibujar_jugador(self):
        self.canvas.delete("jugador")

        x1 = self.jugador_x * self.tam + 10
        y1 = self.jugador_y * self.tam + 10
        x2 = x1 + self.tam - 20
        y2 = y1 + self.tam - 20

        self.canvas.create_oval(x1, y1, x2, y2, fill="#3498db", tags="jugador")

    #DIBUJAR ENEMIGO
    def dibujar_enemigos(self):
        if self.juego_terminado or not self.canvas.winfo_exists():
            return
        
        self.canvas.delete("enemigo")

        for ene in self.enemigos:
            x1 = ene.enemigo_x * self.tam + 10
            y1 = ene.enemigo_y * self.tam + 10
            x2 = x1 + self.tam - 20
            y2 = y1 + self.tam - 20

            self.canvas.create_oval(x1, y1, x2, y2,fill="red",tags="enemigo")
            
    #DIBUJAR TRAMPAS
    def dibujar_trampas(self):
        self.canvas.delete("trampa")
        for (tx, ty) in self.trampas:
            x1 = tx * self.tam + 20
            y1 = ty * self.tam + 20
            x2 = x1 + self.tam - 40
            y2 = y1 + self.tam - 40
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", tags="trampa")
#___________________________________________________________________________
        
#                                 MOVIMIENTO
#___________________________________________________________________________

        #Validacion del movimiento segun el terreno
    def puede_moverse(self, x, y):
        casilla = self.mapa.obtener_casilla(x, y)
        if casilla is None:
            return False
        else:
            return not casilla.bloquea_jugador

    
    def arriba(self, event):
        if self.puede_moverse(self.jugador_x, self.jugador_y - 1):
            s_pasos()
            if self.corriendo and self.energia > 0:
                self.jugador_y -= 2
                self.energia -= 5
            else:
                self.jugador_y -= 1
            self.dibujar_jugador()
            self.verificar_salida()
            self.actualizar_barra_energia()

    def abajo(self, event):
        if self.puede_moverse(self.jugador_x, self.jugador_y + 1):
            s_pasos()
            if self.corriendo and self.energia > 0:
                self.jugador_y += 2
                self.energia -= 5
            else:
                self.jugador_y += 1
            self.dibujar_jugador()
            self.verificar_salida()
            self.actualizar_barra_energia()

    def izquierda(self, event):
        if self.puede_moverse(self.jugador_x - 1, self.jugador_y):
            s_pasos()
            if self.corriendo and self.energia > 0:
                self.jugador_x -= 2
                self.energia -= 5
            else:
                self.jugador_x -= 1
            self.dibujar_jugador()
            self.verificar_salida()
            self.actualizar_barra_energia()

    def derecha(self, event):
        if self.puede_moverse(self.jugador_x + 1, self.jugador_y):
            s_pasos()
            if self.corriendo and self.energia > 0:
                self.jugador_x += 2
                self.energia -= 5
            else:
                self.jugador_x += 1
            self.dibujar_jugador()
            self.verificar_salida()
            self.actualizar_barra_energia()

#___________________________________________________________________________

    def colocar_trampa(self, event=None):
        if self.modo.lower() != "escapa":
            return

        #maximo de trampas activas
        if len(self.trampas) >= self.max_trampas:
            messagebox.showwarning("Límite", "Solo puedes tener 3 trampas activas.")
            return

        #cooldown
        if not self.trampa_disponible:
            messagebox.showwarning("Cooldown", "Debes esperar 5 segundos para colocar otra trampa.")
            return

        posicion = (self.jugador_x, self.jugador_y)

        #evitar poner 2 trampas en una misma casilla
        if posicion in self.trampas:
            return

        s_trampa_colocada()

        self.trampas.append(posicion)
        self.dibujar_trampas()

        animacion_trampa(self, self.jugador_x, self.jugador_y)


        self.trampa_disponible = False
        self.ventana.after(5000, self.reiniciar_trampa)
        self.trampas_colocadas += 1


    def reiniciar_trampa(self):
        self.trampa_disponible = True
#___________________________________________________________________________
        
    def actualizar_barra_energia(self):
        if self.juego_terminado:
            return
        
        porcentaje = self.energia / self.energia_max
        ancho = 200 * porcentaje  #barra completa es 200pix

        self.canvas_barra.coords(self.barra_energia, 0, 0, ancho, 20)

        if porcentaje > 0.6:
            color = "green"
        elif porcentaje > 0.3:
            color = "yellow"
        else:
            color = "red"

        self.canvas_barra.itemconfig(self.barra_energia, fill=color)


    def iniciar_correr(self, event):
        self.corriendo = True

    def detener_correr(self, event):
        self.corriendo = False

    def recuperar_energia(self):
        if self.juego_terminado:
            return
    
        if not self.corriendo and self.energia < self.energia_max:
            self.energia += 1

        self.actualizar_barra_energia()
        self.ventana.after(500, self.recuperar_energia)

#___________________________________________________________________________



    def eliminar_enemigo(self, enemigo):
        if enemigo in self.enemigos:
            self.enemigos.remove(enemigo)
        self.dibujar_enemigos()

    def reaparecer_enemigo(self):
        # buscar una celda válida aleatoria
        intentos = 0
        while True:
            x = random.randint(0, self.mapa.columnas - 1)
            y = random.randint(0, self.mapa.filas - 1)
            intentos += 1

            if self.mapa.es_camino_valido_para_enemigo(x, y):
                break

            if intentos > 200:
                # fallback
                x, y = 0, 0
                break

        nuevo = Enemigo(y, x)
        self.enemigos.append(nuevo)
        self.dibujar_enemigos()
    
    def actualizar_enemigos(self):
        if self.juego_terminado or not self.canvas.winfo_exists():
            return

        for ene in self.enemigos[:]:

            # --------------------------------------------------------
            # MOVIMIENTO SEGÚN MODO
            # --------------------------------------------------------
            if self.modo.lower() == "escapa":
                ene.perseguir(self.jugador_x, self.jugador_y, self.mapa)
            elif self.modo.lower() == "cazador":
                ene.huir(self.jugador_x, self.jugador_y, self.mapa)
            else:
                ene.mover_aleatorio(self.mapa)

            # --------------------------------------------------------
            # 1. TRAMPAS (solo escapa)
            # --------------------------------------------------------
            if (ene.enemigo_x, ene.enemigo_y) in self.trampas:

                animacion_desevanecer(self, ene)
                self.trampas.remove((ene.enemigo_x, ene.enemigo_y))
                self.dibujar_trampas()

                if self.modo.lower() == "escapa":
                    self.puntaje += 50

                self.ventana.after(450, self.eliminar_enemigo, ene)

                if self.modo.lower() == "escapa":
                    self.ventana.after(10000, self.reaparecer_enemigo)
                else:
                    self.ventana.after(3000, self.respawn_cazador)

                continue

            # --------------------------------------------------------
            # 2. COLISIÓN "realista" con radio
            # --------------------------------------------------------
            dx = ene.enemigo_x - self.jugador_x
            dy = ene.enemigo_y - self.jugador_y

            distancia = (dx*dx + dy*dy) ** 0.5
            rango = 1.3   # ⬅ Ajusta esto. 1.2–1.4 suele sentirse muy natural

            if distancia <= rango:

                # MODO ESCAPA — pierdes
                if self.modo.lower() == "escapa":
                    self.juego_terminado = True
                    messagebox.showinfo("Perdiste", "El enemigo te atrapó.")
                    try: self.ventana.destroy()
                    except: pass
                    return

                # MODO CAZADOR — matas
                else:
                    animacion_desevanecer(self, ene)
                    self.ventana.after(450, self.eliminar_enemigo, ene)
                    self.enemigos_eliminados += 1
                    self.puntaje += 10
                    s_atrapar()
                    self.ventana.after(3000, self.respawn_cazador)
                    self.verificar_fin_cazador()
                    continue

            # --------------------------------------------------------
            # 3. ENEMIGO LLEGA A LA SALIDA (solo cazador)
            # --------------------------------------------------------
            celda_actual = self.mapa.obtener_casilla(ene.enemigo_x, ene.enemigo_y)

            if isinstance(celda_actual, Salida) and self.modo.lower() == "cazador":
                self.enemigos_escapados += 1
                self.puntaje -= 20

                messagebox.showwarning(
                    "Un enemigo escapó",
                    f"Un enemigo logró llegar a la salida.\nEscapados: {self.enemigos_escapados}"
                )

                if ene in self.enemigos: self.enemigos.remove(ene)
                self.ventana.after(3000, self.respawn_cazador)
                self.verificar_fin_cazador()
                continue

        self.dibujar_enemigos()
        if not self.juego_terminado:
            self.canvas.after(self.velocidad_enemigos, self.actualizar_enemigos)

#___________________________________________________________________________
    def respawn_cazador(self):
        # No crear más si ya procesamos los max_enemigos
        if (self.enemigos_eliminados + self.enemigos_escapados) >= self.max_enemigos:
            return
        # No crear si ya hay 2 enemigos en pantalla
        if len(self.enemigos) >= 2:
            return

        intentos = 0
        while True:
            x = random.randint(0, self.mapa.columnas - 1)
            y = 0  # spawn en primera fila
            intentos += 1

            # Validar tipo de celda
            if not self.mapa.es_camino_valido_para_enemigo(x, y):
                if intentos > 200:
                    return
                continue

            # No aparecer sobre el jugador
            if (x, y) == (self.jugador_x, self.jugador_y):
                if intentos > 200:
                    return
                continue

            # Verificar que no haya otro enemigo en esa posición
            posicion_ocupada = False
            for ene in self.enemigos:
                if (ene.enemigo_x, ene.enemigo_y) == (x, y):
                    posicion_ocupada = True
                    break

            if posicion_ocupada:
                if intentos > 200:
                    return
                continue

            # Si llegó aquí: posición válida
            self.enemigos.append(Enemigo(y, x))
            self.dibujar_enemigos()
            return

            # Seguridad final
            if intentos > 200:
                return
#___________________________________________________________________________

    def verificar_salida(self):
        celda = self.mapa.obtener_casilla(self.jugador_x, self.jugador_y)

        if self.modo.lower() == "cazador":
            return
        
        elif isinstance(celda, Salida):
            self.juego_terminado = True


            tiempo_total = time.time() - self.inicio_tiempo
            puntaje_tiempo = max(0, int(500 - tiempo_total * 10))
            self.puntaje += puntaje_tiempo

            s_win() #sonido al finalizar

            messagebox.showinfo("¡Ganaste!",f"Llegaste a la salida.\n\nPuntaje final: {self.puntaje}")

            #cerrar ventana de juego
            self.ventana.destroy()

            #btener estadísticas
            stats = self.obtener_estadisticas_finales()

            #abrir GUI final
            agregar_puntaje("escapa", self.nombre_jugador, self.puntaje)
            mostrar_pantalla_final(stats)

    def verificar_fin_cazador(self):
        procesados = self.enemigos_eliminados + self.enemigos_escapados

        # Si ya se llegó al límite de enemigos procesados (10)
        if procesados >= self.max_enemigos:
            self.juego_terminado = True

            s_win()

            mensaje = (f"Juego terminado.\n\n Enemigos cazados: {self.enemigos_eliminados}\n Enemigos escapados: {self.enemigos_escapados}\n Total: {procesados}/{self.max_enemigos}")
            messagebox.showinfo("Fin del modo Cazador", mensaje)

            try:
                self.ventana.destroy()
            except:
                pass

            stats = self.obtener_estadisticas_finales()
            mostrar_pantalla_final(stats)
            return

        faltantes = 2 - len(self.enemigos)
        faltantes = min(faltantes, self.max_enemigos - procesados)

        for i in range(faltantes):
            delay = self.respawn_delay * (i + 1)
            self.ventana.after(delay, self.respawn_cazador)

#___________________________________________________________________________

    def obtener_estadisticas_finales(self):
        tiempo_total = round(time.time() - self.inicio_tiempo, 2)

        #MODO ESCAPA
        if self.modo.lower() == "escapa":
            estadisticas = {"Modo": self.modo, "Puntaje": self.puntaje, "Tiempo": tiempo_total, "Trampas colocadas": self.trampas_colocadas, "Enemigos eliminados": self.enemigos_eliminados}

        #MODO CAZADOR
        else:
            penalizacion_tiempo = int(tiempo_total * 5)

            puntaje_final = self.puntaje - penalizacion_tiempo
            if puntaje_final < 0:
                puntaje_final = 0

            estadisticas = {"Modo": self.modo, "Puntaje": puntaje_final, "Tiempo": tiempo_total, "Enemigos cazados": self.enemigos_eliminados, "Enemigos escapados": self.enemigos_escapados, "Total procesados": self.enemigos_eliminados + self.enemigos_escapados, "Objetivo": self.max_enemigos}

        return estadisticas
    
    
    
