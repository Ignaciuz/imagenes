import pygame

pygame.mixer.init()

#sonidos modo escapa
sonido_win = pygame.mixer.Sound("sonidos/win.ogg")
sonido_eliminar_trampa = pygame.mixer.Sound("sonidos/eliminar.wav")
sonido_trampa_colocada = pygame.mixer.Sound("sonidos/trampa.wav")
sonido_atrapado = pygame.mixer.Sound("sonidos/atrapado.wav")

#sonidos modo cazador
sonido_atrapar = pygame.mixer.Sound("sonidos/atrapar.wav")
sonido_escapado = pygame.mixer.Sound("sonidos/escapado.wav")

# Movimiento
sonido_pasos = pygame.mixer.Sound("sonidos/pasos.mp3")

#Volumen
sonido_pasos.set_volume(0.3)  #volumen bajo para pasos


def s_win():
    sonido_win.play()

def s_eliminar_trampa():
    sonido_eliminar_trampa.play()

def s_trampa_colocada():
    sonido_trampa_colocada.play()

def s_atrapado():
    sonido_atrapado.play()

def s_atrapar():
    sonido_atrapar.play()

def s_escapado():
    sonido_escapado.play()

def s_pasos():
    sonido_pasos.play()
