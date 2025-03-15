import tkinter as tk
from tkinter import messagebox
from schedule_screen import open_schedule  # Import the open_schedule function
from mam import open_nutrition  # Import the open_nutrition function

class HomeScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("LockIN - Αρχική Οθόνη")
        self.root.state("zoomed")

        self.schedule_frame = tk.Frame(root, bg="#f2f2f2")
        self.nutrition_frame = tk.Frame(root, bg="#f2f2f2")

        self.create_menu()
        self.create_title()

    def create_menu(self):
        # Δημιουργία μενού στο πάνω μέρος
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # Προσθήκη επιλογών στο μενού
        menu_bar.add_command(label="Εισαγωγή Μαθημάτων", command=self.open_courses)
        menu_bar.add_command(label="Τι έχει το πρόγραμμα?", command=self.show_schedule)
        menu_bar.add_command(label="Τι θα φάμε σήμερα?", command=self.show_nutrition)
        menu_bar.add_command(label="Ειδοποιήσεις & Streaks", command=self.open_notifications)
        menu_bar.add_command(label="Ρυθμίσεις", command=self.open_settings)

    def create_title(self):
        # Προσθήκη τίτλου
        label = tk.Label(self.root, text="Καλώς ήρθατε στο LockIN", font=("Arial", 14))
        label.pack(pady=20)

    def open_courses(self):
        messagebox.showinfo("Εισαγωγή Μαθημάτων", "Μεταφορά στην οθόνη εισαγωγής μαθημάτων.")

    def open_notifications(self):
        messagebox.showinfo("Ειδοποιήσεις & Streaks", "Μεταφορά στην οθόνη ειδοποιήσεων.")

    def open_settings(self):
        messagebox.showinfo("Ρυθμίσεις", "Μεταφορά στις ρυθμίσεις εφαρμογής.")

    def hide_all_frames(self):
        self.schedule_frame.pack_forget()
        self.nutrition_frame.pack_forget()

    def show_nutrition(self):
        self.hide_all_frames()
        self.nutrition_frame.pack(fill=tk.BOTH, expand=True)
        open_nutrition(self.nutrition_frame)

    def show_schedule(self):
        self.hide_all_frames()
        self.schedule_frame.pack(fill=tk.BOTH, expand=True)
        open_schedule(self.schedule_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = HomeScreen(root)
    root.mainloop()