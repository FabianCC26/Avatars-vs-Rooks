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


        if self.rango <= config.GRID_COLS:
            self.rango_px = self.rango * config.CELL_W
        else:
            self.rango_px = self.rango  # ya viene en píxeles


    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

        try:
            import config
            y = self.rect.centery
            x1 = self.rect.centerx
            x2 = x1 + self.rango_px
            pygame.draw.line(screen, (0, 255, 0), (x1, y), (x2, y), 2)   # verde = rango
            # círculo en el centro (lock-on cuando está por disparar)
            if hasattr(self, "_debug_lock_on") and self._debug_lock_on:
                pygame.draw.circle(screen, (255, 0, 0), (x1, y), 6)      # rojo = tiene objetivo
        except:
            pass


    # Rook.py (solo cambia atacar y update)
    def atacar(self, avatars, tiempo_actual, projectiles):
        cy_rook = self.rect.centery
        cx_rook = self.rect.centerx

        for avatar in avatars:
            cy_a = avatar.rect.centery
            cx_a = avatar.rect.centerx

            misma_fila = abs(cy_a - cy_rook) <= (config.CELL_H // 2)
            dx = cx_a - cx_rook
            # Si tu rango está en celdas, convierte a px: rango_px = self.rango * config.CELL_W
            rango_px = self.rango * config.CELL_W if self.rango <= config.GRID_COLS else self.rango
            en_rango = 0 <= dx <= rango_px

            if misma_fila and en_rango:
                if (tiempo_actual - self.last_attack_time) >= self.velocidad_ataque:
                    
                    from projectile import Projectile
                    projectiles.append(Projectile(self.rect.right, cy_rook, damage=self.daño))
                    self.last_attack_time = tiempo_actual
                break

    def update(self, tiempo_actual, avatars, projectiles=None):
        self.atacar(avatars, tiempo_actual, projectiles)


    """
    def atacar(self, avatars, tiempo_actual):
       # Ataca al primer avatar dentro de rango.
        for avatar in avatars:
            # Comprobar si está dentro del mismo carril (fila)

            
            if abs(avatar.y - self.y) < 40 and abs(avatar.x - self.x) <= self.rango * 100:
                # Control de tiempo entre ataques
                if tiempo_actual - self.last_attack_time >= self.velocidad_ataque * 1000:
                    avatar.vida -= self.daño
                    self.last_attack_time = tiempo_actual
                break  # Solo ataca a uno a la vez
            """

    def esta_muerto(self):
        return self.vida <= 0
