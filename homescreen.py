import tkinter as tk
from tkinter import messagebox
from schedule_screen import open_schedule     # Import the open_schedule function
from mam import open_nutrition                # Import the open_nutrition function
from settings import SettingsMenuApp
from courses import open_courses_screen
from homescreenscreen import HomeScreenScreen  # Import the HomeScreenScreen class
from task import open_task_screen  # Import the new task screen function
from statistics_screen import StatisticsClass
from spendings import ExpenseTrackerApp  # Import the ExpenseTrackerApp class

def open_settings(parent_frame):
    """Display the settings screen in the given parent frame."""
    for widget in parent_frame.winfo_children():  # Clear previous contents of the frame
        widget.destroy()

    # Create and display the SettingsMenuApp in the parent frame
    settings_app = SettingsMenuApp(parent_frame)  # Pass the parent frame as the root
    settings_app.main_frame.pack(fill="both", expand=True)

def open_statistics(parent_frame):
    ## Display the statistics screen
    for widget in parent_frame.winfo_children():  # Clear previous contents of the frame
        widget.destroy()

    # Create and display the StatisticsApp in the parent frame
    statistics_app = StatisticsClass(parent_frame)  # Pass the parent frame as the root
    statistics_app.main_frame.pack(fill="both", expand=True)
    

class HomeScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("LockIN - Αρχική Οθόνη")
        self.root.state("zoomed")

        # Frames για διαφορετικές λειτουργίες
        self.homescreen_frame = None
        self.schedule_frame = tk.Frame(root, bg="#f2f2f2")
        self.nutrition_frame = tk.Frame(root, bg="#f2f2f2")
        self.settings_frame = None
        self.statistics_frame = None
        # Initialize other frames to avoid AttributeError
        self.courses_frame = None
        self.tasks_frame = None
        self.spendings_frame = None  # Initialize spendings frame

        self.create_menu()
        self.create_title()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        menu_bar.add_command(label="Αρχική Οθόνη", command=self.open_homescreen)
        menu_bar.add_command(label="Εισαγωγή Μαθημάτων", command=self.open_courses)
        menu_bar.add_command(label="Τι έχει το πρόγραμμα?", command=self.show_schedule)
        menu_bar.add_command(label="Τι θα φάμε σήμερα?", command=self.show_nutrition)
        menu_bar.add_command(label="Εργασίες", command=self.open_tasks)  # Use Greek for consistency
        menu_bar.add_command(label="Στατιστικά", command=self.show_statistics)
        menu_bar.add_command(label="Διαχείριση Εξόδων", command=self.open_spendings)  # Add Spendings menu option
        menu_bar.add_command(label="Ρυθμίσεις", command=self.show_settings)  # Σύνδεση με τη ρύθμιση
        

    def create_title(self):
        label = tk.Label(self.root, text="Καλώς ήρθατε στο LockIN", font=("Arial", 14))
        label.pack(pady=20)
        if self.statistics_frame:
            self.statistics_frame.pack_forget()

    def open_homescreen(self):
        """Open the home screen."""
        self.hide_all_frames()
        if self.homescreen_frame is None:
            self.homescreen_frame = tk.Frame(self.root, bg="#f2f2f2")
        self.homescreen_frame.pack(fill=tk.BOTH, expand=True)

        # Use the HomeScreenScreen class to display the home screen
        homescreen_screen = HomeScreenScreen(self.homescreen_frame)
        homescreen_screen.display()

    def open_courses(self):
        """Open the courses screen."""
        self.hide_all_frames()
        if self.courses_frame is None:
            self.courses_frame = tk.Frame(self.root, bg="#f2f2f2")
        self.courses_frame.pack(fill=tk.BOTH, expand=True)
        # Remove the local import that's causing issues
        open_courses_screen(self.courses_frame, self)

    def open_notifications(self):
        messagebox.showinfo("Ειδοποιήσεις & Streaks", "Μεταφορά στην οθόνη ειδοποιήσεων.")

    def hide_all_frames(self):
        """Απόκρυψη όλων των άλλων frames όταν επιλέγεται μία λειτουργία."""
        if hasattr(self, "homescreen_frame") and self.homescreen_frame:
            self.homescreen_frame.pack_forget()
        if hasattr(self, "schedule_frame") and self.schedule_frame:
            self.schedule_frame.pack_forget()
        if hasattr(self, "nutrition_frame") and self.nutrition_frame:
            self.nutrition_frame.pack_forget()
        if hasattr(self, "settings_frame") and self.settings_frame:
            self.settings_frame.pack_forget()
        if hasattr(self, "courses_frame") and self.courses_frame:
            self.courses_frame.pack_forget()
        if hasattr(self, "tasks_frame") and self.tasks_frame:
            self.tasks_frame.pack_forget()
        if hasattr(self, "statistics_frame") and self.statistics_frame:
            self.statistics_frame.pack_forget()
        if hasattr(self, "spendings_frame") and self.spendings_frame:
            self.spendings_frame.pack_forget()
        if hasattr(self, "homescreen_frame") and self.homescreen_frame:
            self.homescreen_frame.pack_forget()

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

    def show_statistics(self):
        ## Display the statistics screen

        self.hide_all_frames()
        if not self.statistics_frame:
            self.statistics_frame = tk.Frame(self.root, bg='#ffffff')
            self.statistics_frame.pack(fill=tk.BOTH, expand=True)

        open_statistics(self.statistics_frame)
        self.statistics_frame.pack(fill=tk.BOTH, expand=True)

    def open_tasks(self):
        """Open the tasks screen with Pomodoro timer."""
        self.hide_all_frames()
        if self.tasks_frame is None:
            self.tasks_frame = tk.Frame(self.root, bg="#f2f2f2")
        self.tasks_frame.pack(fill=tk.BOTH, expand=True)
        open_task_screen(self.tasks_frame)

    def open_spendings(self):
        """Open the spendings screen."""
        self.hide_all_frames()
        if self.spendings_frame is None:
            self.spendings_frame = tk.Frame(self.root, bg="#f2f2f2")
            self.spendings_frame.pack(fill=tk.BOTH, expand=True)
            ExpenseTrackerApp(self.spendings_frame)  # Initialize ExpenseTrackerApp in the frame
        else:
            self.spendings_frame.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = HomeScreen(root)
    app.open_homescreen()

    # this should always be last
    root.mainloop()
    
# We made a Tkinter application that serves as a home screen for a student management system. It includes various functionalities such as course management, scheduling, nutrition tracking, task management, statistics, and settings. Each functionality is encapsulated in its own frame, and the main application allows users to navigate between these frames using a menu bar.
# The application is designed to be user-friendly and visually appealing, with a consistent color scheme and layout. It also includes features for managing expenses and notifications, making it a comprehensive tool for students.    
# The code is modular, allowing for easy updates and additions of new features in the future. Overall, it provides a solid foundation for a student management system with a focus on usability and functionality.
# The application is built using the Tkinter library, which is a standard GUI toolkit for Python. It also utilizes customtkinter for enhanced UI components and aesthetics. The code is structured to allow for easy navigation and interaction, making it suitable for both novice and experienced users.
# The use of classes and functions helps to keep the code organized and maintainable, allowing for future enhancements and modifications without significant restructuring. The application is designed to be responsive and adaptable to different screen sizes, ensuring a smooth user experience across various devices.
# Overall our code serves as a solid foundation for a student management system, providing essential features and a user-friendly interface. It can be further expanded with additional functionalities and improvements based on user feedback and requirements.


