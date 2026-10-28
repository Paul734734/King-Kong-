from typing import Callable, List, Tuple

import pygame

from .. import ui
from ..game import sprites
from ..game.levels import LEVELS
from ..game.storage import SaveStore


class LevelSelectModal(ui.Modal):
    PANEL_WIDTH = 640
    PANEL_HEIGHT = 640

    def __init__(self, store: SaveStore, on_close: Callable[[], None], on_select_level: Callable[[int], None]):
        super().__init__()
        self.store = store
        self.on_select_level = on_select_level
        self.close = ui.Button("Fermer", on_close, "secondary")
        self.level_buttons: List[ui.Button] = []
        for level in LEVELS:
            unlocked = level.id == 1 or self.store.get_level(level.id - 1).completed
            button = ui.Button(
                "Jouer" if unlocked else "Verrouillé",
                (lambda lid=level.id: self.on_select_level(lid)),
                "primary" if unlocked else "secondary",
                font_size=14,
                enabled=unlocked,
            )
            self.level_buttons.append(button)
        self.buttons = self.level_buttons + [self.close]

    def refresh(self) -> None:
        for level, button in zip(LEVELS, self.level_buttons):
            unlocked = level.id == 1 or self.store.get_level(level.id - 1).completed
            button.enabled = unlocked
            button.variant = "primary" if unlocked else "secondary"
            button.label = "Jouer" if unlocked else "Verrouillé"

    def row_rect(self, panel: pygame.Rect, index: int) -> pygame.Rect:
        return pygame.Rect(panel.x + 28, panel.y + 84 + index * 90, panel.width - 56, 80)

    def layout(self, size: Tuple[int, int]) -> None:
        panel = self.panel_rect(size)
        self.refresh()
        for index, button in enumerate(self.level_buttons):
            row = self.row_rect(panel, index)
            button.place(row.right - 130, row.centery - 20, 112, 40)
        self.close.place(panel.centerx - 70, panel.bottom - 56, 140, 40)

    def render(self, surface: pygame.Surface) -> None:
        panel = self.panel_rect(surface.get_size())
        ui.draw_panel(surface, panel, (23, 23, 23, 250), (245, 158, 11, 140), 18, 2)
        ui.draw_text(
            surface,
            "Sélection des Labyrinthes Royaux",
            ui.Fonts.get(24, True, "serif"),
            ui.AMBER_300,
            (panel.centerx, panel.y + 44),
            "center",
        )
        for index, level in enumerate(LEVELS):
            row = self.row_rect(panel, index)
            data = self.store.get_level(level.id)
            unlocked = level.id == 1 or self.store.get_level(level.id - 1).completed
            wall = ui.hex_to_rgb(level.wall_color)
            accent = ui.hex_to_rgb(level.accent_color)
            ui.draw_panel(
                surface,
                row,
                (38, 38, 38, 255) if unlocked else (28, 28, 28, 255),
                (*accent, 200) if unlocked else ui.NEUTRAL_800,
                12,
                1,
            )
            badge = pygame.Rect(row.x + 14, row.centery - 26, 52, 52)
            ui.draw_panel(surface, badge, (*wall, 255) if unlocked else (38, 38, 38, 255), (*accent, 255) if unlocked else ui.NEUTRAL_700, 12, 2)
            if unlocked:
                ui.draw_text(surface, str(level.id), ui.Fonts.get(24, True, "serif"), accent, badge.center, "center")
            else:
                sprites.draw_lock(surface, badge.centerx, badge.centery, 20)
            title_color = ui.NEUTRAL_200 if unlocked else ui.NEUTRAL_500
            ui.draw_text(surface, level.title, ui.Fonts.get(14, True), title_color, (badge.right + 14, row.y + 12))
            if unlocked:
                for star in range(3):
                    sprites.draw_star(surface, badge.right + 22 + star * 24, row.y + 46, 9, star < data.stars)
                if data.high_score > 0:
                    ui.draw_text(
                        surface,
                        f"Record : {ui.format_thousands(data.high_score)} pts",
                        ui.Fonts.get(12),
                        ui.AMBER_300,
                        (badge.right + 100, row.y + 46),
                        "midleft",
                    )
            else:
                ui.draw_text(
                    surface,
                    f"Verrouillé (Complétez le Niveau {level.id - 1})",
                    ui.Fonts.get(12),
                    ui.NEUTRAL_500,
                    (badge.right + 14, row.y + 46),
                    "midleft",
                )
