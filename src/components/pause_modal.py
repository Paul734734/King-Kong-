from typing import Callable, Tuple

import pygame

from .. import ui
from ..game import sprites
from ..game.levels import LevelDefinition


class PauseModal(ui.Modal):
    PANEL_WIDTH = 480
    PANEL_HEIGHT = 470

    def __init__(
        self,
        level: LevelDefinition,
        bananas: int,
        lives: int,
        elapsed_seconds: float,
        on_resume: Callable[[], None],
        on_restart: Callable[[], None],
        on_home: Callable[[], None],
        on_open_maquette: Callable[[], None],
        on_toggle_mute: Callable[[], None],
        is_muted: Callable[[], bool],
    ):
        super().__init__()
        self.level = level
        self.bananas = bananas
        self.lives = lives
        self.elapsed_seconds = elapsed_seconds
        self.is_muted = is_muted
        self.resume = ui.Button(
            "Reprendre la Partie (P)", on_resume, "primary",
            icon=lambda s, x, y, z: sprites.draw_play(s, x, y, z, (23, 23, 23)),
        )
        self.restart = ui.Button(
            "Recommencer le Niveau (R)", on_restart, "secondary",
            icon=lambda s, x, y, z: sprites.draw_restart(s, x, y, z),
        )
        self.maquette = ui.Button(
            "Consulter la Maquette (GDD)", on_open_maquette, "secondary",
            icon=lambda s, x, y, z: sprites.draw_book(s, x, y, z),
        )
        self.mute = ui.Button(
            "", on_toggle_mute, "secondary",
            icon=lambda s, x, y, z: sprites.draw_speaker(s, x, y, z + 4, self.is_muted()),
        )
        self.home = ui.Button(
            "Menu Principal", on_home, "ghost",
            icon=lambda s, x, y, z: sprites.draw_home(s, x, y, z, ui.NEUTRAL_400),
        )
        self.buttons = [self.resume, self.restart, self.maquette, self.mute, self.home]

    def layout(self, size: Tuple[int, int]) -> None:
        panel = self.panel_rect(size)
        x = panel.x + 40
        w = panel.width - 80
        self.resume.place(x, panel.y + 190, w, 48)
        self.restart.place(x, panel.y + 248, w, 44)
        self.maquette.place(x, panel.y + 300, w, 44)
        self.mute.place(x, panel.y + 352, 52, 44)
        self.mute.label = "Son Coupé" if self.is_muted() else "Son Actif"
        self.mute.rect.width = w
        self.home.place(x, panel.y + 404, w, 40)

    def render(self, surface: pygame.Surface) -> None:
        panel = self.panel_rect(surface.get_size())
        ui.draw_panel(surface, panel, (23, 23, 23, 250), (245, 158, 11, 140), 18, 2)
        ui.draw_text(surface, "PAUSE ROYALE", ui.Fonts.get(30, True, "serif"), ui.AMBER_300, (panel.centerx, panel.y + 40), "center")
        ui.draw_text(surface, self.level.title, ui.Fonts.get(14), ui.NEUTRAL_400, (panel.centerx, panel.y + 76), "center")
        stats = [
            ("BANANES", f"{self.bananas}/5", sprites.draw_banana),
            ("VIES", str(self.lives), sprites.draw_heart),
            ("CHRONO", ui.format_clock(self.elapsed_seconds), None),
        ]
        cell_w = (panel.width - 80 - 20) // 3
        for index, (label, value, icon) in enumerate(stats):
            cell = pygame.Rect(panel.x + 40 + index * (cell_w + 10), panel.y + 104, cell_w, 66)
            ui.draw_panel(surface, cell, (38, 38, 38, 255), ui.NEUTRAL_700, 10, 1)
            ui.draw_text(surface, label, ui.Fonts.get(11, True), ui.NEUTRAL_400, (cell.centerx, cell.y + 14), "center")
            if icon:
                icon(surface, cell.centerx - 28, cell.y + 44, 20)
                ui.draw_text(surface, value, ui.Fonts.get(18, True, "mono"), ui.NEUTRAL_200, (cell.centerx - 10, cell.y + 44), "midleft")
            else:
                ui.draw_text(surface, value, ui.Fonts.get(18, True, "mono"), ui.NEUTRAL_200, (cell.centerx, cell.y + 44), "center")
