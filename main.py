"""

Punto de entrada principal del juego.

"""

import pygame
from src.config import settings
#from src.ui.main_window import MainWindow

def main():
    """Función principal del juego."""
    pygame.init()
    
    # Configuración de ventana
    screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    pygame.display.set_caption(settings.WINDOW_TITLE)
    
    # Control de FPS
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(settings.COLOR_BACKGROUND)
        pygame.display.flip()
        clock.tick(settings.FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
