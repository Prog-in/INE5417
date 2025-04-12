import tkinter as tk
from abc import ABC, abstractmethod
from tkinter import ttk


class AbstractHelperInterface(ABC):
    def __init__(self, root: tk.Tk, assets: dict[str, tk.PhotoImage]) -> None:
        super().__init__()
        self.root: tk.Tk = root
        self.assets: dict[str, tk.PhotoImage] = assets
        self.frame: ttk.Frame = self.initialize_frame()

    @abstractmethod
    def initialize_frame(self) -> ttk.Frame:
        pass

    def get_frame(self):
        if not self.frame.winfo_exists():
            self.frame = self.initialize_frame()
        return self.frame
