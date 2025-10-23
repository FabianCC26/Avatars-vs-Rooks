import pygame
from src.config import settings
from src.ui.login_screen import LoginScreen
from src.ui.register_screen import RegisterScreen

def main():
    """Punto de entrada principal del juego."""
    pygame.init()
    screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    pygame.display.set_caption(settings.WINDOW_TITLE)

    running = True
    current_screen = "LOGIN"

    while running:
        if current_screen == "LOGIN":
            login_screen = LoginScreen(screen)
            action = login_screen.run()

            if action == "REGISTER":
                current_screen = "REGISTER"
            elif action == "QUIT":
                running = False

        elif current_screen == "REGISTER":
            register_screen = RegisterScreen(screen)
            action = register_screen.run()

            if action == "BACK":
                current_screen = "LOGIN"
            elif action == "QUIT":
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()