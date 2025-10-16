import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
from src.utils.buttons import Button

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Test Button con Texto")

# Crear botones de ejemplo
register_button = Button(pos=(400, 250), size=(220, 80), text="Registrar", bg_color=(0, 128, 255))
login_button = Button(pos=(400, 400), size=(220, 80), text="Iniciar Sesión", bg_color=(0, 200, 100))

running = True
while running:
    screen.fill((30, 30, 30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if register_button.event_mouse(event):
            print("Botón 'Registrar' presionado")

        if login_button.event_mouse(event):
            print("Botón 'Iniciar Sesión' presionado")

    register_button.draw(screen)
    login_button.draw(screen)
    pygame.display.flip()

pygame.quit()
