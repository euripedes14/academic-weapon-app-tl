import customtkinter as ctk
from tkinter import simpledialog, messagebox
from courses import chosen_subjects

# Εφαρμογή breeze theme
ctk.set_default_color_theme("themes/breeze.json")

class StopwatchTimer:
    def __init__(self, parent):
        self.parent = parent
        self.is_running = False
        self.elapsed_seconds = 0
        self.speed = 1

        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True, padx=5, pady=5)

        title_frame = ctk.CTkFrame(self.frame)
        title_frame.pack(pady=(10, 5), fill="x")
        ctk.CTkLabel(title_frame, text="⏱️", font=("Arial", 16)).pack(side="left", padx=(0, 5))
        ctk.CTkLabel(title_frame, text="Χρονόμετρο", font=("Arial", 16, "bold")).pack(side="left")

        timer_display_frame = ctk.CTkFrame(self.frame)
        timer_display_frame.pack(pady=15, padx=20, ipadx=15, ipady=10)
        self.time_display = ctk.CTkLabel(timer_display_frame, text="00:00:00", font=("Arial", 36, "bold"))
        self.time_display.pack(pady=5)

        input_frame = ctk.CTkFrame(self.frame)
        input_frame.pack(pady=10)
        ctk.CTkLabel(input_frame, text="Ώρες:", font=("Arial", 12)).pack(side="left", padx=5)
        self.hours_input = ctk.CTkEntry(input_frame, width=40, font=("Arial", 12))
        self.hours_input.pack(side="left", padx=5)
        self.hours_input.insert(0, "00")
        ctk.CTkLabel(input_frame, text="Λεπτά:", font=("Arial", 12)).pack(side="left", padx=5)
        self.minutes_input = ctk.CTkEntry(input_frame, width=40, font=("Arial", 12))
        self.minutes_input.pack(side="left", padx=5)
        self.minutes_input.insert(0, "00")
        ctk.CTkLabel(input_frame, text="Δευτερόλεπτα:", font=("Arial", 12)).pack(side="left", padx=5)
        self.seconds_input = ctk.CTkEntry(input_frame, width=40, font=("Arial", 12))
        self.seconds_input.pack(side="left", padx=5)
        self.seconds_input.insert(0, "00")

        speed_frame = ctk.CTkFrame(self.frame)
        speed_frame.pack(pady=10)
        ctk.CTkLabel(speed_frame, text="Επιτάχυνση:", font=("Arial", 12)).pack(side="left", padx=5)
        self.speed_var = ctk.StringVar(value="x1")
        self.speed_menu = ctk.CTkComboBox(speed_frame, variable=self.speed_var, values=["x1", "x2", "x4", "x8", "x16"], width=80, command=self.update_speed)
        self.speed_menu.pack(side="left", padx=5)

        button_frame = ctk.CTkFrame(self.frame)
        button_frame.pack(pady=10)
        self.start_button = ctk.CTkButton(button_frame, text="Έναρξη", width=120, command=self.toggle_timer)
        self.start_button.pack(side="left", padx=5)
        reset_button = ctk.CTkButton(button_frame, text="Επαναφορά", width=120, command=self.reset_timer)
        reset_button.pack(side="left", padx=5)

    def update_speed(self, value=None):
        speed_str = self.speed_var.get()
        self.speed = int(speed_str[1:])

    def toggle_timer(self):
        try:
            hours = int(self.hours_input.get())
            minutes = int(self.minutes_input.get())
            seconds = int(self.seconds_input.get())
            if hours < 0 or minutes < 0 or seconds < 0:
                raise ValueError
            self.elapsed_seconds = hours * 3600 + minutes * 60 + seconds
            if self.elapsed_seconds <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Μη έγκυρη Εισαγωγή", "Παρακαλώ εισάγετε έγκυρους θετικούς ακέραιους αριθμούς για ώρες, λεπτά και δευτερόλεπτα.")
            return

        self.is_running = not self.is_running
        if self.is_running:
            self.start_button.configure(text="Παύση")
            self.update_timer()
        else:
            self.start_button.configure(text="Συνέχεια")

    def update_timer(self):
        if not self.is_running:
            return
        if self.elapsed_seconds <= 0:
            self.is_running = False
            self.start_button.configure(text="Έναρξη")
            messagebox.showinfo("Ειδοποίηση", "Ο χρονομετρητής έληξε!")
            return
        self.elapsed_seconds -= self.speed
        hours, remainder = divmod(self.elapsed_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.time_display.configure(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        self.parent.after(1000 // self.speed, self.update_timer)

    def reset_timer(self):
        self.is_running = False
        self.elapsed_seconds = 0
        self.start_button.configure(text="Έναρξη")
        self.time_display.configure(text="00:00:00")
        self.hours_input.delete(0, "end")
        self.hours_input.insert(0, "00")
        self.minutes_input.delete(0, "end")
        self.minutes_input.insert(0, "00")
        self.seconds_input.delete(0, "end")
        self.seconds_input.insert(0, "00")

class PomodoroTimer:
    def __init__(self, parent):
        self.parent = parent
        self.is_running = False
        self.work_seconds = 25 * 60
        self.break_seconds = 5 * 60
        self.seconds_left = self.work_seconds
        self.pomodoro_count = 0
        self.is_break = False
        self.total_sessions = 0
        self.completed_sessions = 0
        self.speed = 1
        self.setup_ui()

    def setup_ui(self):
        self.frame = ctk.CTkFrame(self.parent)
        self.frame.pack(fill="both", expand=True, padx=5, pady=5)

        title_frame = ctk.CTkFrame(self.frame)
        title_frame.pack(pady=(10, 5), fill="x")
        ctk.CTkLabel(title_frame, text="🍅", font=("Arial", 16)).pack(side="left", padx=(0, 5))
        ctk.CTkLabel(title_frame, text="Pomodoro", font=("Arial", 16, "bold")).pack(side="left")

        timer_display_frame = ctk.CTkFrame(self.frame)
        timer_display_frame.pack(pady=15, padx=20, ipadx=15, ipady=10)
        self.mode_label = ctk.CTkLabel(timer_display_frame, text="Ώρα Εργασίας", font=("Arial", 14))
        self.mode_label.pack()
        self.time_display = ctk.CTkLabel(timer_display_frame, text="25:00", font=("Arial", 36, "bold"))
        self.time_display.pack(pady=5)
        self.count_label = ctk.CTkLabel(timer_display_frame, text="Ολοκληρώθηκαν: 0", font=("Arial", 11))
        self.count_label.pack()

        session_input_frame = ctk.CTkFrame(timer_display_frame)
        session_input_frame.pack(pady=5)
        ctk.CTkLabel(session_input_frame, text="Συνεδρίες:", font=("Arial", 12)).pack(side="left")
        self.session_input = ctk.CTkEntry(session_input_frame, font=("Arial", 12), width=50)
        self.session_input.pack(side="left", padx=5)
        self.session_input.insert(0, "1")

        speed_frame = ctk.CTkFrame(self.frame)
        speed_frame.pack(pady=10)
        ctk.CTkLabel(speed_frame, text="Επιτάχυνση:", font=("Arial", 12)).pack(side="left", padx=5)
        self.speed_var = ctk.StringVar(value="x1")
        self.speed_menu = ctk.CTkComboBox(speed_frame, variable=self.speed_var, values=["x1", "x2", "x4", "x8", "x16"], width=80, command=self.update_speed)
        self.speed_menu.pack(side="left", padx=5)

        button_frame = ctk.CTkFrame(self.frame)
        button_frame.pack(pady=10)
        self.start_button = ctk.CTkButton(button_frame, text="Έναρξη", width=120, command=self.toggle_timer)
        self.start_button.pack(side="left", padx=5)
        reset_button = ctk.CTkButton(button_frame, text="Επαναφορά", width=120, command=self.reset_timer)
        reset_button.pack(side="left", padx=5)

    def update_speed(self, value=None):
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
            self.start_button.configure(text="Παύση")
            self.update_timer()
        else:
            self.start_button.configure(text="Συνέχεια")

    def update_timer(self):
        if not self.is_running:
            return
        if self.seconds_left <= 0:
            self.is_running = False
            if self.is_break:
                self.mode_label.configure(text="Ώρα Εργασίας")
                self.seconds_left = self.work_seconds
                messagebox.showinfo("Ειδοποίηση", "Το διάλειμμα τελείωσε! Ώρα για εργασία.")
            else:
                self.mode_label.configure(text="Διάλειμμα")
                self.seconds_left = self.break_seconds
                messagebox.showinfo("Ειδοποίηση", "Η εργασία τελείωσε! Ώρα για διάλειμμα.")
            self.start_button.configure(text="Έναρξη")
            return
        self.seconds_left -= self.speed
        minutes, seconds = divmod(self.seconds_left, 60)
        self.time_display.configure(text=f"{minutes:02d}:{seconds:02d}")
        self.parent.after(1000 // self.speed, self.update_timer)

    def reset_timer(self):
        self.is_running = False
        self.start_button.configure(text="Έναρξη")
        self.is_break = False
        self.seconds_left = self.work_seconds
        self.mode_label.configure(text="Ώρα Εργασίας")
        self.time_display.configure(text="25:00")
        self.pomodoro_count = 0
        self.completed_sessions = 0
        self.count_label.configure(text="Ολοκληρώθηκαν: 0")
        self.session_input.delete(0, "end")
        self.session_input.insert(0, "1")

class TaskScreen:
    def __init__(self, parent):
        self.parent = parent
        self.tasks = []
        self.streak_days = 7

        self.main_frame = ctk.CTkFrame(parent)
        self.main_frame.pack(fill="both", expand=True)

        self.subjects_frame = ctk.CTkFrame(self.main_frame)
        self.subjects_frame.pack(fill="x", padx=20, pady=10)
        self.setup_subject_widget()

        self.streak_frame = ctk.CTkFrame(self.main_frame)
        self.streak_frame.pack(fill="x", padx=20, pady=10)
        self.setup_streak_widget()

        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(fill="x", padx=20, pady=10)
        self.timers_button = ctk.CTkButton(self.button_frame, text="Χρονομετρητές", command=self.show_timers)
        self.timers_button.pack(side="left", padx=10, pady=5)
        self.tasks_button = ctk.CTkButton(self.button_frame, text="Εργασίες", command=self.show_tasks)
        self.tasks_button.pack(side="left", padx=10, pady=5)

        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)

    def setup_subject_widget(self):
        subject_container = ctk.CTkFrame(self.subjects_frame)
        subject_container.pack(fill="x", padx=10, pady=10)
        show_courses_tab(ctk.CTkFrame(subject_container))

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

    def show_timers(self):
        self.clear_content_frame()
        self.timer_frame = ctk.CTkFrame(self.content_frame)
        self.timer_frame.pack(fill="x", padx=20, pady=10)
        # timer_header = ctk.CTkLabel(self.timer_frame, text="Χρονόμετρα", font=("Arial", 14, "bold"))
        # timer_header.pack(fill="x", pady=5)
        self.timer_container = ctk.CTkFrame(self.timer_frame)
        self.timer_container.pack(fill="x", padx=10, pady=10)
        self.pomodoro_container = ctk.CTkFrame(self.timer_container)
        self.pomodoro_container.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.pomodoro = PomodoroTimer(self.pomodoro_container)
        self.stopwatch_container = ctk.CTkFrame(self.timer_container)
        self.stopwatch_container.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.stopwatch = StopwatchTimer(self.stopwatch_container)

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

selected_courses = []

def show_courses_tab(content_frame):
    for widget in content_frame.winfo_children():
        widget.destroy()
    semester_list_frame = content_frame
    semester_list_frame.pack(fill="x", pady=10)
    data = {}
    for subject in chosen_subjects:
        semester = subject.semester
        course_name = subject.course_name
        if not semester or not course_name:
            continue
        if semester in data:
            data[semester].append(course_name)
        else:
            data[semester] = [course_name]
    for sem, courses in data.items():
        sem_header = ctk.CTkFrame(semester_list_frame)
        sem_header.pack(fill="x", padx=10, pady=5)
        toggle_button = ctk.CTkButton(
            sem_header, text=f"+ Semester {sem}",
            command=None
        )
        toggle_button.pack(fill="x")
        course_frame = ctk.CTkFrame(sem_header)
        for course in courses:
            var = ctk.BooleanVar()
            cb = ctk.CTkCheckBox(course_frame, text=course, variable=var)
            cb.pack(anchor="w", padx=20)
            selected_courses.append((course, var))
        toggle_button.configure(command=lambda s=sem, f=course_frame, b=toggle_button: toggle_courses(s, f, b))
    save_button = ctk.CTkButton(content_frame, text="Αποθήκευση", command=save_courses, width=20)
    save_button.pack(pady=20)

def toggle_courses(sem, course_frame, toggle_button):
    if course_frame.winfo_ismapped():
        course_frame.pack_forget()
        toggle_button.configure(text=f"+ Semester {sem}")
    else:
        course_frame.pack(fill="x", padx=30)
        toggle_button.configure(text=f"- Semester {sem}")

study_subjects = []

def save_courses():
    chosen = [course for course, var in selected_courses if var.get()]
    for chosen_course in chosen:
        for subject in chosen_subjects:
            if subject.course_name == chosen_course:
                study_subjects.append(subject)
    messagebox.showinfo("Αποθήκευση", f"Αποθηκεύτηκαν {len(chosen)} μαθήματα.\n\n{', '.join(chosen)}")
    return chosen
