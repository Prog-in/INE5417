from src.INE5417.logic.stone import Stone
from src.INE5417.utils.player_color import PlayerColor


class Player:
    def __init__(self, player_color: PlayerColor) -> None:
        self.name: str = ""
        self.turn: bool = False
        self.winner: bool = False
        self.color: PlayerColor = player_color
        self.stones: list[list[Stone]] = [[Stone(self.color, i), Stone(self.color, i)] for i in range(6)]


    def initialize(self, player_color: PlayerColor) -> None:
        self.name = ""
        self.turn = False
        self.winner = False
        self.color = player_color
        self.stones = [[Stone(self.color, i), Stone(self.color, i)] for i in range(6)]


    def toggle_turn(self) -> None:
        self.turn = not self.turn

    def get_name(self) -> str:
        return self.name

    def get_turn(self) -> bool:
        return self.turn

    def get_winner(self) -> bool:
        return self.winner

    def set_winner(self) -> None:
        self.winner = True

    def get_stone(self, value: int) -> Stone | None:
        try:
            return self.stones[value].pop()
        except IndexError:
            return None
