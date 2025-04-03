import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk

from PIL import ImageTk, Image

from ..dog.dog_actor import DogActor
from ..dog.dog_interface import DogPlayerInterface
from ..logic.board import Board
from ..utils.assets_set import AssetsSet
from ..utils.constants import (
    GAME_NAME,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_GEOMETRY,
    RESOURCES_DIR,
    FONT,
    BOARD_WIDTH,
    BOARD_HEIGHT,
    COLOR_A,
    COLOR_B,
)
from ..utils.game_state import GameState


class PlayerInterface(DogPlayerInterface):
    def __init__(self) -> None:
        super().__init__()
        self.root: tk.Tk = tk.Tk()
        self.assets_set: AssetsSet = AssetsSet.DEFAULT
        self.board: Board = Board()
        self.assets: dict[str, ImageTk.PhotoImage] = {}
        self.stone_buttons: dict[str, ttk.Button] = {}
        self.main_frame: tk.Frame | None = None
        self.load_assets()
        self.populate_window()
        self.menu_file: tk.Menu = self.initialize_menubar()
        # self.player_name: str = self.get_player_name()
        self.player_name: str = ""
        self.dog: DogActor = DogActor()
        self.initialize_dog()
        self.root.mainloop()

    def get_player_name(self) -> str:
        name = simpledialog.askstring(title=GAME_NAME, prompt="Nome do jogador")
        if name:
            return name
        return "User"

    def get_assets_subdirectory(self) -> str:
        if self.assets_set == AssetsSet.ALTERNATIVE:
            return "alternative"
        return "default"

    def load_asset(
        self, asset_name: str, extension: str, dimensions: tuple[int, int]
    ) -> ImageTk.PhotoImage:
        asset_file = RESOURCES_DIR / self.get_assets_subdirectory() / f"{asset_name}.{extension}"
        asset_image = Image.open(asset_file).resize((dimensions[0], dimensions[1]))
        return ImageTk.PhotoImage(asset_image)

    def load_assets(self) -> None:
        assets = {}
        extension = "png"

        assets["menu_image"] = self.load_asset(
            "menu_image", extension, (WINDOW_WIDTH, WINDOW_HEIGHT)
        )

        assets["menu_button"] = self.load_asset(
            "menu_button", extension, (WINDOW_WIDTH // 4, BOARD_HEIGHT // 5)
        )

        assets["board"] = self.load_asset(
            "board", extension, (BOARD_WIDTH, BOARD_HEIGHT)
        )

        assets["circle"] = self.load_asset(
            "circle", extension, (int(BOARD_WIDTH * 0.1), int(BOARD_HEIGHT * 0.1))
        )

        # assets das pedras
        for color in [COLOR_A, COLOR_B]:
            for i in range(6):
                color_name = color + str(i)
                assets[color_name] = self.load_asset(
                    color_name,
                    extension,
                    (int(WINDOW_WIDTH * 0.09), int(WINDOW_HEIGHT * 0.09)),
                )
        self.assets = assets

    def initialize_player_stone_frame(self, player_color: str, frame_parent: tk.Widget, text: str) -> tk.Frame:
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
            button_stone_1.grid(row=i+1, column=0, padx=0, pady=0)
            button_stone_2.grid(row=i+1, column=1, padx=0, pady=0)

        return player_stones_frame

    def initialize_game_frame(self) -> ttk.Frame:
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

        local_player_color, remote_player_color = self.board.get_players_colors()
        local_player_stones_frame = self.initialize_player_stone_frame(local_player_color, game_frame, "Peças do jogador local")
        remote_player_stones_frame = self.initialize_player_stone_frame(remote_player_color, game_frame, "Peças do jogador remoto")

        local_player_stones_frame.grid(row=0, column=0)
        self.canvas_board.grid(row=0, column=1, sticky=tk.NS)
        remote_player_stones_frame.grid(row=0, column=2)

        return game_frame

    def initialize_main_menu(self) -> ttk.Frame:
        menu_frame = ttk.Frame(self.root)
        menu_canvas = tk.Canvas(menu_frame, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        menu_canvas.create_image(
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, image=self.assets["menu_image"]
        )
        menu_button = menu_canvas.create_image(
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, image=self.assets["menu_button"]
        )
        menu_canvas.tag_bind(
            menu_button,
            "<ButtonRelease-1>",
            #lambda event: self.start_game(),
            lambda event: self.start_match()
        )
        menu_canvas.grid(row=0, column=0, sticky=tk.NSEW)

        return menu_frame

    def populate_window(self) -> None:
        s = ttk.Style(self.root)
        s.theme_use("clam")
        s.configure("flat.TButton", borderwidth=0, bg="")
        self.root.title(GAME_NAME)
        self.root.geometry(WINDOW_GEOMETRY)
        self.root.resizable(False, False)
        # self.root.iconbitmap()

        # logo_frame = ttk.Frame(self.root)
        # logo_frame.pack(fill=tk.X, side = tk.TOP, expand=True)

        # Setting the image of the logo inside the frame for the logo
        # logo = tk.PhotoImage(file="images/logo.png")
        # ttk.Label(self.logo_frame, image=self.logo).grid(row=0, column=0)

        self.set_main_frame(self.initialize_main_menu())

        message_frame = ttk.Frame(self.root)
        self.message_label = ttk.Label(message_frame, font=FONT)
        self.update_message_label()
        self.message_label.grid(row=0, column=1)

        self.main_frame.pack(fill=tk.X, side=tk.TOP, anchor=tk.CENTER, expand=True)
        message_frame.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=False)

    def update_all_images(self):
        for button_name, stone_button in self.stone_buttons.items():
            asset_name = button_name[:-2]
            stone_button.configure(image=self.assets[asset_name])
            stone_button.update()
        for i in range(12):
            self.canvas_board.itemconfig("circle" + str(i), image=self.assets["circle"])
        self.canvas_board.itemconfig("board", image=self.assets["board"])

    def switch_assets_set(self):
        if not self.board.get_game_state() == GameState.TITLE:
            return
        if self.assets_set == AssetsSet.DEFAULT:
            self.assets_set = AssetsSet.ALTERNATIVE
        else:
            self.assets_set = AssetsSet.DEFAULT
        self.load_assets()
        self.update_all_images()

    def initialize_menubar(self) -> tk.Menu:
        menubar = tk.Menu(self.root)
        menubar.option_add("*tearOff", tk.FALSE)
        self.root["menu"] = menubar

        menu_file = tk.Menu(menubar, bg="#FFFFFF")
        menubar.add_cascade(menu=menu_file, label="Menu")

        menu_file.add_command(
            label="Voltar ao menu principal",
            command=self.go_to_main_menu,
            activebackground="#A7CCE7",
            activeforeground="#000",
            state=tk.DISABLED
        )
        menu_file.add_command(
            label="Trocar conjunto de imagens",
            command=self.switch_assets_set,
            activebackground="#A7CCE7",
            activeforeground="#000",
            state=tk.DISABLED
        )
        menu_file.add_separator()
        menu_file.add_command(
            label="Sair",
            command=self.end_window,
            activebackground="#EA9E9E",
            activeforeground="#000",
        )
        return menu_file

    def initialize_dog(self) -> None:
        message = "Bem vindo, " + self.player_name + "!"
        # messagebox.showinfo(title=GAME_NAME, message=message)

        message = self.dog.initialize(self.player_name, self) + "."
        # messagebox.showinfo(title="Dog Server", message=message)

    def stone_selected(self, color: str, stone_value: int) -> None:
        game_state = self.board.get_game_state()
        if game_state == GameState.PLAYER_MOVE_1 or GameState.PLAYER_MOVE_2:
            move_type = self.board.decide_move_type()
            valid_circles = self.board.generate_valid_move_list()
            print("valid circles: ", valid_circles)
            for circle_index in valid_circles:
                self.update_circle_visibility(circle_index, tk.NORMAL)
            updated_board = self.board.get_board()
            self.update_gui(updated_board)

    def circle_selected(self, circle_id: int) -> None:
        # TODO: enviar os dados referentes à jogada do outro jogador em send_move
        move_to_send = self.board.triangle_selected(circle_id)
        print(move_to_send)
        self.dog.send_move(move_to_send)
        self.update_stone_state(move_to_send["stone_color"], int(move_to_send["stone_value"]), tk.HIDDEN)

    def start_game(self) -> None:
        game_state = self.board.get_game_state()
        if (game_state == GameState.TITLE
            or game_state == GameState.MATCH_ENDED
            or game_state == GameState.ABANDONED_BY_OTHER_PLAYER
        ):
            self.set_main_frame(self.initialize_game_frame())
            self.board.reset_game()
            updated_board = self.board.get_board()
            self.update_gui(updated_board)

    def receive_start(self, start_status) -> None:
        self.start_game()
        players = start_status.get_players()
        self.board.start_match(players)
        updated_board = self.board.get_board()
        self.update_gui(updated_board)

    def receive_move(self, a_move) -> None:
        print("received move:", a_move)
        self.board.receive_move(a_move)
        updated_board = self.board.get_board()
        self.update_gui(updated_board)

    def receive_withdrawal_notification(self) -> None:
        self.board.receive_withdrawal_notification()
        updated_board = self.board.get_board()
        self.update_gui(updated_board)

    def set_main_frame(self, new_frame: tk.Frame) -> None:
        if self.main_frame is not None:
            self.main_frame.destroy()
        self.main_frame = new_frame
        self.main_frame.pack(fill=tk.BOTH, side=tk.TOP, anchor=tk.CENTER, expand=True)


    def start_match(self) -> None:
        game_state = self.board.get_game_state()
        if game_state == GameState.TITLE:
            answer = messagebox.askyesno("START", "Deseja iniciar uma nova partida?")
            if answer:
                status = self.dog.start_match(2)
                code = status.get_code()
                message = status.get_message()
                if code == "0" or code == "1":
                    messagebox.showinfo(title=GAME_NAME, message=message)
                else:
                    self.set_main_frame(self.initialize_game_frame())
                    players = status.get_players()
                    self.board.start_match(players)
                    updated_board = self.board.get_board()
                    self.update_gui(updated_board)
                    messagebox.showinfo(title=GAME_NAME, message=status.get_message())

    def go_to_main_menu(self):
        game_state = self.board.get_game_state()
        if game_state == GameState.MATCH_ENDED or game_state == GameState.ABANDONED_BY_OTHER_PLAYER:
            self.set_main_frame(self.initialize_main_menu())

    def update_game_state(self) -> None: ...

    def update_circle_image(self, index: int, asset_name: str) -> None:
        self.canvas_board.itemconfig(f"circle{index}", image=self.assets[f"{asset_name}"])

    def update_circle_visibility(self, index: int, state: str) -> None:
        self.canvas_board.itemconfig(f"circle{index}", state=state)

    def update_stone_state(self, stone_color: str, stone_value: int, state: str) -> None:
        stone_button = self.stone_buttons[stone_color + str(stone_value) + ".2"]
        if stone_button.cget("state") != state:
            stone_button.configure(state=state)
        else:
            stone_button = self.stone_buttons[stone_color + str(stone_value) + ".1"]
            stone_button.configure(state=state)
        stone_button.update()
        print(stone_color, stone_value, state)

    def update_stones(self) -> None:
        game_state = self.board.get_game_state()
        if (
            game_state == GameState.TITLE
            or game_state == GameState.MATCH_ENDED
            or game_state == GameState.ABANDONED_BY_OTHER_PLAYER
        ):
            stone_buttons_state = tk.DISABLED
        else:
            stone_buttons_state = tk.NORMAL
        for button in self.stone_buttons.values():
            button.configure(state=stone_buttons_state)
            button.update()

    def update_message_label(self) -> None:
        message = GAME_NAME + ": "
        match self.board.get_game_state():
            case GameState.TITLE:
                message += "Inicie a partida no menu"
            case GameState.PLAYER_MOVE_1:
                message += "Selecione uma pedra"
            case GameState.PLAYER_MOVE_2:
                message += "Selecione um círculo"
            case GameState.WAITING_OTHER_PLAYER:
                message += "Espere o outro jogador jogar"
            case GameState.MATCH_ENDED:
                message += "Partida encerrada"
            case GameState.ABANDONED_BY_OTHER_PLAYER:
                message += "Partida abandonada pelo outro jogador"
        self.message_label.configure(text=message)
        self.message_label.update()

    def update_menu_status(self) -> None:
        game_state = self.board.get_game_state()
        if (
            game_state == GameState.MATCH_ENDED
            or game_state == GameState.ABANDONED_BY_OTHER_PLAYER
        ):
            self.menu_file.entryconfigure(0, state=tk.NORMAL)
        else:
            self.menu_file.entryconfigure(0, state=tk.DISABLED)

        if (game_state == GameState.PLAYER_MOVE_1
            or game_state == GameState.PLAYER_MOVE_2
            or game_state == GameState.WAITING_OTHER_PLAYER
        ):
            self.menu_file.entryconfigure(1, state=tk.NORMAL)
        else:
            self.menu_file.entryconfigure(1, state=tk.DISABLED)
        self.menu_file.update()

    def update_triangle_border(
        self, index: int, border_stone: tuple[str, str] | None
    ) -> None:
        # TODO: implementar a lógica de atualização das bordas dos triângulos
        ...

    def update_board(
        self, board: list[tuple[tuple[str, str] | None, tuple[str, str] | None]]
    ) -> None:
        for i, triangle in enumerate(board):
            positioned_stone = triangle[0]
            asset_name = f"circle"
            if positioned_stone is not None:
                stone_value, stone_color = positioned_stone
                asset_name = f"{stone_color}{stone_value}"
            self.update_circle_image(i, asset_name)

            border_stone = triangle[1]
            self.update_triangle_border(i, border_stone)

    def update_gui(
        self, updated_board: list[tuple[tuple[str, str] | None, tuple[str, str] | None]]
    ) -> None:
        self.update_stones()
        self.update_message_label()
        self.update_menu_status()
        self.update_board(updated_board)

    def end_window(self):
        quit()
