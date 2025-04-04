import tkinter as tk
from tkinter import ttk

from ..utils.constants import BOARD_WIDTH, BOARD_HEIGHT


class BoardInterface:
    def __init__(self, root: tk.Tk, assets: dict[str, tk.PhotoImage], local_player_color: str, remote_player_color: str) -> None:
        self.root = root
        self.assets: dict[str, tk.PhotoImage] = assets
        self.canvas_board: tk.Canvas | None = None
        self.stone_buttons: dict[str, tk.Button] = {}
        self.board_frame: ttk.Frame = self.initialize_game_frame(local_player_color, remote_player_color)

    def get_board_frame(self):
        return self.board_frame

    def initialize_player_stone_frame(self, player_color: str, frame_parent: tk.Widget, text: str) -> ttk.Frame:
        player_stones_frame = ttk.Frame(frame_parent, relief=tk.SOLID, borderwidth=2)
        text_label = ttk.Label(player_stones_frame, text=text)
        text_label.grid(column=0, row=0, columnspan=2, pady=1)

        for i in range(6):
            button_stone_1 = ttk.Button(
                player_stones_frame,
                image=self.assets[f"{player_color}{i}"],
                command=lambda index=i: self.stone_selected(player_color, index),
                state=tk.DISABLED,
                style="flat.TButton",
            )
            button_stone_2 = ttk.Button(
                player_stones_frame,
                image=self.assets[f"{player_color}{i}"],
                command=lambda index=i: self.stone_selected(player_color, index),
                state=tk.DISABLED,
                style="flat.TButton",
            )
            self.stone_buttons[player_color + str(i) + ".1"] = button_stone_1
            self.stone_buttons[player_color + str(i) + ".2"] = button_stone_2
            button_stone_1.grid(row=i + 1, column=0, padx=0, pady=0)
            button_stone_2.grid(row=i + 1, column=1, padx=0, pady=0)

        return player_stones_frame

    def initialize_game_frame(self, local_player_color: str, remote_player_color: str) -> ttk.Frame:
        game_frame = ttk.Frame(self.root)

        self.canvas_board = tk.Canvas(
            game_frame, width=BOARD_WIDTH, height=BOARD_HEIGHT
        )
        self.canvas_board.create_image(
            BOARD_WIDTH // 2, BOARD_HEIGHT // (2 - 0.15), image=self.assets["board"], tags="board"
        )
        circles_coordinates = (
            (100, 100),
            (120, 100),
            (140, 100),
            (160, 100),
            (180, 100),
            (200, 100),
            (220, 100),
            (240, 100),
            (260, 100),
            (280, 100),
            (300, 100),
            (320, 100),
        )
        for i in range(12):
            x, y = circles_coordinates[i]
            button_triangle = self.canvas_board.create_image(
                x, y, image=self.assets["circle"], state=tk.HIDDEN, tags=f"circle{i}"
            )
            self.canvas_board.tag_bind(
                button_triangle,
                "<ButtonRelease-1>",
                lambda event, index=i: self.circle_selected(index),
            )

        local_player_stones_frame = self.initialize_player_stone_frame(local_player_color, game_frame,
                                                                       "Peças do jogador local")
        remote_player_stones_frame = self.initialize_player_stone_frame(remote_player_color, game_frame,
                                                                        "Peças do jogador remoto")

        local_player_stones_frame.grid(row=0, column=0)
        self.canvas_board.grid(row=0, column=1, sticky=tk.NS)
        remote_player_stones_frame.grid(row=0, column=2)

        return game_frame

    def update_widgets(self, new_assets: dict[str, tk.PhotoImage]):
        self.assets = new_assets
        for button_name, stone_button in self.stone_buttons.items():
            asset_name = button_name[:-2]
            stone_button.configure(image=self.assets[asset_name])
            stone_button.update()
        for i in range(12):
            self.canvas_board.itemconfig("circle" + str(i), image=self.assets["circle"])
        self.canvas_board.itemconfig("board", image=self.assets["board"])

    def update_stone_state(self, stone_color: str, stone_value: int, state: str) -> None:
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
        self.canvas_board.itemconfig(f"circle{index}", image=self.assets[f"{asset_name}"])

    def stone_selected(self, color: str, stone_value: int) -> None:
        print(f"pedra selecionada. cor = {color}, valor = {stone_value}")
        #game_state = self.board.get_game_state()
        #if game_state == GameState.PLAYER_MOVE_1 or GameState.PLAYER_MOVE_2:
        # move_type = self.board.decide_move_type()
        # valid_circles = self.board.generate_valid_move_list()
        # print("valid circles: ", valid_circles)
        # for circle_index in valid_circles:
        #     self.update_circle_visibility(circle_index, tk.NORMAL)
        # self.update_gui()

    def circle_selected(self, circle_id: int) -> None:
        print(f"círculo selecionado. id = {circle_id}")
        # TODO: enviar os dados referentes à jogada do outro jogador em send_move
        # move_to_send = None
        # #self.update_stone_state(move_to_send["stone_color"], int(move_to_send["stone_value"]), tk.HIDDEN)
        # self.dog.send_move(move_to_send)