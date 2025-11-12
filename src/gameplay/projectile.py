
import pygame
import config


class Projectile:
    def __init__(self, x, y, damage=1, speed=8, size=10, color=(255, 255, 0)):
        self.damage = damage
        self.speed = speed
        self.color = (0,0,0)
        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.center = (x, y)

    # (compatibilidad si en el main usas p.x)
    def x(self):
        return self.rect.x

    def update(self):
        self.rect.x += self.speed

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)
