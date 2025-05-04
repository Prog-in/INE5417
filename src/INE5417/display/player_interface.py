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
        # Inicializando elementos da interface gráfica
        self.root: tk.Tk = tk.Tk()
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("flat.TButton", borderwidth=0, bg="")
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
        self.theme: Theme = Theme.DEFAULT

        # Carregando as imagens do jogo
        self.assets: dict[str, ImageTk.PhotoImage] = self.load_assets()

        # Inicializando a interface de menu principal
        self.main_menu_interface: MainMenuInterface = MainMenuInterface(
            self.root, self.assets, self
        )

        # inicializando a interface de jogo e os elementos do domínio do problema
        self.game_interface: GameInterface = GameInterface(self.root, self.assets, self)

        # Populando a interface gráfica
        self.populate_window()

        # Indo para a tela de menu principal
        self.go_to_main_menu_screen()

        # Obtendo o nome do jogador
        # self.player_name: str = simpledialog.askstring(prompt="Nome do jogador")
        self.player_name: str = ""

        # Instanciando o DOG Actor
        self.dog: DogActor = DogActor()

        # Inicializando o DOG Actor
        message = self.dog.initialize(self.player_name, self)

        # Notificando o usuário acerca do estado da conexão com o DOG
        messagebox.showinfo(message=message)
        self.root.mainloop()

    def load_assets(self) -> dict[str, tk.PhotoImage]:
        if self.theme == Theme.DEFAULT:
            assets_subdirectory = "default"
        else:
            assets_subdirectory = "alternative"
        asset_dir_path = RESOURCES_DIR / assets_subdirectory
        assets = {}

        menu_image_path = asset_dir_path / "menu_image.png"
        menu_image = Image.open(menu_image_path).resize((WINDOW_WIDTH, WINDOW_HEIGHT))
        resized_menu_image = ImageTk.PhotoImage(menu_image)
        assets["menu_image"] = resized_menu_image

        menu_button_image_path = asset_dir_path / "menu_button.png"
        menu_button_image = Image.open(menu_button_image_path).resize(
            (int(WINDOW_WIDTH / 3.2), BOARD_HEIGHT // 7)
        )
        resized_menu_button_image = ImageTk.PhotoImage(menu_button_image)
        assets["menu_button"] = resized_menu_button_image

        board_image_path = asset_dir_path / "board.png"
        board_image = Image.open(board_image_path).resize((BOARD_WIDTH, BOARD_HEIGHT))
        resized_board_image = ImageTk.PhotoImage(board_image)
        assets["board"] = resized_board_image

        circle_image_path = asset_dir_path / "circle.png"
        circle_image = Image.open(circle_image_path).resize(
            (int(BOARD_WIDTH * 0.13), int(BOARD_HEIGHT * 0.13))
        )
        resized_circle_image = ImageTk.PhotoImage(circle_image)
        assets["circle"] = resized_circle_image

        # assets das pedras
        for color in [COLOR_A, COLOR_B]:
            for i in range(6):
                stone_name = color + str(i)
                stone_image_name = stone_name + ".png"
                stone_image_path = asset_dir_path / stone_image_name
                stone_image = Image.open(stone_image_path).resize(
                    (int(WINDOW_WIDTH * 0.09), int(WINDOW_HEIGHT * 0.09))
                )
                resized_stone_image = ImageTk.PhotoImage(stone_image)
                assets[stone_name] = resized_stone_image

        return assets

    def get_theme(self) -> Theme:
        return self.theme

    def set_theme(self, new_theme: Theme) -> None:
        self.theme = new_theme

    def switch_theme(self) -> None:
        theme = self.get_theme()
        if theme == Theme.DEFAULT:
            self.set_theme(Theme.ALTERNATIVE)
        else:
            self.set_theme(Theme.DEFAULT)
        self.assets = self.load_assets()
        self.main_menu_interface.update_widgets(self.assets)
        self.game_interface.update_widgets(self.assets)

    def populate_window(self) -> None:
        menubar = self.menu.nametowidget(self.menu.winfo_parent())
        self.root.config(menu=menubar)
        self.message_label.pack(fill=tk.X, side=tk.BOTTOM, expand=False)

    def receive_start(self, start_status: StartStatus) -> None:
        players = start_status.get_players()
        self.game_interface.start_match(players)
        self.go_to_game_screen()
        self.update_gui()
        messagebox.showinfo(message="Partida iniciada!")

    def receive_move(self, a_move) -> None:
        print("received move:", a_move)
        self.update_gui()

    def receive_withdrawal_notification(self) -> None:
        print("received withdrawal notification")
        self.update_gui()

    def is_main_screen_filled(self) -> bool:
        if self.main_frame is not None:
            return True
        else:
            return False

    def set_main_screen(self, new_frame: ttk.Frame) -> None:
        if self.is_main_screen_filled():
            self.main_frame.pack_forget()
        self.main_frame = new_frame
        self.main_frame.pack(fill=tk.BOTH, side=tk.TOP, anchor=tk.CENTER, expand=True)

    def go_to_main_menu_screen(self) -> None:
        main_menu_frame = self.main_menu_interface.get_frame()
        self.set_main_screen(main_menu_frame)

    def go_to_game_screen(self) -> None:
        game_frame = self.game_interface.get_frame()
        self.set_main_screen(game_frame)

    def start_match(self) -> None:
        answer = messagebox.askyesno("START", "Deseja iniciar uma nova partida?")
        if answer:
            game_state = self.game_interface.get_game_state()
            if game_state == GameState.TITLE:
                status: StartStatus = self.dog.start_match(2)
                code: str = status.get_code()
                message: str = status.get_message()
                if code == "0" or code == "1":
                    messagebox.showinfo(message=message)
                elif code == "2":
                    players = status.get_players()
                    self.game_interface.start_match(players)
                    self.go_to_game_screen()
                    self.update_gui()
                    messagebox.showinfo(message=message)

    def go_to_main_menu(self):
        game_state = self.game_interface.get_game_state()
        if (
            game_state == GameState.MATCH_ENDED
            or game_state == GameState.ABANDONED_BY_OTHER_PLAYER
        ):
            self.go_to_main_menu_screen()

    def send_move(self, move: dict[str, str]) -> None:
        self.dog.send_move(move)

    def update_circle_visibility(self, index: int, state: str) -> None:
        self.game_interface.update_circle_visibility(index, state)

    def update_gui(self) -> None:
        # Atualizando o label de mensagens
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
        # atualizando os estados dos botões da barra de menu
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

    def exit_game(self) -> None:
        sys.exit(0)
