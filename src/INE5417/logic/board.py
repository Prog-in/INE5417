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
        self.previous_move_info: None | tuple[MoveType, int, int] = None
        self.selected_stone: Stone | None = None
        self.move_to_send: dict[str, str] = {}
        self.move_type: MoveType | None = None
        self.triangles: list[Triangle] = []
        for i in range(12):
            self.triangles.append(Triangle(i))

    def get_players_colors(self) -> tuple[str, str]:
        return self.local_player.get_color(), self.remote_player.get_color()

    def calculate_range(
        self, previous_move_stone_value: int, previous_move_position: int
    ) -> set[Triangle]:
        return {
            self.triangles[(previous_move_position - previous_move_stone_value) % 12],
            self.triangles[(previous_move_position + previous_move_stone_value) % 12],
        }

    def calculate_range_removed_old_stone(
        self, previous_move_position: int
    ) -> set[Triangle]:
        valid_positions = set()
        for i in range(1, 12):
            left = self.triangles[(previous_move_position - i) % 12]
            right = self.triangles[(previous_move_position + i) % 12]
            if not left.is_free():
                stone = left.get_stone()
                stone_color = stone.get_color()
                if stone_color == self.local_player.get_color():
                    valid_positions.add(left)
            if not right.is_free():
                stone = right.get_stone()
                stone_color = stone.get_color()
                if stone_color == self.local_player.get_color():
                    valid_positions.add(right)
            if len(valid_positions) > 0:
                break
        return valid_positions

    def calculate_range_inserted_old_stone(
        self, previous_move_position: int
    ) -> set[Triangle]:
        valid_positions = set()
        for i in range(1, 12):
            left = self.triangles[(previous_move_position - i) % 12]
            right = self.triangles[(previous_move_position + i) % 12]
            if left.is_free():
                valid_positions.add(left)
            if right.is_free():
                valid_positions.add(right)
            if len(valid_positions) > 0:
                break
        return valid_positions

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
        stone_value = self.last_move_info[0].get_value()
        position_index = self.last_move_info[1].get_index()
        candidate_moves = self.calculate_range(stone_value, position_index)
        valid_triangles = self.generate_valid_triangles(candidate_moves)
        return valid_triangles

    def update_move_info(self, selected_triangle: Triangle):
        self.last_move_info = (self.selected_stone, selected_triangle)
        self.selected_stone = None

    def set_selected_stone(self, selected_stone: Stone) -> None:
        self.selected_stone = selected_stone

    def stone_selected(self, stone_value: int, in_left: bool) -> None:
        selected_stone = self.local_player.get_stone(stone_value, in_left)
        self.set_selected_stone(selected_stone)

    def there_was_a_previous_move(self) -> bool:
        if self.last_move_info is None:
            return False
        else:
            return True

    def user_already_selected_a_stone(self) -> bool:
        if self.selected_stone is None:
            return False
        else:
            return True

    def get_is_first_local_player_move(self) -> bool:
        if self.move_type is None:
            return False
        else:
            return True

    def get_previous_move_type(self) -> MoveType:
        return self.previous_move_info[0]

    def get_previous_move_position(self) -> int:
        return self.previous_move_info[1]

    def get_previous_move_stone_value(self) -> int:
        return self.previous_move_info[2]

    def get_selected_stone(self) -> Stone | None:
        return self.selected_stone

    def register_move_type_involved(self, move_type: MoveType) -> None:
        self.move_to_send["move_type"] = move_type.name

    def register_position_involved(self, position_involved: int) -> None:
        self.move_to_send["triangle_index"] = str(position_involved)

    def register_stone_value_involved(self, stone_value_involved: int) -> None:
        self.move_to_send["stone_value"] = str(stone_value_involved)

    def register_game_over(self) -> None:
        self.move_to_send["game_over"] = "1"

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

    def is_selected_position_valid(
        self, selected_position_index: int, valid_positions: set[Triangle]
    ) -> bool:
        is_valid = False
        for valid_position in valid_positions:
            position_index = valid_position.get_index()
            if selected_position_index == position_index:
                is_valid = True
                break
        return is_valid

    def calculate_valid_opponent_moves(self) -> list[Triangle]:
        ...

    def there_are_valid_opponent_moves(self, valid_opponent_moves: list[Triangle]) -> bool:
        if len(valid_opponent_moves) == 0:
            return False
        else:
            return True

    def set_move_type(self, move_type: MoveType) -> None:
        self.move_type = move_type

    def get_move_type(self) -> MoveType:
        return self.move_type

    def position_selected(self, selected_position_index: int) -> None:
        there_was_a_previous_move = self.there_was_a_previous_move()
        if there_was_a_previous_move:
            previous_move_position = self.get_previous_move_position()
            previous_move_stone_value = self.get_previous_move_stone_value()
            if previous_move_stone_value == 0:
                previous_move_type = self.get_previous_move_type()
                if previous_move_type == MoveType.INSERT:
                    valid_positions = self.calculate_range_inserted_old_stone(
                        previous_move_position
                    )
                    is_valid = self.is_selected_position_valid(
                        selected_position_index, valid_positions
                    )
                    if is_valid:
                        # verificar se o usuário já selecionou uma pedra
                        ...
                    else:
                        self.set_is_legal_move(False)
                        return
                else:  # previous_move_type != MoveType.INSERT
                    valid_positions = self.calculate_range_removed_old_stone(
                        previous_move_position
                    )
                    is_valid = self.is_selected_position_valid(
                        selected_position_index, valid_positions
                    )
                    if is_valid:
                        ...
                    else:
                        self.set_is_legal_move(False)
                        return
            else:  # previous_move_stone_value != 0
                valid_positions = self.calculate_range(
                    previous_move_stone_value, previous_move_position
                )
                is_valid = self.is_selected_position_valid(
                    selected_position_index, valid_positions
                )
                if is_valid:
                    ...
                else:
                    self.set_is_legal_move(False)
                    return
        else:  # primeiro lance
            user_already_selected_a_stone = self.user_already_selected_a_stone()
            if user_already_selected_a_stone:
                is_first_local_player_move = self.get_is_first_local_player_move()
                if is_first_local_player_move:
                    self.set_move_type(MoveType.INSERT)
                    self.set_is_legal_move(True)
                    self.insert_stone(self.selected_stone, selected_position_index)
                    self.local_player.remove_stone(self.selected_stone)
                else:
                    last_local_player_move_type = self.get_last_local_player_move_type()
                    if last_local_player_move_type == MoveType.REMOVE:
                        last_local_player_move_position = (
                            self.get_last_local_player_move_position()
                        )
                        if last_local_player_move_position == selected_position_index:
                            last_local_player_move_stone_value = (
                                self.get_last_local_player_move_stone_value()
                            )
                            if (
                                last_local_player_move_stone_value
                                == self.get_selected_stone().get_value()
                            ):
                                self.set_is_legal_move(False)
                                return
                            else:
                                self.set_move_type(MoveType.INSERT)
                                self.insert_stone(self.selected_stone, selected_position_index)
                                self.local_player.remove_stone(self.selected_stone)
                        else:
                            self.set_move_type(MoveType.INSERT)
                            self.insert_stone(self.selected_stone, selected_position_index)
                            self.local_player.remove_stone(self.selected_stone)
                    else:  # last_local_player_move_type != MoveType.REMOVE
                        self.set_move_type(MoveType.INSERT)
                        self.insert_stone(self.selected_stone, selected_position_index)
                        self.local_player.remove_stone(self.selected_stone)
            else:  # not user_already_selected_a_stone
                self.set_is_legal_move(False)
                return
        self.register_position_involved(selected_position_index)
        selected_stone_value = self.selected_stone.get_value()
        self.register_stone_value_involved(selected_stone_value)
        self.register_move_type_involved(self.move_type)
        self.local_player.toggle_turn()
        valid_opponent_moves = self.calculate_valid_opponent_moves()
        there_are_opponent_moves = self.there_are_valid_opponent_moves(valid_opponent_moves)
        if there_are_opponent_moves:
            self.remote_player.toggle_turn()
            self.set_game_state(GameState.REMOTE_PLAYER_TO_MOVE)
        else:
            self.local_player.set_winner()
            self.set_game_state(GameState.MATCH_ENDED)

    def insert_stone(self, stone: Stone, selected_position_index: int) -> None:
        self.triangles[selected_position_index].insert_stone(stone)
        self.selected_stone.set_on_board(True)

    def remove_stone(self, selected_position_index: int) -> Stone:
        removed_stone = self.triangles[selected_position_index].remove_stone()
        removed_stone.set_on_board(False)
        return removed_stone

    def get_received_move_type(self, a_move) -> MoveType:
        return MoveType[a_move[0]]

    def receive_move(self, a_move):
        received_move_type = self.get_received_move_type(a_move)
        if received_move_type == MoveType.INSERT:
            ...
        else:
            ...

    def receive_withdrawal_notification(self):
        self.game_state = GameState.ABANDONED_BY_OTHER_PLAYER

    def reset_move_related_attributes(self) -> None:
        self.last_move_info = None
        self.selected_stone = None

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

        self.local_player.update(players[0][0], players[0][1])
        self.remote_player.update(players[1][0], players[1][1])

        local_player_starts = self.verify_if_local_player_starts(players[0][2])
        if local_player_starts:
            self.local_player.set_color(COLOR_A)
            self.remote_player.set_color(COLOR_B)
            self.local_player.toggle_turn()
        else:
            self.local_player.set_color(COLOR_B)
            self.remote_player.set_color(COLOR_A)
            self.remote_player.toggle_turn()

    def get_game_state(self) -> GameState:
        return self.game_state

    def set_game_state(self, new_game_state: GameState) -> None:
        self.game_state = new_game_state

    def get_turn_player(self) -> Player:
        local_player_turn = self.local_player.get_turn()
        if local_player_turn:
            player = self.local_player
        else:
            player = self.remote_player
        self.local_player.toggle_turn()
        self.remote_player.toggle_turn()
        return player
