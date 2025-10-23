import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
from src.utils.input_box import InputBox

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Test InputBox")
font = pygame.font.Font(None, 32)

input_box1 = InputBox(100, 100, 200, 40, font, placeholder="Usuario")
input_box2 = InputBox(100, 160, 200, 40, font, placeholder="Contraseña", is_password=True)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        input_box1.handle_event(event)
        input_box2.handle_event(event)

    screen.fill((240, 240, 240))
    input_box1.draw(screen)
    input_box2.draw(screen)
    pygame.display.flip()
