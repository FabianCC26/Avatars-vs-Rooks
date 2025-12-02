import pygame
import os

# ----------------- RUTAS -----------------
ASSETS_DIR = os.path.join("src", "assets")

def load_img(path, size=None):
    full = os.path.join(ASSETS_DIR, path)
    print("Buscando imagen:", full)

    img = pygame.image.load(full)

    if size is not None:
        img = pygame.transform.smoothscale(img, size)

    return img

# ----------------- GRID / VENTANA -----------------
GRID_ROWS = 9
GRID_COLS = 5

CELL_SIZE = 70  # solo por referencia
WINDOW_WIDTH = GRID_COLS * CELL_SIZE
WINDOW_HEIGHT = GRID_ROWS * CELL_SIZE

# ----------------- COLORES -----------------
BACKGROUND_COLOR = (20, 20, 20)
GRID_COLOR = (80, 80, 80)
TEXT_COLOR = (255, 255, 255)

# ----------------- ECONOMÍA -----------------
INITIAL_COINS = 100
COINS_PER_KILL = 75   # de la tabla: 75 monedas por avatar eliminado

# ----------------- SPAWN -----------------
SPAWN_INTERVAL = 3.0  # segundos entre spawns

# ----------------- PROYECTILES -----------------
PROJECTILE_SPEED = 8

# ----------------- ROOKS (torres) ----------------------
ROOK_IMAGE_SIZE = (60, 60)
ROOK_STATS = {
    "arena": {
        "vida": 3,
        "daño": 2,
        "rango": 200,
        "velocidad_ataque": 4.0,
        "image": load_img("images/rooks/arena.png",ROOK_IMAGE_SIZE),
        "color": (199, 178, 117),     # Color del proyectil
        "cost": 50,
    },
    "roca": {
        "vida": 14,
        "daño": 4,
        "rango": 200,
        "velocidad_ataque": 4.0,
        "image": load_img("images/rooks/roca.png",ROOK_IMAGE_SIZE),
        "color": (120, 120, 120),
        "cost": 100,
    },
    "fuego": {
        "vida": 16,
        "daño": 8,
        "rango": 200,
        "velocidad_ataque": 4.0,
        "image": load_img("images/rooks/fuego.png",ROOK_IMAGE_SIZE),
        "color": (255, 80, 20),
        "cost": 150,
    },
    "agua": {
        "vida": 16,
        "daño": 8,
        "rango": 200,
        "velocidad_ataque": 4.0,
        "image": load_img("images/rooks/agua.png",ROOK_IMAGE_SIZE),
        "color": (80, 160, 255),
        "cost": 150,
    },
}

# AVATARS (Enemigos)
AVATAR_IMAGE_SIZE = (65, 65)
AVATAR_STATS = {
    "flechador": {
        "vida": 5,
        "daño": 0.2,
        "velocidad": 70 / (12*10),
        "attack_interval": 10.0,
        "color": (200, 220, 255),
        "image": load_img("images/avatars/arquero.png",AVATAR_IMAGE_SIZE),
        "rango": 200,
    },
    "escudero": {
        "vida": 10,
        "daño": 0.3,
        "velocidad": 70 / (10*10),
        "attack_interval": 15.0,
        "image": load_img("images/avatars/escudero.png",AVATAR_IMAGE_SIZE),
        "color": (180, 200, 255),
        "rango": 200,
    },
    "lenador": {
        "vida": 20,
        "daño": 0.9,
        "velocidad": 70 / (13*10),
        "attack_interval": 5.0,
        "image": load_img("images/avatars/leñador.png",AVATAR_IMAGE_SIZE),
        "color": (150, 255, 150),
        "rango": 200,
    },
    "canibal": {
        "vida": 25,
        "daño": 12,
        "velocidad": 70 / (14*10),
        "attack_interval": 3.0,
        "image": load_img("images/avatars/canibal.png",AVATAR_IMAGE_SIZE),
        "color": (255, 150, 150),
        "rango": 200,
    },
}

# ----------------- PROBABILIDADES DE SPAWN -----------------
# Puedes cambiar estos pesos si quieres hacer el juego más o menos difícil.
# La suma no tiene que ser 1, random.choices normaliza internamente.
AVATAR_SPAWN_WEIGHTS = {
    "flechador": 0.35,
    "escudero": 0.30,
    "lenador":  0.20,
    "canibal":  0.15,
}
