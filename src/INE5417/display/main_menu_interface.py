import tkinter as tk
from tkinter import ttk

from ..utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT


class MainMenuInterface:
    def __init__(
        self, root: tk.Tk, assets: dict[str, tk.PhotoImage], player_interface
    ) -> None:
        self.menu_canvas: tk.Canvas | None = None
        self.root: tk.Tk = root
        self.assets: dict[str, tk.PhotoImage] = assets
        self.player_interface = player_interface
        self.frame: ttk.Frame | None = None

    def get_frame(self) -> ttk.Frame:
        return self.frame

    def initialize_frame(self) -> None:
        self.frame = ttk.Frame(self.root)

        # TODO: adicionar a logo no menu
        # logo_frame = ttk.Frame(self.root)
        # logo_frame.pack(fill=tk.X, side = tk.TOP, expand=True)

        # Setting the image of the logo inside the frame for the logo
        # logo = tk.PhotoImage(file="images/logo.png")
        # ttk.Label(self.logo_frame, image=self.logo).grid(row=0, column=0)

        self.menu_canvas = tk.Canvas(
            self.frame, width=WINDOW_WIDTH, height=WINDOW_HEIGHT
        )
        self.menu_canvas.create_image(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2,
            image=self.assets["menu_image"],
            tags="menu_image",
        )
        menu_button = self.menu_canvas.create_image(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2,
            image=self.assets["menu_button"],
            tags="menu_button",
        )
        self.menu_canvas.tag_bind(
            menu_button,
            "<ButtonRelease-1>",
            lambda event: self.start_match(),
        )
        self.menu_canvas.grid(row=0, column=0, sticky=tk.NSEW)

    def start_match(self) -> None:
        self.player_interface.start_match()

    def update_widgets_images(self, assets: dict[str, tk.PhotoImage]) -> None:
        self.assets = assets
        self.menu_canvas.itemconfig("menu_image", image=self.assets["menu_image"])
        self.menu_canvas.itemconfig("menu_button", image=self.assets["menu_button"])
