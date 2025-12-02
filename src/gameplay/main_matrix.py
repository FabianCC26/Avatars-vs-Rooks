import os
import sys

# ---- Arreglo de rutas para poder usar 'src' como paquete de nivel superior ----
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.append(ROOT)

import pygame
import random
import time

from src.gameplay import config
from src.gameplay.rooks import Rook
from src.gameplay.avatars import Avatar
from src.gameplay.projectile import Projectile
from src.utils.joystick_reader import JoystickReader


class MatrixGame:

    COIN_SPAWN_INTERVAL = 6.0  # segundos entre intentos de generar moneda

    def __init__(self, avatar_num):
        pygame.init()

        # ------------------ Ventana y matriz ------------------
        self.WINDOW_W = 1280
        self.WINDOW_H = 720
        self.ANCHO = self.WINDOW_W
        self.ALTO = self.WINDOW_H

        # Grid
        self.FILAS = config.GRID_ROWS
        self.COLUMNAS = config.GRID_COLS

        self.CELL_W = 70
        self.CELL_H = 70

        # Tamaño real de la matriz
        self.MATRIX_W = self.COLUMNAS * self.CELL_W
        self.MATRIX_H = self.FILAS * self.CELL_H

        # Offset para centrar la matriz dentro de la ventana
        self.offset_x = (self.WINDOW_W - self.MATRIX_W) // 2
        self.offset_y = (self.WINDOW_H - self.MATRIX_H) // 2

        # Crear ventana
        self.screen = pygame.display.set_mode((self.WINDOW_W, self.WINDOW_H))
        pygame.display.set_caption("Rooks vs Avatars")

        # ----------- FONDO COMPLETO DE LA VENTANA -----------
        bg_path = os.path.join(ROOT, "src", "assets", "images", "matrix_bg.PNG")
        self.full_bg = pygame.image.load(bg_path).convert()
        self.full_bg = pygame.transform.scale(self.full_bg, (self.WINDOW_W, self.WINDOW_H))

        # Fuente y clock
        self.font = pygame.font.Font(None, 28)
        self.clock = pygame.time.Clock()

        # Estado del juego
        self.coins = config.INITIAL_COINS
        self.rooks = []
        self.avatars = []
        self.projectiles = []
        self.last_spawn = time.time()
        self.rook_types = ["arena", "roca", "fuego", "agua"]
        self.rook_selected = self.rook_types[0]  # "arena"
        self.running = True
        self.game_over = False

        # ---- TIMER DE LA PARTIDA ----
        self.start_time = time.time()
        self.elapsed_time = 0  # segundos acumulados (se congela al perder)

        # ---- MONEDAS EN LA MATRIZ ----
        self.grid_coins = []
        self.last_coin_spawn = time.time()

        # ---- JOYSTICK ----
        self.cursor_col = 0
        self.cursor_row = 0
        self.joystick = JoystickReader(port="COM6")
        self.JOY_MOVE_INTERVAL = 0.15
        self.last_joy_dir = "CENTER"
        self.last_joy_move_time = 0.0
        self.last_joy_button = 1  # 1 = suelto, 0 = presionado

        # ---- LÍMITE DE AVATARS ----
        self.MAX_AVATARS = avatar_num          # número máximo de avatars a generar
        self.spawned_avatars = 0      # contador de avatars generados
        self.won = False              # True = victoria, False = derrota
        self.continue_game = False    # se setea SOLO según win/lose

        # ---- BOTÓN DE FINAL DE PARTIDA (MENÚ) ----
        base_y = self.WINDOW_H // 2
        self.button_menu_rect = pygame.Rect(600, base_y + 180, 260, 40)

    # ---------------------- Helpers de dibujo ----------------------

    def draw_text(self, txt, pos, color=config.TEXT_COLOR, line_spacing=4):
        x, y = pos
        for line in txt.split("\n"):
            surf = self.font.render(line, True, color)
            self.screen.blit(surf, (x, y))
            y += surf.get_height() + line_spacing

    def draw_grid(self):
        for r in range(self.FILAS):
            for c in range(self.COLUMNAS):
                rect = pygame.Rect(
                    self.offset_x + c * self.CELL_W,
                    self.offset_y + r * self.CELL_H,
                    self.CELL_W,
                    self.CELL_H,
                )
                pygame.draw.rect(self.screen, config.GRID_COLOR, rect, 1)

    def draw_coins_on_grid(self):
        for coin in self.grid_coins:
            c = coin["col"]
            r = coin["row"]
            value = coin["value"]

            center_x = self.offset_x + c * self.CELL_W + self.CELL_W // 2
            center_y = self.offset_y + r * self.CELL_H + self.CELL_H // 2

            pygame.draw.circle(self.screen, (255, 215, 0), (center_x, center_y), 15)
            txt = self.font.render(str(value), True, (0, 0, 0))
            rect = txt.get_rect(center=(center_x, center_y))
            self.screen.blit(txt, rect)

    def draw_cell_cursor(self):
        col = self.cursor_col
        row = self.cursor_row

        rect = pygame.Rect(
            self.offset_x + col * self.CELL_W,
            self.offset_y + row * self.CELL_H,
            self.CELL_W,
            self.CELL_H
        )
        pygame.draw.rect(self.screen, (255, 255, 0), rect, 4)

    def draw_button(self, rect, text):
        pygame.draw.rect(self.screen, (200, 200, 200), rect)      # fondo
        pygame.draw.rect(self.screen, (50, 50, 50), rect, 2)      # borde
        txt_surf = self.font.render(text, True, (0, 0, 0))
        txt_rect = txt_surf.get_rect(center=rect.center)
        self.screen.blit(txt_surf, txt_rect)

    # ---------------------- Conversión mouse/grid ----------------------

    def grid_from_mouse(self, pos):
        x, y = pos

        rel_x = x - self.offset_x
        rel_y = y - self.offset_y

        if rel_x < 0 or rel_y < 0 or rel_x >= self.MATRIX_W or rel_y >= self.MATRIX_H:
            return None, None

        col = max(0, min(self.COLUMNAS - 1, rel_x // self.CELL_W))
        row = max(0, min(self.FILAS - 1, rel_y // self.CELL_H))
        return col, row

    def center_cell(self, col, row, sprite_w, sprite_h):
        gx = self.offset_x + col * self.CELL_W + self.CELL_W // 2
        gy = self.offset_y + row * self.CELL_H + self.CELL_H // 2
        return int(gx), int(gy)

    # ---------------------- Lógica de monedas ----------------------

    def spawn_coin(self):
        all_cells = [(c, r) for r in range(self.FILAS) for c in range(self.COLUMNAS)]

        occupied = set()
        for r in self.rooks:
            col, row = self.grid_from_mouse((r.rect.centerx, r.rect.centery))
            if col is not None and row is not None:
                occupied.add((col, row))

        for coin in self.grid_coins:
            occupied.add((coin["col"], coin["row"]))

        free_cells = [cell for cell in all_cells if cell not in occupied]
        if not free_cells:
            return

        col, row = random.choice(free_cells)
        value = random.choice([25, 50, 75])

        self.grid_coins.append({"col": col, "row": row, "value": value})

    # ---------------------- Lógica de juego ----------------------

    def spawn_avatar(self):
        # Genera un avatar SOLO si no hemos llegado al máximo.
        if self.spawned_avatars >= self.MAX_AVATARS:
            return

        col = random.randint(0, self.COLUMNAS - 1)

        x = self.offset_x + col * self.CELL_W + self.CELL_W // 2
        y = self.offset_y + self.MATRIX_H + 10

        tipos = list(config.AVATAR_STATS.keys())
        pesos = [config.AVATAR_SPAWN_WEIGHTS[t] for t in tipos]

        tipo = random.choices(tipos, weights=pesos, k=1)[0]

        self.avatars.append(Avatar(x, y, tipo))
        self.spawned_avatars += 1

    def handle_projectile_collisions(self):
        for p in self.projectiles[:]:
            hit_something = False

            if getattr(p, "owner", None) == "rook":
                for a in self.avatars[:]:
                    if p.rect.colliderect(a.rect):
                        a.vida -= p.damage
                        hit_something = True
                        if a.vida <= 0:
                            self.avatars.remove(a)
                            self.coins += config.COINS_PER_KILL
                        break

            elif getattr(p, "owner", None) == "avatar":
                for r in self.rooks[:]:
                    if p.rect.colliderect(r.rect):
                        r.vida -= p.damage
                        hit_something = True
                        if r.vida <= 0 and r in self.rooks:
                            self.rooks.remove(r)
                        break

            if hit_something and p in self.projectiles:
                self.projectiles.remove(p)

    def reset_game(self):
        self.coins = config.INITIAL_COINS
        self.rooks.clear()
        self.avatars.clear()
        self.projectiles.clear()
        self.grid_coins.clear()
        self.last_spawn = time.time()
        self.last_coin_spawn = time.time()
        self.game_over = False
        self.start_time = time.time()
        self.elapsed_time = 0  # reset del timer

        # Reset de límite de avatars y victoria
        self.spawned_avatars = 0
        self.won = False
        self.continue_game = False   # al reiniciar, por defecto False

    # ---------------------- Acción sobre una celda (moneda/rook) ----------------------

    def handle_cell_action(self, col, row):
        if col is None or row is None:
            return

        # Si hay una moneda en la celda
        for coin in self.grid_coins[:]:
            if coin["col"] == col and coin["row"] == row:
                self.coins += coin["value"]
                self.grid_coins.remove(coin)
                return  # ya hicimos acción

        # Si no hay moneda, colocar un rook
        gx, gy = self.center_cell(col, row, 70, 70)

        # Si ya hay un rook en la celda, no hace nada
        if any((r.rect.centerx == gx and r.rect.centery == gy) for r in self.rooks):
            return

        # Verificar costo
        cost = config.ROOK_STATS[self.rook_selected]["cost"]
        if self.coins >= cost:
            self.rooks.append(Rook(gx, gy, self.rook_selected))
            self.coins -= cost

    def cycle_rook(self, direction=1):
        if not hasattr(self, "rook_types") or not self.rook_types:
            return

        try:
            idx = self.rook_types.index(self.rook_selected)
        except ValueError:
            idx = 0

        new_idx = (idx + direction) % len(self.rook_types)
        self.rook_selected = self.rook_types[new_idx]

    def handle_events(self):
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                self.running = False

            elif evt.type == pygame.MOUSEBUTTONDOWN and evt.button == 1:
                # Si el juego NO ha terminado: colocar rooks / recoger monedas
                if not self.game_over:
                    col, row = self.grid_from_mouse(pygame.mouse.get_pos())
                    self.handle_cell_action(col, row)
                else:
                    # Juego terminado: revisar click en botón de menú
                    mx, my = evt.pos

                    if self.button_menu_rect.collidepoint(mx, my):
                        # Solo cerramos el juego; NO tocamos continue_game
                        self.running = False

            elif evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_1:
                    self.rook_selected = "arena"
                elif evt.key == pygame.K_2:
                    self.rook_selected = "roca"
                elif evt.key == pygame.K_3:
                    self.rook_selected = "fuego"
                elif evt.key == pygame.K_4:
                    self.rook_selected = "agua"
                elif evt.key == pygame.K_r:
                    # Reiniciar partida (no salir)
                    self.reset_game()
                elif evt.key == pygame.K_c:
                    self.cycle_rook(direction=1)

                elif evt.key == pygame.K_LEFT:
                    if self.cursor_col > 0:
                        self.cursor_col -= 1
                elif evt.key == pygame.K_RIGHT:
                    if self.cursor_col < self.COLUMNAS - 1:
                        self.cursor_col += 1
                elif evt.key == pygame.K_UP:
                    if self.cursor_row > 0:
                        self.cursor_row -= 1
                elif evt.key == pygame.K_DOWN:
                    if self.cursor_row < self.FILAS - 1:
                        self.cursor_row += 1
                elif evt.key == pygame.K_SPACE and not self.game_over:
                    self.handle_cell_action(self.cursor_col, self.cursor_row)

    def update_from_joystick(self):
        if not hasattr(self, "joystick") or self.joystick is None:
            return

        direction, button, rook_next = self.joystick.read_state()
        now = time.time()

        if direction == "CENTER":
            self.last_joy_dir = "CENTER"
        else:
            should_move = False

            if direction != self.last_joy_dir:
                should_move = True
            elif now - self.last_joy_move_time >= self.JOY_MOVE_INTERVAL:
                should_move = True

            if should_move:
                if direction == "LEFT":
                    if self.cursor_col > 0:
                        self.cursor_col -= 1
                elif direction == "RIGHT":
                    if self.cursor_col < self.COLUMNAS - 1:
                        self.cursor_col += 1
                elif direction == "UP":
                    if self.cursor_row > 0:
                        self.cursor_row -= 1
                elif direction == "DOWN":
                    if self.cursor_row < self.FILAS - 1:
                        self.cursor_row += 1

                self.last_joy_move_time = now
                self.last_joy_dir = direction

        if button == 0 and self.last_joy_button == 1 and not self.game_over:
            self.handle_cell_action(self.cursor_col, self.cursor_row)

        if rook_next:
            self.cycle_rook(direction=1)
        self.last_joy_button = button

    # ---------------------- Loop principal ----------------------

    def run(self):

        while self.running:

            self.screen.blit(self.full_bg, (0, 0))

            self.handle_events()
            self.update_from_joystick()
            now = time.time()

            if not self.game_over:
                # Actualizar timer
                self.elapsed_time = int(now - self.start_time)

                # Spawneo de avatars (solo si no se llegó al máximo)
                if (now - self.last_spawn) >= config.SPAWN_INTERVAL:
                    self.spawn_avatar()
                    self.last_spawn = now

                # Spawneo de monedas
                if (now - self.last_coin_spawn) >= self.COIN_SPAWN_INTERVAL:
                    if random.random() < 0.8:
                        self.spawn_coin()
                    self.last_coin_spawn = now

                # Rooks
                for r in self.rooks[:]:
                    r.update(now, self.avatars, self.projectiles)
                    if r.vida > 0:
                        r.draw(self.screen)
                    else:
                        self.rooks.remove(r)

                # Projectiles
                for p in self.projectiles[:]:
                    p.update()
                    p.draw(self.screen)
                    if (
                        p.x > self.WINDOW_W + 50
                        or p.x < -50
                        or p.y < -50
                        or p.y > self.WINDOW_H + 50
                    ):
                        self.projectiles.remove(p)

                # Avatars
                for a in self.avatars[:]:
                    a.update(now, self.rooks, self.projectiles)
                    a.draw(self.screen)

                    avatar_center_y = a.rect.centery
                    row_from_y = int((avatar_center_y - self.offset_y) // self.CELL_H)

                    # Si llega a la PRIMERA fila (arriba), pierdes
                    if row_from_y <= 0:
                        self.game_over = True
                        self.won = False   # derrota
                        self.continue_game = False  # 🔴 perdió → no continuar

                    if a.vida <= 0 and a in self.avatars:
                        self.avatars.remove(a)
                        self.coins += config.COINS_PER_KILL

                # Colisiones de proyectiles
                self.handle_projectile_collisions()

                # ---- CONDICIÓN DE VICTORIA ----
                if (
                    not self.game_over
                    and self.spawned_avatars >= self.MAX_AVATARS
                    and len(self.avatars) == 0
                ):
                    self.game_over = True
                    self.won = True
                    self.continue_game = True   # 🟢 ganó → continuar

                # UI (solo cuando el juego sigue)
                self.draw_grid()
                self.draw_coins_on_grid()
                self.draw_cell_cursor()
                self.draw_text(f"Monedas: {self.coins}", (10, 6))
                self.draw_text(f"Rook: {self.rook_selected}", (10, 34))

                self.draw_text(
                    "1: Arena \n2: Roca \n3: Fuego \n4: Agua  \nR: Reiniciar",
                    (10, 60),
                    (180, 180, 255),
                )

                minutes = self.elapsed_time // 60
                seconds = self.elapsed_time % 60
                self.draw_text(f"Tiempo: {minutes:02d}:{seconds:02d}", (10, 200))

            else:
                base_y = self.WINDOW_H // 2

                if self.won:
                    msg = "¡Has ganado!"
                    color = (60, 255, 60)
                else:
                    msg = "¡Has perdido!"
                    color = (255, 60, 60)

                # Mensaje principal
                self.draw_text(
                    msg + "\nR: Reiniciar\nESC: Salir",
                    (600, base_y),
                    color,
                )

                # Tiempo final
                minutes = self.elapsed_time // 60
                seconds = self.elapsed_time % 60
                self.draw_text(
                    f"Tiempo: {minutes:02d}:{seconds:02d}",
                    (600, base_y + 80),
                )

                # Botón único: salir a menú principal
                self.draw_button(self.button_menu_rect, "Main Menu")

                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    self.running = False

            pygame.display.flip()
            self.clock.tick(60)

        # Devuelve si quiere continuar (según ganó/perdió) y el tiempo de la partida
        return self.continue_game, self.elapsed_time


if __name__ == "__main__":
    game = MatrixGame(10)
    salida = game.run()
    print("Salida:", salida)
