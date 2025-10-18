import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
from src.utils.dropdown import Dropdown

pygame.init()
screen = pygame.display.set_mode((500, 400))
pygame.display.set_caption("Test Dropdown")

font = pygame.font.Font(None, 32)

dropdown = Dropdown(
    x=150, y=150, width=200, height=40,
    font=font,
    main_color=(200, 200, 200),
    hover_color=(170, 170, 170),
    text_color=(0, 0, 0),
    options=["Jugador", "Administrador"]
)

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        dropdown.handle_event(event)

    screen.fill((30, 30, 30))
    dropdown.draw(screen)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
