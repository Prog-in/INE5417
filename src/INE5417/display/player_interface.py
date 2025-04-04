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
        self.assets: dict[str, ImageTk.PhotoImage] = self.load_assets()
        self.board: Board = Board(self.root, self.assets)
        self.stone_buttons: dict[str, ttk.Button] = {}
        self.main_frame: ttk.Frame | None = None
        self.message_label: ttk.Label | None = None
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

    def load_assets(self) -> dict[str, tk.PhotoImage]:
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

        return assets

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

    def switch_assets_set(self):
        if not self.board.get_game_state() == GameState.TITLE:
            return
        if self.assets_set == AssetsSet.DEFAULT:
            self.assets_set = AssetsSet.ALTERNATIVE
        else:
            self.assets_set = AssetsSet.DEFAULT
        self.assets = self.load_assets()
        self.board.get_board().update_widgets(self.assets)

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

    def start_game(self) -> None:
        game_state = self.board.get_game_state()
        if (game_state == GameState.TITLE
                or game_state == GameState.MATCH_ENDED
                or game_state == GameState.ABANDONED_BY_OTHER_PLAYER
        ):
            self.set_main_frame(self.board.get_board().get_board_frame())
            self.board.reset_game()
            # self.update_gui()

    def receive_start(self, start_status) -> None:
        self.start_game()
        players = start_status.get_players()
        self.board.start_match(players)
#        self.update_gui()

    def receive_move(self, a_move) -> None:
        print("received move:", a_move)
        self.board.receive_move(a_move)
        self.update_gui()

    def receive_withdrawal_notification(self) -> None:
        self.board.receive_withdrawal_notification()
        self.update_gui()

    def set_main_frame(self, new_frame: ttk.Frame) -> None:
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
                    self.set_main_frame(self.board.get_board().get_board_frame())
                    players = status.get_players()
                    self.board.start_match(players)
                    #self.update_gui()
                    messagebox.showinfo(title=GAME_NAME, message=status.get_message())

    def go_to_main_menu(self):
        game_state = self.board.get_game_state()
        if game_state == GameState.MATCH_ENDED or game_state == GameState.ABANDONED_BY_OTHER_PLAYER:
            self.set_main_frame(self.initialize_main_menu())

    def update_circle_visibility(self, index: int, state: str) -> None:
        self.board.get_board().update_circle_visibility(index, state)

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
        self.board.get_board().update_stones_state(stone_buttons_state)

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
            self, updated_board_frame: ttk.Frame
    ) -> None:
        self.set_main_frame(updated_board_frame)
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

    def update_gui(self) -> None:
        self.update_stones()
        self.update_message_label()
        self.update_menu_status()
        # self.update_board(updated_board_frame)
        self.set_main_frame(self.board.get_board().get_board_frame())

    def end_window(self) -> None:
        quit()
