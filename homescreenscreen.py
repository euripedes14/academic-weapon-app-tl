import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk
import random

funfacts = [
            "Some squirels can fly",
            "If you study you will succeed",
            "There are no bad programming languages, only bad coders"
            ]

def open_homescreenscreen(parent_frame, home_screen):

    for widget in parent_frame.winfo_children():
        widget.destroy()

    container = tk.Frame(parent_frame, bg="#f2f2f2")
    container.pack(fill=tk.BOTH, expand=True)


    indiv_label = ctk.CTkLabel(container,
                               text = "Το Fun fact της ημέρας είναι:",
                               text_color = "#000000",
                               font=('Arial', 30))
    
    indiv_label.pack(anchor = "n", pady = 5)

    funfact_label = ctk.CTkLabel(container,
                                text = random.choice(funfacts),
                                text_color = "#000000",
                                font=('Arial', 20))

    funfact_label.pack(anchor = "n", pady = 5)

    ctk.CTkLabel(container,
                text = "\nΣήμερα η εστία έχει:",
                text_color = "#000000",
                font=('Arial', 20),
                anchor = "n",
                pady = 5).pack()
