import sys
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk

from PIL import ImageTk, Image

from .game_interface import GameInterface
from .main_menu_interface import MainMenuInterface
from ..dog.dog_actor import DogActor
from ..dog.dog_interface import DogPlayerInterface
from ..dog.start_status import StartStatus
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
from ..utils.theme import Theme


class PlayerInterface(DogPlayerInterface):
    def __init__(self) -> None:
        super().__init__()
        self.root: tk.Tk = tk.Tk()
        self.theme: Theme = Theme.DEFAULT
        self.assets: dict[str, ImageTk.PhotoImage] = self.load_assets()
        self.main_menu_interface: MainMenuInterface = MainMenuInterface(
            self.root, self.assets, self
        )
        self.game_interface: GameInterface = GameInterface(self.root, self.assets, self)
        self.stone_buttons: dict[str, ttk.Button] = {}
        self.main_frame: ttk.Frame | None = None
        self.message_label: ttk.Label | None = None
        self.menu_file: tk.Menu | None = None
        self.populate_window()
        #self.player_name: str = self.get_player_name()
        self.player_name: str = ""
        self.dog: DogActor = DogActor()
        self.initialize_dog()
        self.root.mainloop()

    def get_assets_subdirectory(self) -> str:
        return "default" if self.theme == Theme.DEFAULT else "alternative"

    def load_asset(
        self, asset_name: str, extension: str, dimensions: tuple[int, int]
    ) -> ImageTk.PhotoImage:
        asset_file = (
            RESOURCES_DIR / self.get_assets_subdirectory() / f"{asset_name}.{extension}"
        )
        asset_image = Image.open(asset_file).resize((dimensions[0], dimensions[1]))
        return ImageTk.PhotoImage(asset_image)

    def load_assets(self) -> dict[str, tk.PhotoImage]:
        assets = {}
        extension = "png"

        assets["menu_image"] = self.load_asset(
            "menu_image", extension, (WINDOW_WIDTH, WINDOW_HEIGHT)
        )

        assets["menu_button"] = self.load_asset(
            "menu_button", extension, (int(WINDOW_WIDTH / 3.2), BOARD_HEIGHT // 7)
        )

        assets["board"] = self.load_asset(
            "board", extension, (BOARD_WIDTH, BOARD_HEIGHT)
        )

        assets["circle"] = self.load_asset(
            "circle", extension, (int(BOARD_WIDTH * 0.13), int(BOARD_HEIGHT * 0.13))
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

    def populate_window(self) -> None:
        s = ttk.Style(self.root)
        s.theme_use("clam")
        s.configure("flat.TButton", borderwidth=0, bg="")
        self.root.title(GAME_NAME)
        self.root.geometry(WINDOW_GEOMETRY)
        self.root.resizable(False, False)

        self.initialize_message_label()
        self.initialize_menubar()

        self.goto_main_menu()

    def switch_theme(self):
        if self.theme == Theme.DEFAULT:
            self.theme = Theme.ALTERNATIVE
        else:
            self.theme = Theme.DEFAULT
        self.assets = self.load_assets()
        self.main_menu_interface.update_widgets(self.assets)
        self.game_interface.update_widgets(self.assets)

    def initialize_message_label(self) -> None:
        message_frame = ttk.Frame(self.root)
        self.message_label = ttk.Label(message_frame, font=FONT)
        self.update_message_label()
        self.message_label.grid(row=0, column=1)
        message_frame.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=False)

    def initialize_menubar(self) -> None:
        menubar = tk.Menu(self.root)
        menubar.option_add("*tearOff", tk.FALSE)
        self.root["menu"] = menubar

        self.menu_file = tk.Menu(menubar, bg="#FFFFFF")
        menubar.add_cascade(menu=self.menu_file, label="Menu")

        self.menu_file.add_command(
            label="Voltar ao menu principal",
            command=self.go_to_main_menu,
            activebackground="#A7CCE7",
            activeforeground="#000",
            state=tk.DISABLED,
        )
        self.menu_file.add_command(
            label="Trocar conjunto de imagens",
            command=self.switch_theme,
            activebackground="#A7CCE7",
            activeforeground="#000",
            state=tk.DISABLED,
        )
        self.menu_file.add_separator()
        self.menu_file.add_command(
            label="Sair",
            command=self.exit_game,
            activebackground="#EA9E9E",
            activeforeground="#000",
        )

    def get_player_name(self) -> str:
        name = simpledialog.askstring(title=GAME_NAME, prompt="Nome do jogador")
        if not name: name = "User"
        message = "Bem vindo, " + name + "!"
        self.notify(message)
        return name

    def initialize_dog(self) -> None:
        message = self.dog.initialize(self.player_name, self) + "."
        #self.notify(message)

    def start_game(self) -> None:
        game_state = self.game_interface.get_game_state()
        if (
            game_state == GameState.TITLE
            or game_state == GameState.MATCH_ENDED
            or game_state == GameState.ABANDONED_BY_OTHER_PLAYER
        ):
            self.game_interface.reset_game()
            self.switch_to_game_screen()
            self.update_gui()

    def receive_start(self, start_status: StartStatus) -> None:
        self.perform_start_match(start_status.get_players(), "Partida iniciada!")

    def receive_move(self, a_move) -> None:
        print("received move:", a_move)
        self.update_gui()

    def receive_withdrawal_notification(self) -> None:
        print("received withdrawal notification")
        self.update_gui()

    def notify(self, message: str) -> None:
        messagebox.showinfo(title=GAME_NAME, message=message)

    def set_main_frame(self, new_frame: ttk.Frame) -> None:
        if self.main_frame is not None:
            self.main_frame.pack_forget()
        self.main_frame = new_frame
        self.main_frame.pack(fill=tk.BOTH, side=tk.TOP, anchor=tk.CENTER, expand=True)

    def goto_main_menu(self) -> None:
        self.set_main_frame(self.main_menu_interface.get_frame())

    def switch_to_game_screen(self) -> None:
        self.set_main_frame(self.game_interface.get_frame())

    def start_match(self) -> None:
        game_state = self.game_interface.get_game_state()
        if game_state != GameState.TITLE: return

        answer = messagebox.askyesno("START", "Deseja iniciar uma nova partida?")
        if not answer: return

        status: StartStatus = self.dog.start_match(2)
        code: str = status.get_code()
        message: str = status.get_message()
        if code == "0" or code == "1":
            self.notify(message)
            return

        players = status.get_players()
        self.perform_start_match(players, message)

    def perform_start_match(self, players: list[list[str, str, str]], message: str) -> None:
        self.game_interface.perform_start_match(players)
        self.switch_to_game_screen()
        self.update_gui()
        self.notify(message)

    def go_to_main_menu(self):
        game_state = self.game_interface.get_game_state()
        if (
            game_state == GameState.MATCH_ENDED
            or game_state == GameState.ABANDONED_BY_OTHER_PLAYER
        ):
            self.goto_main_menu()

    def send_move(self, move: dict[str, str]) -> None:
        self.dog.send_move(move)

    def update_circle_visibility(self, index: int, state: str) -> None:
        self.game_interface.update_circle_visibility(index, state)

    def update_message_label(self) -> None:
        message = GAME_NAME + ": "
        match self.game_interface.get_game_state():
            case GameState.TITLE:
                message += 'Inicie a partida apertando o "Play"'
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
        game_state = self.game_interface.get_game_state()
        if (
            game_state == GameState.MATCH_ENDED
            or game_state == GameState.ABANDONED_BY_OTHER_PLAYER
        ):
            self.menu_file.entryconfigure(0, state=tk.NORMAL)
        else:
            self.menu_file.entryconfigure(0, state=tk.DISABLED)

        if (
            game_state == GameState.PLAYER_MOVE_1
            or game_state == GameState.PLAYER_MOVE_2
            or game_state == GameState.WAITING_OTHER_PLAYER
        ):
            self.menu_file.entryconfigure(1, state=tk.NORMAL)
        else:
            self.menu_file.entryconfigure(1, state=tk.DISABLED)
        self.menu_file.update()

    def update_gui(self) -> None:
        self.update_message_label()
        self.update_menu_status()

    def exit_game(self) -> None:
        sys.exit(0)
