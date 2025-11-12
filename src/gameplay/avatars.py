import pygame
import config

class Avatar:
    def __init__(self, x, y, tipo):
        stats = config.AVATAR_STATS[tipo]

        self.avatar_type = tipo
        self.vida = stats["vida"]
        self.velocidad = stats["velocidad"]
        self.daño = stats["daño"]
        self.frecuencia_ataque = stats["frecuencia_ataque"]
        self.tipo = stats["tipo"]
        self.color = stats["color"]

        self.last_attack_time = 0

        # Crear el rectángulo de colisión y posición inicial
        self.rect = pygame.Rect(x, y, config.CELL_W, config.CELL_H)

    def move(self):
        """Movimiento hacia la izquierda constante (enemigos que avanzan)."""
        self.rect.x -= 1  # velocidad base
        # Puedes usar self.velocidad si querés un movimiento más rápido
        # self.rect.x -= self.velocidad * 0.1

    def can_attack(self, rook):
        """Determina si puede atacar a una torre cercana."""
        return self.rect.colliderect(rook.rect)

    def attack(self, rook, tiempo_actual):
        """Ataca una torre si está lista para hacerlo."""
        if tiempo_actual - self.last_attack_time >= self.frecuencia_ataque * 100:
            rook.vida -= self.daño
            self.last_attack_time = tiempo_actual

    def update(self, tiempo_actual, rooks):
        """Actualiza movimiento y combate."""
        if not any(self.can_attack(r) for r in rooks):
            self.move()
        else:
            for r in rooks:
                if self.can_attack(r):
                    self.attack(r, tiempo_actual)
                    break