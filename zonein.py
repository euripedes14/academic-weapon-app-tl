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

    # def check_in(self):
    #     if not self.checked_in:
    #         self.checked_in = True
    #         self.checkin_btn.configure(state="disabled")
    #         self.checkout_btn.configure(state="normal")
    #         messagebox.showinfo("Check-In", "Έκανες check-in! Καλή μελέτη!")
    #     else:
    #         messagebox.showinfo("Check-In", "Έχεις ήδη κάνει check-in.")

    #corelogic to be implemented
    
    def check_in(self):
        if not self.checked_in:
            self.checked_in = True
            self.checkin_btn.configure(state="disabled")
            self.checkout_btn.configure(state="normal")
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
            self.checked_in = False
            self.checkin_btn.configure(state="normal")
            self.checkout_btn.configure(state="disabled")
            messagebox.showinfo("Check-Out", "Έκανες check-out! Μπράβο για τη μελέτη σου!")
        else:
            messagebox.showinfo("Check-Out", "Πρέπει να κάνεις πρώτα check-in.")

# Utility function to open the ZoneInScreen
def open_zonein_screen(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()
    ZoneInScreen(parent_frame)

    if __name__ == "__main__":
        root = ctk.CTk()
        root.geometry("900x600")
        open_zonein_screen(root)
        root.mainloop()