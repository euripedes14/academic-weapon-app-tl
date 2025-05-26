# Application Architecture & Class Communication

## Overview

#This application is structured using the Model-View-Controller (MVC) pattern, where:
#- **Model** classes (like `Menu`) provide data and business logic.
#- **View/Controller** classes (like `HomeScreenScreen`, `HomeScreen`) handle the user interface and user interactions.

## Main Classes and Their Roles

### 1. Menu (menu.py)
#- **Role:** Acts as the data provider for the weekly restaurant (εστία) menu and related logic.
#- **Responsibilities:**
#  - Stores the current week's menu in a structured format.
#  - Provides methods to get the current or next meal based on the time.
#  - Provides the status of the restaurant (open/closed and when it opens next).

### 2. HomeScreenScreen (homescreenscreen.py)
#- **Role:** Handles the content and layout of the main home screen (the first screen the user sees).
#- **Responsibilities:**
#  - Displays a personalized greeting using the username from settings.
#  - Shows a random fun fact.
#  - Displays the current or next meal from the Menu class.
#  - Shows the status of the restaurant using Menu's logic.

### 3. HomeScreen (homescreen.py)
#- **Role:** Manages the main application window, navigation bar, and switching between different screens.
#- **Responsibilities:**
#  - Creates and manages the main frame and navigation bar.
#  - Handles navigation between different app sections (home, courses, nutrition, spendings, etc.).
#  - Instantiates and displays the HomeScreenScreen in the content area.

## How Classes Communicate

#- **HomeScreen** creates an instance of **HomeScreenScreen** and calls its `display()` method to render the home page.
#- **HomeScreenScreen** creates an instance of **Menu** to:
#  - Retrieve the current or next meal (`get_current_or_next_meal`)
#  - Get the restaurant status (`get_estia_status`)
#- **HomeScreenScreen** also reads the username from the settings file to personalize the greeting.
#- **Menu** is a pure logic/data class and does not depend on any UI classes.

## Why This Structure?

#- **Separation of Concerns:** Each class has a clear responsibility, making the code easier to maintain and extend.
#- **Reusability:** The `Menu` class can be reused in other screens (e.g., nutrition, statistics) without modification.
#- **Testability:** Logic in `Menu` can be tested independently from the UI.
#- **Scalability:** New screens or features can be added by creating new classes and plugging them into the navigation system.

## Example Communication Flow

#1. User opens the app.
#2. `HomeScreen` is initialized and displays the navigation bar and content frame.
#3. `HomeScreen.open_homescreen()` is called, which creates a `HomeScreenScreen` and calls its `display()` method.
#4. `HomeScreenScreen.display()`:
#   - Reads the username from settings.
#   - Instantiates `Menu` to get the current meal and status.
#   - Updates the UI with this information.



import customtkinter as ctk
from tkinter import messagebox
from schedule_screen import open_schedule
from mam import open_nutrition
from settings import SettingsMenuApp
from courses import CourseUI
from homescreenscreen import HomeScreenScreen
from task import open_task_screen
from statistics_screen import StatisticsClass
from spendings import ExpenseTrackerApp
from CTkMessagebox import CTkMessagebox
import os
import json

##############
#################

def open_settings(parent_frame, username=None):
    for widget in parent_frame.winfo_children():
        widget.destroy()
    settings_app = SettingsMenuApp(parent_frame, username=username)
    settings_app.main_frame.pack(fill="both", expand=True)

def open_statistics(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()
    statistics_app = StatisticsClass(parent_frame)
    statistics_app.main_frame.pack(fill="both", expand=True)

class HomeScreen:
    def __init__(self, root, username=None):
        self.root = root
        self.username = username
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
        self.root.state("zoomed")
        homescreen_screen = HomeScreenScreen(self.content_frame)
        homescreen_screen.display()

    def open_courses(self):
        self.clear_content()
        CourseUI(self.content_frame)

    def show_nutrition(self):
        self.clear_content()
        open_nutrition(self.content_frame)

    def show_schedule(self):
        self.clear_content()
        open_schedule(self.content_frame)

    def show_settings(self):
        self.clear_content()
        open_settings(self.content_frame, username=self.username)

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
        answer = CTkMessagebox(
            title="Αποσύνδεση",
            message="Είστε σίγουροι ότι θέλετε να αποσυνδεθείτε;\nWe will be sad to see you go :c",
            icon="question",
            option_1="Ναι",
            option_2="Όχι"
        ).get()
        if answer == "Ναι":
            self.root.destroy()
            from login import login_app
            login_app()

def on_closing():
    # Cancel any scheduled callbacks here if you have their IDs
    root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

if __name__ == "__main__":
    root = ctk.CTk()

    try:
        root.state("zoomed")  # Try to maximize (works on most Windows)
    except Exception:
        pass
    # Fallback: set geometry to screen size (taskbar remains visible)
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")
     
    app = HomeScreen(root)
    # root.attributes("-fullscreen", True)
    # Set 4:3 aspect ratio (e.g., 800x600)
    # root.geometry("800x600")
    # app_frame = ctk.CTkFrame(root)
    # app_frame.pack(expand=True, fill="both")

    ctk.set_appearance_mode("light")
    root.mainloop()
    # Εφαρμογή breeze theme και εμφάνιση light mode για συνέπεια
    ctk.set_default_color_theme("themes/breeze.json")
    
# We made a Tkinter application that serves as a home screen for a student management system. It includes various functionalities such as course management, scheduling, nutrition tracking, task management, statistics, and settings. Each functionality is encapsulated in its own frame, and the main application allows users to navigate between these frames using a menu bar.
# The application is designed to be user-friendly and visually appealing, with a consistent color scheme and layout. It also includes features for managing expenses and notifications, making it a comprehensive tool for students.    
# The code is modular, allowing for easy updates and additions of new features in the future. Overall, it provides a solid foundation for a student management system with a focus on usability and functionality.
# The application is built using the Tkinter library, which is a standard GUI toolkit for Python. It also utilizes customtkinter for enhanced UI components and aesthetics. The code is structured to allow for easy navigation and interaction, making it suitable for both novice and experienced users.
# The use of classes and functions helps to keep the code organized and maintainable, allowing for future enhancements and modifications without significant restructuring. The application is designed to be responsive and adaptable to different screen sizes, ensuring a smooth user experience across various devices.
# Overall our code serves as a solid foundation for a student management system, providing essential features and a user-friendly interface. It can be further expanded with additional functionalities and improvements based on user feedback and requirements.
