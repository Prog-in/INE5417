import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk

from PIL import ImageTk, Image

from .game_interface import GameInterface
from .main_menu_interface import MainMenuInterface
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

class PlayerInterface:
    def __init__(self) -> None:
        super().__init__()
        self.root: tk.Tk = tk.Tk()
        self.assets: dict[str, ImageTk.PhotoImage] = self.load_assets()
        self.main_menu_interface: MainMenuInterface = MainMenuInterface(
            self.root, self.assets, self
        )
        self.game_interface: GameInterface = GameInterface(self.root, self.assets)
        self.main_frame: ttk.Frame | None = None
        self.message_label: ttk.Label | None = None
        self.menu_file: tk.Menu | None = None
        self.populate_window()
        self.player_name: str = self.get_player_name()
        self.root.mainloop()

    def get_player_name(self) -> str:
        name = simpledialog.askstring(title=GAME_NAME, prompt="Nome do jogador")
        return name if name else "User"

    def load_asset(
        self, asset_name: str, extension: str, dimensions: tuple[int, int]
    ) -> ImageTk.PhotoImage:
        asset_file = (
            RESOURCES_DIR / "default" / f"{asset_name}.{extension}"
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

    def initialize_message_label(self) -> None:
        message_frame = ttk.Frame(self.root)
        self.message_label = ttk.Label(message_frame, font=FONT, text="Label de mensagens")
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
        )
        self.menu_file.add_command(
            label="Trocar conjunto de imagens",
            command=lambda: print("Botão para trocar conjunto de imagens pressionado"),
            activebackground="#A7CCE7",
            activeforeground="#000",
        )
        self.menu_file.add_separator()
        self.menu_file.add_command(
            label="Sair",
            command=lambda: print("Botão para encerrar o programa localmente pressionado"),
            activebackground="#EA9E9E",
            activeforeground="#000",
        )

    def set_main_frame(self, new_frame: ttk.Frame) -> None:
        if self.main_frame is not None:
            self.main_frame.destroy()
        self.main_frame = new_frame
        # FIXME: problema ao retornar ao menu principal apertando o respectivo botão
        self.main_frame.pack(fill=tk.BOTH, side=tk.TOP, anchor=tk.CENTER, expand=True)

    def goto_main_menu(self) -> None:
        self.set_main_frame(self.main_menu_interface.get_frame())

    def goto_game_screen(self) -> None:
        self.set_main_frame(self.game_interface.get_frame())

    def go_to_main_menu(self) -> None:
        print("Botão para ir ao menu principal pressionado")
        self.goto_main_menu()

    def go_to_game_screen(self) -> None:
        print("Botão para ir à tela de partida pressionado")
        self.goto_game_screen()
