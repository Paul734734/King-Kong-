import math
import random
from typing import Callable, List, Tuple

import pygame

from .. import ui
from ..game import sprites
from ..game.levels import LevelDefinition

CONFETTI_COLORS = [(245, 158, 11), (251, 191, 36), (34, 197, 94), (239, 68, 68), (255, 255, 255)]


class Confetto:
    def __init__(self, origin: Tuple[float, float]):
        angle = math.radians(random.uniform(200, 340))
        speed = random.uniform(220, 520)
        self.x, self.y = origin
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = random.choice(CONFETTI_COLORS)
        self.size = random.uniform(4, 8)
        self.life = random.uniform(1.4, 2.4)

    def update(self, dt: float) -> None:
        self.vy += 520 * dt
        self.vx *= 0.99
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt


class VictoryModal(ui.Modal):
    PANEL_WIDTH = 520
    PANEL_HEIGHT = 560

    def __init__(
        self,
        level: LevelDefinition,
        time_seconds: float,
        lives_remaining: int,
        bonus_collected: int,
        score: int,
        stars: int,
        on_next_level: Callable[[], None],
        on_replay: Callable[[], None],
        on_home: Callable[[], None],
        is_final_level: bool,
    ):
        super().__init__()
        self.level = level
        self.time_seconds = time_seconds
        self.lives_remaining = lives_remaining
        self.bonus_collected = bonus_collected
        self.score = score
        self.stars = stars
        self.is_final_level = is_final_level
        self.confetti: List[Confetto] = []
        self.spawned = False
        if is_final_level:
            self.primary = ui.Button(
                "Couronnement & Accueil", on_home, "primary",
                icon=lambda s, x, y, z: sprites.draw_trophy(s, x, y, z + 10),
            )
        else:
            self.primary = ui.Button(
                "Niveau Suivant", on_next_level, "primary",
                icon=lambda s, x, y, z: sprites.draw_arrow(s, x, y, z, "right", (23, 23, 23)),
            )
        self.replay = ui.Button(
            "Rejouer", on_replay, "secondary", icon=lambda s, x, y, z: sprites.draw_restart(s, x, y, z)
        )
        self.home = ui.Button(
            "Menu", on_home, "secondary", icon=lambda s, x, y, z: sprites.draw_home(s, x, y, z)
        )
        self.buttons = [self.primary, self.replay, self.home]

    def layout(self, size: Tuple[int, int]) -> None:
        panel = self.panel_rect(size)
        x = panel.x + 40
        w = panel.width - 80
        self.primary.place(x, panel.y + 436, w, 52)
        self.replay.place(x, panel.y + 498, (w - 10) // 2, 44)
        self.home.place(x + (w - 10) // 2 + 10, panel.y + 498, (w - 10) // 2, 44)

    def update(self, dt: float) -> None:
        for piece in self.confetti:
            piece.update(dt)
        self.confetti = [p for p in self.confetti if p.life > 0]

    def render(self, surface: pygame.Surface) -> None:
        w, h = surface.get_size()
        panel = self.panel_rect((w, h))
        if not self.spawned:
            self.spawned = True
            for origin_x in (w * 0.3, w * 0.7):
                for _ in range(45):
                    self.confetti.append(Confetto((origin_x, h * 0.65)))
        ui.draw_panel(surface, panel, (23, 23, 23, 250), (245, 158, 11, 170), 18, 2)

        if self.is_final_level:
            sprites.draw_trophy(surface, panel.centerx, panel.y + 56, 64)
        else:
            sprites.draw_crown(surface, panel.centerx, panel.y + 56, 64)
        title = "VICTOIRE ROYALE ABSOLUE !" if self.is_final_level else "FÉLICITATIONS MAJESTÉ !"
        ui.draw_text(surface, title, ui.Fonts.get(28, True, "serif"), ui.AMBER_300, (panel.centerx, panel.y + 112), "center")
        message = (
            "Vous avez triomphé des 5 Labyrinthes Royaux et reconquis le Trône Doré !"
            if self.is_final_level
            else f"Vous avez rassemblé les 5 bananes du {self.level.title} sans mourir !"
        )
        font = ui.Fonts.get(14)
        lines = ui.wrap_text(message, font, panel.width - 100)
        for index, line in enumerate(lines[:3]):
            ui.draw_text(surface, line, font, ui.NEUTRAL_400, (panel.centerx, panel.y + 146 + index * 20), "center")

        ui.stars_row(surface, panel.centerx, panel.y + 224, self.stars, 18, 10)

        mins = int(self.time_seconds // 60)
        secs = int(self.time_seconds % 60)
        lives_text = f"{self.lives_remaining} vie{'s' if self.lives_remaining > 1 else ''}"
        rows = [
            ("Bananes Récoltées", "5 / 5 (Parfait)", "banana"),
            ("Temps d'Évasion", f"{mins}m {secs}s", None),
            ("Cœurs Préservés", lives_text, "heart"),
            ("Score du Niveau", ui.format_thousands(self.score), "star"),
        ]
        for index, (label, value, icon) in enumerate(rows):
            row = pygame.Rect(panel.x + 40, panel.y + 262 + index * 42, panel.width - 80, 36)
            ui.draw_panel(surface, row, (38, 38, 38, 255), ui.NEUTRAL_700, 8, 1)
            ui.draw_text(surface, label, ui.Fonts.get(14), ui.NEUTRAL_400, (row.x + 14, row.centery), "midleft")
            vx = row.right - 14
            vfont = ui.Fonts.get(15, True, "mono")
            vw = vfont.size(value)[0]
            ui.draw_text(surface, value, vfont, ui.AMBER_300, (vx, row.centery), "midright")
            if icon == "banana":
                sprites.draw_banana(surface, vx - vw - 16, row.centery, 18)
            elif icon == "heart":
                sprites.draw_heart(surface, vx - vw - 16, row.centery, 16)
            elif icon == "star":
                sprites.draw_star(surface, vx - vw - 16, row.centery, 8, True)

    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface)
        for piece in self.confetti:
            pygame.draw.rect(
                surface,
                piece.color,
                (int(piece.x), int(piece.y), int(piece.size), int(piece.size * 0.6)),
            )
