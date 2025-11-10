import os
import pygame
from src.config import settings
from src.utils.input_box import InputBox
from src.utils.buttons import Button
from src.utils.dropdown import Dropdown  # Selector simple para rol
from src.utils.searchable_dropdown import SearchableDropdown, load_countries  # Selector con búsqueda para país
from src.auth.register_user import registrar_usuario


class RegisterScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(settings.FONT_FAMILY, settings.FONT_TITLE_SIZE)  # Fuente principal
        self.small_font = pygame.font.SysFont(settings.FONT_FAMILY, settings.FONT_DEFAULT_SIZE)  # Fuente secundaria
        self.running = True
        self.message = ""
        self.message_color = (255, 0, 0)

        # Cargar países desde assets
        countries_path = os.path.join("src", "assets", "data", "countries.json")
        self.countries = load_countries(countries_path)

        # Dropdown de rol (simple, 2 opciones)
        self.role_dropdown = Dropdown(
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

        # Selector de país para admin (con búsqueda)
        self.country_dropdown = SearchableDropdown(
            x=440, y=500, width=400, height=40,
            font=self.font,
            options=self.countries if self.countries else [{"name": "Costa Rica", "alpha2": "CR", "alpha3": "CRI"}],
            main_color=(200, 200, 200),
            hover_color=(170, 170, 170),
            text_color=(0, 0, 0),
            placeholder="Select a country…",
            max_visible=10,
            item_height=28
        )

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

            self.role_dropdown.handle_event(event)       # Rol simple
            self.country_dropdown.handle_event(event)    # País con búsqueda

            if self.register_button.event_mouse(event):
                self.registrar_usuario()
            if self.back_button.event_mouse(event):
                return "BACK"

        return None

    def _role(self) -> str:
        # Obtiene el rol seleccionado del dropdown simple
        selected = self.role_dropdown.get_selected()
        return selected if selected in ("player", "admin") else "player"

    def registrar_usuario(self):
        role = self._role()

        data = {
            "role": role,
            "username": self.username_box.get_text(),
            "email": self.email_box.get_text(),
            "password": self.password_box.get_text(),
        }

        if role == "admin":
            data["name"] = self.name_box.get_text()
            data["lastname"] = self.lastname_box.get_text()

            # País seleccionado requerido
            selected_country = self.country_dropdown.get_selected()
            if selected_country is None:
                self.message = "Please select a country for admin."
                self.message_color = (255, 0, 0)
                return

            data["nationality"] = {
                "name": selected_country["name"],
                "alpha2": selected_country["alpha2"],
                "alpha3": selected_country["alpha3"],
            }

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

        # Rol (simple)
        self.role_dropdown.draw(self.screen)

        # Campos admin (sin dibujar aún el country dropdown)
        is_admin = self._role() == "admin"
        if is_admin:
            self.name_box.draw(self.screen)
            self.lastname_box.draw(self.screen)

        # Botones
        self.back_button.draw(self.screen)
        self.register_button.draw(self.screen)

        # Dibujar el country dropdown al final por encima de los botones
        if is_admin:
            self.country_dropdown.draw(self.screen)

        # Mensaje
        if self.message:
            msg_surface = self.font.render(self.message, True, self.message_color)
            msg_rect = msg_surface.get_rect(center=(settings.WINDOW_WIDTH // 2, 720))
            self.screen.blit(msg_surface, msg_rect)

        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            action = self.handle_events()
            if action in ["QUIT", "BACK"]:
                return action
            self.draw()
            clock.tick(settings.FPS)
