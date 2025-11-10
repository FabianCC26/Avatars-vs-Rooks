import os
import json
import pygame
import unicodedata


def _normalize_text(s: str) -> str:
    if not isinstance(s, str):
        return ""
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).lower().strip()


def load_countries(json_path: str):
    if not os.path.exists(json_path):
        return []
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        out = []
        for item in data:
            name = item.get("name", "")
            a2 = item.get("alpha2", "")
            a3 = item.get("alpha3", "")
            if name and a2 and a3:
                out.append({"name": name, "alpha2": a2, "alpha3": a3})
        return out


class SearchableDropdown:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        font: pygame.font.Font,
        options: list[dict],
        main_color=(220, 220, 220),
        hover_color=(200, 200, 200),
        text_color=(0, 0, 0),
        placeholder: str = "Select a country…",
        max_visible: int = 10,
        item_height: int = 38  # Suficiente altura para texto completo
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.main_color = main_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.placeholder = placeholder

        self.all_options = options[:]
        self.filtered = options[:]
        self.query = ""
        self.selected_index = -1
        self.open = False

        self.max_visible = max_visible
        self.item_height = item_height
        self.scroll_offset = 0

        self.hover = False
        self.active = False

    def get_selected(self):
        if self.selected_index >= 0 and self.selected_index < len(self.filtered):
            return self.filtered[self.selected_index]
        return None

    def _apply_filter(self):
        q = _normalize_text(self.query)
        if not q:
            self.filtered = self.all_options[:]
            self.selected_index = -1
            self.scroll_offset = 0
            return

        prefix = []
        code_match = []
        substring = []
        for item in self.all_options:
            name_n = _normalize_text(item["name"])
            a2 = item["alpha2"].lower()
            a3 = item["alpha3"].lower()
            if name_n.startswith(q):
                prefix.append(item)
            elif q in (a2, a3) or a2.startswith(q) or a3.startswith(q):
                code_match.append(item)
            elif q in name_n:
                substring.append(item)
        self.filtered = prefix + code_match + substring
        self.selected_index = 0 if self.filtered else -1
        self.scroll_offset = 0

    def _visible_slice(self):
        start = self.scroll_offset
        end = min(start + self.max_visible, len(self.filtered))
        return start, end

    def _ensure_selected_visible(self):
        if self.selected_index < 0:
            return
        if self.selected_index < self.scroll_offset:
            self.scroll_offset = self.selected_index
        elif self.selected_index >= self.scroll_offset + self.max_visible:
            self.scroll_offset = self.selected_index - self.max_visible + 1
        self.scroll_offset = max(0, min(self.scroll_offset, max(0, len(self.filtered) - self.max_visible)))

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.open = not self.open
                self.active = True
            else:
                dropdown_area = self._dropdown_rect()
                if self.open and dropdown_area and dropdown_area.collidepoint(event.pos):
                    idx = self._index_at_pos(event.pos)
                    if idx is not None and 0 <= idx < len(self.filtered):
                        self.selected_index = idx
                        self.query = self.filtered[idx]["name"]
                    self.open = False
                else:
                    self.open = False
                    self.active = False

        elif event.type == pygame.MOUSEWHEEL and self.open:
            if len(self.filtered) > self.max_visible:
                self.scroll_offset -= event.y
                self.scroll_offset = max(0, min(self.scroll_offset, len(self.filtered) - self.max_visible))

        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_ESCAPE:
                self.open = False
                self.active = False
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                if self.open and self.selected_index >= 0 and self.selected_index < len(self.filtered):
                    self.query = self.filtered[self.selected_index]["name"]
                self.open = False
            elif event.key == pygame.K_BACKSPACE:
                if self.query:
                    self.query = self.query[:-1]
                    self._apply_filter()
            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                if not self.open:
                    self.open = True
                if not self.filtered:
                    return
                delta = -1 if event.key == pygame.K_UP else 1
                if self.selected_index < 0:
                    self.selected_index = 0
                else:
                    self.selected_index = max(0, min(self.selected_index + delta, len(self.filtered) - 1))
                self._ensure_selected_visible()
            else:
                ch = event.unicode
                if ch and ch.isprintable():
                    self.query += ch
                    self._apply_filter()
                    self.open = True
                    self._ensure_selected_visible()

    def _truncate_text(self, text: str, max_width: int) -> str:
        """Trunca el texto si es más largo que max_width."""
        if self.font.size(text)[0] <= max_width:
            return text
        while len(text) > 0 and self.font.size(text + "...")[0] > max_width:
            text = text[:-1]
        return text + "..."

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.main_color, self.rect, border_radius=6)
        text_to_show = self.query if self.query else self.placeholder
        color = self.text_color if self.query else (120, 120, 120)

        # Truncar texto si es muy largo para el cuadro principal
        max_text_width = self.rect.width - 35
        text_to_show = self._truncate_text(text_to_show, max_text_width)

        text_surf = self.font.render(text_to_show, True, color)
        text_rect = text_surf.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        surface.blit(text_surf, text_rect)

        # Triángulo indicador
        tri_x = self.rect.right - 18
        tri_y = self.rect.centery
        pts = [(tri_x - 8, tri_y - 4), (tri_x + 8, tri_y - 4), (tri_x, tri_y + 6)]
        pygame.draw.polygon(surface, (80, 80, 80), pts)

        if self.open:
            dropdown_rect = self._dropdown_rect()
            pygame.draw.rect(surface, (245, 245, 245), dropdown_rect, border_radius=6)
            pygame.draw.rect(surface, (200, 200, 200), dropdown_rect, width=1, border_radius=6)

            start, end = self._visible_slice()
            for i, item in enumerate(self.filtered[start:end], start=start):
                row_rect = pygame.Rect(
                    dropdown_rect.x,
                    dropdown_rect.y + (i - start) * self.item_height,
                    dropdown_rect.width,
                    self.item_height,
                )
                hover = row_rect.collidepoint(pygame.mouse.get_pos())
                bg = self.hover_color if (hover or i == self.selected_index) else (245, 245, 245)
                pygame.draw.rect(surface, bg, row_rect)

                label = f"{item['name']}  ({item['alpha2']}/{item['alpha3']})"
                max_label_width = row_rect.width - 20
                label = self._truncate_text(label, max_label_width)

                label_surf = self.font.render(label, True, self.text_color)
                text_y = row_rect.y + self.item_height / 2 - 2
                label_rect = label_surf.get_rect(midleft=(row_rect.x + 10, text_y))
                surface.blit(label_surf, label_rect)

            # Scrollbar
            if len(self.filtered) > self.max_visible:
                bar_area = pygame.Rect(dropdown_rect.right - 6, dropdown_rect.y, 6, dropdown_rect.height)
                pygame.draw.rect(surface, (230, 230, 230), bar_area)
                ratio = self.max_visible / len(self.filtered)
                bar_h = max(20, int(bar_area.height * ratio))
                max_scroll = len(self.filtered) - self.max_visible
                top_ratio = (self.scroll_offset / max_scroll) if max_scroll > 0 else 0
                bar_top = bar_area.y + int((bar_area.height - bar_h) * top_ratio)
                pygame.draw.rect(surface, (160, 160, 160), (bar_area.x, bar_top, bar_area.width, bar_h), border_radius=3)

    def _dropdown_rect(self) -> pygame.Rect:
        total = min(self.max_visible, max(0, len(self.filtered)))
        return pygame.Rect(self.rect.x, self.rect.bottom + 2, self.rect.width, total * self.item_height)

    def _index_at_pos(self, pos) -> int | None:
        dropdown_rect = self._dropdown_rect()
        if not dropdown_rect.collidepoint(pos):
            return None
        relative_y = pos[1] - dropdown_rect.y
        idx = self.scroll_offset + (relative_y // self.item_height)
        if 0 <= idx < len(self.filtered):
            return idx
        return None
