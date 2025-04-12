import tkinter as tk
from abc import ABC, abstractmethod
from tkinter import ttk


class AbstractHelperInterface(ABC):
    def __init__(
        self, root: tk.Tk, assets: dict[str, tk.PhotoImage], player_interface
    ) -> None:
        super().__init__()
        self.root: tk.Tk = root
        self.assets: dict[str, tk.PhotoImage] = assets
        self.player_interface = player_interface
        self.frame: ttk.Frame | None = None

    @abstractmethod
    def initialize_frame(self) -> ttk.Frame:
        pass

    @abstractmethod
    def update_widgets(self, new_assets: dict[str, tk.PhotoImage]) -> None:
        pass

    def get_frame(self) -> ttk.Frame:
        if self.frame is None:
            self.frame = self.initialize_frame()
        return self.frame
