import pygame

class Dropdown:
    def __init__(self, x, y, width, height, font, main_color, hover_color, text_color, options, default_index=0):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = main_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = font
        self.options = options
        self.selected_index = default_index
        self.show_options = False
        self.option_height = height
        self.hovered_option = None

    def handle_event(self, event):
        """ Maneja los clics y la selección del menú """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.show_options = not self.show_options
            elif self.show_options:
                for i, option in enumerate(self.options):
                    option_rect = pygame.Rect(
                        self.rect.x, self.rect.y + (i + 1) * self.option_height, self.rect.width, self.option_height
                    )
                    if option_rect.collidepoint(event.pos):
                        self.selected_index = i
                        self.show_options = False
                        break
                else:
                    self.show_options = False

    def draw(self, surface):
        """ Dibuja el dropdown y las opciones """
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.rect(surface, self.hover_color if self.rect.collidepoint(mouse_pos) else self.color, self.rect)

        text_surface = self.font.render(self.options[self.selected_index], True, self.text_color)
        surface.blit(text_surface, text_surface.get_rect(center=self.rect.center))

        # Dibujar flecha ▼
        pygame.draw.polygon(
            surface, self.text_color,
            [(self.rect.right - 20, self.rect.centery - 4), (self.rect.right - 10, self.rect.centery - 4), (self.rect.right - 15, self.rect.centery + 4)]
        )

        # Dibujar opciones si está abierto
        if self.show_options:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(
                    self.rect.x, self.rect.y + (i + 1) * self.option_height, self.rect.width, self.option_height
                )
                color = self.hover_color if option_rect.collidepoint(mouse_pos) else self.color
                pygame.draw.rect(surface, color, option_rect)
                text_surface = self.font.render(option, True, self.text_color)
                surface.blit(text_surface, text_surface.get_rect(center=option_rect.center))

    def get_selected(self):
        """ Devuelve el valor seleccionado """
        return self.options[self.selected_index]
