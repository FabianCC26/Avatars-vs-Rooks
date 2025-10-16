"""

Configuración inicial del proyecto.

"""

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

#  RUTAS DE ARCHIVOS

# Carpeta de recursos (imágenes, sonidos, etc.)
ASSETS_PATH = "assets/"
IMAGES_PATH = ASSETS_PATH + "images/"
SOUNDS_PATH = ASSETS_PATH + "sounds/"

# CONFIGURACIONES EXTERNAS

# Ruta del archivo de configuración de Firebase
FIREBASE_CONFIG_PATH = "DBconfig/avatar-vs-rooks-firebase-adminsdk-fbsvc-20a18344a3.json"


# MODO DESARROLLO
DEBUG_MODE = True
