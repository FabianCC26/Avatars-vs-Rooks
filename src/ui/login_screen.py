import pygame
import os
from src.config import settings
from src.utils.input_box import InputBox
from src.utils.buttons import Button
from src.auth.login_user import login_por_username
from src.ui.main_window import MainWindow
from DBconfig.firebase_config import db
from src.auth.password_recovery import enviar_password_recovery


class LoginScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(settings.FONT_FAMILY, settings.FONT_TITLE_SIZE)
        self.small_font = pygame.font.SysFont(settings.FONT_FAMILY, settings.FONT_DEFAULT_SIZE)
        self.xsmall_font = pygame.font.SysFont(settings.FONT_FAMILY, settings.FONT_SMALL_SIZE)
        self.running = True
        self.message = ""
        self.message_color = (255, 0, 0)

        # Campos de texto
        self.username_box = InputBox(440, 260, 400, 40, self.font, placeholder="Username")
        self.password_box = InputBox(440, 320, 400, 40, self.font, placeholder="Password", is_password=True)

        # Botones principales
        self.login_button = Button(pos=(640, 420), size=(200, 60), text="Login", bg_color=settings.COLOR_PRIMARY)
        self.register_button = Button(pos=(640, 530), size=(200, 50), text="Register", bg_color=(150, 150, 150))
        self.forgot_button = Button(
            pos=(640, 600),
            size=(200, 40),
            text="Forgot Password?",
            bg_color=(180, 180, 180),
            font=self.xsmall_font  # Fuente más pequeña definida en settings
        )
        self.quit_button = Button(pos=(100, 50), size=(150, 40), text="Quit", bg_color=(180, 180, 180))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "QUIT"

            self.username_box.handle_event(event)
            self.password_box.handle_event(event)

            if self.login_button.event_mouse(event):
                self.login_user()
            elif self.register_button.event_mouse(event):
                return "REGISTER"
            elif self.forgot_button.event_mouse(event):
                self.forgot_password_flow()
            elif self.quit_button.event_mouse(event):
                self.running = False
                return "QUIT"

        return None

    def forgot_password_flow(self):
        username = self.username_box.get_text().strip()
        if not username:
            self.message = "Please enter your username to recover password."
            self.message_color = (255, 140, 0)
            return

        usuarios_ref = db.collection("users")
        query = usuarios_ref.where("username", "==", username).stream()
        usuario_encontrado = None
        datos_usuario = None

        for doc in query:
            usuario_encontrado = doc
            datos_usuario = doc.to_dict()
            break

        if not usuario_encontrado:
            self.message = "Username not found."
            self.message_color = (255, 0, 0)
            return

        email = datos_usuario.get("email")
        if not email:
            self.message = "User has no email associated."
            self.message_color = (255, 0, 0)
            return

        try:
            enviar_password_recovery(email)
            self.message = f"Password reset email sent to {email}."
            self.message_color = (0, 180, 0)
        except Exception as e:
            self.message = f"Error sending recovery email: {e}"
            self.message_color = (255, 0, 0)

    def login_user(self):
        username = self.username_box.get_text().strip()
        password = self.password_box.get_text().strip()

        if not username or not password:
            self.message = "Please fill in all fields."
            self.message_color = (255, 0, 0)
            return

        self.message = "Checking credentials..."
        self.message_color = (0, 180, 0)
        pygame.display.flip()
        pygame.time.delay(200)

        user_data = login_por_username(username, password)

        if user_data:
            role = user_data.get("role", "player")
            username_val = user_data.get("username", "Unknown User")
            default_photo = os.path.join("src", "assets", "images", "default_photo.png")

            print(f"Login correcto: {username_val} ({role})")
            main_window = MainWindow(role, username_val, default_photo)
            main_window.run()
            self.running = False
        else:
            self.message = "Invalid username or password."
            self.message_color = (255, 0, 0)

    def draw(self):
        self.screen.fill(settings.COLOR_BACKGROUND)

        # Título
        title_surface = self.font.render("User Login", True, settings.COLOR_TEXT)
        title_rect = title_surface.get_rect(center=(settings.WINDOW_WIDTH // 2, 150))
        self.screen.blit(title_surface, title_rect)

        # Campos
        self.username_box.draw(self.screen)
        self.password_box.draw(self.screen)

        # Botones
        self.login_button.draw(self.screen)
        self.register_button.draw(self.screen)
        self.forgot_button.draw(self.screen)
        self.quit_button.draw(self.screen)

        # Texto informativo
        info_text = "Don't have an account?"
        info_surface = self.small_font.render(info_text, True, (0, 0, 0))
        info_rect = info_surface.get_rect(center=(settings.WINDOW_WIDTH // 2, 480))
        self.screen.blit(info_surface, info_rect)

        # Mensaje de estado
        if self.message:
            msg_surface = self.font.render(self.message, True, self.message_color)
            msg_rect = msg_surface.get_rect(center=(settings.WINDOW_WIDTH // 2, 690))
            self.screen.blit(msg_surface, msg_rect)

        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            action = self.handle_events()
            if action in ["QUIT", "REGISTER"]:
                return action
            self.draw()
            clock.tick(settings.FPS)
