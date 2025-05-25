import customtkinter as ctk
from tkinter import simpledialog, messagebox
from courses import CourseManager
import customtkinter as ctk
from tkinter import simpledialog, messagebox
from stopwatch import StopwatchTimer


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
