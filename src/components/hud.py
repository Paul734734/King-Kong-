from typing import Callable, Optional, Tuple

import pygame

from .. import ui
from ..game import sprites
from ..game.levels import LevelDefinition


class HUD:
    def __init__(
        self,
        level: LevelDefinition,
        max_lives: int,
        target_bananas: int,
        is_muted: Callable[[], bool],
        on_toggle_pause: Callable[[], None],
        on_toggle_mute: Callable[[], None],
        on_restart: Callable[[], None],
        on_open_maquette: Callable[[], None],
        on_virtual_direction: Callable[[Optional[Tuple[float, float]]], None],
    ):
        self.level = level
        self.max_lives = max_lives
        self.target_bananas = target_bananas
        self.is_muted = is_muted
        self.on_virtual_direction = on_virtual_direction
        self.lives = 3
        self.bananas = 0
        self.elapsed_seconds = 0.0
        self.is_paused = False

        self.specs = ui.Button(
            "Spécifications", on_open_maquette, "icon", icon=lambda s, x, y, z: sprites.draw_book(s, x, y, z), font_size=13
        )
        self.mute = ui.Button(
            "", on_toggle_mute, "icon",
            icon=lambda s, x, y, z: sprites.draw_speaker(s, x, y, z + 6, self.is_muted()),
        )
        self.restart = ui.Button("", on_restart, "icon", icon=lambda s, x, y, z: sprites.draw_restart(s, x, y, z + 4))
        self.pause = ui.Button(
            "", on_toggle_pause, "icon",
            icon=lambda s, x, y, z: (
                sprites.draw_play(s, x, y, z + 4) if self.is_paused else sprites.draw_pause(s, x, y, z + 4)
            ),
        )
        self.buttons = [self.specs, self.mute, self.restart, self.pause]
        self.dpad_rects = {}
        self.dpad_vectors = {
            "up": (0, -1),
            "left": (-1, 0),
            "right": (1, 0),
            "down": (0, 1),
        }
        self.active_dir: Optional[str] = None

    def layout(self, size: Tuple[int, int]) -> None:
        w, h = size
        self.pause.place(w - 60, 14, 44, 44)
        self.restart.place(w - 110, 14, 44, 44)
        self.mute.place(w - 160, 14, 44, 44)
        self.specs.place(w - 330, 14, 164, 44)
        cell = 46
        base_x = w - 3 * cell - 24
        base_y = h - 3 * cell - 24
        self.dpad_rects = {
            "up": pygame.Rect(base_x + cell, base_y, cell, cell),
            "left": pygame.Rect(base_x, base_y + cell, cell, cell),
            "right": pygame.Rect(base_x + 2 * cell, base_y + cell, cell, cell),
            "down": pygame.Rect(base_x + cell, base_y + 2 * cell, cell, cell),
        }

    def draw(self, surface: pygame.Surface) -> None:
        self.layout(surface.get_size())
        w, h = surface.get_size()
        level = self.level
        accent = ui.hex_to_rgb(level.accent_color)
        wall = ui.hex_to_rgb(level.wall_color)

        header = pygame.Rect(14, 12, 520, 50)
        ui.draw_panel(surface, header, (23, 23, 23, 225), (*wall, 255), 12, 2)
        badge = pygame.Rect(header.x + 8, header.y + 8, 36, 34)
        ui.draw_panel(surface, badge, (*wall, 255), (*accent, 255), 8, 1)
        ui.draw_text(surface, f"N{level.id}", ui.Fonts.get(15, True, "serif"), accent, badge.center, "center")
        title_font = ui.Fonts.get(14, True)
        sub_font = ui.Fonts.get(11)
        ui.draw_text(surface, level.title, title_font, ui.NEUTRAL_200, (badge.right + 10, header.y + 8))
        ui.draw_text(surface, level.subtitle, sub_font, ui.NEUTRAL_400, (badge.right + 10, header.y + 28))

        lives_panel = pygame.Rect(14, 70, 56 + self.max_lives * 26, 40)
        ui.draw_panel(surface, lives_panel, (23, 23, 23, 225), ui.NEUTRAL_700, 12, 1)
        ui.draw_text(surface, "VIES", ui.Fonts.get(11, True), ui.NEUTRAL_400, (lives_panel.x + 10, lives_panel.centery), "midleft")
        for index in range(self.max_lives):
            hx = lives_panel.x + 64 + index * 26
            if index < self.lives:
                sprites.draw_heart(surface, hx, lives_panel.centery, 18, (239, 68, 68))
            else:
                sprites.draw_heart(surface, hx, lives_panel.centery, 16, (60, 60, 60))

        done = self.bananas >= self.target_bananas
        ban_panel = pygame.Rect(lives_panel.right + 10, 70, 100 if not done else 250, 40)
        ui.draw_panel(
            surface,
            ban_panel,
            (245, 158, 11, 55) if done else (23, 23, 23, 225),
            ui.AMBER_400 if done else (245, 158, 11, 100),
            12,
            2,
        )
        sprites.draw_banana(surface, ban_panel.x + 22, ban_panel.centery, 22)
        ui.draw_text(
            surface,
            f"{self.bananas} / {self.target_bananas}",
            ui.Fonts.get(17, True, "mono"),
            ui.AMBER_300,
            (ban_panel.x + 42, ban_panel.centery),
            "midleft",
        )
        if done:
            ui.draw_text(
                surface,
                "Sanctuaire Ouvert !",
                ui.Fonts.get(12, True),
                ui.AMBER_200,
                (ban_panel.x + 118, ban_panel.centery),
                "midleft",
            )

        for button in self.buttons:
            button.draw(surface)

        timer = pygame.Rect(w - 160, 66, 144, 44)
        ui.draw_panel(surface, timer, (23, 23, 23, 225), ui.NEUTRAL_700, 12, 1)
        ui.draw_text(surface, "TEMPS", ui.Fonts.get(11, True), ui.NEUTRAL_400, (timer.x + 12, timer.centery), "midleft")
        ui.draw_text(
            surface,
            ui.format_clock(self.elapsed_seconds),
            ui.Fonts.get(20, True, "mono"),
            ui.NEUTRAL_200,
            (timer.right - 12, timer.centery),
            "midright",
        )

        if done:
            banner = pygame.Rect(0, 0, 640, 40)
            banner.midtop = (w // 2, 120)
            ui.draw_panel(surface, banner, (180, 83, 9, 235), ui.AMBER_400, 20, 2)
            sprites.draw_crown(surface, banner.x + 26, banner.centery, 22)
            ui.draw_text(
                surface,
                "5 BANANES RASSEMBLÉES ! Rejoignez l'Arche Royale pour triompher !",
                ui.Fonts.get(14, True),
                (255, 251, 235),
                (banner.x + 46, banner.centery),
                "midleft",
            )

        hint = pygame.Rect(14, h - 46, 540, 32)
        ui.draw_panel(surface, hint, (23, 23, 23, 200), ui.NEUTRAL_800, 10, 1)
        ui.draw_text(
            surface,
            "Déplacement : ZQSD ou Flèches · Objectif : 5 bananes sans périr",
            ui.Fonts.get(13),
            ui.NEUTRAL_400,
            (hint.x + 12, hint.centery),
            "midleft",
        )

        for name, rect in self.dpad_rects.items():
            pressed = self.active_dir == name
            ui.draw_panel(
                surface,
                rect,
                (245, 158, 11, 120) if pressed else (23, 23, 23, 200),
                ui.NEUTRAL_700,
                10,
                1,
            )
            sprites.draw_arrow(surface, rect.centerx, rect.centery, 18, name)
        centre = pygame.Rect(self.dpad_rects["up"].x, self.dpad_rects["left"].y, 46, 46)
        sprites.draw_crown(surface, centre.centerx, centre.centery, 20)

    def handle_event(self, event: pygame.event.Event, size: Tuple[int, int]) -> bool:
        self.layout(size)
        for button in self.buttons:
            if button.handle_event(event):
                return True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for name, rect in self.dpad_rects.items():
                if rect.collidepoint(event.pos):
                    self.active_dir = name
                    self.on_virtual_direction(self.dpad_vectors[name])
                    return True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.active_dir:
            self.active_dir = None
            self.on_virtual_direction(None)
            return True
        return False
