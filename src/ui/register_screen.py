import pygame
from src.config import settings
from src.utils.input_box import InputBox
from src.utils.buttons import Button
from src.utils.dropdown import Dropdown
from src.auth.register_user import registrar_usuario


class RegisterScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 28)
        self.small_font = pygame.font.SysFont("arial", 22)
        self.running = True
        self.message = ""
        self.message_color = (255, 0, 0)

        # Dropdown de rol
        self.dropdown = Dropdown(
            x=440, y=130, width=400, height=40,
            font=self.font,
            main_color=(200, 200, 200),
            hover_color=(170, 170, 170),
            text_color=(0, 0, 0),
            options=["player", "admin"]
        )

        # Campos comunes
        self.username_box = InputBox(440, 200, 400, 40, self.font, placeholder="Username")
        self.email_box = InputBox(440, 260, 400, 40, self.font, placeholder="Email")
        self.password_box = InputBox(440, 320, 400, 40, self.font, placeholder="Password", is_password=True)

        # Campos admin
        self.name_box = InputBox(440, 380, 400, 40, self.font, placeholder="Name")
        self.lastname_box = InputBox(440, 440, 400, 40, self.font, placeholder="Last name")
        self.nationality_box = InputBox(440, 500, 400, 40, self.font, placeholder="Nationality")

        # Botones
        self.register_button = Button(pos=(640, 630), size=(200, 60), text="Register", bg_color=settings.COLOR_PRIMARY)
        self.back_button = Button(pos=(100, 50), size=(150, 40), text="Back", bg_color=(180, 180, 180))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "QUIT"

            self.username_box.handle_event(event)
            self.email_box.handle_event(event)
            self.password_box.handle_event(event)
            self.name_box.handle_event(event)
            self.lastname_box.handle_event(event)
            self.nationality_box.handle_event(event)
            self.dropdown.handle_event(event)

            if self.register_button.event_mouse(event):
                self.registrar_usuario()
            if self.back_button.event_mouse(event):
                return "BACK"

        return None

    def registrar_usuario(self):
        role = self.dropdown.get_selected()
        data = {
            "role": role,
            "username": self.username_box.get_text(),
            "email": self.email_box.get_text(),
            "password": self.password_box.get_text(),
        }

        if role == "admin":
            data["name"] = self.name_box.get_text()
            data["lastname"] = self.lastname_box.get_text()
            data["nationality"] = self.nationality_box.get_text()

        success, msg = registrar_usuario(data)
        self.message = msg
        self.message_color = (0, 180, 0) if success else (255, 0, 0)

    def draw(self):
        self.screen.fill(settings.COLOR_BACKGROUND)

        # Título
        title_surface = self.font.render("User registration", True, settings.COLOR_TEXT)
        title_rect = title_surface.get_rect(center=(settings.WINDOW_WIDTH // 2, 70))
        self.screen.blit(title_surface, title_rect)

        # Campos
        self.username_box.draw(self.screen)
        self.email_box.draw(self.screen)
        self.password_box.draw(self.screen)

        # Campos admin
        if self.dropdown.get_selected() == "admin":
            self.name_box.draw(self.screen)
            self.lastname_box.draw(self.screen)
            self.nationality_box.draw(self.screen)

        # Botones
        self.back_button.draw(self.screen)
        self.register_button.draw(self.screen)

        # Mensaje
        if self.message:
            msg_surface = self.font.render(self.message, True, self.message_color)
            msg_rect = msg_surface.get_rect(center=(settings.WINDOW_WIDTH // 2, 720))
            self.screen.blit(msg_surface, msg_rect)

        # Dibujar el dropdown al final → para que quede por encima
        self.dropdown.draw(self.screen)

        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            action = self.handle_events()
            if action in ["QUIT", "BACK"]:
                return action
            self.draw()
            clock.tick(settings.FPS)
