import pygame
from src.config import settings
from src.utils.input_box import InputBox
from src.utils.buttons import Button
from src.utils.dropdown import Dropdown
from src.auth.register_user import registrar_usuario


class RegisterScreen:
    def __init__(self, screen):
        """
        Pantalla de registro de usuarios.
        Permite crear nuevos usuarios en Firebase utilizando los componentes
        personalizados de la carpeta utils.
        """
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 28)
        self.running = True
        self.message = ""          # Mensaje de éxito o error
        self.message_color = (255, 0, 0)

        # 🔹 Menú desplegable de rol (ubicado al inicio del formulario)
        self.dropdown = Dropdown(
            x=440, y=130, width=400, height=40,
            font=self.font,
            main_color=(200, 200, 200),
            hover_color=(170, 170, 170),
            text_color=(0, 0, 0),
            options=["player", "admin"]
        )

        # Campos de entrada comunes (textos visibles en inglés)
        self.username_box = InputBox(440, 200, 400, 40, self.font, placeholder="Username")
        self.email_box = InputBox(440, 260, 400, 40, self.font, placeholder="Email")
        self.password_box = InputBox(440, 320, 400, 40, self.font, placeholder="Password", is_password=True)

        # Campos adicionales solo visibles si el rol es "admin"
        self.name_box = InputBox(440, 380, 400, 40, self.font, placeholder="Name")
        self.lastname_box = InputBox(440, 440, 400, 40, self.font, placeholder="Last name")
        self.nationality_box = InputBox(440, 500, 400, 40, self.font, placeholder="Nationality")

        # Botones principales (textos visibles en inglés)
        self.register_button = Button(
            pos=(640, 600), size=(200, 60), text="Register",
            bg_color=settings.COLOR_PRIMARY
        )
        self.back_button = Button(
            pos=(100, 50), size=(150, 40), text="Back",
            bg_color=(180, 180, 180)
        )

    def handle_events(self):
        """Maneja los eventos de teclado y ratón."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "QUIT"

            # Eventos de los campos de texto y menú
            self.username_box.handle_event(event)
            self.email_box.handle_event(event)
            self.password_box.handle_event(event)
            self.name_box.handle_event(event)
            self.lastname_box.handle_event(event)
            self.nationality_box.handle_event(event)
            self.dropdown.handle_event(event)

            # Eventos de los botones
            if self.register_button.event_mouse(event):
                self.registrar_usuario()
            if self.back_button.event_mouse(event):
                return "BACK"

        return None

    def registrar_usuario(self):
        """Obtiene los datos ingresados y registra el usuario en Firebase."""
        role = self.dropdown.get_selected()
        data = {
            "role": role,
            "username": self.username_box.get_text(),
            "email": self.email_box.get_text(),
            "password": self.password_box.get_text(),
        }

        # Si el rol es administrador, agrega los campos adicionales
        if role == "admin":
            data["name"] = self.name_box.get_text()
            data["lastname"] = self.lastname_box.get_text()
            data["nationality"] = self.nationality_box.get_text()

        success, msg = registrar_usuario(data)
        self.message = msg
        self.message_color = (0, 180, 0) if success else (255, 0, 0)

    def draw(self):
        """Dibuja todos los elementos de la pantalla."""
        self.screen.fill(settings.COLOR_BACKGROUND)

        # Título principal
        title_surface = self.font.render("User registration", True, settings.COLOR_TEXT)
        self.screen.blit(title_surface, (settings.WINDOW_WIDTH // 2 - 150, 60))

        # Dibuja los campos comunes
        self.username_box.draw(self.screen)
        self.email_box.draw(self.screen)
        self.password_box.draw(self.screen)

        # Si el rol seleccionado es "admin", mostrar los campos extra
        if self.dropdown.get_selected() == "admin":
            self.name_box.draw(self.screen)
            self.lastname_box.draw(self.screen)
            self.nationality_box.draw(self.screen)

        # Dibujar botones
        self.back_button.draw(self.screen)
        self.register_button.draw(self.screen)

        # 🔹 Dibuja el dropdown al final para que quede por delante de todo
        self.dropdown.draw(self.screen)

        # Mostrar mensaje centrado horizontalmente
        if self.message:
            msg_surface = self.font.render(self.message, True, self.message_color)
            msg_rect = msg_surface.get_rect(center=(settings.WINDOW_WIDTH // 2, 690))
            self.screen.blit(msg_surface, msg_rect)

        pygame.display.flip()

    def run(self):
        """Bucle principal de la pantalla de registro."""
        clock = pygame.time.Clock()
        while self.running:
            action = self.handle_events()
            if action in ["QUIT", "BACK"]:
                return action

            self.draw()
            clock.tick(settings.FPS)
