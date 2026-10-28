import math
from typing import List, Tuple

import pygame

Point = Tuple[float, float]


def blend_circle(surface, color, center, radius, alpha) -> None:
    size = int(radius * 2 + 4)
    layer = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(
        layer, (color[0], color[1], color[2], int(alpha)), (size // 2, size // 2), int(radius)
    )
    surface.blit(layer, (center[0] - size // 2, center[1] - size // 2))


def blend_ellipse(surface, color, center, rx, ry, alpha) -> None:
    w = int(rx * 2 + 4)
    h = int(ry * 2 + 4)
    layer = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.ellipse(
        layer, (color[0], color[1], color[2], int(alpha)), (2, 2, rx * 2, ry * 2)
    )
    surface.blit(layer, (center[0] - w // 2, center[1] - h // 2))


def blend_rect(surface, color, rect, alpha) -> None:
    rect = pygame.Rect(rect)
    if rect.width <= 0 or rect.height <= 0:
        return
    layer = pygame.Surface(rect.size, pygame.SRCALPHA)
    layer.fill((color[0], color[1], color[2], int(alpha)))
    surface.blit(layer, rect.topleft)


def blend_outline(surface, color, rect, alpha, width=1) -> None:
    rect = pygame.Rect(rect)
    layer = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(
        layer,
        (color[0], color[1], color[2], int(alpha)),
        layer.get_rect(),
        width,
    )
    surface.blit(layer, rect.topleft)


def _scaled(points: List[Point], cx: float, cy: float, k: float) -> List[Point]:
    return [(cx + x * k, cy + y * k) for x, y in points]


def draw_banana(surface, cx, cy, size) -> None:
    k = size / 26.0
    outer: List[Point] = []
    inner: List[Point] = []
    for i in range(0, 13):
        a = math.radians(25 + i * 10)
        outer.append((math.cos(a) * 13, -3 + math.sin(a) * 13))
    for i in range(0, 13):
        a = math.radians(40 + i * (100 / 12))
        inner.append((math.cos(a) * 12, -8 + math.sin(a) * 12))
    shape = outer + inner[::-1]
    pts = _scaled(shape, cx, cy + 1 * k, k)
    pygame.draw.polygon(surface, (251, 191, 36), pts)
    pygame.draw.polygon(surface, (180, 83, 9), pts, max(1, int(k)))
    tip_l = _scaled([outer[-1]], cx, cy + 1 * k, k)[0]
    tip_r = _scaled([outer[0]], cx, cy + 1 * k, k)[0]
    pygame.draw.circle(surface, (87, 53, 15), (int(tip_l[0]), int(tip_l[1])), max(2, int(2 * k)))
    pygame.draw.circle(surface, (87, 53, 15), (int(tip_r[0]), int(tip_r[1])), max(2, int(2 * k)))


def draw_heart(surface, cx, cy, size, color=(239, 68, 68)) -> None:
    r = size * 0.27
    pygame.draw.circle(surface, color, (int(cx - r), int(cy - r * 0.6)), int(r + 1))
    pygame.draw.circle(surface, color, (int(cx + r), int(cy - r * 0.6)), int(r + 1))
    pygame.draw.polygon(
        surface,
        color,
        [
            (cx - r * 2.0, cy - r * 0.3),
            (cx + r * 2.0, cy - r * 0.3),
            (cx, cy + size * 0.45),
        ],
    )


def draw_shield(surface, cx, cy, size) -> None:
    k = size / 22.0
    outline = _scaled([(-10, -11), (10, -11), (10, 1), (0, 12), (-10, 1)], cx, cy, k)
    pygame.draw.polygon(surface, (56, 189, 248), outline)
    pygame.draw.polygon(
        surface,
        (224, 242, 254),
        _scaled([(-6, -7), (6, -7), (6, 0), (0, 8), (-6, 0)], cx, cy, k),
    )
    pygame.draw.polygon(surface, (3, 105, 161), outline, max(1, int(k)))


def draw_bolt(surface, cx, cy, size) -> None:
    k = size / 22.0
    pts = _scaled([(2, -12), (-8, 2), (-1, 2), (-3, 12), (8, -3), (1, -3)], cx, cy, k)
    pygame.draw.polygon(surface, (250, 204, 21), pts)
    pygame.draw.polygon(surface, (161, 98, 7), pts, 1)


def draw_snake(surface, cx, cy, size, wobble=0.0) -> None:
    k = size / 26.0
    for i in range(8):
        px = cx + (-11 + i * 3.2) * k + wobble * 0.3
        py = cy + math.sin(i * 0.9 + wobble * 0.3) * 4 * k + 3 * k
        pygame.draw.circle(surface, (22, 163, 74) if i % 2 else (34, 197, 94), (int(px), int(py)), max(3, int((4.6 - i * 0.12) * k)))
    hx = cx + 13 * k + wobble * 0.3
    hy = cy + 1 * k
    pygame.draw.circle(surface, (21, 128, 61), (int(hx), int(hy)), int(5.5 * k))
    pygame.draw.circle(surface, (254, 240, 138), (int(hx + 1.5 * k), int(hy - 2 * k)), max(1, int(1.6 * k)))
    pygame.draw.line(surface, (239, 68, 68), (hx + 5 * k, hy + 1 * k), (hx + 9 * k, hy + 1 * k), max(1, int(k)))


def draw_bat(surface, cx, cy, size, flap=0.0) -> None:
    k = size / 26.0
    up = flap * 1.2
    left = [(-2, 0), (-13, -7 - up), (-11, 0), (-8, 3), (-5, 1), (-2, 5)]
    right = [(2, 0), (13, -7 - up), (11, 0), (8, 3), (5, 1), (2, 5)]
    pygame.draw.polygon(surface, (76, 29, 149), _scaled(left, cx, cy, k))
    pygame.draw.polygon(surface, (76, 29, 149), _scaled(right, cx, cy, k))
    pygame.draw.circle(surface, (46, 16, 101), (int(cx), int(cy + 1 * k)), int(5 * k))
    pygame.draw.polygon(surface, (46, 16, 101), _scaled([(-4, -3), (-3, -8), (-1, -4)], cx, cy, k))
    pygame.draw.polygon(surface, (46, 16, 101), _scaled([(4, -3), (3, -8), (1, -4)], cx, cy, k))
    pygame.draw.circle(surface, (248, 113, 113), (int(cx - 2 * k), int(cy)), max(1, int(1.2 * k)))
    pygame.draw.circle(surface, (248, 113, 113), (int(cx + 2 * k), int(cy)), max(1, int(1.2 * k)))


def draw_skull(surface, cx, cy, size) -> None:
    k = size / 26.0
    pygame.draw.circle(surface, (241, 245, 249), (int(cx), int(cy - 2 * k)), int(10 * k))
    pygame.draw.rect(
        surface,
        (241, 245, 249),
        pygame.Rect(int(cx - 6 * k), int(cy + 4 * k), int(12 * k), int(8 * k)),
        border_radius=max(1, int(2 * k)),
    )
    pygame.draw.circle(surface, (15, 23, 42), (int(cx - 4 * k), int(cy - 3 * k)), max(2, int(3 * k)))
    pygame.draw.circle(surface, (15, 23, 42), (int(cx + 4 * k), int(cy - 3 * k)), max(2, int(3 * k)))
    pygame.draw.polygon(surface, (15, 23, 42), _scaled([(0, 0), (-2, 4), (2, 4)], cx, cy, k))
    for i in range(-2, 3):
        pygame.draw.line(surface, (100, 116, 139), (cx + i * 2.4 * k, cy + 8 * k), (cx + i * 2.4 * k, cy + 12 * k), 1)


def draw_plant(surface, cx, cy, size, open_mouth=True) -> None:
    k = size / 26.0
    pygame.draw.line(surface, (21, 128, 61), (cx, cy + 12 * k), (cx, cy + 2 * k), max(2, int(3 * k)))
    pygame.draw.polygon(surface, (34, 197, 94), _scaled([(0, 9), (-10, 4), (-4, 10)], cx, cy, k))
    pygame.draw.polygon(surface, (34, 197, 94), _scaled([(0, 9), (10, 4), (4, 10)], cx, cy, k))
    gap = 5 if open_mouth else 1
    upper = _scaled([(-11, 2 - gap), (0, -12 - gap), (11, 2 - gap)], cx, cy, k)
    lower = _scaled([(-11, 2 + gap * 0.4), (0, 10 + gap), (11, 2 + gap * 0.4)], cx, cy, k)
    pygame.draw.polygon(surface, (220, 38, 38), lower)
    pygame.draw.polygon(surface, (185, 28, 28), upper)
    for i in range(-2, 3):
        tx = cx + i * 4 * k
        pygame.draw.polygon(
            surface,
            (255, 255, 255),
            [(tx - 1.6 * k, cy + (2 - gap) * k), (tx + 1.6 * k, cy + (2 - gap) * k), (tx, cy + (2 - gap + 4) * k)],
        )


def draw_crown(surface, cx, cy, size) -> None:
    k = size / 20.0
    pts = _scaled([(-9, 7), (-8, -6), (-4, 0), (0, -9), (4, 0), (8, -6), (9, 7)], cx, cy, k)
    pygame.draw.polygon(surface, (251, 191, 36), pts)
    pygame.draw.polygon(surface, (180, 83, 9), pts, max(1, int(k * 0.6)))
    pygame.draw.circle(surface, (239, 68, 68), (int(cx), int(cy + 2 * k)), max(1, int(1.8 * k)))
    pygame.draw.circle(surface, (239, 68, 68), (int(cx - 5 * k), int(cy + 4 * k)), max(1, int(1.3 * k)))
    pygame.draw.circle(surface, (239, 68, 68), (int(cx + 5 * k), int(cy + 4 * k)), max(1, int(1.3 * k)))


def draw_lock(surface, cx, cy, size) -> None:
    k = size / 16.0
    pygame.draw.arc(
        surface,
        (203, 213, 225),
        pygame.Rect(int(cx - 5 * k), int(cy - 9 * k), int(10 * k), int(12 * k)),
        0,
        math.pi,
        max(2, int(2 * k)),
    )
    pygame.draw.rect(
        surface,
        (148, 163, 184),
        pygame.Rect(int(cx - 7 * k), int(cy - 2 * k), int(14 * k), int(11 * k)),
        border_radius=max(1, int(2 * k)),
    )
    pygame.draw.circle(surface, (30, 41, 59), (int(cx), int(cy + 3 * k)), max(1, int(1.8 * k)))


def draw_star(surface, cx, cy, size, filled=True) -> None:
    pts = []
    for i in range(10):
        r = size if i % 2 == 0 else size * 0.45
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    if filled:
        pygame.draw.polygon(surface, (251, 191, 36), pts)
        pygame.draw.polygon(surface, (180, 83, 9), pts, 1)
    else:
        pygame.draw.polygon(surface, (38, 38, 38), pts)
        pygame.draw.polygon(surface, (64, 64, 64), pts, 1)


def draw_gorilla_face(surface, cx, cy, size) -> None:
    k = size / 60.0
    pygame.draw.circle(surface, (28, 25, 23), (int(cx - 24 * k), int(cy - 4 * k)), int(9 * k))
    pygame.draw.circle(surface, (28, 25, 23), (int(cx + 24 * k), int(cy - 4 * k)), int(9 * k))
    pygame.draw.circle(surface, (41, 37, 36), (int(cx), int(cy)), int(25 * k))
    pygame.draw.ellipse(
        surface,
        (87, 83, 78),
        pygame.Rect(int(cx - 15 * k), int(cy + 1 * k), int(30 * k), int(22 * k)),
    )
    pygame.draw.circle(surface, (255, 255, 255), (int(cx - 8 * k), int(cy - 6 * k)), max(2, int(5 * k)))
    pygame.draw.circle(surface, (255, 255, 255), (int(cx + 8 * k), int(cy - 6 * k)), max(2, int(5 * k)))
    pygame.draw.circle(surface, (0, 0, 0), (int(cx - 8 * k), int(cy - 6 * k)), max(1, int(2.4 * k)))
    pygame.draw.circle(surface, (0, 0, 0), (int(cx + 8 * k), int(cy - 6 * k)), max(1, int(2.4 * k)))
    pygame.draw.circle(surface, (20, 18, 17), (int(cx - 3 * k), int(cy + 8 * k)), max(1, int(1.8 * k)))
    pygame.draw.circle(surface, (20, 18, 17), (int(cx + 3 * k), int(cy + 8 * k)), max(1, int(1.8 * k)))
    pygame.draw.arc(
        surface,
        (20, 18, 17),
        pygame.Rect(int(cx - 6 * k), int(cy + 10 * k), int(12 * k), int(8 * k)),
        math.pi,
        2 * math.pi,
        max(1, int(1.5 * k)),
    )
    draw_crown(surface, cx, cy - 31 * k, 34 * k)


def draw_speaker(surface, cx, cy, size, muted, color=(52, 211, 153)) -> None:
    k = size / 20.0
    if muted:
        color = (248, 113, 113)
    body = _scaled([(-8, -3), (-4, -3), (1, -8), (1, 8), (-4, 3), (-8, 3)], cx, cy, k)
    pygame.draw.polygon(surface, color, body)
    if muted:
        pygame.draw.line(surface, color, (cx + 4 * k, cy - 4 * k), (cx + 10 * k, cy + 4 * k), max(2, int(2 * k)))
        pygame.draw.line(surface, color, (cx + 10 * k, cy - 4 * k), (cx + 4 * k, cy + 4 * k), max(2, int(2 * k)))
    else:
        pygame.draw.arc(surface, color, pygame.Rect(int(cx - 2 * k), int(cy - 5 * k), int(10 * k), int(10 * k)), -1.0, 1.0, max(2, int(2 * k)))
        pygame.draw.arc(surface, color, pygame.Rect(int(cx - 5 * k), int(cy - 9 * k), int(18 * k), int(18 * k)), -1.0, 1.0, max(2, int(2 * k)))


def draw_play(surface, cx, cy, size, color=(229, 229, 229)) -> None:
    k = size / 20.0
    pygame.draw.polygon(surface, color, _scaled([(-5, -8), (-5, 8), (8, 0)], cx, cy, k))


def draw_pause(surface, cx, cy, size, color=(229, 229, 229)) -> None:
    k = size / 20.0
    pygame.draw.rect(surface, color, pygame.Rect(int(cx - 6 * k), int(cy - 7 * k), int(4 * k), int(14 * k)))
    pygame.draw.rect(surface, color, pygame.Rect(int(cx + 2 * k), int(cy - 7 * k), int(4 * k), int(14 * k)))


def draw_restart(surface, cx, cy, size, color=(229, 229, 229)) -> None:
    k = size / 20.0
    rect = pygame.Rect(int(cx - 8 * k), int(cy - 8 * k), int(16 * k), int(16 * k))
    pygame.draw.arc(surface, color, rect, 0.6, 5.6, max(2, int(2 * k)))
    pygame.draw.polygon(surface, color, _scaled([(2, -12), (2, -4), (-5, -8)], cx, cy, k))


def draw_home(surface, cx, cy, size, color=(229, 229, 229)) -> None:
    k = size / 20.0
    pygame.draw.polygon(surface, color, _scaled([(-9, 0), (0, -9), (9, 0)], cx, cy, k))
    pygame.draw.rect(surface, color, pygame.Rect(int(cx - 6 * k), int(cy), int(12 * k), int(8 * k)))


def draw_book(surface, cx, cy, size, color=(229, 229, 229)) -> None:
    k = size / 20.0
    pygame.draw.rect(surface, color, pygame.Rect(int(cx - 9 * k), int(cy - 7 * k), int(8 * k), int(14 * k)), 2)
    pygame.draw.rect(surface, color, pygame.Rect(int(cx + 1 * k), int(cy - 7 * k), int(8 * k), int(14 * k)), 2)


def draw_trophy(surface, cx, cy, size) -> None:
    k = size / 30.0
    gold = (251, 191, 36)
    pygame.draw.polygon(surface, gold, _scaled([(-10, -12), (10, -12), (8, 2), (0, 8), (-8, 2)], cx, cy, k))
    pygame.draw.arc(surface, gold, pygame.Rect(int(cx - 17 * k), int(cy - 11 * k), int(12 * k), int(12 * k)), math.pi / 2, 3 * math.pi / 2, max(2, int(2 * k)))
    pygame.draw.arc(surface, gold, pygame.Rect(int(cx + 5 * k), int(cy - 11 * k), int(12 * k), int(12 * k)), -math.pi / 2, math.pi / 2, max(2, int(2 * k)))
    pygame.draw.rect(surface, gold, pygame.Rect(int(cx - 2 * k), int(cy + 7 * k), int(4 * k), int(6 * k)))
    pygame.draw.rect(surface, gold, pygame.Rect(int(cx - 8 * k), int(cy + 12 * k), int(16 * k), int(4 * k)))


def draw_info(surface, cx, cy, size, color=(163, 163, 163)) -> None:
    pygame.draw.circle(surface, color, (int(cx), int(cy)), int(size / 2), 2)
    pygame.draw.circle(surface, color, (int(cx), int(cy - size * 0.2)), max(1, int(size * 0.07)))
    pygame.draw.line(surface, color, (cx, cy - size * 0.05), (cx, cy + size * 0.25), 2)


def draw_arrow(surface, cx, cy, size, direction, color=(229, 229, 229)) -> None:
    k = size / 20.0
    base = {
        "up": [(0, -7), (-7, 6), (7, 6)],
        "down": [(0, 7), (-7, -6), (7, -6)],
        "left": [(-7, 0), (6, -7), (6, 7)],
        "right": [(7, 0), (-6, -7), (-6, 7)],
    }[direction]
    pygame.draw.polygon(surface, color, _scaled(base, cx, cy, k))
