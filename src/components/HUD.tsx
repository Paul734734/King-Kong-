/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { Volume2, VolumeX, Pause, Play, RotateCcw, MapPin, BookOpen, Shield, Zap } from 'lucide-react';
import { LevelDefinition } from '../game/levels.ts';

interface HUDProps {
  level: LevelDefinition;
  lives: number;
  maxLives: number;
  bananas: number;
  targetBananas: number;
  elapsedSeconds: number;
  isPaused: boolean;
  isMuted: boolean;
  onTogglePause: () => void;
  onToggleMute: () => void;
  onRestart: () => void;
  onOpenMaquette: () => void;
  onVirtualDirection: (dir: { x: number; y: number } | null) => void;
}

export const HUD: React.FC<HUDProps> = ({
  level,
  lives,
  maxLives,
  bananas,
  targetBananas,
  elapsedSeconds,
  isPaused,
  isMuted,
  onTogglePause,
  onToggleMute,
  onRestart,
  onOpenMaquette,
  onVirtualDirection,
}) => {
  const [showMinimap, setShowMinimap] = useState(true);

  // Format time mm:ss
  const mins = Math.floor(elapsedSeconds / 60);
  const secs = Math.floor(elapsedSeconds % 60);
  const formattedTime = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;

  const allBananasFound = bananas >= targetBananas;

  return (
    <div className="pointer-events-none absolute inset-0 z-10 flex flex-col justify-between p-3 sm:p-5 select-none">
      {/* Top Header / Bar */}
      <header className="flex items-start justify-between gap-3 w-full">
        {/* Left: Level Info & Objectives */}
        <div className="flex flex-col gap-2">
          {/* Level Badge & Title */}
          <div className="pointer-events-auto bg-neutral-900/90 border border-amber-500/30 rounded-xl px-3.5 py-2 shadow-lg backdrop-blur-md flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-amber-500/20 border border-amber-400/40 flex items-center justify-center font-cinzel font-bold text-amber-400 text-sm">
              N{level.id}
            </div>
            <div>
              <div className="text-[11px] font-semibold tracking-wider uppercase text-amber-400/80">
                {level.title}
              </div>
              <div className="text-xs text-neutral-300 font-medium hidden sm:block">
                {level.subtitle}
              </div>
            </div>
          </div>

          {/* Vies Royales (Hearts) & Banana Tracker */}
          <div className="flex flex-wrap items-center gap-2">
            {/* Lives sockets */}
            <div
              className="pointer-events-auto bg-neutral-900/90 border border-red-500/30 rounded-xl px-3 py-1.5 shadow-md flex items-center gap-1.5"
              aria-label={`Vies restantes: ${lives} sur ${maxLives}`}
            >
              <span className="text-[10px] font-bold uppercase tracking-wider text-red-400 mr-1">Vies</span>
              {Array.from({ length: maxLives }).map((_, i) => (
                <span
                  key={i}
                  className={`text-base transition-transform ${
                    i < lives ? 'text-red-500 scale-100 animate-pulse' : 'text-neutral-700 scale-90 opacity-40'
                  }`}
                >
                  ❤️
                </span>
              ))}
            </div>

            {/* Banana Progress */}
            <div
              className={`pointer-events-auto border rounded-xl px-3.5 py-1.5 shadow-md flex items-center gap-2 transition-all ${
                allBananasFound
                  ? 'bg-amber-500/20 border-amber-400 gold-glow animate-bounce'
                  : 'bg-neutral-900/90 border-amber-500/40'
              }`}
            >
              <span className="text-lg">🍌</span>
              <div className="flex flex-col">
                <div className="flex items-center gap-1.5 font-cinzel font-bold text-sm text-amber-300 tabular-nums">
                  <span>{bananas}</span>
                  <span className="text-neutral-500 text-xs">/</span>
                  <span>{targetBananas}</span>
                </div>
                {allBananasFound && (
                  <span className="text-[10px] font-bold text-amber-300 uppercase tracking-tight">
                    Sanctuaire Ouvert ! 👑
                  </span>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Right: Controls & Timer */}
        <div className="flex flex-col items-end gap-2">
          {/* Action Buttons */}
          <div className="pointer-events-auto flex items-center gap-1.5 bg-neutral-900/90 border border-neutral-800 rounded-xl p-1.5 shadow-lg">
            {/* Maquette Documentation */}
            <button
              onClick={onOpenMaquette}
              className="p-2 rounded-lg hover:bg-neutral-800 text-neutral-300 hover:text-amber-400 transition-colors flex items-center gap-1 text-xs font-semibold"
              title="Documentation & Maquette"
              aria-label="Ouvrir la maquette et spécifications"
            >
              <BookOpen className="w-4 h-4 text-amber-400" />
              <span className="hidden md:inline">Spécifications</span>
            </button>

            <div className="w-[1px] h-4 bg-neutral-800 my-auto" />

            {/* Mute button */}
            <button
              onClick={onToggleMute}
              className="p-2 rounded-lg hover:bg-neutral-800 text-neutral-300 hover:text-white transition-colors"
              title={isMuted ? "Activer le son (M)" : "Couper le son (M)"}
              aria-label="Basculer le son"
            >
              {isMuted ? <VolumeX className="w-4 h-4 text-red-400" /> : <Volume2 className="w-4 h-4 text-emerald-400" />}
            </button>

            {/* Restart button */}
            <button
              onClick={onRestart}
              className="p-2 rounded-lg hover:bg-neutral-800 text-neutral-300 hover:text-amber-400 transition-colors"
              title="Recommencer le niveau (R)"
              aria-label="Recommencer le niveau"
            >
              <RotateCcw className="w-4 h-4" />
            </button>

            {/* Pause button */}
            <button
              onClick={onTogglePause}
              className="p-2 rounded-lg hover:bg-neutral-800 text-neutral-300 hover:text-amber-400 transition-colors"
              title={isPaused ? "Reprendre (P / Echap)" : "Pause (P / Echap)"}
              aria-label="Mettre en pause ou reprendre"
            >
              {isPaused ? <Play className="w-4 h-4 text-amber-400" /> : <Pause className="w-4 h-4" />}
            </button>
          </div>

          {/* Chronometer */}
          <div className="pointer-events-auto bg-neutral-900/90 border border-neutral-800/80 rounded-xl px-3 py-1 text-right shadow-md">
            <span className="text-[10px] uppercase font-bold text-neutral-400 block tracking-wider">Temps</span>
            <span className="font-mono text-sm font-bold text-neutral-200 tabular-nums">
              {formattedTime}
            </span>
          </div>
        </div>
      </header>

      {/* Objective banner in center top if completed */}
      {allBananasFound && (
        <div className="pointer-events-auto mx-auto -mt-6 bg-amber-500/90 text-neutral-950 font-bold px-4 py-1.5 rounded-full shadow-xl border border-amber-300 text-xs sm:text-sm tracking-wide flex items-center gap-2 animate-pulse">
          <span>👑</span>
          <span>5 BANANES RASSEMBLÉES ! Rejoignez l'Arche Royale pour triompher !</span>
        </div>
      )}

      {/* Bottom Area: Virtual D-Pad for Mobile & Instructions Footer */}
      <footer className="w-full flex items-end justify-between gap-4 mt-auto">
        {/* Keyboard instruction hint (hidden on small touch screens) */}
        <div className="pointer-events-auto hidden sm:flex items-center gap-2 bg-neutral-900/80 border border-neutral-800/80 rounded-lg px-3 py-1.5 text-[11px] text-neutral-400 backdrop-blur-sm">
          <span className="text-amber-400 font-semibold">Déplacement :</span>
          <kbd className="px-1.5 py-0.5 bg-neutral-800 rounded border border-neutral-700 text-neutral-200">ZQSD</kbd>
          <span>ou</span>
          <kbd className="px-1.5 py-0.5 bg-neutral-800 rounded border border-neutral-700 text-neutral-200">Flèches</kbd>
          <span className="text-neutral-500">·</span>
          <span>Objectif : 5 🍌 sans périr</span>
        </div>

        {/* Mobile On-Screen Virtual D-Pad (Touch friendly) */}
        <div className="pointer-events-auto sm:hidden ml-auto grid grid-cols-3 gap-1 bg-neutral-900/80 p-2 rounded-2xl border border-neutral-800 backdrop-blur-md">
          <div />
          <button
            onTouchStart={() => onVirtualDirection({ x: 0, y: -1 })}
            onTouchEnd={() => onVirtualDirection(null)}
            onMouseDown={() => onVirtualDirection({ x: 0, y: -1 })}
            onMouseUp={() => onVirtualDirection(null)}
            className="w-11 h-11 bg-neutral-800 active:bg-amber-600 rounded-xl flex items-center justify-center text-lg active:scale-95 transition-all text-neutral-200"
            aria-label="Haut"
          >
            ▲
          </button>
          <div />

          <button
            onTouchStart={() => onVirtualDirection({ x: -1, y: 0 })}
            onTouchEnd={() => onVirtualDirection(null)}
            onMouseDown={() => onVirtualDirection({ x: -1, y: 0 })}
            onMouseUp={() => onVirtualDirection(null)}
            className="w-11 h-11 bg-neutral-800 active:bg-amber-600 rounded-xl flex items-center justify-center text-lg active:scale-95 transition-all text-neutral-200"
            aria-label="Gauche"
          >
            ◀
          </button>
          <div className="w-11 h-11 flex items-center justify-center text-xs text-amber-500 font-bold">
            👑
          </div>
          <button
            onTouchStart={() => onVirtualDirection({ x: 1, y: 0 })}
            onTouchEnd={() => onVirtualDirection(null)}
            onMouseDown={() => onVirtualDirection({ x: 1, y: 0 })}
            onMouseUp={() => onVirtualDirection(null)}
            className="w-11 h-11 bg-neutral-800 active:bg-amber-600 rounded-xl flex items-center justify-center text-lg active:scale-95 transition-all text-neutral-200"
            aria-label="Droite"
          >
            ▶
          </button>

          <div />
          <button
            onTouchStart={() => onVirtualDirection({ x: 0, y: 1 })}
            onTouchEnd={() => onVirtualDirection(null)}
            onMouseDown={() => onVirtualDirection({ x: 0, y: 1 })}
            onMouseUp={() => onVirtualDirection(null)}
            className="w-11 h-11 bg-neutral-800 active:bg-amber-600 rounded-xl flex items-center justify-center text-lg active:scale-95 transition-all text-neutral-200"
            aria-label="Bas"
          >
            ▼
          </button>
          <div />
        </div>
      </footer>
    </div>
  );
};
