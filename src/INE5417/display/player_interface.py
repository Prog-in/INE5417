import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import ImageTk, Image
from tkinter import ttk

from ttkthemes import ThemedTk

from src.INE5417.dog.dog_actor import DogActor
from src.INE5417.dog.dog_interface import DogPlayerInterface
from src.INE5417.logic.board import Board
from src.INE5417.utils.constants import GAME_NAME, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_GEOMETRY, RESOURCES_DIR, FONT, \
    BOARD_WIDTH, BOARD_HEIGHT, BOARD_FACTOR
from src.INE5417.utils.game_state import GameState


class PlayerInterface(DogPlayerInterface):
    def __init__(self) -> None:
        super().__init__()
        self.root: tk.Tk = tk.Tk()
        s = ttk.Style(self.root)
        s.theme_use("clam")
        s.configure("flat.TButton", borderwidth=0, bg="")
        self.board: Board = Board()
        self.assets: dict[str, ImageTk.PhotoImage] = self.load_assets()
        self.populate_window()
        self.menu_file: tk.Menu = self.initialize_menubar()
        self.player_name: str = self.get_player_name()
        self.dog: DogActor = DogActor()
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
        board_image = Image.open(board_file).resize((BOARD_WIDTH, BOARD_HEIGHT))
        assets["board"] = ImageTk.PhotoImage(board_image)

        # assets dos triângulos
        # for i in range(12):
        #     name = "triangle" + str(i)
        #     assets[name] = tk.PhotoImage(file=RESOURCES_DIR + name + extension)

        # assets das pedras
        for i in range(6):
            color_a = "red" + str(i)
            color_a_file = RESOURCES_DIR / f"{color_a}{extension}"
            color_a_image = Image.open(color_a_file).resize((int(WINDOW_WIDTH * 0.09), int(WINDOW_HEIGHT * 0.09)))
            assets[color_a] = ImageTk.PhotoImage(color_a_image)

            color_b = "black" + str(i)
            color_b_file = RESOURCES_DIR / f"{color_b}{extension}"
            color_b_image = Image.open(color_b_file).resize((int(WINDOW_WIDTH * 0.09), int(WINDOW_HEIGHT * 0.09)))
            assets[color_b] = ImageTk.PhotoImage(color_b_image)

        return assets


    def populate_window(self) -> None:
        self.root.title(GAME_NAME)
        self.root.geometry(WINDOW_GEOMETRY)
        self.root.resizable(False, False)
        # self.root.iconbitmap()

        # logo_frame = ttk.Frame(self.root)
        # logo_frame.pack(fill=tk.X, side = tk.TOP, expand=True)

        game_frame = ttk.Frame(self.root)
        game_frame.pack(fill=tk.X, side = tk.TOP, expand=True)

        message_frame = ttk.Frame(self.root)
        message_frame.pack(fill=tk.BOTH, side = tk.TOP, expand=False)

        # Setting the image of the logo inside the frame for the logo
        # logo = tk.PhotoImage(file="images/logo.png")
        # ttk.Label(self.logo_frame, image=self.logo).grid(row=0, column=0)

        canvas_board = tk.Canvas(game_frame, width=BOARD_WIDTH, height=BOARD_HEIGHT)
        canvas_board.create_image(BOARD_WIDTH // 2, BOARD_HEIGHT // (2 - 0.15), image=self.assets["board"])
        triangles_rel_coordinates = (
            (0.495, 0.15),
        )
        for i in range(1):
            relx, rely = triangles_rel_coordinates[i]
            factor = 0.01
            button_triangle = tk.Button(canvas_board, width=int(BOARD_WIDTH * factor), height=int(BOARD_WIDTH * factor * 11/20), bg=self.root.cget("bg"), borderwidth=0)
            button_triangle.place(relx=relx, rely=rely)

        canvas_board.grid(row=0, column=2, sticky=tk.NSEW, rowspan=6)

        for row in range(6):
            button1_stone_colora = ttk.Button(game_frame, image=self.assets[f"red{row}"], style='flat.TButton')
            button2_stone_colora = ttk.Button(game_frame, image=self.assets[f"red{row}"], style='flat.TButton')
            button1_stone_colorb = ttk.Button(game_frame, image=self.assets[f"black{row}"], style='flat.TButton')
            button2_stone_colorb = ttk.Button(game_frame, image=self.assets[f"black{row}"], style='flat.TButton')
            button1_stone_colora.grid(row=row, column=0, sticky=tk.W, padx=0, pady=0)
            button2_stone_colora.grid(row=row, column=1, sticky=tk.W, padx=0, pady=0)
            button1_stone_colorb.grid(row=row, column=3, sticky=tk.E, padx=0, pady=0)
            button2_stone_colorb.grid(row=row, column=4, sticky=tk.E, padx=0, pady=0)

        message_label = ttk.Label(message_frame, text=GAME_NAME, font=FONT)
        message_label.grid(row=0, column=1)


    def initialize_menubar(self) -> tk.Menu:
        menubar = tk.Menu(self.root)
        menubar.option_add('*tearOff', tk.FALSE)
        self.root['menu'] = menubar

        menu_file = tk.Menu(menubar, bg="#FFFFFF")
        menubar.add_cascade(menu=menu_file, label="Menu")

        # menu_file.add_command(label="Regras", command= self.rules_window_child,
        #                            activebackground="#A7CCE7", activeforeground="#000")
        menu_file.add_command(label="Iniciar partida", command=self.start_match,
                                   activebackground="#A7CCE7", activeforeground="#000")
        menu_file.add_command(label="Reiniciar jogo", command=self.start_game,
                                   activebackground="#A7CCE7", activeforeground="#000")
        menu_file.add_separator()
        menu_file.add_command(label="Sair", command=self.end_window,
                                   activebackground="#EA9E9E", activeforeground="#000")
        return menu_file


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
