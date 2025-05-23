# filepath: c:\Users\30694\Desktop\ceid\ceid\8th_sem\tl\academic-weapon-app-tl\homescreenscreen.py
import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk
import random

# Εφαρμογή breeze theme σε όλα τα CTk widgets
# ctk.set_default_color_theme("themes/breeze.json")

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

        # CTkFrame με breeze theme (χωρίς fg_color για να πάρει το theme)
        container = ctk.CTkFrame(self.parent_frame)
        container.pack(fill="both", expand=True, padx=0, pady=0)

        indiv_label = ctk.CTkLabel(
            container,
            text="Το Fun fact της ημέρας είναι:",
            font=('Arial', 30)
        )
        indiv_label.pack(anchor="n", pady=5)

        funfact_label = ctk.CTkLabel(
            container,
            text=random.choice(funfacts),
            font=('Arial', 20)
        )
        funfact_label.pack(anchor="n", pady=5)

        ctk.CTkLabel(
            container,
            text="\nΣήμερα η εστία έχει:",
            font=('Arial', 20),
            anchor="n",
            pady=5
        ).pack()
