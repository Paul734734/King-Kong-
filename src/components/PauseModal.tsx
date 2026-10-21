/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { Play, RotateCcw, Home, BookOpen, Volume2, VolumeX } from 'lucide-react';
import { LevelDefinition } from '../game/levels.ts';

interface PauseModalProps {
  level: LevelDefinition;
  bananas: number;
  lives: number;
  elapsedSeconds: number;
  onResume: () => void;
  onRestart: () => void;
  onHome: () => void;
  onOpenMaquette: () => void;
  isMuted: boolean;
  onToggleMute: () => void;
}

export const PauseModal: React.FC<PauseModalProps> = ({
  level,
  bananas,
  lives,
  elapsedSeconds,
  onResume,
  onRestart,
  onHome,
  onOpenMaquette,
  isMuted,
  onToggleMute,
}) => {
  const mins = Math.floor(elapsedSeconds / 60);
  const secs = Math.floor(elapsedSeconds % 60);
  const timeStr = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-in fade-in zoom-in-95 duration-200">
      <div className="relative w-full max-w-sm bg-neutral-900 border border-neutral-700 rounded-3xl p-6 sm:p-7 shadow-2xl text-center">
        <h2 className="text-2xl font-bold font-cinzel text-amber-400 mb-1">
          PAUSE ROYALE
        </h2>
        <p className="text-xs text-neutral-400 mb-5">{level.title}</p>

        {/* Current Run Snapshot */}
        <div className="grid grid-cols-3 gap-2 bg-neutral-950/80 p-3 rounded-2xl border border-neutral-800 mb-6 text-center">
          <div>
            <span className="text-[10px] text-neutral-400 block font-semibold">BANANES</span>
            <span className="text-sm font-bold text-amber-400 font-mono">🍌 {bananas}/5</span>
          </div>
          <div>
            <span className="text-[10px] text-neutral-400 block font-semibold">VIES</span>
            <span className="text-sm font-bold text-red-400 font-mono">❤️ {lives}</span>
          </div>
          <div>
            <span className="text-[10px] text-neutral-400 block font-semibold">CHRONO</span>
            <span className="text-sm font-bold text-neutral-200 font-mono">{timeStr}</span>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="space-y-2.5">
          <button
            onClick={onResume}
            className="w-full py-3 px-4 rounded-xl bg-amber-500 hover:bg-amber-400 active:scale-95 text-neutral-950 font-bold text-sm tracking-wide shadow-md flex items-center justify-center gap-2 cursor-pointer transition-all"
          >
            <Play className="w-4 h-4 fill-neutral-950" />
            <span>Reprendre la Partie (P)</span>
          </button>

          <button
            onClick={onRestart}
            className="w-full py-2.5 px-4 rounded-xl bg-neutral-800 hover:bg-neutral-700 text-neutral-200 font-medium text-xs flex items-center justify-center gap-2 transition-colors"
          >
            <RotateCcw className="w-4 h-4" />
            <span>Recommencer le Niveau (R)</span>
          </button>

          <button
            onClick={onOpenMaquette}
            className="w-full py-2.5 px-4 rounded-xl bg-neutral-800 hover:bg-neutral-700 text-amber-400 font-medium text-xs flex items-center justify-center gap-2 transition-colors"
          >
            <BookOpen className="w-4 h-4" />
            <span>Consulter la Maquette (GDD)</span>
          </button>

          <div className="flex items-center gap-2 pt-2">
            <button
              onClick={onToggleMute}
              className="flex-1 py-2 px-3 rounded-xl bg-neutral-800 hover:bg-neutral-700 text-neutral-300 text-xs flex items-center justify-center gap-1.5 transition-colors"
            >
              {isMuted ? <VolumeX className="w-4 h-4 text-red-400" /> : <Volume2 className="w-4 h-4 text-emerald-400" />}
              <span>{isMuted ? "Son Coupé" : "Son Actif"}</span>
            </button>

            <button
              onClick={onHome}
              className="flex-1 py-2 px-3 rounded-xl bg-neutral-800 hover:bg-neutral-700 text-neutral-300 text-xs flex items-center justify-center gap-1.5 transition-colors"
            >
              <Home className="w-4 h-4" />
              <span>Menu Principal</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
