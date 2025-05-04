class Stone:
    def __init__(self, i: int):
        self.color: str | None = None
        self.value: int = i
        self.on_board: bool = False

    def update(self, color: str):
        self.color = color

    def get_color(self) -> str:
        return self.color

    def get_value(self) -> int:
        return self.value

    def set_on_board(self, on_board: bool) -> None:
        self.on_board = on_board

    def get_on_board(self) -> bool:
        return self.on_board
