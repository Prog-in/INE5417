import sys
import tkinter as tk
from tkinter import messagebox
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
    COLOR_A,
    COLOR_B, ASSETS_INFO,
)
from ..utils.game_state import GameState
from ..utils.theme import Theme


class PlayerInterface(DogPlayerInterface):
    def __init__(self) -> None:
        super().__init__()
        self.root: tk.Tk = tk.Tk()
        self.initialize_gui_elements()
        self.theme: Theme = self.get_default_theme()
        self.assets: dict[str, ImageTk.PhotoImage] = self.load_assets()
        self.main_menu_interface: MainMenuInterface = MainMenuInterface(
            self.root, self.assets, self
        )
        self.game_interface: GameInterface = GameInterface(self.root, self.assets, self)

        self.main_menu_interface.initialize_frame()

        self.populate_window()

        main_menu_frame = self.main_menu_interface.get_frame()
        self.set_main_frame(main_menu_frame)
        self.main_frame.pack(fill=tk.BOTH, side=tk.TOP, anchor=tk.CENTER, expand=True)

        # self.player_name: str = simpledialog.askstring(prompt="Nome do jogador")
        self.player_name: str = ""
        self.dog: DogActor = DogActor()
        message = self.dog.initialize(self.player_name, self)
        messagebox.showinfo(message=message)
        self.game_interface.set_game_state(GameState.MAIN_MENU)
        self.update_gui()
        self.root.mainloop()

    def initialize_gui_elements(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("flat.TButton", borderwidth=0, background="")
        self.root.title(GAME_NAME)
        self.root.geometry(WINDOW_GEOMETRY)
        self.root.resizable(False, False)

        self.message_label: ttk.Label = ttk.Label(self.root, text=GAME_NAME, font=FONT)

        menubar = tk.Menu(self.root)
        self.menu: tk.Menu = tk.Menu(menubar, bg="#FFFFFF")
        menubar.option_add("*tearOff", tk.FALSE)
        menubar.add_cascade(menu=self.menu, label="Menu")
        self.menu.add_command(
            label="Voltar ao menu principal",
            command=self.go_to_main_menu,
            activebackground="#A7CCE7",
            activeforeground="#000",
            state=tk.DISABLED,
        )
        self.menu.add_command(
            label="Trocar conjunto de imagens",
            command=self.switch_theme,
            activebackground="#A7CCE7",
            activeforeground="#000",
            state=tk.DISABLED,
        )
        self.menu.add_separator()
        self.menu.add_command(
            label="Sair",
            command=self.exit_game,
            activebackground="#EA9E9E",
            activeforeground="#000",
        )
        self.main_frame: ttk.Frame | None = None

    def get_default_theme(self) -> Theme:
        return Theme.DEFAULT

    # TODO: marcar como modelagem de algoritmo
    def load_assets(self) -> dict[str, tk.PhotoImage]:
        if self.theme == Theme.DEFAULT:
            assets_subdirectory = "default"
        else:
            assets_subdirectory = "alternative"
        assets = {}

        assets_bound = len(ASSETS_INFO)
        for i in range(assets_bound):
            image = Image.open(RESOURCES_DIR / assets_subdirectory / ASSETS_INFO[i][0])
            resized_image = image.resize(ASSETS_INFO[i][1])
            assets[ASSETS_INFO[i][0].removesuffix(".png")] = ImageTk.PhotoImage(resized_image)

        colors = [COLOR_A, COLOR_B]
        colors_bound = len(colors)
        for i in range(colors_bound):
            for j in range(6):
                stone_image = Image.open(RESOURCES_DIR / assets_subdirectory / (colors[i]  + str(j) + ".png"))
                resized_stone_image = stone_image.resize((int(WINDOW_WIDTH * 0.07), int(WINDOW_HEIGHT * 0.07)))
                assets[colors[i] + str(j)] = ImageTk.PhotoImage(resized_stone_image)

        return assets

    def set_main_frame(self, new_frame: ttk.Frame) -> None:
        self.main_frame = new_frame

    def get_theme(self) -> Theme:
        return self.theme

    def set_theme(self, new_theme: Theme) -> None:
        self.theme = new_theme

    def switch_theme(self) -> None:
        game_state = self.game_interface.get_game_state()
        if game_state == GameState.MAIN_MENU:
            theme = self.get_theme()
            if theme == Theme.DEFAULT:
                self.set_theme(Theme.ALTERNATIVE)
            else:
                self.set_theme(Theme.DEFAULT)
            self.assets = self.load_assets()
            self.main_menu_interface.update_widgets_images(self.assets)
            self.game_interface.update_widgets_images(self.assets)

    def populate_window(self) -> None:
        parent_name = self.menu.winfo_parent()
        menubar = self.menu.nametowidget(parent_name)
        self.root.config(menu=menubar)
        self.message_label.pack(fill=tk.X, side=tk.BOTTOM, expand=False)

    def perform_match_start(self, start_status: StartStatus, game_state: GameState) -> None:
        players = start_status.get_players()
        self.game_interface.start_match(players)
        self.game_interface.initialize_frame()
        game_frame = self.game_interface.get_frame()
        is_main_screen_filled = self.is_main_screen_filled()
        if is_main_screen_filled:
            self.main_frame.pack_forget()
        self.set_main_frame(game_frame)
        self.main_frame.pack(
            fill=tk.BOTH, side=tk.TOP, anchor=tk.CENTER, expand=True
        )
        self.game_interface.set_game_state(game_state)
        self.update_gui()

    def receive_start(self, start_status: StartStatus) -> None:
        game_state = self.game_interface.get_game_state()
        if game_state == GameState.MAIN_MENU:
            self.perform_match_start(start_status, GameState.REMOTE_PLAYER_TO_MOVE)
            messagebox.showinfo(message="Partida iniciada!")

    def receive_move(self, a_move: dict[str, str]) -> None:
        game_state = self.game_interface.get_game_state()
        if game_state == GameState.REMOTE_PLAYER_TO_MOVE:
            self.game_interface.receive_move(a_move)
            self.game_interface.update_board(a_move, False)
            self.update_gui()

    def receive_withdrawal_notification(self) -> None:
        game_state = self.game_interface.get_game_state()
        if game_state == GameState.LOCAL_PLAYER_TO_MOVE or GameState.REMOTE_PLAYER_TO_MOVE:
            self.game_interface.set_game_state(GameState.ABANDONED_BY_OTHER_PLAYER)
            self.update_gui()

    def is_main_screen_filled(self) -> bool:
        if self.main_frame is not None:
            return True
        else:
            return False

    def start_match(self) -> None:
        game_state = self.game_interface.get_game_state()
        if game_state == GameState.MAIN_MENU:
            answer = messagebox.askyesno("START", "Deseja iniciar uma nova partida?")
            if answer:
                start_status: StartStatus = self.dog.start_match(2)
                message: str = start_status.get_message()
                code: str = start_status.get_code()
                if code == "0" or code == "1":
                    messagebox.showinfo(message=message)
                elif code == "2":
                    self.perform_match_start(start_status, GameState.LOCAL_PLAYER_TO_MOVE)
                    messagebox.showinfo(message=message)

    def go_to_main_menu(self):
        game_state = self.game_interface.get_game_state()
        if (
            game_state == GameState.GAME_OVER
            or game_state == GameState.ABANDONED_BY_OTHER_PLAYER
        ):
            main_menu_frame = self.main_menu_interface.get_frame()
            is_main_screen_filled = self.is_main_screen_filled()
            if is_main_screen_filled:
                self.main_frame.pack_forget()
            self.set_main_frame(main_menu_frame)
            self.main_frame.pack(
                fill=tk.BOTH, side=tk.TOP, anchor=tk.CENTER, expand=True
            )
            self.game_interface.set_game_state(GameState.MAIN_MENU)
            self.update_gui()

    def send_move(self, move: dict[str, str]) -> None:
        self.dog.send_move(move)

    def update_gui(self) -> None:
        game_state = self.game_interface.get_game_state()

        # Atualizando o label de mensagens
        message = GAME_NAME + ": "
        match game_state:
            case GameState.MAIN_MENU:
                message += 'Inicie a partida apertando o "Play"'
            case GameState.LOCAL_PLAYER_TO_MOVE:
                message += "Selecione uma pedra ou círculo"
            case GameState.REMOTE_PLAYER_TO_MOVE:
                message += "Espere o outro jogador jogar"
            case GameState.GAME_OVER:
                message += "Partida encerrada: "
                is_local_player_winner = self.game_interface.is_local_player_winner()
                if is_local_player_winner:
                    message += "Jogador local venceu"
                else:
                    message += "Jogador remoto venceu"
            case GameState.ABANDONED_BY_OTHER_PLAYER:
                message += "Partida abandonada pelo outro jogador"
        self.message_label.configure(text=message)
        self.message_label.update()

        if (
            game_state == GameState.GAME_OVER
            or game_state == GameState.ABANDONED_BY_OTHER_PLAYER
        ):
            self.menu.entryconfigure(1, state=tk.NORMAL)
        else:
            self.menu.entryconfigure(1, state=tk.DISABLED)

        if game_state == GameState.MAIN_MENU:
            self.menu.entryconfigure(2, state=tk.NORMAL)
            self.menu.entryconfigure(4, state=tk.NORMAL)
        else:
            self.menu.entryconfigure(2, state=tk.DISABLED)
            self.menu.entryconfigure(4, state=tk.DISABLED)

        self.menu.update()

    def exit_game(self) -> None:
        game_state = self.game_interface.get_game_state()
        if game_state == GameState.MAIN_MENU:
            sys.exit(0)
