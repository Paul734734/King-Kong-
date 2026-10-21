/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { X, Lock, Play, Star, Trophy } from 'lucide-react';
import { LEVELS, LevelDefinition } from '../game/levels.ts';

interface LevelSelectModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectLevel: (levelId: number) => void;
  levelProgress: Record<number, { stars: number; highScore: number; completed: boolean }>;
}

export const LevelSelectModal: React.FC<LevelSelectModalProps> = ({
  isOpen,
  onClose,
  onSelectLevel,
  levelProgress,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-in fade-in duration-200">
      <div className="relative w-full max-w-2xl max-h-[90vh] flex flex-col bg-neutral-900 border border-amber-500/40 rounded-3xl shadow-2xl overflow-hidden">
        {/* Header */}
        <header className="flex items-center justify-between px-6 py-4 border-b border-neutral-800 bg-neutral-950/80">
          <div className="flex items-center gap-3">
            <span className="text-2xl">🗺️</span>
            <div>
              <h2 className="text-lg font-bold font-cinzel text-amber-400">
                Sélection des Labyrinthes Royaux
              </h2>
              <p className="text-xs text-neutral-400">
                5 mondes uniques · 5 bananes sacrées à récolter par niveau
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2 rounded-xl text-neutral-400 hover:text-white hover:bg-neutral-800 transition-colors"
            aria-label="Fermer la sélection des niveaux"
          >
            <X className="w-5 h-5" />
          </button>
        </header>

        {/* Levels Grid */}
        <div className="flex-1 overflow-y-auto p-6 space-y-3.5">
          {LEVELS.map((level) => {
            const prog = levelProgress[level.id];
            // Level 1 is always unlocked. Others are unlocked if previous is completed
            const isUnlocked = level.id === 1 || levelProgress[level.id - 1]?.completed;
            const stars = prog?.stars || 0;
            const highScore = prog?.highScore || 0;

            return (
              <div
                key={level.id}
                className={`p-4 rounded-2xl border transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-4 ${
                  isUnlocked
                    ? 'bg-neutral-950/60 border-neutral-800 hover:border-amber-500/50 shadow-md'
                    : 'bg-neutral-950/30 border-neutral-900 opacity-60'
                }`}
              >
                {/* Level Details */}
                <div className="flex items-center gap-4">
                  <div
                    className="w-12 h-12 rounded-xl flex items-center justify-center font-cinzel font-bold text-lg"
                    style={{
                      backgroundColor: `${level.wallColor}30`,
                      border: `1.5px solid ${level.wallColor}`,
                      color: level.accentColor,
                    }}
                  >
                    {isUnlocked ? level.id : <Lock className="w-5 h-5 text-neutral-600" />}
                  </div>

                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="font-bold text-sm text-neutral-100">{level.title}</h3>
                      {prog?.completed && (
                        <span className="text-[10px] bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 px-1.5 py-0.5 rounded font-semibold">
                          Terminé
                        </span>
                      )}
                    </div>
                    <p className="text-xs text-neutral-400 mt-0.5">{level.subtitle}</p>

                    {/* Stats & Stars */}
                    {isUnlocked && (
                      <div className="flex items-center gap-3 mt-1 text-xs">
                        <div className="flex items-center text-amber-400">
                          {[1, 2, 3].map((s) => (
                            <Star
                              key={s}
                              className={`w-3.5 h-3.5 ${
                                s <= stars ? 'fill-amber-400' : 'text-neutral-700'
                              }`}
                            />
                          ))}
                        </div>
                        {highScore > 0 && (
                          <span className="text-neutral-400 font-mono text-[11px]">
                            Record : <strong className="text-amber-300">{highScore.toLocaleString()}</strong> pts
                          </span>
                        )}
                      </div>
                    )}
                  </div>
                </div>

                {/* Launch Button */}
                <div>
                  {isUnlocked ? (
                    <button
                      onClick={() => onSelectLevel(level.id)}
                      className="w-full sm:w-auto px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 active:scale-95 text-neutral-950 font-bold text-xs flex items-center justify-center gap-1.5 transition-all shadow-md cursor-pointer"
                    >
                      <Play className="w-3.5 h-3.5 fill-neutral-950" />
                      <span>Jouer</span>
                    </button>
                  ) : (
                    <span className="text-xs text-neutral-600 flex items-center gap-1 font-medium">
                      <Lock className="w-3.5 h-3.5" />
                      Verrouillé (Complétez le Niveau {level.id - 1})
                    </span>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {/* Footer */}
        <footer className="px-6 py-3 border-t border-neutral-800 bg-neutral-950/80 text-right">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-neutral-800 hover:bg-neutral-700 text-neutral-200 text-xs font-semibold transition-colors"
          >
            Fermer
          </button>
        </footer>
      </div>
    </div>
  );
};
