import pygame
from src.gameplay import config

class Projectile:
    def __init__(self, x, y, damage, direction,
                 color=(255, 255, 255), owner="rook", speed=None):
        """
        direction:
            "up"   -> se mueve hacia arriba
            "down" -> se mueve hacia abajo
        owner:
            "rook"   -> hiere avatars
            "avatar" -> hiere rooks
        """
        self.x = float(x)
        self.y = float(y)

        self.damage = damage
        self.direction = direction
        self.color = color
        self.owner = owner

        self.speed = speed if speed is not None else config.PROJECTILE_SPEED

        self.size = 12

        self.rect = pygame.Rect(
            int(self.x) - self.size // 2,
            int(self.y) - self.size // 2,
            self.size,
            self.size,
        )

    def update(self):
        if self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed

        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

    def draw(self, screen):
        # blanco brillante para que se vea bien
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x), int(self.y)),
            self.size // 2,
        )