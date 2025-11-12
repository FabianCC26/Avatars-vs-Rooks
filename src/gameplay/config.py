# ============================
# CONFIGURACIÓN GENERAL DEL JUEGO
# ============================

#ANCHO = 900
#ALTO = 600

# Dimensiones de la ventana
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

# Tamaño de cada celda de la cuadrícula
CELL_SIZE = 100
CELL_W = 60
CELL_H = 60

# Dimensiones de la matriz
GRID_COLS = 9
GRID_ROWS = 6

# Color del fondo
BACKGROUND_COLOR = (230, 230, 230)
GRID_COLOR = (200, 200, 200)
LEFT_ZONE_COLOR = (180, 220, 180)  # color diferente para la primera columna
TEXT_COLOR = (0,0,0)

# Monedas iniciales
INITIAL_COINS = 150

# Tiempo entre aparición de avatares (en segundos)
SPAWN_INTERVAL = 10

# Recompensa por eliminar un avatar
COINS_PER_KILL = 75

# ============================
# STATS DE LOS ROOKS (DEFENSORES)
# ============================

ROOK_ATACK_INTERVAL = 10

ROOK_STATS = {
    "arena": {
        "vida": 100,
        "daño": 15,
        "rango": 1,
        "velocidad_ataque": 1.0,
        "cost": 50,
        "color": (194, 178, 128)
    },
    "roca": {
        "vida": 200,
        "daño": 25,
        "rango": 1,
        "velocidad_ataque": 1.2,
        "cost": 100,
        "color": (120, 120, 120)
    },
    "fuego": {
        "vida": 80,
        "daño": 40,
        "rango": 3,
        "velocidad_ataque": 0.6,
        "cost": 150,
        "color": (255, 80, 0)
    },
    "agua": {
        "vida": 100,
        "daño": 20,
        "rango": 2,
        "velocidad_ataque": 0.8,
        "cost": 150,
        "color": (0, 120, 255)
    }
}

# ============================
# STATS DE LOS AVATARES (ENEMIGOS)
# ============================

AVATAR_STATS = {
    "Avatar_Flechador": {
        "vida": 5,                 # Resistencia (puntos)
        "velocidad": 12,           # Velocidad de avance (cada X seg)
        "daño": 2,                 # Poder de ataque
        "frecuencia_ataque": 10,   # Cada X seg
        "tipo": "rango",
        "color": (255, 255, 51)
    },
    "Avatar_Escudero": {
        "vida": 10,
        "velocidad": 10,
        "daño": 3,
        "frecuencia_ataque": 15,
        "tipo": "melee",
        "color": (64, 64, 64)
    },
    "Avatar_Leñador": {
        "vida": 20,
        "velocidad": 13,
        "daño": 9,
        "frecuencia_ataque": 5,  # si hay torre enfrente
        "tipo": "melee",
        "color": (102, 0, 0)
    },
    "Avatar_Canibal": {
        "vida": 25,
        "velocidad": 14,
        "daño": 12,
        "frecuencia_ataque": 3,  # si hay torre enfrente
        "tipo": "melee",
        "color": (204, 0, 102)
    }
}