import pygame
import random
import time
import sys

import config
from rooks import Rook
from avatars import Avatar
from projectile import Projectile

pygame.init()

ANCHO = config.WINDOW_WIDTH
ALTO = config.WINDOW_HEIGHT
FILAS = config.GRID_ROWS
COLUMNAS = config.GRID_COLS
CELL_W = config.WINDOW_WIDTH // config.GRID_COLS
CELL_H = config.WINDOW_HEIGHT // config.GRID_ROWS

screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Rooks vs Avatars - 9x6")

font = pygame.font.Font(None, 28)
clock = pygame.time.Clock()

# Estado del juego
coins = config.INITIAL_COINS
rooks = []
avatars = []
projectiles = []
last_spawn = time.time()
rook_selected = "arena"
running = True
game_over = False


def draw_text(txt, pos, color=config.TEXT_COLOR):
    surf = font.render(txt, True, color)
    screen.blit(surf, pos)


def draw_grid():
    for r in range(FILAS):
        for c in range(COLUMNAS):
            rect = pygame.Rect(c * CELL_W, r * CELL_H, CELL_W, CELL_H)
            if c == 0:
                pygame.draw.rect(screen, config.LEFT_ZONE_COLOR, rect)
            else:
                pygame.draw.rect(screen, config.GRID_COLOR, rect, 1)


def grid_from_mouse(pos):
    x, y = pos
    col = max(0, min(COLUMNAS - 1, x // CELL_W))
    row = max(0, min(FILAS - 1, y // CELL_H))
    return col, row


def center_cell(col, row, sprite_w, sprite_h):
    gx = col * CELL_W + (CELL_W // 2 - sprite_w // 2)
    gy = row * CELL_H + (CELL_H // 2 - sprite_h // 2)
    return int(gx), int(gy)


def spawn_avatar():
    row = random.randint(0, FILAS - 1)
    y = row * CELL_H + CELL_H // 2
    tipo = random.choice(list(config.AVATAR_STATS.keys()))
    avatars.append(Avatar(ANCHO + 10, y, tipo))
    


def handle_projectile_collisions():
    global coins
    for p in projectiles[:]:
        for a in avatars[:]:
            if p.rect.colliderect(a.rect):
                a.vida -= p.damage
                projectiles.remove(p)
                if a.vida <= 0:
                    avatars.remove(a)
                    coins += config.COINS_PER_KILL
                break


# Loop principal
while running:
    screen.fill(config.BACKGROUND_COLOR)

    for evt in pygame.event.get():

        if evt.type == pygame.QUIT:
            running = False

        elif evt.type == pygame.MOUSEBUTTONDOWN and evt.button == 1 and not game_over:
            col, row = grid_from_mouse(pygame.mouse.get_pos())
            if col > 0:  # No en la columna de derrota
                gx, gy = center_cell(col, row, 50, 50)
                if not any((r.x == gx and r.y == gy) for r in rooks):
                    cost = config.ROOK_STATS[rook_selected]["cost"]
                    if coins >= cost:
                        rooks.append(Rook(gx, gy, rook_selected))
                        coins -= cost

        elif evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_1:
                rook_selected = "arena"
            elif evt.key == pygame.K_2:
                rook_selected = "roca"
            elif evt.key == pygame.K_3:
                rook_selected = "fuego"
            elif evt.key == pygame.K_4:
                rook_selected = "agua"

            elif evt.key == pygame.K_r:
                coins = config.INITIAL_COINS
                rooks.clear()
                avatars.clear()
                projectiles.clear()
                last_spawn = time.time()
                game_over = False

    # Spawneo de avatars
    if not game_over and (time.time() - last_spawn) >= config.SPAWN_INTERVAL:
        spawn_avatar()
        last_spawn = time.time()

    if not game_over:    
        now = time.time()
        for r in rooks[:]:
            r.update(now, avatars, projectiles)
            if r.vida > 0:
                r.draw(screen)
            else:
                rooks.remove(r)

        for p in projectiles[:]:
            p.update()
            pygame.draw.circle(screen, (255, 0, 0), p.rect.center, 2)
            p.draw(screen)
            if p.rect.left > ANCHO + 50:
                projectiles.remove(p)

        now = time.time()
        
        for a in avatars[:]:
            a.update(now, rooks)
            for r in rooks[:]:
                if a.can_attack(r):
                    a.attack(r)
                if r.vida <= 0 and r in rooks:
                    rooks.remove(r)
            if a.rect.left < CELL_W:
                game_over = True
            if a.vida <= 0:
                avatars.remove(a)
                coins += config.COINS_PER_KILL
            else:
                a.draw(screen)                   


        handle_projectile_collisions()

        draw_grid()
        draw_text(f"Monedas: {coins}", (10, 6))
        draw_text(f"Rook: {rook_selected}", (10, 34))
        draw_text("1:Arena 2:Roca 3:Fuego 4:Agua  R:Reiniciar", (10, 60), (180, 180, 255))

    if game_over:
        draw_text("¡Has perdido! Presiona R para reiniciar o ESC para salir", (ANCHO // 4, ALTO // 2), (255, 60, 60))
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            running = False

    pygame.display.flip()
    clock.tick(60)