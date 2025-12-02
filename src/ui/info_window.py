import os
import pygame
from src.config import settings
from src.utils.buttons import Button


class InfoWindow:
    def __init__(
        self,
        screen,
        background_surface,
        font,

        # posiciones (x,y)
        h2p_pos=(settings.WINDOW_WIDTH // 2, (settings.WINDOW_HEIGHT // 2)+170),
        avatars_pos=(975, 170),
        rook_pos=(325, 170),

        # tamaños (w,h)
        h2p_size=(720, 360),
        avatars_size=(650, 325),
        rook_size=(650, 325)
    ):
        self.screen = screen
        self.background = background_surface
        self.font = font
        self.running = True

        # Rutas absolutas
        base_path = os.path.dirname(os.path.dirname(__file__))  # /src
        img_dir = os.path.join(base_path, "assets", "images")

        # Cargar imágenes con safe_load
        self.img_h2p = self.safe_load(os.path.join(img_dir, "instrucciones.png"))
        self.img_avatars = self.safe_load(os.path.join(img_dir, "inst_avatars.png"))
        self.img_rook = self.safe_load(os.path.join(img_dir, "inst_rook.png"))

        # Escalar imágenes si corresponde
        if h2p_size:
            self.img_h2p = pygame.transform.scale(self.img_h2p, h2p_size)

        if avatars_size:
            self.img_avatars = pygame.transform.scale(self.img_avatars, avatars_size)

        if rook_size:
            self.img_rook = pygame.transform.scale(self.img_rook, rook_size)

        # Calcular posiciones
        self.h2p_rect = self.img_h2p.get_rect(center=h2p_pos)
        self.avatars_rect = self.img_avatars.get_rect(center=avatars_pos)
        self.rook_rect = self.img_rook.get_rect(center=rook_pos)

        # Botón Back
        self.back_button = Button(
            pos=((settings.WINDOW_WIDTH // 2)+575, (settings.WINDOW_HEIGHT - 70) + 30),
            size=(100, 60),
            text="Back",
            hover_color=(180, 180, 180),
            bg_color=(120, 120, 120),
            text_color=(0, 0, 0),
            font=self.font
        )

    # -------------------------------------------------------------------------
    def safe_load(self, path):
        """Carga imagen desde ruta absoluta; si falla devuelve dummy (para tests)."""
        try:
            return pygame.image.load(path)
        except FileNotFoundError:
            surf = pygame.Surface((400, 200))
            surf.fill((150, 150, 150))
            return surf

    # -------------------------------------------------------------------------
    def draw(self):
        self.screen.blit(self.background, (0, 0))

        # Dibujar las 3 imágenes
        self.screen.blit(self.img_h2p, self.h2p_rect)
        self.screen.blit(self.img_avatars, self.avatars_rect)
        self.screen.blit(self.img_rook, self.rook_rect)

        # Botón
        self.back_button.draw(self.screen)

        pygame.display.flip()

    # -------------------------------------------------------------------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "QUIT"

            if self.back_button.event_mouse(event):
                return "BACK"

    # -------------------------------------------------------------------------
    def run(self):
        """Bucle principal: espera interacción y devuelve 'BACK' o 'QUIT'."""
        clock = pygame.time.Clock()

        while self.running:
            action = self.handle_events()

            if action in ("BACK", "QUIT"):
                return action

            self.draw()
            clock.tick(settings.FPS)
