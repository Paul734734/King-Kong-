/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useEffect } from 'react';
import confetti from 'canvas-confetti';
import { Trophy, Star, ArrowRight, RotateCcw, Home, Sparkles } from 'lucide-react';
import { LevelDefinition } from '../game/levels.ts';

interface VictoryModalProps {
  level: LevelDefinition;
  timeSeconds: number;
  livesRemaining: number;
  bonusCollected: number;
  score: number;
  stars: number;
  onNextLevel: () => void;
  onReplay: () => void;
  onHome: () => void;
  isFinalLevel: boolean;
}

export const VictoryModal: React.FC<VictoryModalProps> = ({
  level,
  timeSeconds,
  livesRemaining,
  bonusCollected,
  score,
  stars,
  onNextLevel,
  onReplay,
  onHome,
  isFinalLevel,
}) => {
  // Fire festive confetti on mount
  useEffect(() => {
    try {
      confetti({
        particleCount: 80,
        spread: 70,
        origin: { y: 0.6 },
        colors: ['#f59e0b', '#fbbf24', '#22c55e', '#ef4444', '#ffffff'],
      });
    } catch {
      // ignore
    }
  }, []);

  const mins = Math.floor(timeSeconds / 60);
  const secs = Math.floor(timeSeconds % 60);
  const timeFormatted = `${mins}m ${secs}s`;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md animate-in fade-in zoom-in-95 duration-200">
      <div className="relative w-full max-w-lg bg-neutral-900 border-2 border-amber-500/60 rounded-3xl p-6 sm:p-8 shadow-2xl gold-glow text-center overflow-hidden">
        {/* Ambient Top Glow */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-72 h-36 bg-amber-500/20 rounded-full blur-2xl pointer-events-none" />

        {/* Crown & Trophy Icon */}
        <div className="relative mx-auto mb-4 w-20 h-20 rounded-2xl bg-gradient-to-b from-amber-400 to-amber-600 flex items-center justify-center shadow-lg text-4xl transform -rotate-3 hover:rotate-0 transition-transform">
          {isFinalLevel ? '🏆' : '👑'}
        </div>

        {/* Message de Félicitations */}
        <h2 className="text-2xl sm:text-3xl font-extrabold font-cinzel text-amber-300 mb-1">
          {isFinalLevel ? "VICTOIRE ROYALE ABSOLUE !" : "FÉLICITATIONS MAJESTÉ !"}
        </h2>
        <p className="text-xs sm:text-sm text-neutral-300 mb-6">
          {isFinalLevel
            ? "Vous avez triomphé des 5 Labyrinthes Royaux et reconquis le Trône Doré !"
            : `Vous avez rassemblé les 5 bananes du ${level.title} sans mourir !`}
        </p>

        {/* Stars Earned */}
        <div className="flex items-center justify-center gap-2 mb-6" aria-label={`Étoiles gagnées : ${stars} sur 3`}>
          {[1, 2, 3].map((s) => (
            <Star
              key={s}
              className={`w-8 h-8 transition-transform duration-300 ${
                s <= stars
                  ? 'fill-amber-400 text-amber-400 scale-110 drop-shadow'
                  : 'fill-neutral-800 text-neutral-700 scale-90'
              }`}
            />
          ))}
        </div>

        {/* Mastery Performance Metrics */}
        <div className="grid grid-cols-2 gap-3 mb-6 bg-neutral-950/70 p-4 rounded-2xl border border-neutral-800 text-left">
          <div className="space-y-0.5">
            <span className="text-[11px] font-semibold text-neutral-400 uppercase tracking-wider block">
              Bananes Récoltées
            </span>
            <div className="text-base font-bold text-amber-400 flex items-center gap-1">
              <span>🍌</span>
              <span>5 / 5 (Parfait)</span>
            </div>
          </div>

          <div className="space-y-0.5">
            <span className="text-[11px] font-semibold text-neutral-400 uppercase tracking-wider block">
              Temps d'Évasion
            </span>
            <div className="text-base font-bold text-neutral-200 tabular-nums">
              ⏱️ {timeFormatted}
            </div>
          </div>

          <div className="space-y-0.5">
            <span className="text-[11px] font-semibold text-neutral-400 uppercase tracking-wider block">
              Cœurs Préservés
            </span>
            <div className="text-base font-bold text-red-400 flex items-center gap-1">
              <span>❤️</span>
              <span>{livesRemaining} vie{livesRemaining > 1 ? 's' : ''}</span>
            </div>
          </div>

          <div className="space-y-0.5">
            <span className="text-[11px] font-semibold text-neutral-400 uppercase tracking-wider block">
              Score du Niveau
            </span>
            <div className="text-base font-bold text-amber-300 tabular-nums font-mono">
              ⭐ {score.toLocaleString()}
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row items-center gap-3">
          {!isFinalLevel ? (
            <button
              data-start="true"
              onClick={onNextLevel}
              className="w-full sm:w-auto flex-1 py-3 px-5 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-neutral-950 font-bold text-sm tracking-wide shadow-lg flex items-center justify-center gap-2 cursor-pointer transition-transform active:scale-95"
            >
              <span>Niveau Suivant</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          ) : (
            <button
              data-start="true"
              onClick={onHome}
              className="w-full sm:w-auto flex-1 py-3 px-5 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-neutral-950 font-bold text-sm tracking-wide shadow-lg flex items-center justify-center gap-2 cursor-pointer transition-transform active:scale-95"
            >
              <span>Couronnement & Accueil</span>
              <Trophy className="w-4 h-4" />
            </button>
          )}

          <button
            onClick={onReplay}
            className="w-full sm:w-auto py-3 px-4 rounded-xl bg-neutral-800 hover:bg-neutral-700 text-neutral-200 font-semibold text-sm flex items-center justify-center gap-1.5 transition-colors"
          >
            <RotateCcw className="w-4 h-4" />
            Rejouer
          </button>

          <button
            onClick={onHome}
            className="w-full sm:w-auto py-3 px-4 rounded-xl bg-neutral-800 hover:bg-neutral-700 text-neutral-200 font-semibold text-sm flex items-center justify-center gap-1.5 transition-colors"
          >
            <Home className="w-4 h-4" />
            Menu
          </button>
        </div>
      </div>
    </div>
  );
};
