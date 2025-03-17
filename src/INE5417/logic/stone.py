from src.INE5417.utils.player_color import PlayerColor


class Stone:
    def __init__(self, color: PlayerColor, i: int):
        self.color: PlayerColor = color
        self.value: int = i

    def get_value(self) -> int:
        return self.value
