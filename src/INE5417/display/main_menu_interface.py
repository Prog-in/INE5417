import tkinter as tk
from tkinter import ttk

from .AbstractHelperInterface import AbstractHelperInterface
from ..utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT


class MainMenuInterface(AbstractHelperInterface):
    def __init__(self, root: tk.Tk, assets: dict[str, tk.PhotoImage], player_interface):
        super().__init__(root, assets)
        self.player_interface = player_interface

    def initialize_frame(self) -> ttk.Frame:
        menu_frame = ttk.Frame(self.root)

        # TODO: adicionar a logo no menu
        # logo_frame = ttk.Frame(self.root)
        # logo_frame.pack(fill=tk.X, side = tk.TOP, expand=True)

        # Setting the image of the logo inside the frame for the logo
        # logo = tk.PhotoImage(file="images/logo.png")
        # ttk.Label(self.logo_frame, image=self.logo).grid(row=0, column=0)

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
            lambda event: self.player_interface.start_match(),
        )
        menu_canvas.grid(row=0, column=0, sticky=tk.NSEW)

        return menu_frame
