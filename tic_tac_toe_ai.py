import tkinter as tk
from tkinter import messagebox, simpledialog
import random, pickle, os

# Score file
SCORE_FILE = "tic_tac_toe_scores.pkl"

# Themes
THEMES = {
    "Classic": {"bg": "white", "fg": "black", "btn_bg": "lightgray", "btn_fg": "black"},
    "Dark": {"bg": "#2E2E2E", "fg": "white", "btn_bg": "#4B4B4B", "btn_fg": "white"},
    "Ocean": {"bg": "#DFF6FF", "fg": "#006994", "btn_bg": "#006994", "btn_fg": "white"}
}

class TicTacToe:
    def __init__(self, root, mode, player_x_name, player_o_name):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.resizable(False, False)

        self.game_mode = mode
        self.player_x_name = player_x_name
        self.player_o_name = player_o_name
        self.theme_name = "Classic"
        self.theme = THEMES[self.theme_name]
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.history = []
        self.timer_running = False
        self.time_elapsed = 0
        self.timer_id = None

        self.scores = self.load_scores()
        self.create_ui()
        self.apply_theme()
        self.start_timer()

    def create_ui(self):
        # Score
        self.score_label = tk.Label(self.root, text=self.score_text(), font=("Arial", 14))
        self.score_label.grid(row=0, column=0, columnspan=3, pady=(5, 0))

        # Timer
        self.timer_label = tk.Label(self.root, text="Time: 0s", font=("Arial", 12))
        self.timer_label.grid(row=1, column=0, columnspan=3, pady=(0, 5))

        # Board buttons
        self.buttons = []
        for r in range(3):
            row_buttons = []
            for c in range(3):
                btn = tk.Button(self.root, text="", font=("Arial", 28, "bold"),
                                width=5, height=2, relief="solid", bd=2,
                                command=lambda row=r, col=c: self.make_move(row, col))
                btn.grid(row=r+2, column=c, padx=2, pady=2, sticky="nsew")
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        # Restart & Undo
        self.restart_button = tk.Button(self.root, text="Restart", command=self.reset_game, width=10)
        self.restart_button.grid(row=5, column=0, pady=5)

        self.undo_button = tk.Button(self.root, text="Undo", command=self.undo_move, width=10)
        self.undo_button.grid(row=5, column=1, pady=5)

        # Theme menu
        self.theme_var = tk.StringVar(value=self.theme_name)
        self.theme_menu = tk.OptionMenu(self.root, self.theme_var, *THEMES.keys(), command=self.change_theme)
        self.theme_menu.grid(row=5, column=2, pady=5)

        # Restart All
        self.restart_all_button = tk.Button(self.root, text="Restart All (Reset Scores)",
                                            command=self.reset_all, width=30)
        self.restart_all_button.grid(row=6, column=0, columnspan=3, pady=10)

    def apply_theme(self):
        self.theme = THEMES[self.theme_name]
        self.root.config(bg=self.theme["bg"])
        self.score_label.config(bg=self.theme["bg"], fg=self.theme["fg"])
        self.timer_label.config(bg=self.theme["bg"], fg=self.theme["fg"])
        for r in self.buttons:
            for b in r:
                b.config(bg=self.theme["btn_bg"], fg=self.theme["btn_fg"])
        self.restart_button.config(bg=self.theme["btn_bg"], fg=self.theme["btn_fg"])
        self.undo_button.config(bg=self.theme["btn_bg"], fg=self.theme["btn_fg"])
        self.restart_all_button.config(bg=self.theme["btn_bg"], fg=self.theme["btn_fg"])
        self.theme_menu.config(bg=self.theme["btn_bg"], fg=self.theme["btn_fg"])

    def change_theme(self, new_theme):
        self.theme_name = new_theme
        self.apply_theme()

    def score_text(self):
        return f"{self.player_x_name} (X): {self.scores['X']}  {self.player_o_name} (O): {self.scores['O']}  Draws: {self.scores['D']}"

    def save_scores(self):
        with open(SCORE_FILE, "wb") as f:
            pickle.dump(self.scores, f)

    def load_scores(self):
        if os.path.exists(SCORE_FILE):
            with open(SCORE_FILE, "rb") as f:
                return pickle.load(f)
        return {"X": 0, "O": 0, "D": 0}

    def make_move(self, row, col):
        if self.board[row][col] == "":
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            self.history.append((row, col))
            if self.check_winner(self.current_player):
                self.end_game(f"{self.get_player_name(self.current_player)} wins!")
                return
            elif self.is_draw():
                self.end_game("Draw!")
                return
            self.switch_player()

            if self.game_mode == "PvAI" and self.current_player == "O":
                self.root.after(500, self.ai_move)

    def ai_move(self):
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == "":
                    self.board[r][c] = "O"
                    if self.check_winner("O"):
                        self.buttons[r][c].config(text="O")
                        self.end_game(f"{self.player_o_name} wins!")
                        return
                    self.board[r][c] = ""

        for r in range(3):
            for c in range(3):
                if self.board[r][c] == "":
                    self.board[r][c] = "X"
                    if self.check_winner("X"):
                        self.board[r][c] = "O"
                        self.buttons[r][c].config(text="O")
                        if self.check_winner("O"):
                            self.end_game(f"{self.player_o_name} wins!")
                        else:
                            self.switch_player()
                        return
                    self.board[r][c] = ""

        empty = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == ""]
        if empty:
            r, c = random.choice(empty)
            self.board[r][c] = "O"
            self.buttons[r][c].config(text="O")
            if self.check_winner("O"):
                self.end_game(f"{self.player_o_name} wins!")
                return
            elif self.is_draw():
                self.end_game("Draw!")
                return
            self.switch_player()

    def get_player_name(self, symbol):
        return self.player_x_name if symbol == "X" else self.player_o_name

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self, player):
        for r in range(3):
            if all(self.board[r][c] == player for c in range(3)):
                return True
        for c in range(3):
            if all(self.board[r][c] == player for r in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)):
            return True
        if all(self.board[i][2-i] == player for i in range(3)):
            return True
        return False

    def is_draw(self):
        return all(self.board[r][c] != "" for r in range(3) for c in range(3))

    def end_game(self, result):
        if self.player_x_name in result:
            self.scores["X"] += 1
        elif self.player_o_name in result:
            self.scores["O"] += 1
        else:
            self.scores["D"] += 1
        self.save_scores()
        messagebox.showinfo("Game Over", result)
        self.reset_game()

    def reset_game(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for r in self.buttons:
            for b in r:
                b.config(text="")
        self.history.clear()
        self.current_player = "X"
        self.score_label.config(text=self.score_text())
        self.time_elapsed = 0

    def reset_all(self):
        self.scores = {"X": 0, "O": 0, "D": 0}
        self.save_scores()
        self.reset_game()

    def undo_move(self):
        if self.history:
            last_row, last_col = self.history.pop()
            self.board[last_row][last_col] = ""
            self.buttons[last_row][last_col].config(text="")
            self.switch_player()

    def start_timer(self):
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if self.timer_running:
            self.timer_label.config(text=f"Time: {self.time_elapsed}s")
            self.time_elapsed += 1
            self.timer_id = self.root.after(1000, self.update_timer)


def choose_game_mode():
    popup = tk.Tk()
    popup.title("Choose Game Mode")
    popup.geometry("300x200")
    popup.resizable(False, False)

    def select_mode(mode):
        player_x_name = simpledialog.askstring("Player X Name", "Enter name for Player X:")
        if not player_x_name:
            player_x_name = "Player X"

        if mode == "PvP":
            player_o_name = simpledialog.askstring("Player O Name", "Enter name for Player O:")
            if not player_o_name:
                player_o_name = "Player O"
        else:
            player_o_name = "Computer"

        popup.destroy()
        root = tk.Tk()
        TicTacToe(root, mode, player_x_name, player_o_name)
        root.mainloop()

    label = tk.Label(popup, text="Choose Game Mode", font=("Arial", 14))
    label.pack(pady=10)

    btn_pvp = tk.Button(popup, text="Player vs Player", width=20, command=lambda: select_mode("PvP"))
    btn_pvp.pack(pady=5)

    btn_pvai = tk.Button(popup, text="Player vs AI", width=20, command=lambda: select_mode("PvAI"))
    btn_pvai.pack(pady=5)

    popup.mainloop()


if __name__ == "__main__":
    choose_game_mode()
