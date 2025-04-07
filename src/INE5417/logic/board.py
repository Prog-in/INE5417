import tkinter as tk
from tkinter import ttk

from .player import Player
from .stone import Stone
from .triangle import Triangle
from ..utils.constants import COLOR_A, COLOR_B
from ..utils.game_state import GameState
from ..utils.move_type import MoveType


class Board:
    def __init__(self) -> None:
        # deve ser fixo pois, no caso de variável, deveria haver uma comunicação entre as instâncias do jogo
        # para acertar qual cor cada jogador usaria.
        self.local_player: Player = Player(COLOR_A)
        self.remote_player: Player = Player(COLOR_B)
        self.game_state: GameState = GameState.TITLE
        self.last_move_info: None | tuple[int, Triangle] = None
        self.selected_stone: Stone | None = None
        self.triangles: list[Triangle] = self.initialize_triagles()

    def get_players_colors(self) -> tuple[str, str]:
        return self.local_player.get_color(), self.remote_player.get_color()

    def initialize_triagles(self) -> list[Triangle]:
        return [Triangle() for _ in range(12)]

    def reset_game(self):
        self.local_player: Player = Player(self.local_player.get_color())
        self.remote_player: Player = Player(self.remote_player.get_color())
        self.triangles = self.initialize_triagles()

    def calculate_range(self, last_move_info: None | tuple[int, int]) -> set[Triangle]:
        if last_move_info is None:
            return set(self.triangles)
        value, position = last_move_info
        if value == 0:
            for i in range(1, 12):
                var = set()
                left = self.triangles[(position - i) % 12]
                right = self.triangles[(position + i) % 12]
                if left.is_free():
                    var.add(left)
                if right.is_free():
                    var.add(right)
                if len(var):
                    return var
            return set()
        else:
            return {
                self.triangles[(position - value) % 12],
                self.triangles[(position + value) % 12],
            }

    def generate_valid_triangles(
        self, candidate_moves: set[Triangle]
    ) -> list[Triangle]:
        return [
            t
            for t in candidate_moves
            if t.is_free() or t.get_stone().get_color() == self.local_player.get_color()
        ]
        # for t in candidate_moves:
        #    if t.is_free() or t.get_stone().get_color() == self.local_player.get_color():
        #        yield t

    def generate_valid_move_list(self) -> list[Triangle]:
        candidate_moves = self.calculate_range(self.last_move_info)
        valid_triangles = self.generate_valid_triangles(candidate_moves)
        return valid_triangles

    def update_move_info(self, selected_triangle: Triangle):
        self.last_move_info = (self.selected_stone, selected_triangle)
        self.selected_stone = None

    def execute_move(self, selected_triangle_index: int) -> dict[str, str]:
        # atualizar self.last_move_info aqui?
        self.update_move_info(self.triangles[selected_triangle_index])
        move_type = self.decide_move_type()
        if move_type == MoveType.INSERT:
            self.insert_stone(selected_triangle_index)
        else:
            self.remove_stone(selected_triangle_index)
        return self.generate_dog_food()

    def decide_move_type(self, selected_stone: Stone) -> MoveType:
        if selected_stone.get_color() != self.local_player.get_color():
            return MoveType.ASK_AGAIN
        if selected_stone.get_on_board():
            return MoveType.REMOVE
        counter = 0
        for t in self.triangles:
            if t.get_stone().get_value() == selected_stone.get_value():
                counter += 1
        if counter < 2:
            return MoveType.INSERT
        return MoveType.ASK_AGAIN

    def insert_stone(self, selected_triangle_index: int, selected_stone: Stone) -> None:
        selected_triangle = self.triangles[selected_triangle_index]
        selected_triangle.insert_stone(selected_stone)
        selected_stone.set_on_board(True)

    def remove_stone(self, selected_triangle_index: int) -> None:
        selected_triangle = self.triangles[selected_triangle_index]
        removed_stone = selected_triangle.remove_stone()
        removed_stone.set_on_board(False)

    def generate_dog_food(
        self, move_type: str, triangle_index: int, stone_value: int, is_over: bool
    ) -> dict[str, str]:
        return {
            "move_type": move_type,
            "triangle_index": str(triangle_index),
            "stone_value": str(stone_value),
            "is_over": str(is_over),
        }

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
