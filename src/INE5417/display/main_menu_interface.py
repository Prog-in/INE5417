import tkinter as tk
from tkinter import ttk

from .abstract_helper_interface import AbstractHelperInterface
from ..utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT


class MainMenuInterface(AbstractHelperInterface):
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
            lambda event: self.player_interface.go_to_game_screen(),
        )
        menu_canvas.grid(row=0, column=0, sticky=tk.NSEW)

        return menu_frame
