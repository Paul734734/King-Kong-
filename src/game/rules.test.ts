import test from 'node:test';
import assert from 'node:assert/strict';
import {
  isTileWalkable,
  isCollidingWithEntity,
  applyDamageToPlayer,
  checkLevelObjectiveMet,
  calculateLevelScore,
  canOccupyPosition,
  PlayerState,
} from './rules.ts';

test('isTileWalkable correctly identifies passable vs stone walls', () => {
  const grid = [
    '#####',
    '#...#',
    '#####',
  ];
  assert.equal(isTileWalkable(grid, 0, 0), false); // Wall '#'
  assert.equal(isTileWalkable(grid, 1, 1), true);  // Path '.'
  assert.equal(isTileWalkable(grid, 2, 1), true);  // Path '.'
  assert.equal(isTileWalkable(grid, -1, 0), false); // Out of bounds
  assert.equal(isTileWalkable(grid, 5, 5), false);  // Out of bounds
});

test('isCollidingWithEntity detects overlapping radii', () => {
  assert.equal(isCollidingWithEntity(2.0, 2.0, 0.4, 2.2, 2.0, 0.4), true);
  assert.equal(isCollidingWithEntity(2.0, 2.0, 0.4, 5.0, 5.0, 0.4), false);
});

test('applyDamageToPlayer removes a life and triggers invulnerability', () => {
  const initialPlayer: PlayerState = {
    x: 1,
    y: 1,
    lives: 3,
    maxLives: 5,
    bananasCollected: 2,
    targetBananas: 5,
    hasShield: false,
    invulnerabilityTimer: 0,
    isDead: false,
  };

  const { player: hitPlayer, damaged } = applyDamageToPlayer(initialPlayer, 1);
  assert.equal(damaged, true);
  assert.equal(hitPlayer.lives, 2);
  assert.equal(hitPlayer.isDead, false);
  assert.equal(hitPlayer.invulnerabilityTimer > 0, true);

  // While invulnerable, player does NOT take extra damage
  const { player: immunePlayer, damaged: immuneDamaged } = applyDamageToPlayer(hitPlayer, 1);
  assert.equal(immuneDamaged, false);
  assert.equal(immunePlayer.lives, 2);
});

test('applyDamageToPlayer uses shield first if available', () => {
  const shieldedPlayer: PlayerState = {
    x: 1,
    y: 1,
    lives: 3,
    maxLives: 5,
    bananasCollected: 0,
    targetBananas: 5,
    hasShield: true,
    invulnerabilityTimer: 0,
    isDead: false,
  };

  const { player: protectedPlayer, damaged } = applyDamageToPlayer(shieldedPlayer, 1);
  assert.equal(damaged, true);
  assert.equal(protectedPlayer.lives, 3); // Lives preserved!
  assert.equal(protectedPlayer.hasShield, false); // Shield popped
  assert.equal(protectedPlayer.invulnerabilityTimer > 0, true);
});

test('checkLevelObjectiveMet requires 5 bananas', () => {
  assert.equal(checkLevelObjectiveMet(0, 5), false);
  assert.equal(checkLevelObjectiveMet(4, 5), false);
  assert.equal(checkLevelObjectiveMet(5, 5), true);
  assert.equal(checkLevelObjectiveMet(6, 5), true);
});

test('calculateLevelScore computes score and 3-star rating', () => {
  const result = calculateLevelScore(45, 5, 3, 1);
  assert.equal(result.stars, 3);
  assert.equal(result.score > 5000, true);
});
