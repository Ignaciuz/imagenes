import tkinter as tk
from juego import Juego

#____________________________________________________________
#                           GLOBALES
#____________________________________________________________

modo_seleccionado = None
ventana_nombre = None
ventana_menu = None
entry_nombre = None
dificultad_var = None

#____________________________________________________________
#                REGISTRO DE NOMBRE + DIFICULTAD
#____________________________________________________________

def abrir_registro_nombre(modo):
    global modo_seleccionado, ventana_nombre, entry_nombre, dificultad_var

    modo_seleccionado = modo  # almacena modo elegido ("escapa" o "cazador")

    ventana_nombre = tk.Toplevel()
    ventana_nombre.title("Nombre y dificultad")
    ventana_nombre.geometry("350x300")

    tk.Label(ventana_nombre,text="Ingrese su nombre:",font=("Arial", 12)).pack(pady=5)

    entry_nombre = tk.Entry(ventana_nombre, font=("Arial", 12))
    entry_nombre.pack()

    # ---------- Selección de dificultad ----------
    tk.Label(ventana_nombre, text="Seleccione dificultad:", font=("Arial", 12)).pack(pady=10)

    dificultad_var = tk.StringVar(value="medio")  #valor por defecto

    tk.Radiobutton(ventana_nombre, text="Fácil",   variable=dificultad_var, value="facil", font=("Arial", 11)).pack(anchor="w", padx=30)
    tk.Radiobutton(ventana_nombre, text="Medio",   variable=dificultad_var, value="medio", font=("Arial", 11)).pack(anchor="w", padx=30)
    tk.Radiobutton(ventana_nombre, text="Difícil", variable=dificultad_var, value="dificil", font=("Arial", 11)).pack(anchor="w", padx=30)

    #Botón continuar
    btn_continuar = tk.Button(ventana_nombre, text="Continuar", font=("Arial", 12), command=confirmar_nombre)
    btn_continuar.pack(pady=15)


def confirmar_nombre():
    global entry_nombre, ventana_nombre, modo_seleccionado, ventana_menu, dificultad_var

    nombre = entry_nombre.get().strip()
    if nombre == "":
        return  #no continuar si el nombre está vacío

    dificultad = dificultad_var.get()  #"facil" / "medio" / "dificil"

    ventana_nombre.destroy()   #cerrar ventana de nombre
    ventana_menu.destroy()     #cerrar menú principal

    #crear instancia del juego con modo + nombre + dificultad
    Juego(modo_seleccionado, nombre, dificultad)



#____________________________________________________________
#                 BOTONES DEL MENÚ PRINCIPAL
#____________________________________________________________

def iniciar_escapa():
    abrir_registro_nombre("escapa")

def iniciar_cazador():
    abrir_registro_nombre("cazador")

def salir():
    ventana_menu.destroy()


#____________________________________________________________
#                    MENÚ PRINCIPAL
#____________________________________________________________

ventana_menu = tk.Tk()
ventana_menu.title("Seleccionar modo de juego")
ventana_menu.geometry("500x400")
ventana_menu.configure(bg="#f0f4f8")

titulo = tk.Label(ventana_menu, text="Seleccione un modo de juego", font=("Helvetica", 20, "bold"), bg="#f0f4f8", fg="#2c3e50")
titulo.pack(pady=40)

btn1 = tk.Button(ventana_menu, text="Modo Escapa", font=("Helvetica", 16), bg="#5dade2", fg="white", width=20, height=2, command=iniciar_escapa)
btn1.pack(pady=20)

btn2 = tk.Button(ventana_menu, text="Modo Cazador", font=("Helvetica", 16), bg="#5dade2", fg="white", width=20, height=2, command=iniciar_cazador)
btn2.pack(pady=20)

btn3 = tk.Button(ventana_menu,text="Salir", font=("Helvetica", 16), bg="#c0392b", fg="white", width=20, height=2, command=salir)
btn3.pack(pady=20)

#main
ventana_menu.mainloop()
