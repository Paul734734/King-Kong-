import array
import math
import random
import threading
from pathlib import Path
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

import pygame

from .storage import SaveStore

SAMPLE_RATE = 22050

MUSIC_VOLUME = 0.30
BPM = 118
BEAT = 60.0 / BPM

# (basse, accord) pour chaque mesure : Am | F | C | G | Am | F | G | Am
CHORDS = [
    (45, (57, 60, 64)), (41, (53, 57, 60)), (48, (60, 64, 67)), (43, (55, 59, 62)),
    (45, (57, 60, 64)), (41, (53, 57, 60)), (43, (55, 59, 62)), (45, (57, 60, 64)),
]

# Mélodie par mesure : (temps, note MIDI, durée en temps)
MELODY = [
    [(0, 76, 1), (1, 72, .5), (1.5, 74, .5), (2, 76, 1), (3, 79, 1)],
    [(0, 77, 1), (1, 76, .5), (1.5, 72, .5), (2, 74, 2)],
    [(0, 76, 1), (1, 79, .5), (1.5, 76, .5), (2, 72, 1), (3, 74, 1)],
    [(0, 74, 1.5), (1.5, 71, .5), (2, 74, 1), (3, 79, 1)],
    [(0, 76, 1), (1, 72, .5), (1.5, 74, .5), (2, 76, 1), (3, 81, 1)],
    [(0, 81, 1), (1, 79, .5), (1.5, 77, .5), (2, 76, 2)],
    [(0, 74, 1), (1, 79, 1), (2, 71, 1), (3, 74, 1)],
    [(0, 72, 2), (2, 69, 2)],
]


def _constant(freq: float) -> Callable[[float], float]:
    return lambda t: freq


def _exp_ramp(f0: float, f1: float, duration: float) -> Callable[[float], float]:
    return lambda t: f0 * (f1 / f0) ** min(1.0, t / duration)


def _linear_ramp(f0: float, f1: float, duration: float) -> Callable[[float], float]:
    return lambda t: f0 + (f1 - f0) * min(1.0, t / duration)


def _steps(points: List[tuple]) -> Callable[[float], float]:
    def freq(t: float) -> float:
        current = points[0][1]
        for start, value in points:
            if t >= start:
                current = value
        return current

    return freq


@dataclass
class Tone:
    wave: str
    duration: float
    freq: Callable[[float], float]
    volume: float
    end_volume: float
    offset: float = 0.0


def _wave_sample(wave: str, phase: float) -> float:
    p = phase % 1.0
    if wave == "sine":
        return math.sin(2 * math.pi * p)
    if wave == "triangle":
        return 1.0 - 4.0 * abs(((p + 0.25) % 1.0) - 0.5)
    if wave == "sawtooth":
        return 2 * p - 1
    if wave == "square":
        return 1.0 if p < 0.5 else -1.0
    return 0.0


# ---------------------------------------------------------------------------
# Rendu de la musique de fond
# ---------------------------------------------------------------------------
def _midi(n: int) -> float:
    return 440.0 * 2 ** ((n - 69) / 12)


def _add_note(buf, start_s, dur_s, freq, wave, vol):
    start = int(start_s * SAMPLE_RATE)
    count = min(int(dur_s * SAMPLE_RATE), len(buf) - start)
    attack = int(0.008 * SAMPLE_RATE)
    step = freq / SAMPLE_RATE
    phase = 0.0
    for i in range(count):
        env = min(1.0, i / attack) * (1 - i / count) ** 0.6
        phase += step
        buf[start + i] += _wave_sample(wave, phase) * vol * env


def _add_kick(buf, start_s):
    start = int(start_s * SAMPLE_RATE)
    count = min(int(0.12 * SAMPLE_RATE), len(buf) - start)
    phase = 0.0
    for i in range(count):
        t = i / SAMPLE_RATE
        phase += (120 * (45 / 120) ** (t / 0.12)) / SAMPLE_RATE
        buf[start + i] += math.sin(2 * math.pi * phase) * 0.32 * (1 - i / count)


