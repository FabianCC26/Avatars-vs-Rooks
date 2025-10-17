
#Constructor de botones

import pygame

class Button:
    def __init__(self, pos, size, text="", font=None, text_color=(255, 255, 255),
                 bg_color=(0, 128, 255), hover_color=(0, 100, 200), scale=1):
        """
        Crea un botón con texto y animación de clic.

        Parámetros:
        - pos: (x, y) posición del centro del botón
        - size: (ancho, alto)
        - text: texto del botón
        - font: fuente Pygame (si es None, usa por defecto)
        - text_color: color del texto
        - bg_color: color base del botón
        - hover_color: color cuando el cursor está encima
        - scale: escala visual del botón
        """
        self.pos = pos
        self.size = (int(size[0] * scale), int(size[1] * scale))
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.font = font or pygame.font.SysFont("arial", 26, bold=True)

        # Crear superficies
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)
        self.pressed = False

    def draw(self, surface):
        """Dibuja el botón con el color adecuado y el texto centrado"""
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.bg_color
        self.image.fill(color)

        # Renderizar texto
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.size[0] / 2, self.size[1] / 2))
        self.image.blit(text_surface, text_rect)

        # Dibujar botón en pantalla
        surface.blit(self.image, self.rect)

    def event_mouse(self, event):
        """Maneja los eventos del mouse y devuelve True si se hace clic"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.pressed = True
                # Pequeño efecto de "clic"
                self.image = pygame.transform.scale(self.image, (int(self.size[0] * 0.95), int(self.size[1] * 0.95)))
                self.rect = self.image.get_rect(center=self.pos)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.pressed:
                self.pressed = False
                # Volver a tamaño normal
                self.image = pygame.Surface(self.size, pygame.SRCALPHA)
                self.rect = self.image.get_rect(center=self.pos)
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    return True

        return False
