from typing import Callable, Dict, List, Tuple

import pygame

from .. import ui
from ..game import sprites
from ..game.levels import LEVELS

TABS: List[Tuple[str, str]] = [
    ("concept", "Concept & Lore"),
    ("gameplay", "Boucle de Gameplay (5 bananes)"),
    ("personnage", "King (Le Roi)"),
    ("ennemis", "Ennemis & Pièges"),
    ("niveaux", "5 Labyrinthes"),
    ("economie", "Vies & Économie"),
]

CONTENT: Dict[str, List[tuple]] = {
    "concept": [
        ("h1", "Le Pitch Royal : La Renaissance du Roi Kong"),
        (
            "p",
            "Autrefois souverain vénéré de la Cité des Canopées, le légendaire Roi Kong a vu son royaume scellé par une malédiction ancestrale. Pour briser le maléfice et reprendre sa place sur le Trône Doré, King doit s'aventurer dans une succession de 5 labyrinthes séculaires truffés de périls mortels et ramener les 5 Bananes Sacrées de chaque dynastie.",
        ),
        ("h", "Labyrinthes Méticuleux"),
        (
            "p",
            "Des architectures labyrinthiques variées avec carrefours stratégiques, chemins à risques et alcoves secrètes dissimulant des bonus de survie.",
        ),
        ("h", "Objectif Précis (5 bananes)"),
        (
            "p",
            "Rassemblez exactement 5 bananes dorées par niveau. Aucune sortie n'est possible sans ce tribut complet, forçant le joueur à explorer l'intégralité du dédale !",
        ),
        ("h", "Récompenses & Félicitations"),
        (
            "p",
            "Notation par étoiles (1 à 3 étoiles royales), calcul de score par chrono et vies restantes, et célébration festive de confettis dorés au sanctuaire.",
        ),
    ],
    "gameplay": [
        ("h1", "La Boucle de Gameplay Principale (Core Loop)"),
        ("h", "Étape 1 : Infiltration & Découverte du Labyrinthe"),
        (
            "p",
            "King apparaît au point d'entrée sécurisé. Le joueur observe la disposition des couloirs, repère les lueurs des bananes dorées et planifie son itinéraire en évitant les pièges visibles.",
        ),
        ("h", "Étape 2 : Évitement Actif des Dangers"),
        (
            "p",
            "Synchronisation avec les cycles des pics au sol (télégraphiés 0.5s avant sortie) et anticipation des trajectoires de patrouille des serpents et chauves-souris.",
        ),
        ("h", "Étape 3 : Moisson des 5 Bananes Sacrées"),
        (
            "p",
            "Chaque banane déclenche un arpège sonore triomphal et incrémente le compteur HUD (1/5 ... 5/5). Dès la 5ème banane obtenue, un signal doré prévient le joueur que l'Arche Royale est descellée.",
        ),
        ("h", "Étape 4 : Exfiltration vers l'Arche du Sanctuaire"),
        (
            "p",
            "Le joueur doit retourner vivant vers la sortie illuminée. Franchir le portail déclenche le décompte de score, l'écran de félicitations et déverrouille le monde suivant.",
        ),
    ],
    "personnage": [
        ("h1", "King Kong (Sa Majesté le Roi)"),
        (
            "p",
            "Grand singe royal au dos argenté, coiffé de la Couronne d'Or à rubis impériaux et drapé de sa cape pourpre carmin.",
        ),
        ("li", "Vitesse : 3.0 cases/s (4.5 en boost)"),
        ("li", "Vies : 3 cœurs (extensible à 5)"),
        ("li", "Bouclier : Absorption de choc"),
        ("h", "Mécanique de Bouclier d'Ananas"),
        (
            "p",
            "Lorsqu'il ramasse un bouclier, une bulle d'énergie céleste protège le Roi. Le prochain impact subi (piège ou monstre) est totalement annulé et le bouclier se dissipe sans retirer de cœur.",
        ),
        ("h", "Période d'Invulnérabilité (Grace Frames)"),
        (
            "p",
            "Après chaque coup reçu, King clignote pendant 1,8 seconde durant laquelle aucun nouveau dégât ne peut être infligé, permettant de fuir un piège actif ou un groupe d'ennemis.",
        ),
    ],
    "ennemis": [
        ("h1", "Bestiaire des Ennemis & Pièges"),
        ("icon_h", "snake", "Vipères & Serpents à Sonnette"),
        ("p", "Patrouillent les corridors en ligne droite. Mouvement fluide, inflige 1 dégât au contact."),
        ("icon_h", "bat", "Chauves-souris Prédatrices"),
        (
            "p",
            "Vol rapide et saccadé le long d'axes verticaux ou horizontaux. Vitesse élevée nécessitant un timing précis.",
        ),
        ("icon_h", "skull", "Gardes Squelettes Royaux"),
        (
            "p",
            "Anciennes sentinelles impériales en armure qui montent la garde devant les intersections majeures.",
        ),
        ("icon_h", "plant", "Plantes Carnivores Voraces"),
        (
            "p",
            "Obstacles vivants stationnaires dont les mâchoires claquent pour verrouiller les couloirs étroits.",
        ),
        ("icon_h", "bolt", "Dalles de Pics Rétractables"),
        (
            "p",
            "Pièges cycliques. Un voyant d'armement jaune/rouge s'allume 0,5s avant l'éjection foudroyante des pointes en acier.",
        ),
        ("icon_h", "fire", "Geysers de Feu & Magma"),
        (
            "p",
            "Fissures au sol crachant des colonnes de feu incandescentes. L'aura orange annonce l'embrasement imminent.",
        ),
    ],
    "niveaux": [("h1", "Architecture des 5 Niveaux Conçus")] + [("level", level) for level in LEVELS],
    "economie": [
        ("h1", "Système de Vies, Score & Récompenses Royales"),
        ("h", "Formule de Calcul du Score"),
        ("li", "5 Bananes : +5 000 pts (1 000 pts / banane)"),
        ("li", "Bonus Temps : jusqu'à +3 000 pts (dégressif selon les secondes)"),
        ("li", "Cœurs Préservés : +800 pts par cœur intact"),
        ("li", "Objets Secrets : +500 pts par cœur ou bouclier récolté"),
        ("h", "Attribution des Étoiles Royales"),
        ("star_row", 3, "3 Étoiles : 3 cœurs restants + temps < 60 secondes"),
        ("star_row", 2, "2 Étoiles : au moins 2 cœurs restants + temps < 120 secondes"),
        ("star_row", 1, "1 Étoile : niveau complété avec 5 bananes"),
    ],
}


