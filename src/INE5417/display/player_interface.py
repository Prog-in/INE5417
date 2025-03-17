import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk

from ttkthemes import ThemedTk

from src.INE5417.dog.dog_actor import DogActor
from src.INE5417.dog.dog_interface import DogPlayerInterface
from src.INE5417.logic.board import Board
from src.INE5417.utils.constants import GAME_NAME, WINDOW_GEOMETRY, RESOURCES_DIR, FONT
from src.INE5417.utils.game_state import GameState


class PlayerInterface(DogPlayerInterface):
    def __init__(self) -> None:
        super().__init__()
        self.dog: DogActor = DogActor()
        self.root: tk.Tk = ThemedTk(theme="Equilux")
        # self.root: tk.Tk = ThemedTk(theme="Adapta")
        self.board: Board = Board()
        self.player_name: str = self.get_player_name()
        self.assets: dict[str, tk.PhotoImage] = self.load_assets()
        self.menu_file: tk.Menu
        self.populate_window()
        self.initialize_dog()
        self.update_game_state()
        self.root.mainloop()


    def get_player_name(self) -> str:
        name = simpledialog.askstring(title=GAME_NAME, prompt="Nome do jogador")
        if name:
            return name
        return "User"


    def load_assets(self) -> dict[str, tk.PhotoImage]:
        assets = {}
        extension = ".png"

        board_file = RESOURCES_DIR / f"board{extension}"

        assets["board"] = tk.PhotoImage(file=board_file)

        # assets dos triângulos
        # for i in range(12):
        #     name = "triangle" + str(i)
        #     assets[name] = tk.PhotoImage(file=RESOURCES_DIR + name + extension)

        # assets das pedras
        for i in range(6):
            color_a = "red" + str(i)
            color_a_file = RESOURCES_DIR / f"{color_a}{extension}"
            assets[color_a] = tk.PhotoImage(file=color_a)

            color_b = "black" + str(i)
            color_b_file = RESOURCES_DIR / f"{color_b}{extension}"
            assets[color_b] = tk.PhotoImage(file=color_b_file)

        return assets


    def populate_window(self) -> None:
        self.root.title(GAME_NAME)
        self.root.geometry(WINDOW_GEOMETRY)
        self.root.resizable(False, False)
        # self.root.iconbitmap()

        # logo_frame = ttk.Frame(self.root)
        # logo_frame.pack(fill=tk.X, side = tk.TOP, expand=True)

        board_frame = ttk.Frame(self.root)
        board_frame.pack(fill=tk.X, side = tk.TOP, expand=True)

        message_frame = ttk.Frame(self.root)
        message_frame.pack(fill=tk.BOTH, side = tk.TOP, expand=False)

        # Setting the image of the logo inside the frame for the logo
        # logo = tk.PhotoImage(file="images/logo.png")
        # ttk.Label(self.logo_frame, image=self.logo).grid(row=0, column=0)

        message_label = ttk.Label(message_frame, text=GAME_NAME, font=FONT)
        message_label.grid(row=0, column=1)

        self.initialize_menubar()

    def initialize_menubar(self) -> None:
        menubar = tk.Menu(self.root)
        menubar.option_add('*tearOff', tk.FALSE)
        self.root['menu'] = menubar

        self.menu_file = tk.Menu(menubar, bg="#FFFFFF")
        menubar.add_cascade(menu=self.menu_file, label="Menu")

        # menu_file.add_command(label="Regras", command= self.rules_window_child,
        #                            activebackground="#A7CCE7", activeforeground="#000")
        self.menu_file.add_command(label="Iniciar partida", command=self.start_match,
                                   activebackground="#A7CCE7", activeforeground="#000")
        self.menu_file.add_command(label="Reiniciar jogo", command=self.start_game,
                                   activebackground="#A7CCE7", activeforeground="#000")
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Sair", command=self.end_window,
                                   activebackground="#EA9E9E", activeforeground="#000")


    def initialize_dog(self) -> None:
        message = "Boas vindas, " + self.player_name + "!"
        messagebox.showinfo(title=GAME_NAME, message=message)

        message = self.dog.initialize(self.player_name, self) + "!"
        messagebox.showinfo(title="Dog Server", message=message)


    def start_game(self):
        game_state = self.board.get_game_state()
        if game_state.MATCH_ENDED or game_state.ABANDONED_BY_OTHER_PLAYER:
            self.board.reset_game()
            game_state = self.board.get_status()
            self.update_gui(game_state)


    def receive_start(self, start_status):
        self.start_game()
        players = start_status.get_players()
        self.board.start_match(players)
        game_state = self.board.get_status()
        self.update_gui(game_state)


    def receive_move(self, a_move):
        self.board.receive_move(a_move)
        gui_state = self.board.get_status()
        self.update_gui(gui_state)


    def receive_withdrawal_notification(self):
        self.board.receive_withdrawal_notification()
        game_state = self.board.get_status()
        self.update_gui(game_state)


    def start_match(self):
        game_state = self.board.get_game_state()
        if game_state.TITLE:
            answer = messagebox.askyesno("START", "Deseja iniciar uma nova partida?")
            if answer:
                status = self.dog.start_match(2)
                code = status.get_code()
                message = status.get_message()
                if code == "0" or code == "1":
                    messagebox.showinfo(title=GAME_NAME, message=message)
                else:
                    players = status.get_players()
                    # local_player_id = status.get_local_id()
                    self.board.start_match(players)
                    game_state = self.board.get_status()
                    self.update_gui(game_state)
                    messagebox.showinfo(title=GAME_NAME, message=status.get_message())


    def update_game_state(self) -> None:
        ...


    def update_gui(self, gui_state) -> None:
        ...


    def update_menu_status(self):
        game_state = self.board.get_game_state()
        if game_state == GameState.MATCH_ENDED or game_state == GameState.ABANDONED_BY_OTHER_PLAYER:
            self.menu_file.entryconfigure("Reiniciar jogo", state="normal")
        else:
            self.menu_file.entryconfigure("Reiniciar jogo", state="disabled")
        if game_state == GameState.TITLE:
            self.menu_file.entryconfigure("Iniciar partida", state="normal")
        else:
            self.menu_file.entryconfigure("Iniciar partida", state="disabled")


    def end_window(self):
        quit()
