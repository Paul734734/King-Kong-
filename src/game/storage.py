import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict


@dataclass
class SavedLevelData:
    stars: int = 0
    high_score: int = 0
    completed: bool = False


class SaveStore:
    def __init__(self, path: Path | None = None):
        self.path = path or Path.home() / ".king_kong_labyrinth" / "save.json"
        self.progress: Dict[int, SavedLevelData] = {1: SavedLevelData()}
        self.muted: bool = False
        self._load()

    def _load(self) -> None:
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return
        try:
            progress = raw.get("progress", {})
            loaded = {
                int(level_id): SavedLevelData(
                    stars=int(data.get("stars", 0)),
                    high_score=int(data.get("high_score", 0)),
                    completed=bool(data.get("completed", False)),
                )
                for level_id, data in progress.items()
            }
            if loaded:
                self.progress = loaded
            self.muted = bool(raw.get("muted", False))
        except (AttributeError, TypeError, ValueError):
            return

    def _save(self) -> None:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            payload = {
                "muted": self.muted,
                "progress": {str(k): asdict(v) for k, v in self.progress.items()},
            }
            self.path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        except OSError:
            return

    def get_level(self, level_id: int) -> SavedLevelData:
        return self.progress.get(level_id, SavedLevelData())

    def record_completion(self, level_id: int, stars: int, score: int) -> None:
        existing = self.progress.get(level_id, SavedLevelData())
        self.progress[level_id] = SavedLevelData(
            stars=max(existing.stars, stars),
            high_score=max(existing.high_score, score),
            completed=True,
        )
        self._save()

    def set_muted(self, muted: bool) -> None:
        self.muted = muted
        self._save()

    @property
    def total_stars(self) -> int:
        return sum(item.stars for item in self.progress.values())

    @property
    def total_score(self) -> int:
        return sum(item.high_score for item in self.progress.values())
