# entities/projectile.py
import pygame

class Projectile:
    def __init__(self, x, y, damage, color=(255,255,255)):
        self.x = x
        self.y = y
        self.speed = 6
        self.damage = damage
        self.color = color
        self.width = 10
        self.height = 6
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def update(self):
        self.x += self.speed
        self.rect.x = int(self.x)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
