import tkinter as tk
from tkinter import messagebox
from schedule_screen import open_schedule     # Import the open_schedule function
from mam import open_nutrition                # Import the open_nutrition function
from settings import SettingsMenuApp
from courses import open_courses_screen
from task import open_task_screen  # Import the new task screen function

def open_settings(parent_frame):
    """Display the settings screen in the given parent frame."""
    for widget in parent_frame.winfo_children():  # Clear previous contents of the frame
        widget.destroy()

    # Create and display the SettingsMenuApp in the parent frame
    settings_app = SettingsMenuApp(parent_frame)  # Pass the parent frame as the root
    settings_app.main_frame.pack(fill="both", expand=True)

    

class HomeScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("LockIN - Αρχική Οθόνη")
        self.root.state("zoomed")

        # Frames για διαφορετικές λειτουργίες
        self.schedule_frame = tk.Frame(root, bg="#f2f2f2")
        self.nutrition_frame = tk.Frame(root, bg="#f2f2f2")
        self.settings_frame = None

        self.create_menu()
        self.create_title()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        menu_bar.add_command(label="Εισαγωγή Μαθημάτων", command=self.open_courses)
        menu_bar.add_command(label="Τι έχει το πρόγραμμα?", command=self.show_schedule)
        menu_bar.add_command(label="Τι θα φάμε σήμερα?", command=self.show_nutrition)
        menu_bar.add_command(label="Εργασίες", command=self.open_tasks)  # Use Greek for consistency
        menu_bar.add_command(label="Ειδοποιήσεις & Streaks", command=self.open_notifications)
        menu_bar.add_command(label="Ρυθμίσεις", command=self.show_settings)  # Σύνδεση με τη ρύθμιση

    def create_title(self):
        label = tk.Label(self.root, text="Καλώς ήρθατε στο LockIN", font=("Arial", 14))
        label.pack(pady=20)

    def open_courses(self):
        """Open the courses screen."""
        self.hide_all_frames()
        if not hasattr(self, "courses_frame"):
            self.courses_frame = tk.Frame(self.root, bg="#f2f2f2")
        self.courses_frame.pack(fill=tk.BOTH, expand=True)
        # Remove the local import that's causing issues
        open_courses_screen(self.courses_frame, self)

    def open_notifications(self):
        messagebox.showinfo("Ειδοποιήσεις & Streaks", "Μεταφορά στην οθόνη ειδοποιήσεων.")

    def hide_all_frames(self):
        """Απόκρυψη όλων των άλλων frames όταν επιλέγεται μία λειτουργία."""
        self.schedule_frame.pack_forget()
        self.nutrition_frame.pack_forget()
        if self.settings_frame:
            self.settings_frame.pack_forget()
        if hasattr(self, "courses_frame"):
            self.courses_frame.pack_forget()
        if hasattr(self, "tasks_frame"):
            self.tasks_frame.pack_forget()

    def show_nutrition(self):
        """Δείξε το παράθυρο διατροφής."""
        self.hide_all_frames()
        self.nutrition_frame.pack(fill=tk.BOTH, expand=True)
        open_nutrition(self.nutrition_frame)

    def show_schedule(self):
        """Δείξε το παράθυρο προγράμματος."""
        self.hide_all_frames()
        self.schedule_frame.pack(fill=tk.BOTH, expand=True)
        open_schedule(self.schedule_frame)

    def show_settings(self):
        """Display the settings screen using the open_settings function."""
        self.hide_all_frames()

        # Create the settings frame if it doesn't exist
        if not self.settings_frame:
            self.settings_frame = tk.Frame(self.root, bg='#ffffff')
            self.settings_frame.pack(fill=tk.BOTH, expand=True)

        # Use the new function to display settings
        open_settings(self.settings_frame)
        self.settings_frame.pack(fill=tk.BOTH, expand=True)

    def open_tasks(self):
        """Open the tasks screen with Pomodoro timer."""
        self.hide_all_frames()
        if not hasattr(self, "tasks_frame"):
            self.tasks_frame = tk.Frame(self.root, bg="#f2f2f2")
        self.tasks_frame.pack(fill=tk.BOTH, expand=True)
        open_task_screen(self.tasks_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = HomeScreen(root)
    root.mainloop()