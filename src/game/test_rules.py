import unittest

from .levels import LEVELS
from .rules import PlayerState, Rules


class RulesTests(unittest.TestCase):
    def test_is_tile_walkable(self):
        grid = ["#####", "#...#", "#####"]
        self.assertFalse(Rules.is_tile_walkable(grid, 0, 0))
        self.assertTrue(Rules.is_tile_walkable(grid, 1, 1))
        self.assertTrue(Rules.is_tile_walkable(grid, 2, 1))
        self.assertFalse(Rules.is_tile_walkable(grid, -1, 0))
        self.assertFalse(Rules.is_tile_walkable(grid, 5, 5))

    def test_is_colliding_with_entity(self):
        self.assertTrue(Rules.is_colliding_with_entity(2.0, 2.0, 0.4, 2.2, 2.0, 0.4))
        self.assertFalse(Rules.is_colliding_with_entity(2.0, 2.0, 0.4, 5.0, 5.0, 0.4))

    def test_damage_removes_life_and_grants_invulnerability(self):
        player = PlayerState(x=1, y=1, lives=3, bananas_collected=2)
        hit, damaged = Rules.apply_damage_to_player(player, 1)
        self.assertTrue(damaged)
        self.assertEqual(hit.lives, 2)
        self.assertFalse(hit.is_dead)
        self.assertGreater(hit.invulnerability_timer, 0)

        immune, immune_damaged = Rules.apply_damage_to_player(hit, 1)
        self.assertFalse(immune_damaged)
        self.assertEqual(immune.lives, 2)

    def test_damage_uses_shield_first(self):
        player = PlayerState(x=1, y=1, lives=3, has_shield=True)
        protected, damaged = Rules.apply_damage_to_player(player, 1)
        self.assertTrue(damaged)
        self.assertEqual(protected.lives, 3)
        self.assertFalse(protected.has_shield)
        self.assertGreater(protected.invulnerability_timer, 0)

    def test_last_life_kills_player(self):
        player = PlayerState(x=1, y=1, lives=1)
        dead, damaged = Rules.apply_damage_to_player(player, 1)
        self.assertTrue(damaged)
        self.assertTrue(dead.is_dead)
        self.assertEqual(dead.invulnerability_timer, 0)

    def test_objective_requires_five_bananas(self):
        self.assertFalse(Rules.check_level_objective_met(0, 5))
        self.assertFalse(Rules.check_level_objective_met(4, 5))
        self.assertTrue(Rules.check_level_objective_met(5, 5))
        self.assertTrue(Rules.check_level_objective_met(6, 5))

    def test_level_score_and_stars(self):
        score, stars = Rules.calculate_level_score(45, 5, 3, 1)
        self.assertEqual(stars, 3)
        self.assertGreater(score, 5000)
        _, two_stars = Rules.calculate_level_score(100, 5, 2, 0)
        self.assertEqual(two_stars, 2)
        _, one_star = Rules.calculate_level_score(300, 5, 1, 0)
        self.assertEqual(one_star, 1)

    def test_can_occupy_position_blocks_walls(self):
        grid = ["#####", "#...#", "#####"]
        self.assertTrue(Rules.can_occupy_position(1.5, 1.5, 0.34, grid))
        self.assertFalse(Rules.can_occupy_position(0.9, 1.5, 0.34, grid))

    def test_resolve_movement_slides_along_walls(self):
        grid = ["#####", "#...#", "#####"]
        x, y = Rules.resolve_movement(1.5, 1.5, 0.5, 1.5, 0.34, grid)
        self.assertEqual((x, y), (1.5, 1.5))
        x, y = Rules.resolve_movement(1.5, 1.5, 2.0, 1.5, 0.34, grid)
        self.assertEqual((x, y), (2.0, 1.5))

    def test_levels_are_consistent(self):
        for level in LEVELS:
            self.assertEqual(len(level.grid), level.height)
            for row in level.grid:
                self.assertEqual(len(row), level.width)
            sx, sy = level.player_spawn
            self.assertTrue(Rules.can_occupy_position(sx, sy, 0.34, level.grid))
            ex, ey = level.sanctuary_exit
            self.assertTrue(Rules.can_occupy_position(ex, ey, 0.34, level.grid))
            bananas = [p for p in level.pickups if p.type == "banana"]
            self.assertEqual(len(bananas), 5)


class LevelSolvabilityTests(unittest.TestCase):
    def test_every_level_is_solvable(self):
        from collections import deque

        for level in LEVELS:
            grid = level.grid
            start = (int(level.player_spawn[0]), int(level.player_spawn[1]))
            seen = {start}
            queue = deque([start])
            while queue:
                x, y = queue.popleft()
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nxt = (x + dx, y + dy)
                    if grid[nxt[1]][nxt[0]] != "#" and nxt not in seen:
                        seen.add(nxt)
                        queue.append(nxt)
            for pickup in level.pickups:
                self.assertIn((int(pickup.x), int(pickup.y)), seen, f"{level.id}:{pickup.id}")
            exit_tile = (int(level.sanctuary_exit[0]), int(level.sanctuary_exit[1]))
            self.assertIn(exit_tile, seen, f"{level.id}:exit")
            for trap in level.traps:
                self.assertNotEqual(grid[trap.y][trap.x], "#", f"{level.id}:{trap.id}")


if __name__ == "__main__":
    unittest.main()
