import tkinter as tk
from tkinter import simpledialog, messagebox
from tkcalendar import DateEntry

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
            {"text": "Ολοκλήρωση εργασίας Μαθηματικών", "deadline": None},
            {"text": "Διάβασμα κεφαλαίου 3 για τη Φυσική", "deadline": None},
            {"text": "Προετοιμασία παρουσίασης για την Πληροφορική", "deadline": None},
            {"text": "Email στον καθηγητή για το ερευνητικό project", "deadline": None}
        ]

        for task in example_tasks:
            self.add_task_to_list(task["text"], task["deadline"])

    def add_task(self):
        task_info = self.task_dialog()
        if task_info:
            self.add_task_to_list(task_info['text'], task_info['deadline'])

    def task_dialog(self, task_text='', deadline=None):
        dialog = tk.Toplevel(self.parent)
        dialog.title("Εισάγετε Εργασία")
        dialog.geometry("400x300")
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        dialog.resizable(False, False)

        tk.Label(dialog, text="Εργασία:").pack(pady=5)
        task_entry = tk.Entry(dialog)
        task_entry.pack(pady=5, padx=10, fill=tk.X)
        task_entry.insert(0, task_text)

        tk.Label(dialog, text="Θέλετε να προσθέσετε προθεσμία;").pack(pady=5)
        answer_frame = tk.Frame(dialog)
        answer_frame.pack(pady=5)

        deadline_var = tk.StringVar(value="no")

        yes_rb = tk.Radiobutton(answer_frame, text="Ναι", variable=deadline_var, value="yes")
        yes_rb.pack(side=tk.LEFT, padx=5)
        no_rb = tk.Radiobutton(answer_frame, text="Όχι", variable=deadline_var, value="no")
        no_rb.pack(side=tk.LEFT, padx=5)

        deadline_entry = DateEntry(dialog, width=12, background='darkblue', foreground='white', borderwidth=2)

        def show_deadline_entry():
            if deadline_var.get() == "yes":
                deadline_entry.pack(pady=5)
            else:
                deadline_entry.pack_forget()

        deadline_var.trace("w", lambda *args: show_deadline_entry())

        if deadline:
            tk.Label(dialog,
                     text="Η εργασία έχει ήδη προθεσμία. Θέλετε να την αφαιρέσετε ή να την επεξεργαστείτε;").pack(
                pady=5)
            edit_frame = tk.Frame(dialog)
            edit_frame.pack(pady=5)

            edit_var = tk.StringVar(value="keep")
            edit_rb = tk.Radiobutton(edit_frame, text="Επεξεργασία", variable=edit_var, value="edit")
            edit_rb.pack(side=tk.LEFT, padx=5)
            remove_rb = tk.Radiobutton(edit_frame, text="Αφαίρεση", variable=edit_var, value="remove")
            remove_rb.pack(side=tk.LEFT, padx=5)
            keep_rb = tk.Radiobutton(edit_frame, text="Διατήρηση", variable=edit_var, value="keep")
            keep_rb.pack(side=tk.LEFT, padx=5)

            def handle_existing_deadline():
                if edit_var.get() == "edit":
                    deadline_entry.pack(pady=5)
                elif edit_var.get() == "remove":
                    deadline_entry.pack_forget()
                else:
                    deadline_entry.pack_forget()

            edit_var.trace("w", lambda *args: handle_existing_deadline())

        def on_ok():
            dialog.task_info = {
                'text': task_entry.get(),
                'deadline': deadline_entry.get_date() if deadline_var.get() == "yes" or (
                            deadline and edit_var.get() == "edit") else None
            }
            dialog.destroy()

        tk.Button(dialog, text="OK", command=on_ok).pack(pady=10)
        self.parent.wait_window(dialog)
        return getattr(dialog, 'task_info', None)

    def add_task_to_list(self, task_text, deadline):
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

        deadline_label = tk.Label(task_frame, text=str(deadline) if deadline else "",
                                  bg="#ffffff", anchor="e")
        deadline_label.pack(side=tk.RIGHT, padx=5)

        edit_btn = tk.Button(task_frame, text="Επεξεργασία",
                             command=lambda t=task_text, l=task_label, d=deadline, dl=deadline_label: self.edit_task(t,
                                                                                                                     l,
                                                                                                                     d,
                                                                                                                     dl))
        edit_btn.pack(side=tk.RIGHT, padx=5)

        delete_btn = tk.Button(task_frame, text="Διαγραφή",
                               command=lambda t=task_text, f=task_frame: self.delete_task(t, f))
        delete_btn.pack(side=tk.RIGHT, padx=5)

        self.tasks.append({"text": task_text, "var": var, "label": task_label, "deadline": deadline,
                           "deadline_label": deadline_label})

    def edit_task(self, task_text, task_label, old_deadline, deadline_label):
        task_info = self.task_dialog(task_text, old_deadline)
        if task_info:
            task_label.config(text=task_info['text'])
            deadline_label.config(text=str(task_info['deadline']) if task_info['deadline'] else "")
            for task in self.tasks:
                if task["text"] == task_text:
                    task["text"] = task_info['text']
                    task["deadline"] = task_info['deadline']
                    break

    def delete_task(self, task_text, task_frame):
        if messagebox.askokcancel("Διαγραφή Εργασίας", "Είστε σίγουροι ότι θέλετε να διαγράψετε αυτή την εργασία;"):
            task_frame.destroy()
            self.tasks = [task for task in self.tasks if task["text"] != task_text]

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
        self.total_seconds = 0
        self.seconds_left = 0
        self.pomodoro_count = 0
        self.is_break = False

        self.setup_ui()

    def setup_ui(self):
        # Create main frame
        self.frame = tk.Frame(self.parent, bg="#f2f2f2")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = tk.Label(self.frame, text="Χρονόμετρο", font=("Arial", 18, "bold"), bg="#f2f2f2")
        title_label.pack(pady=20)

        # Timer display frame
        timer_frame = tk.Frame(self.frame, bg="#f2f2f2")
        timer_frame.pack(pady=20)

        # Mode label (Work/Break)
        self.mode_label = tk.Label(timer_frame, text="", font=("Arial", 14), bg="#f2f2f2", fg="#d64545")
        self.mode_label.pack()

        # Timer display
        self.time_display = tk.Label(timer_frame, text="00:00:00", font=("Arial", 48), bg="#f2f2f2")
        self.time_display.pack(pady=10)

        # Pomodoro count
        self.count_label = tk.Label(timer_frame, text="", font=("Arial", 12), bg="#f2f2f2")
        self.count_label.pack()

        # Control buttons frame
        button_frame = tk.Frame(self.frame, bg="#f2f2f2")
        button_frame.pack(pady=20)

        # Start button
        self.start_button = tk.Button(button_frame, text="Ρύθμιση", font=("Arial", 12),
                                      width=10, command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=5)

        # Reset button
        reset_button = tk.Button(button_frame, text="Επαναφορά", font=("Arial", 12),
                                 width=10, command=self.reset_timer)
        reset_button.pack(side=tk.LEFT, padx=5)

    def start_timer(self):
        self.get_timer_settings()
        if self.total_seconds > 0:
            self.is_running = True
            self.update_timer()

    def get_timer_settings(self):
        dialog = tk.Toplevel(self.parent)
        dialog.title("Ρυθμίσεις Χρονομέτρου")
        dialog.geometry("300x200")
        dialog.resizable(False, False)

        tk.Label(dialog, text="Δώστε χρόνο σε ώρες:").pack(pady=5)
        hours_entry = tk.Entry(dialog)
        hours_entry.pack(pady=5, padx=10, fill=tk.X)

        tk.Label(dialog, text="Επιλέξτε λειτουργία:").pack(pady=5)
        mode_var = tk.StringVar(value="normal")

        normal_rb = tk.Radiobutton(dialog, text="Κανονική αντίστροφη μέτρηση", variable=mode_var, value="normal")
        normal_rb.pack(pady=5)
        pomodoro_rb = tk.Radiobutton(dialog, text="Pomodoro", variable=mode_var, value="pomodoro")
        pomodoro_rb.pack(pady=5)

        def on_ok():
            try:
                hours = float(hours_entry.get())
                if hours <= 0:
                    raise ValueError("Ο χρόνος πρέπει να είναι θετικός αριθμός.")
                self.total_seconds = int(hours * 3600)
                self.seconds_left = self.total_seconds
                self.mode = mode_var.get()
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Σφάλμα", str(e))

        tk.Button(dialog, text="OK", command=on_ok).pack(pady=10)
        self.parent.wait_window(dialog)

    def update_timer(self):
        if not self.is_running:
            return

        if self.seconds_left <= 0:
            if self.mode == "pomodoro":
                if self.is_break:
                    self.is_break = False
                    self.seconds_left = min(25 * 60, self.total_seconds - self.pomodoro_count * 30 * 60)
                    self.mode_label.config(text="Ώρα Εργασίας", fg="#d64545")
                else:
                    self.is_break = True
                    self.pomodoro_count += 1
                    self.count_label.config(text=f"Ολοκληρώθηκαν: {self.pomodoro_count}")
                    self.seconds_left = 5 * 60
                    self.mode_label.config(text="Ώρα Διαλείμματος", fg="#45d645")
            else:
                messagebox.showinfo("Χρονόμετρο", "Ο χρόνος τελείωσε!")
                self.reset_timer()
                return

        minutes, seconds = divmod(self.seconds_left, 60)
        hours, minutes = divmod(minutes, 60)
        self.time_display.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        self.seconds_left -= 1
        self.parent.after(1000, self.update_timer)

    def reset_timer(self):
        self.is_running = False
        self.start_button.config(text="Ρύθμιση")
        self.seconds_left = self.total_seconds
        self.mode_label.config(text="")
        self.time_display.config(text="00:00:00")
        self.count_label.config(text="")
        self.pomodoro_count = 0
        self.is_break = False


def open_task_screen(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()

    task_screen = TaskScreen(parent_frame)