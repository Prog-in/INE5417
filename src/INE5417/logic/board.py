import random

from src.INE5417.logic.player import Player
from src.INE5417.logic.triangle import Triangle
from src.INE5417.utils.game_state import GameState
from src.INE5417.utils.player_color import PlayerColor


class Board:
    def __init__(self) -> None:
        colors = self.get_colors()
        self.local_player: Player = Player(colors[0])
        self.remote_player: Player = Player(colors[1])
        self.game_state: GameState = GameState.TITLE
        self.regular_move: bool = True
        self.triangles: list[Triangle] = self.initialize_triagles()


    def get_colors(self) -> list[PlayerColor]:
        local_player_is_blue = bool(random.getrandbits(1))
        if local_player_is_blue:
            return [PlayerColor.COLOR_A, PlayerColor.COLOR_B]
        return [PlayerColor.COLOR_B, PlayerColor.COLOR_A]


    def initialize_triagles(self) -> list[Triangle]:
        triangles = []
        for i in range(12):
            triangles.append(Triangle())
        return triangles


    def reset_game(self):
        colors = self.get_colors()
        self.local_player: Player = Player(colors[0])
        self.remote_player: Player = Player(colors[1])
        self.triangles = self.initialize_triagles()


    def select_triangle(self):
        ...


    def receive_move(self, a_move):
        # grid_line1 = int(a_move["first_action_line"])
        # grid_column1 = int(a_move["first_action_column"])
        # grid_line2 = int(a_move["second_action_line"])
        # grid_column2 = int(a_move["second_action_column"])
        if self.game_state == GameState.WAITING_OTHER_PLAYER:
            self.select_triangle()


    def receive_withdrawal_notification(self):
        self.game_state = GameState.ABANDONED_BY_OTHER_PLAYER


    def start_match(self, players) -> None:
        # playerA_name  = players[0][0]
        # playerA_id    = players[0][1]
        playerA_order = players[0][2]
        # playerB_name  = players[1][0]
        # playerB_id    = players[1][1]
        # TODO: endender o que é vem em local_player_id e o que deve ser salvo em Player
        self.local_player.initialize(0)
        self.remote_player.initialize(1)
        if playerA_order == "1":
            self.local_player.toggle_turn()
            self.game_state = GameState.PLAYER_MOVE_1
        else:
            self.remote_player.toggle_turn()
            self.game_state = GameState.WAITING_OTHER_PLAYER


    def get_game_state(self) -> GameState:
        return self.game_state


    def get_turn_player(self) -> Player | None:
        player = None
        if self.local_player.get_turn():
            player = self.local_player
        if self.remote_player.get_turn():
            player = self.remote_player
        # player = self.local_player if self.local_player.get_turn() else self.remote_player
        self.local_player.toggle_turn()
        self.remote_player.toggle_turn()
        return player


    def get_status(self):
        turn_player = self.get_turn_player()
        if not self.regular_move:
            ... # jogada irregular
        else:
            match self.game_state:
                case GameState.TITLE:
                    ...
                case GameState.PLAYER_MOVE_1:
                    ...
                case GameState.PLAYER_MOVE_2:
                    ...
                case GameState.WAITING_OTHER_PLAYER:
                    ...
                case GameState.MATCH_ENDED:
                    ...


    def select_board_triangle(self, grid_line, grid_column):
        move_to_send = {}
        if self.game_state == GameState.PLAYER_MOVE_1:
            ...
        return move_to_send
