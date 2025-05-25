import customtkinter as ctk
from tkinter import simpledialog, messagebox
from courses import CourseManager
import customtkinter as ctk

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
