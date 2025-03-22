from pathlib import Path

GAME_NAME: str = "Qyshinsu"
VERSION: str = "0.1"
WINDOW_WIDTH: int = 1000
WINDOW_HEIGHT: int = 800
WINDOW_GEOMETRY: str = f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
BOARD_FACTOR: float = 0.587
BOARD_WIDTH: int = int(WINDOW_WIDTH * BOARD_FACTOR)
BOARD_HEIGHT: int = int(WINDOW_HEIGHT * BOARD_FACTOR)
RESOURCES_DIR: Path = Path(__file__).parent.parent.parent / "resources"
FONT: str = "Arial 12 bold"