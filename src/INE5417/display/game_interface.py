import tkinter as tk
from tkinter import ttk

from .AbstractHelperInterface import AbstractHelperInterface
from ..utils.constants import BOARD_WIDTH, BOARD_HEIGHT, COLOR_A, COLOR_B


class GameInterface(AbstractHelperInterface):
    def __init__(self, root: tk.Tk, assets: dict[str, tk.PhotoImage]) -> None:
        self.canvas_board: tk.Canvas | None = None
        self.stone_buttons: dict[str, tk.Button] = {}
        super().__init__(root, assets)

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
                command=lambda index=i: print(f"pedra selecionada. cor = {player_color}, valor = {index}"),
                state=tk.NORMAL if is_local else tk.DISABLED,
                style="flat.TButton",
            )
            button_stone_2 = ttk.Button(
                player_stones_frame,
                image=self.assets[f"{player_color}{i}"],
                command=lambda index=i: print(f"pedra selecionada. cor = {player_color}, valor = {index}"),
                state=tk.NORMAL if is_local else tk.DISABLED,
                style="flat.TButton",
            )
            self.stone_buttons[player_color + str(i) + ".1"] = button_stone_1
            self.stone_buttons[player_color + str(i) + ".2"] = button_stone_2
            button_stone_1.grid(row=i + 1, column=0, padx=0, pady=0)
            button_stone_2.grid(row=i + 1, column=1, padx=0, pady=0)

        return player_stones_frame

    def initialize_frame(self) -> ttk.Frame:
        game_frame = ttk.Frame(self.root)

        self.canvas_board = tk.Canvas(
            game_frame, width=BOARD_WIDTH, height=BOARD_HEIGHT
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
                x, y, image=self.assets["circle"], tags=f"circle{i}"
            )
            self.canvas_board.tag_bind(
                button_triangle,
                "<ButtonRelease-1>",
                lambda event, index=i: print(f"círculo selecionado. id = {index}"),
            )

        local_player_color, remote_player_color = [COLOR_A, COLOR_B]
        local_player_stones_frame = self.initialize_player_stone_frame(
            local_player_color, game_frame, True, "Peças do jogador local"
        )
        remote_player_stones_frame = self.initialize_player_stone_frame(
            remote_player_color, game_frame, False, "Peças do jogador remoto"
        )

        local_player_stones_frame.grid(row=0, column=0)
        self.canvas_board.grid(row=0, column=1, sticky=tk.NS)
        remote_player_stones_frame.grid(row=0, column=2)

        return game_frame
