import pygame
from src.config import settings
from src.ui.login_screen import LoginScreen

def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    pygame.display.set_caption("Test Login Screen")

    login = LoginScreen(screen)
    action = login.run()

    print(f"Pantalla cerrada con acción: {action}")
    pygame.quit()

if __name__ == "__main__":
    main()
