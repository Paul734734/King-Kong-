# King Kong Labyrinth — La Quête Royale

King Kong Labyrinth est un jeu d'aventure et de labyrinthe développé en Python avec Pygame. Le joueur explore différents environnements, collecte des bananes, évite les pièges et les ennemis, puis tente de rejoindre la sortie.

## Présentation

Aux portes d'un royaume mystérieux, King doit récupérer les bananes primordiales dispersées dans des labyrinthes dangereux. Chaque niveau propose son propre environnement, ses obstacles et ses défis.

Le joueur doit faire preuve d'observation, de stratégie et de précision pour survivre et progresser dans l'aventure.

## Fonctionnalités

- Plusieurs niveaux avec des labyrinthes et des environnements distincts.
- Collecte de bananes pour atteindre les objectifs des niveaux.
- Ennemis avec différents comportements.
- Pièges et obstacles à éviter.
- Objets à récupérer, notamment des cœurs et des boucliers.
- Gestion des vies et de l'invulnérabilité temporaire.
- Calcul des scores et attribution d'étoiles selon les performances.
- Menus, sélection des niveaux, pause, victoire et fin de partie.
- Gestion de la musique et du son.
- Système de sauvegarde de la progression.
- Interface graphique redimensionnable.

## Technologies

- Python
- Pygame
- Git
- GitHub

## Prérequis

- Python 3.10 ou une version compatible avec le projet.
- pip.
- Git pour cloner le dépôt.

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/Paul734734/King-Kong-.git
cd King-Kong-
```

### 2. Créer un environnement virtuel

Sous Linux :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dépendances

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Lancement du jeu

Depuis la racine du projet, exécuter :

```bash
python main.py
```

La fenêtre du jeu devrait s'ouvrir.

## Structure du projet

```text
King-Kong-/
├── assets/
│   └── music/
│       └── mondamusic-ethnic-tribal-jungle-music-597218.mp3
├── src/
│   ├── components/
│   │   ├── game_over_modal.py
│   │   ├── hud.py
│   │   ├── level_select_modal.py
│   │   ├── maquette_modal.py
│   │   ├── pause_modal.py
│   │   ├── rules_modal.py
│   │   ├── title_screen.py
│   │   └── victory_modal.py
│   ├── game/
│   │   ├── game_canvas.py
│   │   ├── levels.py
│   │   ├── rules.py
│   │   ├── sound.py
│   │   ├── sprites.py
│   │   ├── storage.py
│   │   └── test_rules.py
│   ├── app.py
│   ├── main.py
│   └── ui.py
├── main.py
├── requirements.txt
└── README.md
```

## Rôle des principaux fichiers

- `main.py` : point d'entrée du programme.
- `src/main.py` : démarrage de l'application.
- `src/app.py` : gestion de l'application, des écrans et du déroulement du jeu.
- `src/game/levels.py` : définition des niveaux, labyrinthes, ennemis, pièges et objets.
- `src/game/game_canvas.py` : affichage et déroulement du jeu.
- `src/game/rules.py` : règles de déplacement, collisions, dégâts, objectifs et scores.
- `src/game/sound.py` : gestion du son et de la musique.
- `src/game/storage.py` : gestion des sauvegardes.
- `src/game/sprites.py` : éléments graphiques du jeu.
- `src/components/` : composants de l'interface et fenêtres du jeu.
- `assets/music/` : ressources musicales.

## Tests

Le projet contient des tests pour certaines règles du jeu.

Pour installer pytest :

```bash
python -m pip install pytest
```

Pour exécuter les tests :

```bash
python -m pytest src/game/test_rules.py
```

## Objectif du jeu

Explore les labyrinthes, récupère les bananes requises, évite les dangers et rejoins la sortie pour terminer les niveaux.

Préserve tes vies et améliore ton score pour obtenir le meilleur résultat possible.

## Dépôt GitHub

https://github.com/Paul734734/King-Kong-

## Licence

Aucune licence n'est spécifiée pour le moment. Tous droits relatifs au code et aux ressources restent réservés à leurs ayants droit, sauf indication contraire.
