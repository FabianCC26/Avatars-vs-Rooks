"""
Configuración inicial del proyecto.
"""
import os
from dotenv import load_dotenv

# Carga el archivo .env desde la misma carpeta
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# Dimensiones de la ventana principal (en píxeles)
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Título de la ventana
WINDOW_TITLE = "Avatars vs Rooks"

# Colores base (RGB)
COLOR_BACKGROUND = (245, 245, 245)
COLOR_PRIMARY = (15, 158, 213)
COLOR_SECONDARY = (131, 202, 235)
COLOR_TEXT = (33, 33, 33)

# FPS (frames por segundo) para pygame
FPS = 60

# RUTAS DE ARCHIVOS

# Carpeta de recursos (imágenes, sonidos, etc.)
ASSETS_PATH = "assets/"
IMAGES_PATH = ASSETS_PATH + "images/"
SOUNDS_PATH = ASSETS_PATH + "sounds/"

# CONFIGURACIONES EXTERNAS

# Ruta del archivo de configuración de Firebase
FIREBASE_CONFIG_PATH = "DBconfig/avatar-vs-rooks-firebase-adminsdk-fbsvc-20a18344a3.json"

# MODO DESARROLLO
DEBUG_MODE = True

# FUENTES Y TAMAÑOS DE TEXTO
FONT_FAMILY = "arial"
FONT_TITLE_SIZE = 28
FONT_DEFAULT_SIZE = 22
FONT_SMALL_SIZE = 18
