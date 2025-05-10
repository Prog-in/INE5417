import tkinter as tk
from tkinter import ttk, messagebox

from ..logic.board import Board
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
            button_stone_1 = ttk.Button(
                player_stones_frame,
                image=self.assets[f"{player_color}{i}"],
                command=lambda index=i: self.stone_selected(index, True) if is_local else "",
                state=tk.NORMAL if is_local else tk.DISABLED,
                style="flat.TButton",
            )
            button_stone_2 = ttk.Button(
                player_stones_frame,
                image=self.assets[f"{player_color}{i}"],
                command=lambda index=i: self.stone_selected(index, False) if is_local else "",
                state=tk.NORMAL if is_local else tk.DISABLED,
                style="flat.TButton",
            )
            self.stone_buttons[player_color + str(i) + ".1"] = button_stone_1
            self.stone_buttons[player_color + str(i) + ".2"] = button_stone_2
            button_stone_1.grid(row=i + 1, column=0, padx=0, pady=0)
            button_stone_2.grid(row=i + 1, column=1, padx=0, pady=0)

        return player_stones_frame

    def initialize_frame(self, local_player_color: str, remote_player_color: str) -> None:
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
        circles_coordinates = (
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
            x, y = circles_coordinates[i]
            button_triangle = self.canvas_board.create_image(
                x, y, image=self.assets["circle"], state=tk.HIDDEN, tags=f"circle{i}"
            )
            self.canvas_board.tag_bind(
                button_triangle,
                "<ButtonRelease-1>",
                lambda event, index=i: self.position_selected(index),
            )

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

    def receive_move(self, a_move) -> None:
        self.board.receive_move(a_move)

    def update_board(self, updated_board_frame: ttk.Frame) -> None:
        ...
        # for i, triangle in enumerate(board):
        #     positioned_stone = triangle[0]
        #     asset_name = f"circle"
        #     if positioned_stone is not None:
        #         stone_value, stone_color = positioned_stone
        #         asset_name = f"{stone_color}{stone_value}"
        #     self.update_circle_image(i, asset_name)
        #
        #     border_stone = triangle[1]
        #     self.update_triangle_border(i, border_stone)

    def update_triangle_border(
        self, index: int, border_stone: tuple[str, str] | None
    ) -> None:
        # TODO: implementar a lógica de atualização das bordas dos triângulos
        ...

    def update_widgets_images(self, new_assets: dict[str, tk.PhotoImage]) -> None:
        self.assets = new_assets
        for button_name, stone_button in self.stone_buttons.items():
            asset_name = button_name[:-2]
            stone_button.configure(image=self.assets[asset_name])
            stone_button.update()
        for i in range(12):
            self.canvas_board.itemconfig("circle" + str(i), image=self.assets["circle"])
        self.canvas_board.itemconfig("board", image=self.assets["board"])

    def update_stone_state(
        self, stone_color: str, stone_value: int, state: str
    ) -> None:
        stone_button = self.stone_buttons[stone_color + str(stone_value) + ".2"]
        if stone_button.cget("state") != state:
            stone_button.configure(state=state)
        else:
            stone_button = self.stone_buttons[stone_color + str(stone_value) + ".1"]
            stone_button.configure(state=state)
        stone_button.update()

    def update_stones_state(self, state: str):
        for button in self.stone_buttons.values():
            button.configure(state=state)
            button.update()

    def update_circle_visibility(self, index: int, state: str) -> None:
        self.canvas_board.itemconfig(f"circle{index}", state=state)

    def update_circle_image(self, index: int, asset_name: str) -> None:
        self.canvas_board.itemconfig(
            f"circle{index}", image=self.assets[f"{asset_name}"]
        )

    def stone_selected(self, stone_value: int, in_left: bool) -> None:
        game_state = self.get_game_state()
        if game_state == GameState.LOCAL_PLAYER_TO_MOVE:
            self.board.stone_selected(stone_value, in_left)

    def position_selected(self, position_id: int) -> None:
        game_state = self.get_game_state()
        if game_state == GameState.LOCAL_PLAYER_TO_MOVE:
            move_type = self.board.position_selected(position_id)
            if move_type == MoveType.ASK_AGAIN:
                messagebox.showinfo(message="Jogada inválida. Tente novamente")
            else:
                move_to_send = self.board.get_move_to_send()
                self.update_stone_state(
                    move_to_send["stone_color"], int(move_to_send["stone_value"]), tk.HIDDEN
                )
                self.player_interface.send_move(move_to_send)
