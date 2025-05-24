import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import datetime
from error_control import ErrorControl

class CTkInputDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, prompt):
        super().__init__(parent)
        self.title(title)
        self.geometry("350x150")
        self.resizable(False, False)
        self.value = None

        ctk.CTkLabel(self, text=prompt, font=("Arial", 12)).pack(pady=(20, 10))
        self.entry = ctk.CTkEntry(self, width=250)
        self.entry.pack(pady=5)
        self.entry.focus()

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="OK", command=self.on_ok).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Cancel", command=self.on_cancel).pack(side="left", padx=10)

        self.bind("<Return>", lambda event: self.on_ok())
        self.bind("<Escape>", lambda event: self.on_cancel())

        self.grab_set()
        self.wait_window()

    def on_ok(self):
        self.value = self.entry.get()
        self.destroy()

    def on_cancel(self):
        self.value = None
        self.destroy()

class TaskScreen:
    def __init__(self, parent):
        self.parent = parent
        self.tasks = []
        self.streak_days = 7

        self.main_frame = ctk.CTkFrame(parent)
        self.main_frame.pack(fill="both", expand=True)

        self.streak_frame = ctk.CTkFrame(self.main_frame)
        self.streak_frame.pack(fill="x", padx=20, pady=10)
        self.setup_streak_widget()

        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(fill="x", padx=20, pady=10)
        self.tasks_button = ctk.CTkButton(self.button_frame, text="Εργασίες", command=self.show_tasks)
        self.tasks_button.pack(side="left", padx=10, pady=5)
        self.zonein_button = ctk.CTkButton(self.button_frame, text="Zone In", command=self.open_zonein)
        self.zonein_button.pack(side="left", padx=10, pady=5)

        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)

    def open_zonein(self):
        self.clear_content_frame()
        from zonein import open_zonein_screen  # Local import to avoid circular import issues
        open_zonein_screen(self.content_frame)

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
        # To-Do list header
        todo_header = ctk.CTkFrame(self.todo_frame)
        todo_header.pack(fill="x", pady=0)
        ctk.CTkLabel(todo_header, text="Σημερινές Εργασίες", font=("Arial", 14, "bold")).pack(side="left", padx=10, pady=5)
        add_btn = ctk.CTkButton(todo_header, text="Προσθήκη Εργασίας", command=self.add_task)
        add_btn.pack(side="right", padx=10, pady=5)

        # Create scrollable frame for tasks
        self.tasks_frame = ctk.CTkScrollableFrame(self.todo_frame, orientation="vertical")
        self.tasks_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.tasks = []  # Clear the tasks list each time you set up the todo list

        # Add tasks from events.txt
        self.add_example_tasks()

    
    def add_example_tasks(self):
    # Clear any existing widgets in the tasks_frame before adding new ones
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()
        self.tasks = []

    # Load real events from file
        events = self.load_events_from_file()
        today = datetime.datetime.now().date()
        has_future_events = False

        for date_str, event_name, event_hour in events:
            try:
            # Try parsing the date in both possible formats
                for fmt in ("%d/%m/%Y", "%m/%d/%y"):
                    try:
                        event_date = datetime.datetime.strptime(date_str.strip(), fmt).date()
                        break
                    except ValueError:
                     continue
                else:
                    continue  # Skip if date format is not recognized

                if event_date >= today:
                    task_str = f"{event_name} ({date_str} {event_hour})"
                    self.add_task_to_list(task_str)
                    has_future_events = True
            except Exception:
                continue  # Skip malformed lines

        if not has_future_events:
            self.add_task_to_list("Δεν υπάρχουν προγραμματισμένες εργασίες.")

   
    def add_task(self):
        task_text = CTkInputDialog(self.parent, "Προσθήκη Εργασίας", "Εισάγετε νέα εργασία:").value
        if not task_text:
            CTkMessagebox(title="Μη έγκυρη Εισαγωγή", message="Παρακαλώ εισάγετε ένα όνομα για την εργασία.", icon="warning")
            return
        task_time = CTkInputDialog(self.parent, "Προσθήκη Ώρας", "Εισάγετε ώρα (π.χ. 14:00):").value
        if not task_time:
            CTkMessagebox(title="Μη έγκυρη Εισαγωγή", message="Παρακαλώ εισάγετε μια ώρα.", icon="warning")
            return
        
        date_str = datetime.datetime.now().strftime('%d/%m/%Y')
        if not ErrorControl.is_time_slot_available(date_str, task_time):
            CTkMessagebox(title="Σύγκρουση Ώρας", message="Υπάρχει ήδη εργασία για αυτή την ημερομηνία και ώρα.", icon="warning")
            return
        # Save to events.txt with both task and time
        with open("events.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.datetime.now().strftime('%d/%m/%Y')}|{task_text}|{task_time}\n")

        self.add_task_to_list(f"{task_text} ({datetime.datetime.now().strftime('%d/%m/%Y')} {task_time})")

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
            pass  # Add your streak logic here

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def load_events_from_file(self):
        events = []
        try:
            with open("events.txt", "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) == 3:
                        events.append(tuple(parts))
        except FileNotFoundError:
            pass
        return events

def open_task_screen(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()
    TaskScreen(parent_frame)