from .stone import Stone


class Triangle:
    def __init__(self, index: int) -> None:
        self.stone: Stone | None = None
        self.index: int = index

    def reset(self):
        self.stone = None

    def get_stone(self) -> Stone | None:
        return self.stone

    def get_index(self) -> int:
        return self.index

    def insert_stone(self, stone: Stone) -> None:
        self.stone = stone

    def remove_stone(self) -> Stone | None:
        tmp = self.stone
        self.stone = None
        return tmp

    def is_free(self) -> bool:
        return self.stone is None
