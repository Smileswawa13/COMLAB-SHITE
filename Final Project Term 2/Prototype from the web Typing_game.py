# Developer: Jimmy Carter
# Contact: jimmy4carter@gmail.com
# Phone: +2348038660259
# GitHub: https://github.com/Jimmy4carter

import tkinter as tk
import time
import random

class TypingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test Game")
        self.root.geometry("400x300")
        self.root.configure(bg="#FDF6E3")  # Set background color
        
        self.texts = [
            "The quick brown fox jumps over the lazy dog.",
            "Python is a powerful programming language.",
            "Coding is fun and rewarding.",
            "Keep calm and code on.",
            "Practice makes perfect.",
            "Type your way to success."
        ]

        self.typing_speed = 0
        self.time_start = 0
        self.typing_started = False
        self.time_remaining = 0
        self.timer_running = False
        self.text_to_type = ""

        self.label_instruction = tk.Label(self.root, text="Type the text below:", bg="#FDF6E3", fg="#586E75", font=("Arial", 12))
        self.label_instruction.pack()

        self.label_text = tk.Label(self.root, text="", bg="#FDF6E3", fg="#073642", font=("Arial", 14, "italic"))
        self.label_text.pack()

        self.user_text = tk.Text(self.root, height=3, width=50, bg="#EEE8D5", fg="#002B36", font=("Arial", 12))
        self.user_text.pack()

        self.btn_start = tk.Button(self.root, text="Start Typing", command=self.start_typing, bg="#268BD2", fg="white", font=("Arial", 12))
        self.btn_start.pack()

        self.btn_stop = tk.Button(self.root, text="Stop", command=self.stop_typing, bg="#DC322F", fg="white", font=("Arial", 12))
        self.btn_stop.pack()

        self.label_timer = tk.Label(self.root, text="", bg="#FDF6E3", fg="#268BD2", font=("Arial", 16))
        self.label_timer.pack()

        self.label_result = tk.Label(self.root, text="", bg="#FDF6E3", fg="#073642", font=("Arial", 14))
        self.label_result.pack()

    def start_typing(self):
        self.typing_started = False
        self.time_remaining = 0
        self.set_text_to_type()
        self.time_start = time.time()
        self.start_timer()

    def set_text_to_type(self):
        self.text_to_type = random.choice(self.texts)
        self.label_text.config(text=self.text_to_type)
        self.time_remaining = len(self.text_to_type.split()) * 3  # Allocate 3 seconds for each word

    def start_timer(self):
        if not self.timer_running:
            self.update_timer()

    def update_timer(self):
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        time_format = f"{minutes:02d}:{seconds:02d}"
        self.label_timer.config(text=time_format)

        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.timer_running = True
            self.root.after(1000, self.update_timer)
        else:
            self.stop_typing()

    def stop_typing(self):
        self.timer_running = False
        self.calculate_speed()

    def calculate_speed(self):
        typed_text = self.user_text.get("1.0", "end-1c")
        correct_characters = sum(1 for a, b in zip(typed_text, self.text_to_type) if a == b)
        accuracy = (correct_characters / len(self.text_to_type)) * 100 if self.text_to_type else 0
        
        self.typing_speed = len(typed_text.split()) / ((time.time() - self.time_start) / 60)
        self.label_result.config(text=f"Your typing speed: {self.typing_speed:.2f} WPM\nAccuracy: {accuracy:.2f}%")

def main():
    root = tk.Tk()
    root.configure(bg="#FDF6E3")  # Set background color for the window
    game = TypingGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
