import tkinter as tk
from tkinter import ttk

from ..utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT


class MainMenuInterface:
    def __init__(self, root: tk.Tk, assets: dict[str, tk.PhotoImage], player_interface):
        self.root: tk.Tk = root
        self.assets: dict[str, tk.PhotoImage] = assets
        self.player_interface = player_interface
        self.frame: ttk.Frame = self.initialize_frame()

    def get_frame(self):
        return self.frame

    def initialize_frame(self) -> ttk.Frame:
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
            lambda event: self.player_interface.start_match(),
        )
        menu_canvas.grid(row=0, column=0, sticky=tk.NSEW)

        return menu_frame
