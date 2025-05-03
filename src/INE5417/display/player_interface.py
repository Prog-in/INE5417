import sys
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk

from PIL import ImageTk, Image, ImageFile

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
        self.message_label: ttk.Label = ttk.Label(self.root, font=FONT)
        self.menu: tk.Menu = self.initialize_menu()
        # main_frame é inicializado apenas quando a interface do menu principal
        # é renderizada
        self.main_frame: ttk.Frame | None = None
        self.theme: Theme = self.get_default_theme()
        self.assets: dict[str, ImageTk.PhotoImage] = self.load_assets()
        self.main_menu_interface: MainMenuInterface = MainMenuInterface(self.root, self.assets, self)
        self.game_interface: GameInterface = GameInterface(self.root, self.assets, self)
        self.populate_window()
        self.goto_main_menu()
        #self.player_name: str = simpledialog.askstring(prompt="Nome do jogador")
        self.player_name: str = ""
        self.dog: DogActor = DogActor()
        message = self.dog.initialize(self.player_name, self)
        messagebox.showinfo(message=message)
        self.root.mainloop()

    def create_style(self, root: tk.Tk) -> ttk.Style:
        return ttk.Style(root)

    def configure_style(self, style: ttk.Style) -> None:
        style.theme_use("clam")
        style.configure("flat.TButton", borderwidth=0, bg="")

    def set_root_properties(self, root: tk.Tk) -> None:
        root.title(GAME_NAME)
        root.geometry(WINDOW_GEOMETRY)
        root.resizable(False, False)

    def configure_root(self, root: tk.Tk) -> None:
        style = self.create_style(root)
        self.configure_style(style)
        self.set_root_properties(root)

    def get_default_theme(self) -> Theme:
        return Theme.DEFAULT

    def get_assets_subdirectory(self) -> str:
        if self.theme == Theme.DEFAULT:
            return "default"
        else: 
            return "alternative"

    def concatenate_image_path(self, subdirectory: str, asset_filename: str) -> Path:
        return RESOURCES_DIR / subdirectory / f"{asset_filename}"

    def get_filepath(self, filename: str) -> Path:
        subdirectory = self.get_assets_subdirectory()
        return self.concatenate_image_path(subdirectory, filename)

    def get_image(self, asset_filepath: Path) -> ImageFile.ImageFile:
        return Image.open(asset_filepath)

    def resize_image(self, image: ImageFile.ImageFile, dimensions: tuple[int, int]):
        return image.resize(dimensions)

    def image_to_photoimage(self, image) -> ImageTk.PhotoImage:
        return ImageTk.PhotoImage(image)

    def load_asset(
        self, asset_filename: str, dimensions: tuple[int, int]
    ) -> ImageTk.PhotoImage:
        asset_filepath = self.get_filepath(asset_filename)
        image = self.get_image(asset_filepath)
        resized_image = self.resize_image(image, dimensions)
        return self.image_to_photoimage(resized_image) 

    def construct_assets_dict(self) -> dict[str, ImageTk.PhotoImage]:
        return dict()

    def remove_extension_from_filename(self, filename: str) -> str:
        # captura o nome do arquivo sem a extensão ".png"
        return filename[:-4]

    def insert_key_pair_into_assets(self, key: str, value: tk.PhotoImage, assets: dict[str, tk.PhotoImage]) -> None:
        assets[key] = value

    def add_image_to_assets(self, filename: str, value: tk.PhotoImage, assets: dict[str, tk.PhotoImage]) -> None:
        key = self.remove_extension_from_filename(filename)
        self.insert_key_pair_into_assets(key, value, assets)

    def get_menu_image_filename(self) -> str:
        return "menu_image.png"

    def get_menu_image_dimensions(self) -> tuple[int, int]:
        return WINDOW_WIDTH, WINDOW_HEIGHT

    def load_menu_image(self, assets: dict[str, tk.PhotoImage]) -> None:
        image_filename = self.get_menu_image_filename()
        image_dimensions = self.get_menu_image_dimensions()
        image = self.load_asset(image_filename, image_dimensions)
        self.add_image_to_assets(image_filename, image, assets)

    def get_menu_button_image_filename(self) -> str:
        return "menu_button.png"

    def get_menu_button_image_dimensions(self) -> tuple[int, int]:
        return int(WINDOW_WIDTH / 3.2), WINDOW_HEIGHT // 7

    def load_menu_button_image(self, assets: dict[str, tk.PhotoImage]) -> None:
        image_filename = self.get_menu_button_image_filename()
        image_dimensions = self.get_menu_button_image_dimensions()
        image = self.load_asset(image_filename, image_dimensions)
        self.add_image_to_assets(image_filename, image, assets)

    def get_board_image_filename(self) -> str:
        return "board.png"

    def get_board_image_dimensions(self) -> tuple[int, int]:
        return BOARD_WIDTH, BOARD_HEIGHT

    def load_board_image(self, assets: dict[str, tk.PhotoImage]) -> None:
        image_filename = self.get_board_image_filename()
        image_dimensions = self.get_board_image_dimensions()
        image = self.load_asset(image_filename, image_dimensions)
        self.add_image_to_assets(image_filename, image, assets)

    def get_circle_image_filename(self) -> str:
        return "circle.png"

    def get_circle_image_dimensions(self) -> tuple[int, int]:
        return int(BOARD_WIDTH * 0.13), int(BOARD_HEIGHT * 0.13)

    def load_circle_image(self, assets: dict[str, tk.PhotoImage]) -> None:
        image_filename = self.get_circle_image_filename()
        image_dimensions = self.get_circle_image_dimensions()
        image = self.load_asset(image_filename, image_dimensions)
        self.add_image_to_assets(image_filename, image, assets)

    def get_stone_image_dimensions(self) -> tuple[int, int]:
        return int(WINDOW_WIDTH * 0.09), int(WINDOW_HEIGHT * 0.09)

    def get_players_colors(self) -> tuple[str, str]:
        return (COLOR_A, COLOR_B)

    def get_players_colors_length(self, players_colors: tuple[str, str]) -> int:
        return len(players_colors)

    def get_element_from_players_colors(self, players_colors: tuple[str, str], index: int) -> str:
        return players_colors[index]

    def number_to_string(self, number: int) -> str:
        return str(number)

    def concatenate_strings(self, string1: str, string2: str) -> str:
        return string1 + string2

    def get_stone_image_extension(self) -> str:
        return ".png"

    def get_stone_image_filename(self, color: str, stone_value: int) -> str:
        stone_value_str = self.number_to_string(stone_value)
        filename_without_extension = self.concatenate_strings(color, stone_value_str)
        extension = self.get_stone_image_extension()
        return self.concatenate_strings(filename_without_extension, extension)

    def load_stones_images(self, assets: dict[str, tk.PhotoImage]) -> None:
        stone_image_dimensions = self.get_stone_image_dimensions()
        players_colors = self.get_players_colors()
        colors_length = self.get_players_colors_length(players_colors)
        for i in range(colors_length):
            color = self.get_element_from_players_colors(players_colors, i)
            for j in range(6):
                stone_image_filename = self.get_stone_image_filename(color, j)
                stone_image = self.load_asset(stone_image_filename, stone_image_dimensions)
                self.add_image_to_assets(stone_image_filename, stone_image, assets)

    def load_assets(self) -> dict[str, tk.PhotoImage]:
        assets = self.construct_assets_dict()
        self.load_menu_image(assets)
        self.load_menu_button_image(assets)
        self.load_board_image(assets)
        self.load_circle_image(assets)
        self.load_stones_images(assets)
        return assets

    def initialize_menu(self) -> tk.Menu:
        menubar = tk.Menu(self.root)
        menu = tk.Menu(menubar, bg="#FFFFFF")

        menubar.option_add("*tearOff", tk.FALSE)
        menubar.add_cascade(menu=menu, label="Menu")

        menu.add_command(
            label="Voltar ao menu principal",
            command=self.go_to_main_menu,
            activebackground="#A7CCE7",
            activeforeground="#000",
            state=tk.DISABLED,
        )
        menu.add_command(
            label="Trocar conjunto de imagens",
            command=self.switch_theme,
            activebackground="#A7CCE7",
            activeforeground="#000",
            state=tk.DISABLED,
        )
        menu.add_separator()
        menu.add_command(
            label="Sair",
            command=self.exit_game,
            activebackground="#EA9E9E",
            activeforeground="#000",
        )
        return menu

    def switch_theme(self):
        if self.theme == Theme.DEFAULT:
            self.theme = Theme.ALTERNATIVE
        else:
            self.theme = Theme.DEFAULT
        self.assets = self.load_assets()
        self.main_menu_interface.update_widgets(self.assets)
        self.game_interface.update_widgets(self.assets)

    def place_menu(self) -> None:
        menubar = self.menu.nametowidget(self.menu.winfo_parent())
        self.root.config(menu=menubar)

    def place_message_label(self) -> None:
        self.update_message_label()
        self.message_label.pack(fill=tk.X, side=tk.BOTTOM, expand=False)

    def populate_window(self) -> None:
        self.place_menu()
        self.place_message_label()

    def start_game(self) -> None:
        game_state = self.game_interface.get_game_state()
        if (
            game_state == GameState.TITLE
            or game_state == GameState.MATCH_ENDED
            or game_state == GameState.ABANDONED_BY_OTHER_PLAYER
        ):
            self.game_interface.reset_game()
            self.goto_game_screen()
            self.update_gui()

    def receive_start(self, start_status: StartStatus) -> None:
        self.perform_start_match(start_status.get_players(), "Partida iniciada!")

    def receive_move(self, a_move) -> None:
        print("received move:", a_move)
        self.update_gui()

    def receive_withdrawal_notification(self) -> None:
        print("received withdrawal notification")
        self.update_gui()

    def is_main_frame_populated(self) -> bool:
        return self.main_frame is not None

    def set_main_frame(self, new_frame: ttk.Frame) -> None:
        self.main_frame = new_frame

    def map_main_frame(self) -> None:
        self.main_frame.pack(fill=tk.BOTH, side=tk.TOP, anchor=tk.CENTER, expand=True)

    def define_main_frame(self, new_frame: ttk.Frame) -> None:
        if self.is_main_frame_populated():
            self.main_frame.pack_forget()
        self.set_main_frame(new_frame)
        self.map_main_frame()

    def goto_main_menu(self) -> None:
        main_menu_frame = self.main_menu_interface.get_frame()
        self.define_main_frame(main_menu_frame)

    def goto_game_screen(self) -> None:
        game_frame = self.game_interface.get_frame()
        self.define_main_frame(game_frame)

    def start_match(self) -> None:
        game_state = self.game_interface.get_game_state()
        if game_state != GameState.TITLE:
            return
        answer = messagebox.askyesno("START", "Deseja iniciar uma nova partida?")
        if not answer:
            return
        status: StartStatus = self.dog.start_match(2)
        code: str = status.get_code()
        message: str = status.get_message()
        if code == "0" or code == "1":
            messagebox.showinfo(message=message)
            return
        players = status.get_players()
        self.perform_start_match(players, message)

    def perform_start_match(
        self, players: list[list[str, str, str]], message: str
    ) -> None:
        self.game_interface.perform_start_match(players)
        self.goto_game_screen()
        self.update_gui()
        messagebox.showinfo(message=message)

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
            self.menu.entryconfigure(0, state=tk.NORMAL)
        else:
            self.menu.entryconfigure(0, state=tk.DISABLED)

        if (
            game_state == GameState.PLAYER_MOVE_1
            or game_state == GameState.PLAYER_MOVE_2
            or game_state == GameState.WAITING_OTHER_PLAYER
        ):
            self.menu.entryconfigure(1, state=tk.NORMAL)
        else:
            self.menu.entryconfigure(1, state=tk.DISABLED)
        self.menu.update()

    def update_gui(self) -> None:
        self.update_message_label()
        self.update_menu_status()

    def exit_game(self) -> None:
        sys.exit(0)
