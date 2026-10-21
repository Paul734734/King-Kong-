/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useEffect, useRef } from 'react';
import { LevelDefinition } from './levels.ts';
import { sounds } from './sound.ts';
import {
  isCollidingWithEntity,
  applyDamageToPlayer,
  checkLevelObjectiveMet,
  resolveMovement,
  PlayerState,
  ItemPickup,
} from './rules.ts';

interface GameCanvasProps {
  level: LevelDefinition;
  onBananaCollected: (count: number) => void;
  onLivesChanged: (lives: number) => void;
  onGameOver: (reason: string) => void;
  onLevelComplete: (timeSeconds: number, livesRemaining: number, bonusCount: number) => void;
  isPaused: boolean;
  virtualInput: { x: number; y: number } | null;
}

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  life: number;
  maxLife: number;
  color: string;
  size: number;
}

export const GameCanvas: React.FC<GameCanvasProps> = ({
  level,
  onBananaCollected,
  onLivesChanged,
  onGameOver,
  onLevelComplete,
  isPaused,
  virtualInput,
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  // Live mutable simulation state in refs to prevent React rerender teardowns at 60Hz
  const stateRef = useRef({
    player: {
      x: level.playerSpawn.x,
      y: level.playerSpawn.y,
      lives: 3,
      maxLives: 5,
      bananasCollected: 0,
      targetBananas: 5,
      hasShield: false,
      invulnerabilityTimer: 0,
      isDead: false,
    } as PlayerState,
    speedBoostTimer: 0,
    facing: 'down' as 'up' | 'down' | 'left' | 'right',
    walkCycle: 0,
    isMoving: false,
    bonusItemsCollected: 0,
    startTime: performance.now(),
    lastFrameTime: performance.now(),
    elapsedSeconds: 0,
    completed: false,
    trauma: 0, // camera shake trauma
    pickups: level.pickups.map(p => ({ ...p, collected: false })) as ItemPickup[],
    traps: level.traps.map(t => ({
      ...t,
      timer: t.offset % t.interval,
      active: false,
      warning: false,
    })),
    enemies: level.enemies.map(e => ({
      ...e,
      currentX: e.x,
      currentY: e.y,
      dir: 1,
      animTime: 0,
    })),
    particles: [] as Particle[],
    keys: {
      up: false,
      down: false,
      left: false,
      right: false,
    },
  });

  // Track keyboard inputs
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const k = e.key.toLowerCase();
      if (['arrowup', 'w', 'z'].includes(k)) stateRef.current.keys.up = true;
      if (['arrowdown', 's'].includes(k)) stateRef.current.keys.down = true;
      if (['arrowleft', 'a', 'q'].includes(k)) stateRef.current.keys.left = true;
      if (['arrowright', 'd'].includes(k)) stateRef.current.keys.right = true;
    };

    const handleKeyUp = (e: KeyboardEvent) => {
      const k = e.key.toLowerCase();
      if (['arrowup', 'w', 'z'].includes(k)) stateRef.current.keys.up = false;
      if (['arrowdown', 's'].includes(k)) stateRef.current.keys.down = false;
      if (['arrowleft', 'a', 'q'].includes(k)) stateRef.current.keys.left = false;
      if (['arrowright', 'd'].includes(k)) stateRef.current.keys.right = false;
    };

    const handleBlur = () => {
      stateRef.current.keys.up = false;
      stateRef.current.keys.down = false;
      stateRef.current.keys.left = false;
      stateRef.current.keys.right = false;
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);
    window.addEventListener('blur', handleBlur);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
      window.removeEventListener('blur', handleBlur);
    };
  }, []);

  // Reset or initialize level state when level changes
  useEffect(() => {
    stateRef.current = {
      player: {
        x: level.playerSpawn.x,
        y: level.playerSpawn.y,
        lives: 3,
        maxLives: 5,
        bananasCollected: 0,
        targetBananas: 5,
        hasShield: false,
        invulnerabilityTimer: 0,
        isDead: false,
      },
      speedBoostTimer: 0,
      facing: 'down',
      walkCycle: 0,
      isMoving: false,
      bonusItemsCollected: 0,
      startTime: performance.now(),
      lastFrameTime: performance.now(),
      elapsedSeconds: 0,
      completed: false,
      trauma: 0,
      pickups: level.pickups.map(p => ({ ...p, collected: false })),
      traps: level.traps.map(t => ({
        ...t,
        timer: t.offset % t.interval,
        active: false,
        warning: false,
      })),
      enemies: level.enemies.map(e => ({
        ...e,
        currentX: e.x,
        currentY: e.y,
        dir: 1,
        animTime: 0,
      })),
      particles: [],
      keys: { up: false, down: false, left: false, right: false },
    };
    onBananaCollected(0);
    onLivesChanged(3);
  }, [level, onBananaCollected, onLivesChanged]);

  // Main 60 FPS Canvas Game Loop
  useEffect(() => {
    let animId: number;

    const render = (time: number) => {
      const s = stateRef.current;
      const rawDt = (time - s.lastFrameTime) / 1000;
      s.lastFrameTime = time;
      const dt = Math.min(rawDt, 0.05); // clamped dt

      const canvas = canvasRef.current;
      if (!canvas) {
        animId = requestAnimationFrame(render);
        return;
      }
      const ctx = canvas.getContext('2d');
      if (!ctx) {
        animId = requestAnimationFrame(render);
        return;
      }

      // Handle Resize smoothly
      const dpr = window.devicePixelRatio || 1;
      const displayWidth = canvas.parentElement ? canvas.parentElement.clientWidth : 800;
      const displayHeight = canvas.parentElement ? canvas.parentElement.clientHeight : 600;

      if (canvas.width !== displayWidth * dpr || canvas.height !== displayHeight * dpr) {
        canvas.width = displayWidth * dpr;
        canvas.height = displayHeight * dpr;
      }

      ctx.save();
      ctx.scale(dpr, dpr);

      // Simulation Updates (if not paused, not dead, not completed)
      if (!isPaused && !s.player.isDead && !s.completed) {
        s.elapsedSeconds += dt;

        // Timers
        if (s.player.invulnerabilityTimer > 0) {
          s.player.invulnerabilityTimer -= dt;
        }
        if (s.speedBoostTimer > 0) {
          s.speedBoostTimer -= dt;
        }
        if (s.trauma > 0) {
          s.trauma = Math.max(0, s.trauma - dt * 2.5);
        }

        // Input Vector
        let moveX = 0;
        let moveY = 0;

        if (s.keys.up) moveY -= 1;
        if (s.keys.down) moveY += 1;
        if (s.keys.left) moveX -= 1;
        if (s.keys.right) moveX += 1;

        // Merge virtual input if active
        if (virtualInput && (virtualInput.x !== 0 || virtualInput.y !== 0)) {
          moveX = virtualInput.x;
          moveY = virtualInput.y;
        }

        // Normalize
        const len = Math.hypot(moveX, moveY);
        s.isMoving = len > 0.05;

        if (s.isMoving) {
          const normX = moveX / len;
          const normY = moveY / len;

          // Facing direction
          if (Math.abs(normX) > Math.abs(normY)) {
            s.facing = normX > 0 ? 'right' : 'left';
          } else {
            s.facing = normY > 0 ? 'down' : 'up';
          }

          const baseSpeed = s.speedBoostTimer > 0 ? 4.5 : 3.0; // tiles per second
          const stepDist = baseSpeed * dt;
          const targetX = s.player.x + normX * stepDist;
          const targetY = s.player.y + normY * stepDist;

          const resolved = resolveMovement(
            s.player.x,
            s.player.y,
            targetX,
            targetY,
            0.34,
            level.grid
          );
          s.player.x = resolved.x;
          s.player.y = resolved.y;

          s.walkCycle += dt * 8;
        }

        // Check Pickups
        s.pickups.forEach((pickup) => {
          if (pickup.collected) return;
          if (isCollidingWithEntity(s.player.x, s.player.y, 0.38, pickup.x, pickup.y, 0.35)) {
            pickup.collected = true;

            if (pickup.type === 'banana') {
              s.player.bananasCollected += 1;
              sounds.playBanana();
              onBananaCollected(s.player.bananasCollected);

              // Spawn celebration sparkle particles
              for (let i = 0; i < 15; i++) {
                const angle = Math.random() * Math.PI * 2;
                const spd = 1.2 + Math.random() * 2.5;
                s.particles.push({
                  x: pickup.x,
                  y: pickup.y,
                  vx: Math.cos(angle) * spd,
                  vy: Math.sin(angle) * spd,
                  life: 0.6,
                  maxLife: 0.6,
                  color: '#fbbf24',
                  size: 3 + Math.random() * 3,
                });
              }
            } else if (pickup.type === 'heart') {
              s.player.lives = Math.min(s.player.maxLives, s.player.lives + 1);
              s.bonusItemsCollected += 1;
              sounds.playHeart();
              onLivesChanged(s.player.lives);

              for (let i = 0; i < 12; i++) {
                s.particles.push({
                  x: pickup.x,
                  y: pickup.y,
                  vx: (Math.random() - 0.5) * 2,
                  vy: (Math.random() - 0.5) * 2,
                  life: 0.5,
                  maxLife: 0.5,
                  color: '#f43f5e',
                  size: 4,
                });
              }
            } else if (pickup.type === 'shield') {
              s.player.hasShield = true;
              s.bonusItemsCollected += 1;
              sounds.playShield();
            } else if (pickup.type === 'speed') {
              s.speedBoostTimer = 6.0; // 6 seconds of speed
              s.bonusItemsCollected += 1;
              sounds.playShield();
            }
          }
        });

        // Update Traps
        s.traps.forEach((trap) => {
          trap.timer = (trap.timer + dt) % trap.interval;
          const burstStart = trap.interval * 0.65;
          const warningStart = trap.interval * 0.45;

          trap.warning = trap.timer >= warningStart && trap.timer < burstStart;
          trap.active = trap.timer >= burstStart;

          // Check trap damage if active
          if (trap.active) {
            if (isCollidingWithEntity(s.player.x, s.player.y, 0.35, trap.x + 0.5, trap.y + 0.5, 0.35)) {
              const res = applyDamageToPlayer(s.player, 1);
              if (res.damaged) {
                s.player = res.player;
                s.trauma = 1.0; // camera shake!
                sounds.playDamage();
                onLivesChanged(s.player.lives);

                // Blood/star particles
                for (let i = 0; i < 14; i++) {
                  s.particles.push({
                    x: s.player.x,
                    y: s.player.y,
                    vx: (Math.random() - 0.5) * 3,
                    vy: (Math.random() - 0.5) * 3,
                    life: 0.4,
                    maxLife: 0.4,
                    color: '#ef4444',
                    size: 3,
                  });
                }

                if (s.player.isDead) {
                  sounds.playGameOver();
                  onGameOver(trap.type === 'spikes' ? "Empalé par des pics royaux !" : "Brûlé par les flammes du donjon !");
                }
              }
            }
          }
        });

        // Update Enemies
        s.enemies.forEach((enemy) => {
          enemy.animTime += dt;
          if (enemy.patrolAxis === 'x') {
            enemy.currentX += enemy.dir * enemy.speed * dt;
            if (Math.abs(enemy.currentX - enemy.x) > enemy.patrolRange) {
              enemy.dir *= -1;
            }
          } else if (enemy.patrolAxis === 'y') {
            enemy.currentY += enemy.dir * enemy.speed * dt;
            if (Math.abs(enemy.currentY - enemy.y) > enemy.patrolRange) {
              enemy.dir *= -1;
            }
          } else if (enemy.patrolAxis === 'circle') {
            // slight wobble
            enemy.currentX = enemy.x + Math.sin(enemy.animTime * 2) * 0.1;
            enemy.currentY = enemy.y + Math.cos(enemy.animTime * 2) * 0.1;
          }

          // Enemy collision with King
          if (isCollidingWithEntity(s.player.x, s.player.y, 0.36, enemy.currentX, enemy.currentY, 0.38)) {
            const res = applyDamageToPlayer(s.player, 1);
            if (res.damaged) {
              s.player = res.player;
              s.trauma = 1.0;
              sounds.playDamage();
              onLivesChanged(s.player.lives);

              for (let i = 0; i < 14; i++) {
                s.particles.push({
                  x: s.player.x,
                  y: s.player.y,
                  vx: (Math.random() - 0.5) * 3,
                  vy: (Math.random() - 0.5) * 3,
                  life: 0.4,
                  maxLife: 0.4,
                  color: '#f97316',
                  size: 3,
                });
              }

              if (s.player.isDead) {
                sounds.playGameOver();
                onGameOver(`Attaqué par ${enemy.name} !`);
              }
            }
          }
        });

        // Check Sanctuary Exit Goal
        const goalMet = checkLevelObjectiveMet(s.player.bananasCollected, s.player.targetBananas);
        if (goalMet) {
          if (isCollidingWithEntity(s.player.x, s.player.y, 0.38, level.sanctuaryExit.x, level.sanctuaryExit.y, 0.45)) {
            s.completed = true;
            sounds.playLevelVictory();
            onLevelComplete(s.elapsedSeconds, s.player.lives, s.bonusItemsCollected);
          }
        }
      }

      // Update Particles
      for (let i = s.particles.length - 1; i >= 0; i--) {
        const p = s.particles[i];
        p.life -= dt;
        p.x += p.vx * dt;
        p.y += p.vy * dt;
        if (p.life <= 0) {
          s.particles.splice(i, 1);
        }
      }

      // ================= CAMERA & DRAWING PASS =================
      const tileSize = 48; // pixel size per grid tile
      const viewW = displayWidth;
      const viewH = displayHeight;
      const levelPixelW = level.width * tileSize;
      const levelPixelH = level.height * tileSize;

      // Smart camera: Center if maze fits inside view, otherwise clamp cleanly to maze edges
      let targetCamX = s.player.x * tileSize - viewW / 2;
      let targetCamY = s.player.y * tileSize - viewH / 2;

      if (levelPixelW <= viewW) {
        targetCamX = -(viewW - levelPixelW) / 2;
      } else {
        targetCamX = Math.max(0, Math.min(levelPixelW - viewW, targetCamX));
      }

      if (levelPixelH <= viewH) {
        targetCamY = -(viewH - levelPixelH) / 2;
      } else {
        targetCamY = Math.max(0, Math.min(levelPixelH - viewH, targetCamY));
      }

      // Add trauma screen shake
      const shakeX = (Math.random() - 0.5) * 14 * (s.trauma * s.trauma);
      const shakeY = (Math.random() - 0.5) * 14 * (s.trauma * s.trauma);
      const camX = targetCamX + shakeX;
      const camY = targetCamY + shakeY;

      ctx.fillStyle = '#070709';
      ctx.fillRect(0, 0, viewW, viewH);

      ctx.save();
      ctx.translate(-camX, -camY);

      // Draw Grid / Maze Floor & Walls
      const minTileX = Math.max(0, Math.floor(camX / tileSize));
      const maxTileX = Math.min(level.width - 1, Math.ceil((camX + viewW) / tileSize));
      const minTileY = Math.max(0, Math.floor(camY / tileSize));
      const maxTileY = Math.min(level.height - 1, Math.ceil((camY + viewH) / tileSize));

      for (let ty = minTileY; ty <= maxTileY; ty++) {
        for (let tx = minTileX; tx <= maxTileX; tx++) {
          const char = level.grid[ty]?.[tx];
          const px = tx * tileSize;
          const py = ty * tileSize;

          if (char === '#') {
            // Stylized Wall
            ctx.fillStyle = level.wallColor;
            ctx.fillRect(px, py, tileSize, tileSize);

            // 3D Bevel highlight
            ctx.fillStyle = 'rgba(255, 255, 255, 0.18)';
            ctx.fillRect(px, py, tileSize, 4);
            ctx.fillRect(px, py, 4, tileSize);

            // Bevel shadow
            ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
            ctx.fillRect(px, py + tileSize - 4, tileSize, 4);
            ctx.fillRect(px + tileSize - 4, py, 4, tileSize);

            // Inner engraved brick stone detail
            ctx.strokeStyle = 'rgba(0, 0, 0, 0.35)';
            ctx.lineWidth = 1.5;
            ctx.strokeRect(px + 4, py + 4, tileSize - 8, tileSize - 8);

            // Accent royal trim on wall joints
            if ((tx + ty) % 4 === 0) {
              ctx.fillStyle = `${level.accentColor}33`;
              ctx.fillRect(px + tileSize / 2 - 3, py + tileSize / 2 - 3, 6, 6);
            }
          } else {
            // Floor tile
            ctx.fillStyle = level.floorColor;
            ctx.fillRect(px, py, tileSize, tileSize);

            // Cobblestone tile pattern
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
            ctx.lineWidth = 1;
            ctx.strokeRect(px, py, tileSize, tileSize);
          }
        }
      }

      // Draw Traps
      s.traps.forEach((trap) => {
        const px = trap.x * tileSize;
        const py = trap.y * tileSize;

        ctx.fillStyle = '#0f172a';
        ctx.fillRect(px + 3, py + 3, tileSize - 6, tileSize - 6);

        // Outer trap frame
        ctx.strokeStyle = trap.warning ? '#f59e0b' : trap.active ? '#ef4444' : '#334155';
        ctx.lineWidth = 2;
        ctx.strokeRect(px + 3, py + 3, tileSize - 6, tileSize - 6);

        if (trap.type === 'spikes') {
          if (trap.warning) {
            // Warning glowing sockets
            ctx.fillStyle = '#f59e0b';
            for (let i = 0; i < 4; i++) {
              ctx.beginPath();
              ctx.arc(px + 14 + (i % 2) * 20, py + 14 + Math.floor(i / 2) * 20, 4, 0, Math.PI * 2);
              ctx.fill();
            }
          }
          if (trap.active) {
            // Thrusting steel spikes
            ctx.fillStyle = '#f8fafc';
            for (let i = 0; i < 4; i++) {
              const sx = px + 14 + (i % 2) * 20;
              const sy = py + 14 + Math.floor(i / 2) * 20;
              ctx.beginPath();
              ctx.moveTo(sx, sy - 10);
              ctx.lineTo(sx - 6, sy + 6);
              ctx.lineTo(sx + 6, sy + 6);
              ctx.closePath();
              ctx.fill();

              ctx.fillStyle = '#94a3b8';
              ctx.beginPath();
              ctx.moveTo(sx, sy - 10);
              ctx.lineTo(sx, sy + 6);
              ctx.lineTo(sx + 6, sy + 6);
              ctx.closePath();
              ctx.fill();
            }
          }
        } else if (trap.type === 'fire') {
          if (trap.warning) {
            ctx.fillStyle = 'rgba(249, 115, 22, 0.45)';
            ctx.beginPath();
            ctx.arc(px + tileSize / 2, py + tileSize / 2, 16, 0, Math.PI * 2);
            ctx.fill();
          }
          if (trap.active) {
            // Multi-layer flame burst
            const fRadius = 18 + Math.sin(time * 0.02) * 3;
            ctx.fillStyle = '#ef4444';
            ctx.beginPath();
            ctx.arc(px + tileSize / 2, py + tileSize / 2, fRadius, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = '#f97316';
            ctx.beginPath();
            ctx.arc(px + tileSize / 2, py + tileSize / 2, fRadius * 0.7, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = '#fef08a';
            ctx.beginPath();
            ctx.arc(px + tileSize / 2, py + tileSize / 2, fRadius * 0.4, 0, Math.PI * 2);
            ctx.fill();
          }
        }
      });

      // Draw Sanctuary Exit (Arche Royale)
      const exitPx = level.sanctuaryExit.x * tileSize;
      const exitPy = level.sanctuaryExit.y * tileSize;
      const goalReady = s.player.bananasCollected >= s.player.targetBananas;

      ctx.save();
      ctx.translate(exitPx, exitPy);

      if (goalReady) {
        // Glorious radiating golden portal
        const pulse = 1 + Math.sin(time * 0.007) * 0.2;
        const grad = ctx.createRadialGradient(0, 0, 4, 0, 0, 36 * pulse);
        grad.addColorStop(0, 'rgba(254, 240, 138, 0.95)');
        grad.addColorStop(0.5, 'rgba(245, 158, 11, 0.7)');
        grad.addColorStop(1, 'rgba(217, 119, 6, 0)');
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(0, 0, 36 * pulse, 0, Math.PI * 2);
        ctx.fill();

        // Royal Sanctuary Pillars & Arch
        ctx.fillStyle = '#fbbf24';
        ctx.fillRect(-20, -22, 40, 44);

        ctx.fillStyle = '#1c1917';
        ctx.beginPath();
        ctx.arc(0, 2, 14, Math.PI, 0);
        ctx.lineTo(14, 20);
        ctx.lineTo(-14, 20);
        ctx.closePath();
        ctx.fill();

        ctx.font = '20px Cinzel, serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('👑', 0, -5);
      } else {
        // Locked Stone Gate
        ctx.fillStyle = '#334155';
        ctx.fillRect(-18, -20, 36, 40);

        ctx.strokeStyle = '#64748b';
        ctx.lineWidth = 2;
        ctx.strokeRect(-16, -18, 32, 36);

        ctx.font = '16px sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('🔒', 0, 0);
      }
      ctx.restore();

      // Draw Pickups
      s.pickups.forEach((pickup) => {
        if (pickup.collected) return;
        const px = pickup.x * tileSize;
        const py = pickup.y * tileSize;
        const bob = Math.sin(time * 0.005 + pickup.x * 2) * 5;

        ctx.save();
        ctx.translate(px, py + bob);

        if (pickup.type === 'banana') {
          // Radiant golden aura
          ctx.beginPath();
          ctx.arc(0, 0, 15, 0, Math.PI * 2);
          ctx.fillStyle = 'rgba(251, 191, 36, 0.35)';
          ctx.fill();

          ctx.font = '26px sans-serif';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText('🍌', 0, 0);
        } else if (pickup.type === 'heart') {
          ctx.beginPath();
          ctx.arc(0, 0, 14, 0, Math.PI * 2);
          ctx.fillStyle = 'rgba(239, 68, 68, 0.3)';
          ctx.fill();

          ctx.font = '22px sans-serif';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText('❤️', 0, 0);
        } else if (pickup.type === 'shield') {
          ctx.beginPath();
          ctx.arc(0, 0, 15, 0, Math.PI * 2);
          ctx.fillStyle = 'rgba(56, 189, 248, 0.35)';
          ctx.fill();

          ctx.font = '22px sans-serif';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText('🛡️', 0, 0);
        } else if (pickup.type === 'speed') {
          ctx.font = '22px sans-serif';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText('⚡', 0, 0);
        }

        ctx.restore();
      });

      // Draw Enemies
      s.enemies.forEach((enemy) => {
        const ePx = enemy.currentX * tileSize;
        const ePy = enemy.currentY * tileSize;

        ctx.save();
        ctx.translate(ePx, ePy);

        // Shadow under enemy
        ctx.fillStyle = 'rgba(0, 0, 0, 0.45)';
        ctx.beginPath();
        ctx.ellipse(0, 12, 13, 6, 0, 0, Math.PI * 2);
        ctx.fill();

        if (enemy.type === 'snake') {
          const wobble = Math.sin(enemy.animTime * 8) * 3;
          ctx.font = '26px sans-serif';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText('🐍', wobble, 0);
        } else if (enemy.type === 'bat') {
          const flap = Math.sin(enemy.animTime * 14) * 5;
          ctx.font = '26px sans-serif';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText('🦇', 0, flap);
        } else if (enemy.type === 'guard') {
          ctx.font = '26px sans-serif';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText('💀', 0, 0);
        } else if (enemy.type === 'carnivorous_plant') {
          const chomp = Math.sin(enemy.animTime * 4) > 0 ? '🌱' : '🪴';
          ctx.font = '26px sans-serif';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText(chomp, 0, 0);
        }

        ctx.restore();
      });

      // Draw Particles
      s.particles.forEach((p) => {
        const px = p.x * tileSize;
        const py = p.y * tileSize;
        const alpha = p.life / p.maxLife;

        ctx.save();
        ctx.globalAlpha = Math.max(0, alpha);
        ctx.fillStyle = p.color;
        ctx.beginPath();
        ctx.arc(px, py, p.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      });

      // Draw Player: King Kong with Crown & Cape
      const kingPx = s.player.x * tileSize;
      const kingPy = s.player.y * tileSize;
      const isInvulnerable = s.player.invulnerabilityTimer > 0;
      const blink = isInvulnerable && Math.floor(time / 80) % 2 === 0;

      if (!blink) {
        ctx.save();
        ctx.translate(kingPx, kingPy);

        // Ground shadow
        ctx.fillStyle = 'rgba(0, 0, 0, 0.45)';
        ctx.beginPath();
        ctx.ellipse(0, 14, 16, 7, 0, 0, Math.PI * 2);
        ctx.fill();

        // Speed trail ghost
        if (s.speedBoostTimer > 0) {
          ctx.fillStyle = 'rgba(234, 179, 8, 0.35)';
          ctx.beginPath();
          ctx.arc(0, 0, 22, 0, Math.PI * 2);
          ctx.fill();
        }

        // Shield sphere
        if (s.player.hasShield) {
          ctx.strokeStyle = '#38bdf8';
          ctx.lineWidth = 3;
          ctx.beginPath();
          ctx.arc(0, 0, 24, 0, Math.PI * 2);
          ctx.stroke();

          ctx.fillStyle = 'rgba(56, 189, 248, 0.2)';
          ctx.fill();
        }

        // Royal Cape (crimson red)
        ctx.fillStyle = '#dc2626';
        const capeWave = Math.sin(s.walkCycle) * 3;
        ctx.beginPath();
        ctx.moveTo(-10, -6);
        ctx.lineTo(10, -6);
        ctx.lineTo(12 + capeWave, 16);
        ctx.lineTo(-12 + capeWave, 16);
        ctx.closePath();
        ctx.fill();

        // King Gorilla Body (Dark Fur & Muscular Silhouette)
        ctx.fillStyle = '#1c1917';
        ctx.beginPath();
        ctx.arc(0, 2, 14, 0, Math.PI * 2);
        ctx.fill();

        // Chest plate / Silverback highlight
        ctx.fillStyle = '#44403c';
        ctx.beginPath();
        ctx.ellipse(0, 3, 9, 7, 0, 0, Math.PI * 2);
        ctx.fill();

        // Gorilla Head & Face
        ctx.fillStyle = '#1c1917';
        ctx.beginPath();
        ctx.arc(0, -7, 10, 0, Math.PI * 2);
        ctx.fill();

        // Eyes (determined look)
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(-3, -7, 2.5, 0, Math.PI * 2);
        ctx.arc(3, -7, 2.5, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = '#000000';
        ctx.beginPath();
        ctx.arc(-3, -7, 1.2, 0, Math.PI * 2);
        ctx.arc(3, -7, 1.2, 0, Math.PI * 2);
        ctx.fill();

        // Golden Royal Crown with Rubies
        ctx.fillStyle = '#fbbf24';
        ctx.beginPath();
        ctx.moveTo(-8, -13);
        ctx.lineTo(-7, -20);
        ctx.lineTo(-3, -16);
        ctx.lineTo(0, -23); // High central peak
        ctx.lineTo(3, -16);
        ctx.lineTo(7, -20);
        ctx.lineTo(8, -13);
        ctx.closePath();
        ctx.fill();

        // Crown ruby gems
        ctx.fillStyle = '#ef4444';
        ctx.beginPath();
        ctx.arc(0, -17, 1.6, 0, Math.PI * 2);
        ctx.arc(-5, -15, 1.2, 0, Math.PI * 2);
        ctx.arc(5, -15, 1.2, 0, Math.PI * 2);
        ctx.fill();

        ctx.restore();
      }

      ctx.restore(); // restore camera transform
      ctx.restore(); // restore dpr scale

      animId = requestAnimationFrame(render);
    };

    animId = requestAnimationFrame(render);
    return () => cancelAnimationFrame(animId);
  }, [level, isPaused, virtualInput, onBananaCollected, onLivesChanged, onGameOver, onLevelComplete]);

  return (
    <div className="relative w-full h-full overflow-hidden select-none">
      <canvas
        ref={canvasRef}
        data-testid="game-canvas"
        className="w-full h-full block bg-neutral-950 cursor-crosshair touch-none"
      />
    </div>
  );
};
