/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

export interface LevelTrap {
  id: string;
  type: 'spikes' | 'fire';
  x: number;
  y: number;
  interval: number; // in seconds
  offset: number; // initial offset
}

export interface LevelEnemy {
  id: string;
  type: 'snake' | 'bat' | 'guard' | 'carnivorous_plant';
  name: string;
  x: number;
  y: number;
  speed: number;
  patrolAxis: 'x' | 'y' | 'follow' | 'circle';
  patrolRange: number;
}

export interface LevelPickup {
  id: string;
  type: 'banana' | 'heart' | 'shield' | 'speed';
  x: number;
  y: number;
}

export interface LevelDefinition {
  id: number;
  title: string;
  subtitle: string;
  lore: string;
  theme: 'jungle' | 'dungeon' | 'temple' | 'magma' | 'throne';
  wallColor: string;
  floorColor: string;
  accentColor: string;
  width: number;
  height: number;
  grid: string[];
  playerSpawn: { x: number; y: number };
  sanctuaryExit: { x: number; y: number };
  pickups: LevelPickup[];
  traps: LevelTrap[];
  enemies: LevelEnemy[];
}

export const LEVELS: LevelDefinition[] = [
  {
    id: 1,
    title: "Niveau 1 : Les Jardins Royaux",
    subtitle: "L'éveil du Roi Kong dans la canopée sacrée",
    lore: "Aux portes de son royaume perdu, King doit récupérer les 5 bananes primordiales éparpillées parmi la végétation pour ouvrir la porte de l'enceinte de pierre.",
    theme: 'jungle',
    wallColor: '#166534',
    floorColor: '#052e16',
    accentColor: '#4ade80',
    width: 15,
    height: 13,
    grid: [
      "###############",
      "#...#.....#...#",
      "#.###.###.#.#.#",
      "#...#...#...#.#",
      "###.###.#####.#",
      "#.....#.#.....#",
      "#.###.#.#.###.#",
      "#...#.....#...#",
      "###.#######.###",
      "#...#.....#...#",
      "#.###.###.###.#",
      "#.....#.#.....#",
      "###############"
    ],
    playerSpawn: { x: 1.5, y: 1.5 },
    sanctuaryExit: { x: 13.5, y: 11.5 },
    pickups: [
      { id: 'b1_1', type: 'banana', x: 7.5, y: 1.5 },
      { id: 'b1_2', type: 'banana', x: 13.5, y: 3.5 },
      { id: 'b1_3', type: 'banana', x: 1.5, y: 7.5 },
      { id: 'b1_4', type: 'banana', x: 7.5, y: 7.5 },
      { id: 'b1_5', type: 'banana', x: 1.5, y: 11.5 },
      // Bonus items
      { id: 'h1_1', type: 'heart', x: 13.5, y: 1.5 },
      { id: 's1_1', type: 'shield', x: 7.5, y: 11.5 },
    ],
    traps: [
      { id: 't1_1', type: 'spikes', x: 4, y: 1, interval: 3.0, offset: 0 },
      { id: 't1_2', type: 'spikes', x: 10, y: 1, interval: 3.0, offset: 1.5 },
      { id: 't1_3', type: 'spikes', x: 7, y: 5, interval: 2.5, offset: 0.8 },
      { id: 't1_4', type: 'spikes', x: 3, y: 11, interval: 3.2, offset: 1.0 },
    ],
    enemies: [
      { id: 'e1_1', type: 'snake', name: 'Vipère Émeraude', x: 3.5, y: 5.5, speed: 1.2, patrolAxis: 'x', patrolRange: 2.0 },
      { id: 'e1_2', type: 'snake', name: 'Cobra Royal', x: 11.5, y: 7.5, speed: 1.4, patrolAxis: 'x', patrolRange: 2.0 },
      { id: 'e1_3', type: 'carnivorous_plant', name: 'Plante Vorace', x: 7.5, y: 9.5, speed: 0, patrolAxis: 'circle', patrolRange: 0 },
    ]
  },
  {
    id: 2,
    title: "Niveau 2 : Les Catacombes Sombre-Royales",
    subtitle: "Les couloirs hantés par les chauves-souris ancestrales",
    lore: "Une brume bleutée et des torches tremblantes jalonnent les galeries sous le palais royal. Les chauves-souris en maraude attaquent dès qu'on s'aventure dans leurs nids.",
    theme: 'dungeon',
    wallColor: '#334155',
    floorColor: '#0f172a',
    accentColor: '#38bdf8',
    width: 17,
    height: 13,
    grid: [
      "#################",
      "#...#...#...#...#",
      "#.###.#.#.#.###.#",
      "#...#.#...#.#...#",
      "###.#.#####.#.###",
      "#...#...#...#...#",
      "#.#####.#.#####.#",
      "#...#...#...#...#",
      "###.#.#####.#.###",
      "#...#.#...#.#...#",
      "#.###.#.#.#.###.#",
      "#...#...#...#...#",
      "#################"
    ],
    playerSpawn: { x: 1.5, y: 1.5 },
    sanctuaryExit: { x: 15.5, y: 11.5 },
    pickups: [
      { id: 'b2_1', type: 'banana', x: 8.5, y: 1.5 },
      { id: 'b2_2', type: 'banana', x: 15.5, y: 1.5 },
      { id: 'b2_3', type: 'banana', x: 1.5, y: 11.5 },
      { id: 'b2_4', type: 'banana', x: 8.5, y: 7.5 },
      { id: 'b2_5', type: 'banana', x: 15.5, y: 5.5 },
      // Bonus
      { id: 'p2_1', type: 'speed', x: 8.5, y: 5.5 },
      { id: 'h2_1', type: 'heart', x: 1.5, y: 5.5 },
    ],
    traps: [
      { id: 't2_1', type: 'fire', x: 5, y: 1, interval: 2.5, offset: 0 },
      { id: 't2_2', type: 'fire', x: 11, y: 1, interval: 2.5, offset: 1.2 },
      { id: 't2_3', type: 'spikes', x: 3, y: 7, interval: 2.0, offset: 0.5 },
      { id: 't2_4', type: 'spikes', x: 13, y: 7, interval: 2.0, offset: 1.5 },
      { id: 't2_5', type: 'fire', x: 8, y: 11, interval: 2.8, offset: 0.8 },
    ],
    enemies: [
      { id: 'e2_1', type: 'bat', name: 'Chauve-souris Furtive', x: 4.5, y: 3.5, speed: 2.0, patrolAxis: 'y', patrolRange: 2.0 },
      { id: 'e2_2', type: 'bat', name: 'Vampire des Cryptes', x: 12.5, y: 9.5, speed: 2.2, patrolAxis: 'y', patrolRange: 2.0 },
      { id: 'e2_3', type: 'snake', name: 'Crotale d\'Obsidienne', x: 8.5, y: 9.5, speed: 1.3, patrolAxis: 'x', patrolRange: 2.0 },
    ]
  },
  {
    id: 3,
    title: "Niveau 3 : Le Temple Solaire Oublié",
    subtitle: "Dalles dorées et la garde d'honneur squelette",
    lore: "Autrefois cœur spirituel de la dynastie simiesque, ce sanctuaire est gardé par les sentinelles squelettiques royales qui n'ont jamais abandonné leur poste séculaire.",
    theme: 'temple',
    wallColor: '#854d0e',
    floorColor: '#451a03',
    accentColor: '#facc15',
    width: 17,
    height: 15,
    grid: [
      "#################",
      "#...#.....#.....#",
      "#.###.###.###.###",
      "#.#...#.#...#...#",
      "#.#.###.#.###.#.#",
      "#...#...#.....#.#",
      "#####.#######.#.#",
      "#.....#...#...#.#",
      "#.###.#.#.#.###.#",
      "#.#...#.#.#...#.#",
      "#.#.###.#.###.#.#",
      "#...#...#...#...#",
      "###.#.#####.#.###",
      "#...#.......#...#",
      "#################"
    ],
    playerSpawn: { x: 1.5, y: 1.5 },
    sanctuaryExit: { x: 8.5, y: 7.5 },
    pickups: [
      { id: 'b3_1', type: 'banana', x: 15.5, y: 1.5 },
      { id: 'b3_2', type: 'banana', x: 1.5, y: 13.5 },
      { id: 'b3_3', type: 'banana', x: 15.5, y: 13.5 },
      { id: 'b3_4', type: 'banana', x: 8.5, y: 1.5 },
      { id: 'b3_5', type: 'banana', x: 8.5, y: 13.5 },
      // Bonus
      { id: 's3_1', type: 'shield', x: 1.5, y: 7.5 },
      { id: 'h3_1', type: 'heart', x: 15.5, y: 7.5 },
    ],
    traps: [
      { id: 't3_1', type: 'spikes', x: 4, y: 3, interval: 2.2, offset: 0 },
      { id: 't3_2', type: 'spikes', x: 12, y: 3, interval: 2.2, offset: 1.1 },
      { id: 't3_3', type: 'fire', x: 8, y: 5, interval: 2.6, offset: 0.4 },
      { id: 't3_4', type: 'spikes', x: 4, y: 11, interval: 2.0, offset: 1.0 },
      { id: 't3_5', type: 'fire', x: 12, y: 11, interval: 2.5, offset: 1.5 },
    ],
    enemies: [
      { id: 'e3_1', type: 'guard', name: 'Garde Squelette Royal', x: 4.5, y: 7.5, speed: 1.3, patrolAxis: 'x', patrolRange: 2.5 },
      { id: 'e3_2', type: 'guard', name: 'Sentinelle Dorée', x: 12.5, y: 7.5, speed: 1.3, patrolAxis: 'x', patrolRange: 2.5 },
      { id: 'e3_3', type: 'bat', name: 'Chauve-souris des Tombeaux', x: 8.5, y: 3.5, speed: 2.1, patrolAxis: 'y', patrolRange: 1.8 },
      { id: 'e3_4', type: 'snake', name: 'Vipère du Grès', x: 8.5, y: 11.5, speed: 1.2, patrolAxis: 'x', patrolRange: 2.0 },
    ]
  },
  {
    id: 4,
    title: "Niveau 4 : Le Cratère Ardent de Magma",
    subtitle: "Rivières de roche en fusion et braises mortelles",
    lore: "La terre gronde sous les pas imposants de King. Les geysers de flammes jaillissent des fissures du sol, et le moindre faux pas peut coûter un précieux cœur royal.",
    theme: 'magma',
    wallColor: '#7f1d1d',
    floorColor: '#450a0a',
    accentColor: '#f97316',
    width: 17,
    height: 15,
    grid: [
      "#################",
      "#...#...#...#...#",
      "###.#.#.#.#.#.###",
      "#...#.#...#.#...#",
      "#.###.#####.###.#",
      "#.#...#...#...#.#",
      "#.#.###.#.###.#.#",
      "#...#...#...#...#",
      "###.###.#.###.###",
      "#...#...#...#...#",
      "#.###.#####.###.#",
      "#...#.#...#.#...#",
      "###.#.#.#.#.#.###",
      "#...#...#...#...#",
      "#################"
    ],
    playerSpawn: { x: 1.5, y: 1.5 },
    sanctuaryExit: { x: 15.5, y: 13.5 },
    pickups: [
      { id: 'b4_1', type: 'banana', x: 8.5, y: 1.5 },
      { id: 'b4_2', type: 'banana', x: 1.5, y: 7.5 },
      { id: 'b4_3', type: 'banana', x: 15.5, y: 7.5 },
      { id: 'b4_4', type: 'banana', x: 8.5, y: 13.5 },
      { id: 'b4_5', type: 'banana', x: 8.5, y: 7.5 },
      // Bonus
      { id: 's4_1', type: 'shield', x: 15.5, y: 1.5 },
      { id: 'h4_1', type: 'heart', x: 1.5, y: 13.5 },
    ],
    traps: [
      { id: 't4_1', type: 'fire', x: 3, y: 3, interval: 1.8, offset: 0 },
      { id: 't4_2', type: 'fire', x: 13, y: 3, interval: 1.8, offset: 0.9 },
      { id: 't4_3', type: 'fire', x: 8, y: 5, interval: 2.0, offset: 0.5 },
      { id: 't4_4', type: 'spikes', x: 5, y: 7, interval: 2.0, offset: 1.0 },
      { id: 't4_5', type: 'spikes', x: 11, y: 7, interval: 2.0, offset: 0.2 },
      { id: 't4_6', type: 'fire', x: 3, y: 11, interval: 1.8, offset: 1.2 },
      { id: 't4_7', type: 'fire', x: 13, y: 11, interval: 1.8, offset: 0.3 },
    ],
    enemies: [
      { id: 'e4_1', type: 'bat', name: 'Salamandre Ailée', x: 5.5, y: 5.5, speed: 2.3, patrolAxis: 'x', patrolRange: 2.2 },
      { id: 'e4_2', type: 'bat', name: 'Chauve-souris Pyromane', x: 11.5, y: 9.5, speed: 2.4, patrolAxis: 'x', patrolRange: 2.2 },
      { id: 'e4_3', type: 'guard', name: 'Guerrier des Cendres', x: 8.5, y: 9.5, speed: 1.5, patrolAxis: 'y', patrolRange: 2.0 },
      { id: 'e4_4', type: 'carnivorous_plant', name: 'Bourgeon de Lave', x: 1.5, y: 9.5, speed: 0, patrolAxis: 'circle', patrolRange: 0 },
    ]
  },
  {
    id: 5,
    title: "Niveau 5 : Le Sanctuaire du Trône Doré",
    subtitle: "L'épreuve finale pour couronner le Roi Suprême",
    lore: "Le sommet du mont royal abrite le trône d'or mythique. Pour asseoir définitivement sa domination et sauver son peuple de la disette, King doit triompher du labyrinthe ultime et s'emparer des 5 Bananes Sacrées !",
    theme: 'throne',
    wallColor: '#581c87',
    floorColor: '#2e1065',
    accentColor: '#eab308',
    width: 19,
    height: 15,
    grid: [
      "###################",
      "#...#.......#...#.#",
      "#.###.#####.#.#.#.#",
      "#...#...#...#.#...#",
      "###.###.#.###.###.#",
      "#...#...#...#.....#",
      "#.#####.###.#####.#",
      "#...#.......#...#.#",
      "###.#.#####.#.###.#",
      "#...#...#...#...#.#",
      "#.#####.#.#####.#.#",
      "#.#.....#.....#...#",
      "#.#.#########.###.#",
      "#...#.......#.....#",
      "###################"
    ],
    playerSpawn: { x: 1.5, y: 1.5 },
    sanctuaryExit: { x: 9.5, y: 7.5 }, // Le trône au centre exact du grand labyrinthe
    pickups: [
      { id: 'b5_1', type: 'banana', x: 9.5, y: 1.5 },
      { id: 'b5_2', type: 'banana', x: 17.5, y: 1.5 },
      { id: 'b5_3', type: 'banana', x: 1.5, y: 13.5 },
      { id: 'b5_4', type: 'banana', x: 17.5, y: 13.5 },
      { id: 'b5_5', type: 'banana', x: 9.5, y: 13.5 },
      // Bonus
      { id: 's5_1', type: 'shield', x: 1.5, y: 7.5 },
      { id: 'h5_1', type: 'heart', x: 17.5, y: 7.5 },
      { id: 'p5_1', type: 'speed', x: 9.5, y: 9.5 },
    ],
    traps: [
      { id: 't5_1', type: 'fire', x: 5, y: 1, interval: 2.0, offset: 0 },
      { id: 't5_2', type: 'fire', x: 13, y: 1, interval: 2.0, offset: 1.0 },
      { id: 't5_3', type: 'spikes', x: 3, y: 5, interval: 1.9, offset: 0.5 },
      { id: 't5_4', type: 'spikes', x: 15, y: 5, interval: 1.9, offset: 1.2 },
      { id: 't5_5', type: 'fire', x: 7, y: 7, interval: 2.2, offset: 0.3 },
      { id: 't5_6', type: 'fire', x: 11, y: 7, interval: 2.2, offset: 1.4 },
      { id: 't5_7', type: 'spikes', x: 5, y: 11, interval: 1.8, offset: 0.8 },
      { id: 't5_8', type: 'spikes', x: 13, y: 11, interval: 1.8, offset: 0.2 },
    ],
    enemies: [
      { id: 'e5_1', type: 'guard', name: 'Commandant de la Garde Impériale', x: 3.5, y: 7.5, speed: 1.6, patrolAxis: 'y', patrolRange: 2.5 },
      { id: 'e5_2', type: 'guard', name: 'Champion du Roi Noir', x: 15.5, y: 7.5, speed: 1.6, patrolAxis: 'y', patrolRange: 2.5 },
      { id: 'e5_3', type: 'bat', name: 'Chauve-souris Royale d\'Ombre', x: 9.5, y: 3.5, speed: 2.4, patrolAxis: 'x', patrolRange: 3.0 },
      { id: 'e5_4', type: 'snake', name: 'Vipère Impériale Géante', x: 9.5, y: 11.5, speed: 1.5, patrolAxis: 'x', patrolRange: 3.0 },
      { id: 'e5_5', type: 'carnivorous_plant', name: 'Hydre Végétale Royale', x: 13.5, y: 13.5, speed: 0, patrolAxis: 'circle', patrolRange: 0 },
    ]
  }
];
