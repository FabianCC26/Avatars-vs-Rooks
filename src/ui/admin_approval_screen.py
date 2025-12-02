import pygame
from src.config import settings
from src.utils.input_box import InputBox
from src.utils.buttons import Button
from src.auth.admin_approval import approve_admin_by_token, reject_admin_by_token


class AdminApprovalScreen:
    """
    Pantalla para que un administrador aprobado ingrese un token de aprobación
    y apruebe o rechace solicitudes de nuevo administrador.
    """

    def __init__(self, screen, admin_username: str):
        # Usamos la misma superficie que main_window
        self.screen = screen
        self.admin_username = admin_username

        self.running = True

        # Fuentes
        self.title_font = pygame.font.SysFont("arial", 32, bold=True)
        self.text_font = pygame.font.SysFont("arial", 20)
        # Fuente específica para el token (más pequeña para que no se vea gigante)
        self.token_font = pygame.font.SysFont("arial", 22)

        # Mensajes de feedback
        self.message = ""
        self.message_color = (200, 0, 0)

        # Input para el token: ancho grande y max_chars alto para no truncar el token
        self.token_input = InputBox(
            x=200,
            y=200,
            w=880,
            h=40,
            font=self.token_font,
            placeholder="Paste approval token here",
            is_password=False,
            max_chars=80,  # IMPORTANTE: tokens largos no se recortan
        )

        # Botones de acción
        self.approve_button = Button(
            pos=(settings.WINDOW_WIDTH // 2 - 120, 300),
            size=(180, 70),
            text="Approve",
            bg_color=(34, 139, 34),
            hover_color=(24, 119, 24),
            text_color=(255, 255, 255),
            font=self.text_font,
        )

        self.reject_button = Button(
            pos=(settings.WINDOW_WIDTH // 2 + 120, 300),
            size=(180, 70),
            text="Reject",
            bg_color=(178, 34, 34),
            hover_color=(148, 24, 24),
            text_color=(255, 255, 255),
            font=self.text_font,
        )

        self.back_button = Button(
            pos=(120, 60),
            size=(140, 40),
            text="Back",
            bg_color=(200, 200, 200),
            hover_color=(170, 170, 170),
            text_color=(0, 0, 0),
            font=self.text_font,
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "QUIT"

            # Input token
            self.token_input.handle_event(event)

            # Botón Back
            if self.back_button.event_mouse(event):
                self.running = False
                return "BACK"

            # Botón Approve
            if self.approve_button.event_mouse(event):
                self._handle_approve()

            # Botón Reject
            if self.reject_button.event_mouse(event):
                self._handle_reject()

        return None

    def _handle_approve(self):
        """
        Maneja la acción de aprobar un administrador.
        """
        raw_token = self.token_input.get_text()
        token = raw_token.strip()

        if not token:
            self.message = "Please enter a token."
            self.message_color = (200, 0, 0)
            return

        ok, msg = approve_admin_by_token(token, self.admin_username.lower())
        self.message = msg
        self.message_color = (0, 160, 0) if ok else (200, 0, 0)

    def _handle_reject(self):
        """
        Maneja la acción de rechazar una solicitud de administrador.
        """
        raw_token = self.token_input.get_text()
        token = raw_token.strip()

        if not token:
            self.message = "Please enter a token."
            self.message_color = (200, 0, 0)
            return

        ok, msg = reject_admin_by_token(token, self.admin_username.lower())
        self.message = msg
        self.message_color = (139, 0, 0) if ok else (200, 0, 0)

    def draw(self):
        # Fondo simple gris claro
        self.screen.fill((245, 245, 245))

        # Título
        title_surface = self.title_font.render("Admin approval", True, (0, 0, 0))
        title_rect = title_surface.get_rect(center=(settings.WINDOW_WIDTH // 2, 100))
        self.screen.blit(title_surface, title_rect)

        # Texto de ayuda
        help_text = "Paste the approval token received by email and choose Approve or Reject."
        help_surface = self.text_font.render(help_text, True, (50, 50, 50))
        help_rect = help_surface.get_rect(center=(settings.WINDOW_WIDTH // 2, 150))
        self.screen.blit(help_surface, help_rect)

        # Input de token
        self.token_input.draw(self.screen)

        # Botones
        self.approve_button.draw(self.screen)
        self.reject_button.draw(self.screen)
        self.back_button.draw(self.screen)

        # Mensaje de resultado
        if self.message:
            msg_surface = self.text_font.render(self.message, True, self.message_color)
            msg_rect = msg_surface.get_rect(center=(settings.WINDOW_WIDTH // 2, 380))
            self.screen.blit(msg_surface, msg_rect)

        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            action = self.handle_events()
            if action in ("QUIT", "BACK"):
                return action
            self.draw()
            clock.tick(settings.FPS)
        return None
