from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass(frozen=True)
class LevelTrap:
    id: str
    type: str
    x: int
    y: int
    interval: float
    offset: float


@dataclass(frozen=True)
class LevelEnemy:
    id: str
    type: str
    name: str
    x: float
    y: float
    speed: float
    patrol_axis: str
    patrol_range: float


@dataclass(frozen=True)
class LevelPickup:
    id: str
    type: str
    x: float
    y: float


@dataclass(frozen=True)
class LevelDefinition:
    id: int
    title: str
    subtitle: str
    lore: str
    theme: str
    wall_color: str
    floor_color: str
    accent_color: str
    width: int
    height: int
    grid: Tuple[str, ...]
    player_spawn: Tuple[float, float]
    sanctuary_exit: Tuple[float, float]
    pickups: Tuple[LevelPickup, ...] = field(default_factory=tuple)
    traps: Tuple[LevelTrap, ...] = field(default_factory=tuple)
    enemies: Tuple[LevelEnemy, ...] = field(default_factory=tuple)


LEVELS: List[LevelDefinition] = [
    LevelDefinition(
        id=1,
        title='Niveau 1 : Les Jardins Royaux',
        subtitle="L'éveil du Roi Kong dans la canopée sacrée",
        lore="Aux portes de son royaume perdu, King doit récupérer les 5 bananes primordiales éparpillées parmi la végétation pour ouvrir la porte de l'enceinte de pierre.",
        theme='jungle',
        wall_color='#166534',
        floor_color='#052e16',
        accent_color='#4ade80',
        width=15,
        height=13,
        grid=(
            "###############",
            "#.....#.......#",
            "#.###.#.#.#.#.#",
            "#...#...#.#.#.#",
            "#.#.#####.###.#",
            "#...#...#...#.#",
            "#.#.#.#.###.#.#",
            "#...#.#.....#.#",
            "#.#.#.#.#####.#",
            "#.#...........#",
            "#.#.#####.#.#.#",
            "#.........#...#",
            "###############",
        ),
        player_spawn=(1.5, 1.5),
        sanctuary_exit=(13.5, 11.5),
        pickups=(
            LevelPickup("b1_1", "banana", 13.5, 1.5),
            LevelPickup("b1_2", "banana", 3.5, 9.5),
            LevelPickup("b1_3", "banana", 9.5, 5.5),
            LevelPickup("b1_4", "banana", 7.5, 11.5),
            LevelPickup("b1_5", "banana", 7.5, 1.5),
            LevelPickup("h1_1", "heart", 9.5, 11.5),
            LevelPickup("s1_1", "shield", 1.5, 7.5),
        ),
        traps=(
            LevelTrap("t1_1", "spikes", 12, 9, 3, 0),
            LevelTrap("t1_2", "spikes", 3, 10, 3, 1.5),
            LevelTrap("t1_3", "spikes", 1, 5, 2.5, 0.8),
            LevelTrap("t1_4", "spikes", 9, 7, 3.2, 1),
        ),
        enemies=(
            LevelEnemy("e1_1", "snake", 'Vipère Émeraude', 9.5, 1.5, 1.2, "x", 2),
            LevelEnemy("e1_2", "snake", 'Cobra Royal', 5.5, 9.5, 1.4, "x", 2),
            LevelEnemy("e1_3", "carnivorous_plant", 'Plante Vorace', 13.5, 7.5, 0, "circle", 0),
        ),
    ),
    LevelDefinition(
        id=2,
        title='Niveau 2 : Les Catacombes Sombre-Royales',
        subtitle='Les couloirs hantés par les chauves-souris ancestrales',
        lore="Une brume bleutée et des torches tremblantes jalonnent les galeries sous le palais royal. Les chauves-souris en maraude attaquent dès qu'on s'aventure dans leurs nids.",
        theme='dungeon',
        wall_color='#334155',
        floor_color='#0f172a',
        accent_color='#38bdf8',
        width=17,
        height=13,
        grid=(
            "#################",
            "#.#.....#.....#.#",
            "#.###.#.#.###.#.#",
            "#.......#...#...#",
            "#.#####.#.#.#.#.#",
            "#.....#.#...#...#",
            "#.#.#.#.#.#.#.###",
            "#.#.#...#...#...#",
            "#.#.#.###.#.#.#.#",
            "#.#.#.....#...#.#",
            "#.#.###.#.#.###.#",
            "#.#.............#",
            "#################",
        ),
        player_spawn=(1.5, 1.5),
        sanctuary_exit=(15.5, 11.5),
        pickups=(
            LevelPickup("b2_1", "banana", 13.5, 1.5),
            LevelPickup("b2_2", "banana", 3.5, 11.5),
            LevelPickup("b2_3", "banana", 7.5, 5.5),
            LevelPickup("b2_4", "banana", 11.5, 7.5),
            LevelPickup("b2_5", "banana", 9.5, 11.5),
            LevelPickup("p2_1", "speed", 5.5, 3.5),
            LevelPickup("h2_1", "heart", 5.5, 1.5),
        ),
        traps=(
            LevelTrap("t2_1", "fire", 15, 2, 2.5, 0),
            LevelTrap("t2_2", "fire", 5, 5, 2.5, 1.2),
            LevelTrap("t2_3", "spikes", 1, 8, 2, 0.5),
            LevelTrap("t2_4", "spikes", 3, 6, 2, 1.5),
            LevelTrap("t2_5", "fire", 7, 1, 2.8, 0.8),
        ),
        enemies=(
            LevelEnemy("e2_1", "bat", 'Chauve-souris Furtive', 13.5, 5.5, 2, "y", 2),
            LevelEnemy("e2_2", "bat", 'Vampire des Cryptes', 11.5, 5.5, 2.2, "y", 2),
            LevelEnemy("e2_3", "snake", "Crotale d'Obsidienne", 5.5, 11.5, 1.3, "x", 2),
        ),
    ),
    LevelDefinition(
        id=3,
        title='Niveau 3 : Le Temple Solaire Oublié',
        subtitle="Dalles dorées et la garde d'honneur squelette",
        lore="Autrefois cœur spirituel de la dynastie simiesque, ce sanctuaire est gardé par les sentinelles squelettiques royales qui n'ont jamais abandonné leur poste séculaire.",
        theme='temple',
        wall_color='#854d0e',
        floor_color='#451a03',
        accent_color='#facc15',
        width=17,
        height=15,
        grid=(
            "#################",
            "#.#...#.........#",
            "#.#.#.#.#.###.#.#",
            "#.#.#.......#...#",
            "#.#.#.#.###.#.###",
            "#.#.#.......#.#.#",
            "#.#.#.###.###.#.#",
            "#.........#.....#",
            "#.###.#.#.###.#.#",
            "#.#...#.#.#...#.#",
            "#.#.###.#.#.#.#.#",
            "#.......#...#.#.#",
            "#.#######.###.#.#",
            "#.............#.#",
            "#################",
        ),
        player_spawn=(1.5, 1.5),
        sanctuary_exit=(15.5, 13.5),
        pickups=(
            LevelPickup("b3_1", "banana", 3.5, 13.5),
            LevelPickup("b3_2", "banana", 13.5, 1.5),
            LevelPickup("b3_3", "banana", 9.5, 7.5),
            LevelPickup("b3_4", "banana", 5.5, 5.5),
            LevelPickup("b3_5", "banana", 13.5, 9.5),
            LevelPickup("s3_1", "shield", 11.5, 5.5),
            LevelPickup("h3_1", "heart", 3.5, 3.5),
        ),
        traps=(
            LevelTrap("t3_1", "spikes", 14, 7, 2.2, 0),
            LevelTrap("t3_2", "spikes", 15, 11, 2.2, 1.1),
            LevelTrap("t3_3", "fire", 5, 11, 2.6, 0.4),
            LevelTrap("t3_4", "spikes", 1, 9, 2, 1),
            LevelTrap("t3_5", "fire", 12, 9, 2.5, 1.5),
        ),
        enemies=(
            LevelEnemy("e3_1", "guard", 'Garde Squelette Royal', 5.5, 7.5, 1.3, "x", 2.5),
            LevelEnemy("e3_2", "guard", 'Sentinelle Dorée', 9.5, 13.5, 1.3, "x", 2.5),
            LevelEnemy("e3_3", "bat", 'Chauve-souris des Tombeaux', 13.5, 7.5, 2.1, "y", 1.8),
            LevelEnemy("e3_4", "snake", 'Vipère du Grès', 9.5, 1.5, 1.2, "x", 2),
        ),
    ),
    LevelDefinition(
        id=4,
        title='Niveau 4 : Le Cratère Ardent de Magma',
        subtitle='Rivières de roche en fusion et braises mortelles',
        lore='La terre gronde sous les pas imposants de King. Les geysers de flammes jaillissent des fissures du sol, et le moindre faux pas peut coûter un précieux cœur royal.',
        theme='magma',
        wall_color='#7f1d1d',
        floor_color='#450a0a',
        accent_color='#f97316',
        width=17,
        height=15,
        grid=(
            "#################",
            "#...............#",
            "#.#.###.#.#####.#",
            "#.....#.....#...#",
            "#####.###.#.#####",
            "#...#...........#",
            "#.#####.#####.#.#",
            "#...........#.#.#",
            "#.###.#.#.#.#.#.#",
            "#.#.#.#...#.....#",
            "#.#.#.#.#####.#.#",
            "#...#.......#...#",
            "###.###.#######.#",
            "#.....#.........#",
            "#################",
        ),
        player_spawn=(1.5, 1.5),
        sanctuary_exit=(15.5, 13.5),
        pickups=(
            LevelPickup("b4_1", "banana", 9.5, 5.5),
            LevelPickup("b4_2", "banana", 3.5, 11.5),
            LevelPickup("b4_3", "banana", 15.5, 1.5),
            LevelPickup("b4_4", "banana", 11.5, 11.5),
            LevelPickup("b4_5", "banana", 5.5, 7.5),
            LevelPickup("s4_1", "shield", 1.5, 7.5),
            LevelPickup("h4_1", "heart", 7.5, 9.5),
        ),
        traps=(
            LevelTrap("t4_1", "fire", 9, 2, 1.8, 0),
            LevelTrap("t4_2", "fire", 11, 3, 1.8, 0.9),
            LevelTrap("t4_3", "fire", 13, 11, 2, 0.5),
            LevelTrap("t4_4", "spikes", 15, 7, 2, 1),
            LevelTrap("t4_5", "spikes", 7, 11, 2, 0.2),
            LevelTrap("t4_6", "fire", 11, 8, 1.8, 1.2),
            LevelTrap("t4_7", "fire", 3, 7, 1.8, 0.3),
        ),
        enemies=(
            LevelEnemy("e4_1", "bat", 'Salamandre Ailée', 7.5, 7.5, 2.3, "x", 2.2),
            LevelEnemy("e4_2", "bat", 'Chauve-souris Pyromane', 9.5, 1.5, 2.4, "x", 2.2),
            LevelEnemy("e4_3", "guard", 'Guerrier des Cendres', 13.5, 7.5, 1.5, "y", 2),
            LevelEnemy("e4_4", "carnivorous_plant", 'Bourgeon de Lave', 6.5, 5.5, 0, "circle", 0),
        ),
    ),
    LevelDefinition(
        id=5,
        title='Niveau 5 : Le Sanctuaire du Trône Doré',
        subtitle="L'épreuve finale pour couronner le Roi Suprême",
        lore="Le sommet du mont royal abrite le trône d'or mythique. Pour asseoir définitivement sa domination et sauver son peuple de la disette, King doit triompher du labyrinthe ultime et s'emparer des 5 Bananes Sacrées !",
        theme='throne',
        wall_color='#581c87',
        floor_color='#2e1065',
        accent_color='#eab308',
        width=19,
        height=15,
        grid=(
            "###################",
            "#.#.......#.......#",
            "#.#####.#.#.#.###.#",
            "#.......#...#.....#",
            "#######.#.#.#.###.#",
            "#.#.......#.......#",
            "#.#.###.#.#.#.#.#.#",
            "#...........#...#.#",
            "#.#########.#.###.#",
            "#.#.....#...#.....#",
            "#.#.###.#.###.#.###",
            "#.#...#.....#.....#",
            "#.###.#.#.#.#.###.#",
            "#...........#.....#",
            "###################",
        ),
        player_spawn=(1.5, 1.5),
        sanctuary_exit=(17.5, 13.5),
        pickups=(
            LevelPickup("b5_1", "banana", 13.5, 3.5),
            LevelPickup("b5_2", "banana", 5.5, 11.5),
            LevelPickup("b5_3", "banana", 11.5, 9.5),
            LevelPickup("b5_4", "banana", 7.5, 5.5),
            LevelPickup("b5_5", "banana", 1.5, 7.5),
            LevelPickup("s5_1", "shield", 11.5, 1.5),
            LevelPickup("h5_1", "heart", 17.5, 11.5),
            LevelPickup("p5_1", "speed", 15.5, 1.5),
        ),
        traps=(
            LevelTrap("t5_1", "fire", 17, 6, 2, 0),
            LevelTrap("t5_2", "fire", 5, 5, 2, 1),
            LevelTrap("t5_3", "spikes", 17, 3, 1.9, 0.5),
            LevelTrap("t5_4", "spikes", 5, 1, 1.9, 1.2),
            LevelTrap("t5_5", "fire", 9, 6, 2.2, 0.3),
            LevelTrap("t5_6", "fire", 14, 7, 2.2, 1.4),
            LevelTrap("t5_7", "spikes", 14, 3, 1.8, 0.8),
            LevelTrap("t5_8", "spikes", 7, 11, 1.8, 0.2),
        ),
        enemies=(
            LevelEnemy("e5_1", "guard", 'Commandant de la Garde Impériale', 11.5, 5.5, 1.6, "y", 2.5),
            LevelEnemy("e5_2", "guard", 'Champion du Roi Noir', 13.5, 7.5, 1.6, "y", 2.5),
            LevelEnemy("e5_3", "bat", "Chauve-souris Royale d'Ombre", 7.5, 13.5, 2.4, "x", 3),
            LevelEnemy("e5_4", "snake", 'Vipère Impériale Géante', 5.5, 7.5, 1.5, "x", 3),
            LevelEnemy("e5_5", "carnivorous_plant", 'Hydre Végétale Royale', 10.5, 11.5, 0, "circle", 0),
        ),
    ),
]


def get_level(level_id: int) -> LevelDefinition:
    for level in LEVELS:
        if level.id == level_id:
            return level
    return LEVELS[0]
