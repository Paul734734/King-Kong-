import math
import random
from dataclasses import dataclass
from typing import Callable, List, Optional, Tuple

import pygame

from . import sprites
from .levels import LevelDefinition, LevelEnemy, LevelTrap
from .rules import ItemPickup, PlayerState, Rules
from .sound import SoundManager


def _rgb(value: str) -> Tuple[int, int, int]:
    value = value.lstrip("#")
    return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)


@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    life: float
    max_life: float
    color: Tuple[int, int, int]
    size: float

    def update(self, dt: float) -> None:
        self.life -= dt
        self.x += self.vx * dt
        self.y += self.vy * dt

    @property
    def alive(self) -> bool:
        return self.life > 0


class TrapRuntime:
    def __init__(self, definition: LevelTrap):
        self.definition = definition
        self.id = definition.id
        self.type = definition.type
        self.x = definition.x
        self.y = definition.y
        self.interval = definition.interval
        self.timer = definition.offset % definition.interval
        self.active = False
        self.warning = False

    def update(self, dt: float) -> None:
        self.timer = (self.timer + dt) % self.interval
        burst_start = self.interval * 0.65
        warning_start = self.interval * 0.45
        self.warning = warning_start <= self.timer < burst_start
        self.active = self.timer >= burst_start


class EnemyRuntime:
    def __init__(self, definition: LevelEnemy):
        self.definition = definition
        self.id = definition.id
        self.type = definition.type
        self.name = definition.name
        self.x = definition.x
        self.y = definition.y
        self.speed = definition.speed
        self.patrol_axis = definition.patrol_axis
        self.patrol_range = definition.patrol_range
        self.current_x = definition.x
        self.current_y = definition.y
        self.direction = 1
        self.anim_time = 0.0

    def update(self, dt: float) -> None:
        self.anim_time += dt
        if self.patrol_axis == "x":
            self.current_x += self.direction * self.speed * dt
            if abs(self.current_x - self.x) > self.patrol_range:
                self.direction *= -1
        elif self.patrol_axis == "y":
            self.current_y += self.direction * self.speed * dt
            if abs(self.current_y - self.y) > self.patrol_range:
                self.direction *= -1
        elif self.patrol_axis == "circle":
            self.current_x = self.x + math.sin(self.anim_time * 2) * 0.1
            self.current_y = self.y + math.cos(self.anim_time * 2) * 0.1


