import tkinter as tk
from tkinter import ttk, simpledialog
import time
import datetime

class StopwatchTimer:
    def __init__(self, parent):
        self.parent = parent
        self.is_running = False
        self.elapsed_seconds = 0
        
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
        
        # Control buttons frame
        button_frame = tk.Frame(self.frame, bg="#f2f2f2")
        button_frame.pack(pady=10)
        
        # Styled buttons with gradient effect using ttk
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 11), padding=6)
        
        self.start_button = ttk.Button(button_frame, text="Έναρξη", style="TButton",
                                    width=12, command=self.toggle_timer)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        reset_button = ttk.Button(button_frame, text="Μηδενισμός", style="TButton",
                               width=12, command=self.reset_timer)
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
            
        self.elapsed_seconds += 1
        
        # Calculate hours, minutes, seconds
        hours, remainder = divmod(self.elapsed_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        # Update display
        self.time_display.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        
        # Schedule the next update
        self.parent.after(1000, self.update_timer)
    
    def reset_timer(self):
        self.is_running = False
        self.elapsed_seconds = 0
        self.start_button.config(text="Έναρξη")
        self.time_display.config(text="00:00:00")

class TaskScreen:
    def __init__(self, parent):
        self.parent = parent
        self.tasks = []
        self.streak_days = 7  # Example streak count
        
        # Create main container with sections
        self.main_frame = tk.Frame(parent, bg="#f2f2f2")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Timer section - use a nicer frame with border
        self.timer_frame = tk.Frame(self.main_frame, bg="#f2f2f2", bd=1, relief=tk.RIDGE)
        self.timer_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Title for timer section
        timer_header = tk.Label(self.timer_frame, text="Χρονομετρητές", 
                               font=("Arial", 14, "bold"), bg="#e0e0e0")
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
        
        # Control buttons frame
        button_frame = tk.Frame(self.frame, bg="#f2f2f2")
        button_frame.pack(pady=10)
        
        # Styled buttons using ttk
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 11), padding=6)
        
        # Start button
        self.start_button = ttk.Button(button_frame, text="Έναρξη", style="TButton", 
                                      width=12, command=self.toggle_timer)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        # Reset button
        reset_button = ttk.Button(button_frame, text="Επαναφορά", style="TButton", 
                                width=12, command=self.reset_timer)
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
