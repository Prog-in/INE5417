from .stone import Stone
from ..utils.constants import COLOR_A, COLOR_B


class Player:
    def __init__(self) -> None:
        self.id: str = ""
        self.turn: bool = False
        self.winner: bool = False
        self.color: str | None = None
        self.stones: list[list[Stone]] = []
        for i in range(6):
            same_value_stones = []
            for j in range(2):
                same_value_stones.append(Stone(i))
                same_value_stones.append(Stone(i))
            self.stones.append(same_value_stones)

    def reset(self) -> None:
        self.id: str = ""
        self.turn: bool = False
        self.winner: bool = False

    def update(self, player_id: str, player_order: int) -> None:
        if player_order == 1:
            self.color = COLOR_A
            self.turn = True
        else:  # player_order == 2
            self.color = COLOR_B
        for i in range(6):
            for j in range(2):
                stone = self.stones[i][j]
                stone.update(self.color)
        self.id = player_id

    def toggle_turn(self) -> None:
        self.turn = not self.turn

    def get_id(self) -> str:
        return self.id

    def get_color(self) -> str:
        return self.color

    def get_turn(self) -> bool:
        return self.turn

    def get_winner(self) -> bool:
        return self.winner

    def set_winner(self) -> None:
        self.winner = True

    def get_stone(self, value: int, in_left: bool) -> Stone | None:
        if len(self.stones[value]) == 0:
            return None
        else:
            return self.stones[value][not in_left]

    def remove_stone(self, value: int) -> None:
        if len(self.stones[value]) > 0:
            self.stones[value].pop()
