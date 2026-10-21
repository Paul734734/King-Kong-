/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

export interface Position {
  x: number;
  y: number;
}

export interface PlayerState {
  x: number;
  y: number;
  lives: number;
  maxLives: number;
  bananasCollected: number;
  targetBananas: number;
  hasShield: boolean;
  invulnerabilityTimer: number; // in seconds
  isDead: boolean;
}

export interface ItemPickup {
  id: string;
  type: 'banana' | 'heart' | 'shield' | 'speed';
  x: number;
  y: number;
  collected: boolean;
}

export interface TrapState {
  id: string;
  type: 'spikes' | 'fire';
  x: number;
  y: number;
  active: boolean; // whether it deals damage right now
}

export interface EnemyEntity {
  id: string;
  type: 'snake' | 'bat' | 'guard' | 'carnivorous_plant';
  x: number;
  y: number;
  radius: number;
}

/**
 * Checks if a tile coordinate is passable (not a wall)
 */
export function isTileWalkable(grid: string[], tileX: number, tileY: number): boolean {
  if (tileY < 0 || tileY >= grid.length) return false;
  const row = grid[tileY];
  if (!row || tileX < 0 || tileX >= row.length) return false;
  const char = row[tileX];
  return char !== '#'; // '#' represents an impassable stone wall
}

/**
 * Circle / AABB overlap check for pickups
 */
export function isCollidingWithEntity(
  x1: number,
  y1: number,
  r1: number,
  x2: number,
  y2: number,
  r2: number
): boolean {
  const dx = x1 - x2;
  const dy = y1 - y2;
  const distSq = dx * dx + dy * dy;
  const radSum = r1 + r2;
  return distSq <= radSum * radSum;
}

/**
 * Applies damage to player with shield & invulnerability logic
 */
export function applyDamageToPlayer(player: PlayerState, damage: number = 1): { player: PlayerState; damaged: boolean } {
  if (player.isDead || player.invulnerabilityTimer > 0) {
    return { player: { ...player }, damaged: false };
  }

  // If shield is active, absorb hit and destroy shield
  if (player.hasShield) {
    return {
      player: {
        ...player,
        hasShield: false,
        invulnerabilityTimer: 1.2, // 1.2 seconds grace period
      },
      damaged: true,
    };
  }

  const newLives = Math.max(0, player.lives - damage);
  return {
    player: {
      ...player,
      lives: newLives,
      isDead: newLives <= 0,
      invulnerabilityTimer: newLives > 0 ? 1.8 : 0, // 1.8s invulnerability on hit
    },
    damaged: true,
  };
}

/**
 * Checks if 5 bananas collected
 */
export function checkLevelObjectiveMet(bananasCollected: number, target: number = 5): boolean {
  return bananasCollected >= target;
}

/**
 * Computes level completion score
 */
export function calculateLevelScore(
  timeSeconds: number,
  bananasCollected: number,
  livesRemaining: number,
  bonusItemsCount: number = 0
): { score: number; stars: number } {
  const bananaScore = bananasCollected * 1000;
  const timeBonus = Math.max(0, 3000 - Math.floor(timeSeconds) * 25);
  const livesBonus = livesRemaining * 800;
  const bonusItemScore = bonusItemsCount * 500;
  
  const score = bananaScore + timeBonus + livesBonus + bonusItemScore;

  // Star rating logic (1 to 3 stars)
  let stars = 1;
  if (livesRemaining >= 3 && timeSeconds <= 60) {
    stars = 3;
  } else if (livesRemaining >= 2 && timeSeconds <= 120) {
    stars = 2;
  }

  return { score, stars };
}

/**
 * Next position clamp with walls
 */
export function resolveMovement(
  currentX: number,
  currentY: number,
  targetX: number,
  targetY: number,
  radius: number,
  grid: string[]
): { x: number; y: number } {
  // Try direct move
  const canMoveX = canOccupyPosition(targetX, currentY, radius, grid);
  const canMoveY = canOccupyPosition(currentX, targetY, radius, grid);

  let finalX = currentX;
  let finalY = currentY;

  if (canMoveX) {
    finalX = targetX;
  }
  if (canMoveY) {
    finalY = targetY;
  }

  // If diagonal stuck, test target both
  if (!canMoveX && !canMoveY && canOccupyPosition(targetX, targetY, radius, grid)) {
    return { x: targetX, y: targetY };
  }

  return { x: finalX, y: finalY };
}

export function canOccupyPosition(x: number, y: number, radius: number, grid: string[]): boolean {
  // Test four corners of bounding box
  const minX = Math.floor(x - radius);
  const maxX = Math.floor(x + radius);
  const minY = Math.floor(y - radius);
  const maxY = Math.floor(y + radius);

  for (let ty = minY; ty <= maxY; ty++) {
    for (let tx = minX; tx <= maxX; tx++) {
      if (!isTileWalkable(grid, tx, ty)) {
        return false;
      }
    }
  }
  return true;
}
