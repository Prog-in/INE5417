from .stone import Stone


class Triangle:
    def __init__(self):
        self.border_stone: Stone | None = None
        self.stone: Stone | None = None

    def reset(self):
        self.border_stone = None
        self.stone = None

    def get_stone(self) -> Stone | None:
        return self.stone

    def insert_stone(self, stone: Stone) -> None:
        self.stone = stone

    def remove_stone(self) -> Stone | None:
        if self.stone is not None:
            self.border_stone = self.stone
        tmp = self.stone
        self.stone = None
        return tmp

    def get_border_stone(self) -> Stone:
        return self.border_stone

    def is_free(self) -> bool:
        return self.stone is None
