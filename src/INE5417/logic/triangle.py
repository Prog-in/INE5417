from src.INE5417.logic.stone import Stone


class Triangle:
    def __init__(self):
        self.border_stones: list[Stone] = []
        self.stone: Stone | None  = None

    def get_stone(self):
        return self.stone

    def set_stone(self, stone: Stone):
        if isinstance(self.stone, Stone):
            self.border_stones.append(self.stone)
        self.stone = stone

    def get_border_stones(self) -> list[Stone]:
        return self.border_stones
