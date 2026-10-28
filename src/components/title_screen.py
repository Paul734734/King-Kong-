from typing import Callable, Tuple

import pygame

from .. import ui
from ..game import sprites
from ..game.storage import SaveStore


class TitleScreen:
    def __init__(
        self,
        store: SaveStore,
        on_start_game: Callable[[int], None],
        on_open_level_select: Callable[[], None],
        on_open_maquette: Callable[[], None],
        on_open_rules: Callable[[], None],
        on_toggle_mute: Callable[[], None],
        is_muted: Callable[[], bool],
    ):
        self.store = store
        self.is_muted = is_muted
        self.play = ui.Button(
            "LANCER LA QUÊTE", lambda: on_start_game(1), "primary", font_size=22
        )
        self.levels = ui.Button("Niveaux (1-5)", on_open_level_select, "secondary", font_size=17)
        self.maquette = ui.Button(
            "Maquette & Cahier des Charges", on_open_maquette, "ghost", font_size=14, bold=False
        )
        self.rules = ui.Button("Règles & Contrôles", on_open_rules, "ghost", font_size=14, bold=False)
        self.mute = ui.Button(
            "",
            on_toggle_mute,
            "icon",
            icon=lambda s, cx, cy, size: sprites.draw_speaker(s, cx, cy, size + 8, self.is_muted()),
        )
        self.buttons = [self.play, self.levels, self.maquette, self.rules, self.mute]

    def layout(self, size: Tuple[int, int]) -> None:
        w, h = size
        cx = w // 2
        top = max(150, h // 2 - 230)
        self.mute.place(w - 64, 16, 44, 44)
        self.play.place(cx - 190, top + 330, 380, 62)
        self.levels.place(cx - 190, top + 404, 380, 48)
        self.maquette.place(cx - 250, top + 464, 270, 34)
        self.rules.place(cx + 30, top + 464, 200, 34)

    def draw(self, surface: pygame.Surface) -> None:
        self.layout(surface.get_size())
        w, h = surface.get_size()
        cx = w // 2
        top = max(150, h // 2 - 230)
        surface.fill(ui.NEUTRAL_950)
        sprites.blend_circle(surface, (245, 158, 11), (cx, top + 80), 260, 22)
        sprites.blend_circle(surface, (217, 119, 6), (cx - 300, h - 60), 220, 14)
        sprites.blend_circle(surface, (124, 58, 237), (cx + 340, top + 20), 200, 12)

        star_bar = pygame.Rect(16, 16, 280, 44)
        ui.draw_panel(surface, star_bar, (23, 23, 23, 220), ui.NEUTRAL_700, 12)
        sprites.draw_star(surface, star_bar.x + 24, star_bar.centery, 11, True)
        ui.draw_text(
            surface,
            f"{self.store.total_stars} / 15",
            ui.Fonts.get(17, True, "serif"),
            ui.AMBER_300,
            (star_bar.x + 44, star_bar.centery),
            "midleft",
        )
        ui.draw_text(
            surface,
            f"Score : {ui.format_thousands(self.store.total_score)}",
            ui.Fonts.get(14, False, "mono"),
            ui.NEUTRAL_400,
            (star_bar.x + 136, star_bar.centery),
            "midleft",
        )

        crest = pygame.Rect(0, 0, 110, 110)
        crest.center = (cx, top + 20)
        ui.draw_panel(surface, crest, (28, 25, 23, 255), ui.AMBER_500, 26, 3)
        sprites.draw_gorilla_face(surface, crest.centerx, crest.centery + 12, 64)
        sprites.draw_banana(surface, crest.right - 6, crest.bottom - 4, 34)

        ui.draw_gradient_text_title(surface, "KING KONG LABYRINTH", 54, (cx, top + 120))
        ui.draw_text(
            surface,
            "La Quête des 5 Bananes Sacrées du Royaume Perdu",
            ui.Fonts.get(18, False),
            (253, 230, 138),
            (cx, top + 170),
            "center",
        )

        badge = pygame.Rect(0, 0, 600, 44)
        badge.center = (cx, top + 235)
        ui.draw_panel(surface, badge, (245, 158, 11, 30), (245, 158, 11, 110), 22, 1)
        ui.draw_text(
            surface,
            "Objectif : Récoltez 5 Bananes dorées sans succomber pour ouvrir la porte !",
            ui.Fonts.get(15, False),
            ui.AMBER_200,
            badge.center,
            "center",
        )

        for button in self.buttons:
            button.draw(surface)
        ui.draw_text(
            surface,
            "·",
            ui.Fonts.get(16),
            ui.NEUTRAL_700,
            (self.rules.rect.left - 10, self.rules.rect.centery),
            "center",
        )
        ui.draw_text(
            surface,
            "ZQSD / Flèches pour diriger le Roi · Touche Espace ou Entrée pour Jouer",
            ui.Fonts.get(13),
            ui.NEUTRAL_500,
            (cx, h - 26),
            "center",
        )

    def handle_event(self, event: pygame.event.Event, size: Tuple[int, int]) -> bool:
        self.layout(size)
        for button in self.buttons:
            if button.handle_event(event):
                return True
        return False
