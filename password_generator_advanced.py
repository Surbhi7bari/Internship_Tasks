import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import string
import pyperclip
import os

# ---------- Config ----------
SIMILAR_CHARS = set("O0oIl1")
THEMES = {
    "Light": {"bg": "#ffffff", "fg": "#000000", "entry_bg": "#ffffff"},
    "Dark": {"bg": "#000000", "fg": "#ffffff", "entry_bg": "#020202"},
    "Ocean": {"bg": "#215e6f", "fg": "#ffffff", "entry_bg": "#458CA0"}
}
MAX_HISTORY = 10

# ---------- State ----------
password_history = []

# ---------- Helpers ----------
def apply_theme(theme_name):
    theme = THEMES.get(theme_name, THEMES["Light"])
    root.config(bg=theme["bg"])
    for widget in root.winfo_children():
        _apply_theme_recursive(widget, theme)

def _apply_theme_recursive(widget, theme):
    try:
        widget_type = widget.winfo_class()
        if widget_type in ("Frame", "LabelFrame"):
            widget.config(bg=theme["bg"])
        elif widget_type == "Label":
            widget.config(bg=theme["bg"], fg=theme["fg"])
        elif widget_type in ("Button", "TButton"):
            # ttk Button styling handled separately
            pass
        elif widget_type == "Entry":
            try:
                widget.config(bg=theme["entry_bg"], fg=theme["fg"])
            except:
                pass
    except:
        pass
    for child in widget.winfo_children():
        _apply_theme_recursive(child, theme)

def update_strength(password):
    length = len(password)
    categories = sum([
        any(c.islower() for c in password),
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(c in string.punctuation for c in password)
    ])
    if length >= 12 and categories >= 3:
        strength_label.config(text="Strength: Strong", foreground="green")
    elif length >= 8 and categories >= 2:
        strength_label.config(text="Strength: Medium", foreground="orange")
    else:
        strength_label.config(text="Strength: Weak", foreground="red")

def update_history_list():
    history_listbox.delete(0, tk.END)
    for pwd in password_history:
        history_listbox.insert(tk.END, pwd)

def save_password_to_file():
    if not password_var.get():
        messagebox.showwarning("No password", "Generate a password first.")
        return
    path = filedialog.asksaveasfilename(defaultextension=".txt",
                                        filetypes=[("Text Files", "*.txt")],
                                        title="Save passwords to...")
    if not path:
        return
    try:
        with open(path, "a", encoding="utf-8") as f:
            for p in password_history:
                f.write(p + "\n")
        messagebox.showinfo("Saved", f"Passwords saved to {os.path.basename(path)}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save file:\n{e}")

def copy_to_clipboard():
    pwd = password_var.get()
    if not pwd:
        messagebox.showwarning("No password", "Generate a password first.")
        return
    pyperclip.copy(pwd)
    messagebox.showinfo("Copied", "Password copied to clipboard.")

# ---------- Core Generation ----------
def generate_password():
    sel_strength = strength_level_var.get()

    # Adjust defaults for chosen strength
    if sel_strength == "Weak":
        length_var.set(6)
        upper_var.set(False)
        lower_var.set(True)
        digits_var.set(False)
        symbols_var.set(False)
    elif sel_strength == "Medium":
        length_var.set(10)
        upper_var.set(True)
        lower_var.set(True)
        digits_var.set(True)
        symbols_var.set(False)
    elif sel_strength == "Strong":
        length_var.set(14)
        upper_var.set(True)
        lower_var.set(True)
        digits_var.set(True)
        symbols_var.set(True)
    # Custom -> keep user selections

    length = length_var.get()
    use_upper = upper_var.get()
    use_lower = lower_var.get()
    use_digits = digits_var.get()
    use_symbols = symbols_var.get()
    avoid_similar = avoid_var.get()

    if not (use_upper or use_lower or use_digits or use_symbols):
        messagebox.showwarning("Selection Error", "Please select at least one character type.")
        return

    pool = ""
    if use_upper:
        pool += string.ascii_uppercase
    if use_lower:
        pool += string.ascii_lowercase
    if use_digits:
        pool += string.digits
    if use_symbols:
        pool += string.punctuation

    if avoid_similar:
        pool = "".join([c for c in pool if c not in SIMILAR_CHARS])

    # ensure at least one char from each selected category if possible
    password_chars = []
    categories = []
    if use_upper:
        categories.append(string.ascii_uppercase)
    if use_lower:
        categories.append(string.ascii_lowercase)
    if use_digits:
        categories.append(string.digits)
    if use_symbols:
        categories.append(string.punctuation)

    # Guarantee coverage if length >= number of categories
    if length >= len(categories):
        for cat in categories:
            filtered = cat
            if avoid_similar:
                filtered = "".join([c for c in cat if c not in SIMILAR_CHARS])
            if filtered:
                password_chars.append(random.choice(filtered))

    # fill remaining
    while len(password_chars) < length:
        password_chars.append(random.choice(pool))

    random.shuffle(password_chars)
    password = "".join(password_chars[:length])

    password_var.set(password)
    update_strength(password)

    if password not in password_history:
        password_history.insert(0, password)
        if len(password_history) > MAX_HISTORY:
            password_history.pop()
        update_history_list()