class GameCanvas:
    TILE_SIZE = 48
    PLAYER_RADIUS = 0.34
    BASE_SPEED = 3.0
    BOOST_SPEED = 4.5
    BOOST_SECONDS = 6.0

    UP_KEYS = (pygame.K_UP, pygame.K_w, pygame.K_z)
    DOWN_KEYS = (pygame.K_DOWN, pygame.K_s)
    LEFT_KEYS = (pygame.K_LEFT, pygame.K_a, pygame.K_q)
    RIGHT_KEYS = (pygame.K_RIGHT, pygame.K_d)

    def __init__(
        self,
        level: LevelDefinition,
        sounds: SoundManager,
        on_banana_collected: Callable[[int], None],
        on_lives_changed: Callable[[int], None],
        on_game_over: Callable[[str], None],
        on_level_complete: Callable[[float, int, int], None],
    ):
        self.level = level
        self.sounds = sounds
        self.on_banana_collected = on_banana_collected
        self.on_lives_changed = on_lives_changed
        self.on_game_over = on_game_over
        self.on_level_complete = on_level_complete
        self.is_paused = False
        self.virtual_input: Optional[Tuple[float, float]] = None
        self.map_surface = self._build_map_surface()
        self.reset()

    def reset(self) -> None:
        level = self.level
        self.player = PlayerState(x=level.player_spawn[0], y=level.player_spawn[1])
        self.speed_boost_timer = 0.0
        self.facing = "down"
        self.walk_cycle = 0.0
        self.is_moving = False
        self.bonus_items_collected = 0
        self.elapsed_seconds = 0.0
        self.completed = False
        self.trauma = 0.0
        self.pickups: List[ItemPickup] = [
            ItemPickup(p.id, p.type, p.x, p.y) for p in level.pickups
        ]
        self.traps = [TrapRuntime(t) for t in level.traps]
        self.enemies = [EnemyRuntime(e) for e in level.enemies]
        self.particles: List[Particle] = []
        self.on_banana_collected(0)
        self.on_lives_changed(3)

    def _build_map_surface(self) -> pygame.Surface:
        level = self.level
        tile = self.TILE_SIZE
        surface = pygame.Surface((level.width * tile, level.height * tile))
        wall = _rgb(level.wall_color)
        floor = _rgb(level.floor_color)
        accent = _rgb(level.accent_color)
        for ty in range(level.height):
            for tx in range(level.width):
                char = level.grid[ty][tx]
                px = tx * tile
                py = ty * tile
                if char == "#":
                    pygame.draw.rect(surface, wall, (px, py, tile, tile))
                    sprites.blend_rect(surface, (255, 255, 255), (px, py, tile, 4), 46)
                    sprites.blend_rect(surface, (255, 255, 255), (px, py, 4, tile), 46)
                    sprites.blend_rect(surface, (0, 0, 0), (px, py + tile - 4, tile, 4), 128)
                    sprites.blend_rect(surface, (0, 0, 0), (px + tile - 4, py, 4, tile), 128)
                    sprites.blend_outline(
                        surface, (0, 0, 0), (px + 4, py + 4, tile - 8, tile - 8), 90, 2
                    )
                    if (tx + ty) % 4 == 0:
                        sprites.blend_rect(
                            surface, accent, (px + tile // 2 - 3, py + tile // 2 - 3, 6, 6), 51
                        )
                else:
                    pygame.draw.rect(surface, floor, (px, py, tile, tile))
                    sprites.blend_outline(surface, (255, 255, 255), (px, py, tile, tile), 13, 1)
        return surface

    def _input_vector(self, keys) -> Tuple[float, float]:
        move_x = 0.0
        move_y = 0.0
        if any(keys[k] for k in self.UP_KEYS):
            move_y -= 1
        if any(keys[k] for k in self.DOWN_KEYS):
            move_y += 1
        if any(keys[k] for k in self.LEFT_KEYS):
            move_x -= 1
        if any(keys[k] for k in self.RIGHT_KEYS):
            move_x += 1
        if self.virtual_input and (self.virtual_input[0] != 0 or self.virtual_input[1] != 0):
            move_x, move_y = self.virtual_input
        return move_x, move_y

    def _burst(self, x, y, color, count, spread, life, size) -> None:
        for _ in range(count):
            self.particles.append(
                Particle(
                    x,
                    y,
                    (random.random() - 0.5) * spread,
                    (random.random() - 0.5) * spread,
                    life,
                    life,
                    color,
                    size,
                )
            )

    def _damage_player(self, color, reason: str) -> None:
        result, damaged = Rules.apply_damage_to_player(self.player, 1)
        if not damaged:
            return
        self.player = result
        self.trauma = 1.0
        self.sounds.play_damage()
        self.on_lives_changed(self.player.lives)
        self._burst(self.player.x, self.player.y, color, 14, 3, 0.4, 3)
        if self.player.is_dead:
            self.sounds.play_game_over()
            self.on_game_over(reason)

    def _collect_pickups(self) -> None:
        player = self.player
        for pickup in self.pickups:
            if pickup.collected:
                continue
            if not Rules.is_colliding_with_entity(
                player.x, player.y, 0.38, pickup.x, pickup.y, 0.35
            ):
                continue
            pickup.collected = True
            if pickup.type == "banana":
                player.bananas_collected += 1
                self.sounds.play_banana()
                self.on_banana_collected(player.bananas_collected)
                for _ in range(15):
                    angle = random.random() * math.pi * 2
                    speed = 1.2 + random.random() * 2.5
                    self.particles.append(
                        Particle(
                            pickup.x,
                            pickup.y,
                            math.cos(angle) * speed,
                            math.sin(angle) * speed,
                            0.6,
                            0.6,
                            (251, 191, 36),
                            3 + random.random() * 3,
                        )
                    )
            elif pickup.type == "heart":
                player.lives = min(player.max_lives, player.lives + 1)
                self.bonus_items_collected += 1
                self.sounds.play_heart()
                self.on_lives_changed(player.lives)
                self._burst(pickup.x, pickup.y, (244, 63, 94), 12, 2, 0.5, 4)
            elif pickup.type == "shield":
                player.has_shield = True
                self.bonus_items_collected += 1
                self.sounds.play_shield()
            elif pickup.type == "speed":
                self.speed_boost_timer = self.BOOST_SECONDS
                self.bonus_items_collected += 1
                self.sounds.play_shield()

    def _update_traps(self, dt: float) -> None:
        for trap in self.traps:
            trap.update(dt)
            if trap.active and Rules.is_colliding_with_entity(
                self.player.x, self.player.y, 0.35, trap.x + 0.5, trap.y + 0.5, 0.35
            ):
                reason = (
                    "Empalé par des pics royaux !"
                    if trap.type == "spikes"
                    else "Brûlé par les flammes du donjon !"
                )
                self._damage_player((239, 68, 68), reason)

    def _update_enemies(self, dt: float) -> None:
        for enemy in self.enemies:
            enemy.update(dt)
            if Rules.is_colliding_with_entity(
                self.player.x, self.player.y, 0.36, enemy.current_x, enemy.current_y, 0.38
            ):
                self._damage_player((249, 115, 22), f"Attaqué par {enemy.name} !")

    def update(self, dt: float, keys) -> None:
        dt = min(dt, 0.05)
        if not self.is_paused and not self.player.is_dead and not self.completed:
            self.elapsed_seconds += dt
            player = self.player
            if player.invulnerability_timer > 0:
                player.invulnerability_timer -= dt
            if self.speed_boost_timer > 0:
                self.speed_boost_timer -= dt
            if self.trauma > 0:
                self.trauma = max(0.0, self.trauma - dt * 2.5)

            move_x, move_y = self._input_vector(keys)
            length = math.hypot(move_x, move_y)
            self.is_moving = length > 0.05
            if self.is_moving:
                norm_x = move_x / length
                norm_y = move_y / length
                if abs(norm_x) > abs(norm_y):
                    self.facing = "right" if norm_x > 0 else "left"
                else:
                    self.facing = "down" if norm_y > 0 else "up"
                speed = self.BOOST_SPEED if self.speed_boost_timer > 0 else self.BASE_SPEED
                step = speed * dt
                self.player.x, self.player.y = Rules.resolve_movement(
                    self.player.x,
                    self.player.y,
                    self.player.x + norm_x * step,
                    self.player.y + norm_y * step,
                    self.PLAYER_RADIUS,
                    self.level.grid,
                )
                self.walk_cycle += dt * 8

            self._collect_pickups()
            self._update_traps(dt)
            if not self.player.is_dead:
                self._update_enemies(dt)

            if not self.player.is_dead and Rules.check_level_objective_met(
                self.player.bananas_collected, self.player.target_bananas
            ):
                ex, ey = self.level.sanctuary_exit
                if Rules.is_colliding_with_entity(
                    self.player.x, self.player.y, 0.38, ex, ey, 0.45
                ):
                    self.completed = True
                    self.sounds.play_level_victory()
                    self.on_level_complete(
                        self.elapsed_seconds, self.player.lives, self.bonus_items_collected
                    )

        for particle in self.particles:
            particle.update(dt)
        self.particles = [p for p in self.particles if p.alive]

    def _camera(self, view_w: int, view_h: int) -> Tuple[float, float]:
        tile = self.TILE_SIZE
        level_w = self.level.width * tile
        level_h = self.level.height * tile
        cam_x = self.player.x * tile - view_w / 2
        cam_y = self.player.y * tile - view_h / 2
        if level_w <= view_w:
            cam_x = -(view_w - level_w) / 2
        else:
            cam_x = max(0, min(level_w - view_w, cam_x))
        if level_h <= view_h:
            cam_y = -(view_h - level_h) / 2
        else:
            cam_y = max(0, min(level_h - view_h, cam_y))
        shake = 14 * self.trauma * self.trauma
        cam_x += (random.random() - 0.5) * shake
        cam_y += (random.random() - 0.5) * shake
        return cam_x, cam_y

    def draw(self, surface: pygame.Surface, time_ms: float) -> None:
        view_w, view_h = surface.get_size()
        surface.fill((7, 7, 9))
        cam_x, cam_y = self._camera(view_w, view_h)
        cam = (int(cam_x), int(cam_y))
        surface.blit(self.map_surface, (-cam[0], -cam[1]))
        self._draw_traps(surface, cam, time_ms)
        self._draw_exit(surface, cam, time_ms)
        self._draw_pickups(surface, cam, time_ms)
        self._draw_enemies(surface, cam)
        self._draw_particles(surface, cam)
        self._draw_player(surface, cam, time_ms)

    def _screen(self, x: float, y: float, cam) -> Tuple[int, int]:
        return int(x * self.TILE_SIZE - cam[0]), int(y * self.TILE_SIZE - cam[1])

    def _draw_traps(self, surface, cam, time_ms) -> None:
        tile = self.TILE_SIZE
        for trap in self.traps:
            px = trap.x * tile - cam[0]
            py = trap.y * tile - cam[1]
            pygame.draw.rect(surface, (15, 23, 42), (px + 3, py + 3, tile - 6, tile - 6))
            frame = (
                (245, 158, 11)
                if trap.warning
                else (239, 68, 68)
                if trap.active
                else (51, 65, 85)
            )
            pygame.draw.rect(surface, frame, (px + 3, py + 3, tile - 6, tile - 6), 2)
            if trap.type == "spikes":
                if trap.warning:
                    for i in range(4):
                        pygame.draw.circle(
                            surface,
                            (245, 158, 11),
                            (px + 14 + (i % 2) * 20, py + 14 + (i // 2) * 20),
                            4,
                        )
                if trap.active:
                    for i in range(4):
                        sx = px + 14 + (i % 2) * 20
                        sy = py + 14 + (i // 2) * 20
                        pygame.draw.polygon(
                            surface,
                            (248, 250, 252),
                            [(sx, sy - 10), (sx - 6, sy + 6), (sx + 6, sy + 6)],
                        )
                        pygame.draw.polygon(
                            surface,
                            (148, 163, 184),
                            [(sx, sy - 10), (sx, sy + 6), (sx + 6, sy + 6)],
                        )
            elif trap.type == "fire":
                center = (int(px + tile / 2), int(py + tile / 2))
                if trap.warning:
                    sprites.blend_circle(surface, (249, 115, 22), center, 16, 115)
                if trap.active:
                    radius = 18 + math.sin(time_ms * 0.02) * 3
                    pygame.draw.circle(surface, (239, 68, 68), center, int(radius))
                    pygame.draw.circle(surface, (249, 115, 22), center, int(radius * 0.7))
                    pygame.draw.circle(surface, (254, 240, 138), center, int(radius * 0.4))

    def _draw_exit(self, surface, cam, time_ms) -> None:
        ex, ey = self._screen(self.level.sanctuary_exit[0], self.level.sanctuary_exit[1], cam)
        ready = Rules.check_level_objective_met(
            self.player.bananas_collected, self.player.target_bananas
        )
        if ready:
            pulse = 1 + math.sin(time_ms * 0.007) * 0.2
            outer = int(36 * pulse)
            size = outer * 2 + 4
            glow = pygame.Surface((size, size), pygame.SRCALPHA)
            for r in range(outer, 3, -2):
                t = (outer - r) / max(1, outer - 4)
                u = 1 - t
                if u > 0.5:
                    w = (1 - u) / 0.5
                    col = (254 + (245 - 254) * w, 240 + (158 - 240) * w, 138 + (11 - 138) * w)
                    alpha = 0.95 + (0.7 - 0.95) * w
                else:
                    w = u / 0.5
                    col = (217 + (245 - 217) * w, 119 + (158 - 119) * w, 6 + (11 - 6) * w)
                    alpha = 0.7 * w
                pygame.draw.circle(
                    glow,
                    (int(col[0]), int(col[1]), int(col[2]), int(alpha * 255)),
                    (size // 2, size // 2),
                    r,
                )
            surface.blit(glow, (ex - size // 2, ey - size // 2))
            pygame.draw.rect(surface, (251, 191, 36), (ex - 20, ey - 22, 40, 44))
            arch = [
                (14 * math.cos(a), 2 + 14 * math.sin(a))
                for a in [math.pi + i * math.pi / 12 for i in range(13)]
            ]
            arch = [(ex + x, ey + y) for x, y in arch] + [(ex + 14, ey + 20), (ex - 14, ey + 20)]
            pygame.draw.polygon(surface, (28, 25, 23), arch)
            sprites.draw_crown(surface, ex, ey - 5, 20)
        else:
            pygame.draw.rect(surface, (51, 65, 85), (ex - 18, ey - 20, 36, 40))
            pygame.draw.rect(surface, (100, 116, 139), (ex - 16, ey - 18, 32, 36), 2)
            sprites.draw_lock(surface, ex, ey, 16)

    def _draw_pickups(self, surface, cam, time_ms) -> None:
        for pickup in self.pickups:
            if pickup.collected:
                continue
            px, py = self._screen(pickup.x, pickup.y, cam)
            bob = math.sin(time_ms * 0.005 + pickup.x * 2) * 5
            py = int(py + bob)
            if pickup.type == "banana":
                sprites.blend_circle(surface, (251, 191, 36), (px, py), 15, 89)
                sprites.draw_banana(surface, px, py, 26)
            elif pickup.type == "heart":
                sprites.blend_circle(surface, (239, 68, 68), (px, py), 14, 77)
                sprites.draw_heart(surface, px, py, 22)
            elif pickup.type == "shield":
                sprites.blend_circle(surface, (56, 189, 248), (px, py), 15, 89)
                sprites.draw_shield(surface, px, py, 22)
            elif pickup.type == "speed":
                sprites.draw_bolt(surface, px, py, 22)

    def _draw_enemies(self, surface, cam) -> None:
        for enemy in self.enemies:
            ex, ey = self._screen(enemy.current_x, enemy.current_y, cam)
            sprites.blend_ellipse(surface, (0, 0, 0), (ex, ey + 12), 13, 6, 115)
            if enemy.type == "snake":
                sprites.draw_snake(surface, ex, ey, 26, math.sin(enemy.anim_time * 8) * 3)
            elif enemy.type == "bat":
                sprites.draw_bat(surface, ex, ey + math.sin(enemy.anim_time * 14) * 5, 26, math.sin(enemy.anim_time * 14) * 3)
            elif enemy.type == "guard":
                sprites.draw_skull(surface, ex, ey, 26)
            elif enemy.type == "carnivorous_plant":
                sprites.draw_plant(surface, ex, ey, 26, math.sin(enemy.anim_time * 4) > 0)

    def _draw_particles(self, surface, cam) -> None:
        for p in self.particles:
            px, py = self._screen(p.x, p.y, cam)
            alpha = max(0.0, p.life / p.max_life)
            sprites.blend_circle(surface, p.color, (px, py), p.size, alpha * 255)

    def _draw_player(self, surface, cam, time_ms) -> None:
        player = self.player
        blink = player.invulnerability_timer > 0 and int(time_ms // 80) % 2 == 0
        if blink:
            return
        kx, ky = self._screen(player.x, player.y, cam)
        sprites.blend_ellipse(surface, (0, 0, 0), (kx, ky + 14), 16, 7, 115)
        if self.speed_boost_timer > 0:
            sprites.blend_circle(surface, (234, 179, 8), (kx, ky), 22, 89)
        if player.has_shield:
            sprites.blend_circle(surface, (56, 189, 248), (kx, ky), 24, 51)
            pygame.draw.circle(surface, (56, 189, 248), (kx, ky), 24, 3)

        wave = math.sin(self.walk_cycle) * 3
        pygame.draw.polygon(
            surface,
            (220, 38, 38),
            [
                (kx - 10, ky - 6),
                (kx + 10, ky - 6),
                (kx + 12 + wave, ky + 16),
                (kx - 12 + wave, ky + 16),
            ],
        )
        pygame.draw.circle(surface, (28, 25, 23), (kx, ky + 2), 14)
        pygame.draw.ellipse(surface, (68, 64, 60), (kx - 9, ky - 4, 18, 14))
        pygame.draw.circle(surface, (28, 25, 23), (kx, ky - 7), 10)
        pygame.draw.circle(surface, (255, 255, 255), (kx - 3, ky - 7), 3)
        pygame.draw.circle(surface, (255, 255, 255), (kx + 3, ky - 7), 3)
        pygame.draw.circle(surface, (0, 0, 0), (kx - 3, ky - 7), 1)
        pygame.draw.circle(surface, (0, 0, 0), (kx + 3, ky - 7), 1)
        crown = [(-8, -13), (-7, -20), (-3, -16), (0, -23), (3, -16), (7, -20), (8, -13)]
        pygame.draw.polygon(surface, (251, 191, 36), [(kx + x, ky + y) for x, y in crown])
        pygame.draw.circle(surface, (239, 68, 68), (kx, ky - 17), 2)
        pygame.draw.circle(surface, (239, 68, 68), (kx - 5, ky - 15), 1)
        pygame.draw.circle(surface, (239, 68, 68), (kx + 5, ky - 15), 1)
