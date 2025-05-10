import enum


class GameState(enum.Enum):
    MAIN_MENU = 0
    LOCAL_PLAYER_TO_MOVE = 1
    REMOTE_PLAYER_TO_MOVE = 2
    MATCH_ENDED = 3
    ABANDONED_BY_OTHER_PLAYER = 4
