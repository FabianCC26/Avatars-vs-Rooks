import pygame, os

class ButtonWithImage:
    def __init__(self, image_path, pos, size, text="", hover_color=None, fill=None, text_color=(0,0,0), font=None):
        self.pos = pos
        self.size = size
        self.rect = pygame.Rect(0, 0, size[0], size[1])
        self.rect.center = pos

        self.pressed = False

        self.hover_color = hover_color
        self.fill = fill
        self.text = text
        self.text_color = text_color
        self.font = font

        # Carga inicial
        self._load_image(image_path)

    def _load_image(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"No se encontró la imagen: {path}")
        img = pygame.image.load(path)
        # convert_alpha() requiere display inicializado
        img = img.convert_alpha() if img.get_alpha() is not None else img.convert()
        # Escala al tamaño del botón
        self.image = pygame.transform.smoothscale(img, self.rect.size)

    def set_image(self, path: str):
        """Cambia la imagen del botón y mantiene tamaño/pos."""
        self._load_image(path)

    def event_mouse(self, event):
        """Maneja los eventos del mouse y devuelve True si se hace clic"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.pressed = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.pressed:
                self.pressed = False
                # Volver a tamaño normal

                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    return True

    def draw(self, surface):
        # Fondo (opcional)
        if self.hover_color:
            # Dibuja fondo sólo si el mouse está encima (hover)
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(surface, self.hover_color, self.rect, border_radius=12)
        if self.fill:
            pygame.draw.rect(surface, self.fill, self.rect, border_radius=12)

        # Imagen centrada en el rect
        surface.blit(self.image, self.rect)

        # Texto (si hubiera)
        if self.text and self.font:
            txt = self.font.render(self.text, True, self.text_color)
            txt_rect = txt.get_rect(center=self.rect.center)
            surface.blit(txt, txt_rect)