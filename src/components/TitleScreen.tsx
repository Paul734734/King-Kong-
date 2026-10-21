/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { Play, Map, BookOpen, HelpCircle, Trophy, Volume2, VolumeX } from 'lucide-react';
import { LEVELS } from '../game/levels.ts';

interface TitleScreenProps {
  onStartGame: (levelId?: number) => void;
  onOpenLevelSelect: () => void;
  onOpenMaquette: () => void;
  onOpenRules: () => void;
  isMuted: boolean;
  onToggleMute: () => void;
  levelProgress: Record<number, { stars: number; highScore: number; completed: boolean }>;
}

export const TitleScreen: React.FC<TitleScreenProps> = ({
  onStartGame,
  onOpenLevelSelect,
  onOpenMaquette,
  onOpenRules,
  isMuted,
  onToggleMute,
  levelProgress,
}) => {
  // Compute total stars & score
  const totalStars = Object.values(levelProgress).reduce((acc, curr) => acc + (curr.stars || 0), 0);
  const totalScore = Object.values(levelProgress).reduce((acc, curr) => acc + (curr.highScore || 0), 0);

  return (
    <div className="relative w-full h-full min-h-screen flex flex-col items-center justify-between p-6 overflow-hidden bg-neutral-950 text-neutral-100 arcade-grid select-none">
      {/* Background ambient royal spotlights */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-amber-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-10 left-10 w-[350px] h-[350px] bg-emerald-600/10 rounded-full blur-2xl pointer-events-none" />

      {/* Top Bar: Progress & Sound */}
      <header className="relative z-10 w-full max-w-4xl flex items-center justify-between">
        <div className="flex items-center gap-3 bg-neutral-900/80 border border-neutral-800 rounded-2xl px-4 py-2 backdrop-blur-md shadow-md">
          <div className="flex items-center gap-1.5 text-amber-400 font-bold text-sm">
            <Trophy className="w-4 h-4" />
            <span className="font-cinzel">{totalStars} / 15 ⭐</span>
          </div>
          <div className="w-[1px] h-4 bg-neutral-800" />
          <span className="text-xs text-neutral-400 font-mono">
            Score : <strong className="text-amber-300 font-bold">{totalScore.toLocaleString()}</strong>
          </span>
        </div>

        <button
          onClick={onToggleMute}
          className="p-2.5 rounded-xl bg-neutral-900/80 border border-neutral-800 text-neutral-300 hover:text-amber-400 transition-colors shadow-md"
          title={isMuted ? "Activer le son" : "Couper le son"}
          aria-label="Basculer le son"
        >
          {isMuted ? <VolumeX className="w-5 h-5 text-red-400" /> : <Volume2 className="w-5 h-5 text-emerald-400" />}
        </button>
      </header>

      {/* Hero Centerpiece: King Kong Emblem, Title & CTAs */}
      <main className="relative z-10 flex flex-col items-center max-w-2xl text-center my-auto py-6">
        {/* Royal Crest / King Avatar */}
        <div className="relative mb-6 group cursor-default">
          <div className="w-28 h-28 sm:w-32 sm:h-32 rounded-3xl bg-gradient-to-b from-amber-400/20 via-neutral-900 to-neutral-950 border-2 border-amber-500/60 flex flex-col items-center justify-center shadow-2xl gold-glow transform transition-transform group-hover:scale-105 duration-300">
            {/* Crown */}
            <span className="text-3xl sm:text-4xl -mb-1 animate-pulse">👑</span>
            {/* King Gorilla Face */}
            <span className="text-4xl sm:text-5xl">🦍</span>
            {/* Banana Trophy */}
            <span className="absolute -bottom-2 -right-2 text-2xl rotate-12 filter drop-shadow">🍌</span>
          </div>
        </div>

        {/* Title Lockup */}
        <h1 className="text-3xl sm:text-5xl md:text-6xl font-extrabold font-cinzel text-transparent bg-clip-text bg-gradient-to-r from-amber-200 via-amber-400 to-amber-600 tracking-wider mb-2 drop-shadow-lg">
          KING KONG LABYRINTH
        </h1>
        <p className="text-sm sm:text-base text-amber-200/90 font-medium tracking-wide max-w-lg mb-6">
          La Quête des 5 Bananes Sacrées du Royaume Perdu
        </p>

        {/* Goal Badge */}
        <div className="inline-flex items-center gap-2 bg-neutral-900/90 border border-amber-500/40 rounded-full px-4 py-1.5 mb-8 shadow-inner text-xs sm:text-sm text-neutral-300">
          <span className="text-base">🎯</span>
          <span>Objectif : Récoltez <strong>5 Bananes dorées</strong> sans succomber pour ouvrir la porte !</span>
        </div>

        {/* Menu Buttons Action Stack */}
        <div className="flex flex-col sm:flex-row items-center gap-3.5 w-full max-w-md">
          {/* Main Play CTA */}
          <button
            data-start="true"
            onClick={() => onStartGame(1)}
            className="w-full sm:w-auto flex-1 flex items-center justify-center gap-2.5 py-3.5 px-6 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-neutral-950 font-cinzel font-extrabold text-base tracking-wider shadow-xl gold-glow hover:scale-[1.02] active:scale-[0.98] transition-all cursor-pointer"
          >
            <Play className="w-5 h-5 fill-neutral-950" />
            LANCER LA QUÊTE
          </button>

          {/* Level Select */}
          <button
            onClick={onOpenLevelSelect}
            className="w-full sm:w-auto flex items-center justify-center gap-2 py-3.5 px-5 rounded-xl bg-neutral-900/90 hover:bg-neutral-800 border border-neutral-700 hover:border-amber-500/50 text-neutral-200 font-semibold text-sm transition-all shadow-md cursor-pointer"
          >
            <Map className="w-4 h-4 text-amber-400" />
            Niveaux (1-5)
          </button>
        </div>

        {/* Secondary Actions: Maquette GDD & Rules */}
        <div className="flex items-center justify-center gap-4 mt-6">
          <button
            onClick={onOpenMaquette}
            className="flex items-center gap-1.5 text-xs font-semibold text-amber-400/90 hover:text-amber-300 hover:underline transition-colors py-1"
          >
            <BookOpen className="w-4 h-4" />
            Maquette & Cahier des Charges
          </button>
          <span className="text-neutral-700">·</span>
          <button
            onClick={onOpenRules}
            className="flex items-center gap-1.5 text-xs font-semibold text-neutral-400 hover:text-neutral-200 hover:underline transition-colors py-1"
          >
            <HelpCircle className="w-4 h-4" />
            Règles & Contrôles
          </button>
        </div>
      </main>

      {/* Footer / Control Hint */}
      <footer className="relative z-10 text-center text-xs text-neutral-500">
        <p>ZQSD / Flèches pour diriger le Roi · Touche Espace ou Entrée pour Jouer</p>
      </footer>
    </div>
  );
};
