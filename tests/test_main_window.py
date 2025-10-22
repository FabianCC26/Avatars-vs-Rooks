import pygame
from src.ui.main_window import MainWindow
from src.config import settings


if __name__ == "__main__":
    image_path = "src/assets/images/default_photo.png"
    window = MainWindow("Admin.", "Admin123", image_path)
    window.run()

    


