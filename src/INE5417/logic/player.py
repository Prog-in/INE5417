from .stone import Stone


class Player:
    def __init__(self) -> None:
        self.id: str = ""
        self.name: str = ""
        self.turn: bool = False
        self.winner: bool = False
        self.color: str | None = None
        self.stones: list[list[Stone]] = []
        self.populate_stone_list()

    def reset(self) -> None:
        self.id = ""
        self.name = ""
        self.turn = False
        self.winner = False
        self.color = None
        self.stones = []
        self.populate_stone_list()

    def populate_stone_list(self) -> None:
        for i in range(6):
            left_stone = Stone(i)
            right_stone = Stone(i)
            self.stones.append([left_stone, right_stone])

    def update(self, player_name: str, player_id: str) -> None:
        for i in range(6):
            for j in range(2):
                self.stones[i][j].update(self.color)
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

    def get_stone(self, value: int, in_left: bool) -> Stone:
        return self.stones[value][in_left - 1]

    def insert_stone(self, stone: Stone, in_left: bool) -> None:
        selected_stone_value = stone.get_value()
        self.stones[selected_stone_value].insert(in_left - 1, stone)

    def remove_stone(self, selected_stone: Stone) -> None:
        selected_stone_value = selected_stone.get_value()
        self.stones[selected_stone_value].remove(selected_stone)