# ---------- UI Building ----------
root = tk.Tk()
root.title("Random Password Generator")
root.geometry("520x520")
root.resizable(False, False)
style = ttk.Style(root)

# Top frame: title + output
top_frame = tk.Frame(root)
top_frame.pack(fill="x", pady=(12, 6))

title = tk.Label(top_frame, text="Random Password Generator", font=("Segoe UI", 16, "bold"))
title.pack()

output_entry = tk.Entry(top_frame, textvariable=tk.StringVar(), font=("Consolas", 14), justify="center")
password_var = output_entry.cget("textvariable")
password_var = tk.StringVar()
output_entry.config(textvariable=password_var, width=38)
output_entry.pack(pady=(8, 2))

strength_label = ttk.Label(top_frame, text="Strength: ", font=("Segoe UI", 11))
strength_label.pack()

# Middle frame: controls grouped
controls_frame = tk.Frame(root)
controls_frame.pack(fill="x", padx=12, pady=8)

# Left subframe: strength + options
left_frame = tk.LabelFrame(controls_frame, text="Password Options", padx=10, pady=8)
left_frame.pack(side="left", fill="both", expand=True, padx=(0,8))

# Strength level
strength_level_var = tk.StringVar(value="Custom")
tk.Label(left_frame, text="Select Strength Level:").grid(row=0, column=0, sticky="w")
strength_combo = ttk.Combobox(left_frame, textvariable=strength_level_var,
                              values=["Weak", "Medium", "Strong", "Custom"], state="readonly", width=10)
strength_combo.grid(row=1, column=0, sticky="w", pady=(0,8))
strength_combo.set("Custom")

# Length spinner
length_var = tk.IntVar(value=12)
tk.Label(left_frame, text="Password Length:").grid(row=2, column=0, sticky="w")
length_spin = tk.Spinbox(left_frame, from_=4, to=64, textvariable=length_var, width=6)
length_spin.grid(row=3, column=0, sticky="w", pady=(0,8))

# Checkboxes (stacked)
upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=False)
avoid_var = tk.BooleanVar(value=False)

tk.Checkbutton(left_frame, text="Include Uppercase", variable=upper_var).grid(row=4, column=0, sticky="w")
tk.Checkbutton(left_frame, text="Include Lowercase", variable=lower_var).grid(row=5, column=0, sticky="w")
tk.Checkbutton(left_frame, text="Include Digits", variable=digits_var).grid(row=6, column=0, sticky="w")
tk.Checkbutton(left_frame, text="Include Symbols", variable=symbols_var).grid(row=7, column=0, sticky="w")
tk.Checkbutton(left_frame, text="Avoid Similar Characters (O/0 l/1)", variable=avoid_var).grid(row=8, column=0, sticky="w")

# Right subframe: theme + buttons
right_frame = tk.LabelFrame(controls_frame, text="Actions", padx=10, pady=8)
right_frame.pack(side="right", fill="y")

theme_var = tk.StringVar(value="Light")
tk.Label(right_frame, text="Select Theme:").pack(anchor="w")
theme_combo = ttk.Combobox(right_frame, textvariable=theme_var, values=list(THEMES.keys()), state="readonly", width=12)
theme_combo.pack(pady=(0,8))
theme_combo.set("Light")
apply_btn = ttk.Button(right_frame, text="Apply Theme", command=lambda: apply_theme(theme_var.get()))
apply_btn.pack(fill="x", pady=(0,8))

# Buttons row (Generate, Copy, Save)
btn_frame = tk.Frame(right_frame)
btn_frame.pack(fill="x", pady=(6,0))
gen_btn = ttk.Button(btn_frame, text="Generate", command=generate_password)
gen_btn.pack(side="left", expand=True, fill="x", padx=(0,4))
copy_btn = ttk.Button(btn_frame, text="Copy", command=copy_to_clipboard)
copy_btn.pack(side="left", expand=True, fill="x", padx=4)
save_btn = ttk.Button(btn_frame, text="Save", command=save_password_to_file)
save_btn.pack(side="left", expand=True, fill="x", padx=(4,0))

# History frame
history_frame = tk.LabelFrame(root, text="Password History (last 10)", padx=8, pady=8)
history_frame.pack(fill="both", expand=True, padx=12, pady=(8,12))

history_listbox = tk.Listbox(history_frame, height=8)
history_listbox.pack(side="left", fill="both", expand=True)
history_scroll = ttk.Scrollbar(history_frame, orient="vertical", command=history_listbox.yview)
history_scroll.pack(side="right", fill="y")
history_listbox.config(yscrollcommand=history_scroll.set)

# Apply initial theme and generate once
apply_theme("Light")
root.after(120, generate_password)

root.mainloop()
