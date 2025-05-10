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
        self.previous_move_info: None | tuple[MoveType, int, int] = None
        self.last_local_player_move_info: None | tuple[MoveType, int, int] = None
        self.selected_stone: Stone | None = None
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

    def stone_selected(self, stone_value: int, in_left: bool) -> None:
        self.selected_stone = self.local_player.get_stone(stone_value, in_left)

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
        if self.last_local_player_move_info is None:
            return False
        else:
            return True

    def remove_stone_from_user_inventory(self) -> None: ...

    def get_previous_move_type(self) -> MoveType:
        return self.previous_move_info[0]

    def get_previous_move_position(self) -> int:
        return self.previous_move_info[1]

    def get_previous_move_stone_value(self) -> int:
        return self.previous_move_info[2]

    def get_last_local_player_move_type(self) -> MoveType:
        return self.last_local_player_move_info[0]

    def get_last_local_player_move_position(self) -> int:
        return self.last_local_player_move_info[1]

    def get_last_local_player_move_stone_value(self) -> int:
        return self.last_local_player_move_info[2]

    def get_selected_stone(self) -> Stone | None:
        return self.selected_stone

    def register_irregular_move(self) -> MoveType:
        return MoveType.ASK_AGAIN

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

    def set_move_type(self, move_type: MoveType) -> None:
        self.move_type = move_type

    def get_move_type(self) -> MoveType:
        return self.move_type

    def position_selected(self, selected_position_index: int) -> MoveType:
        there_was_a_previous_move = self.there_was_a_previous_move()
        if not there_was_a_previous_move:
            previous_move_position = self.get_previous_move_position()
            previous_move_stone_value = self.get_previous_move_stone_value()
            if previous_move_stone_value == 0:
                previous_move_type = self.get_previous_move_type()
                if previous_move_type == MoveType.REMOVE:
                    valid_positions = self.calculate_range_removed_old_stone(
                        previous_move_position
                    )
                    is_valid = self.is_selected_position_valid(
                        selected_position_index, valid_positions
                    )
                    if is_valid:
                        ...
                    else:
                        return self.register_irregular_move()
                else:
                    valid_positions = self.calculate_range_inserted_old_stone(
                        previous_move_position
                    )
                    is_valid = self.is_selected_position_valid(
                        selected_position_index, valid_positions
                    )
                    if is_valid:
                        ...
                    else:
                        return self.register_irregular_move()
            else:
                valid_positions = self.calculate_range(
                    previous_move_stone_value, previous_move_position
                )
                is_valid = self.is_selected_position_valid(
                    selected_position_index, valid_positions
                )
                if is_valid:
                    ...
                else:
                    return self.register_irregular_move()
        else:  # primeiro lance
            user_already_selected_a_stone = self.user_already_selected_a_stone()
            if user_already_selected_a_stone:
                is_first_local_player_move = self.get_is_first_local_player_move()
                if is_first_local_player_move:
                    self.insert_stone(selected_position_index)
                    self.local_player.remove_stone(self.selected_stone)
                    self.remove_stone_from_user_inventory()
                    # registrar posição envolvida na jogada local + continuação
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
                                return self.register_irregular_move()
                            else:
                                self.insert_stone(selected_position_index)
                                self.remove_stone_from_user_inventory()
                                # registrar posição envolvida na jogada local + continuação
                        else:
                            self.insert_stone(selected_position_index)
                            self.remove_stone_from_user_inventory()
                            # registrar posição envolvida na jogada local + continuação
                    else:
                        self.insert_stone(selected_position_index)
                        self.remove_stone_from_user_inventory()
                        # registrar posição envolvida na jogada local + continuação
            else:
                return self.register_irregular_move()

    def decide_move_type(self) -> MoveType:
        if self.selected_stone.get_color() != self.local_player.get_color():
            return MoveType.ASK_AGAIN
        # FIXME(Hélcio): O jogador clica NO TABULEIRO quando ele quer remover
        # uma pedra. Se fode aí pra arrumar.
        if self.selected_stone.get_on_board():
            return MoveType.REMOVE
        counter = 0
        for t in self.triangles:
            if t.get_stone().get_value() == self.selected_stone.get_value():
                counter += 1
        if counter < 2:
            return MoveType.INSERT
        return MoveType.ASK_AGAIN

    def insert_stone(self, selected_position_index: int) -> None:
        self.triangles[selected_position_index].insert_stone(self.selected_stone)
        self.selected_stone.set_on_board(True)

    def remove_stone(self, selected_position_index: int) -> Stone:
        removed_stone = self.triangles[selected_position_index].remove_stone()
        removed_stone.set_on_board(False)
        return removed_stone

    def generate_dog_food(
        self,
        move_type: MoveType,
        triangle_index: int,
        removed_stone: Stone | None,
        you_lost: bool,
    ) -> dict[str, str]:
        move_to_send = {
            "move_type": move_type.value,
            "triangle_index": str(triangle_index),
            "you_lost": str(you_lost),
        }
        if move_type == MoveType.INSERT:
            move_to_send["stone_value"] = str(removed_stone.get_value())
        return move_to_send

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
