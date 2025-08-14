import tkinter as tk
import random

# Initialize scores and player name
user_score = 0
comp_score = 0
player_name = "Player"

# Themes
themes = {
    "Classic Light": {"bg": "#f0f0f0", "fg": "#000000", "btn_bg": "#ffffff", "btn_fg": "#000000"},
    "Dark": {"bg": "#2b2b2b", "fg": "#ffffff", "btn_bg": "#444444", "btn_fg": "#ffffff"},
    "Ocean": {"bg": "#003366", "fg": "#ffffff", "btn_bg": "#005599", "btn_fg": "#ffffff"}
}
current_theme = "Classic Light"

# Game logic
def determine_winner(user_choice):
    global user_score, comp_score
    options = ['Rock', 'Paper', 'Scissors']
    comp_choice = random.choice(options)

    if user_choice == comp_choice:
        result = f"It's a tie! You both chose {user_choice}."
        result_label.config(fg="orange")
    elif (
        (user_choice == 'Rock' and comp_choice == 'Scissors') or
        (user_choice == 'Scissors' and comp_choice == 'Paper') or
        (user_choice == 'Paper' and comp_choice == 'Rock')
    ):
        result = f"You win! {user_choice} beats {comp_choice}."
        user_score += 1
        result_label.config(fg="lightgreen")
    else:
        result = f"You lose! {comp_choice} beats {user_choice}."
        comp_score += 1
        result_label.config(fg="red")

    result_label.config(text=result)
    score_label.config(text=f"Score — {player_name}: {user_score}  Computer: {comp_score}")
    play_again_btn.config(state="normal")

# Reset scores
def reset_game():
    global user_score, comp_score
    user_score = 0
    comp_score = 0
    score_label.config(text=f"Score — {player_name}: 0  Computer: 0")
    result_label.config(text="Make your move!", fg=themes[current_theme]["fg"])
    play_again_btn.config(state="disabled")

# Play another round without resetting scores
def play_again():
    result_label.config(text="Make your move!", fg=themes[current_theme]["fg"])
    play_again_btn.config(state="disabled")

# Change theme
def change_theme(theme_name):
    global current_theme
    current_theme = theme_name
    theme = themes[theme_name]
    game_window.config(bg=theme["bg"])
    title_label.config(bg=theme["bg"], fg=theme["fg"])
    score_label.config(bg=theme["bg"], fg=theme["fg"])
    result_label.config(bg=theme["bg"], fg=theme["fg"])
    reset_btn.config(bg=theme["btn_bg"], fg=theme["btn_fg"])
    play_again_btn.config(bg=theme["btn_bg"], fg=theme["btn_fg"])
    for btn in game_buttons:
        btn.config(bg=theme["btn_bg"], fg=theme["btn_fg"])
    theme_menu.config(bg=theme["btn_bg"], fg=theme["btn_fg"])

# Start Game
def start_game():
    global player_name
    name = name_entry.get().strip()
    if name:
        player_name = name
    intro_window.destroy()
    launch_game_window()

# Launch Game Window
def launch_game_window():
    global game_window, title_label, score_label, result_label, reset_btn, play_again_btn, game_buttons, theme_menu

    game_window = tk.Tk()
    game_window.title("Rock Paper Scissors")
    game_window.geometry("450x420")
    game_window.resizable(False, False)

    # Title
    title_label = tk.Label(game_window, text=f"Rock, Paper, Scissors — {player_name}",
                           font=("Helvetica", 20, "bold"))
    title_label.pack(pady=(10, 5))

    # Score display
    score_label = tk.Label(game_window, text=f"Score — {player_name}: 0  Computer: 0",
                           font=("Helvetica", 14))
    score_label.pack(pady=(0, 10))

    # Buttons for choices
    frame = tk.Frame(game_window)
    frame.pack(pady=10)
    game_buttons = []
    for choice in ['Rock', 'Paper', 'Scissors']:
        btn = tk.Button(frame, text=choice, width=10, height=2, font=("Helvetica", 12, "bold"),
                        relief="raised", bd=3, command=lambda c=choice: determine_winner(c))
        btn.pack(side='left', padx=5)
        game_buttons.append(btn)

    # Result display
    result_label = tk.Label(game_window, text="Make your move!", font=("Helvetica", 14), pady=10)
    result_label.pack()

    # Play Again button
    play_again_btn = tk.Button(game_window, text="Play Again", command=play_again,
                               font=("Helvetica", 12, "bold"), relief="ridge", bd=3, state="disabled")
    play_again_btn.pack(pady=5)

    # Reset button
    reset_btn = tk.Button(game_window, text="Reset Game", command=reset_game,
                          font=("Helvetica", 12, "bold"), relief="ridge", bd=3)
    reset_btn.pack(pady=5)

    # Theme selection menu
    theme_menu = tk.Menubutton(game_window, text="Change Theme", relief="raised", bd=3,
                                font=("Helvetica", 12))
    theme_dropdown = tk.Menu(theme_menu, tearoff=0)
    for theme in themes:
        theme_dropdown.add_command(label=theme, command=lambda t=theme: change_theme(t))
    theme_menu.config(menu=theme_dropdown)
    theme_menu.pack(pady=5)

    change_theme(current_theme)
    game_window.mainloop()

# Intro Screen
intro_window = tk.Tk()
intro_window.title("Rock Paper Scissors - Welcome")
intro_window.geometry("400x250")
intro_window.resizable(False, False)

tk.Label(intro_window, text="Welcome to Rock, Paper, Scissors!", font=("Helvetica", 16, "bold")).pack(pady=10)
tk.Label(intro_window, text="Enter your name:", font=("Helvetica", 12)).pack(pady=5)
name_entry = tk.Entry(intro_window, font=("Helvetica", 12))
name_entry.pack(pady=5)

tk.Button(intro_window, text="Start Game", font=("Helvetica", 12, "bold"), command=start_game).pack(pady=20)

intro_window.mainloop()
