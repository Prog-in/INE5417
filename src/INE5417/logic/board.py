from .player import Player
from .stone import Stone
from .triangle import Triangle
from ..utils.game_state import GameState
from ..utils.move_type import MoveType


class Board:
    def __init__(self) -> None:
        # deve ser fixo pois, no caso de variável, deveria haver uma comunicação entre as instâncias do jogo
        # para acertar qual cor cada jogador usaria.
        self.local_player: Player = Player()
        self.remote_player: Player = Player()
        self.game_state: GameState = self.get_title_state()
        self.triangles: list[Triangle] = self.initialize_triangles()
        self.previous_move_info: None | tuple[MoveType, int, int] = None
        self.last_local_player_move_info: None | tuple[MoveType, int, int] = None
        self.selected_stone: Stone | None = None

    def get_title_state(self) -> GameState:
        return GameState.TITLE

    def initialize_triangles(self) -> list[Triangle]:
        triangles = []
        for i in range(12):
            triangles.append(Triangle(i))
        return triangles

    def get_players_colors(self) -> tuple[str, str]:
        return self.local_player.get_color(), self.remote_player.get_color()

    def reset_game(self):
        self.local_player.reset()
        self.remote_player.reset()

    def calculate_range(self, previous_move_stone_value: int, previous_move_position: int) -> set[Triangle]:
        return {
            self.triangles[(previous_move_position - previous_move_stone_value) % 12],
            self.triangles[(previous_move_position + previous_move_stone_value) % 12],
        }

    def calculate_range_removed_old_stone(self, previous_move_position: int) -> set[Triangle]:
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

    def calculate_range_inserted_old_stone(self, previous_move_position: int) -> set[Triangle]:
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
        candidate_moves = self.calculate_range(self.last_move_info)
        valid_triangles = self.generate_valid_triangles(candidate_moves)
        return valid_triangles

    def update_move_info(self, selected_triangle: Triangle):
        self.last_move_info = (self.selected_stone, selected_triangle)
        self.selected_stone = None

    def stone_selected(self, color: str, stone_value: int, in_left: bool) -> None:
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

    def remove_stone_from_user_inventory(self) -> None:
        ...

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

    def is_selected_position_valid(self, selected_position_index: int, valid_positions: set[Triangle]) -> bool:
        is_valid = False
        for valid_position in valid_positions:
            position_index = valid_position.get_index()
            if selected_position_index == position_index:
                is_valid = True
                break
        return is_valid

    def position_selected(self, selected_position_index: int) -> MoveType:
        there_was_a_previous_move = self.there_was_a_previous_move()
        if not there_was_a_previous_move:
            previous_move_position = self.get_previous_move_position()
            previous_move_stone_value = self.get_previous_move_stone_value()
            if previous_move_stone_value == 0:
                previous_move_type = self.get_previous_move_type()
                if previous_move_type == MoveType.REMOVE:
                    valid_positions = self.calculate_range_removed_old_stone(previous_move_position)
                    is_valid = self.is_selected_position_valid(selected_position_index, valid_positions)
                    if is_valid:
                        ...
                    else:
                        return self.register_irregular_move()
                else:
                    valid_positions = self.calculate_range_inserted_old_stone(previous_move_position)
                    is_valid = self.is_selected_position_valid(selected_position_index, valid_positions)
                    if is_valid:
                        ...
                    else:
                        return self.register_irregular_move()
            else:
                valid_positions = self.calculate_range(previous_move_stone_value, previous_move_position)
                is_valid = self.is_selected_position_valid(selected_position_index, valid_positions)
                if is_valid:
                    ...
                else:
                    return self.register_irregular_move()
        else: # primeiro lance
            user_already_selected_a_stone = self.user_already_selected_a_stone()
            if user_already_selected_a_stone:
                is_first_local_player_move = self.get_is_first_local_player_move()
                if is_first_local_player_move:
                    self.insert_stone(selected_position_index)
                    self.remove_stone_from_user_inventory()
                    # registrar posição envolvida na jogada local + continuação
                else:
                    last_local_player_move_type = self.get_last_local_player_move_type()
                    if last_local_player_move_type == MoveType.REMOVE:
                        last_local_player_move_position = self.get_last_local_player_move_position()
                        if last_local_player_move_position == selected_position_index:
                            last_local_player_move_stone_value = self.get_last_local_player_move_stone_value()
                            if last_local_player_move_stone_value == self.get_selected_stone().get_value():
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
        selected_triangle = self.triangles[selected_position_index]
        selected_triangle.insert_stone(self.selected_stone)
        self.selected_stone.set_on_board(True)

    def remove_stone(self, selected_position_index: int) -> Stone:
        selected_triangle = self.triangles[selected_position_index]
        removed_stone = selected_triangle.remove_stone()
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

    def receive_move(self, a_move):
        if self.game_state == GameState.WAITING_OTHER_PLAYER:
            ...

    def receive_withdrawal_notification(self):
        self.game_state = GameState.ABANDONED_BY_OTHER_PLAYER

    def reset_move_related_fields(self) -> None:
        self.last_move_info = None
        self.selected_stone = None

    def remove_stones_from_triangles(self) -> None:
        for triangle in self.triangles:
            triangle.reset()

    def update_player_instances(
        self,
        local_player_id: str,
        local_player_order: int,
        remote_player_id: str,
        remote_player_order: int,
    ) -> None:
        self.local_player.reset()
        self.remote_player.reset()

        self.local_player.update(local_player_id, local_player_order)
        self.remote_player.update(remote_player_id, remote_player_order)

    def verify_if_local_player_starts(local_player_order: int) -> bool:
        if local_player_order == 1:
            return True
        else:
            return False

    def set_local_player_starts(self) -> None:
        self.game_state = GameState.PLAYER_MOVE_1

    def set_remote_player_starts(self) -> None:
        self.game_state = GameState.WAITING_OTHER_PLAYER

    def start_match(self, players: list[list[str]]) -> None:
        player_a_name = players[0][0]
        player_a_id = players[0][1]
        player_a_order = int(players[0][2])
        player_b_name = players[1][0]
        player_b_id = players[1][1]
        player_b_order = int(players[1][2])

        self.reset_move_related_fields()
        self.remove_stones_from_triangles()
        self.update_player_instances(
            player_a_id, player_a_order, player_b_id, player_b_order
        )
        local_player_starts = self.verify_if_local_player_starts()
        if local_player_starts:
            self.set_local_player_starts()
        else:
            self.set_remote_player_starts()

    def get_game_state(self) -> GameState:
        return self.game_state

    def get_turn_player(self) -> Player:
        local_player_turn = self.local_player.get_turn()
        if local_player_turn:
            player = self.local_player
        else:
            player = self.remote_player
        self.local_player.toggle_turn()
        self.remote_player.toggle_turn()
        return player
