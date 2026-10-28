from typing import Callable, Dict, List, Optional, Tuple

import pygame

from .game import sprites

Color = Tuple[int, int, int]

NEUTRAL_950: Color = (10, 10, 12)
NEUTRAL_900: Color = (23, 23, 23)
NEUTRAL_800: Color = (38, 38, 38)
NEUTRAL_700: Color = (64, 64, 64)
NEUTRAL_500: Color = (115, 115, 115)
NEUTRAL_400: Color = (163, 163, 163)
NEUTRAL_200: Color = (229, 229, 229)
AMBER_200: Color = (253, 230, 138)
AMBER_300: Color = (252, 211, 77)
AMBER_400: Color = (251, 191, 36)
AMBER_500: Color = (245, 158, 11)
AMBER_600: Color = (217, 119, 6)
RED_400: Color = (248, 113, 113)
RED_500: Color = (239, 68, 68)
EMERALD_400: Color = (52, 211, 153)

SANS_FAMILIES = "dejavusans,liberationsans,ubuntu,freesans,arial"
SERIF_FAMILIES = "dejavuserif,liberationserif,freeserif,georgia"
MONO_FAMILIES = "dejavusansmono,liberationmono,couriernew"


class Fonts:
    _cache: Dict[Tuple[str, int, bool], pygame.font.Font] = {}

    @classmethod
    def get(cls, size: int, bold: bool = False, family: str = "sans") -> pygame.font.Font:
        key = (family, size, bold)
        font = cls._cache.get(key)
        if font is None:
            names = {"sans": SANS_FAMILIES, "serif": SERIF_FAMILIES, "mono": MONO_FAMILIES}[
                family
            ]
            font = pygame.font.SysFont(names, size, bold=bold)
            cls._cache[key] = font
        return font


def hex_to_rgb(value: str) -> Color:
    value = value.lstrip("#")
    return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)


def format_thousands(value: int) -> str:
    return f"{value:,}".replace(",", "\u202f")


def format_clock(seconds: float) -> str:
    total = int(seconds)
    return f"{total // 60:02d}:{total % 60:02d}"


def draw_text(
    surface: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    color,
    pos: Tuple[float, float],
    anchor: str = "topleft",
) -> pygame.Rect:
    image = font.render(text, True, color)
    rect = image.get_rect()
    setattr(rect, anchor, (int(pos[0]), int(pos[1])))
    surface.blit(image, rect)
    return rect


def wrap_text(text: str, font: pygame.font.Font, max_width: int) -> List[str]:
    lines: List[str] = []
    for paragraph in text.split("\n"):
        words = paragraph.split(" ")
        current = ""
        for word in words:
            candidate = word if not current else f"{current} {word}"
            if font.size(candidate)[0] <= max_width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        lines.append(current)
    return lines


def draw_wrapped(
    surface: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    color,
    x: int,
    y: int,
    max_width: int,
    line_gap: int = 4,
) -> int:
    lines = wrap_text(text, font, max_width)
    height = font.get_linesize() + line_gap
    for index, line in enumerate(lines):
        draw_text(surface, line, font, color, (x, y + index * height))
    return len(lines) * height


def measure_wrapped(text: str, font: pygame.font.Font, max_width: int, line_gap: int = 4) -> int:
    return len(wrap_text(text, font, max_width)) * (font.get_linesize() + line_gap)


def draw_panel(
    surface: pygame.Surface,
    rect: pygame.Rect,
    fill,
    border=None,
    radius: int = 14,
    border_width: int = 2,
) -> None:
    layer = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(layer, fill, layer.get_rect(), border_radius=radius)
    if border is not None:
        pygame.draw.rect(layer, border, layer.get_rect(), border_width, border_radius=radius)
    surface.blit(layer, rect.topleft)


def draw_overlay(surface: pygame.Surface, alpha: int = 170) -> None:
    layer = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    layer.fill((0, 0, 0, alpha))
    surface.blit(layer, (0, 0))


def draw_gradient_text_title(
    surface: pygame.Surface, text: str, size: int, center: Tuple[int, int]
) -> pygame.Rect:
    font = Fonts.get(size, True, "serif")
    mask = font.render(text, True, (255, 255, 255))
    width, height = mask.get_size()
    gradient = pygame.Surface((width, height), pygame.SRCALPHA)
    start = AMBER_200
    mid = AMBER_400
    end = AMBER_600
    for x in range(width):
        t = x / max(1, width - 1)
        if t < 0.5:
            u = t / 0.5
            col = tuple(int(start[i] + (mid[i] - start[i]) * u) for i in range(3))
        else:
            u = (t - 0.5) / 0.5
            col = tuple(int(mid[i] + (end[i] - mid[i]) * u) for i in range(3))
        pygame.draw.line(gradient, col, (x, 0), (x, height))
    gradient.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    shadow = font.render(text, True, (0, 0, 0))
    shadow.set_alpha(120)
    rect = gradient.get_rect(center=center)
    surface.blit(shadow, rect.move(2, 3))
    surface.blit(gradient, rect)
    return rect


