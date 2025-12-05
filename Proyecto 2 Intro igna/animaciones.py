def animacion_jugador(juego, frame_actual=0):

    # Detener animación si termina el juego
    if juego.juego_terminado:
        return

    juego.canvas.delete("jugador_idle")

    # Cálculo del tamaño del pulso
    pulso_base = juego.tam - 20
    fase = frame_actual % 4

    if fase == 0:
        cambio_tamaño = 0
    elif fase == 1:
        cambio_tamaño = 2
    elif fase == 2:
        change_size = 4
        cambio_tamaño = 4
    else:
        cambio_tamaño = 2

    # Calcular el óvalo del efecto
    x_min = juego.jugador_x * juego.tam + 10 - cambio_tamaño
    y_min = juego.jugador_y * juego.tam + 10 - cambio_tamaño
    x_max = x_min + pulso_base + cambio_tamaño * 2
    y_max = y_min + pulso_base + cambio_tamaño * 2

    juego.canvas.create_oval(x_min, y_min, x_max, y_max, outline="#85C1E9", width=2, tags="jugador_idle")

    # Llamar siguiente frame
    def siguiente_frame():
        animacion_jugador(juego, frame_actual + 1)

    juego.ventana.after(150, siguiente_frame)



# ---------------------------------------------------------------
#   ANIMACIÓN 2 — COLOCAR TRAMPA
# ---------------------------------------------------------------
def animacion_trampa(juego, trampa_x, trampa_y, frame_actual=0):
    """
    Animación rápida de expansión visual cuando se coloca una trampa.
    """

    if frame_actual > 6:
        juego.canvas.delete("trampa_anim")
        return

    juego.canvas.delete("trampa_anim")

    tamaño_base = juego.tam // 3
    tamaño_actual = tamaño_base + frame_actual * 3

    # Calcular posición centrada
    x_min = trampa_x * juego.tam + (juego.tam // 2 - tamaño_actual // 2)
    y_min = trampa_y * juego.tam + (juego.tam // 2 - tamaño_actual // 2)
    x_max = x_min + tamaño_actual
    y_max = y_min + tamaño_actual

    juego.canvas.create_oval(x_min, y_min, x_max, y_max, outline="black", width=3, tags="trampa_anim")

    # Siguiente frame
    def siguiente_frame():
        animacion_trampa(juego, trampa_x, trampa_y, frame_actual + 1)

    juego.ventana.after(60, siguiente_frame)



# ---------------------------------------------------------------
#   ANIMACIÓN 3 — DESVANECER ENEMIGO AL MORIR
# ---------------------------------------------------------------
def animacion_desevanecer(juego, enemigo, frame_actual=0):

    if frame_actual > 6:
        # Limpiar sprite final
        juego.canvas.delete(f"enemigo_fade_{id(enemigo)}")
        return

    juego.canvas.delete(f"enemigo_fade_{id(enemigo)}")

    # Cálculo del nivel de opacidad (simulación con valores de rojo)
    opacidad_color = 255 - frame_actual * 40
    color_hex = f"#{opacidad_color:02x}0000"

    # Posición del enemigo
    x_min = enemigo.enemigo_x * juego.tam + 10
    y_min = enemigo.enemigo_y * juego.tam + 10
    x_max = x_min + juego.tam - 20
    y_max = y_min + juego.tam - 20

    juego.canvas.create_oval(x_min, y_min, x_max, y_max, fill=color_hex, outline="", tags=f"enemigo_fade_{id(enemigo)}")

    # Siguiente frame
    def siguiente_frame():
        animacion_desevanecer(juego, enemigo, frame_actual + 1)

    juego.ventana.after(70, siguiente_frame)
