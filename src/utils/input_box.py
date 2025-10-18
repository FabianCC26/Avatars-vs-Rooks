import pygame

class InputBox:
    def __init__(self, x, y, w, h, font, placeholder="", is_password=False, max_chars=30):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color("gray70")
        self.color_active = pygame.Color("dodgerblue3")
        self.color = self.color_inactive
        self.text = ""
        self.font = font
        self.placeholder = placeholder
        self.active = False
        self.is_password = is_password
        self.show_password = False
        self.max_chars = max_chars

        # Padding interno y separación del ojo
        self.padding_x = 10
        self.padding_right = 35 if is_password else 10

        # Botón del ojo (si aplica)
        if is_password:
            self.eye_rect = pygame.Rect(x + w - 28, y + (h // 2 - 8), 18, 16)
        else:
            self.eye_rect = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Clic dentro del input
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

            # Clic en el icono del ojo
            if self.eye_rect and self.eye_rect.collidepoint(event.pos):
                self.show_password = not self.show_password

            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                print(f"Texto ingresado: {self.text}")
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < self.max_chars:
                self.text += event.unicode

    def draw(self, screen):
        # Mostrar texto (u ocultarlo si es password)
        display_text = (
            self.text if (not self.is_password or self.show_password)
            else "•" * len(self.text)
        )

        # Renderizar texto
        color_text = (0, 0, 0) if self.text else (150, 150, 150)
        text_surface = self.font.render(
            display_text if self.text else self.placeholder,
            True,
            color_text
        )

        # Centrar verticalmente
        text_y = self.rect.y + (self.rect.height - text_surface.get_height()) // 2

        # Limitar texto visible (respetando padding y el espacio del ojo)
        max_width = self.rect.width - (self.padding_x + self.padding_right)
        while text_surface.get_width() > max_width:
            display_text = display_text[1:]
            text_surface = self.font.render(display_text, True, color_text)

        # Fondo y borde
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        pygame.draw.rect(screen, self.color, self.rect, 2)

        # Dibujar texto
        screen.blit(text_surface, (self.rect.x + self.padding_x, text_y))

        # Dibujar icono del ojo si aplica
        if self.eye_rect:
            self.draw_eye_icon(screen)

    def draw_eye_icon(self, screen):
        color = (50, 50, 50)
        pygame.draw.ellipse(screen, color, self.eye_rect, 2)
        center = self.eye_rect.center
        pygame.draw.circle(screen, color, center, 3)
        if not self.show_password:
            pygame.draw.line(screen, color, self.eye_rect.topleft, self.eye_rect.bottomright, 2)

    def get_text(self):
        return self.text