def _add_hat(buf, start_s, rng):
    start = int(start_s * SAMPLE_RATE)
    count = min(int(0.04 * SAMPLE_RATE), len(buf) - start)
    for i in range(count):
        buf[start + i] += rng.uniform(-1, 1) * 0.04 * (1 - i / count)


def render_music_loop() -> bytes:
    bar = 4 * BEAT
    total = int(len(CHORDS) * bar * SAMPLE_RATE)
    buf = [0.0] * total
    rng = random.Random(7)
    eighth = BEAT / 2

    for b, (root, chord) in enumerate(CHORDS):
        t0 = b * bar
        for k in range(8):  # basse + arpège en croches
            t = t0 + k * eighth
            bass = root + (12 if k % 4 == 3 else 0)
            _add_note(buf, t, eighth * 0.95, _midi(bass), "triangle", 0.30)
            arp = chord[[0, 1, 2, 1, 0, 1, 2, 1][k]] + 12
            _add_note(buf, t, eighth * 0.85, _midi(arp), "square", 0.04)
            if k % 2 == 1:
                _add_hat(buf, t, rng)
        _add_kick(buf, t0)
        _add_kick(buf, t0 + 2 * BEAT)
        for beat, note, length in MELODY[b]:  # mélodie
            _add_note(buf, t0 + beat * BEAT, length * BEAT * 0.92,
                      _midi(note), "square", 0.08)

    pcm = array.array("h", (int(max(-1.0, min(1.0, v)) * 32767 * 0.9) for v in buf))
    return pcm.tobytes()


