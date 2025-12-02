import pygame
import pytest
from src.ui.leaderbords_screen import LeaderboardWindow
from src.config import settings

@pytest.mark.visual
def test_leaderboard_window_runs():
    pygame.init()

    screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    font = pygame.font.SysFont("Arial", 32)

    # Fondo de ejemplo
    background = pygame.Surface((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    background.fill((230, 230, 230))

    # Datos del ranking
    usuarios = [
        {"name": "Daniel", "score": 120},
        {"name": "María", "score": 90},
        {"name": "Juan", "score": 60},
        {"name": "Jose", "score": 10},
        {"name": "Mar", "score": 20},
        {"name": "Jhon", "score": 600},
        {"name": "Rey", "score": 100},
        {"name": "Lola", "score": 97},
        {"name": "Emma", "score": 60},
        
    ]

    window = LeaderboardWindow(screen, background, font, usuarios)

    running = True
    while running:
        for event in pygame.event.get():
            # Mantiene la ventana abierta hasta presionar una tecla o cerrar la ventana
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                running = False

        window.draw()

    pygame.quit()
    assert True
