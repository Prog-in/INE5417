from time import time
from pathlib import Path

milliseconds = int(time() * 1000)
game_id = str(milliseconds - 1639872000000)
path = Path(__file__).parent
file = open(path / "game.id", "w")
file.write(game_id)
file.close()
