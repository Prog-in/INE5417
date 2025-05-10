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
from ..utils.move_type import MoveType
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

    def get_default_theme(self) -> Theme:
        return Theme.DEFAULT

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

        stone_colora_0_image_path = asset_dir_path / (COLOR_A + "0.png")
        stone_colora_0_image = Image.open(stone_colora_0_image_path).resize(
            (int(WINDOW_WIDTH * 0.09), int(WINDOW_HEIGHT * 0.09))
        )
        resized_stone_colora_0_image = ImageTk.PhotoImage(stone_colora_0_image)
        assets[COLOR_A + "0"] = resized_stone_colora_0_image

        stone_colora_1_image_path = asset_dir_path / (COLOR_A + "1.png")
        stone_colora_1_image = Image.open(stone_colora_1_image_path).resize(
            (int(WINDOW_WIDTH * 0.09), int(WINDOW_HEIGHT * 0.09))
        )
        resized_stone_colora_1_image = ImageTk.PhotoImage(stone_colora_1_image)
        assets[COLOR_A + "1"] = resized_stone_colora_1_image

        stone_colora_2_image_path = asset_dir_path / (COLOR_A + "2.png")
        stone_colora_2_image = Image.open(stone_colora_2_image_path).resize(
            (int(WINDOW_WIDTH * 0.09), int(WINDOW_HEIGHT * 0.09))
        )
        resized_stone_colora_2_image = ImageTk.PhotoImage(stone_colora_2_image)
        assets[COLOR_A + "2"] = resized_stone_colora_2_image

        stone_colora_3_image_path = asset_dir_path / (COLOR_A + "3.png")
        stone_colora_3_image = Image.open(stone_colora_3_image_path).resize(
            (int(WINDOW_WIDTH * 0.09), int(WINDOW_HEIGHT * 0.09))
        )
        resized_stone_colora_3_image = ImageTk.PhotoImage(stone_colora_3_image)
        assets[COLOR_A + "3"] = resized_stone_colora_3_image

        stone_colora_4_image_path = asset_dir_path / (COLOR_A + "4.png")
        stone_colora_4_image = Image.open(stone_colora_4_image_path).resize(
            (int(WINDOW_WIDTH * 0.09), int(WINDOW_HEIGHT * 0.09))
        )
        resized_stone_colora_4_image = ImageTk.PhotoImage(stone_colora_4_image)
        assets[COLOR_A + "4"] = resized_stone_colora_4_image

        stone_colora_5_image_path = asset_dir_path / (COLOR_A + "5.png")
        stone_colora_5_image = Image.open(stone_colora_5_image_path).resize(
            (int(WINDOW_WIDTH * 0.09), int(WINDOW_HEIGHT * 0.09))
        )
        resized_stone_colora_5_image = ImageTk.PhotoImage(stone_colora_5_image)
        assets[COLOR_A + "5"] = resized_stone_colora_5_image

        stone_colorb_0_image_path = asset_dir_path / (COLOR_B + "0.png")
        stone_colorb_0_image = Image.open(stone_colorb_0_image_path).resize(
            (int(WINDOW_WIDTH * 0.09), int(WINDOW_HEIGHT * 0.09))
        )
        resized_stone_colorb_0_image = ImageTk.PhotoImage(stone_colorb_0_image)
        assets[COLOR_B + "0"] = resized_stone_colorb_0_image

        stone_colorb_1_image_path = asset_dir_path / (COLOR_B + "1.png")
        stone_colorb_1_image = Image.open(stone_colorb_1_image_path).resize(
            (int(WINDOW_WIDTH * 0.09), int(WINDOW_HEIGHT * 0.09))
        )
        resized_stone_colorb_1_image = ImageTk.PhotoImage(stone_colorb_1_image)
        assets[COLOR_B + "1"] = resized_stone_colorb_1_image

        stone_colorb_2_image_path = asset_dir_path / (COLOR_B + "2.png")
        stone_colorb_2_image = Image.open(stone_colorb_2_image_path).resize(
            (int(WINDOW_WIDTH * 0.09), int(WINDOW_HEIGHT * 0.09))
        )
        resized_stone_colorb_2_image = ImageTk.PhotoImage(stone_colorb_2_image)
        assets[COLOR_B + "2"] = resized_stone_colorb_2_image

        stone_colorb_3_image_path = asset_dir_path / (COLOR_B + "3.png")
        stone_colorb_3_image = Image.open(stone_colorb_3_image_path).resize(
            (int(WINDOW_WIDTH * 0.09), int(WINDOW_HEIGHT * 0.09))
        )
        resized_stone_colorb_3_image = ImageTk.PhotoImage(stone_colorb_3_image)
        assets[COLOR_B + "3"] = resized_stone_colorb_3_image

        stone_colorb_4_image_path = asset_dir_path / (COLOR_B + "4.png")
        stone_colorb_4_image = Image.open(stone_colorb_4_image_path).resize(
            (int(WINDOW_WIDTH * 0.09), int(WINDOW_HEIGHT * 0.09))
        )
        resized_stone_colorb_4_image = ImageTk.PhotoImage(stone_colorb_4_image)
        assets[COLOR_B + "4"] = resized_stone_colorb_4_image

        stone_colorb_5_image_path = asset_dir_path / (COLOR_B + "5.png")
        stone_colorb_5_image = Image.open(stone_colorb_5_image_path).resize(
            (int(WINDOW_WIDTH * 0.09), int(WINDOW_HEIGHT * 0.09))
        )
        resized_stone_colorb_5_image = ImageTk.PhotoImage(stone_colorb_5_image)
        assets[COLOR_B + "5"] = resized_stone_colorb_5_image

        return assets

    def set_main_frame(self, new_frame: ttk.Frame) -> None:
        self.main_frame = new_frame

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
        self.main_menu_interface.update_widgets_images(self.assets)
        self.game_interface.update_widgets_images(self.assets)

    def populate_window(self) -> None:
        menubar = self.menu.nametowidget(self.menu.winfo_parent())
        self.root.config(menu=menubar)
        self.message_label.pack(fill=tk.X, side=tk.BOTTOM, expand=False)

    def receive_start(self, start_status: StartStatus) -> None:
        game_state = self.game_interface.get_game_state()
        if game_state == GameState.MAIN_MENU:
            players = start_status.get_players()
            self.game_interface.start_match(players)
            self.game_interface.initialize_frame(COLOR_B, COLOR_A)
            game_frame = self.game_interface.get_frame()
            is_main_screen_filled = self.is_main_screen_filled()
            if is_main_screen_filled:
                self.main_frame.pack_forget()
            self.set_main_frame(game_frame)
            self.main_frame.pack(
                fill=tk.BOTH, side=tk.TOP, anchor=tk.CENTER, expand=True
            )
            self.game_interface.set_game_state(GameState.REMOTE_PLAYER_TO_MOVE)
            self.update_gui()
            messagebox.showinfo(message="Partida iniciada!")

    def receive_move(self, a_move) -> None:
        print("received move:", a_move)
        game_state = self.game_interface.get_game_state()
        if game_state == GameState.REMOTE_PLAYER_TO_MOVE:
            self.game_interface.receive_move(a_move)
        self.update_board()
        self.update_gui()

    def receive_withdrawal_notification(self) -> None:
        game_state = self.game_interface.get_game_state()
        if game_state == GameState.LOCAL_PLAYER_TO_MOVE or GameState.REMOTE_PLAYER_TO_MOVE:
            self.game_interface.set_game_state(GameState.ABANDONED_BY_OTHER_PLAYER)
            self.update_gui()

    def update_board(self) -> None:
        ...

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
                status: StartStatus = self.dog.start_match(2)
                message: str = status.get_message()
                code: str = status.get_code()
                if code == "0" or code == "1":
                    messagebox.showinfo(message=message)
                elif code == "2":
                    players = status.get_players()
                    self.game_interface.start_match(players)
                    # TODO: verificar o que acontece ao iniciar uma segunda partida
                    self.game_interface.initialize_frame(COLOR_A, COLOR_B)
                    game_frame = self.game_interface.get_frame()
                    is_main_screen_filled = self.is_main_screen_filled()
                    if is_main_screen_filled:
                        self.main_frame.pack_forget()
                    self.set_main_frame(game_frame)
                    self.main_frame.pack(
                        fill=tk.BOTH, side=tk.TOP, anchor=tk.CENTER, expand=True
                    )
                    self.game_interface.set_game_state(GameState.LOCAL_PLAYER_TO_MOVE)
                    self.update_gui()
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

    def send_move(self, move: dict[str, str]) -> None:
        self.dog.send_move(move)

    def update_circle_visibility(self, index: int, state: str) -> None:
        self.game_interface.update_circle_visibility(index, state)

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
                message += "Partida encerrada"
            case GameState.ABANDONED_BY_OTHER_PLAYER:
                message += "Partida abandonada pelo outro jogador"
        self.message_label.configure(text=message)
        self.message_label.update()

        print("update: game_state =", game_state)
        # atualizando os estados dos botões da barra de menu
        if (
            game_state == GameState.GAME_OVER
            or game_state == GameState.ABANDONED_BY_OTHER_PLAYER
        ):
            self.menu.entryconfigure(1, state=tk.NORMAL)
        else:
            self.menu.entryconfigure(1, state=tk.DISABLED)

        if (
            game_state == GameState.LOCAL_PLAYER_TO_MOVE
            or game_state == GameState.REMOTE_PLAYER_TO_MOVE
        ):
            self.menu.entryconfigure(2, state=tk.NORMAL)
        else:
            self.menu.entryconfigure(2, state=tk.DISABLED)

        if (
                game_state == GameState.GAME_OVER
                or game_state == GameState.ABANDONED_BY_OTHER_PLAYER
        ):
            self.menu.entryconfigure(4, state=tk.NORMAL)
        else:
            self.menu.entryconfigure(4, state=tk.DISABLED)
        self.menu.update()

    def exit_game(self) -> None:
        sys.exit(0)
