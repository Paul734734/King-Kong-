/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { X, Crown, Shield, Heart, Zap, Skull, Flame, Sparkles, Compass, CheckCircle2, Award, Info } from 'lucide-react';
import { LEVELS } from '../game/levels.ts';

interface MaquetteModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const MaquetteModal: React.FC<MaquetteModalProps> = ({ isOpen, onClose }) => {
  const [activeTab, setActiveTab] = useState<'concept' | 'gameplay' | 'personnage' | 'ennemis' | 'niveaux' | 'economie'>('concept');

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-black/80 backdrop-blur-md animate-in fade-in duration-200">
      <div className="relative w-full max-w-4xl max-h-[92vh] flex flex-col bg-neutral-900 border border-amber-500/40 rounded-2xl shadow-2xl overflow-hidden">
        {/* Header */}
        <header className="flex items-center justify-between px-6 py-4 border-b border-neutral-800 bg-neutral-950/80">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-amber-500/20 border border-amber-400/40 flex items-center justify-center text-xl">
              👑
            </div>
            <div>
              <h2 className="text-lg sm:text-xl font-bold font-cinzel text-amber-400 flex items-center gap-2">
                Maquette & Spécifications Complètes
              </h2>
              <p className="text-xs text-neutral-400">
                Game Design Document (GDD) & Architecture du jeu du Roi dans le Labyrinthe
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2 rounded-xl text-neutral-400 hover:text-white hover:bg-neutral-800 transition-colors"
            aria-label="Fermer la documentation"
          >
            <X className="w-5 h-5" />
          </button>
        </header>

        {/* Navigation Tabs */}
        <nav className="flex items-center gap-1 overflow-x-auto px-6 py-2.5 bg-neutral-950/40 border-b border-neutral-800 text-xs font-semibold scrollbar-none">
          <button
            onClick={() => setActiveTab('concept')}
            className={`px-3.5 py-1.5 rounded-lg whitespace-nowrap transition-all ${
              activeTab === 'concept'
                ? 'bg-amber-500 text-neutral-950 font-bold shadow-md'
                : 'text-neutral-400 hover:text-neutral-200 hover:bg-neutral-800/60'
            }`}
          >
            🌟 Concept & Lore
          </button>
          <button
            onClick={() => setActiveTab('gameplay')}
            className={`px-3.5 py-1.5 rounded-lg whitespace-nowrap transition-all ${
              activeTab === 'gameplay'
                ? 'bg-amber-500 text-neutral-950 font-bold shadow-md'
                : 'text-neutral-400 hover:text-neutral-200 hover:bg-neutral-800/60'
            }`}
          >
            🕹️ Boucle de Gameplay (5 🍌)
          </button>
          <button
            onClick={() => setActiveTab('personnage')}
            className={`px-3.5 py-1.5 rounded-lg whitespace-nowrap transition-all ${
              activeTab === 'personnage'
                ? 'bg-amber-500 text-neutral-950 font-bold shadow-md'
                : 'text-neutral-400 hover:text-neutral-200 hover:bg-neutral-800/60'
            }`}
          >
            🦍 King (Le Roi)
          </button>
          <button
            onClick={() => setActiveTab('ennemis')}
            className={`px-3.5 py-1.5 rounded-lg whitespace-nowrap transition-all ${
              activeTab === 'ennemis'
                ? 'bg-amber-500 text-neutral-950 font-bold shadow-md'
                : 'text-neutral-400 hover:text-neutral-200 hover:bg-neutral-800/60'
            }`}
          >
            ⚔️ Ennemis & Pièges
          </button>
          <button
            onClick={() => setActiveTab('niveaux')}
            className={`px-3.5 py-1.5 rounded-lg whitespace-nowrap transition-all ${
              activeTab === 'niveaux'
                ? 'bg-amber-500 text-neutral-950 font-bold shadow-md'
                : 'text-neutral-400 hover:text-neutral-200 hover:bg-neutral-800/60'
            }`}
          >
            🗺️ 5 Labyrinthes
          </button>
          <button
            onClick={() => setActiveTab('economie')}
            className={`px-3.5 py-1.5 rounded-lg whitespace-nowrap transition-all ${
              activeTab === 'economie'
                ? 'bg-amber-500 text-neutral-950 font-bold shadow-md'
                : 'text-neutral-400 hover:text-neutral-200 hover:bg-neutral-800/60'
            }`}
          >
            ❤️ Vies & Économie
          </button>
        </nav>

