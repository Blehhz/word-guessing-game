import tkinter as tk
import random
import os

# ---------------- SCORE HANDLING ----------------
def get_data(user_name):
    file_path = f"user_data/{user_name.lower()}_word_score.txt"
    if os.path.isfile(file_path):
        with open(file_path, "r") as f:
            return int(f.read().strip() or 0)
    return 0

def update_score(high_score, user_name):
    if not os.path.exists("user_data"):
        os.makedirs("user_data")
    file_path = f"user_data/{user_name.lower()}_word_score.txt"
    with open(file_path, "w") as f:
        f.write(str(high_score))

# ---------------- WORDS ----------------
def load_words(filename="words.txt"):
    categories = {}
    with open(filename, "r") as f:
        for line in f:
            if ":" in line:
                cat, words = line.strip().split(":")
                categories[cat.strip()] = [w.strip().lower() for w in words.split(",")]
    return categories

# ---------------- CUSTOM ROUNDED BUTTON ----------------
class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, bg="#88C0D0", fg="#2E3440", command=None, radius=20, width=120, height=40, **kwargs):
        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0, **kwargs)
        self.command = command
        self.radius = radius
        self.bg_color = bg
        self.fg_color = fg
        self.text = text
        self.draw_button()
        self.bind("<Button-1>", lambda e: self.on_click())
        self.bind("<Enter>", lambda e: self.itemconfig("bg_rect", fill="#81A1C1"))
        self.bind("<Leave>", lambda e: self.itemconfig("bg_rect", fill=self.bg_color))

    def draw_button(self):
        x0, y0, x1, y1 = 2, 2, self.winfo_reqwidth()-2, self.winfo_reqheight()-2
        self.create_round_rect(x0, y0, x1, y1, r=self.radius, fill=self.bg_color, outline="", tags="bg_rect")
        self.create_text(x1//2, y1//2, text=self.text, fill=self.fg_color, font=("Helvetica", 12, "bold"))

    def create_round_rect(self, x1, y1, x2, y2, r=25, **kwargs):
        self.create_arc(x1, y1, x1+r*2, y1+r*2, start=90, extent=90, style="pieslice", **kwargs)
        self.create_arc(x2-2*r, y1, x2, y1+2*r, start=0, extent=90, style="pieslice", **kwargs)
        self.create_arc(x1, y2-2*r, x1+2*r, y2, start=180, extent=90, style="pieslice", **kwargs)
        self.create_arc(x2-2*r, y2-2*r, x2, y2, start=270, extent=90, style="pieslice", **kwargs)
        self.create_rectangle(x1+r, y1, x2-r, y2, **kwargs)
        self.create_rectangle(x1, y1+r, x2, y2-r, **kwargs)

    def on_click(self):
        if self.command:
            self.command()

# ---------------- GUI GAME ----------------
class WordGuessGame:
    DARK_BG = "#2E3440"
    LIGHT_TEXT = "#ECEFF4"
    ACCENT1 = "#88C0D0"
    ACCENT2 = "#81A1C1"
    ACCENT3 = "#A3BE8C"
    ACCENT4 = "#B48EAD"
    WARN = "#D08770"
    SCORE = "#EBCB8B"
    ENTRY_BG = "#3B4252"

    def __init__(self, master):
        self.master = master
        self.master.title("Word Guessing Game")
        self.master.geometry("650x500")
        self.master.configure(bg=self.DARK_BG)
        self.master.resizable(False, False)
        self.categories = load_words()
        
        self.username = ""
        self.high_score = 0
        self.score = 0

        self.setup_name_screen()

    # ---------------- NAME SCREEN ----------------
    def setup_name_screen(self):
        self.clear_screen()
        tk.Label(self.master, text="🎮 Word Guessing Game", font=("Helvetica", 24, "bold"),
                 fg=self.LIGHT_TEXT, bg=self.DARK_BG).pack(pady=20)
        tk.Label(self.master, text="Enter your name:", font=("Helvetica", 14),
                 fg=self.LIGHT_TEXT, bg=self.DARK_BG).pack(pady=10)

        self.name_entry = tk.Entry(self.master, font=("Helvetica", 14), width=25,
                                   bg=self.ENTRY_BG, fg=self.LIGHT_TEXT, insertbackground=self.LIGHT_TEXT)
        self.name_entry.pack(pady=5)
        self.name_entry.focus()
        self.name_entry.bind("<Return>", lambda e: self.submit_name())

        RoundedButton(self.master, "Next", bg=self.ACCENT1, fg=self.DARK_BG, command=self.submit_name).pack(pady=15)

        self.info_label = tk.Label(self.master, text="", font=("Helvetica", 12, "bold"),
                                   fg=self.WARN, bg=self.DARK_BG)
        self.info_label.pack(pady=10)

    def submit_name(self):
        name = self.name_entry.get().strip()
        if not name:
            self.info_label.config(text="⚠️ Please enter your name!")
            return
        self.username = name
        self.high_score = get_data(self.username)
        self.setup_difficulty_screen()

    # ---------------- DIFFICULTY SCREEN ----------------
    def setup_difficulty_screen(self):
        self.clear_screen()
        tk.Label(self.master, text=f"Hello {self.username}!", font=("Helvetica", 20, "bold"),
                 fg=self.LIGHT_TEXT, bg=self.DARK_BG).pack(pady=20)
        tk.Label(self.master, text="Choose difficulty:", font=("Helvetica", 16),
                 fg=self.LIGHT_TEXT, bg=self.DARK_BG).pack(pady=15)
        
        diff_frame = tk.Frame(self.master, bg=self.DARK_BG)
        diff_frame.pack(pady=10)

        RoundedButton(diff_frame, "Easy", bg=self.ACCENT1, fg=self.DARK_BG, command=lambda: self.start_game("easy")).pack(side="left", padx=8)
        RoundedButton(diff_frame, "Medium", bg=self.ACCENT2, fg=self.DARK_BG, command=lambda: self.start_game("medium")).pack(side="left", padx=8)
        RoundedButton(diff_frame, "Hard", bg=self.ACCENT3, fg=self.DARK_BG, command=lambda: self.start_game("hard")).pack(side="left", padx=8)

        self.info_label = tk.Label(self.master, text="", font=("Helvetica", 12, "bold"),
                                   fg=self.WARN, bg=self.DARK_BG)
        self.info_label.pack(pady=10)

    # ---------------- START GAME ----------------
    def start_game(self, difficulty):
        levels = {"easy": 10, "medium": 7, "hard": 5}
        self.attempts = levels[difficulty]
        self.score = 0
        self.start_round()

    # ---------------- START ROUND ----------------
    def start_round(self):
        self.clear_screen()
        self.category = random.choice(list(self.categories.keys()))
        self.word = random.choice(self.categories[self.category])
        self.guessed = ["_"] * len(self.word)
        self.used_letters = set()
        self.hint_used = False
        self.setup_game_screen()

    # ---------------- GAME SCREEN ----------------
    def setup_game_screen(self):
        self.clear_screen()
        tk.Label(self.master, text=f"Category: {self.category}", font=("Helvetica", 16, "bold"),
                 fg=self.LIGHT_TEXT, bg=self.DARK_BG).pack(pady=5)
        
        self.word_var = tk.StringVar(value=" ".join(self.guessed))
        tk.Label(self.master, textvariable=self.word_var, font=("Helvetica", 28, "bold"),
                 fg=self.LIGHT_TEXT, bg=self.DARK_BG).pack(pady=10)

        self.attempts_var = tk.StringVar(value=f"Attempts left: {self.attempts}")
        tk.Label(self.master, textvariable=self.attempts_var, font=("Helvetica", 14),
                 fg=self.ACCENT1, bg=self.DARK_BG).pack()
        
        self.used_var = tk.StringVar(value="Used letters: None")
        tk.Label(self.master, textvariable=self.used_var, font=("Helvetica", 14),
                 fg=self.ACCENT2, bg=self.DARK_BG).pack(pady=5)

        self.input_frame = tk.Frame(self.master, bg=self.DARK_BG)
        self.input_frame.pack(pady=10)

        self.guess_entry = tk.Entry(self.input_frame, font=("Helvetica", 14), width=20,
                                    bg=self.ENTRY_BG, fg=self.LIGHT_TEXT, insertbackground=self.LIGHT_TEXT)
        self.guess_entry.pack(side="left", padx=5)
        self.guess_entry.focus()
        self.guess_entry.bind("<Return>", lambda e: self.make_guess())

        self.guess_btn = RoundedButton(self.input_frame, "Guess", bg=self.ACCENT3, fg=self.DARK_BG, command=self.make_guess)
        self.guess_btn.pack(side="left", padx=5)
        self.hint_btn = RoundedButton(self.input_frame, "Hint", bg=self.ACCENT4, fg=self.DARK_BG, command=self.use_hint)
        self.hint_btn.pack(side="left", padx=5)

        self.score_label = tk.Label(self.master, text=f"Score: {self.score}    High Score: {self.high_score}",
                                    font=("Helvetica", 14, "bold"), fg=self.SCORE, bg=self.DARK_BG)
        self.score_label.pack(pady=15)

        self.info_label = tk.Label(self.master, text="", font=("Helvetica", 14, "bold"),
                                   fg=self.WARN, bg=self.DARK_BG)
        self.info_label.pack(pady=5)

    # ---------------- GAME LOGIC ----------------
    def make_guess(self, _=None):
        guess = self.guess_entry.get().strip().lower()
        self.guess_entry.delete(0, "end")
        self.info_label.config(text="")
        if not guess:
            return

        if guess == self.word:
            self.score += 1
            self.check_high_score()
            self.end_round(win=True)
            return

        if guess == "hint":
            self.use_hint()
            return

        if len(guess) != 1 or not guess.isalpha():
            self.info_label.config(text="⚠️ Enter a single letter or the full word")
            return

        if guess in self.used_letters:
            self.info_label.config(text="⚠️ You already guessed that letter!")
            return

        self.used_letters.add(guess)
        if guess in self.word:
            for i, c in enumerate(self.word):
                if c == guess:
                    self.guessed[i] = c
        else:
            self.attempts -= 1

        self.update_game_screen()

        if "_" not in self.guessed:
            self.score += 1
            self.check_high_score()
            self.end_round(win=True)
        elif self.attempts <= 0:
            self.end_round(win=False)

    def use_hint(self, _=None):
        if self.hint_used:
            self.info_label.config(text="⚠️ You already used your hint!")
            return
        hidden_indices = [i for i, l in enumerate(self.guessed) if l == "_"]
        if hidden_indices:
            idx = random.choice(hidden_indices)
            self.guessed[idx] = self.word[idx]
            self.hint_used = True
            self.info_label.config(text=f"🔎 Hint used! Letter '{self.word[idx]}' revealed")
            self.update_game_screen()

    def update_game_screen(self):
        self.word_var.set(" ".join(self.guessed))
        self.attempts_var.set(f"Attempts left: {self.attempts}")
        self.used_var.set("Used letters: " + ", ".join(sorted(self.used_letters)) if self.used_letters else "Used letters: None")
        self.score_label.config(text=f"Score: {self.score}    High Score: {self.high_score}")

    def check_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            update_score(self.high_score, self.username)

    # ---------------- END ROUND WITHOUT POPUPS ----------------
    def end_round(self, win):
        # Hide input
        self.guess_entry.pack_forget()
        self.guess_btn.pack_forget()
        self.hint_btn.pack_forget()

        if win:
            self.info_label.config(text=f"🎉 You guessed it! Word: '{self.word}'")
        else:
            self.info_label.config(text=f"💀 Out of attempts! Word was '{self.word}'")

        # Show Play Again / Quit buttons
        self.end_frame = tk.Frame(self.master, bg=self.DARK_BG)
        self.end_frame.pack(pady=10)
        RoundedButton(self.end_frame, "Play Again", bg=self.ACCENT3, fg=self.DARK_BG, command=self.start_round).pack(side="left", padx=5)
        RoundedButton(self.end_frame, "Quit", bg=self.ACCENT4, fg=self.DARK_BG, command=self.master.destroy).pack(side="left", padx=5)

    # ---------------- UTIL ----------------
    def clear_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

# ------------------- RUN GAME -------------------
if __name__ == "__main__":
    root = tk.Tk()
    game = WordGuessGame(root)
    root.mainloop()
