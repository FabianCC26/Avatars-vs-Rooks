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
# De la tabla:
# Sand:   Attack 2, Cost 50,  Resistance 3
# Rock:   Attack 4, Cost 100, Resistance 14
# Fire:   Attack 8, Cost 150, Resistance 16
# Water:  Attack 8, Cost 150, Resistance 16

ROOK_IMAGE_SIZE = (60, 60)
ROOK_STATS = {
    "arena": {
        "vida": 3,                   # Resistance
        "daño": 1,                   # Attack
        "rango": 200,
        "velocidad_ataque": 4.0,     # puedes ajustar luego si quieres otro ritmo
        "image": load_img("images/rooks/arena.png", ROOK_IMAGE_SIZE),
        "color": (199, 178, 117),    # Color del proyectil
        "cost": 50,
    },
    "roca": {
        "vida": 14,
        "daño": 2,
        "rango": 200,
        "velocidad_ataque": 4.0,
        "image": load_img("images/rooks/roca.png", ROOK_IMAGE_SIZE),
        "color": (120, 120, 120),
        "cost": 100,
    },
    "fuego": {
        "vida": 16,
        "daño": 4,
        "rango": 200,
        "velocidad_ataque": 4.0,
        "image": load_img("images/rooks/fuego.png", ROOK_IMAGE_SIZE),
        "color": (255, 80, 20),
        "cost": 150,
    },
    "agua": {
        "vida": 14,
        "daño": 6,
        "rango": 200,
        "velocidad_ataque": 4.0,
        "image": load_img("images/rooks/agua.png", ROOK_IMAGE_SIZE),
        "color": (80, 160, 255),
        "cost": 150,
    },
}

# ----------------- AVATARS (Enemigos) -----------------
# Tabla:
# Archer     -> Power Attack 2,  Resistance 5,  Speed 12, DPS 10
# Squire     -> Power Attack 3,  Resistance 10, Speed 10, DPS 15
# Lummberjack-> Power Attack 9,  Resistance 20, Speed 13, DPS 5
# Canibbal   -> Power Attack 12, Resistance 25, Speed 14, DPS 3
#
# Mapeo:
#   vida   = Resistance
#   daño   = Power Attack
#   velocidad ~ 0.05 * Speed  (mantiene magnitud parecida a la que ya usabas)
#   attack_interval = daño / DPS

AVATAR_IMAGE_SIZE = (65, 65)
AVATAR_STATS = {
    "flechador": {  # Archer
        "vida": 2,
        "daño": 0.5,
        "velocidad": 0.05 * 12,     # Speed 12
        "attack_interval": 2 ,  # DPS 10
        "color": (200, 220, 255),
        "image": load_img("images/avatars/arquero.png", AVATAR_IMAGE_SIZE),
        "rango": 200,
    },
    "escudero": {   # Squire
        "vida": 6,
        "daño": 0.7,
        "velocidad": 0.05 * 10,     # Speed 10
        "attack_interval": 3,  # DPS 15
        "image": load_img("images/avatars/escudero.png", AVATAR_IMAGE_SIZE),
        "color": (180, 200, 255),
        "rango": 200,
    },
    "lenador": {    # Lumberjack
        "vida": 3,
        "daño": 1,
        "velocidad": 0.05 * 13,     # Speed 13
        "attack_interval": 4,   # DPS 5
        "image": load_img("images/avatars/leñador.png", AVATAR_IMAGE_SIZE),
        "color": (150, 255, 150),
        "rango": 200,
    },
    "canibal": {    # Cannibal
        "vida": 2,
        "daño": 1.2,
        "velocidad": 0.05 * 14,     # Speed 14
        "attack_interval": 6,  # DPS 3
        "image": load_img("images/avatars/canibal.png", AVATAR_IMAGE_SIZE),
        "color": (255, 150, 150),
        "rango": 200,
    },
}

# ----------------- PROBABILIDADES DE SPAWN -----------------
AVATAR_SPAWN_WEIGHTS = {
    "flechador": 0.40,
    "escudero": 0.30,
    "lenador":  0.20,
    "canibal":  0.15,
}
