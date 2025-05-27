import tkinter as tk
from tkinter import ttk, messagebox

from ..logic.board import Board
from ..logic.player import Player
from ..utils.constants import BOARD_WIDTH, BOARD_HEIGHT
from ..utils.game_state import GameState
from ..utils.move_type import MoveType


class GameInterface:
    def __init__(
            self, root: tk.Tk, assets: dict[str, tk.PhotoImage], player_interface
    ) -> None:
        self.board: Board = Board()
        self.canvas_board: tk.Canvas | None = None
        self.stone_buttons: dict[str, tk.Button] = dict()
        self.pressed_button: tk.Button | None = None
        self.local_player_buttons_of_stones_in_board: list[tuple[int, tk.Button]] = []
        self.remote_player_buttons_of_stones_in_board: list[tuple[int, tk.Button]] = []
        self.root: tk.Tk = root
        self.assets: dict[str, tk.PhotoImage] = assets
        self.player_interface = player_interface
        self.frame: ttk.Frame | None = None

    def get_frame(self) -> ttk.Frame:
        return self.frame

    def get_game_state(self) -> GameState:
        return self.board.get_game_state()

    def set_game_state(self, new_game_state: GameState) -> None:
        self.board.set_game_state(new_game_state)

    def initialize_player_stone_frame(
            self, player_color: str, parent_widget: tk.Widget, is_local: bool, text: str
    ) -> ttk.Frame:
        player_stones_frame = ttk.Frame(parent_widget, relief=tk.SOLID, borderwidth=2)
        text_label = ttk.Label(player_stones_frame, text=text)
        text_label.grid(column=0, row=0, columnspan=2, pady=1)

        for i in range(6):
            button_stone_1 = tk.Button(
                player_stones_frame,
                image=self.assets[f"{player_color}{i}"],
                state=tk.DISABLED,
                relief="flat",
            )
            button_stone_2 = tk.Button(
                player_stones_frame,
                image=self.assets[f"{player_color}{i}"],
                state=tk.DISABLED,
                relief="flat",
            )
            if is_local:
                button_stone_1.configure(state=tk.NORMAL)
                button_stone_2.configure(state=tk.NORMAL)
                button_stone_1.bind("<Button-1>",
                                    lambda event, stone=button_stone_1, index=i, in_left=True: self.stone_selected(
                                        stone, index, in_left))
                button_stone_2.bind("<Button-1>",
                                    lambda event, stone=button_stone_2, index=i, in_left=False: self.stone_selected(
                                        stone, index, in_left))
            self.stone_buttons[player_color + str(i) + ".1"] = button_stone_1
            self.stone_buttons[player_color + str(i) + ".2"] = button_stone_2
            button_stone_1.grid(row=i + 1, column=0, padx=0, pady=0)
            button_stone_2.grid(row=i + 1, column=1, padx=0, pady=0)

        return player_stones_frame

    def initialize_frame(self) -> None:
        self.frame = ttk.Frame(self.root)

        self.canvas_board = tk.Canvas(
            self.frame, width=BOARD_WIDTH, height=BOARD_HEIGHT
        )
        self.canvas_board.create_image(
            BOARD_WIDTH // 2,
            BOARD_HEIGHT // (2 - 0.15),
            image=self.assets["board"],
            tags="board",
        )
        positions_coordinates = (
            (320, 100),
            (420, 130),
            (480, 195),
            (490, 275),
            (450, 350),
            (360, 400),
            (265, 410),
            (170, 380),
            (105, 315),
            (90, 230),
            (135, 155),
            (220, 105),
        )
        for i in range(12):
            x, y = positions_coordinates[i]
            button_triangle = self.canvas_board.create_image(
                x, y, image=self.assets["circle"], state=tk.NORMAL, tags=f"circle{i}"
            )
            self.canvas_board.tag_bind(
                button_triangle,
                "<ButtonRelease-1>",
                lambda event, index=i: self.position_selected(index),
            )

        borders_coordinates = (
            (330, 45),
            (455, 85),
            (540, 170),
            (560, 280),
            (510, 375),
            (395, 450),
            (260, 465),
            (135, 425),
            (45, 338),
            (30, 220),
            (75, 125),
            (185, 60),
        )
        for i in range(12):
            x, y = borders_coordinates[i]
            self.canvas_board.create_image(
                x, y, state=tk.HIDDEN, tags=f"border{i}"
            )

        local_player_color = self.board.get_local_player_color()
        remote_player_color = self.board.get_remote_player_color()

        local_player_stones_frame = self.initialize_player_stone_frame(
            local_player_color, self.frame, True, "Peças do jogador local"
        )
        remote_player_stones_frame = self.initialize_player_stone_frame(
            remote_player_color, self.frame, False, "Peças do jogador remoto"
        )

        local_player_stones_frame.grid(row=0, column=0)
        self.canvas_board.grid(row=0, column=1, sticky=tk.NS)
        remote_player_stones_frame.grid(row=0, column=2)

    def start_match(self, players: list[list[str]]) -> None:
        self.board.start_match(players)

    def receive_move(self, a_move: dict[str, str]) -> None:
        if self.board.is_stone_in_border():
            position = self.board.get_stone_in_border_position()
            self.canvas_board.itemconfig(f"circle{position}", state=tk.NORMAL, image=self.assets["circle"])
            self.canvas_board.itemconfig(f"border{position}", state=tk.HIDDEN)
        self.board.receive_move(a_move)

    def update_widgets_images(self, assets: dict[str, tk.PhotoImage]) -> None:
        self.assets = assets
        for button_name, stone_button in self.stone_buttons.items():
            asset_name = button_name[:-2]
            stone_button.configure(image=self.assets[asset_name])
            stone_button.update()
        for i in range(12):
            self.canvas_board.itemconfig("circle" + str(i), image=self.assets["circle"])
        self.canvas_board.itemconfig("board", image=self.assets["board"])

    def get_leftmost_stone_button(self, stone_color: str, stone_value: int) -> ttk.Button:
        return self.stone_buttons[stone_color + str(stone_value) + ".1"]

    def get_rightmost_stone_button(self, stone_color: str, stone_value: int) -> ttk.Button:
        return self.stone_buttons[stone_color + str(stone_value) + ".2"]

    def identify_stone_button(self, stone_color: str, stone_value: int, in_left: bool, state: str) -> ttk.Button:
        if in_left:
            stone_button = self.get_leftmost_stone_button(stone_color, stone_value)
            if stone_button.cget("state") == state:
                return stone_button
            else:
                stone_button = self.get_rightmost_stone_button(stone_color, stone_value)
                return stone_button
        else:
            stone_button = self.get_rightmost_stone_button(stone_color, stone_value)
            if stone_button.cget("state") == state:
                return stone_button
            else:
                stone_button = self.get_leftmost_stone_button(stone_color, stone_value)
                return stone_button

    def pop_stone_button_from_board(self, is_local_move: bool, stone_button_value: int) -> tk.Button:
        if is_local_move:
            collection = self.local_player_buttons_of_stones_in_board
        else:
            collection = self.remote_player_buttons_of_stones_in_board
        for info in collection:
            if info[0] == stone_button_value:
                collection.remove(info)
                return info[1]

    def update_stone_state(
            self, stone_color: str, stone_value: int, in_left: bool, state: str
    ) -> None:
        stone_button = self.identify_stone_button(stone_color, stone_value, in_left, state)
        stone_button.configure(state=state)
        stone_button.update()

    def update_stones_state(self, state: str):
        for button in self.stone_buttons.values():
            button.configure(state=state)
            button.update()

    def set_pressed_button(self, button: tk.Button | None) -> None:
        self.pressed_button = button

    def stone_selected(self, pressed_button: ttk.Button, stone_value: int, in_left: bool) -> None:
        if self.pressed_button is not None:
            self.pressed_button.configure(background="#d9d9d9")
        self.set_pressed_button(pressed_button)
        self.pressed_button.configure(background="yellow")
        game_state = self.get_game_state()
        if game_state == GameState.LOCAL_PLAYER_TO_MOVE:
            self.board.stone_selected(stone_value, in_left)

    def position_selected(self, position_id: int) -> None:
        game_state = self.get_game_state()
        if game_state == GameState.LOCAL_PLAYER_TO_MOVE:
            self.set_pressed_button(None)
            self.board.position_selected(position_id)
            game_state = self.get_game_state()
            if game_state == GameState.GAME_OVER or game_state == GameState.REMOTE_PLAYER_TO_MOVE:
                self.board.set_is_legal_move(True)
                move_to_send = self.board.get_move_to_send()
                # TODO: ler mais sobre "match_status" no DOG
                move_to_send["match_status"] = "next"
                self.update_board(move_to_send, True)
                self.player_interface.send_move(move_to_send)
                self.player_interface.update_gui()
            else:
                self.board.set_is_legal_move(False)
                messagebox.showinfo(message="Jogada inválida. Tente novamente")

    def get_move_type_from_move(self, move: dict[str, str]) -> MoveType:
        return MoveType[move["move_type"]]

    def identify_stone_value_from_move(self, move: dict[str, str]) -> int:
        return int(move["stone_value"])

    def identify_position_from_move(self, move: dict[str, str]) -> int:
        return int(move["triangle_index"])

    def identify_in_left_from_move(self, move: dict[str, str]) -> bool:
        if move["in_left"] == "True":
            return True
        else:
            return False

    def update_board(self, move: dict[str, str], is_local_move: bool) -> None:
        stone_value = self.identify_stone_value_from_move(move)
        if is_local_move:
            stone_color = self.board.get_local_player_color()
        else:
            stone_color = self.board.get_remote_player_color()
        position = self.identify_position_from_move(move)
        in_left = self.identify_in_left_from_move(move)

        is_stone_in_border = self.board.is_stone_in_border()
        if is_stone_in_border:
            stone_in_border = self.board.get_stone_in_border()
            stone_in_border_color = stone_in_border.get_color()
            remote_player_color = self.board.get_remote_player_color()
            if stone_in_border_color == remote_player_color:
                stone_in_border_position = self.board.get_stone_in_border_position()
                self.canvas_board.itemconfig(f"circle{stone_in_border_position}", state=tk.NORMAL, image=self.assets["circle"])
                self.canvas_board.itemconfig(f"border{stone_in_border_position}", state=tk.HIDDEN)

        move_type = self.get_move_type_from_move(move)
        if move_type == MoveType.INSERT:
            if is_local_move:
                stone_button = self.identify_stone_button(stone_color, stone_value, in_left, tk.NORMAL)
                self.local_player_buttons_of_stones_in_board.append((stone_value, stone_button))
            else:
                stone_button = self.identify_stone_button(stone_color, stone_value, in_left, tk.DISABLED)
                self.remote_player_buttons_of_stones_in_board.append((stone_value, stone_button))
            stone_button.grid_forget()
            stone_button.update()
            self.canvas_board.itemconfig(f"circle{position}", image=self.assets[stone_color + str(stone_value)])
        else:
            # Colocando pedra do jogador local na borda
            border_stone_button = self.pop_stone_button_from_board(is_local_move, int(move["stone_value"]))
            border_stone_button.grid(row=int(move["stone_value"]), column=1-in_left)
            border_stone_button.update()
            removed_stone = self.board.get_removed_stone()
            self.board.set_removed_stone(None)
            self.board.set_border_stone_info((removed_stone, position))
            self.canvas_board.itemconfig(f"circle{position}", state=tk.HIDDEN, image=self.assets["circle"])
            self.canvas_board.itemconfig(f"border{position}", state=tk.NORMAL, image=self.assets[stone_color + str(stone_value)])
