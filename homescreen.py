import customtkinter as ctk
from tkinter import messagebox
from schedule_screen import open_schedule
from mam import open_nutrition
from settings import SettingsMenuApp
from courses import open_courses_screen
from homescreenscreen import HomeScreenScreen
from task import open_task_screen
from statistics_screen import StatisticsClass
from spendings import ExpenseTrackerApp

# Εφαρμογή breeze theme σε όλα τα CTk widgets
ctk.set_default_color_theme("themes/breeze.json")

def open_settings(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()
    settings_app = SettingsMenuApp(parent_frame)
    settings_app.main_frame.pack(fill="both", expand=True)

def open_statistics(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()
    statistics_app = StatisticsClass(parent_frame)
    statistics_app.main_frame.pack(fill="both", expand=True)

class HomeScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("LockIN - Αρχική Οθόνη")
        self.root.state("zoomed")

        # Main frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Top navigation bar
        self.nav_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.nav_frame.pack(side="top", fill="x", padx=0, pady=0)

        # Content frame (make it fill all available space)
        self.content_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.content_frame.pack(side="top", fill="both", expand=True, padx=0, pady=0)

        # Navigation buttons (all on top)
        self.add_nav_button("Αρχική Οθόνη", self.open_homescreen)
        self.add_nav_button("Εισαγωγή Μαθημάτων", self.open_courses)
        self.add_nav_button("Τι έχει το πρόγραμμα;", self.show_schedule)
        self.add_nav_button("Τι θα φάμε σήμερα;", self.show_nutrition)
        self.add_nav_button("Μελέτη", self.open_tasks)
        self.add_nav_button("Στατιστικά", self.show_statistics)
        self.add_nav_button("Διαχείριση Εξόδων", self.open_spendings)
        self.add_nav_button("Ρυθμίσεις", self.show_settings)
        self.add_nav_button("Αποσύνδεση", self.logout, fg_color="#faa2a2", hover_color="#f88379")

        self.open_homescreen()

    def add_nav_button(self, text, command, fg_color=None, hover_color=None):
        # Εφαρμογή breeze theme: αφήνουμε τα default αν δεν δοθούν τιμές
        btn = ctk.CTkButton(
            self.nav_frame,
            text=text,
            command=command,
            width=150,
            fg_color=fg_color if fg_color else None,
            hover_color=hover_color if hover_color else None,
            corner_radius=5,
            text_color="#000000"
        )
        btn.pack(side="left", padx=8, pady=5)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def open_homescreen(self):
        self.clear_content()
        homescreen_screen = HomeScreenScreen(self.content_frame)
        homescreen_screen.display()

    def open_courses(self):
        self.clear_content()
        open_courses_screen(self.content_frame)

    def show_nutrition(self):
        self.clear_content()
        open_nutrition(self.content_frame)

    def show_schedule(self):
        self.clear_content()
        open_schedule(self.content_frame)

    def show_settings(self):
        self.clear_content()
        open_settings(self.content_frame)

    def show_statistics(self):
        self.clear_content()
        open_statistics(self.content_frame)

    def open_tasks(self):
        self.clear_content()
        open_task_screen(self.content_frame)

    def open_spendings(self):
        self.clear_content()
        ExpenseTrackerApp(self.content_frame)

    def logout(self):
        self.root.destroy()
        from login import login_app
        login_app()

if __name__ == "__main__":
    root = ctk.CTk()
    # Εφαρμογή breeze theme και εμφάνιση light mode για συνέπεια
    ctk.set_default_color_theme("themes/breeze.json")
    ctk.set_appearance_mode("light")
    app = HomeScreen(root)
    root.mainloop()
    
# We made a Tkinter application that serves as a home screen for a student management system. It includes various functionalities such as course management, scheduling, nutrition tracking, task management, statistics, and settings. Each functionality is encapsulated in its own frame, and the main application allows users to navigate between these frames using a menu bar.
# The application is designed to be user-friendly and visually appealing, with a consistent color scheme and layout. It also includes features for managing expenses and notifications, making it a comprehensive tool for students.    
# The code is modular, allowing for easy updates and additions of new features in the future. Overall, it provides a solid foundation for a student management system with a focus on usability and functionality.
# The application is built using the Tkinter library, which is a standard GUI toolkit for Python. It also utilizes customtkinter for enhanced UI components and aesthetics. The code is structured to allow for easy navigation and interaction, making it suitable for both novice and experienced users.
# The use of classes and functions helps to keep the code organized and maintainable, allowing for future enhancements and modifications without significant restructuring. The application is designed to be responsive and adaptable to different screen sizes, ensuring a smooth user experience across various devices.
# Overall our code serves as a solid foundation for a student management system, providing essential features and a user-friendly interface. It can be further expanded with additional functionalities and improvements based on user feedback and requirements.