        {/* Content Body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6 text-neutral-200 text-sm leading-relaxed">
          {/* TAB 1: Concept & Lore */}
          {activeTab === 'concept' && (
            <div className="space-y-6 animate-in fade-in">
              <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 flex gap-4 items-start">
                <span className="text-3xl">👑</span>
                <div>
                  <h3 className="text-base font-bold text-amber-400 mb-1 font-cinzel">
                    Le Pitch Royal : La Renaissance du Roi Kong
                  </h3>
                  <p className="text-neutral-300 text-sm">
                    Autrefois souverain vénéré de la Cité des Canopées, le légendaire Roi Kong a vu son royaume scellé par une malédiction ancestrale. Pour briser le maléfice et reprendre sa place sur le Trône Doré, King doit s'aventurer dans une succession de 5 labyrinthes séculaires truffés de périls mortels et ramener les <strong>5 Bananes Sacrées</strong> de chaque dynastie.
                  </p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-4 rounded-xl bg-neutral-950/60 border border-neutral-800">
                  <div className="text-amber-400 font-bold text-sm mb-2 flex items-center gap-2">
                    <Compass className="w-4 h-4" />
                    Labyrinthes Méticuleux
                  </div>
                  <p className="text-xs text-neutral-400">
                    Des architectures labyrinthiques variées avec carrefours stratégiques, chemins à risques et alcoves secrètes dissimulant des bonus de survie.
                  </p>
                </div>

                <div className="p-4 rounded-xl bg-neutral-950/60 border border-neutral-800">
                  <div className="text-amber-400 font-bold text-sm mb-2 flex items-center gap-2">
                    <Sparkles className="w-4 h-4" />
                    Objectif Précis (5 🍌)
                  </div>
                  <p className="text-xs text-neutral-400">
                    Rassemblez exactement 5 bananes dorées par niveau. Aucune sortie n'est possible sans ce tribut complet, forçant le joueur à explorer l'intégralité du dédale !
                  </p>
                </div>

                <div className="p-4 rounded-xl bg-neutral-950/60 border border-neutral-800">
                  <div className="text-amber-400 font-bold text-sm mb-2 flex items-center gap-2">
                    <Award className="w-4 h-4" />
                    Récompenses & Félicitations
                  </div>
                  <p className="text-xs text-neutral-400">
                    Notation par étoiles (1 à 3 étoiles royales), calcul de score par chrono et vies restantes, et célébration festive de confettis dorés au sanctuaire.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: Gameplay Loop */}
          {activeTab === 'gameplay' && (
            <div className="space-y-6 animate-in fade-in">
              <h3 className="text-base font-bold text-amber-400 font-cinzel">
                La Boucle de Gameplay Principale (Core Loop)
              </h3>

              <div className="relative pl-6 space-y-6 before:absolute before:left-2 before:top-2 before:bottom-2 before:w-0.5 before:bg-amber-500/40">
                <div className="relative">
                  <div className="absolute -left-[21px] top-1 w-3 h-3 rounded-full bg-amber-500 ring-4 ring-neutral-900" />
                  <h4 className="font-bold text-amber-300 text-sm">Étape 1 : Infiltration & Découverte du Labyrinthe</h4>
                  <p className="text-xs text-neutral-400 mt-1">
                    King apparaît au point d'entrée sécurisé. Le joueur observe la disposition des couloirs, repère les lueurs des bananes dorées et planifie son itinéraire en évitant les pièges visibles.
                  </p>
                </div>

                <div className="relative">
                  <div className="absolute -left-[21px] top-1 w-3 h-3 rounded-full bg-amber-500 ring-4 ring-neutral-900" />
                  <h4 className="font-bold text-amber-300 text-sm">Étape 2 : Évitement Actif des Dangers</h4>
                  <p className="text-xs text-neutral-400 mt-1">
                    Synchronisation avec les cycles des pics au sol (télégraphiés 0.5s avant sortie) et anticipation des trajectoires de patrouille des serpents et chauves-souris.
                  </p>
                </div>

                <div className="relative">
                  <div className="absolute -left-[21px] top-1 w-3 h-3 rounded-full bg-amber-500 ring-4 ring-neutral-900" />
                  <h4 className="font-bold text-amber-300 text-sm">Étape 3 : Moisson des 5 Bananes Sacrées</h4>
                  <p className="text-xs text-neutral-400 mt-1">
                    Chaque banane déclenche un arpège sonore triomphal et incrémente le compteur HUD (1/5 ... 5/5). Dès la 5ème banane obtenue, un signal doré prévient le joueur que l'Arche Royale est descellée.
                  </p>
                </div>

                <div className="relative">
                  <div className="absolute -left-[21px] top-1 w-3 h-3 rounded-full bg-amber-500 ring-4 ring-neutral-900" />
                  <h4 className="font-bold text-amber-300 text-sm">Étape 4 : Exfiltration vers l'Arche du Sanctuaire</h4>
                  <p className="text-xs text-neutral-400 mt-1">
                    Le joueur doit retourner vivant vers la sortie illuminée. Franchir le portail déclenche le décompte de score, l'écran de félicitations et déverrouille le monde suivant.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* TAB 3: King Character */}
          {activeTab === 'personnage' && (
            <div className="space-y-6 animate-in fade-in">
              <div className="flex flex-col sm:flex-row items-center gap-6 p-4 rounded-xl bg-neutral-950/60 border border-neutral-800">
                <div className="w-24 h-24 rounded-2xl bg-amber-500/10 border-2 border-amber-400/60 flex flex-col items-center justify-center text-4xl shadow-inner">
                  👑
                  <span className="text-3xl -mt-2">🦍</span>
                </div>
                <div className="space-y-1">
                  <h3 className="text-lg font-bold text-amber-400 font-cinzel">King Kong (Sa Majesté le Roi)</h3>
                  <p className="text-xs text-neutral-300">
                    Grand singe royal au dos argenté, coiffé de la Couronne d'Or à rubis impériaux et drapé de sa cape pourpre carmin.
                  </p>
                  <div className="flex flex-wrap gap-2 pt-2">
                    <span className="px-2.5 py-1 rounded bg-neutral-800 text-[11px] font-mono text-amber-300">
                      Vitesse : 3.0 cases/s (4.5 en boost)
                    </span>
                    <span className="px-2.5 py-1 rounded bg-neutral-800 text-[11px] font-mono text-red-400">
                      Vies : 3 cœurs (extensible à 5)
                    </span>
                    <span className="px-2.5 py-1 rounded bg-neutral-800 text-[11px] font-mono text-blue-400">
                      Bouclier : Absorption de choc
                    </span>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="p-4 rounded-xl bg-neutral-950/40 border border-neutral-800">
                  <h4 className="font-bold text-amber-300 text-sm mb-2 flex items-center gap-2">
                    <Shield className="w-4 h-4 text-blue-400" />
                    Mécanique de Bouclier d'Ananas
                  </h4>
                  <p className="text-xs text-neutral-400">
                    Lorsqu'il ramasse un bouclier, une bulle d'énergie céleste protège le Roi. Le prochain impact subi (piège ou monstre) est totalement annulé et le bouclier se dissipe sans retirer de cœur.
                  </p>
                </div>

                <div className="p-4 rounded-xl bg-neutral-950/40 border border-neutral-800">
                  <h4 className="font-bold text-amber-300 text-sm mb-2 flex items-center gap-2">
                    <Heart className="w-4 h-4 text-red-400" />
                    Période d'Invulnérabilité (Grace Frames)
                  </h4>
                  <p className="text-xs text-neutral-400">
                    Après chaque coup reçu, King clignote pendant 1,8 seconde durant laquelle aucun nouveau dégât ne peut être infligé, permettant de fuir un piège actif ou un groupe d'ennemis.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* TAB 4: Enemies & Traps */}
          {activeTab === 'ennemis' && (
            <div className="space-y-6 animate-in fade-in">
              <h3 className="text-base font-bold text-amber-400 font-cinzel">Bestiaire des Ennemis & Pièges</h3>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="p-3.5 rounded-xl bg-neutral-950/60 border border-neutral-800 flex gap-3">
                  <span className="text-2xl">🐍</span>
                  <div>
                    <h4 className="font-bold text-emerald-400 text-sm">Vipères & Serpents à Sonnette</h4>
                    <p className="text-xs text-neutral-400 mt-1">
                      Patrouillent les corridors en ligne droite. Mouvement fluide, inflige 1 dégât au contact.
                    </p>
                  </div>
                </div>

                <div className="p-3.5 rounded-xl bg-neutral-950/60 border border-neutral-800 flex gap-3">
                  <span className="text-2xl">🦇</span>
                  <div>
                    <h4 className="font-bold text-purple-400 text-sm">Chauves-souris Prédatrices</h4>
                    <p className="text-xs text-neutral-400 mt-1">
                      Vol rapide et saccadé le long d'axes verticaux ou horizontaux. Vitesse élevée nécessitant un timing précis.
                    </p>
                  </div>
                </div>

                <div className="p-3.5 rounded-xl bg-neutral-950/60 border border-neutral-800 flex gap-3">
                  <span className="text-2xl">💀</span>
                  <div>
                    <h4 className="font-bold text-amber-300 text-sm">Gardes Squelettes Royaux</h4>
                    <p className="text-xs text-neutral-400 mt-1">
                      Anciennes sentinelles impériales en armure qui montent la garde devant les intersections majeures.
                    </p>
                  </div>
                </div>

                <div className="p-3.5 rounded-xl bg-neutral-950/60 border border-neutral-800 flex gap-3">
                  <span className="text-2xl">🌱</span>
                  <div>
                    <h4 className="font-bold text-lime-400 text-sm">Plantes Carnivores Voraces</h4>
                    <p className="text-xs text-neutral-400 mt-1">
                      Obstacles vivants stationnaires dont les mâchoires claquent pour verrouiller les couloirs étroits.
                    </p>
                  </div>
                </div>

                <div className="p-3.5 rounded-xl bg-neutral-950/60 border border-neutral-800 flex gap-3">
                  <span className="text-2xl">⚡</span>
                  <div>
                    <h4 className="font-bold text-amber-400 text-sm">Dalles de Pics Rétractables</h4>
                    <p className="text-xs text-neutral-400 mt-1">
                      Pièges cycliques. Un voyant d'armement jaune/rouge s'allume 0,5s avant l'éjection foudroyante des pointes en acier.
                    </p>
                  </div>
                </div>

                <div className="p-3.5 rounded-xl bg-neutral-950/60 border border-neutral-800 flex gap-3">
                  <span className="text-2xl">🔥</span>
                  <div>
                    <h4 className="font-bold text-red-400 text-sm">Geysers de Feu & Magma</h4>
                    <p className="text-xs text-neutral-400 mt-1">
                      Fissures au sol crachant des colonnes de feu incandescentes. L'aura orange annonce l'embrasement imminent.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* TAB 5: Levels */}
          {activeTab === 'niveaux' && (
            <div className="space-y-4 animate-in fade-in">
              <h3 className="text-base font-bold text-amber-400 font-cinzel">
                Architecture des 5 Niveaux Conçus
              </h3>

              <div className="space-y-3">
                {LEVELS.map((lvl) => (
                  <div key={lvl.id} className="p-4 rounded-xl bg-neutral-950/60 border border-neutral-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div className="flex items-center gap-3">
                      <div
                        className="w-10 h-10 rounded-xl flex items-center justify-center font-bold text-sm"
                        style={{ backgroundColor: `${lvl.wallColor}40`, border: `1px solid ${lvl.wallColor}`, color: lvl.accentColor }}
                      >
                        N{lvl.id}
                      </div>
                      <div>
                        <h4 className="font-bold text-neutral-100 text-sm">{lvl.title}</h4>
                        <p className="text-xs text-neutral-400">{lvl.subtitle}</p>
                      </div>
                    </div>

                    <div className="flex items-center gap-3 text-xs text-neutral-400">
                      <span className="px-2 py-1 bg-neutral-800/80 rounded border border-neutral-700">
                        {lvl.width}x{lvl.height} cases
                      </span>
                      <span className="px-2 py-1 bg-neutral-800/80 rounded border border-neutral-700 text-amber-300">
                        5 Bananes
                      </span>
                      <span className="px-2 py-1 bg-neutral-800/80 rounded border border-neutral-700 text-red-400">
                        {lvl.traps.length} Pièges
                      </span>
                      <span className="px-2 py-1 bg-neutral-800/80 rounded border border-neutral-700 text-purple-400">
                        {lvl.enemies.length} Monstres
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 6: Economy & Scoring */}
          {activeTab === 'economie' && (
            <div className="space-y-6 animate-in fade-in">
              <h3 className="text-base font-bold text-amber-400 font-cinzel">
                Système de Vies, Score & Récompenses Royales
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 rounded-xl bg-neutral-950/60 border border-neutral-800">
                  <h4 className="font-bold text-amber-300 text-sm mb-2">Formule de Calcul du Score</h4>
                  <ul className="text-xs text-neutral-300 space-y-1.5 list-disc list-inside">
                    <li><strong>5 Bananes :</strong> +5 000 pts (1 000 pts / banane)</li>
                    <li><strong>Bonus Temps :</strong> Jusqu'à +3 000 pts (dégressif selon les secondes)</li>
                    <li><strong>Cœurs Préservés :</strong> +800 pts par cœur intact</li>
                    <li><strong>Objets Secrets :</strong> +500 pts par cœur ou bouclier récolté</li>
                  </ul>
                </div>

                <div className="p-4 rounded-xl bg-neutral-950/60 border border-neutral-800">
                  <h4 className="font-bold text-amber-300 text-sm mb-2">Attribution des Étoiles Royales</h4>
                  <div className="space-y-2 text-xs">
                    <div className="flex items-center gap-2">
                      <span className="text-amber-400 font-bold">⭐⭐⭐ 3 Étoiles :</span>
                      <span className="text-neutral-400">3 cœurs restants + temps &lt; 60 secondes</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-amber-400 font-bold">⭐⭐ 2 Étoiles :</span>
                      <span className="text-neutral-400">Au moins 2 cœurs restants + temps &lt; 120 secondes</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-amber-400 font-bold">⭐ 1 Étoile :</span>
                      <span className="text-neutral-400">Niveau complété avec 5 bananes</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <footer className="px-6 py-3.5 border-t border-neutral-800 bg-neutral-950/80 flex justify-between items-center">
          <div className="text-xs text-neutral-400 flex items-center gap-1.5">
            <Info className="w-4 h-4 text-amber-400" />
            <span>Toutes les fonctionnalités décrites sont actives et jouables en temps réel dans l'application.</span>
          </div>
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-neutral-950 font-bold text-xs transition-colors shadow-lg"
          >
            Fermer la Documentation
          </button>
        </footer>
      </div>
    </div>
  );
};
