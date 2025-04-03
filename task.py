import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

class StopwatchTimer:
    def __init__(self, parent):
        self.parent = parent
        self.is_running = False
        self.elapsed_seconds = 0
        self.speed = 1  # Default speed

        # Create the UI
        self.frame = tk.Frame(parent, bg="#f2f2f2")
        self.frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Title with icon
        title_frame = tk.Frame(self.frame, bg="#f2f2f2")
        title_frame.pack(pady=(10, 5))

        title_icon = tk.Label(title_frame, text="⏱️", font=("Arial", 16), bg="#f2f2f2")
        title_icon.pack(side=tk.LEFT, padx=(0, 5))

        title_label = tk.Label(title_frame, text="Χρονόμετρο", font=("Arial", 16, "bold"), bg="#f2f2f2")
        title_label.pack(side=tk.LEFT)

        # Timer display frame with border and shadow effect
        timer_display_frame = tk.Frame(self.frame, bg="#ffffff", bd=1, relief=tk.RAISED)
        timer_display_frame.pack(pady=15, padx=20, ipadx=15, ipady=10)

        # Timer display
        self.time_display = tk.Label(timer_display_frame, text="00:00:00", font=("Arial", 36, "bold"), bg="#ffffff", fg="#333333")
        self.time_display.pack(pady=5)

        # Input fields for hours, minutes, and seconds
        input_frame = tk.Frame(self.frame, bg="#f2f2f2")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Ώρες:", font=("Arial", 12), bg="#f2f2f2").pack(side=tk.LEFT, padx=5)
        self.hours_input = tk.Entry(input_frame, width=3, font=("Arial", 12))
        self.hours_input.pack(side=tk.LEFT, padx=5)
        self.hours_input.insert(0, "00")

        tk.Label(input_frame, text="Λεπτά:", font=("Arial", 12), bg="#f2f2f2").pack(side=tk.LEFT, padx=5)
        self.minutes_input = tk.Entry(input_frame, width=3, font=("Arial", 12))
        self.minutes_input.pack(side=tk.LEFT, padx=5)
        self.minutes_input.insert(0, "00")

        tk.Label(input_frame, text="Δευτερόλεπτα:", font=("Arial", 12), bg="#f2f2f2").pack(side=tk.LEFT, padx=5)
        self.seconds_input = tk.Entry(input_frame, width=3, font=("Arial", 12))
        self.seconds_input.pack(side=tk.LEFT, padx=5)
        self.seconds_input.insert(0, "00")

        # Speed selection dropdown
        speed_frame = tk.Frame(self.frame, bg="#f2f2f2")
        speed_frame.pack(pady=10)
        tk.Label(speed_frame, text="Επιτάχυνση:", font=("Arial", 12), bg="#f2f2f2").pack(side=tk.LEFT, padx=5)
        self.speed_var = tk.StringVar(value="x1")
        self.speed_menu = ttk.Combobox(speed_frame, textvariable=self.speed_var, values=["x1", "x2", "x4", "x8", "x16"], state="readonly")
        self.speed_menu.pack(side=tk.LEFT, padx=5)
        self.speed_menu.bind("<<ComboboxSelected>>", self.update_speed)

        # Control buttons frame
        button_frame = tk.Frame(self.frame, bg="#f2f2f2")
        button_frame.pack(pady=10)

        # Styled buttons with gradient effect using ttk
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 11), padding=6)

        self.start_button = ttk.Button(button_frame, text="Έναρξη", style="TButton", width=12, command=self.toggle_timer)
        self.start_button.pack(side=tk.LEFT, padx=5)

        reset_button = ttk.Button(button_frame, text="Επαναφορά", style="TButton", width=12, command=self.reset_timer)
        reset_button.pack(side=tk.LEFT, padx=5)

    def update_speed(self, event):
        speed_str = self.speed_var.get()
        self.speed = int(speed_str[1:])

    def toggle_timer(self):
        try:
            hours = int(self.hours_input.get())
            minutes = int(self.minutes_input.get())
            seconds = int(self.seconds_input.get())

            if hours < 0 or minutes < 0 or seconds < 0:
                raise ValueError("Negative values are not allowed.")

            self.elapsed_seconds = hours * 3600 + minutes * 60 + seconds

            if self.elapsed_seconds <= 0:
                raise ValueError("Timer duration must be greater than zero.")
        except ValueError:
            messagebox.showwarning("Μη έγκυρη Εισαγωγή",
                                   "Παρακαλώ εισάγετε έγκυρους θετικούς ακέραιους αριθμούς για ώρες, λεπτά και δευτερόλεπτα.")
            return

        self.is_running = not self.is_running
        if self.is_running:
            self.start_button.config(text="Παύση")
            self.update_timer()
        else:
            self.start_button.config(text="Συνέχεια")

    def update_timer(self):
        if not self.is_running:
            return

        if self.elapsed_seconds <= 0:
            self.is_running = False
            self.start_button.config(text="Έναρξη")
            messagebox.showinfo("Ειδοποίηση", "Ο χρονομετρητής έληξε!")
            return

        self.elapsed_seconds -= self.speed

        # Calculate hours, minutes, seconds
        hours, remainder = divmod(self.elapsed_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Update display
        self.time_display.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")

        # Schedule the next update
        self.parent.after(1000 // self.speed, self.update_timer)

    def reset_timer(self):
        self.is_running = False
        self.elapsed_seconds = 0
        self.start_button.config(text="Έναρξη")
        self.time_display.config(text="00:00:00")
        self.hours_input.delete(0, tk.END)
        self.hours_input.insert(0, "00")
        self.minutes_input.delete(0, tk.END)
        self.minutes_input.insert(0, "00")
        self.seconds_input.delete(0, tk.END)
        self.seconds_input.insert(0, "00")

class PomodoroTimer:
    def __init__(self, parent):
        self.parent = parent
        self.is_running = False
        self.work_seconds = 25 * 60  # 25 minutes
        self.break_seconds = 5 * 60   # 5 minutes
        self.seconds_left = self.work_seconds
        self.pomodoro_count = 0
        self.is_break = False
        self.total_sessions = 0  # Total number of Pomodoro sessions
        self.completed_sessions = 0  # Completed Pomodoro sessions
        self.speed = 1  # Default speed

        self.setup_ui()

    def setup_ui(self):
        # Create main frame
        self.frame = tk.Frame(self.parent, bg="#f2f2f2")
        self.frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Title with icon
        title_frame = tk.Frame(self.frame, bg="#f2f2f2")
        title_frame.pack(pady=(10, 5))

        title_icon = tk.Label(title_frame, text="🍅", font=("Arial", 16), bg="#f2f2f2")
        title_icon.pack(side=tk.LEFT, padx=(0, 5))

        title_label = tk.Label(title_frame, text="Pomodoro", font=("Arial", 16, "bold"), bg="#f2f2f2")
        title_label.pack(side=tk.LEFT)

        # Timer display frame with border and shadow effect
        timer_display_frame = tk.Frame(self.frame, bg="#ffffff", bd=1, relief=tk.RAISED)
        timer_display_frame.pack(pady=15, padx=20, ipadx=15, ipady=10)

        # Mode label (Work/Break)
        self.mode_label = tk.Label(timer_display_frame, text="Ώρα Εργασίας", font=("Arial", 14), bg="#ffffff", fg="#d64545")
        self.mode_label.pack()

        # Timer display
        self.time_display = tk.Label(timer_display_frame, text="25:00", font=("Arial", 36, "bold"), bg="#ffffff", fg="#333333")
        self.time_display.pack(pady=5)

        # Pomodoro count
        self.count_label = tk.Label(timer_display_frame, text="Ολοκληρώθηκαν: 0", font=("Arial", 11), bg="#ffffff")
        self.count_label.pack()

        # Input for number of sessions
        session_input_frame = tk.Frame(timer_display_frame, bg="#ffffff")
        session_input_frame.pack(pady=5)
        tk.Label(session_input_frame, text="Συνεδρίες:", font=("Arial", 12), bg="#ffffff").pack(side=tk.LEFT)
        self.session_input = tk.Entry(session_input_frame, font=("Arial", 12), width=5)
        self.session_input.pack(side=tk.LEFT, padx=5)
        self.session_input.insert(0, "1")  # Default to 1 session

        # Speed selection dropdown
        speed_frame = tk.Frame(self.frame, bg="#f2f2f2")
        speed_frame.pack(pady=10)
        tk.Label(speed_frame, text="Επιτάχυνση:", font=("Arial", 12), bg="#f2f2f2").pack(side=tk.LEFT, padx=5)
        self.speed_var = tk.StringVar(value="x1")
        self.speed_menu = ttk.Combobox(speed_frame, textvariable=self.speed_var, values=["x1", "x2", "x4", "x8", "x16"], state="readonly")
        self.speed_menu.pack(side=tk.LEFT, padx=5)
        self.speed_menu.bind("<<ComboboxSelected>>", self.update_speed)

        # Control buttons frame
        button_frame = tk.Frame(self.frame, bg="#f2f2f2")
        button_frame.pack(pady=10)

        # Styled buttons using ttk
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 11), padding=6)

        # Start button
        self.start_button = ttk.Button(button_frame, text="Έναρξη", style="TButton", width=12, command=self.toggle_timer)
        self.start_button.pack(side=tk.LEFT, padx=5)

        # Reset button
        reset_button = ttk.Button(button_frame, text="Επαναφορά", style="TButton", width=12, command=self.reset_timer)
        reset_button.pack(side=tk.LEFT, padx=5)

    def update_speed(self, event):
        speed_str = self.speed_var.get()
        self.speed = int(speed_str[1:])

    def toggle_timer(self):
        try:
            self.total_sessions = int(self.session_input.get())
            if self.total_sessions <= 0:
                messagebox.showwarning("Μη έγκυρη Εισαγωγή", "Παρακαλώ εισάγετε έναν θετικό αριθμό συνεδριών.")
                return
        except ValueError:
            messagebox.showwarning("Μη έγκυρη Εισαγωγή", "Παρακαλώ εισάγετε έναν έγκυρο αριθμό συνεδριών.")
            return

        self.is_running = not self.is_running
        if self.is_running:
            self.start_button.config(text="Παύση")
            self.update_timer()
        else:
            self.start_button.config(text="Συνέχεια")

    def update_timer(self):
        if not self.is_running:
            return

        if self.seconds_left <= 0:
            self.is_running = False
            if self.is_break:
                self.mode_label.config(text="Ώρα Εργασίας", fg="#d64545")
                self.seconds_left = self.work_seconds
                messagebox.showinfo("Ειδοποίηση", "Το διάλειμμα τελείωσε! Ώρα για εργασία.")
            else:
                self.mode_label.config(text="Διάλειμμα", fg="#45d65e")
                self.seconds_left = self.break_seconds
                messagebox.showinfo("Ειδοποίηση", "Η εργασία τελείωσε! Ώρα για διάλειμμα.")
            self.start_button.config(text="Έναρξη")
            return

        self.seconds_left -= self.speed

        minutes, seconds = divmod(self.seconds_left, 60)
        self.time_display.config(text=f"{minutes:02d}:{seconds:02d}")
        self.parent.after(1000 // self.speed, self.update_timer)

    def reset_timer(self):
        self.is_running = False
        self.start_button.config(text="Έναρξη")
        self.is_break = False
        self.seconds_left = self.work_seconds
        self.mode_label.config(text="Ώρα Εργασίας", fg="#d64545")
        self.time_display.config(text="25:00")
        self.pomodoro_count = 0
        self.completed_sessions = 0
        self.count_label.config(text="Ολοκληρώθηκαν: 0")
        self.session_input.delete(0, tk.END)
        self.session_input.insert(0, "1")

class TaskScreen:
    def __init__(self, parent):
        self.parent = parent
        self.tasks = []
        self.streak_days = 7  # Example streak count

        # Create main container with sections
        self.main_frame = tk.Frame(parent, bg="#f2f2f2")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create top section for Streak
        self.streak_frame = tk.Frame(self.main_frame, bg="#f2f2f2", bd=1, relief=tk.RIDGE)
        self.streak_frame.pack(fill=tk.X, padx=20, pady=10)
        self.setup_streak_widget()

        # Create button frame for "Χρονομετρητές" and "Εργασίες"
        self.button_frame = tk.Frame(self.main_frame, bg="#f2f2f2", bd=1, relief=tk.RIDGE)
        self.button_frame.pack(fill=tk.X, padx=20, pady=10)

        self.timers_button = tk.Button(self.button_frame, text="Χρονομετρητές", command=self.show_timers)
        self.timers_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.tasks_button = tk.Button(self.button_frame, text="Εργασίες", command=self.show_tasks)
        self.tasks_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Create content frame that will be updated
        self.content_frame = tk.Frame(self.main_frame, bg="#f2f2f2", bd=1, relief=tk.RIDGE)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    def setup_streak_widget(self):
        streak_container = tk.Frame(self.streak_frame, bg="#f0f0f0")
        streak_container.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(streak_container, text="Συνεχόμενες Ημέρες", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(anchor="w")

        flame_icon = "🔥"

        streak_display = tk.Frame(streak_container, bg="#f0f0f0")
        streak_display.pack(fill=tk.X, pady=5)

        tk.Label(streak_display, text=flame_icon, font=("Arial", 24), bg="#f0f0f0").pack(side=tk.LEFT)

        tk.Label(streak_display, text=str(self.streak_days), font=("Arial", 24, "bold"), bg="#f0f0f0").pack(side=tk.LEFT)

        tk.Label(streak_container, text="Συνέχισε την καλή δουλειά! Ολοκλήρωσε όλες τις εργασίες για να διατηρήσεις το σερί σου.", font=("Arial", 10), bg="#f0f0f0").pack(anchor="w", pady=5)

    def show_timers(self):
        self.clear_content_frame()

        # Timer section - use a nicer frame with border
        self.timer_frame = tk.Frame(self.content_frame, bg="#f2f2f2", bd=1, relief=tk.RIDGE)
        self.timer_frame.pack(fill=tk.X, padx=20, pady=10)

        # Title for timer section
        timer_header = tk.Label(self.timer_frame, text="Χρονόμετρα", font=("Arial", 14, "bold"), bg="#e0e0e0")
        timer_header.pack(fill=tk.X, pady=5)

        # Create a horizontal container for both timers
        self.timer_container = tk.Frame(self.timer_frame, bg="#f2f2f2")
        self.timer_container.pack(fill=tk.X, padx=10, pady=10)

        # Left side: Pomodoro Timer
        self.pomodoro_container = tk.Frame(self.timer_container, bg="#f2f2f2", bd=1, relief=tk.GROOVE)
        self.pomodoro_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.pomodoro = PomodoroTimer(self.pomodoro_container)

        # Right side: Stopwatch
        self.stopwatch_container = tk.Frame(self.timer_container, bg="#f2f2f2", bd=1, relief=tk.GROOVE)
        self.stopwatch_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.stopwatch = StopwatchTimer(self.stopwatch_container)

    def show_tasks(self):
        self.clear_content_frame()

        # Create middle section for To-Do List
        self.todo_frame = tk.Frame(self.content_frame, bg="#f2f2f2", bd=1, relief=tk.RIDGE)
        self.todo_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.setup_todo_list()

    def setup_todo_list(self):
        # To-Do list header
        todo_header = tk.Frame(self.todo_frame, bg="#e0e0e0")
        todo_header.pack(fill=tk.X, pady=0)

        tk.Label(todo_header, text="Σημερινές Εργασίες", font=("Arial", 14, "bold"), bg="#e0e0e0").pack(side=tk.LEFT,
                                                                                                        padx=10, pady=5)

        add_btn = tk.Button(todo_header, text="Προσθήκη Εργασίας", command=self.add_task)
        add_btn.pack(side=tk.RIGHT, padx=10, pady=5)

        # Create scrollable frame for tasks
        self.tasks_frame = tk.Frame(self.todo_frame, bg="#f8f8f8")
        self.tasks_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)  # Increased padding

        # Add scrollbar
        self.scrollbar = tk.Scrollbar(self.tasks_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a canvas to hold the tasks
        self.canvas = tk.Canvas(self.tasks_frame, bg="#f8f8f8", yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)  # Increased padding

        # Configure scrollbar
        self.scrollbar.config(command=self.canvas.yview)

        # Create an inner frame to hold the tasks
        self.inner_frame = tk.Frame(self.canvas, bg="#f8f8f8")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="n")  # Centered with anchor="n"

        # Bind the inner frame to the canvas scroll region
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Add example tasks
        self.add_example_tasks()

    def add_example_tasks(self):
        example_tasks = [
            "Ολοκλήρωση εργασίας Μαθηματικών",
            "Διάβασμα κεφαλαίου 3 για τη Φυσική",
            "Προετοιμασία παρουσίασης για την Πληροφορική",
            "Αποστολή email στον καθηγητή για το ερευνητικό έργο"
        ]

        for task in example_tasks:
            self.add_task_to_list(task)

    def add_task(self):
        task_text = simpledialog.askstring("Προσθήκη Εργασίας", "Εισάγετε νέα εργασία:")
        if not task_text:
            messagebox.showwarning("Μη έγκυρη Εισαγωγή", "Παρακαλώ εισάγετε ένα όνομα για την εργασία.")
            return
        self.add_task_to_list(task_text)

    def add_task_to_list(self, task_text):
        task_frame = tk.Frame(self.inner_frame, bg="#ffffff", bd=1, relief=tk.SOLID)
        task_frame.pack(fill=tk.X, pady=2)

        var = tk.BooleanVar(value=False)
        cb = tk.Checkbutton(task_frame, variable=var, command=lambda v=var: self.update_task_completed(v), bg="#ffffff")
        cb.pack(side=tk.LEFT)

        task_label = tk.Label(task_frame, text=task_text, bg="#ffffff", anchor="w")
        task_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.tasks.append({"text": task_text, "var": var, "label": task_label})

    def update_task_completed(self, var):
        # Update the appearance of completed tasks
        for task in self.tasks:
            if task["var"] == var:
                if var.get():
                    task["label"].config(fg="#888888", font=("Arial", 10, "overstrike"))
                else:
                    task["label"].config(fg="#000000", font=("Arial", 10))
                break

        # Check if all tasks are completed to update streak
        self.check_streak_update()

    def check_streak_update(self):
        completed = sum(1 for task in self.tasks if task["var"].get())
        if completed > 0 and completed == len(self.tasks):
            # All tasks completed - would update streak in a real app
            pass

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

def open_task_screen(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()

    task_screen = TaskScreen(parent_frame)