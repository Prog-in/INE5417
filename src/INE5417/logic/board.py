import random

from .player import Player
from .stone import Stone
from .triangle import Triangle
from ..utils.constants import COLOR_A, COLOR_B
from ..utils.game_state import GameState


class Board:
    def __init__(self) -> None:
        colors = self.get_colors()
        self.local_player: Player = Player(colors[0])
        self.remote_player: Player = Player(colors[1])
        self.game_state: GameState = GameState.TITLE
        self.regular_move: bool = True
        self.triangles: list[Triangle] = self.initialize_triagles()

    def get_colors(self) -> list[str]:
        colors = [COLOR_A, COLOR_B]
        random.shuffle(colors)
        return colors

    def initialize_triagles(self) -> list[Triangle]:
        return [Triangle() for _ in range(12)]

    def reset_game(self):
        colors = self.get_colors()
        self.local_player: Player = Player(colors[0])
        self.remote_player: Player = Player(colors[1])
        self.triangles = self.initialize_triagles()

    def stone_selected(self, stone_color: str, stone_number: int) -> list[int]:
        # TODO: implementar lógica de verificação de triângulos válidos e retorná-los (não remover a pedra do jogador
        #  ainda)
        return [0]

    def triangle_selected(self, triangle_index: int):
        # TODO: implementar cadeia de execuções para o caso de um triângulo válido ser selecionado (remover a pedra do
        #  jogador apenas nesse passo)
        ...

    def receive_move(self, a_move):
        if self.game_state == GameState.WAITING_OTHER_PLAYER:
            ...

    def receive_withdrawal_notification(self):
        self.game_state = GameState.ABANDONED_BY_OTHER_PLAYER

    def start_match(self, players: list[list[str, str, str]]) -> None:
        player_a_name = players[0][0]
        player_a_id = players[0][1]
        player_a_order = int(players[0][2])
        player_b_name = players[1][0]
        player_b_id = players[1][1]
        player_b_order = int(players[1][2])
        self.local_player.initialize(player_a_id, player_a_order)
        self.remote_player.initialize(player_b_id, player_b_order)
        if player_a_order == 1:
            self.game_state = GameState.PLAYER_MOVE_1
        else:
            self.game_state = GameState.WAITING_OTHER_PLAYER

    def get_game_state(self) -> GameState:
        return self.game_state

    def get_turn_player(self) -> Player:
        player = (
            self.local_player if self.local_player.get_turn() else self.remote_player
        )
        self.local_player.toggle_turn()
        self.remote_player.toggle_turn()
        return player

    def get_board(self) -> list[tuple[tuple[str, str] | None, list[tuple[str, str]]]]:
        board = []
        for triangle in self.triangles:
            board.append(
                (
                    self.stone_to_tuple(triangle.stone) if triangle.stone else None,
                    [
                        self.stone_to_tuple(border_stone)
                        for border_stone in triangle.border_stones
                    ],
                )
            )
        return board

    def stone_to_tuple(self, stone: Stone) -> tuple[str, str]:
        return str(stone.value), stone.color
