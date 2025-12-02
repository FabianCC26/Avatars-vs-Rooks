import pygame
import time

class InputBox:
    def __init__(self, x, y, w, h, font, placeholder="", is_password=False, max_chars=30):
        # Rect y estilo
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color("gray70")
        self.color_active = pygame.Color("dodgerblue3")
        self.color = self.color_inactive

        # Texto y estado
        self.text = ""
        self.font = font
        self.placeholder = placeholder
        self.active = False
        self.is_password = is_password
        self.show_password = False
        self.max_chars = max_chars

        # Cursor y selección
        self.caret_pos = 0                # Índice del cursor en el string (0..len)
        self.sel_start = None             # Índice inicio de selección (inclusive)
        self.sel_end = None               # Índice fin de selección (exclusivo)
        self.drag_selecting = False       # Arrastre con mouse para seleccionar
        self.last_click_time = 0.0        # Para doble clic
        self.last_click_pos = -1          # Para doble clic, caret previo

        # Scroll horizontal en píxeles para mantener el cursor visible
        self.scroll_x = 0

        # Padding interno y espacio para el botón "ojo"
        self.padding_x = 10
        self.padding_right = 35 if is_password else 10

        # Botón del ojo (si aplica)
        if is_password:
            self.eye_rect = pygame.Rect(x + w - 28, y + (h // 2 - 8), 18, 16)
        else:
            self.eye_rect = None

        # Parpadeo del cursor
        self.cursor_visible = True
        self.last_blink = time.time()
        self.blink_interval = 0.5  # segundos

        # Clipboard (puede requerir display iniciado). Se usa condicionalmente.
        try:
            if not pygame.scrap.get_init():
                pygame.scrap.init()
            self.clipboard_ok = True
        except Exception:
            self.clipboard_ok = False

    # Utilidades de selección y cursor

    def _has_selection(self):
        return self.sel_start is not None and self.sel_end is not None and self.sel_start != self.sel_end

    def _clear_selection(self):
        self.sel_start = None
        self.sel_end = None

    def _set_selection(self, a, b):
        self.sel_start = min(a, b)
        self.sel_end = max(a, b)

    def _delete_selection(self):
        if not self._has_selection():
            return
        left = self.text[:self.sel_start]
        right = self.text[self.sel_end:]
        self.text = left + right
        self.caret_pos = len(left)
        self._clear_selection()

    # Clipboard helpers (pueden no estar disponibles)
    def _clip_set(self, s: str):
        if not self.clipboard_ok:
            return
        try:
            pygame.scrap.put(pygame.SCRAP_TEXT, s.encode("utf-8"))
        except Exception:
            pass

    def _clip_get(self) -> str:
        if not self.clipboard_ok:
            return ""
        try:
            raw = pygame.scrap.get(pygame.SCRAP_TEXT)
            if not raw:
                return ""
            if isinstance(raw, bytes):
                text = raw.decode("utf-8", errors="ignore")
            else:
                text = str(raw)
            # Limpiar caracteres problemáticos (incluye '\x00' y no imprimibles)
            cleaned = "".join(ch for ch in text if ch.isprintable())
            return cleaned
        except Exception:
            return ""

    # Mapeo de posición x del mouse a índice de carácter

    def _visible_text_and_offset(self):
        # Texto mostrado (considera ocultar password) y prefijo para cálculo de ancho
        display_text = self.text if (not self.is_password or self.show_password) else ("•" * len(self.text))
        return display_text

    def _text_width(self, s: str) -> int:
        return self.font.size(s)[0]

    def _index_from_mouse_x(self, mouse_x: int) -> int:
        # Devuelve índice aproximado en función del x del mouse dentro del área de texto
        display_text = self._visible_text_and_offset()
        area_x = self.rect.x + self.padding_x
        x = mouse_x - area_x + self.scroll_x
        if x <= 0:
            return 0
        # Búsqueda lineal (texto corto)
        acc = 0
        for i, ch in enumerate(display_text):
            w = self._text_width(ch)
            if acc + w / 2 >= x:
                return i
            acc += w
        return len(display_text)

    def _ensure_caret_visible(self):
        # Ajusta scroll_x para que el cursor quede dentro del rect visible
        area_left = self.rect.x + self.padding_x
        area_right = self.rect.right - self.padding_right
        visible_width = max(0, area_right - area_left)

        display_text = self._visible_text_and_offset()
        caret_px = self._text_width(display_text[:self.caret_pos])

        if caret_px - self.scroll_x > visible_width:
            self.scroll_x = caret_px - visible_width + 2
        elif caret_px - self.scroll_x < 0:
            self.scroll_x = max(0, caret_px - 2)

    # Manejo de eventos

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Clic dentro del input
            if self.rect.collidepoint(event.pos):
                prev_active = self.active
                self.active = True
                self.color = self.color_active

                # Clic en el icono del ojo
                if self.eye_rect and self.eye_rect.collidepoint(event.pos):
                    self.show_password = not self.show_password
                    return

                # Detección de doble clic para seleccionar palabra
                now = time.time()
                double = (now - self.last_click_time) < 0.35 and self.last_click_pos == self.caret_pos
                self.last_click_time = now

                # Mover caret al punto clicado
                idx = self._index_from_mouse_x(event.pos[0])
                self.caret_pos = max(0, min(len(self.text), idx))
                self._ensure_caret_visible()

                if double and len(self.text) > 0:
                    # Seleccionar palabra bajo el cursor
                    start = self.caret_pos
                    end = self.caret_pos
                    while start > 0 and self.text[start - 1].isalnum():
                        start -= 1
                    while end < len(self.text) and self.text[end].isalnum():
                        end += 1
                    self._set_selection(start, end)
                else:
                    # Empezar selección por arrastre
                    self.drag_selecting = True
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        # Extiende selección existente
                        if not self._has_selection():
                            self._set_selection(self.caret_pos, self.caret_pos)
                    else:
                        self._clear_selection()

                self.last_click_pos = self.caret_pos

            else:
                # Clic fuera desactiva el input (a menos que sea el ojo)
                self.active = False
                self.color = self.color_inactive

        elif event.type == pygame.MOUSEMOTION and self.drag_selecting and self.active:
            # Extender selección mientras se arrastra
            idx = self._index_from_mouse_x(event.pos[0])
            idx = max(0, min(len(self.text), idx))
            if not self._has_selection():
                self._set_selection(self.caret_pos, idx)
            else:
                if self.sel_start == self.caret_pos:
                    self._set_selection(self.caret_pos, idx)
                elif self.sel_end == self.caret_pos:
                    self._set_selection(idx, self.caret_pos)
                else:
                    # Si había una selección previa, mantener el ancla en el extremo más cercano
                    anchor = self.sel_start if abs(self.sel_start - idx) < abs(self.sel_end - idx) else self.sel_end
                    self._set_selection(anchor, idx)
            self._ensure_caret_visible()

        elif event.type == pygame.MOUSEBUTTONUP:
            self.drag_selecting = False

        if event.type == pygame.KEYDOWN and self.active:
            mods = pygame.key.get_mods()
            ctrl = (mods & pygame.KMOD_CTRL) != 0
            shift = (mods & pygame.KMOD_SHIFT) != 0

            if event.key == pygame.K_RETURN:
                pass

            # Selección total
            elif ctrl and event.key == pygame.K_a:
                self.sel_start = 0
                self.sel_end = len(self.text)
                self.caret_pos = self.sel_end
                self._ensure_caret_visible()

            # Copiar
            elif ctrl and event.key == pygame.K_c:
                if self._has_selection():
                    self._clip_set(self.text[self.sel_start:self.sel_end])

            # Cortar
            elif ctrl and event.key == pygame.K_x:
                if self._has_selection():
                    self._clip_set(self.text[self.sel_start:self.sel_end])
                    self._delete_selection()
                    self._ensure_caret_visible()

            # Pegar
            elif ctrl and event.key == pygame.K_v:
                paste = self._clip_get()
                if paste:
                    # Normalizar saltos de línea
                    paste = paste.replace("\n", " ").replace("\r", " ")
                    # Filtrar no imprimibles por seguridad extra
                    paste = "".join(ch for ch in paste if ch.isprintable())

                    # Limitar para no exceder max_chars
                    available = self.max_chars - len(self.text) + (
                        self.sel_end - self.sel_start if self._has_selection() else 0
                    )
                    if available <= 0:
                        return
                    if self._has_selection():
                        self._delete_selection()
                    paste = paste[:available]
                    self.text = self.text[:self.caret_pos] + paste + self.text[self.caret_pos:]
                    self.caret_pos += len(paste)
                    self._ensure_caret_visible()

            # Movimiento del cursor
            elif event.key == pygame.K_LEFT:
                if ctrl:
                    # Saltar palabra a la izquierda
                    if self.caret_pos > 0:
                        i = self.caret_pos - 1
                        while i > 0 and self.text[i].isspace():
                            i -= 1
                        while i > 0 and self.text[i - 1].isalnum():
                            i -= 1
                        new_pos = i
                    else:
                        new_pos = 0
                else:
                    new_pos = max(0, self.caret_pos - 1)

                if shift:
                    if not self._has_selection():
                        self._set_selection(self.caret_pos, new_pos)
                    else:
                        self._set_selection(self.sel_start, new_pos)
                    self.caret_pos = new_pos
                else:
                    self.caret_pos = new_pos
                    self._clear_selection()
                self._ensure_caret_visible()

            elif event.key == pygame.K_RIGHT:
                if ctrl:
                    # Saltar palabra a la derecha
                    if self.caret_pos < len(self.text):
                        i = self.caret_pos
                        while i < len(self.text) and self.text[i].isalnum():
                            i += 1
                        while i < len(self.text) and self.text[i].isspace():
                            i += 1
                        new_pos = min(len(self.text), i)
                    else:
                        new_pos = len(self.text)
                else:
                    new_pos = min(len(self.text), self.caret_pos + 1)

                if shift:
                    if not self._has_selection():
                        self._set_selection(self.caret_pos, new_pos)
                    else:
                        self._set_selection(self.sel_start, new_pos)
                    self.caret_pos = new_pos
                else:
                    self.caret_pos = new_pos
                    self._clear_selection()
                self._ensure_caret_visible()

            elif event.key == pygame.K_HOME:
                new_pos = 0
                if shift:
                    if not self._has_selection():
                        self._set_selection(self.caret_pos, new_pos)
                    else:
                        self._set_selection(self.sel_start, new_pos)
                else:
                    self._clear_selection()
                self.caret_pos = new_pos
                self._ensure_caret_visible()

            elif event.key == pygame.K_END:
                new_pos = len(self.text)
                if shift:
                    if not self._has_selection():
                        self._set_selection(self.caret_pos, new_pos)
                    else:
                        self._set_selection(self.sel_start, new_pos)
                else:
                    self._clear_selection()
                self.caret_pos = new_pos
                self._ensure_caret_visible()

            # Borrar hacia atrás
            elif event.key == pygame.K_BACKSPACE:
                if self._has_selection():
                    self._delete_selection()
                elif self.caret_pos > 0:
                    self.text = self.text[:self.caret_pos - 1] + self.text[self.caret_pos:]
                    self.caret_pos -= 1
                self._ensure_caret_visible()

            # Borrar hacia adelante
            elif event.key == pygame.K_DELETE:
                if self._has_selection():
                    self._delete_selection()
                elif self.caret_pos < len(self.text):
                    self.text = self.text[:self.caret_pos] + self.text[self.caret_pos + 1:]
                self._ensure_caret_visible()

            # Inserción de texto normal
            else:
                if event.unicode and event.unicode.isprintable():
                    if self._has_selection():
                        self._delete_selection()
                    if len(self.text) < self.max_chars:
                        self.text = self.text[:self.caret_pos] + event.unicode + self.text[self.caret_pos:]
                        self.caret_pos += 1
                        self._ensure_caret_visible()

        # Actualizar parpadeo del cursor
        now = time.time()
        if now - self.last_blink >= self.blink_interval:
            self.cursor_visible = not self.cursor_visible
            self.last_blink = now

    # Dibujo

    def draw(self, screen):
        # Preparar texto visible
        if self.text:
            raw_display = self.text if (not self.is_password or self.show_password) else ("•" * len(self.text))
            color_text = (0, 0, 0)
        else:
            raw_display = self.placeholder
            color_text = (150, 150, 150)

        # Fondo y borde
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        pygame.draw.rect(screen, self.color, self.rect, 2)

        # Área de texto útil
        area_left = self.rect.x + self.padding_x
        area_right = self.rect.right - self.padding_right
        visible_width = max(0, area_right - area_left)

        # Alinear scroll_x con la longitud del texto
        display_for_width = self._visible_text_and_offset()
        text_pixel_len = self._text_width(display_for_width)
        self.scroll_x = max(0, min(self.scroll_x, max(0, text_pixel_len - visible_width)))

        # Render del texto con scroll horizontal
        text_surface = self.font.render(raw_display, True, color_text)
        text_y = self.rect.y + (self.rect.height - text_surface.get_height()) // 2
        screen.blit(text_surface, (area_left - self.scroll_x, text_y))

        # Selección: resaltar rango seleccionado
        if self._has_selection():
            vis_text = self._visible_text_and_offset()
            left_px = self._text_width(vis_text[:self.sel_start]) - self.scroll_x
            right_px = self._text_width(vis_text[:self.sel_end]) - self.scroll_x
            sel_x = area_left + max(0, left_px)
            sel_w = max(0, right_px - left_px)
            sel_rect = pygame.Rect(sel_x, text_y, sel_w, text_surface.get_height())
            sel_color = (30, 144, 255, 100)
            sel_surf = pygame.Surface((sel_rect.width, sel_rect.height), pygame.SRCALPHA)
            sel_surf.fill(sel_color)
            screen.blit(sel_surf, (sel_rect.x, sel_rect.y))

            selected_str = raw_display[self.sel_start:self.sel_end]
            before_px = self._text_width(raw_display[:self.sel_start])
            sel_text_surf = self.font.render(selected_str, True, (255, 255, 255))
            screen.blit(sel_text_surf, (area_left - self.scroll_x + before_px, text_y))

        # Cursor de texto
        if self.active and self.cursor_visible and not self._has_selection():
            vis_text = self._visible_text_and_offset()
            caret_px = self._text_width(vis_text[:self.caret_pos]) - self.scroll_x
            cx = area_left + caret_px
            cy1 = self.rect.y + 6
            cy2 = self.rect.bottom - 6
            pygame.draw.line(screen, (0, 0, 0), (cx, cy1), (cx, cy2), 1)

        # Icono del ojo (si aplica)
        if self.eye_rect:
            self.draw_eye_icon(screen)

    def draw_eye_icon(self, screen):
        color = (50, 50, 50)
        pygame.draw.ellipse(screen, color, self.eye_rect, 2)
        center = self.eye_rect.center
        pygame.draw.circle(screen, color, center, 3)
        if not self.show_password:
            pygame.draw.line(screen, color, self.eye_rect.topleft, self.eye_rect.bottomright, 2)

    def get_text(self):
        return self.text
