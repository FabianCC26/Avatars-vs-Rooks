import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
from src.config import settings
from src.utils.buttons import Button
from src.ui.register_screen import RegisterScreen


def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    pygame.display.set_caption("Test Registration Screen")

    font = pygame.font.SysFont("arial", 32)
    register_button = Button(
        pos=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2),
        size=(300, 100),
        text="Registrarse",
        bg_color=settings.COLOR_PRIMARY
    )

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(settings.COLOR_BACKGROUND)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # abrir la pantalla de registro si se hace click en el boton de registarse
            if register_button.event_mouse(event):
                register_screen = RegisterScreen(screen)
                result = register_screen.run()
                if result == "QUIT":
                    running = False

        # dibujar el boton
        register_button.draw(screen)

        # dibujar el titulo
        title = font.render("Pantalla de prueba principal", True, settings.COLOR_TEXT)
        screen.blit(title, (settings.WINDOW_WIDTH // 2 - 220, 200))

        pygame.display.flip()
        clock.tick(settings.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
