/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { X, Target, Heart, Shield, Sparkles, Navigation } from 'lucide-react';

interface RulesModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const RulesModal: React.FC<RulesModalProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-in fade-in duration-200">
      <div className="relative w-full max-w-xl bg-neutral-900 border border-amber-500/40 rounded-3xl shadow-2xl p-6 sm:p-7 overflow-hidden text-neutral-200">
        <header className="flex items-center justify-between pb-4 border-b border-neutral-800 mb-5">
          <div className="flex items-center gap-3">
            <span className="text-2xl">📜</span>
            <h2 className="text-lg font-bold font-cinzel text-amber-400">
              Règles du Jeu & Guide de Survie
            </h2>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-neutral-400 hover:text-white hover:bg-neutral-800 transition-colors"
            aria-label="Fermer les règles"
          >
            <X className="w-5 h-5" />
          </button>
        </header>

        <div className="space-y-4 text-xs sm:text-sm">
          <div className="p-3.5 rounded-xl bg-neutral-950/70 border border-neutral-800 flex items-start gap-3">
            <div className="p-2 rounded-lg bg-amber-500/10 text-amber-400 text-lg">
              🍌
            </div>
            <div>
              <h3 className="font-bold text-amber-300">Objectif Clé : 5 Bananes par Niveau</h3>
              <p className="text-neutral-400 text-xs mt-0.5">
                Chaque niveau contient exactement 5 bananes sacrées. L'Arche Royale reste scellée tant que les 5 bananes ne sont pas en votre possession.
              </p>
            </div>
          </div>

          <div className="p-3.5 rounded-xl bg-neutral-950/70 border border-neutral-800 flex items-start gap-3">
            <div className="p-2 rounded-lg bg-red-500/10 text-red-400 text-lg">
              ❤️
            </div>
            <div>
              <h3 className="font-bold text-red-300">Système de Vies (3 Cœurs Royaux)</h3>
              <p className="text-neutral-400 text-xs mt-0.5">
                Vous commencez avec 3 cœurs. Toucher un piège actif ou un ennemi vous fait perdre 1 vie avec un temps d'invulnérabilité de 1,8s. Trouvez des cœurs bonus pour vous régénérer jusqu'à 5 vies !
              </p>
            </div>
          </div>

          <div className="p-3.5 rounded-xl bg-neutral-950/70 border border-neutral-800 flex items-start gap-3">
            <div className="p-2 rounded-lg bg-blue-500/10 text-blue-400 text-lg">
              🛡️
            </div>
            <div>
              <h3 className="font-bold text-blue-300">Bouclier & Vitesse</h3>
              <p className="text-neutral-400 text-xs mt-0.5">
                Le Bouclier d'Ananas absorbe entièrement le prochain coup sans perte de cœur. Les éclairs dorés vous accordent un boost de vitesse temporaire.
              </p>
            </div>
          </div>

          <div className="p-3.5 rounded-xl bg-neutral-950/70 border border-neutral-800 flex items-start gap-3">
            <div className="p-2 rounded-lg bg-purple-500/10 text-purple-400 text-lg">
              ⌨️
            </div>
            <div>
              <h3 className="font-bold text-purple-300">Contrôles</h3>
              <p className="text-neutral-400 text-xs mt-0.5">
                <strong>Clavier :</strong> Touches ZQSD ou Flèches directionnelles.<br />
                <strong>Mobile / Écran tactile :</strong> D-Pad virtuel en bas à droite de l'écran.
              </p>
            </div>
          </div>
        </div>

        <footer className="mt-6 pt-4 border-t border-neutral-800 flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-neutral-950 font-bold text-xs transition-colors shadow-md"
          >
            Compris, Majesté !
          </button>
        </footer>
      </div>
    </div>
  );
};
