import pygame
import random
import time
import sys

import config
from rooks import Rook
from avatars import Avatar
from projectile import Projectile

class Game:
    def __init__(self):
        pygame.init()

        # Constantes desde config
        self.ANCHO = config.WINDOW_WIDTH
        self.ALTO = config.WINDOW_HEIGHT
        self.FILAS = config.GRID_ROWS
        self.COLUMNAS = config.GRID_COLS
        self.CELL_W = config.WINDOW_WIDTH // config.GRID_COLS
        self.CELL_H = config.WINDOW_HEIGHT // config.GRID_ROWS

        #Base de la ventana
        self.screen = pygame.display.set_mode((self.ANCHO, self.ALTO))
        pygame.display.set_caption("Rooks vs Avatars - 9x6")
        self.font = pygame.font.Font(None, 28)
        self.clock = pygame.time.Clock()

        # Estado del juego
        self.coins = config.INITIAL_COINS
        self.rooks = []
        self.avatars = []
        self.projectiles = []
        self.last_spawn = time.time()
        self.rook_selected = "arena"
        self.running = True
        self.game_over = False
        
        self.game_over_handled = False
        self.final_coins = 0

   
    def draw_text(self, txt, pos, color=config.TEXT_COLOR, center=False):
        surf = self.font.render(txt, True, color)
        rect = surf.get_rect()
        if center:
            rect.center = pos
        else:
            rect.topleft = pos
        self.screen.blit(surf, rect)

    #Dibuja la matriz principal del juego:
    def draw_grid(self):
        for r in range(self.FILAS):
            for c in range(self.COLUMNAS):
                rect = pygame.Rect(c * self.CELL_W, r * self.CELL_H, self.CELL_W, self.CELL_H)
                if c == 0:
                    pygame.draw.rect(self.screen, config.LEFT_ZONE_COLOR, rect)
                else:
                    pygame.draw.rect(self.screen, config.GRID_COLOR, rect, 1)


    def grid_from_mouse(self, pos):
        x, y = pos
        col = max(0, min(self.COLUMNAS - 1, x // self.CELL_W))
        row = max(0, min(self.FILAS - 1, y // self.CELL_H))
        return col, row

    def center_cell(self, col, row, sprite_w, sprite_h):
        gx = col * self.CELL_W + (self.CELL_W // 2 - sprite_w // 2)
        gy = row * self.CELL_H + (self.CELL_H // 2 - sprite_h // 2)
        return int(gx), int(gy)


    #Lógica de juego
    def spawn_avatar(self):
        row = random.randint(0, self.FILAS - 1)
        y = row * self.CELL_H + self.CELL_H // 2
        tipo = random.choice(list(config.AVATAR_STATS.keys()))
        self.avatars.append(Avatar(self.ANCHO + 10, y, tipo))

    def handle_projectile_collisions(self):
        for p in self.projectiles[:]:
            for a in self.avatars[:]:
                if p.rect.colliderect(a.rect):
                    a.vida -= p.damage
                    if p in self.projectiles:
                        self.projectiles.remove(p)
                    if a.vida <= 0 and a in self.avatars:
                        self.avatars.remove(a)
                        self.coins += config.COINS_PER_KILL
                    break


    def reset(self):
        self.coins = config.INITIAL_COINS
        self.rooks.clear()
        self.avatars.clear()
        self.projectiles.clear()
        self.last_spawn = time.time()
        self.game_over = False
        self.game_over_handled = False
        self.final_coins = 0

    # Events:

    def handle_events(self):
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                self.running = False

            elif evt.type == pygame.MOUSEBUTTONDOWN and evt.button == 1 and not self.game_over:
                col, row = self.grid_from_mouse(pygame.mouse.get_pos())
                if col > 0:
                    gx, gy = self.center_cell(col, row, 50, 50)  # Rook topleft “centrado”
                    if not any((r.x == gx and r.y == gy) for r in self.rooks):
                        cost = config.ROOK_STATS[self.rook_selected]["cost"]
                        if self.coins >= cost:
                            self.rooks.append(Rook(gx, gy, self.rook_selected))
                            self.coins -= cost

            elif evt.type == pygame.KEYDOWN:

                # Menú de torres:
                if evt.key == pygame.K_1:
                    self.rook_selected = "arena"
                elif evt.key == pygame.K_2:
                    self.rook_selected = "roca"
                elif evt.key == pygame.K_3:
                    self.rook_selected = "fuego"
                elif evt.key == pygame.K_4:
                    self.rook_selected = "agua"

                # Reinicio
                elif evt.key == pygame.K_r:
                    self.reset()

    def update_and_draw_game(self):

        # Spawneo de avatars:
        if not self.game_over and (time.time() - self.last_spawn) >= config.SPAWN_INTERVAL:
            self.spawn_avatar()
            self.last_spawn = time.time()

        # Rooks
        now = time.time()
        for r in self.rooks[:]:
            r.update(now, self.avatars, self.projectiles)
            if r.vida > 0:
                r.draw(self.screen)
            else:
                self.rooks.remove(r)

        # Proyectiles
        for p in self.projectiles[:]:
            p.update()
            # Debug puntito rojo
            pygame.draw.circle(self.screen, (255, 0, 0), p.rect.center, 2)
            p.draw(self.screen)
            if p.rect.left > self.ANCHO + 50:
                self.projectiles.remove(p)

        # Avatares
        now = time.time()
        for a in self.avatars[:]:
            a.update(now, self.rooks)
            # combate cuerpo a cuerpo (si aplica tu Avatar/Rook)
            for r in self.rooks[:]:
                if a.can_attack(r):
                    a.attack(r)
                if r.vida <= 0 and r in self.rooks:
                    self.rooks.remove(r)

            # condición de derrota
            if a.rect.left < self.CELL_W:
                self.game_over = True

            # muerte del avatar
            if a.vida <= 0:
                if a in self.avatars:
                    self.avatars.remove(a)
                self.coins += config.COINS_PER_KILL
            else:
                a.draw(self.screen)

        # Colisiones proyectil-avatar
        self.handle_projectile_collisions()

        self.draw_grid()
        self.draw_text(f"Monedas: {self.coins}", (10, 6))
        self.draw_text(f"Rook: {self.rook_selected}", (10, 34))
        self.draw_text("1:Arena 2:Roca 3:Fuego 4:Agua  R:Reiniciar", (10, 60), (180, 180, 255))

    # ===== Pantalla de Game Over (solo texto) =====
    def draw_game_over(self):
        if not self.game_over_handled:
            self.final_coins = self.coins
            self.rooks.clear()
            self.avatars.clear()
            self.projectiles.clear()
            self.game_over_handled = True

        self.screen.fill(config.BACKGROUND_COLOR)
        self.draw_text("¡Has perdido!", (self.ANCHO // 2, self.ALTO // 2 - 20), (255, 60, 60), center=True)
        self.draw_text(f"Monedas recolectadas: {self.final_coins}", (self.ANCHO // 2, self.ALTO // 2 + 20), config.TEXT_COLOR, center=True)
        self.draw_text("Presiona R para reiniciar o ESC para salir", (self.ANCHO // 2, self.ALTO // 2 + 60), (180, 180, 255), center=True)

        # ESC para salir:
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.running = False

    # Bucle principal:

    def run(self):
        while self.running:
            self.screen.fill(config.BACKGROUND_COLOR)
            self.handle_events()

            # Pantalla de derrota (limpia y muestra solo texto)
            if self.game_over:
                self.draw_game_over()
                pygame.display.flip()
                self.clock.tick(60)
                continue  # no dibujar ni actualizar nada más

            # Juego normal
            self.update_and_draw_game()

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    Game().run()
