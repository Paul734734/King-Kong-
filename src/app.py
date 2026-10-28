from enum import Enum
from typing import List, Optional, Tuple

import pygame

from .components.game_over_modal import GameOverModal
from .components.hud import HUD
from .components.level_select_modal import LevelSelectModal
from .components.maquette_modal import MaquetteModal
from .components.pause_modal import PauseModal
from .components.rules_modal import RulesModal
from .components.title_screen import TitleScreen
from .components.victory_modal import VictoryModal
from .game.game_canvas import GameCanvas
from .game.levels import LEVELS, LevelDefinition, get_level
from .game.rules import Rules
from .game.sound import SoundManager
from .game.storage import SaveStore
from . import ui
from .game import sprites


class ScreenState(Enum):
    TITLE = "title"
    PLAYING = "playing"
    PAUSED = "paused"
    LEVEL_CLEAR = "level_clear"
    GAME_OVER = "game_over"


class App:
    FPS = 60
    MAX_LIVES = 5
    TARGET_BANANAS = 5
    CAPTION = "King Kong Labyrinth - La Quête Royale"

    def __init__(
        self,
        size: Tuple[int, int] = (1100, 720),
        autostart_level: Optional[int] = None,
        fullscreen: bool = False,
    ):
        pygame.init()
        flags = pygame.RESIZABLE | (pygame.FULLSCREEN if fullscreen else 0)
        self.screen = pygame.display.set_mode(size, flags)
        pygame.display.set_caption(self.CAPTION)
        self._set_icon()
        self.clock = pygame.time.Clock()
        self.running = True

        self.store = SaveStore()
        self.sounds = SoundManager(self.store)

        self.state = ScreenState.TITLE
        self.current_level_id = 1
        self.bananas = 0
        self.lives = 3
        self.game_over_reason = ""
        self.canvas: Optional[GameCanvas] = None
        self.hud: Optional[HUD] = None
        self.state_modal: Optional[ui.Modal] = None
        self.overlays: List[ui.Modal] = []

        self.title = TitleScreen(
            self.store,
            self.start_game,
            self.open_level_select,
            self.open_maquette,
            self.open_rules,
            self.toggle_mute,
            self.sounds.get_muted,
        )

        if autostart_level is not None:
            self.start_game(autostart_level)

    def _set_icon(self) -> None:
        icon = pygame.Surface((64, 64), pygame.SRCALPHA)
        pygame.draw.rect(icon, (28, 25, 23), icon.get_rect(), border_radius=14)
        sprites.draw_gorilla_face(icon, 32, 38, 44)
        pygame.display.set_icon(icon)

    @property
    def current_level(self) -> LevelDefinition:
        return get_level(self.current_level_id)

    def toggle_mute(self) -> None:
        self.sounds.toggle_mute()

    def open_level_select(self) -> None:
        self.overlays.append(LevelSelectModal(self.store, self.close_overlay, self.start_game))

    def open_maquette(self) -> None:
        self.overlays.append(MaquetteModal(self.close_overlay))

    def open_rules(self) -> None:
        self.overlays.append(RulesModal(self.close_overlay))

    def close_overlay(self) -> None:
        if self.overlays:
            self.overlays.pop()

    def start_game(self, level_id: int = 1) -> None:
        self.current_level_id = level_id
        self.bananas = 0
        self.lives = 3
        self.game_over_reason = ""
        self.overlays.clear()
        self.state_modal = None
        level = self.current_level
        self.canvas = GameCanvas(
            level,
            self.sounds,
            self._set_bananas,
            self._set_lives,
            self.handle_game_over,
            self.handle_level_complete,
        )
        self.hud = HUD(
            level,
            self.MAX_LIVES,
            self.TARGET_BANANAS,
            self.sounds.get_muted,
            self.toggle_pause,
            self.toggle_mute,
            self.restart_level,
            self.open_maquette,
            self._set_virtual_input,
        )
        self.state = ScreenState.PLAYING
        self.sounds.play_music()

    def restart_level(self) -> None:
        self.start_game(self.current_level_id)

    def go_home(self) -> None:
        self.sounds.stop_music()
        self.state = ScreenState.TITLE
        self.state_modal = None
        self.overlays.clear()

    def _set_bananas(self, value: int) -> None:
        self.bananas = value

    def _set_lives(self, value: int) -> None:
        self.lives = value

    def _set_virtual_input(self, vector) -> None:
        if self.canvas is not None:
            self.canvas.virtual_input = vector

    def toggle_pause(self) -> None:
        if self.state == ScreenState.PLAYING:
            self.state = ScreenState.PAUSED
            self.sounds.pause_music()
            self.state_modal = PauseModal(
                self.current_level,
                self.bananas,
                self.lives,
                self.canvas.elapsed_seconds if self.canvas else 0,
                self.toggle_pause,
                self.restart_level,
                self.go_home,
                self.open_maquette,
                self.toggle_mute,
                self.sounds.get_muted,
            )
        elif self.state == ScreenState.PAUSED:
            self.state = ScreenState.PLAYING
            self.sounds.resume_music()
            self.state_modal = None

    def handle_game_over(self, reason: str) -> None:
        self.game_over_reason = reason
        self.state = ScreenState.GAME_OVER
        self.state_modal = GameOverModal(
            self.current_level,
            reason,
            self.bananas,
            self.restart_level,
            self.go_home,
            self.open_maquette,
        )

    def handle_level_complete(self, time_seconds: float, lives_left: int, bonus_count: int) -> None:
        score, stars = Rules.calculate_level_score(
            time_seconds, self.TARGET_BANANAS, lives_left, bonus_count
        )
        self.store.record_completion(self.current_level_id, stars, score)
        self.state = ScreenState.LEVEL_CLEAR
        self.state_modal = VictoryModal(
            self.current_level,
            time_seconds,
            lives_left,
            bonus_count,
            score,
            stars,
            self.next_level,
            self.restart_level,
            self.go_home,
            self.current_level_id == len(LEVELS),
        )

    def next_level(self) -> None:
        if self.current_level_id < len(LEVELS):
            self.start_game(self.current_level_id + 1)
        else:
            self.go_home()

    def handle_key(self, event: pygame.event.Event) -> bool:
        key = event.key
        if self.overlays:
            if key == pygame.K_ESCAPE:
                self.close_overlay()
                return True
            self.overlays[-1].handle_event(event, self.screen.get_size())
            return True
        if self.state == ScreenState.TITLE:
            if key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                self.start_game(1)
                return True
        elif self.state == ScreenState.PLAYING:
            if key in (pygame.K_ESCAPE, pygame.K_p):
                self.toggle_pause()
                return True
            if key == pygame.K_r:
                self.restart_level()
                return True
            if key == pygame.K_m:
                self.toggle_mute()
                return True
        elif self.state == ScreenState.PAUSED:
            if key in (pygame.K_ESCAPE, pygame.K_p):
                self.toggle_pause()
                return True
        elif self.state == ScreenState.GAME_OVER:
            if key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_r):
                self.restart_level()
                return True
        elif self.state == ScreenState.LEVEL_CLEAR:
            if key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.next_level()
                return True
        return False

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.running = False
            return
        if event.type == pygame.KEYDOWN:
            self.handle_key(event)
            return
        size = self.screen.get_size()
        if self.overlays:
            self.overlays[-1].handle_event(event, size)
            return
        if self.state == ScreenState.TITLE:
            self.title.handle_event(event, size)
        elif self.state == ScreenState.PLAYING and self.hud:
            self.hud.handle_event(event, size)
        elif self.state_modal is not None:
            self.state_modal.handle_event(event, size)

    def update(self, dt: float) -> None:
        if self.state == ScreenState.TITLE:
            return
        if self.canvas is not None:
            frozen = self.state != ScreenState.PLAYING or bool(self.overlays)
            self.canvas.is_paused = frozen
            self.canvas.update(dt, pygame.key.get_pressed())
        if self.hud is not None and self.canvas is not None:
            self.hud.lives = self.lives
            self.hud.bananas = self.bananas
            self.hud.elapsed_seconds = self.canvas.elapsed_seconds
            self.hud.is_paused = self.state == ScreenState.PAUSED
        if self.state_modal is not None:
            self.state_modal.update(dt)

    def draw(self) -> None:
        self.screen = pygame.display.get_surface()
        if self.state == ScreenState.TITLE:
            self.title.draw(self.screen)
        else:
            if self.canvas is not None:
                self.canvas.draw(self.screen, pygame.time.get_ticks())
            if self.hud is not None:
                self.hud.draw(self.screen)
            if self.state_modal is not None:
                self.state_modal.draw(self.screen)
        for overlay in self.overlays:
            overlay.draw(self.screen)

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(self.FPS) / 1000.0
            for event in pygame.event.get():
                self.handle_event(event)
            self.update(dt)
            self.draw()
            pygame.display.flip()
        pygame.quit()
