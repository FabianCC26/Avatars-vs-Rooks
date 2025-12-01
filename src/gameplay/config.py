import pygame

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

# ======================================================
# ROOKS (torres) — basado en “Resumen de los Rooks”
# ======================================================
# Nota: en tu código interno usas "arena", "roca", "fuego", "agua",
# así que mapeamos:
#   Sand Rook  -> "arena"
#   Rock Rook  -> "roca"
#   Fire Rook  -> "fuego"
#   Water Rook -> "agua"
#
# Ataque = daño
# Resistencia = vida
# Frecuencia de ataque = 4 s para todas las rooks (dato adicional)

ROOK_STATS = {
    "arena": {  # Sand Rook
        "vida": 3,
        "daño": 2,
        "rango": 200,               # píxeles (puedes ajustarlo)
        "velocidad_ataque": 4.0,    # segundos entre disparos
        "color": (210, 180, 140),
        "cost": 50,
    },
    "roca": {  # Rock Rook
        "vida": 14,
        "daño": 4,
        "rango": 200,
        "velocidad_ataque": 4.0,
        "color": (100, 100, 100),
        "cost": 100,
    },
    "fuego": {  # Fire Rook
        "vida": 16,
        "daño": 8,
        "rango": 200,
        "velocidad_ataque": 4.0,
        "color": (255, 80, 0),
        "cost": 150,
    },
    "agua": {  # Water Rook
        "vida": 16,
        "daño": 8,
        "rango": 200,
        "velocidad_ataque": 4.0,
        "color": (0, 120, 255),
        "cost": 150,
    },
}

# ======================================================
# AVATARS — basado en “Resumen de los Avatars”
# ======================================================
# Tabla:
#  Flechador: ataque 2, resis 5,  avanza cada 12 s, ataca cada 10 s
#  Escudero:  ataque 3, resis 10, avanza cada 10 s, ataca cada 15 s
#  Leñador:   ataque 9, resis 20, avanza cada 13 s, ataca cada 5 s (si hay torre)
#  Caníbal:   ataque 12, resis 25, avanza cada 14 s, ataca cada 3 s (si hay torre)
#
# En tu clase Avatar usas:
#   vida      -> resistencia
#   daño      -> poder de ataque
#   velocidad -> píxeles por frame
#
# Tomamos que “avanza cada X segundos” ≈ tarda X s en recorrer UNA casilla.
# Como la casilla vale 70 px y asumimos 60 FPS:
# velocidad(px/frame) = 70 / (60 * X)

AVATAR_STATS = {
    "flechador": {
        "vida": 5,
        "daño": 0.2,
        "velocidad": 70 / (12*10),  # ≈ 0.0972
        "attack_interval": 10.0,
        "color": (200, 220, 255),
        "rango":200,
    },
    "escudero": {
        "vida": 10,
        "daño": 0.3,
        "velocidad": 70 / (10*10),  # ≈ 0.1167
        "attack_interval": 15.0,
        "color": (180, 200, 255),
        "rango":200,
    },
    "lenador": {
        "vida": 20,
        "daño": 0.9,
        "velocidad": 70 / (13*10),  # ≈ 0.0897
        "attack_interval": 5.0,
        "color": (150, 255, 150),
        "rango":200,
    },
    "canibal": {
        "vida": 25,
        "daño": 12,
        "velocidad": 70 / (14*10),  # ≈ 0.0833
        "attack_interval": 3.0,
        "color": (255, 150, 150),
        "rango":200,
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
