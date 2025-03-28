import random

from .player import Player
from .stone import Stone
from .triangle import Triangle
from ..utils.constants import COLOR_A, COLOR_B
from ..utils.game_state import GameState


class Board:
    def __init__(self) -> None:
        # deve ser fixo pois, no caso de variável, deveria haver uma comunicação entre as instâncias do jogo
        # para acertar qual cor cada jogador usaria.
        self.local_player: Player = Player(COLOR_A)
        self.remote_player: Player = Player(COLOR_B)
        self.game_state: GameState = GameState.TITLE
        self.regular_move: bool = True
        self.last_positioned_stone: Stone | None = None
        self.selected_stone: Stone | None = None
        self.triangles: list[Triangle] = self.initialize_triagles()

    # def get_random_colors(self) -> list[str]:
    #     colors = [COLOR_A, COLOR_B]
    #     random.shuffle(colors)
    #     return colors

    def get_players_colors(self):
        return self.local_player.get_color(), self.remote_player.get_color()

    def initialize_triagles(self) -> list[Triangle]:
        return [Triangle() for _ in range(12)]

    def reset_game(self):
        self.local_player: Player = Player(self.local_player.get_color())
        self.remote_player: Player = Player(self.remote_player.get_color())
        self.triangles = self.initialize_triagles()

    def stone_selected(self, stone_color: str, stone_value: int) -> list[int]:
        player = self.local_player if stone_color == self.local_player.get_color() else self.remote_player
        self.selected_stone = player.get_stone(stone_value)
        print("pedra selecionada", self.selected_stone.get_value())
        if self.last_positioned_stone is None:  # primeiro move
            return list(range(12))
        else:  # moves posteriores
            # TODO: esquematizar uma forma relação direta entre a pedra posicionada anteriormente e seu triângulo
            last_positioned_stones_triangle_index = 0  # apenas para o analisador sintático não reclamar de variável sem valor
            for i, triangle in enumerate(self.triangles):
                if triangle.get_stone() == self.last_positioned_stone:
                    last_positioned_stones_triangle_index = i
                    break
            if stone_value > 0:
                possible_triangles_indexes = [
                    (last_positioned_stones_triangle_index - stone_value) % 12,
                    (last_positioned_stones_triangle_index + stone_value) % 12
                ]
                return [i for i in possible_triangles_indexes if self.triangles[i].get_stone() is None]
            else:
                # TODO: tratar caso especial da pedra zero
                return []


    def triangle_selected(self, triangle_index: int) -> dict[str, str]:
        # TODO: implementar cadeia de execuções para o caso de um triângulo válido ser selecionado (remover a pedra do
        #  jogador apenas nesse passo)
        self.last_positioned_stone = self.selected_stone
        self.local_player.remove_stone(self.selected_stone.get_value())
        move_to_send = {
            "move_type": "placing",
            "triangle_index": str(triangle_index),
            "stone_color": self.selected_stone.get_color(),
            "stone_value": str(self.selected_stone.get_value()),
            "match_status": "next"  # dog key-value
        }
        return move_to_send

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

    def get_board(self) -> list[tuple[tuple[str, str] | None, tuple[str, str] | None]]:
        board = []
        for triangle in self.triangles:
            board.append(
                (
                    self.stone_to_tuple(triangle.stone) if triangle.stone else None,
                    self.stone_to_tuple(triangle.border_stone) if triangle.border_stone else None,
                )
            )
        return board

    def stone_to_tuple(self, stone: Stone) -> tuple[str, str]:
        return str(stone.value), stone.color