IconDrawer = Callable[[pygame.Surface, float, float, float], None]


class Button:
    VARIANTS = {
        "primary": {
            "fill": AMBER_500,
            "hover": AMBER_400,
            "text": (23, 23, 23),
            "border": AMBER_300,
        },
        "secondary": {
            "fill": NEUTRAL_800,
            "hover": NEUTRAL_700,
            "text": NEUTRAL_200,
            "border": NEUTRAL_700,
        },
        "danger": {
            "fill": (185, 28, 28),
            "hover": (220, 38, 38),
            "text": (255, 255, 255),
            "border": RED_400,
        },
        "ghost": {
            "fill": (23, 23, 23, 0),
            "hover": (64, 64, 64, 160),
            "text": NEUTRAL_400,
            "border": None,
        },
        "icon": {
            "fill": (23, 23, 23, 230),
            "hover": NEUTRAL_700,
            "text": NEUTRAL_200,
            "border": NEUTRAL_700,
        },
    }

    def __init__(
        self,
        label: str,
        callback: Callable[[], None],
        variant: str = "secondary",
        icon: Optional[IconDrawer] = None,
        font_size: int = 16,
        bold: bool = True,
        enabled: bool = True,
    ):
        self.label = label
        self.callback = callback
        self.variant = variant
        self.icon = icon
        self.font_size = font_size
        self.bold = bold
        self.enabled = enabled
        self.rect = pygame.Rect(0, 0, 0, 0)

    def place(self, x: int, y: int, w: int, h: int) -> "Button":
        self.rect = pygame.Rect(x, y, w, h)
        return self

    def draw(self, surface: pygame.Surface) -> None:
        style = self.VARIANTS[self.variant]
        hovered = self.enabled and self.rect.collidepoint(pygame.mouse.get_pos())
        fill = style["hover"] if hovered else style["fill"]
        if not self.enabled:
            fill = (30, 30, 30)
        draw_panel(surface, self.rect, fill, style["border"] if self.enabled else NEUTRAL_800, 10, 2)
        text_color = style["text"] if self.enabled else NEUTRAL_500
        font = Fonts.get(self.font_size, self.bold)
        icon_size = self.font_size + 4
        text_w = font.size(self.label)[0] if self.label else 0
        gap = 10 if (self.icon and self.label) else 0
        icon_w = icon_size if self.icon else 0
        total = icon_w + gap + text_w
        start_x = self.rect.centerx - total // 2
        if self.icon:
            self.icon(surface, start_x + icon_w / 2, self.rect.centery, icon_size)
        if self.label:
            draw_text(
                surface,
                self.label,
                font,
                text_color,
                (start_x + icon_w + gap, self.rect.centery),
                "midleft",
            )

    def handle_event(self, event: pygame.event.Event) -> bool:
        if (
            self.enabled
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        ):
            self.callback()
            return True
        return False


def stars_row(surface: pygame.Surface, center_x: int, y: int, earned: int, size: int = 16, gap: int = 8) -> None:
    total_w = 3 * size * 2 + 2 * gap
    x = center_x - total_w // 2 + size
    for index in range(3):
        sprites.draw_star(surface, x + index * (size * 2 + gap), y, size, index < earned)


class Modal:
    PANEL_WIDTH = 520
    PANEL_HEIGHT = 420

    def __init__(self):
        self.buttons: List[Button] = []

    def panel_rect(self, surface_size: Tuple[int, int]) -> pygame.Rect:
        rect = pygame.Rect(0, 0, self.PANEL_WIDTH, self.PANEL_HEIGHT)
        rect.center = (surface_size[0] // 2, surface_size[1] // 2)
        return rect

    def layout(self, surface_size: Tuple[int, int]) -> None:
        return None

    def render(self, surface: pygame.Surface) -> None:
        return None

    def update(self, dt: float) -> None:
        return None

    def draw(self, surface: pygame.Surface) -> None:
        self.layout(surface.get_size())
        draw_overlay(surface)
        self.render(surface)
        for button in self.buttons:
            button.draw(surface)

    def handle_event(self, event: pygame.event.Event, surface_size: Tuple[int, int]) -> bool:
        self.layout(surface_size)
        for button in self.buttons:
            if button.handle_event(event):
                return True
        return event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP)
