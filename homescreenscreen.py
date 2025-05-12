# filepath: c:\Users\30694\Desktop\ceid\ceid\8th_sem\tl\academic-weapon-app-tl\homescreenscreen.py
import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk
import random

funfacts = [
    "Some squirrels can fly",
    "If you study you will succeed",
    "There are no bad programming languages, only bad coders"
]

class HomeScreenScreen:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame

    def display(self):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        # Use CTkFrame and make it fill/expand
        container = ctk.CTkFrame(self.parent_frame, fg_color="#ffffff")
        container.pack(fill="both", expand=True, padx=0, pady=0)

        indiv_label = ctk.CTkLabel(
            container,
            text="Το Fun fact της ημέρας είναι:",
            text_color="#000000",
            font=('Arial', 30)
        )
        indiv_label.pack(anchor="n", pady=5)

        funfact_label = ctk.CTkLabel(
            container,
            text=random.choice(funfacts),
            text_color="#000000",
            font=('Arial', 20)
        )
        funfact_label.pack(anchor="n", pady=5)

        ctk.CTkLabel(
            container,
            text="\nΣήμερα η εστία έχει:",
            text_color="#000000",
            font=('Arial', 20),
            anchor="n",
            pady=5
        ).pack()