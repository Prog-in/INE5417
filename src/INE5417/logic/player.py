from .stone import Stone
from ..utils.constants import COLOR_A, COLOR_B


class Player:
    def __init__(self, player_color: str) -> None:
        self.id: str = ""
        self.turn: bool = False
        self.winner: bool = False
        self.color: str = player_color
        self.stones: list[list[Stone]] = [
            [Stone(self.color, i), Stone(self.color, i)] for i in range(6)
        ]

    def initialize(self, player_id: str, player_order: int) -> None:
        if player_order == 1:
            self.color = COLOR_A
            self.turn = True
        else:  # player_order == 2
            self.color = COLOR_B
            self.turn = False
        self.id = player_id
        self.winner = False
        self.stones = [[Stone(self.color, i), Stone(self.color, i)] for i in range(6)]

    def toggle_turn(self) -> None:
        self.turn = not self.turn

    def get_id(self) -> str:
        return self.id

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
