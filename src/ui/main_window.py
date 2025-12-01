import os
import pygame
from src.config import settings
from src.utils.buttons import Button
from src.utils.input_box import InputBox
from src.utils.spotify_api_configuration import MusicAPI
from src.utils.buttons_with_images import ButtonWithImage
from src.config.settings import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from src.ui.info_window import InfoWindow
from src.utils.user_preferences import load_user_preferences, save_user_preferences  # ✅ Nuevo import
from src.gameplay.main_matrix import MatrixGame

class MainWindow:

    def __init__(self, role, user, photo):

        self.screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        self.running = True
        pygame.display.set_caption("Main Window")

        self.tinted = (0, 0, 0)
        self.button_text_color = self.tinted
        self.actual_menu_layout = "Main menu"

        # Backgrounds:
        dark_bg_path = os.path.join("src", "assets", "images", "dark_bg.png")
        self.dark_bg = pygame.image.load(dark_bg_path).convert()
        self.dark_bg = pygame.transform.scale(self.dark_bg, (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))

        light_bg_path = os.path.join("src", "assets", "images", "light_bg.png")
        self.light_bg = pygame.image.load(light_bg_path).convert()
        self.light_bg = pygame.transform.scale(self.light_bg, (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))

        self.actual_bg = self.light_bg

        # Fuentes:
        font_path = os.path.join("src", "assets", "fonts", "Minecraftia-Regular.ttf")
        font_size = 25
        self.font = pygame.font.Font(font_path, font_size)

        # Buttons Configuration:
        self.button_light_bg = (217, 217, 217)
        self.button_light_hoover = (180, 180, 180)

        self.button_dark_bg = (115, 115, 115)
        self.button_dark_hoover = (180, 180, 180)

        self.image_light_path = os.path.join("src", "assets", "images", "config_light.PNG")
        self.image_dark_path = os.path.join("src", "assets", "images", "config_dark.PNG")

        self.config_button_actual_image = self.image_light_path

        # Main Menu Buttons:
        self.play_button = Button(
            pos=(640, 350),
            size=(300, 80),
            text="PLAY",
            hover_color=self.button_light_hoover,
            bg_color=self.button_light_bg,
            text_color=self.button_text_color,
            font=self.font
        )

        self.user_ranking_button = Button(
            pos=(640, 450),
            size=(300, 80),
            text="USER´S RANKING",
            hover_color=self.button_light_hoover,
            bg_color=self.button_light_bg,
            text_color=self.button_text_color,
            font=self.font
        )

        self.global_ranking_button = Button(
            pos=(640, 550), size=(300, 80),
            text="GLOBAL RANKING",
            hover_color=self.button_light_hoover,
            bg_color=self.button_light_bg,
            text_color=self.button_text_color,
            font=self.font
        )

        self.configuration_button = ButtonWithImage(
            image_path=self.config_button_actual_image,
            pos=(1000, 550),
            size=(90, 90),
            text="",
            hover_color=self.button_light_hoover,
            fill=self.tinted,
            text_color=self.button_text_color,
        )

        self.info_button = Button(
            pos=(250, 550),
            size=(150, 60),
            text="INFO",
            hover_color=self.button_light_hoover,
            bg_color=self.button_light_bg,
            text_color=self.button_text_color,
            font=self.font
        )

        self.user_info_canva = Button(
            pos=(470, 100), size=(500, 90),
            text=(str(user) + "   -   " + str(role)),
            hover_color=self.button_light_bg,
            bg_color=self.button_light_bg,
            text_color=self.button_text_color,
            font=self.font
        )

        self.user_photo_canva = ButtonWithImage(
            image_path=photo,
            pos=(170, 100),
            size=(90, 90),
            text="",
            hover_color=self.button_light_hoover,
            fill=self.tinted,
            text_color=self.button_text_color,
        )

        # Configuration menu:
        self.light_theme_button = Button(
            pos=(430, 95), size=(300, 80),
            text="Light Theme",
            hover_color=self.button_light_hoover,
            bg_color=self.button_light_bg,
            text_color=self.button_text_color,
            font=self.font
        )

        self.dark_theme_button = Button(
            pos=(780, 95), size=(300, 80),
            text="Dark Theme",
            hover_color=self.button_light_hoover,
            bg_color=self.button_light_bg,
            text_color=self.button_text_color,
            font=self.font
        )

        self.back_to_main_button = Button(
            pos=(640, 600), size=(300, 80),
            text="Back",
            hover_color=self.button_light_hoover,
            bg_color=self.button_light_bg,
            text_color=self.button_text_color,
            font=self.font
        )

        # Tint colors in configuration menu:
        self.tint1 = Button(pos=(330, 230), size=(80, 80), text="", hover_color=(206, 14, 14), bg_color=(206, 14, 14), text_color=self.button_text_color, font=self.font)
        self.tint2 = Button(pos=(430, 230), size=(80, 80), text="", hover_color=(50, 63, 180), bg_color=(50, 63, 180), text_color=self.button_text_color, font=self.font)
        self.tint3 = Button(pos=(540, 230), size=(80, 80), text="", hover_color=(36, 174, 58), bg_color=(36, 174, 58), text_color=self.button_text_color, font=self.font)
        self.tint4 = Button(pos=(673, 230), size=(80, 80), text="", hover_color=(138, 50, 180), bg_color=(138, 50, 180), text_color=self.button_text_color, font=self.font)
        self.tint5 = Button(pos=(773, 230), size=(80, 80), text="", hover_color=(235, 96, 6), bg_color=(235, 96, 6), text_color=self.button_text_color, font=self.font)
        self.tint6 = Button(pos=(873, 230), size=(80, 80), text="", hover_color=(0, 0, 0), bg_color=(0, 0, 0), text_color=self.button_text_color, font=self.font)

        self.music_input_box = InputBox(490, 300, 300, 40, self.font, placeholder="Song name")

        self.search_song_button = Button(
            pos=(640, 390),
            size=(300, 80),
            text="Search",
            hover_color=self.button_light_hoover,
            bg_color=self.button_light_bg,
            text_color=self.button_text_color,
            font=self.font
        )

        self.pause_song_button = Button(
            pos=(640, 500),
            size=(300, 80),
            text="Pause",
            hover_color=self.button_light_hoover,
            bg_color=self.button_light_bg,
            text_color=self.button_text_color,
            font=self.font
        )

        self.resume_song_button = Button(
            pos=(730, 500),
            size=(120, 80),
            text="Resume",
            hover_color=self.button_light_hoover,
            bg_color=self.button_light_bg,
            text_color=self.button_text_color,
            font=self.font
        )

        self.api = MusicAPI(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI
        )

        # ✅ Preferencias del usuario
        self.username = user
        self.preferences = load_user_preferences(self.username)

        theme = self.preferences.get("theme", "light")
        color = tuple(self.preferences.get("color", (0, 0, 0)))

        if theme == "dark":
            self.turn_dark()
        else:
            self.turn_light()

        self.tint(color)

    def put_music_api(self, song):
        self.api.play_song(song)

    def pause_music_api(self):
        self.api.pause()

    def resume_mucis_api(self):
        self.api.resume()

    def turn_dark(self):
        self.actual_bg = self.dark_bg
        self.play_button.bg_color = self.button_dark_bg
        self.play_button.hover_color = self.button_dark_hoover
        self.user_ranking_button.bg_color = self.button_dark_bg
        self.user_ranking_button.hover_color = self.button_dark_hoover
        self.global_ranking_button.bg_color = self.button_dark_bg
        self.global_ranking_button.hover_color = self.button_dark_hoover
        self.configuration_button.set_image(self.image_dark_path)
        self.light_theme_button.bg_color = self.button_dark_bg
        self.light_theme_button.hover_color = self.button_dark_hoover
        self.dark_theme_button.bg_color = self.button_dark_bg
        self.dark_theme_button.hover_color = self.button_dark_hoover
        self.back_to_main_button.bg_color = self.button_dark_bg
        self.back_to_main_button.hover_color = self.button_dark_hoover
        self.search_song_button.bg_color = self.button_dark_bg
        self.search_song_button.hover_color = self.button_dark_hoover
        self.pause_song_button.bg_color = self.button_dark_bg
        self.pause_song_button.hover_color = self.button_dark_hoover
        self.resume_song_button.bg_color = self.button_dark_bg
        self.resume_song_button.hover_color = self.button_dark_hoover
        self.user_info_canva.bg_color = self.button_dark_bg
        self.user_info_canva.hover_color = self.button_dark_bg
        self.info_button.bg_color = self.button_dark_bg
        self.info_button.hover_color = self.button_dark_hoover
        self.main_menu_draw()

        self.preferences["theme"] = "dark"
        save_user_preferences(self.username, self.preferences)

    def turn_light(self):
        self.actual_bg = self.light_bg
        self.play_button.bg_color = self.button_light_bg
        self.play_button.hover_color = self.button_light_hoover
        self.user_ranking_button.bg_color = self.button_light_bg
        self.user_ranking_button.hover_color = self.button_light_hoover
        self.global_ranking_button.bg_color = self.button_light_bg
        self.global_ranking_button.hover_color = self.button_light_hoover
        self.configuration_button.set_image(self.image_light_path)
        self.light_theme_button.bg_color = self.button_light_bg
        self.light_theme_button.hover_color = self.button_light_hoover
        self.dark_theme_button.bg_color = self.button_light_bg
        self.dark_theme_button.hover_color = self.button_light_hoover
        self.back_to_main_button.bg_color = self.button_light_bg
        self.back_to_main_button.hover_color = self.button_light_hoover
        self.search_song_button.bg_color = self.button_light_bg
        self.search_song_button.hover_color = self.button_light_hoover
        self.pause_song_button.bg_color = self.button_light_bg
        self.pause_song_button.hover_color = self.button_light_hoover
        self.resume_song_button.bg_color = self.button_light_bg
        self.resume_song_button.hover_color = self.button_light_hoover
        self.user_info_canva.bg_color = self.button_light_bg
        self.user_info_canva.hover_color = self.button_light_bg
        self.info_button.bg_color = self.button_light_bg
        self.info_button.hover_color = self.button_light_hoover
        self.main_menu_draw()

       
        self.preferences["theme"] = "light"
        save_user_preferences(self.username, self.preferences)

    def tint(self, color):
        self.play_button.text_color = color
        self.user_ranking_button.text_color = color
        self.global_ranking_button.text_color = color
        self.configuration_button.fill = color
        self.light_theme_button.text_color = color
        self.dark_theme_button.text_color = color
        self.back_to_main_button.text_color = color
        self.search_song_button.text_color = color
        self.pause_song_button.text_color = color
        self.resume_song_button.text_color = color
        self.info_button.text_color = color
        self.main_menu_draw()

    
        self.preferences["color"] = list(color)
        save_user_preferences(self.username, self.preferences)

    def main_menu_draw(self):
        self.screen.blit(self.actual_bg, (0, 0))
        if self.actual_menu_layout == "Configuration":
            self.light_theme_button.draw(self.screen)
            self.dark_theme_button.draw(self.screen)
            self.back_to_main_button.draw(self.screen)
            self.tint1.draw(self.screen)
            self.tint2.draw(self.screen)
            self.tint3.draw(self.screen)
            self.tint4.draw(self.screen)
            self.tint5.draw(self.screen)
            self.tint6.draw(self.screen)
            self.search_song_button.draw(self.screen)
            self.music_input_box.draw(self.screen)
            self.pause_song_button.draw(self.screen)
        else:
            self.user_info_canva.draw(self.screen)
            self.play_button.draw(self.screen)
            self.user_ranking_button.draw(self.screen)
            self.global_ranking_button.draw(self.screen)
            self.configuration_button.draw(self.screen)
            self.info_button.draw(self.screen)
            self.user_photo_canva.draw(self.screen)
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "QUIT"

            if self.actual_menu_layout == "Main menu":
                if self.configuration_button.event_mouse(event):
                    self.actual_menu_layout = "Configuration"


                if self.play_button.event_mouse(event):
                    game = MatrixGame()
                    game.run()
                
                if self.info_button.event_mouse(event):
                    from src.ui.info_window import InfoWindow
                    theme_colors = {
                        "bg": self.button_light_bg if self.actual_bg == self.light_bg else self.button_dark_bg,
                        "hover": self.button_light_hoover if self.actual_bg == self.light_bg else self.button_dark_hoover,
                        "text": self.tinted
                    }
                    info_window = InfoWindow(self.screen, self.actual_bg, self.font)
                    info_action = info_window.run()
                    self.main_menu_draw()
                    if info_action == "QUIT":
                        self.running = False
                        return "QUIT"

            elif self.actual_menu_layout == "Configuration":
                if self.music_input_box.handle_event(event):
                    print(self.music_input_box.get_text())
                if self.search_song_button.event_mouse(event):
                    self.put_music_api(self.music_input_box.get_text())
                if self.pause_song_button.event_mouse(event):
                    self.pause_music_api()
                if self.resume_song_button.event_mouse(event):
                    self.resume_mucis_api()
                if self.dark_theme_button.event_mouse(event):
                    self.turn_dark()
                if self.light_theme_button.event_mouse(event):
                    self.turn_light()
                if self.back_to_main_button.event_mouse(event):
                    self.actual_menu_layout = "Main menu"
                if self.tint1.event_mouse(event):
                    self.tint((206, 14, 14))
                if self.tint2.event_mouse(event):
                    self.tint((50, 63, 180))
                if self.tint3.event_mouse(event):
                    self.tint((36, 174, 58))
                if self.tint4.event_mouse(event):
                    self.tint((138, 50, 180))
                if self.tint5.event_mouse(event):
                    self.tint((235, 96, 6))
                if self.tint6.event_mouse(event):
                    self.tint((0, 0, 0))

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            action = self.handle_events()
            if action in ["QUIT", "BACK"]:
                return action
            self.main_menu_draw()
            clock.tick(settings.FPS)
        return None
