import customtkinter as ctk
from tkinter import simpledialog, messagebox
from courses import CourseManager
import customtkinter as ctk
from tkinter import simpledialog, messagebox
from stopwatch import StopwatchTimer
import json



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
        ########
        self.session_completed = False
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

        button_frame = ctk.CTkFrame(self.frame)
        button_frame.pack(pady=10)
        self.pause_button = ctk.CTkButton(button_frame, text="Παύση", width=120, command=self.pause_timer)
        self.pause_button.pack(side="left", padx=5)
        reset_button = ctk.CTkButton(button_frame, text="Επαναφορά", width=120, command=self.reset_timer)
        reset_button.pack(side="left", padx=5)

    def start_timer(self, sessions=1, work_minutes=25, break_minutes=5):
        self.total_sessions = sessions
        self.work_seconds = work_minutes * 60
        self.break_seconds = break_minutes * 60
        self.seconds_left = self.work_seconds
        self.is_break = False
        self.completed_sessions = 0
        self.is_running = True
        self.update_count_label()
        self.update_timer()
        self.mode_label.configure(text="Ώρα Εργασίας")
        self.time_display.configure(text=f"{work_minutes:02d}:00")

    def update_count_label(self):
        self.count_label.configure(text=f"Ολοκληρώθηκαν: {self.completed_sessions}/{self.total_sessions}")

    def pause_timer(self):
        self.is_running = False
        self.pause_button.configure(text="Συνέχεια", command=self.resume_timer)

    def resume_timer(self):
        self.is_running = True
        self.pause_button.configure(text="Παύση", command=self.pause_timer)
        self.update_timer()

    def update_timer(self):
        if not self.is_running:
            return
        if self.seconds_left <= 0:
            if self.is_break:
                self.completed_sessions += 1
                self.update_count_label()
                if self.completed_sessions >= self.total_sessions:
                    self.is_running = False
                    self.mode_label.configure(text="Τέλος Συνεδριών!")
                    self.time_display.configure(text="00:00")
                    return
                self.mode_label.configure(text="Ώρα Εργασίας")
                self.seconds_left = self.work_seconds
            else:
                self.mode_label.configure(text="Διάλειμμα")
                self.seconds_left = self.break_seconds
            self.is_break = not self.is_break
        minutes, seconds = divmod(self.seconds_left, 60)
        self.time_display.configure(text=f"{minutes:02d}:{seconds:02d}")
        self.seconds_left -= 1
        self.parent.after(1000, self.update_timer)

    def reset_timer(self):
        self.is_running = False
        self.is_break = False
        self.seconds_left = self.work_seconds
        self.mode_label.configure(text="Ώρα Εργασίας")
        self.time_display.configure(text=f"{self.work_seconds//60:02d}:00")
        self.completed_sessions = 0
        self.update_count_label()
        self.pause_button.configure(text="Παύση", command=self.pause_timer)
    #########
