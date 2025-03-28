from .stone import Stone


class Triangle:
    def __init__(self):
        self.border_stone: Stone | None = None
        self.stone: Stone | None = None

    def get_stone(self):
        return self.stone

    def move_stone_to_border(self):
        self.border_stone = self.stone
        self.stone = None

    def place_stone(self, stone: Stone):
        if self.stone is not None:
            self.border_stone = self.stone
        self.stone = stone

    def get_border_stone(self) -> Stone | None:
        return self.border_stone
