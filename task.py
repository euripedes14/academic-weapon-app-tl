import customtkinter as ctk
from tkinter import simpledialog, messagebox
from courses import chosen_subjects
from zonein import open_zonein_screen #change


# Εφαρμογή breeze theme
ctk.set_default_color_theme("themes/breeze.json")



class TaskScreen:
    def __init__(self, parent):
        self.parent = parent
        self.tasks = []
        self.streak_days = 7

        self.main_frame = ctk.CTkFrame(parent)
        self.main_frame.pack(fill="both", expand=True)

        # self.subjects_frame = ctk.CTkFrame(self.main_frame)
        # self.subjects_frame.pack(fill="x", padx=20, pady=10)
        # self.setup_subject_widget()

        self.streak_frame = ctk.CTkFrame(self.main_frame)
        self.streak_frame.pack(fill="x", padx=20, pady=10)
        self.setup_streak_widget()

        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(fill="x", padx=20, pady=10)
        # self.timers_button = ctk.CTkButton(self.button_frame, text="Χρονομετρητές", command=self.show_timers)
        # self.timers_button.pack(side="left", padx=10, pady=5)
        self.tasks_button = ctk.CTkButton(self.button_frame, text="Εργασίες", command=self.show_tasks)
        self.tasks_button.pack(side="left", padx=10, pady=5)

        #######
        self.zonein_button = ctk.CTkButton(self.button_frame, text="Zone In", command=self.open_zonein)
        self.zonein_button.pack(side="left", padx=10, pady=5)
        #########

        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)

#############
    def open_zonein(self):
        self.clear_content_frame()
        from zonein import open_zonein_screen  # Local import to avoid circular import issues
        open_zonein_screen(self.content_frame)
#########

    # def setup_subject_widget(self):
    #     subject_container = ctk.CTkFrame(self.subjects_frame)
    #     subject_container.pack(fill="x", padx=10, pady=10)
    #     # Optionally, add a label or leave empty if you want
    #     ctk.CTkLabel(subject_container, text="Επιλογή μαθημάτων γίνεται πλέον από το Zone In.", font=("Arial", 12, "italic")).pack(padx=10, pady=10)

    def setup_streak_widget(self):
        streak_container = ctk.CTkFrame(self.streak_frame)
        streak_container.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(streak_container, text="Συνεχόμενες Ημέρες", font=("Arial", 14, "bold")).pack(anchor="w")
        flame_icon = "🔥"
        streak_display = ctk.CTkFrame(streak_container)
        streak_display.pack(fill="x", pady=5)
        ctk.CTkLabel(streak_display, text=flame_icon, font=("Arial", 24)).pack(side="left")
        ctk.CTkLabel(streak_display, text=str(self.streak_days), font=("Arial", 24, "bold")).pack(side="left")
        ctk.CTkLabel(streak_container, text="Συνέχισε την καλή δουλειά! Ολοκλήρωσε όλες τις εργασίες για να διατηρήσεις το σερί σου.", font=("Arial", 10)).pack(anchor="w", pady=5)


    def show_tasks(self):
        self.clear_content_frame()
        self.todo_frame = ctk.CTkFrame(self.content_frame)
        self.todo_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.setup_todo_list()

    def setup_todo_list(self):
        todo_header = ctk.CTkFrame(self.todo_frame)
        todo_header.pack(fill="x", pady=0)
        ctk.CTkLabel(todo_header, text="Σημερινές Εργασίες", font=("Arial", 14, "bold")).pack(side="left", padx=10, pady=5)
        add_btn = ctk.CTkButton(todo_header, text="Προσθήκη Εργασίας", command=self.add_task)
        add_btn.pack(side="right", padx=10, pady=5)

        self.tasks_frame = ctk.CTkScrollableFrame(self.todo_frame, orientation="vertical")
        self.tasks_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.add_example_tasks()

    def add_example_tasks(self):
        example_tasks = [
            "User example task 1"
        ]
        # Read events from file and add them as tasks
        try:
            with open("events.txt", "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) == 3:
                        date, event_name, event_hour = parts
                        task_str = f"{event_name} ({date} {event_hour})"
                        example_tasks.append(task_str)
        except FileNotFoundError:
            pass

        for task in example_tasks:
            self.add_task_to_list(task)
        

    def add_task_to_list(self, task_text):
        task_frame = ctk.CTkFrame(self.tasks_frame)
        task_frame.pack(fill="x", pady=2)
        var = ctk.BooleanVar(value=False)
        cb = ctk.CTkCheckBox(task_frame, variable=var, command=lambda v=var: self.update_task_completed(v), text="")
        cb.pack(side="left")
        task_label = ctk.CTkLabel(task_frame, text=task_text, anchor="w")
        task_label.pack(side="left", fill="x", expand=True, padx=5)
        self.tasks.append({"text": task_text, "var": var, "label": task_label})

    def update_task_completed(self, var):
        for task in self.tasks:
            if task["var"] == var:
                if var.get():
                    task["label"].configure(text_color="#888888", font=("Arial", 10, "overstrike"))
                else:
                    task["label"].configure(text_color="#000000", font=("Arial", 10))
                break
        self.check_streak_update()

    def check_streak_update(self):
        completed = sum(1 for task in self.tasks if task["var"].get())
        if completed > 0 and completed == len(self.tasks):
            pass

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

def open_task_screen(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()
    TaskScreen(parent_frame)
