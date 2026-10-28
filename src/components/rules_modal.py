from typing import Callable, Tuple

import pygame

from .. import ui
from ..game import sprites


class RulesModal(ui.Modal):
    PANEL_WIDTH = 640
    PANEL_HEIGHT = 600

    SECTIONS = [
        (
            "banana",
            "Objectif Clé : 5 Bananes par Niveau",
            "Chaque niveau contient exactement 5 bananes sacrées. L'Arche Royale reste scellée tant que les 5 bananes ne sont pas en votre possession.",
        ),
        (
            "heart",
            "Système de Vies (3 Cœurs Royaux)",
            "Vous commencez avec 3 cœurs. Toucher un piège actif ou un ennemi vous fait perdre 1 vie avec un temps d'invulnérabilité de 1,8s. Trouvez des cœurs bonus pour vous régénérer jusqu'à 5 vies !",
        ),
        (
            "shield",
            "Bouclier & Vitesse",
            "Le Bouclier d'Ananas absorbe entièrement le prochain coup sans perte de cœur. Les éclairs dorés vous accordent un boost de vitesse temporaire.",
        ),
        (
            "crown",
            "Contrôles",
            "Clavier : touches ZQSD ou flèches directionnelles (WASD fonctionne aussi). Souris : D-Pad virtuel en bas à droite de l'écran. P ou Échap pour la pause, R pour recommencer, M pour couper le son.",
        ),
    ]

    def __init__(self, on_close: Callable[[], None]):
        super().__init__()
        self.close = ui.Button("Compris, Majesté !", on_close, "primary")
        self.buttons = [self.close]

    def layout(self, size: Tuple[int, int]) -> None:
        panel = self.panel_rect(size)
        self.close.place(panel.centerx - 130, panel.bottom - 64, 260, 46)

    def render(self, surface: pygame.Surface) -> None:
        panel = self.panel_rect(surface.get_size())
        ui.draw_panel(surface, panel, (23, 23, 23, 250), (245, 158, 11, 140), 18, 2)
        ui.draw_text(surface, "Règles du Jeu & Guide de Survie", ui.Fonts.get(24, True, "serif"), ui.AMBER_300, (panel.centerx, panel.y + 44), "center")
        y = panel.y + 90
        body = ui.Fonts.get(14)
        for icon, title, text in self.SECTIONS:
            box_h = 22 + 8 + ui.measure_wrapped(text, body, panel.width - 150) + 16
            box = pygame.Rect(panel.x + 28, y, panel.width - 56, box_h)
            ui.draw_panel(surface, box, (38, 38, 38, 255), ui.NEUTRAL_700, 12, 1)
            cx, cy = box.x + 36, box.y + 36
            if icon == "banana":
                sprites.draw_banana(surface, cx, cy, 30)
            elif icon == "heart":
                sprites.draw_heart(surface, cx, cy, 28)
            elif icon == "shield":
                sprites.draw_shield(surface, cx, cy, 28)
            else:
                sprites.draw_crown(surface, cx, cy, 28)
            ui.draw_text(surface, title, ui.Fonts.get(16, True), ui.AMBER_300, (box.x + 74, box.y + 10))
            ui.draw_wrapped(surface, text, body, ui.NEUTRAL_400, box.x + 74, box.y + 36, box.width - 94)
            y += box_h + 12
