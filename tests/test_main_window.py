import os
import sys
import pygame

# ---- Arreglo de rutas para poder usar 'src' como paquete de nivel superior ----
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from src.ui.main_window import MainWindow
from src.config import settings

pygame.init()

if __name__ == "__main__":
    image_path = "src/assets/images/default_photo.png"
    window = MainWindow("Player.", "jmq3", image_path)
    window.run()
