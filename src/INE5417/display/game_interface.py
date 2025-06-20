import tkinter as tk
from tkinter import ttk, messagebox

from ..logic.board import Board
from ..utils.constants import BOARD_WIDTH, BOARD_HEIGHT, POSITIONS_COORDINATES, BORDERS_COORDINATES
from ..utils.game_state import GameState
from ..utils.move_type import MoveType


class GameInterface:
    def __init__(
            self, root: tk.Tk, assets: dict[str, tk.PhotoImage], player_interface
    ) -> None:
        self.board: Board = Board()
        self.canvas_board: tk.Canvas | None = None
        self.border_stone_button_info: tuple[int, tk.Button, int] | None = None
        self.stone_buttons: dict[str, tk.Button] = dict()
        self.pressed_button: tk.Button | None = None
        self.local_player_buttons_of_stones_in_board: list[tuple[int, tk.Button, int]] = []
        self.remote_player_buttons_of_stones_in_board: list[tuple[int, tk.Button, int]] = []
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

    def set_assets(self, assets: dict[str, tk.PhotoImage]) -> None:
        self.assets = assets

    def set_border_stone_button_info(self, border_stone_button_info: tuple[int, tk.Button, int]) -> None:
        self.border_stone_button_info = border_stone_button_info

    def is_local_player_winner(self) -> bool:
        return self.board.is_local_player_winner()

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
            button_stone_1.grid(row=i+1, column=0, padx=0, pady=0)
            button_stone_2.grid(row=i+1, column=1, padx=0, pady=0)

        return player_stones_frame

    def initialize_frame(self) -> None:
        self.frame = ttk.Frame(self.root)

        self.canvas_board = tk.Canvas(
            self.frame, width=BOARD_WIDTH, height=BOARD_HEIGHT
        )
        self.canvas_board.create_image(
            BOARD_WIDTH // 2,
            BOARD_HEIGHT // 2,
            image=self.assets["board"],
            tags="board",
            )

        for i in range(12):
            button_triangle = self.canvas_board.create_image(
                POSITIONS_COORDINATES[i][0], POSITIONS_COORDINATES[i][1], image=self.assets["circle"], state=tk.NORMAL, tags=f"circle{i}"
            )
            self.canvas_board.tag_bind(
                button_triangle,
                "<ButtonRelease-1>",
                lambda event, index=i: self.position_selected(index),
            )
            self.canvas_board.create_image(
                BORDERS_COORDINATES[i][0], BORDERS_COORDINATES[i][1], state=tk.HIDDEN, tags=f"border{i}"
            )

        local_player_color = self.board.get_local_player_color()
        remote_player_color = self.board.get_remote_player_color()

        local_player_stones_frame = self.initialize_player_stone_frame(
            local_player_color, self.frame, True, "Peças do jogador local"
        )
        remote_player_stones_frame = self.initialize_player_stone_frame(
            remote_player_color, self.frame, False, "Peças do jogador remoto"
        )

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        local_player_stones_frame.grid(row=0, column=0, sticky=tk.E)
        self.canvas_board.grid(row=0, column=1, sticky=tk.NS)
        remote_player_stones_frame.grid(row=0, column=2, sticky=tk.W)

    def start_match(self, players: list[list[str]]) -> None:
        self.board.start_match(players)

    def receive_move(self, a_move: dict[str, str]) -> None:
        is_stone_in_border = self.board.is_stone_in_border()
        if is_stone_in_border:
            position = self.board.get_stone_in_border_position()
            self.canvas_board.itemconfig(f"circle{position}", state=tk.NORMAL, image=self.assets["circle"])
            self.canvas_board.itemconfig(f"border{position}", state=tk.HIDDEN)
            self.grid_border_stone_button()
            self.board.set_border_stone_info(None)
        self.board.receive_move(a_move)

    def update_widgets_images(self, assets: dict[str, tk.PhotoImage]) -> None:
        self.set_assets(assets)
        if self.frame is not None:
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

    def pop_stone_button_from_board(self, is_local_move: bool, stone_button_value: int) -> tuple[int, tk.Button, int]:
        if is_local_move:
            collection = self.local_player_buttons_of_stones_in_board
        else:
            collection = self.remote_player_buttons_of_stones_in_board
        bound = len(collection)
        for i in range(bound):
            if collection[i][0] == stone_button_value:
                button_info = collection[i]
                collection.remove(collection[i])
                return button_info

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

    def was_a_stone_button_pressed(self) -> bool:
        if self.pressed_button is not None:
            return True
        else:
            return False

    def stone_selected(self, pressed_button: ttk.Button, stone_value: int, in_left: bool) -> None:
        game_state = self.get_game_state()
        if game_state == GameState.LOCAL_PLAYER_TO_MOVE:
            was_a_stone_button_pressed = self.was_a_stone_button_pressed()
            if was_a_stone_button_pressed:
                self.pressed_button.configure(background="#d9d9d9")
            self.set_pressed_button(pressed_button)
            self.pressed_button.configure(background="yellow")
            self.board.stone_selected(stone_value, in_left)

    def verify_move_validity(self) -> bool:
        is_legal_move = self.board.get_is_legal_move()
        if is_legal_move:
            self.board.perform_game_over_verification()
            was_a_stone_button_pressed = self.was_a_stone_button_pressed()
            if was_a_stone_button_pressed:
                self.pressed_button.configure(background="#d9d9d9")
                self.set_pressed_button(None)
            return True
        else:
            return False

    def position_selected(self, position_id: int) -> None:
        game_state = self.get_game_state()
        if game_state == GameState.LOCAL_PLAYER_TO_MOVE:
            self.board.position_selected(position_id)
            is_valid_move = self.verify_move_validity()
            if is_valid_move:
                move_to_send = self.board.get_move_to_send()
                self.update_board(move_to_send, True)
                self.player_interface.send_move(move_to_send)
                self.player_interface.update_gui()
            else:
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

    def grid_border_stone_button(self) -> None:
        self.border_stone_button_info[1].grid(row=self.border_stone_button_info[0]+1, column=1-self.border_stone_button_info[2])

    def update_board(self, move: dict[str, str], is_local_move: bool) -> None:
        stone_value = self.identify_stone_value_from_move(move)
        if is_local_move:
            stone_color = self.board.get_local_player_color()
        else:
            stone_color = self.board.get_remote_player_color()

        position = self.identify_position_from_move(move)

        is_stone_in_border = self.board.is_stone_in_border()
        if is_local_move and is_stone_in_border:
            stone_in_border_position = self.board.get_stone_in_border_position()
            self.canvas_board.itemconfig(f"circle{stone_in_border_position}", state=tk.NORMAL, image=self.assets["circle"])
            self.canvas_board.itemconfig(f"border{stone_in_border_position}", state=tk.HIDDEN)
            self.grid_border_stone_button()
            self.board.set_border_stone_info(None)

        move_type = self.get_move_type_from_move(move)
        if move_type == MoveType.INSERT:
            in_left = self.identify_in_left_from_move(move)
            if is_local_move:
                stone_button = self.identify_stone_button(stone_color, stone_value, in_left, tk.NORMAL)
                self.local_player_buttons_of_stones_in_board.append((stone_value, stone_button, in_left))
            else:
                stone_button = self.identify_stone_button(stone_color, stone_value, in_left, tk.DISABLED)
                self.remote_player_buttons_of_stones_in_board.append((stone_value, stone_button, in_left))
            stone_button.grid_forget()
            stone_button.update()
            self.canvas_board.itemconfig(f"circle{position}", image=self.assets[stone_color + str(stone_value)])
        else:
            removed_stone = self.board.get_removed_stone()
            border_stone_button_info = self.pop_stone_button_from_board(is_local_move, int(move["stone_value"]))
            self.set_border_stone_button_info(border_stone_button_info)
            self.board.set_removed_stone(None)
            self.board.set_border_stone_info((removed_stone, position))
            self.canvas_board.itemconfig(f"circle{position}", state=tk.HIDDEN, image=self.assets["circle"])
            self.canvas_board.itemconfig(f"border{position}", state=tk.NORMAL, image=self.assets[stone_color + str(stone_value)])
