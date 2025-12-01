import os
import sys

# ---- Arreglo de rutas para poder usar 'src' como paquete de nivel superior ----
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.append(ROOT)

import pygame

from src.gameplay import config
from src.gameplay.projectile import Projectile


class Avatar:
    def __init__(self, x, y, tipo: str):
        self.tipo = tipo
        stats = config.AVATAR_STATS[tipo]

        self.x = float(x)
        self.y = float(y)
        self.vida = stats["vida"]
        self.velocidad = stats["velocidad"]
        self.daño = stats["daño"]
        self.attack_interval = stats["attack_interval"]
        self.rango = stats["rango"]          # rango en píxeles
        self.color = stats["color"]

        self.size = 50
        self.rect = pygame.Rect(
            int(self.x) - self.size // 2,
            int(self.y) - self.size // 2,
            self.size,
            self.size,
        )

        self.last_attack_time = 0.0

        # Solo lo usamos para resaltar el cuerpo si tiene objetivo
        self.has_target_in_range = False

    def update(self, now: float, rooks, projectiles):
        # ----------------- MOVIMIENTO -----------------
        # Intentar mover hacia arriba, pero detenerse si en la siguiente
        # posición chocaría con un rook (se queda "en frente").
        next_y = self.y - self.velocidad
        next_rect = self.rect.copy()
        next_rect.centery = int(next_y)

        if not any(next_rect.colliderect(r.rect) for r in rooks):
            self.y = next_y

        # Actualizamos el rect con la posición final
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

        # ----------------- BÚSQUEDA DE OBJETIVO -----------------
        self.has_target_in_range = False
        posibles = []

        for r in rooks:
            # Misma columna (aprox)
            if abs(r.rect.centerx - self.rect.centerx) <= r.rect.width // 2:
                dy = self.rect.centery - r.rect.centery  # rook arriba -> dy positivo
                if 0 < dy <= self.rango:
                    posibles.append((r, dy))

        if not posibles:
            return

        # Tomar el rook MÁS CERCANO hacia arriba
        target, dy_target = min(posibles, key=lambda pair: pair[1])
        self.has_target_in_range = True

        # ----------------- DISPARO A DISTANCIA -----------------
        if now - self.last_attack_time >= self.attack_interval:
            proj = Projectile(
                x=self.rect.centerx,
                y=self.rect.centery,
                damage=self.daño,
                direction="up",        # balas hacia arriba
                color=self.color,
                owner="avatar",
            )
            projectiles.append(proj)
            self.last_attack_time = now

    # Estas ya no se usan, pero las dejo por compatibilidad
    def can_attack(self, rook) -> bool:
        return self.rect.colliderect(rook.rect)

    def attack_rook(self, rook):
        rook.vida -= self.daño

    def draw(self, screen):
        # Si tiene objetivo en rango, lo pinto un poco más brillante
        if self.has_target_in_range:
            body_color = (
                min(self.color[0] + 40, 255),
                min(self.color[1] + 40, 255),
                min(self.color[2] + 40, 255),
            )
        else:
            body_color = self.color

        
        pygame.draw.rect(screen, body_color, self.rect, border_radius=6)
