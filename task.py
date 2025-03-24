import tkinter as tk
from tkinter import ttk, simpledialog
import time
import datetime

class TaskScreen:
    def __init__(self, parent):
        self.parent = parent
        self.tasks = []
        self.streak_days = 7  # Example streak count
        
        # Create main container with 3 sections
        self.main_frame = tk.Frame(parent, bg="#f2f2f2")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create top section for Pomodoro
        self.pomodoro_frame = tk.Frame(self.main_frame, bg="#f2f2f2")
        self.pomodoro_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Add pomodoro timer to top section
        self.pomodoro = PomodoroTimer(self.pomodoro_frame)
        
        # Create middle section for To-Do List
        self.todo_frame = tk.Frame(self.main_frame, bg="#f2f2f2", bd=1, relief=tk.RIDGE)
        self.todo_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.setup_todo_list()
        
        # Create bottom section for Streak
        self.streak_frame = tk.Frame(self.main_frame, bg="#f2f2f2", bd=1, relief=tk.RIDGE)
        self.streak_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.setup_streak_widget()
    
    def setup_todo_list(self):
        # To-Do list header
        todo_header = tk.Frame(self.todo_frame, bg="#e0e0e0")
        todo_header.pack(fill=tk.X, pady=0)
        
        tk.Label(todo_header, text="Σημερινές Εργασίες", font=("Arial", 14, "bold"), 
                bg="#e0e0e0").pack(side=tk.LEFT, padx=10, pady=5)
        
        add_btn = tk.Button(todo_header, text="Προσθήκη Εργασίας", command=self.add_task)
        add_btn.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Create scrollable frame for tasks
        self.tasks_frame = tk.Frame(self.todo_frame, bg="#f8f8f8")
        self.tasks_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add example tasks
        self.add_example_tasks()
    
    def add_example_tasks(self):
        example_tasks = [
            "Ολοκλήρωση εργασίας Μαθηματικών",
            "Διάβασμα κεφαλαίου 3 για τη Φυσική",
            "Προετοιμασία παρουσίασης για την Πληροφορική",
            "Email στον καθηγητή για το ερευνητικό project"
        ]
        
        for task in example_tasks:
            self.add_task_to_list(task)
    
    def add_task(self):
        task_text = simpledialog.askstring("Προσθήκη Εργασίας", "Εισάγετε νέα εργασία:")
        if task_text:
            self.add_task_to_list(task_text)
    
    def add_task_to_list(self, task_text):
        task_frame = tk.Frame(self.tasks_frame, bg="#ffffff", bd=1, relief=tk.SOLID)
        task_frame.pack(fill=tk.X, pady=2)
        
        var = tk.BooleanVar(value=False)
        cb = tk.Checkbutton(task_frame, variable=var, 
                          command=lambda v=var: self.update_task_completed(v),
                          bg="#ffffff")
        cb.pack(side=tk.LEFT)
        
        task_label = tk.Label(task_frame, text=task_text, 
                             bg="#ffffff", anchor="w")
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
    
    def setup_streak_widget(self):
        streak_container = tk.Frame(self.streak_frame, bg="#f0f0f0")
        streak_container.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(streak_container, text="Συνεχόμενες Ημέρες", 
                font=("Arial", 14, "bold"), bg="#f0f0f0").pack(anchor="w")
        
        flame_icon = "🔥" 
        
        streak_display = tk.Frame(streak_container, bg="#f0f0f0")
        streak_display.pack(fill=tk.X, pady=5)
        
        tk.Label(streak_display, text=flame_icon, 
                font=("Arial", 24), bg="#f0f0f0").pack(side=tk.LEFT)
        
        tk.Label(streak_display, text=str(self.streak_days), 
                font=("Arial", 24, "bold"), bg="#f0f0f0").pack(side=tk.LEFT)
        
        tk.Label(streak_container, 
                text="Συνέχισε την καλή δουλειά! Ολοκλήρωσε όλες τις εργασίες για να διατηρήσεις το σερί σου.",
                font=("Arial", 10), bg="#f0f0f0").pack(anchor="w", pady=5)

class PomodoroTimer:
    def __init__(self, parent):
        self.parent = parent
        self.is_running = False
        self.work_seconds = 25 * 60  # 25 minutes
        self.break_seconds = 5 * 60   # 5 minutes
        self.seconds_left = self.work_seconds
        self.pomodoro_count = 0
        self.is_break = False
        
        self.setup_ui()
    
    def setup_ui(self):
        # Create main frame
        self.frame = tk.Frame(self.parent, bg="#f2f2f2")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(self.frame, text="Χρονόμετρο Pomodoro", font=("Arial", 18, "bold"), bg="#f2f2f2")
        title_label.pack(pady=20)
        
        # Timer display frame
        timer_frame = tk.Frame(self.frame, bg="#f2f2f2")
        timer_frame.pack(pady=20)
        
        # Mode label (Work/Break)
        self.mode_label = tk.Label(timer_frame, text="Ώρα Εργασίας", font=("Arial", 14), bg="#f2f2f2", fg="#d64545")
        self.mode_label.pack()
        
        # Timer display
        self.time_display = tk.Label(timer_frame, text="25:00", font=("Arial", 48), bg="#f2f2f2")
        self.time_display.pack(pady=10)
        
        # Pomodoro count
        self.count_label = tk.Label(timer_frame, text="Ολοκληρώθηκαν: 0", font=("Arial", 12), bg="#f2f2f2")
        self.count_label.pack()
        
        # Control buttons frame
        button_frame = tk.Frame(self.frame, bg="#f2f2f2")
        button_frame.pack(pady=20)
        
        # Start button
        self.start_button = tk.Button(button_frame, text="Έναρξη", font=("Arial", 12), 
                                      width=10, command=self.toggle_timer)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        # Reset button
        reset_button = tk.Button(button_frame, text="Επαναφορά", font=("Arial", 12), 
                                width=10, command=self.reset_timer)
        reset_button.pack(side=tk.LEFT, padx=5)
    
    def toggle_timer(self):
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
            # Timer finished
            if self.is_break:
                # Break finished, start work
                self.is_break = False
                self.seconds_left = self.work_seconds
                self.mode_label.config(text="Ώρα Εργασίας", fg="#d64545")
            else:
                # Work finished, start break
                self.is_break = True
                self.pomodoro_count += 1
                self.count_label.config(text=f"Ολοκληρώθηκαν: {self.pomodoro_count}")
                self.seconds_left = self.break_seconds
                self.mode_label.config(text="Ώρα Διαλείμματος", fg="#45d645")
        
        minutes, seconds = divmod(self.seconds_left, 60)
        self.time_display.config(text=f"{minutes:02d}:{seconds:02d}")
        self.seconds_left -= 1
        self.parent.after(1000, self.update_timer)
    
    def reset_timer(self):
        self.is_running = False
        self.start_button.config(text="Έναρξη")
        self.is_break = False
        self.seconds_left = self.work_seconds
        self.mode_label.config(text="Ώρα Εργασίας", fg="#d64545")
        self.time_display.config(text="25:00")

def open_task_screen(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()
        
    task_screen = TaskScreen(parent_frame)
