class Stone:
    def __init__(self, color: str, i: int):
        self.color: str = color
        self.value: int = i

    def get_color(self) -> str:
        return self.color

    def get_value(self) -> int:
        return self.value
