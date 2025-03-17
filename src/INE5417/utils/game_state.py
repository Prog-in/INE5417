import enum


class GameState(enum.Enum):
    TITLE = 0
    PLAYER_MOVE_1 = 1
    PLAYER_MOVE_2 = 2
    WAITING_OTHER_PLAYER = 3
    MATCH_ENDED = 4
    ABANDONED_BY_OTHER_PLAYER = 5
