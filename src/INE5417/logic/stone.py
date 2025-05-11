class Stone:
    def __init__(self, i: int):
        self.color: str | None = None
        self.value: int = i

    def update(self, color: str):
        self.color = color

    def get_color(self) -> str:
        return self.color

    def get_value(self) -> int:
        return self.value
