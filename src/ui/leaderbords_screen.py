import pygame
from src.config import settings
from src.utils.buttons import Button


class LeaderboardWindow:
    def __init__(self, screen, background_surface, font, usuarios):
        self.screen = screen
        self.background = background_surface
        self.font = font
        self.running = True

        # Ordenar usuarios por puntaje
        self.usuarios = sorted(usuarios, key=lambda u: u["score"], reverse=True)

        # Detectar si es tema claro u oscuro
        first_pixel = self.background.get_at((0, 0))
        is_light = first_pixel.r > 150 and first_pixel.g > 150 and first_pixel.b > 150

        if is_light:
            self.button_bg = (217, 217, 217)
            self.button_hover = (180, 180, 180)
            self.text_color = (0, 0, 0)
            self.panel_color = (240, 240, 240)
        else:
            self.button_bg = (115, 115, 115)
            self.button_hover = (180, 180, 180)
            self.text_color = (0, 0, 0)
            self.panel_color = (200, 200, 200)

        # Botón Back
        self.back_button = Button(
            pos=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT - 60),
            size=(300, 80),
            text="Back",
            hover_color=self.button_hover,
            bg_color=self.button_bg,
            text_color=self.text_color,
            font=self.font
        )

    # ---------------------------------------------
    # Dibujar ventana
    # ---------------------------------------------
    def draw(self):
        self.screen.blit(self.background, (0, 0))

        # Panel central
        panel_width = 1200
        panel_height = 520
        panel_x = (settings.WINDOW_WIDTH - panel_width) // 2
        panel_y = 20

        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill((*self.panel_color, 230))
        self.screen.blit(panel_surface, (panel_x, panel_y))

        # Título centrado
        title = "Leaderboard"
        title_surface = self.font.render(title, True, self.text_color)
        title_rect = title_surface.get_rect(center=(settings.WINDOW_WIDTH // 2, panel_y + 20))
        self.screen.blit(title_surface, title_rect)

        # --- COLUMNAS FIJAS PARA 10 USUARIOS ---
        y_start = panel_y + 130
        line_spacing = 45

        # Tres columnas
        pos_x = panel_x + panel_width // 2 - 300
        name_x = panel_x + panel_width // 2
        score_x = panel_x + panel_width // 2 + 300

        max_slots = 10  # SIEMPRE 10 FILAS

        for index in range(1, max_slots + 1):
            y = y_start + (index - 1) * line_spacing - 50

            if index <= len(self.usuarios):
                user = self.usuarios[index - 1]
                pos_text = f"{index}"
                name_text = user["name"]
                score_text = str(user["score"])
            else:
                pos_text = f"{index}"
                name_text = "----------------"
                score_text = "---"

            # Render posición
            pos_surface = self.font.render(pos_text, True, self.text_color)
            pos_rect = pos_surface.get_rect(center=(pos_x, y))
            self.screen.blit(pos_surface, pos_rect)

            # Render nombre
            name_surface = self.font.render(name_text, True, self.text_color)
            name_rect = name_surface.get_rect(center=(name_x, y))
            self.screen.blit(name_surface, name_rect)

            # Render puntaje
            score_surface = self.font.render(score_text, True, self.text_color)
            score_rect = score_surface.get_rect(center=(score_x, y))
            self.screen.blit(score_surface, score_rect)

        # Botón Back
        back_width, back_height = 300, 80
        back_center_x = settings.WINDOW_WIDTH // 2 + 450
        back_center_y = panel_y + panel_height + 55 + back_height // 2

        self.back_button.pos = (back_center_x, back_center_y)
        self.back_button.rect.center = self.back_button.pos
        self.back_button.draw(self.screen)

        pygame.display.flip()

    # ---------------------------------------------
    # Eventos
    # ---------------------------------------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "QUIT"

            if self.back_button.event_mouse(event):
                return "BACK"

    # ---------------------------------------------
    # Loop principal
    # ---------------------------------------------
    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            action = self.handle_events()
            if action in ["BACK", "QUIT"]:
                return action

            self.draw()
            clock.tick(settings.FPS)

        return None
