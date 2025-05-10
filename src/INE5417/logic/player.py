from .stone import Stone
from ..utils.constants import COLOR_A, COLOR_B


class Player:
    def __init__(self) -> None:
        self.id: str = ""
        self.name: str = ""
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
        self.name: str = ""
        self.turn: bool = False
        self.winner: bool = False
        self.stones = []
        for i in range(6):
            same_value_stones = []
            for j in range(2):
                same_value_stones.append(Stone(i))
                same_value_stones.append(Stone(i))
            self.stones.append(same_value_stones)

    def update(self, player_name: str, player_id: str) -> None:
        for i in range(6):
            for j in range(2):
                stone = self.stones[i][j]
                stone.update(self.color)
        self.id = player_id
        self.name = player_name

    def toggle_turn(self) -> None:
        self.turn = not self.turn

    def get_id(self) -> str:
        return self.id

    def set_color(self, new_color: str) -> None:
        self.color = new_color

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
