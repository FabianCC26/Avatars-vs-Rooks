import os
import sys

# ---- Arreglo de rutas para poder usar 'src' como paquete de nivel superior ----
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.append(ROOT)

import pygame

from src.gameplay import config
from src.gameplay.projectile import Projectile   # <-- FALTA ESTO

class Rook:
    def __init__(self, x, y, tipo: str):
        self.tipo = tipo
        stats = config.ROOK_STATS[tipo]

        self.x = x
        self.y = y
        self.vida = stats["vida"]
        self.daño = stats["daño"]
        self.rango = stats["rango"]
        self.velocidad_ataque = stats["velocidad_ataque"]
        self.image = stats["image"]
        self.color = stats["color"] 
        self.cost = stats["cost"]

        self.last_attack_time = 0.0

        self.size = 50
        self.rect = pygame.Rect(
            self.x - self.size // 2,
            self.y - self.size // 2,
            self.size,
            self.size,
        )

    def update(self, now: float, avatars, projectiles: list):
        # cooldown
        if now - self.last_attack_time < self.velocidad_ataque:
            return

        objetivo = None
        for a in avatars:
            # misma columna
            misma_columna = abs(a.rect.centerx - self.rect.centerx) <= self.rect.width // 2
            # avatar DEBAJO de la torre
            dy = a.rect.centery - self.rect.centery
            en_rango = 0 < dy <= self.rango

            if misma_columna and en_rango:
                objetivo = a
                break

        if objetivo is not None:
            proj = Projectile(
                x=self.rect.centerx,
                y=self.rect.centery,
                damage=self.daño,
                direction="down",      # ↓↓↓
                color=self.color,
                owner="rook",
            )
            projectiles.append(proj)
            self.last_attack_time = now

    def draw(self, screen):
        screen.blit(self.image, self.rect)


