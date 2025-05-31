from pathlib import Path

GAME_NAME: str = "Qyshinsu"
VERSION: str = "0.1"

RESOURCES_DIR: Path = Path(__file__).parent.parent.parent / "resources"

FONT: str = "Arial 12 bold"

WINDOW_WIDTH: int = 1000
WINDOW_HEIGHT: int = 800
WINDOW_GEOMETRY: str = f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
BOARD_WIDTH: int = int(WINDOW_WIDTH * 0.587)
BOARD_HEIGHT: int = int(WINDOW_HEIGHT * 0.587)

COLOR_A = "red"
COLOR_B = "black"

ASSETS_INFO = (
    ("menu_image.png", (WINDOW_WIDTH, WINDOW_HEIGHT)),
    ("menu_button.png", (int(WINDOW_WIDTH / 3.2), BOARD_HEIGHT // 7)),
    ("board.png", (BOARD_WIDTH, BOARD_HEIGHT)),
    ("circle.png", (int(BOARD_WIDTH * 0.13), int(BOARD_HEIGHT * 0.13)))
)

POSITIONS_COORDINATES = (
    (320, 80),
    (420, 110),
    (480, 175),
    (490, 255),
    (450, 330),
    (360, 380),
    (265, 390),
    (170, 360),
    (105, 295),
    (90, 210),
    (135, 135),
    (220, 85),
)

BORDERS_COORDINATES = (
    (330, 25),
    (455, 65),
    (540, 150),
    (560, 260),
    (510, 355),
    (395, 430),
    (260, 445),
    (135, 405),
    (45, 318),
    (30, 200),
    (75, 105),
    (185, 40),
)

