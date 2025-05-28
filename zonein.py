import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from pomodoro import PomodoroTimer
from stopwatch import StopwatchTimer
from courses import CourseManager
import json


class ZoneInScreen:
    def __init__(self, parent, username):
        self.parent = parent
        self.username = username
        self.checked_in = False
        self.manager = CourseManager(username=username)
        self.chosen_subjects = self.manager.load_chosen_subjects()

        self.main_frame = ctk.CTkFrame(parent)
        self.main_frame.pack(fill="both", expand=True)

        # Header
        header = ctk.CTkLabel(self.main_frame, text="Zone In", font=("Arial", 20, "bold"))
        header.pack(pady=20)

        # Subject selection menu under header
        self.subjects_frame = ctk.CTkFrame(self.main_frame)
        self.subjects_frame.pack(fill="x", padx=20, pady=10)
        self.selected_subjects = []
        self.show_subjects_menu()

        # Check-in/out buttons
        btn_frame = ctk.CTkFrame(self.main_frame)
        btn_frame.pack(pady=10)
        self.checkin_btn = ctk.CTkButton(btn_frame, text="Check-In", command=self.check_in, width=120)
        self.checkin_btn.pack(side="left", padx=10)
        self.checkout_btn = ctk.CTkButton(btn_frame, text="Check-Out", command=self.check_out, width=120, state="disabled")
        self.checkout_btn.pack(side="left", padx=10)

        # Timers section
        timers_frame = ctk.CTkFrame(self.main_frame)
        timers_frame.pack(fill="x", padx=20, pady=20)

        timers_header = ctk.CTkLabel(timers_frame, text="Χρονόμετρα", font=("Arial", 14, "bold"))
        timers_header.pack(fill="x", pady=5)

        timers_container = ctk.CTkFrame(timers_frame)
        timers_container.pack(fill="x", padx=10, pady=10)

        # Pomodoro Timer
        self.pomodoro_container = ctk.CTkFrame(timers_container)
        self.pomodoro_container.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.pomodoro = PomodoroTimer(self.pomodoro_container)

        # Stopwatch Timer
        self.stopwatch_container = ctk.CTkFrame(timers_container)
        self.stopwatch_container.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.stopwatch = StopwatchTimer(self.stopwatch_container)

    def show_subjects_menu(self):
        ctk.CTkLabel(self.subjects_frame, text="Επιλογή Μαθημάτων για Check-In", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)
        for subj in self.chosen_subjects:
            var = ctk.BooleanVar()
            cb = ctk.CTkCheckBox(self.subjects_frame, text=subj, variable=var)
            cb.pack(anchor="w", padx=20)
            self.selected_subjects.append((subj, var))

    def check_in(self):
        selected_subjects = [subject for subject, var in self.selected_subjects if var.get()]
        if not selected_subjects:
            CTkMessagebox(title="Δεν έχεις επιλέξει μάθημα", message="Πρέπει να επιλέξεις τουλάχιστον ένα μάθημα πριν κάνεις check-in.", icon="warning")
            return

        if not self.checked_in:
            self.checked_in = True
            self.checkin_btn.configure(state="disabled")
            self.checkout_btn.configure(state="normal")
            # Διαβάζω τις ρυθμίσεις timer του χρήστη
            try:
                with open("user_preferences.json", "r", encoding="utf-8") as f:
                    prefs = json.load(f)
                    user_prefs = prefs.get(self.username, prefs.get("default", {}))
                    timer_type = user_prefs.get("timer_type", "stopwatch")
                    timer_minutes = user_prefs.get("timer_minutes", 25)
                    pomodoro_sessions = user_prefs.get("pomodoro_sessions", 4)
            except Exception:
                timer_type = "stopwatch"
                timer_minutes = 25
                pomodoro_sessions = 4

            if timer_type == "pomodoro":
                self.pomodoro.reset_timer()
                self.pomodoro.start_timer(sessions=pomodoro_sessions, work_minutes=timer_minutes)
                CTkMessagebox(title="Check-In", message="Έκανες check-in! Ξεκίνησε το Pomodoro!", icon="check")
            elif timer_type == "stopwatch":
                self.stopwatch.reset_timer()
                self.stopwatch.start_timer(hours=0, minutes=timer_minutes, seconds=0)
                CTkMessagebox(title="Check-In", message="Έκανες check-in! Καλή μελέτη!", icon="check")
            else:
                CTkMessagebox(title="Check-In", message="Έχεις ήδη κάνει check-in.", icon="info")
        else:
            CTkMessagebox(title="Check-In", message="Έχεις ήδη κάνει check-in.", icon="info")

    def check_out(self):
        if not self.checked_in:
            CTkMessagebox(title="Check-Out", message="Πρέπει να κάνεις πρώτα check-in.", icon="info")
            return
        # Διαβάζω τις ρυθμίσεις timer του χρήστη
        try:
            with open("user_preferences.json", "r", encoding="utf-8") as f:
                prefs = json.load(f)
                user_prefs = prefs.get(self.username, prefs.get("default", {}))
                timer_type = user_prefs.get("timer_type", "stopwatch")
                timer_minutes = user_prefs.get("timer_minutes", 25)
                pomodoro_sessions = user_prefs.get("pomodoro_sessions", 4)
        except Exception:
            timer_type = "stopwatch"
            timer_minutes = 25
            pomodoro_sessions = 4

        if timer_type == "pomodoro":
            pomodoro_incomplete = (
                hasattr(self.pomodoro, 'total_sessions') and hasattr(self.pomodoro, 'completed_sessions') and
                self.pomodoro.completed_sessions < self.pomodoro.total_sessions
            )
            if self.pomodoro.is_running or pomodoro_incomplete:
                self.pomodoro.reset_timer()
                self.checked_in = False
                self.checkin_btn.configure(state="normal")
                self.checkout_btn.configure(state="disabled")
                CTkMessagebox(title="Προειδοποίηση", message="Δεν ολοκλήρωσες όλες τις συνεδρίες Pomodoro. Θα χαθούν τα streaks!", icon="warning")
            else:
                self.pomodoro.reset_timer()
                self.checked_in = False
                self.checkin_btn.configure(state="normal")
                self.checkout_btn.configure(state="disabled")
                CTkMessagebox(title="Συγχαρητήρια!", message="Συγχαρητήρια! Πήρες το streak σου!", icon="check")
        elif timer_type == "stopwatch":
            if self.stopwatch.is_running and self.stopwatch.elapsed_seconds > 0:
                self.stopwatch.reset_timer()
                self.checked_in = False
                self.checkin_btn.configure(state="normal")
                self.checkout_btn.configure(state="disabled")
                CTkMessagebox(title="Προειδοποίηση", message="Θα χάσεις το streak σου!", icon="warning")
            elif not self.stopwatch.is_running and self.stopwatch.elapsed_seconds == 0:
                self.stopwatch.reset_timer()
                self.checked_in = False
                self.checkin_btn.configure(state="normal")
                self.checkout_btn.configure(state="disabled")
                CTkMessagebox(title="Συγχαρητήρια!", message="Συγχαρητήρια! Πήρες το streak σου!", icon="check")
            else:
                self.stopwatch.reset_timer()
                self.checked_in = False
                self.checkin_btn.configure(state="normal")
                self.checkout_btn.configure(state="disabled")
                CTkMessagebox(title="Check-Out", message="Έκανες check-out!", icon="info")
        else:
            # fallback για άγνωστο timer
            self.stopwatch.reset_timer()
            self.pomodoro.reset_timer()
            self.checked_in = False
            self.checkin_btn.configure(state="normal")
            self.checkout_btn.configure(state="disabled")
            CTkMessagebox(title="Check-Out", message="Έκανες check-out!", icon="info")

# Utility function to open the ZoneInScreen

def open_zonein_screen(parent_frame, username="default"):
    for widget in parent_frame.winfo_children():
        widget.destroy()
    ZoneInScreen(parent_frame, username=username)