class MaquetteModal(ui.Modal):
    PANEL_WIDTH = 860
    PANEL_HEIGHT = 640

    def __init__(self, on_close: Callable[[], None]):
        super().__init__()
        self.active_tab = "concept"
        self.scroll = 0
        self.close = ui.Button("Fermer la Documentation", on_close, "primary")
        self.tab_rects: Dict[str, pygame.Rect] = {}
        self.content_cache: Dict[Tuple[str, int], pygame.Surface] = {}
        self.content_rect = pygame.Rect(0, 0, 0, 0)
        self.buttons = [self.close]

    def layout(self, size: Tuple[int, int]) -> None:
        panel = self.panel_rect(size)
        self.close.place(panel.right - 260, panel.bottom - 54, 230, 40)
        x = panel.x + 24
        y = panel.y + 78
        self.tab_rects = {}
        font = ui.Fonts.get(13, True)
        for key, label in TABS:
            width = font.size(label)[0] + 26
            if x + width > panel.right - 24:
                x = panel.x + 24
                y += 36
            self.tab_rects[key] = pygame.Rect(x, y, width, 30)
            x += width + 8
        top = y + 44
        self.content_rect = pygame.Rect(panel.x + 24, top, panel.width - 48, panel.bottom - 70 - top)

    def _build_content(self, key: str, width: int) -> pygame.Surface:
        blocks = CONTENT[key]
        h1 = ui.Fonts.get(20, True, "serif")
        h = ui.Fonts.get(16, True)
        p = ui.Fonts.get(14)
        inner = width - 8
        height = 10
        for block in blocks:
            kind = block[0]
            if kind == "h1":
                height += h1.get_linesize() + 14
            elif kind == "h":
                height += h.get_linesize() + 6
            elif kind == "icon_h":
                height += 34
            elif kind == "p":
                height += ui.measure_wrapped(block[1], p, inner) + 10
            elif kind == "li":
                height += ui.measure_wrapped(block[1], p, inner - 24) + 4
            elif kind == "star_row":
                height += 34
            elif kind == "level":
                height += 82
        surface = pygame.Surface((width, height + 10), pygame.SRCALPHA)
        y = 10
        for block in blocks:
            kind = block[0]
            if kind == "h1":
                ui.draw_text(surface, block[1], h1, ui.AMBER_300, (0, y))
                y += h1.get_linesize() + 14
            elif kind == "h":
                ui.draw_text(surface, block[1], h, ui.AMBER_200, (0, y))
                y += h.get_linesize() + 6
            elif kind == "icon_h":
                self._draw_icon(surface, block[1], 14, y + 14)
                ui.draw_text(surface, block[2], h, ui.AMBER_200, (36, y + 4))
                y += 34
            elif kind == "p":
                y += ui.draw_wrapped(surface, block[1], p, ui.NEUTRAL_400, 0, y, inner) + 10
            elif kind == "li":
                pygame.draw.circle(surface, ui.AMBER_400, (8, y + 9), 3)
                y += ui.draw_wrapped(surface, block[1], p, ui.NEUTRAL_200, 22, y, inner - 24) + 4
            elif kind == "star_row":
                for index in range(3):
                    sprites.draw_star(surface, 12 + index * 22, y + 14, 8, index < block[1])
                ui.draw_text(surface, block[2], p, ui.NEUTRAL_200, (84, y + 14), "midleft")
                y += 34
            elif kind == "level":
                self._draw_level_card(surface, block[1], y, width)
                y += 82
        return surface

    def _draw_icon(self, surface, name, x, y) -> None:
        if name == "snake":
            sprites.draw_snake(surface, x, y, 24)
        elif name == "bat":
            sprites.draw_bat(surface, x, y, 24)
        elif name == "skull":
            sprites.draw_skull(surface, x, y, 24)
        elif name == "plant":
            sprites.draw_plant(surface, x, y, 24)
        elif name == "bolt":
            sprites.draw_bolt(surface, x, y, 22)
        elif name == "fire":
            pygame.draw.circle(surface, (239, 68, 68), (x, y), 11)
            pygame.draw.circle(surface, (249, 115, 22), (x, y), 8)
            pygame.draw.circle(surface, (254, 240, 138), (x, y), 4)

    def _draw_level_card(self, surface, level, y, width) -> None:
        wall = ui.hex_to_rgb(level.wall_color)
        accent = ui.hex_to_rgb(level.accent_color)
        card = pygame.Rect(0, y, width - 8, 74)
        ui.draw_panel(surface, card, (*wall, 64), (*wall, 255), 10, 1)
        ui.draw_text(surface, level.title, ui.Fonts.get(15, True), accent, (14, y + 10))
        ui.draw_text(surface, level.subtitle, ui.Fonts.get(13), ui.NEUTRAL_400, (14, y + 32))
        chips = [
            f"{level.width}x{level.height} cases",
            "5 Bananes",
            f"{len(level.traps)} Pièges",
            f"{len(level.enemies)} Monstres",
        ]
        x = 14
        font = ui.Fonts.get(12, True)
        for chip in chips:
            w = font.size(chip)[0] + 18
            ui.draw_panel(surface, pygame.Rect(x, y + 50, w, 20), (38, 38, 38, 255), ui.NEUTRAL_700, 8, 1)
            ui.draw_text(surface, chip, font, ui.NEUTRAL_200, (x + w // 2, y + 60), "center")
            x += w + 8

    def _content(self) -> pygame.Surface:
        key = (self.active_tab, self.content_rect.width)
        cached = self.content_cache.get(key)
        if cached is None:
            cached = self._build_content(self.active_tab, self.content_rect.width)
            self.content_cache[key] = cached
        return cached

    def _max_scroll(self) -> int:
        return max(0, self._content().get_height() - self.content_rect.height)

    def render(self, surface: pygame.Surface) -> None:
        panel = self.panel_rect(surface.get_size())
        ui.draw_panel(surface, panel, (23, 23, 23, 250), (245, 158, 11, 140), 18, 2)
        ui.draw_text(surface, "Maquette & Spécifications Complètes", ui.Fonts.get(22, True, "serif"), ui.AMBER_300, (panel.x + 28, panel.y + 18))
        ui.draw_text(
            surface,
            "Game Design Document (GDD) & Architecture du jeu du Roi dans le Labyrinthe",
            ui.Fonts.get(12),
            ui.NEUTRAL_400,
            (panel.x + 28, panel.y + 48),
        )
        font = ui.Fonts.get(13, True)
        for key, label in TABS:
            rect = self.tab_rects[key]
            active = key == self.active_tab
            ui.draw_panel(surface, rect, ui.AMBER_500 if active else (38, 38, 38, 255), None, 8)
            ui.draw_text(surface, label, font, (23, 23, 23) if active else ui.NEUTRAL_400, rect.center, "center")

        self.scroll = max(0, min(self.scroll, self._max_scroll()))
        previous_clip = surface.get_clip()
        surface.set_clip(self.content_rect)
        surface.blit(self._content(), (self.content_rect.x, self.content_rect.y - self.scroll))
        surface.set_clip(previous_clip)

        if self._max_scroll() > 0:
            track = pygame.Rect(self.content_rect.right + 6, self.content_rect.y, 6, self.content_rect.height)
            pygame.draw.rect(surface, ui.NEUTRAL_800, track, border_radius=3)
            ratio = self.content_rect.height / self._content().get_height()
            thumb_h = max(30, int(track.height * ratio))
            thumb_y = track.y + int((track.height - thumb_h) * (self.scroll / self._max_scroll()))
            pygame.draw.rect(surface, ui.AMBER_500, (track.x, thumb_y, 6, thumb_h), border_radius=3)

        ui.draw_text(
            surface,
            "Toutes les fonctionnalités décrites sont actives et jouables.",
            ui.Fonts.get(12),
            ui.NEUTRAL_500,
            (panel.x + 28, panel.bottom - 34),
            "midleft",
        )

    def handle_event(self, event: pygame.event.Event, surface_size: Tuple[int, int]) -> bool:
        self.layout(surface_size)
        if event.type == pygame.MOUSEWHEEL:
            self.scroll = max(0, min(self._max_scroll(), self.scroll - event.y * 40))
            return True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.scroll = min(self._max_scroll(), self.scroll + 40)
                return True
            if event.key == pygame.K_UP:
                self.scroll = max(0, self.scroll - 40)
                return True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for key, rect in self.tab_rects.items():
                if rect.collidepoint(event.pos):
                    self.active_tab = key
                    self.scroll = 0
                    return True
        return super().handle_event(event, surface_size)
