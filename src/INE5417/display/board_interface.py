import tkinter as tk
import tkinter.ttk

class BoardInterface:
    def __init__(self, root: tk.Tk):
        self.board_frame: ttk.Frame = ttk.Frame(root)
        
    def get_board_frame(self):
        return self.board_frame
