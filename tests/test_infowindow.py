import pygame
import pytest
from src.ui.info_window import InfoWindow
from src.config import settings

@pytest.fixture
def setup_pygame():
    pygame.init()
    pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    yield
    pygame.quit()

def test_infowindow_back_button(setup_pygame):
    # Crear fondo simple (gris claro)
    background = pygame.Surface((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    background.fill((200, 200, 200))

    # Fuente
    font = pygame.font.SysFont("Arial", 28)

    # Crear InfoWindow real
    window = InfoWindow(pygame.display.get_surface(), background, font)

    # Simular un clic sobre el botón Back
    click_event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        {
            "pos": window.back_button.rect.center,
            "button": 1
        }
    )
    pygame.event.post(click_event)

    # Ejecutar una sola iteración
    result = window.run()

    # Validar que devolvió BACK
    assert result == "BACK"
