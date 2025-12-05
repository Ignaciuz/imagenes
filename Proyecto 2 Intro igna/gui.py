import tkinter as tk
from tkinter import messagebox
from puntajes import obtener_top5

#____________________________________________________________________

#              PANTALLA FINAL (SIN PEDIR NOMBRE)
#____________________________________________________________________

def mostrar_pantalla_final(stats):

    ventana_final = tk.Tk()
    ventana_final.title("Resumen de la Partida")
    ventana_final.geometry("420x450")
    ventana_final.resizable(False, False)

    frame = tk.Frame(ventana_final, bg="#f0f0f0")
    frame.pack(fill="both", expand=True)

    lbl_titulo = tk.Label(frame,
                          text="RESUMEN DE LA PARTIDA",
                          font=("Arial", 18, "bold"),
                          bg="#f0f0f0")
    lbl_titulo.pack(pady=15)

    modo = stats.get("Modo", "").lower()

    #_________________ ESTADÍSTICAS INDIVIDUALES _________________

    if modo == "escapa":
        lista_mostrar = [
            ("Puntaje", stats.get("Puntaje", 0)),
            ("Tiempo", stats.get("Tiempo", "0")),
            ("Enemigos eliminados", stats.get("Enemigos eliminados", 0)),
            ("Trampas colocadas", stats.get("Trampas colocadas", 0))]

    elif modo == "cazador":
        lista_mostrar = [
            ("Puntaje", stats.get("Puntaje", 0)),
            ("Tiempo", stats.get("Tiempo", "0")),
            ("Enemigos cazados", stats.get("Enemigos cazados", 0)),
            ("Enemigos escapados", stats.get("Enemigos escapados", 0))]

    else:
        lista_mostrar = []

    for texto, valor in lista_mostrar:
        tk.Label(frame,text=f"{texto}: {valor}",font=("Arial", 14),bg="#f0f0f0").pack(pady=5)

    # _________________ TOP 5 _________________

    lbl_top = tk.Label(frame,text="TOP 5 — " + stats["Modo"].upper(),font=("Arial", 16, "bold"),bg="#f0f0f0")
    lbl_top.pack(pady=10)

    top = obtener_top5(stats["Modo"])

    for entrada in top:
        nombre = entrada[0]
        puntaje = entrada[1]

        tk.Label(frame,
                 text=f"{nombre}: {puntaje}",
                 font=("Arial", 14),bg="#f0f0f0").pack()


    # _________________ BOTÓN VOLVER AL MENÚ _________________

    def volver_menu():
        ventana_final.destroy()
        import main  #para volver al menu principal

    btn_volver = tk.Button(frame,text="Volver al menú",font=("Arial", 14),command=volver_menu)
    btn_volver.pack(pady=15)

#____________________________________________________________________

def mostrar_pantalla_derrota(modo):

    ventana = tk.Tk()
    ventana.title("Fin del juego")
    ventana.geometry("350x250")
    ventana.resizable(False, False)

    frame = tk.Frame(ventana, bg="#f0f0f0")
    frame.pack(fill="both", expand=True)

    tk.Label(frame,
             text=f"Perdiste en modo {modo.upper()}",
             font=("Arial", 16, "bold"),
             bg="#f0f0f0").pack(pady=20)

    tk.Label(frame,
             text="Mejor suerte la próxima...",
             font=("Arial", 14),
             bg="#f0f0f0").pack(pady=10)

    def volver_menu():
        ventana.destroy()
        import main

    tk.Button(frame,
              text="Volver al menú",
              font=("Arial", 14),
              command=volver_menu).pack(pady=20)

#____________________________________________________________________

#                  INTERFAZ GRÁFICA DEL JUEGO
#____________________________________________________________________


def crear_interfaz_juego(juego):

    ventana = tk.Tk()

    #forzar foco en la ventana del juego
    ventana.focus_force()
    ventana.attributes('-topmost', True)

    ventana.title("Escapa del Laberinto")
    ventana.geometry("700x700")
    ventana.configure(bg="#f0f4f8")

    #HUD (barra superior)
    frame_hud = tk.Frame(ventana, bg="#f0f4f8")
    frame_hud.pack(pady=10)

    label_energia = tk.Label(frame_hud,text="Energía:",font=("Helvetica", 12),bg="#f0f4f8")
    label_energia.pack(side="left", padx=5)

    #barra de energía
    canvas_barra = tk.Canvas(frame_hud,width=200,height=20,bg="lightgray",highlightthickness=0)
    canvas_barra.pack(side="left")

    barra_energia = canvas_barra.create_rectangle(0, 0, 200, 20, fill="green")

    #canvas principal donde se dibuja el mapa
    canvas = tk.Canvas(ventana,width=600,height=600,bg="white")
    canvas.pack()

    return ventana, canvas, canvas_barra, barra_energia
