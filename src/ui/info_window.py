import pygame
from src.config import settings
from src.utils.buttons import Button

class InfoWindow:
    def __init__(self, screen, background_surface, font):
        self.screen = screen
        self.background = background_surface
        self.font = font
        self.running = True

        # Detectar tema
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

        # Creamos el boton back
        self.back_button = Button(
            pos=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT - 60),
            size=(300, 80),
            text="Back",
            hover_color=self.button_hover,
            bg_color=self.button_bg,
            text_color=self.text_color,
            font=self.font
        )

    def draw_text(self, text, x, y):
        surface = self.font.render(text, True, self.text_color)
        self.screen.blit(surface, (x, y))

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        # panel centrado
        panel_width = 1200
        panel_height = 520
        panel_x = (settings.WINDOW_WIDTH - panel_width) // 2
        panel_y = 20

        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill((*self.panel_color, 250))
        self.screen.blit(panel_surface, (panel_x, panel_y))

        # texto
        x = panel_x + 20
        y = panel_y + 20
        line_space = 30

        self.draw_text("Avatars VS Rooks is an educational video game designed to reinforce", x, y)
        self.draw_text("programming concepts such as recursion, data structures", x, y + line_space)
        self.draw_text("and iteration and disk storage.", x, y + line_space * 2)

        y = y + line_space * 4
        self.draw_text("Goal:", x, y)
        self.draw_text("Place your Rooks, eliminate all the Avatars, and don't let them reach", x, y + line_space)
        self.draw_text("the other side of the map.", x, y + line_space * 2)

        y = y + line_space * 4
        self.draw_text("Rooks", x, y)
        self.draw_text("Arrowed: 2 attack points", x, y + line_space)
        self.draw_text("Squire: 3 attack points", x, y + line_space * 2)
        self.draw_text("Woodcutter: 9 attack points", x, y + line_space * 3)
        self.draw_text("Cannibal: 12 attack points", x, y + line_space * 4)

        y = y + line_space * 6
        self.draw_text("How to play:", x, y)
        self.draw_text("Earn coins, select your Rooks and place them to destroy the Avatars", x, y + line_space)

        
        back_width, back_height = 300, 80
        back_center_x = settings.WINDOW_WIDTH // 2
        back_center_y = panel_y + panel_height + 15 + back_height // 2

        self.back_button.pos = (back_center_x, back_center_y)
        
        self.back_button.rect.center = self.back_button.pos

        # dibujar boton back
        self.back_button.draw(self.screen)

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "QUIT"
            if self.back_button.event_mouse(event):
                return "BACK"

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            action = self.handle_events()
            if action in ["BACK", "QUIT"]:
                return action
            self.draw()
            clock.tick(settings.FPS)
        return None