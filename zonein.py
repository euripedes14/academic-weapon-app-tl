import customtkinter as ctk
from tkinter import messagebox
from pomodoro import PomodoroTimer
from stopwatch import StopwatchTimer
from courses import chosen_subjects

class ZoneInScreen:
    def __init__(self, parent):
        self.parent = parent
        self.checked_in = False

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

        # Organize subjects by semester
        data = {}
        for subject in chosen_subjects:
            semester = subject.semester
            course_name = subject.course_name
            if not semester or not course_name:
                continue
            if semester in data:
                data[semester].append((course_name, subject))
            else:
                data[semester] = [(course_name, subject)]

        for sem, courses in data.items():
            sem_header = ctk.CTkFrame(self.subjects_frame)
            sem_header.pack(fill="x", padx=10, pady=5)
            toggle_button = ctk.CTkButton(
                sem_header, text=f"+ Semester {sem}",
                command=None
            )
            toggle_button.pack(fill="x")
            course_frame = ctk.CTkFrame(sem_header)
            for course_name, subject in courses:
                var = ctk.BooleanVar()
                cb = ctk.CTkCheckBox(course_frame, text=course_name, variable=var)
                cb.pack(anchor="w", padx=20)
                self.selected_subject_vars.append((subject, var))
            toggle_button.configure(command=lambda f=course_frame, b=toggle_button, s=sem: self.toggle_courses(s, f, b))

    def toggle_courses(self, sem, course_frame, toggle_button):
        if course_frame.winfo_ismapped():
            course_frame.pack_forget()
            toggle_button.configure(text=f"+ Semester {sem}")
        else:
            course_frame.pack(fill="x", padx=30)
            toggle_button.configure(text=f"- Semester {sem}")

    def check_in(self):
        selected_subjects = [subject for subject, var in self.selected_subject_vars if var.get()]
        if not selected_subjects:
            messagebox.showwarning("Δεν έχεις επιλέξει μάθημα", "Πρέπει να επιλέξεις τουλάχιστον ένα μάθημα πριν κάνεις check-in.")
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
            # Optionally set sessions to 1 or user value
            self.pomodoro.session_input.delete(0, "end")
            self.pomodoro.session_input.insert(0, "1")
            if not self.pomodoro.is_running:
                self.pomodoro.toggle_timer()
            messagebox.showinfo("Check-In", "Έκανες check-in! Ξεκίνησε το Pomodoro!")
        
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
            messagebox.showinfo("Check-In", "Έκανες check-in! Καλή μελέτη!")
        else:
            messagebox.showinfo("Check-In", "Έχεις ήδη κάνει check-in.")


    def check_out(self):
        if self.checked_in:
            if self.stopwatch.is_running and self.stopwatch.elapsed_seconds > 0:
                self.stopwatch.reset_timer()
                self.checked_in = False
                self.checkin_btn.configure(state="normal")
                self.checkout_btn.configure(state="disabled")
                messagebox.showwarning("Προειδοποίηση", "Θα χάσεις το streak σου!")
            elif self.stopwatch.elapsed_seconds == 0:
                self.checked_in = False
                self.checkin_btn.configure(state="normal")
                self.checkout_btn.configure(state="disabled")
                messagebox.showinfo("Συγχαρητήρια!", "Συγχαρητήρια! Πήρες το streak σου!")
            elif self.pomodoro.is_running and self.pomodoro.elapsed_seconds > 0:
                self.pomodoro.reset_timer()
                self.checked_in = False
                self.checkin_btn.configure(state="normal")
                self.checkout_btn.configure(state="disabled")
                messagebox.showwarning("Προειδοποίηση", "Θα χάσεις το streak σου!")
            elif self.pomodoro.elapsed_seconds == 0:
                self.checked_in = False
                self.checkin_btn.configure(state="normal")
                self.checkout_btn.configure(state="disabled")
                messagebox.showinfo("Συγχαρητήρια!", "Συγχαρητήρια! Πήρες το streak σου!")
            else:
            # fallback for any other case
                self.checked_in = False
                self.checkin_btn.configure(state="normal")
                self.checkout_btn.configure(state="disabled")
                messagebox.showinfo("Check-Out", "Έκανες check-out!")
        else:
            messagebox.showinfo("Check-Out", "Πρέπει να κάνεις πρώτα check-in.")

# Utility function to open the ZoneInScreen
def open_zonein_screen(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()
    ZoneInScreen(parent_frame)
