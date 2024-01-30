import tkinter as tk
import time
import random
import threading

class TypeSpeed:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Typing Speed Tester")
        self.root.geometry("800x600")

        self.texts = open("texts.txt", "r").read().split("\n")

        self.frame = tk.Frame(self.root)

        self.sample_label = tk.Label(self.frame, text=random.choice(self.texts), font=("Helvetica", 18))
        self.sample_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(self.frame, width=40, font=("Helvetica", 24), textvariable=self.input_var)
        self.input_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=10)
        self.input_var.trace_add("write", self.check_input)
 
        self.speed_label = tk.Label(self.frame, text='Speed: \n0.00 CPS\n0.00 WPM', font=("Helvetica", 18))
        self.speed_label.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        self.reset_button = tk.Button(self.frame, text="Reset", command=self.reset)
        self.reset_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        self.frame.pack(expand=True)

        self.counter = 0
        self.running = False
        self.words_in_sample = len(self.sample_label.cget('text').split())

        self.root.mainloop()

    def check_input(self, *args):
        if not self.running:
            self.running = True
            t = threading.Thread(target=self.start_timer)
            t.start()

        input_text = self.input_var.get()
        sample_text = self.sample_label.cget('text')

        for i, char in enumerate(input_text):
            if i >= len(sample_text) or char != sample_text[i]:
                self.input_entry.config(fg="red")
                return
        self.input_entry.config(fg="black")

        if input_text == sample_text:
            self.running = False
            self.input_entry.config(fg="green")

    def start_timer(self):
        while self.running:
            time.sleep(0.1)
            self.counter += 0.1
            input_text = self.input_var.get()
            sample_text = self.sample_label.cget('text')

            for i, char in enumerate(input_text):
                if i >= len(sample_text) or char != sample_text[i]:
                    break

            cps = len(input_text) / self.counter
            wpm = cps * 60 / self.words_in_sample
            self.speed_label.config(text=f"Speed: \n{cps:.2f} CPS\n{wpm:.2f} WPM")

    def reset(self):
        self.running = False
        self.counter = 0
        self.speed_label.config(text="Speed: \n0.00 CPS\n0.00 WPM")
        self.sample_label.config(text=random.choice(self.texts))
        self.words_in_sample = len(self.sample_label.cget('text').split())
        self.input_var.set('')
        self.input_entry.config(fg="black")

TypeSpeed()