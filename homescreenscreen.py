import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk
import random
from datetime import datetime
from menu import Menu
import json

funfacts = [
       "Some squirrels can fly.",
    "If you study you will succeed.",
    "There are no bad programming languages, only bad coders.",
    "Success is the sum of small efforts, repeated day in and day out.",
    "The best way to get started is to quit talking and begin doing.",
    "Every great developer you know got there by solving problems they were unqualified to solve until they actually did it.",
    "The only way to do great work is to love what you do. – Steve Jobs",
    "Programming isn't about what you know; it's about what you can figure out.",
    "Did you know? The first computer bug was an actual moth found in a computer in 1947.",
    "Python is named after Monty Python, not the snake.",
    "The first website is still online: http://info.cern.ch/",
    "Motivation gets you started. Habit keeps you going.",
    "Debugging is like being the detective in a crime movie where you are also the murderer.",
    "Dream big, work hard, stay focused, and surround yourself with good people.",
    "The only limit to our realization of tomorrow will be our doubts of today. – F.D. Roosevelt",
    "Java was originally called Oak.",
    "The original name for Windows was Interface Manager.",
    "Learning never exhausts the mind. – Leonardo da Vinci",
    "You don’t have to be great to start, but you have to start to be great.",
    "The best error message is the one that never shows up."
]

class HomeScreenScreen:
    def __init__(self, parent_frame, username=None):
        self.parent_frame = parent_frame
        self.username = username

    def get_username(self):
        if self.username:
            return self.username
        try:
            with open("settings.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                user = next(iter(data.values()))
                return user.get("profile", {}).get("username", "AlienUser123")
        except Exception:
            return "AlienUser123"

    def display(self):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        # --- Main Container ---
        container = ctk.CTkFrame(self.parent_frame)
        container.pack(fill="both", expand=True, padx=30, pady=30)

        # --- Greeting Section ---
        greeting_card = ctk.CTkFrame(container, corner_radius=15)
        greeting_card.pack(pady=10, fill="x", expand=False)

        username = self.get_username()
        hour = datetime.now().hour
        if hour < 12:
            greeting = f"☀️ Καλημέρα, {username}!"
        elif hour < 18:
            greeting = f"🌤️ Καλό απόγευμα, {username}!"
        else:
            greeting = f"🌙 Καλό βράδυ, {username}!"

        ctk.CTkLabel(
            greeting_card,
            text=greeting,
            font=('Arial', 24, "bold"),
            text_color="#1a1a1a",
            fg_color="transparent"
        ).pack(pady=10, padx=10)

        funfact_card = ctk.CTkFrame(container, corner_radius=15)
        funfact_card.pack(pady=10, fill="x", expand=False)

        ctk.CTkLabel(
            funfact_card,
            text="📌 Fun Fact",
            font=('Arial', 20, "bold"),
            text_color="#444"
        ).pack(pady=(10, 5))

        funfact_label = ctk.CTkLabel(
            funfact_card,
            text=random.choice(funfacts),
            font=('Arial', 16),
            wraplength=600,
            justify="center"
        )
        funfact_label.pack(pady=(0, 10), padx=10)

        # --- Estia / Menu Section ---
        menu_card = ctk.CTkFrame(container, corner_radius=15)
        menu_card.pack(pady=10, fill="x", expand=False)

        ctk.CTkLabel(
            menu_card,
            text="🍽️ Σήμερα η εστία έχει:",
            font=('Arial', 20, "bold"),
            text_color="#444"
        ).pack(pady=(10, 5))

        # Estia status
        menu_obj = Menu()
        today, meal, meal_menu = menu_obj.get_current_or_next_meal()
        estia_status = menu_obj.get_estia_status()

        ctk.CTkLabel(
            menu_card,
            text=estia_status,
            font=('Arial', 16, 'bold'),
            text_color="#2e7d32" if "ανοιχτή" in estia_status else "#d84315"
        ).pack(pady=5)

        # Format menu info
        if isinstance(meal_menu, dict):
            menu_text = f"{meal.capitalize()}:\n"
            menu_text += f"• Πρώτο πιάτο: {meal_menu.get('first_course', '')}\n"
            menu_text += f"• Κυρίως: {', '.join(meal_menu.get('main_courses', []))}\n"
            menu_text += f"• Σαλάτα: {meal_menu.get('salad', '')}\n"
            menu_text += f"• Επιδόρπιο: {meal_menu.get('dessert', '')}"
        else:
            menu_text = f"{meal.capitalize()}:\n{meal_menu}"

        ctk.CTkLabel(
            menu_card,
            text=menu_text,
            font=('Arial', 16),
            wraplength=600,
            justify="left"
        ).pack(pady=(0, 10), padx=10)
