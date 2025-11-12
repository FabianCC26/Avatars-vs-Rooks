import pygame
import config

class Rook:
    def __init__(self, x, y, tipo):
        self.tipo = tipo
        stats = config.ROOK_STATS[tipo]
        self.x = x
        self.y = y
        self.vida = stats["vida"]
        self.daño = stats["daño"]
        self.rango = stats["rango"]
        self.velocidad_ataque = stats["velocidad_ataque"]
        self.color = stats["color"]
        self.cost = stats["cost"]
        self.last_attack_time = 0  # Tiempo del último ataque

        self.size = 50
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def atacar(self, avatars, tiempo_actual):
        """Ataca al primer avatar dentro de rango."""
        for avatar in avatars:
            # Comprobar si está dentro del mismo carril (fila)
            if abs(avatar.y - self.y) < 40 and abs(avatar.x - self.x) <= self.rango * 100:
                # Control de tiempo entre ataques
                if tiempo_actual - self.last_attack_time >= self.velocidad_ataque * 1000:
                    avatar.vida -= self.daño
                    self.last_attack_time = tiempo_actual
                break  # Solo ataca a uno a la vez

    def update(self, tiempo_actual, avatars, projectiles=None):
        """Actualiza comportamiento del rook (ataque, estado, etc)."""
        self.atacar(avatars, tiempo_actual)

    def esta_muerto(self):
        return self.vida <= 0
