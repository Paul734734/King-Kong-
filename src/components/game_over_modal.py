from typing import Callable, Tuple

import pygame

from .. import ui
from ..game import sprites
from ..game.levels import LevelDefinition


class GameOverModal(ui.Modal):
    PANEL_WIDTH = 500
    PANEL_HEIGHT = 480

    def __init__(
        self,
        level: LevelDefinition,
        reason: str,
        bananas_collected: int,
        on_retry: Callable[[], None],
        on_home: Callable[[], None],
        on_open_maquette: Callable[[], None],
    ):
        super().__init__()
        self.level = level
        self.reason = reason or "Submergé par les pièges du labyrinthe"
        self.bananas_collected = bananas_collected
        self.retry = ui.Button(
            "Réessayer Immédiatement", on_retry, "danger",
            icon=lambda s, x, y, z: sprites.draw_restart(s, x, y, z, (255, 255, 255)),
        )
        self.home = ui.Button(
            "Menu", on_home, "secondary",
            icon=lambda s, x, y, z: sprites.draw_home(s, x, y, z),
        )
        self.help = ui.Button(
            "Consulter les astuces et la maquette", on_open_maquette, "ghost", font_size=14, bold=False,
            icon=lambda s, x, y, z: sprites.draw_info(s, x, y, z - 4),
        )
        self.buttons = [self.retry, self.home, self.help]

    def layout(self, size: Tuple[int, int]) -> None:
        panel = self.panel_rect(size)
        x = panel.x + 40
        w = panel.width - 80
        self.retry.place(x, panel.y + 300, w, 52)
        self.home.place(x, panel.y + 362, w, 44)
        self.help.place(x, panel.y + 420, w, 36)

    def render(self, surface: pygame.Surface) -> None:
        panel = self.panel_rect(surface.get_size())
        ui.draw_panel(surface, panel, (23, 23, 23, 250), (239, 68, 68, 170), 18, 2)
        circle = (panel.centerx, panel.y + 70)
        sprites.blend_circle(surface, (239, 68, 68), circle, 44, 50)
        sprites.draw_skull(surface, circle[0], circle[1], 50)
        ui.draw_text(surface, "LE ROI EST TOMBÉ !", ui.Fonts.get(30, True, "serif"), ui.RED_400, (panel.centerx, panel.y + 138), "center")
        ui.draw_text(surface, self.level.title, ui.Fonts.get(14), ui.NEUTRAL_400, (panel.centerx, panel.y + 172), "center")
        box = pygame.Rect(panel.x + 40, panel.y + 198, panel.width - 80, 84)
        ui.draw_panel(surface, box, (38, 38, 38, 255), ui.NEUTRAL_700, 10, 1)
        ui.draw_text(surface, "Cause :", ui.Fonts.get(14, True), ui.NEUTRAL_400, (box.x + 16, box.y + 14))
        ui.draw_wrapped(surface, self.reason, ui.Fonts.get(14), ui.NEUTRAL_200, box.x + 80, box.y + 14, box.width - 96)
        ui.draw_text(surface, "Bananes Récoltées :", ui.Fonts.get(14, True), ui.NEUTRAL_400, (box.x + 16, box.bottom - 24))
        sprites.draw_banana(surface, box.x + 190, box.bottom - 16, 18)
        ui.draw_text(surface, f"{self.bananas_collected} / 5", ui.Fonts.get(14, True, "mono"), ui.AMBER_300, (box.x + 204, box.bottom - 24))
