import tkinter as tk
from tkinter import messagebox
import time, random

# Sentences for different levels
LEVELS = {
    1: ["The quick brown fox jumps over the lazy dog.",
        "Coding is fun and powerful.",
        "Python makes life easier."],
    2: ["Artificial intelligence is transforming the world of technology.",
        "Practice and consistency are the keys to becoming a great coder.",
        "Typing fast and accurately can save a lot of time in daily work."],
    3: ["Success in programming comes from curiosity, patience, and constant practice.",
        "Building projects is the best way to master Python and improve problem-solving skills.",
        "Technology evolves rapidly, so developers must keep learning and adapting."]
}

class TypingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Game 🎮")
        self.root.geometry("900x500")
        self.root.configure(bg="#0f1724")

        self.level = 1
        self.time_left = 60
        self.start_time = None
        self.sentence = ""
        self.ended = False

        # UI Layout
        tk.Label(root, text="Typing Speed Game 🎮", font=("Helvetica", 22, "bold"), bg="#0f1724", fg="#38bdf8").pack(pady=10)

        # Level & Timer
        self.level_var = tk.StringVar(value="Level: 1")
        self.timer_var = tk.StringVar(value="Time: 60s")
        tk.Label(root, textvariable=self.level_var, font=("Helvetica", 14), bg="#0f1724", fg="#facc15").pack()
        tk.Label(root, textvariable=self.timer_var, font=("Helvetica", 14), bg="#0f1724", fg="#f87171").pack()

        # Target text
        self.target = tk.Label(root, text="", font=("Consolas", 14), wraplength=850, bg="#0f1724", fg="white", justify="center")
        self.target.pack(pady=20)

        # Typing box
        self.entry = tk.Text(root, height=6, font=("Consolas", 14), wrap="word")
        self.entry.pack(padx=20, pady=10, fill="both", expand=True)
        self.entry.bind("<KeyRelease>", self.check_input)

        # Score label
        self.score_var = tk.StringVar(value="Score: 0")
        tk.Label(root, textvariable=self.score_var, font=("Helvetica", 14), bg="#0f1724", fg="#4ade80").pack(pady=10)

        # Buttons
        tk.Button(root, text="Start Game", font=("Helvetica", 12), bg="#38bdf8", fg="black", command=self.start_game).pack(pady=5)
        tk.Button(root, text="Restart", font=("Helvetica", 12), bg="#facc15", fg="black", command=self.restart).pack(pady=5)

    def start_game(self):
        self.level = 1
        self.score = 0
        self.time_left = 60
        self.level_var.set(f"Level: {self.level}")
        self.score_var.set("Score: 0")
        self.next_sentence()
        self.update_timer()

    def restart(self):
        self.entry.delete("1.0", "end")
        self.start_game()

    def next_sentence(self):
        self.sentence = random.choice(LEVELS[self.level])
        self.target.config(text=self.sentence)
        self.entry.delete("1.0", "end")

    def update_timer(self):
        if self.time_left > 0 and not self.ended:
            self.timer_var.set(f"Time: {self.time_left}s")
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        elif not self.ended:
            self.game_over()

    def check_input(self, event=None):
        typed = self.entry.get("1.0", "end-1c")
        if typed.strip() == self.sentence.strip():
            self.calculate_score()
            if self.level < 3:
                self.level += 1
                self.level_var.set(f"Level: {self.level}")
                self.next_sentence()
            else:
                self.win_game()

    def calculate_score(self):
        typed = self.entry.get("1.0", "end-1c")
        elapsed = 60 - self.time_left
        minutes = elapsed / 60 if elapsed > 0 else 1
        wpm = (len(typed) / 5) / minutes
        accuracy = (sum(1 for i in range(len(self.sentence)) if i < len(typed) and typed[i] == self.sentence[i]) / len(self.sentence)) * 100
        points = int(wpm + accuracy)
        self.score += points
        self.score_var.set(f"Score: {self.score}")

    def game_over(self):
        self.ended = True
        messagebox.showinfo("Game Over", f"⏳ Time's up!\nFinal Score: {self.score}")

    def win_game(self):
        self.ended = True
        messagebox.showinfo("Congratulations 🎉", f"You completed all levels!\nFinal Score: {self.score}")

if __name__ == "__main__":
    root = tk.Tk()
    game = TypingGame(root)
    root.mainloop()