class SoundManager:
    def __init__(self, store: SaveStore):
        self.store = store
        self.is_muted = store.muted
        self.ready = False
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.music_sound: Optional[pygame.mixer.Sound] = None
        self.music_channel: Optional[pygame.mixer.Channel] = None
        self._music_wanted = False
        self._music_playing = False
        self._lock = threading.Lock()
        self._init_mixer()

    def _init_mixer(self) -> None:
        try:
            pygame.mixer.pre_init(SAMPLE_RATE, -16, 1, 512)
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            pygame.mixer.set_reserved(1)  # canal 0 réservé à la musique
            self.music_channel = pygame.mixer.Channel(0)
            self.ready = True
            self._build_sounds()
            threading.Thread(target=self._build_music, daemon=True).start()
        except pygame.error:
            self.ready = False

    def _render(self, tones: List[Tone]) -> pygame.mixer.Sound:
        total = max(tone.offset + tone.duration for tone in tones)
        buffer = [0.0] * (int(total * SAMPLE_RATE) + 1)
        for tone in tones:
            start = int(tone.offset * SAMPLE_RATE)
            count = int(tone.duration * SAMPLE_RATE)
            phase = 0.0
            ratio = tone.end_volume / tone.volume
            for i in range(count):
                t = i / SAMPLE_RATE
                phase += tone.freq(t) / SAMPLE_RATE
                gain = tone.volume * ratio ** (t / tone.duration)
                buffer[start + i] += _wave_sample(tone.wave, phase) * gain
        pcm = array.array(
            "h",
            (int(max(-1.0, min(1.0, v)) * 32767 * 0.9) for v in buffer),
        )
        return pygame.mixer.Sound(buffer=pcm.tobytes())

    def _build_sounds(self) -> None:
        self.sounds["banana"] = self._render(
            [
                Tone(
                    "triangle",
                    0.35,
                    _steps([(0, 523.25), (0.05, 659.25), (0.10, 783.99), (0.15, 1046.50)]),
                    0.25,
                    0.001,
                )
            ]
        )
        self.sounds["heart"] = self._render(
            [Tone("sine", 0.3, _exp_ramp(440, 880, 0.2), 0.2, 0.001)]
        )

        def shield_freq(t: float) -> float:
            if t < 0.25:
                return 300 + (900 - 300) * (t / 0.25)
            return 900 * (600 / 900) ** min(1.0, (t - 0.25) / 0.15)

        self.sounds["shield"] = self._render([Tone("sine", 0.4, shield_freq, 0.2, 0.01)])
        self.sounds["damage"] = self._render(
            [Tone("sawtooth", 0.25, _exp_ramp(180, 50, 0.25), 0.35, 0.001)]
        )
        self.sounds["trap_warning"] = self._render(
            [Tone("square", 0.05, _constant(800), 0.05, 0.001)]
        )
        self.sounds["trap_burst"] = self._render(
            [Tone("sawtooth", 0.15, _exp_ramp(240, 80, 0.15), 0.18, 0.001)]
        )
        self.sounds["level_victory"] = self._render(
            [
                Tone("triangle", 0.35, _constant(freq), 0.25, 0.001, offset=idx * 0.12)
                for idx, freq in enumerate([440, 554.37, 659.25, 880])
            ]
        )
        self.sounds["game_over"] = self._render(
            [
                Tone("sawtooth", 0.28, _constant(freq), 0.2, 0.001, offset=idx * 0.14)
                for idx, freq in enumerate([350, 310, 260, 195])
            ]
        )

    # ---------- Musique de fond ----------
    def _load_music_file(self) -> Optional[pygame.mixer.Sound]:
        """Cherche une vraie musique dans assets/music (ogg, wav, mp3)."""
        folder = Path(__file__).resolve().parents[2] / "assets" / "music"
        if not folder.is_dir():
            return None
        for ext in ("*.ogg", "*.wav", "*.mp3"):
            for file in sorted(folder.glob(ext)):
                try:
                    return pygame.mixer.Sound(str(file))
                except pygame.error:
                    continue
        return None

    def _build_music(self) -> None:
        sound = self._load_music_file() or pygame.mixer.Sound(buffer=render_music_loop())
        with self._lock:
            self.music_sound = sound
            if self._music_wanted:
                self._start_music()

    def _music_volume(self) -> float:
        return 0.0 if self.is_muted else MUSIC_VOLUME

    def _start_music(self) -> None:
        if not self.ready or self.music_sound is None or self.music_channel is None:
            return
        if self._music_playing:
            return
        self._music_playing = True
        self.music_channel.play(self.music_sound, loops=-1, fade_ms=1500)
        self.music_channel.set_volume(self._music_volume())

    def play_music(self) -> None:
        with self._lock:
            self._music_wanted = True
            if self.ready and self.music_channel is not None:
                self.music_channel.unpause()
            self._start_music()

    def stop_music(self, fade_ms: int = 600) -> None:
        with self._lock:
            self._music_wanted = False
            self._music_playing = False
            if self.ready and self.music_channel is not None:
                self.music_channel.unpause()
                self.music_channel.fadeout(fade_ms)

    def pause_music(self) -> None:
        if self.ready and self.music_channel is not None:
            self.music_channel.pause()

    def resume_music(self) -> None:
        if self.ready and self.music_channel is not None:
            self.music_channel.unpause()

    # ---------- Mute ----------
    def toggle_mute(self) -> bool:
        self.is_muted = not self.is_muted
        self.store.set_muted(self.is_muted)
        if self.ready and self.music_channel is not None:
            self.music_channel.set_volume(self._music_volume())
        return self.is_muted

    def get_muted(self) -> bool:
        return self.is_muted

    # ---------- Effets ----------
    def _play(self, name: str) -> None:
        if self.is_muted or not self.ready:
            return
        sound: Optional[pygame.mixer.Sound] = self.sounds.get(name)
        if sound is not None:
            sound.play()

    def play_banana(self) -> None:
        self._play("banana")

    def play_heart(self) -> None:
        self._play("heart")

    def play_shield(self) -> None:
        self._play("shield")

    def play_damage(self) -> None:
        self._play("damage")

    def play_trap_warning(self) -> None:
        self._play("trap_warning")

    def play_trap_burst(self) -> None:
        self._play("trap_burst")

    def play_level_victory(self) -> None:
        self.stop_music(300)  # la musique s'efface pour laisser place au jingle
        self._play("level_victory")

    def play_game_over(self) -> None:
        self.stop_music(300)
        self._play("game_over")
