# Let's combine the three README files into one.
# We'll preserve their headings, content, and avoid repeating the MIT License three times — instead, we'll put it once at the end.

# Extracted contents from the search results
readme1 = """# 🔑 Random Password Generator (Advanced)

A professional Tkinter-based desktop app for generating secure passwords with multiple customization options, password history, themes, and export to `.exe`.

---

## ✨ Features
- 🎨 **Themes** — Light, Dark, and Ocean styles.
- 📊 **Password Strength Indicator** — Color-coded Weak, Medium, Strong.
- 🔁 **Auto-generate on startup**.
- 💾 **Save to File** — Save passwords in a `.txt` file.
- 📋 **Password History** — Keep track of recently generated passwords.
- 🔒 **Avoid Similar Characters** — Exclude confusing characters like `O/0` or `l/1`.
- 📈 **Strength Level Selection** — Weak, Medium, Strong, or Custom settings.

---

## 📥 Installation
1. **Clone or Download** this repository.
2. Make sure you have **Python 3.10+** installed.
3. Install required dependencies:
   ```bash
   pip install tk
"""

readme2 = """# 🎮 Rock Paper Scissors — GUI Version

A fun and colorful **Rock, Paper, Scissors** game built using **Python's Tkinter** library.  
Players can enter their name, play multiple rounds, track scores, and restart anytime.  

---

## 📌 Features
- **Player Name Input** — Personalizes the score display.
- **Themed Colors** — Clean dark theme with green/red/yellow for results.
- **Three Buttons in One Row** — Rock, Paper, Scissors aligned horizontally.
- **Score Tracking** — Keeps track of your wins vs. the computer.
- **Play Again** — Quickly start the next round without resetting scores.
- **Reset Game** — Resets both player and computer scores.
- **Responsive Layout** — Buttons and text adjust neatly in the window.

---

## 🛠️ Requirements
- Python 3.x
- Tkinter (comes pre-installed with Python)
- No extra libraries required.

---

## ▶️ How to Run
1. **Clone or Download** the project folder.
2. Open a terminal or command prompt inside the folder.
3. Run:
   ```bash
   python rps_gui.py
"""
readme3 = """# Tic Tac Toe with AI & Themes

A feature-rich **Tic Tac Toe** game built using **Python's Tkinter** library.  
Supports **Player vs Player** and **Player vs AI** modes, multiple themes, a timer, score tracking, undo moves, and persistent score saving.

---

## 🎮 Features
- **Two Game Modes**:
  - Player vs Player (PvP)
  - Player vs AI (PvAI)
- **Three Themes**:
  - Classic
  - Dark
  - Ocean
- **Score Tracking**:
  - Saves scores persistently in `tic_tac_toe_scores.pkl`
  - Separate counts for Player X, Player O, and Draws
- **Restart Options**:
  - Restart game (board reset)
  - Restart All (reset scores + board)
- **Undo Last Move** button
- **Timer** to track game duration
- **Responsive Button Grid** for a clean look

---

## 📂 Files
- `tic_tac_toe_ai.py` — Main game file
- `tic_tac_toe_scores.pkl` — Automatically created for storing scores

---

## 🛠 Requirements
- Python 3.x
- Tkinter (comes pre-installed with Python on most systems)

---

## ▶ How to Run
1. Make sure you have Python 3 installed.
2. Save the file `tic_tac_toe_ai.py` to a folder.
3. Open a terminal/command prompt in that folder.
4. Run:
   ```bash
   python tic_tac_toe_ai.py
"""

license_text = """---

## 📄 License

MIT License

Copyright (c) 2025 Surbhi Bari

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell  
copies of the Software, and to permit persons to whom the Software is  
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all  
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  
SOFTWARE.
"""

combined_content = f"{readme1}\n\n{readme2}\n\n{readme3}\n\n{license_text}"

# Save to a new README file
output_path = "/mnt/data/COMBINED_README.md"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(combined_content)

output_path
