import argparse
from typing import Optional, Sequence

from .app import App
from .game.levels import LEVELS


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="King Kong Labyrinth - La Quête Royale")
    parser.add_argument(
        "--autostart",
        type=int,
        nargs="?",
        const=1,
        choices=[level.id for level in LEVELS],
        help="Lance directement le niveau indiqué (1 par défaut)",
    )
    parser.add_argument("--fullscreen", action="store_true", help="Mode plein écran")
    parser.add_argument("--width", type=int, default=1100)
    parser.add_argument("--height", type=int, default=720)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    args = parse_args(argv)
    App(
        size=(args.width, args.height),
        autostart_level=args.autostart,
        fullscreen=args.fullscreen,
    ).run()


if __name__ == "__main__":
    main()
