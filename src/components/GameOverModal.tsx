/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { Skull, RotateCcw, Home, HelpCircle } from 'lucide-react';
import { LevelDefinition } from '../game/levels.ts';

interface GameOverModalProps {
  level: LevelDefinition;
  reason: string;
  bananasCollected: number;
  onRetry: () => void;
  onHome: () => void;
  onOpenMaquette: () => void;
}

export const GameOverModal: React.FC<GameOverModalProps> = ({
  level,
  reason,
  bananasCollected,
  onRetry,
  onHome,
  onOpenMaquette,
}) => {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md animate-in fade-in zoom-in-95 duration-200">
      <div className="relative w-full max-w-md bg-neutral-900 border-2 border-red-500/50 rounded-3xl p-6 sm:p-8 shadow-2xl danger-glow text-center overflow-hidden">
        {/* Skull Icon */}
        <div className="mx-auto mb-4 w-18 h-18 rounded-2xl bg-red-950/80 border border-red-500/40 flex items-center justify-center text-4xl shadow-inner text-red-400">
          💀
        </div>

        {/* Title */}
        <h2 className="text-2xl sm:text-3xl font-extrabold font-cinzel text-red-400 mb-1">
          LE ROI EST TOMBÉ !
        </h2>
        <p className="text-xs text-neutral-400 mb-4">{level.title}</p>

        {/* Cause of Defeat & Bananas */}
        <div className="p-3.5 rounded-xl bg-neutral-950/70 border border-neutral-800 text-left mb-6 space-y-2">
          <div className="text-xs text-neutral-300">
            <span className="font-semibold text-red-400">Cause : </span>
            {reason || "Submergé par les pièges du labyrinthe"}
          </div>
          <div className="text-xs text-neutral-300 flex items-center gap-1.5">
            <span className="font-semibold text-amber-400">Bananes Récoltées : </span>
            <span>🍌 {bananasCollected} / 5</span>
          </div>
        </div>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row items-center gap-3">
          <button
            data-start="true"
            onClick={onRetry}
            className="w-full sm:w-auto flex-1 py-3 px-5 rounded-xl bg-gradient-to-r from-red-600 to-amber-600 hover:from-red-500 hover:to-amber-500 text-white font-bold text-sm tracking-wide shadow-lg flex items-center justify-center gap-2 cursor-pointer transition-transform active:scale-95"
          >
            <RotateCcw className="w-4 h-4" />
            <span>Réessayer Immédiatement</span>
          </button>

          <button
            onClick={onHome}
            className="w-full sm:w-auto py-3 px-4 rounded-xl bg-neutral-800 hover:bg-neutral-700 text-neutral-200 font-semibold text-sm flex items-center justify-center gap-1.5 transition-colors"
          >
            <Home className="w-4 h-4" />
            Menu
          </button>
        </div>

        {/* Maquette Hint */}
        <button
          onClick={onOpenMaquette}
          className="mt-4 text-xs text-neutral-500 hover:text-amber-400 transition-colors inline-flex items-center gap-1"
        >
          <HelpCircle className="w-3.5 h-3.5" />
          Consulter les astuces et la maquette
        </button>
      </div>
    </div>
  );
};
