import os
import pygame
from src.config import settings
from src.utils.buttons import Button
from src.utils.buttons_with_images import ButtonWithImage

class MainWindow:

    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        self.running = True
        pygame.display.set_caption("Main Window")

        self.tinted = (0, 0, 0)

        self.button_text_color = self.tinted

        self.actual_menu_layout = "Main menu"


        #Backgrounds:
        dark_bg_path = os.path.join("src", "assets", "images", "dark_bg.png")
        self.dark_bg = pygame.image.load(dark_bg_path).convert()
        self.dark_bg = pygame.transform.scale(self.dark_bg, (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))

        light_bg_path = os.path.join("src","assets", "images", "light_bg.png")
        self.light_bg = pygame.image.load(light_bg_path).convert()
        self.light_bg = pygame.transform.scale(self.light_bg, (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))

        self.actual_bg = self.light_bg


        #Fuentes:
        font_path = os.path.join("src", "assets", "fonts", "Minecraftia-Regular.ttf")
        font_size = 25
        self.font = pygame.font.Font(font_path, font_size)


        #Buttons Configuration:
        self.button_light_bg = (217,217,217)
        self.button_light_hoover = (180,180,180)

        self.button_dark_bg = (115,115,115)
        self.button_dark_hoover = (180,180,180)

        self.image_light_path = os.path.join("src", "assets", "images", "config_light.PNG")
        self.image_dark_path= os.path.join("src", "assets", "images", "config_dark.PNG")

        self.config_button_actual_image = self.image_light_path


        #Main Menu Buttons:
        
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
            font= self.font
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


        #Configuration menu:
        self.light_theme_button = Button(
            pos=(640, 80), size=(300, 80), 
            text="Light Theme",
            hover_color=self.button_light_hoover,
            bg_color=self.button_light_bg, 
            text_color=self.button_text_color, 
            font= self.font
        )


        self.dark_theme_button = Button(
            pos=(640, 180), size=(300, 80), 
            text="Dark Theme",
            hover_color=self.button_light_hoover,
            bg_color=self.button_light_bg, 
            text_color=self.button_text_color, 
            font= self.font
        )

        self.back_to_main_button = Button(
            pos=(640, 600), size=(300, 80), 
            text="Back",
            hover_color=self.button_light_hoover,
            bg_color=self.button_light_bg, 
            text_color=self.button_text_color, 
            font= self.font
        )

        # Tint colors in configuration menu:

        #Color: (206, 14, 14)
        self.tint1 = Button(
            pos=(530, 300), size=(80, 80), 
            text="",
            hover_color=(206, 14, 14),
            bg_color=(206, 14, 14), 
            text_color=self.button_text_color, 
            font= self.font
        )

        #Color: 50, 63, 180
        self.tint2 = Button(
            pos=(640, 300), size=(80, 80), 
            text="",
            hover_color=(50,53,180),
            bg_color=(50,53,180), 
            text_color=self.button_text_color, 
            font= self.font
        )

        #Color: 36, 174, 58
        self.tint3 = Button(
            pos=(750, 300), size=(80, 80), 
            text="",
            hover_color=(36, 174, 58),
            bg_color=(36, 174, 58), 
            text_color=self.button_text_color, 
            font= self.font
        )

        #Color: 138, 50, 180
        self.tint4 = Button(
            pos=(530, 400), size=(80, 80), 
            text="",
            hover_color=(138, 50, 180),
            bg_color=(138, 50, 180), 
            text_color=self.button_text_color, 
            font= self.font
        )

        #Color: 235, 96, 6
        self.tint5 = Button(
            pos=(640, 400), size=(80, 80), 
            text="",
            hover_color=(235, 96, 6),
            bg_color=(235, 96, 6), 
            text_color=self.button_text_color, 
            font= self.font
        )

        #Color: 0,0,0
        self.tint6 = Button(
            pos=(750, 400), size=(80, 80), 
            text="",
            hover_color=(0,0,0),
            bg_color=(0,0,0), 
            text_color=self.button_text_color, 
            font= self.font
        )

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

        self.main_menu_draw()


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

        self.main_menu_draw()


    def tint(self, color):

        self.play_button.text_color = color
        self.user_ranking_button.text_color = color
        self.global_ranking_button.text_color = color
        self.configuration_button.fill = color
        self.light_theme_button.text_color = color
        self.dark_theme_button.text_color = color
        self.back_to_main_button.text_color = color

        self.main_menu_draw()
    

    def configuration_draw(self):
         self.actual_menu_layout = "Configuration"
         self.main_menu_draw()


    def main_menu_draw(self):

        self.screen.blit(self.actual_bg, (0, 0))      
        #self.screen.fill((200, 200, 200))

        if (self.actual_menu_layout == "Configuration"):
            self.light_theme_button.draw(self.screen)
            self.dark_theme_button.draw(self.screen)
            self.back_to_main_button.draw(self.screen)

            self.tint1.draw(self.screen)
            self.tint2.draw(self.screen)
            self.tint3.draw(self.screen)
            self.tint4.draw(self.screen)
            self.tint5.draw(self.screen)
            self.tint6.draw(self.screen)

        else:
            self.play_button.draw(self.screen)
            self.user_ranking_button.draw(self.screen)
            self.global_ranking_button.draw(self.screen)
            self.configuration_button.draw(self.screen)

        pygame.display.flip()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "QUIT"

            if self.actual_menu_layout == "Main menu":
                if self.configuration_button.event_mouse(event):
                    self.configuration_draw()

                if self.play_button.event_mouse(event):
                    pass

                if self.user_ranking_button.event_mouse(event):
                    pass
                if self.global_ranking_button.event_mouse(event):
                    pass

            elif self.actual_menu_layout == "Configuration":
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
                    self.tint((0,0,0))

    def run(self):

        """Bucle principal de la pantalla de registro."""
        clock = pygame.time.Clock()
        while self.running:
            action = self.handle_events()
            if action in ["QUIT", "BACK"]:
                return action

            self.main_menu_draw()
            clock.tick(settings.FPS)

        pygame.quit()
