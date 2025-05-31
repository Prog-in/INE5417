from .player import Player
from .stone import Stone
from .triangle import Triangle
from ..utils.constants import COLOR_A, COLOR_B
from ..utils.game_state import GameState
from ..utils.move_type import MoveType


class Board:
    def __init__(self) -> None:
        self.local_player: Player = Player()
        self.remote_player: Player = Player()
        self.game_state: GameState | None = None
        self.is_legal_move: bool | None = None
        self.last_opponent_move_info: tuple[int, int, MoveType] | None = None
        self.selected_stone_info: tuple[Stone, bool] | None = None
        self.border_stone_info: tuple[Stone, int] | None = None
        self.removed_stone: Stone | None = None
        self.move_to_send: dict[str, str] = {}
        self.triangles: list[Triangle] = []
        for i in range(12):
            self.triangles.append(Triangle(i))

    def get_selected_stone(self) -> Stone | None:
        return self.selected_stone_info[0]

    def is_selected_stone_in_left(self) -> bool:
        return self.selected_stone_info[1]

    def is_stone_in_border(self) -> bool:
        if self.border_stone_info is None:
            return False
        else:
            return True

    def set_border_stone_info(self, border_stone_info: tuple[Stone, int] | None) -> None:
        self.border_stone_info = border_stone_info

    def get_stone_in_border(self) -> Stone:
        return self.border_stone_info[0]

    def get_stone_in_border_position(self) -> int:
        return self.border_stone_info[1]

    def get_local_player_color(self) -> str:
        return self.local_player.get_color()

    def get_remote_player_color(self) -> str:
        return self.remote_player.get_color()

    def is_local_player_winner(self) -> bool:
        return self.local_player.get_winner()

    def calculate_range(
        self, previous_move_stone_value: int, previous_move_position: int, player_color: str
    ) -> set[Triangle]:
        legal_positions_set = set()
        possible_triangles = {
            self.triangles[(previous_move_position - previous_move_stone_value) % 12],
            self.triangles[(previous_move_position + previous_move_stone_value) % 12],
        }
        legal_positions_list = list(possible_triangles)
        list_length = len(legal_positions_list)
        for i in range(list_length):
            triangle = legal_positions_list[i]
            if triangle.is_free():
                legal_positions_set.add(triangle)
            else:
                stone = triangle.get_stone()
                stone_color = stone.get_color()
                if stone_color == player_color:
                    legal_positions_set.add(triangle)
        return legal_positions_set

    def calculate_range_removed_old_stone(
        self, previous_move_position: int, old_stone_color: str
    ) -> set[Triangle]:
        legal_positions = set()
        for i in range(1, 12):
            possible_triangles = [
                self.triangles[(previous_move_position - i) % 12],
                self.triangles[(previous_move_position + i) % 12]
            ]
            for triangle in possible_triangles:
                if not triangle.is_free():
                    stone = triangle.get_stone()
                    stone_color = stone.get_color()
                    if stone_color != old_stone_color:
                        legal_positions.add(triangle)
            if len(legal_positions) > 0:
                return legal_positions
        return legal_positions

    def calculate_range_inserted_old_stone(
        self, previous_move_position: int
    ) -> set[Triangle]:
        legal_positions = set()
        for i in range(1, 12):
            possible_triangles = [
                self.triangles[(previous_move_position - i) % 12],
                self.triangles[(previous_move_position + i) % 12]
            ]
            for triangle in possible_triangles:
                if triangle.is_free():
                    legal_positions.add(triangle)
            if len(legal_positions) > 0:
                return legal_positions
        return legal_positions

    def set_last_opponent_move_info(self, stone_value_involved: int, position_involved: int, move_type: MoveType) -> None:
        self.last_opponent_move_info = (stone_value_involved, position_involved, move_type)

    def get_last_opponent_move_type(self) -> MoveType:
        return self.last_opponent_move_info[2]

    def get_last_opponent_move_position(self) -> int:
        return int(self.last_opponent_move_info[1])

    def get_last_opponent_move_stone_value(self) -> int:
        return int(self.last_opponent_move_info[0])

    def set_selected_stone_info(self, selected_stone_info: tuple[Stone, bool] | None) -> None:
        self.selected_stone_info = selected_stone_info

    def stone_selected(self, stone_value: int, in_left: bool) -> None:
        selected_stone = self.local_player.get_stone(stone_value, in_left)
        self.set_selected_stone_info((selected_stone, in_left))

    def there_was_a_previous_move(self) -> bool:
        if self.last_opponent_move_info is None:
            return False
        else:
            return True

    def user_already_selected_a_stone(self) -> bool:
        if self.selected_stone_info is None:
            return False
        else:
            return True

    def is_first_local_player_move(self) -> bool:
        if self.move_to_send == {}:
            return True
        else:
            return False

    def reset_move_signature(self) -> None:
        self.move_to_send = {}

    def register_move_type_involved(self, move_type: MoveType) -> None:
        self.move_to_send["move_type"] = move_type.name

    def register_position_involved(self, position_involved: int) -> None:
        self.move_to_send["triangle_index"] = str(position_involved)

    def register_stone_value_involved(self, stone_value_involved: int) -> None:
        self.move_to_send["stone_value"] = str(stone_value_involved)

    def register_in_left(self, in_left: bool) -> None:
        self.move_to_send["in_left"] = str(in_left)

    # TODO: marcar como modelagem de algoritmo
    def register_game_over(self, is_game_over: bool) -> None:
        if is_game_over:
            self.move_to_send["match_status"] = "finished"
        else:
            self.move_to_send["match_status"] = "next"

    def get_last_local_player_move_type(self) -> MoveType:
        return MoveType[self.move_to_send["move_type"]]

    def get_last_local_player_move_position(self) -> int:
        return int(self.move_to_send["triangle_index"])

    def get_last_local_player_move_stone_value(self) -> int:
        return int(self.move_to_send["stone_value"])

    def get_move_to_send(self) -> dict[str, str]:
        return self.move_to_send

    def set_is_legal_move(self, is_legal_move: bool) -> None:
        self.is_legal_move = is_legal_move

    def get_is_legal_move(self) -> bool:
        return self.is_legal_move

    def is_selected_position_legal(
        self, selected_position_index: int, legal_positions: set[Triangle]
    ) -> bool:
        legal_positions_list = list(legal_positions)
        list_length = len(legal_positions_list)
        for i in range(list_length):
            legal_position = legal_positions_list[i]
            position_index = legal_position.get_index()
            if selected_position_index == position_index:
                return True
        return False

    def is_stone_of_given_color_in_selected_position(self, selected_position_index: int, color: str) -> bool:
        stone_in_triangle = self.get_stone_in_position(selected_position_index)
        if stone_in_triangle is not None:
            stone_in_triangle_color = stone_in_triangle.get_color()
            if stone_in_triangle_color == color:
                return True
            else:
                return False
        else:
            return False

    def calculate_legal_opponent_moves(self) -> set[Triangle]:
        local_player_color = self.local_player.get_color()
        remote_player_color = self.remote_player.get_color()

        stone_value_involved = self.get_last_local_player_move_stone_value()
        move_type_involved = self.get_last_local_player_move_type()
        move_position_involved = self.get_last_local_player_move_position()
        if stone_value_involved == 0:
            if move_type_involved == MoveType.INSERT:
                return self.calculate_range_inserted_old_stone(move_position_involved)
            else:
                return self.calculate_range_removed_old_stone(move_position_involved, local_player_color)
        else:
            return self.calculate_range(stone_value_involved, move_position_involved, remote_player_color)

    def there_are_legal_opponent_moves(self, legal_opponent_moves: set[Triangle]) -> bool:
        if len(legal_opponent_moves) == 0:
            return False
        else:
            return True

    def perform_stone_insertion(self, selected_position_index: int, selected_stone_value: int) -> None:
        self.reset_move_signature()
        self.register_position_involved(selected_position_index)
        self.register_stone_value_involved(selected_stone_value)
        self.register_move_type_involved(MoveType.INSERT)
        is_selected_stone_in_left = self.is_selected_stone_in_left()
        self.register_in_left(is_selected_stone_in_left)
        selected_stone = self.get_selected_stone()
        self.insert_stone(selected_stone, selected_position_index)
        self.local_player.remove_stone(selected_stone)
        self.set_selected_stone_info(None)
        self.set_is_legal_move(True)

    def get_value_of_stone_in_selected_position(self, selected_position_index: int) -> int:
        stone_in_selected_position = self.get_stone_in_position(selected_position_index)
        return stone_in_selected_position.get_value()

    def set_removed_stone(self, removed_stone: Stone | None) -> None:
        self.removed_stone = removed_stone

    def get_removed_stone(self) -> Stone:
        return self.removed_stone

    def perform_stone_remotion(self, selected_position_index: int) -> None:
        self.reset_move_signature()
        stone_in_selected_position_value = self.get_value_of_stone_in_selected_position(selected_position_index)
        self.register_position_involved(selected_position_index)
        self.register_stone_value_involved(stone_in_selected_position_value)
        self.register_move_type_involved(MoveType.REMOVE)
        removed_stone = self.remove_stone_from_position(selected_position_index)
        self.remote_player.insert_stone(removed_stone, False)
        self.set_removed_stone(removed_stone)
        self.set_is_legal_move(True)

    # TODO: fazer modelagem de algoritmo
    def get_number_of_stones_on_board_with_value(self, selected_stone_value: int) -> int:
        counter = 0
        for i in range(12):
            if not self.triangles[i].is_free() and self.triangles[i].get_stone().get_value() == selected_stone_value:
                counter += 1
        return counter

    def execute_stone_insertion(self, selected_position_index: int) -> None:
        user_already_selected_a_stone = self.user_already_selected_a_stone()
        if user_already_selected_a_stone:
            selected_stone = self.get_selected_stone()
            selected_stone_value = selected_stone.get_value()
            number_of_stones_on_board_with_value = self.get_number_of_stones_on_board_with_value(selected_stone_value)
            if number_of_stones_on_board_with_value < 2:
                is_first_local_player_move = self.is_first_local_player_move()
                if not is_first_local_player_move:
                    last_local_player_move_type = self.get_last_local_player_move_type()
                    last_local_player_move_position = self.get_last_local_player_move_position()
                    last_local_player_move_stone_value = self.get_last_local_player_move_stone_value()
                    if not (last_local_player_move_type == MoveType.REMOVE
                            and last_local_player_move_position == selected_position_index
                            and last_local_player_move_stone_value == selected_stone_value):
                        self.perform_stone_insertion(selected_position_index, selected_stone_value)
                    else:
                        self.set_is_legal_move(False)
                else:
                    self.perform_stone_insertion(selected_position_index, selected_stone_value)
            else:
                self.set_is_legal_move(False)
        else: 
            self.set_is_legal_move(False)

    def position_selected(self, selected_position_index: int) -> None:
        local_player_color = self.local_player.get_color()
        remote_player_color = self.remote_player.get_color()

        there_was_a_previous_move = self.there_was_a_previous_move()
        if there_was_a_previous_move:
            previous_move_position = self.get_last_opponent_move_position()
            previous_move_stone_value = self.get_last_opponent_move_stone_value()
            if previous_move_stone_value == 0:
                previous_move_type = self.get_last_opponent_move_type()
                if previous_move_type == MoveType.INSERT:
                    legal_positions = self.calculate_range_inserted_old_stone(previous_move_position)
                    is_selected_position_legal = self.is_selected_position_legal(selected_position_index, legal_positions)
                    if is_selected_position_legal:
                        self.execute_stone_insertion(selected_position_index)
                    else:
                        self.set_is_legal_move(False)
                else:
                    legal_positions = self.calculate_range_removed_old_stone(previous_move_position, remote_player_color)
                    is_selected_position_legal = self.is_selected_position_legal(selected_position_index, legal_positions)
                    if is_selected_position_legal:
                        self.perform_stone_remotion(selected_position_index)
                    else:
                        self.set_is_legal_move(False)
            else:
                legal_positions = self.calculate_range(previous_move_stone_value, previous_move_position, local_player_color)
                is_selected_position_legal = self.is_selected_position_legal(selected_position_index, legal_positions)
                if is_selected_position_legal:
                    is_local_player_stone_in_selected_position = self.is_stone_of_given_color_in_selected_position(selected_position_index, local_player_color)
                    if not is_local_player_stone_in_selected_position:
                        self.execute_stone_insertion(selected_position_index)
                    else:
                        self.perform_stone_remotion(selected_position_index)
                else:
                    self.set_is_legal_move(False)
        else:
            self.execute_stone_insertion(selected_position_index)

    def verify_game_over(self) -> None:
        self.local_player.toggle_turn()
        legal_opponent_moves = self.calculate_legal_opponent_moves()
        there_are_legal_opponent_moves = self.there_are_legal_opponent_moves(legal_opponent_moves)
        if not there_are_legal_opponent_moves:
            self.register_game_over(True)
            self.local_player.set_winner()
            self.set_game_state(GameState.GAME_OVER)
        else:
            self.register_game_over(False)
            self.remote_player.toggle_turn()
            self.set_game_state(GameState.REMOTE_PLAYER_TO_MOVE)

    def insert_stone(self, stone: Stone, selected_position_index: int) -> None:
        self.triangles[selected_position_index].insert_stone(stone)

    def remove_stone_from_position(self, selected_position_index: int) -> Stone:
        removed_stone = self.triangles[selected_position_index].remove_stone()
        return removed_stone

    def get_stone_in_position(self, position: int) -> Stone:
        return self.triangles[position].get_stone()

    def get_received_move_type(self, a_move: dict[str, str]) -> MoveType:
        return MoveType[a_move["move_type"]]

    def verify_if_is_game_over(self, a_move: dict[str, str]) -> bool:
        if a_move["match_status"] == "finished":
            return True
        else:
            return False

    def receive_move(self, a_move: dict[str, str]) -> None:
        received_move_type = self.get_received_move_type(a_move)
        if received_move_type == MoveType.INSERT:
            stone = self.remote_player.get_stone(int(a_move["stone_value"]), bool(a_move["in_left"]))
            self.remote_player.remove_stone(stone)
            self.insert_stone(stone, int(a_move["triangle_index"]))
            self.set_last_opponent_move_info(int(a_move["stone_value"]), int(a_move["triangle_index"]), MoveType.INSERT)
        else:
            stone = self.remove_stone_from_position(int(a_move["triangle_index"]))
            self.set_border_stone_info((stone, int(a_move["triangle_index"])))
            self.remote_player.insert_stone(stone, False)
            self.set_last_opponent_move_info(int(a_move["stone_value"]), int(a_move["triangle_index"]), MoveType.REMOVE)
        is_game_over = self.verify_if_is_game_over(a_move)
        if is_game_over:
            self.remote_player.set_winner()
            self.set_game_state(GameState.GAME_OVER)
        else:
            self.remote_player.toggle_turn()
            self.local_player.toggle_turn()
            self.set_game_state(GameState.LOCAL_PLAYER_TO_MOVE)

    def receive_withdrawal_notification(self) -> None:
        self.game_state = GameState.ABANDONED_BY_OTHER_PLAYER

    def reset_move_related_attributes(self) -> None:
        self.last_opponent_move_info = None
        self.selected_stone_info = None
        self.is_legal_move = None
        self.border_stone_info = None
        self.removed_stone = None

    def remove_stones_from_triangles(self) -> None:
        for i in range(12):
            self.triangles[i].reset()

    def verify_if_local_player_starts(self, local_player_order: str) -> bool:
        if local_player_order == "1":
            return True
        else:
            return False

    def start_match(self, players: list[list[str]]) -> None:
        self.reset_move_related_attributes()
        self.remove_stones_from_triangles()

        self.local_player.reset()
        self.remote_player.reset()

        local_player_starts = self.verify_if_local_player_starts(players[0][2])
        if local_player_starts:
            self.local_player.set_color(COLOR_A)
            self.remote_player.set_color(COLOR_B)
            self.local_player.toggle_turn()
        else:
            self.local_player.set_color(COLOR_B)
            self.remote_player.set_color(COLOR_A)
            self.remote_player.toggle_turn()

        self.local_player.update(players[0][0], players[0][1])
        self.remote_player.update(players[1][0], players[1][1])

    def get_game_state(self) -> GameState:
        return self.game_state

    def set_game_state(self, new_game_state: GameState) -> None:
        self.game_state = new_game_state
