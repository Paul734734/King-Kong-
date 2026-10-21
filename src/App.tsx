/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useCallback } from 'react';
import { TitleScreen } from './components/TitleScreen.tsx';
import { GameCanvas } from './game/GameCanvas.tsx';
import { HUD } from './components/HUD.tsx';
import { VictoryModal } from './components/VictoryModal.tsx';
import { GameOverModal } from './components/GameOverModal.tsx';
import { LevelSelectModal } from './components/LevelSelectModal.tsx';
import { MaquetteModal } from './components/MaquetteModal.tsx';
import { RulesModal } from './components/RulesModal.tsx';
import { PauseModal } from './components/PauseModal.tsx';
import { LEVELS, LevelDefinition } from './game/levels.ts';
import { sounds } from './game/sound.ts';
import { calculateLevelScore } from './game/rules.ts';

type ScreenState = 'title' | 'playing' | 'paused' | 'level_clear' | 'game_over';

interface SavedLevelData {
  stars: number;
  highScore: number;
  completed: boolean;
}

export default function App() {
  const [screen, setScreen] = useState<ScreenState>('title');
  const [currentLevelId, setCurrentLevelId] = useState<number>(1);
  const [restartCount, setRestartCount] = useState<number>(0);
  const [bananas, setBananas] = useState<number>(0);
  const [lives, setLives] = useState<number>(3);
  const [maxLives] = useState<number>(5);
  const [elapsedSeconds, setElapsedSeconds] = useState<number>(0);
  const [isMuted, setIsMuted] = useState<boolean>(sounds.getMuted());
  const [virtualInput, setVirtualInput] = useState<{ x: number; y: number } | null>(null);

  // Modals
  const [showLevelSelect, setShowLevelSelect] = useState<boolean>(false);
  const [showMaquette, setShowMaquette] = useState<boolean>(false);
  const [showRules, setShowRules] = useState<boolean>(false);

  // End of run victory/defeat snapshots
  const [victoryData, setVictoryData] = useState<{
    timeSeconds: number;
    livesRemaining: number;
    bonusCollected: number;
    score: number;
    stars: number;
  } | null>(null);

  const [gameOverReason, setGameOverReason] = useState<string>('');

  // Stored progress
  const [levelProgress, setLevelProgress] = useState<Record<number, SavedLevelData>>(() => {
    try {
      const saved = localStorage.getItem('king_kong_labyrinth_progress');
      if (saved) return JSON.parse(saved);
    } catch {
      // fallback
    }
    return {
      1: { stars: 0, highScore: 0, completed: false },
    };
  });

  const currentLevel: LevelDefinition = LEVELS.find((l) => l.id === currentLevelId) || LEVELS[0];

  // Sync dataset.state with screen
  useEffect(() => {
    let stateVal = 'title';
    if (screen === 'playing') stateVal = 'playing';
    else if (screen === 'paused') stateVal = 'paused';
    else if (screen === 'level_clear' || screen === 'game_over') stateVal = 'gameover';
    document.body.dataset.state = stateVal;
  }, [screen]);

  // Support ?autostart=1
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    if (params.get('autostart') === '1') {
      startGame(1);
    }
  }, []);

  // Timer while playing
  useEffect(() => {
    if (screen !== 'playing') return;
    const interval = setInterval(() => {
      setElapsedSeconds((prev) => prev + 1);
    }, 1000);
    return () => clearInterval(interval);
  }, [screen]);

  // Keyboard Shortcuts (Enter/Space in title, P/Esc to pause, R to restart, M for mute)
  useEffect(() => {
    const handleGlobalKeyDown = (e: KeyboardEvent) => {
      // Avoid shortcuts if user is typing in inputs
      if (['INPUT', 'TEXTAREA'].includes((e.target as HTMLElement)?.tagName)) return;

      const k = e.key.toLowerCase();

      if (screen === 'title') {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          startGame(1);
        }
      } else if (screen === 'playing') {
        if (e.key === 'Escape' || k === 'p') {
          e.preventDefault();
          setScreen('paused');
        } else if (k === 'r') {
          e.preventDefault();
          restartLevel();
        } else if (k === 'm') {
          e.preventDefault();
          toggleMute();
        }
      } else if (screen === 'paused') {
        if (e.key === 'Escape' || k === 'p') {
          e.preventDefault();
          setScreen('playing');
        }
      }
    };

    window.addEventListener('keydown', handleGlobalKeyDown);
    return () => window.removeEventListener('keydown', handleGlobalKeyDown);
  }, [screen, isMuted]);

  const startGame = useCallback((levelId: number = 1) => {
    setCurrentLevelId(levelId);
    setRestartCount((c) => c + 1);
    setBananas(0);
    setLives(3);
    setElapsedSeconds(0);
    setVictoryData(null);
    setGameOverReason('');
    setShowLevelSelect(false);
    setShowMaquette(false);
    setShowRules(false);
    setScreen('playing');
  }, []);

  const restartLevel = useCallback(() => {
    startGame(currentLevelId);
  }, [startGame, currentLevelId]);

  const toggleMute = useCallback(() => {
    const newMuted = sounds.toggleMute();
    setIsMuted(newMuted);
  }, []);

  const handleGameOver = useCallback((reason: string) => {
    setGameOverReason(reason);
    setScreen('game_over');
  }, []);

  const handleLevelComplete = useCallback((timeSecs: number, livesLeft: number, bonusCount: number) => {
    const { score, stars } = calculateLevelScore(timeSecs, 5, livesLeft, bonusCount);

    setVictoryData({
      timeSeconds: timeSecs,
      livesRemaining: livesLeft,
      bonusCollected: bonusCount,
      score,
      stars,
    });

    // Update persistent progress
    setLevelProgress((prev) => {
      const existing = prev[currentLevelId] || { stars: 0, highScore: 0, completed: false };
      const updated = {
        ...prev,
        [currentLevelId]: {
          stars: Math.max(existing.stars, stars),
          highScore: Math.max(existing.highScore, score),
          completed: true,
        },
      };
      try {
        localStorage.setItem('king_kong_labyrinth_progress', JSON.stringify(updated));
      } catch {
        // ignore
      }
      return updated;
    });

    setScreen('level_clear');
  }, [currentLevelId]);

  const handleNextLevel = useCallback(() => {
    if (currentLevelId < LEVELS.length) {
      startGame(currentLevelId + 1);
    } else {
      setScreen('title');
    }
  }, [currentLevelId, startGame]);

  return (
    <div className="relative w-screen h-screen overflow-hidden bg-neutral-950 font-sans">
      {/* Title Screen View */}
      {screen === 'title' && (
        <TitleScreen
          onStartGame={startGame}
          onOpenLevelSelect={() => setShowLevelSelect(true)}
          onOpenMaquette={() => setShowMaquette(true)}
          onOpenRules={() => setShowRules(true)}
          isMuted={isMuted}
          onToggleMute={toggleMute}
          levelProgress={levelProgress}
        />
      )}

      {/* Live Game View & HUD */}
      {screen !== 'title' && (
        <main className="relative w-full h-full">
          <GameCanvas
            key={`${currentLevelId}-${restartCount}`}
            level={currentLevel}
            onBananaCollected={setBananas}
            onLivesChanged={setLives}
            onGameOver={handleGameOver}
            onLevelComplete={handleLevelComplete}
            isPaused={screen === 'paused'}
            virtualInput={virtualInput}
          />

          <HUD
            level={currentLevel}
            lives={lives}
            maxLives={maxLives}
            bananas={bananas}
            targetBananas={5}
            elapsedSeconds={elapsedSeconds}
            isPaused={screen === 'paused'}
            isMuted={isMuted}
            onTogglePause={() => setScreen(screen === 'paused' ? 'playing' : 'paused')}
            onToggleMute={toggleMute}
            onRestart={restartLevel}
            onOpenMaquette={() => setShowMaquette(true)}
            onVirtualDirection={setVirtualInput}
          />
        </main>
      )}

      {/* Status & Menu Modals */}
      {screen === 'paused' && (
        <PauseModal
          level={currentLevel}
          bananas={bananas}
          lives={lives}
          elapsedSeconds={elapsedSeconds}
          onResume={() => setScreen('playing')}
          onRestart={restartLevel}
          onHome={() => setScreen('title')}
          onOpenMaquette={() => setShowMaquette(true)}
          isMuted={isMuted}
          onToggleMute={toggleMute}
        />
      )}

      {screen === 'level_clear' && victoryData && (
        <VictoryModal
          level={currentLevel}
          timeSeconds={victoryData.timeSeconds}
          livesRemaining={victoryData.livesRemaining}
          bonusCollected={victoryData.bonusCollected}
          score={victoryData.score}
          stars={victoryData.stars}
          onNextLevel={handleNextLevel}
          onReplay={restartLevel}
          onHome={() => setScreen('title')}
          isFinalLevel={currentLevelId === LEVELS.length}
        />
      )}

      {screen === 'game_over' && (
        <GameOverModal
          level={currentLevel}
          reason={gameOverReason}
          bananasCollected={bananas}
          onRetry={restartLevel}
          onHome={() => setScreen('title')}
          onOpenMaquette={() => setShowMaquette(true)}
        />
      )}

      {/* Global Modals (Level Selection, Maquette GDD, Rules) */}
      <LevelSelectModal
        isOpen={showLevelSelect}
        onClose={() => setShowLevelSelect(false)}
        onSelectLevel={(id) => startGame(id)}
        levelProgress={levelProgress}
      />

      <MaquetteModal
        isOpen={showMaquette}
        onClose={() => setShowMaquette(false)}
      />

      <RulesModal
        isOpen={showRules}
        onClose={() => setShowRules(false)}
      />
    </div>
  );
}
