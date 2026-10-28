import math
from dataclasses import dataclass, replace
from typing import Sequence, Tuple


@dataclass
class Position:
    x: float
    y: float


@dataclass
class PlayerState:
    x: float
    y: float
    lives: int = 3
    max_lives: int = 5
    bananas_collected: int = 0
    target_bananas: int = 5
    has_shield: bool = False
    invulnerability_timer: float = 0.0
    is_dead: bool = False


@dataclass
class ItemPickup:
    id: str
    type: str
    x: float
    y: float
    collected: bool = False


@dataclass
class TrapState:
    id: str
    type: str
    x: float
    y: float
    active: bool = False


@dataclass
class EnemyEntity:
    id: str
    type: str
    x: float
    y: float
    radius: float


class Rules:
    SHIELD_GRACE_SECONDS = 1.2
    HIT_GRACE_SECONDS = 1.8

    @staticmethod
    def is_tile_walkable(grid: Sequence[str], tile_x: int, tile_y: int) -> bool:
        if tile_y < 0 or tile_y >= len(grid):
            return False
        row = grid[tile_y]
        if not row or tile_x < 0 or tile_x >= len(row):
            return False
        return row[tile_x] != "#"

    @staticmethod
    def is_colliding_with_entity(
        x1: float, y1: float, r1: float, x2: float, y2: float, r2: float
    ) -> bool:
        dx = x1 - x2
        dy = y1 - y2
        rad_sum = r1 + r2
        return dx * dx + dy * dy <= rad_sum * rad_sum

    @classmethod
    def apply_damage_to_player(
        cls, player: PlayerState, damage: int = 1
    ) -> Tuple[PlayerState, bool]:
        if player.is_dead or player.invulnerability_timer > 0:
            return replace(player), False

        if player.has_shield:
            return (
                replace(
                    player,
                    has_shield=False,
                    invulnerability_timer=cls.SHIELD_GRACE_SECONDS,
                ),
                True,
            )

        new_lives = max(0, player.lives - damage)
        return (
            replace(
                player,
                lives=new_lives,
                is_dead=new_lives <= 0,
                invulnerability_timer=cls.HIT_GRACE_SECONDS if new_lives > 0 else 0.0,
            ),
            True,
        )

    @staticmethod
    def check_level_objective_met(bananas_collected: int, target: int = 5) -> bool:
        return bananas_collected >= target

    @staticmethod
    def calculate_level_score(
        time_seconds: float,
        bananas_collected: int,
        lives_remaining: int,
        bonus_items_count: int = 0,
    ) -> Tuple[int, int]:
        banana_score = bananas_collected * 1000
        time_bonus = max(0, 3000 - math.floor(time_seconds) * 25)
        lives_bonus = lives_remaining * 800
        bonus_item_score = bonus_items_count * 500

        score = banana_score + time_bonus + lives_bonus + bonus_item_score

        stars = 1
        if lives_remaining >= 3 and time_seconds <= 60:
            stars = 3
        elif lives_remaining >= 2 and time_seconds <= 120:
            stars = 2

        return score, stars

    @classmethod
    def can_occupy_position(
        cls, x: float, y: float, radius: float, grid: Sequence[str]
    ) -> bool:
        min_x = math.floor(x - radius)
        max_x = math.floor(x + radius)
        min_y = math.floor(y - radius)
        max_y = math.floor(y + radius)

        for ty in range(min_y, max_y + 1):
            for tx in range(min_x, max_x + 1):
                if not cls.is_tile_walkable(grid, tx, ty):
                    return False
        return True

    @classmethod
    def resolve_movement(
        cls,
        current_x: float,
        current_y: float,
        target_x: float,
        target_y: float,
        radius: float,
        grid: Sequence[str],
    ) -> Tuple[float, float]:
        can_move_x = cls.can_occupy_position(target_x, current_y, radius, grid)
        can_move_y = cls.can_occupy_position(current_x, target_y, radius, grid)

        final_x = current_x
        final_y = current_y

        if can_move_x:
            final_x = target_x
        if can_move_y:
            final_y = target_y

        if (
            not can_move_x
            and not can_move_y
            and cls.can_occupy_position(target_x, target_y, radius, grid)
        ):
            return target_x, target_y

        return final_x, final_y
