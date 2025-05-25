import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from pomodoro import PomodoroTimer
from stopwatch import StopwatchTimer
from courses import CourseManager

class ZoneInScreen:
    def __init__(self, parent):
        self.parent = parent
        self.checked_in = False
        self.chosen_subjects = CourseManager.load_chosen_subjects()

        self.main_frame = ctk.CTkFrame(parent)
        self.main_frame.pack(fill="both", expand=True)

        # Header
        header = ctk.CTkLabel(self.main_frame, text="Zone In", font=("Arial", 20, "bold"))
        header.pack(pady=20)

        # Subject selection menu under header
        self.subjects_frame = ctk.CTkFrame(self.main_frame)
        self.subjects_frame.pack(fill="x", padx=20, pady=10)
        self.selected_subject_vars = []
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
            self.selected_subject_vars.append((subj, var))

    def check_in(self):
        selected_subjects = [subject for subject, var in self.selected_subject_vars if var.get()]
        if not selected_subjects:
            CTkMessagebox(title="Δεν έχεις επιλέξει μάθημα", message="Πρέπει να επιλέξεις τουλάχιστον ένα μάθημα πριν κάνεις check-in.", icon="warning")
            return

        if not self.checked_in:
            self.checked_in = True
            self.checkin_btn.configure(state="disabled")
            self.checkout_btn.configure(state="normal")
            # Read timer preference
            timer_pref = "stopwatch"
            try:
                with open("user_timer_pref.txt", "r") as f:
                    timer_pref = f.read().strip()
            except FileNotFoundError:
                pass  # Default to stopwatch if not set

            if timer_pref == "pomodoro":
                # Reset Pomodoro timer and start it
                self.pomodoro.reset_timer()
                self.pomodoro.session_input.delete(0, "end")
                self.pomodoro.session_input.insert(0, "1")
                if not self.pomodoro.is_running:
                    self.pomodoro.toggle_timer()
                CTkMessagebox(title="Check-In", message="Έκανες check-in! Ξεκίνησε το Pomodoro!", icon="check")
            elif timer_pref == "stopwatch":
                # Set StopwatchTimer to 30 minutes and start it
                self.stopwatch.hours_input.delete(0, "end")
                self.stopwatch.hours_input.insert(0, "00")
                self.stopwatch.minutes_input.delete(0, "end")
                self.stopwatch.minutes_input.insert(0, "30")
                self.stopwatch.seconds_input.delete(0, "end")
                self.stopwatch.seconds_input.insert(0, "00")
                if not self.stopwatch.is_running:
                    self.stopwatch.toggle_timer()
                CTkMessagebox(title="Check-In", message="Έκανες check-in! Καλή μελέτη!", icon="check")
            else:
                CTkMessagebox(title="Check-In", message="Έχεις ήδη κάνει check-in.", icon="info")
        else:
            CTkMessagebox(title="Check-In", message="Έχεις ήδη κάνει check-in.", icon="info")

    def check_out(self):
        if self.checked_in:
            if self.stopwatch.is_running and self.stopwatch.elapsed_seconds > 0:
                self.stopwatch.reset_timer()
                self.checked_in = False
                self.checkin_btn.configure(state="normal")
                self.checkout_btn.configure(state="disabled")
                CTkMessagebox(title="Προειδοποίηση", message="Θα χάσεις το streak σου!", icon="warning")
            elif self.stopwatch.elapsed_seconds == 0:
                self.checked_in = False
                self.checkin_btn.configure(state="normal")
                self.checkout_btn.configure(state="disabled")
                CTkMessagebox(title="Συγχαρητήρια!", message="Συγχαρητήρια! Πήρες το streak σου!", icon="check")
            elif self.pomodoro.is_running and self.pomodoro.elapsed_seconds > 0:
                self.pomodoro.reset_timer()
                self.checked_in = False
                self.checkin_btn.configure(state="normal")
                self.checkout_btn.configure(state="disabled")
                CTkMessagebox(title="Προειδοποίηση", message="Θα χάσεις το streak σου!", icon="warning")
            elif self.pomodoro.elapsed_seconds == 0:
                self.checked_in = False
                self.checkin_btn.configure(state="normal")
                self.checkout_btn.configure(state="disabled")
                CTkMessagebox(title="Συγχαρητήρια!", message="Συγχαρητήρια! Πήρες το streak σου!", icon="check")
            else:
                # fallback for any other case
                self.checked_in = False
                self.checkin_btn.configure(state="normal")
                self.checkout_btn.configure(state="disabled")
                CTkMessagebox(title="Check-Out", message="Έκανες check-out!", icon="info")
        else:
            CTkMessagebox(title="Check-Out", message="Πρέπει να κάνεις πρώτα check-in.", icon="info")

# Utility function to open the ZoneInScreen
def open_zonein_screen(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()
    ZoneInScreen(parent_frame)
