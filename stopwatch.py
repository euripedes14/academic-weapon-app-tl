# Κλάση: StopwatchTimer
# Ρόλος: Υλοποιεί ένα απλό χρονόμετρο αντίστροφης μέτρησης (countdown timer).
# Χρησιμοποιείται από:
# ZoneInScreen (στο zonein.py)
# Μπορεί να χρησιμοποιηθεί και αυτόνομα.
# Μέθοδοι:
# __init__(self, parent)
# Αρχικοποιεί το χρονόμετρο, δημιουργεί το UI (inputs για ώρες/λεπτά/δευτερόλεπτα, κουμπιά).
# start_timer(self, hours=0, minutes=0, seconds=0)
# Ξεκινά το χρονόμετρο με συγκεκριμένη διάρκεια.
# pause_timer(self)
# Παύει το χρονόμετρο.
# resume_timer(self)
# Συνεχίζει το χρονόμετρο μετά από παύση.
# update_timer(self)
# Ενημερώνει το χρόνο κάθε δευτερόλεπτο, σταματά όταν φτάσει στο 0.
# reset_timer(self)
# Επαναφέρει το χρονόμετρο στην αρχική του κατάσταση.


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
        self._after_id = None

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

        button_frame = ctk.CTkFrame(self.frame)
        button_frame.pack(pady=10)
        self.pause_button = ctk.CTkButton(button_frame, text="Παύση", width=120, command=self.pause_timer)
        self.pause_button.pack(side="left", padx=5)
        reset_button = ctk.CTkButton(button_frame, text="Επαναφορά", width=120, command=self.reset_timer)
        reset_button.pack(side="left", padx=5)

    def start_timer(self, hours=0, minutes=0, seconds=0):
        self.elapsed_seconds = hours * 3600 + minutes * 60 + seconds
        self.initial_seconds = self.elapsed_seconds  # Αποθήκευση αρχικής τιμής
        if self.elapsed_seconds <= 0:
            self.time_display.configure(text="00:00:00")
            return
        self.is_running = True
        self.update_timer()

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
        if self.elapsed_seconds <= 0:
            self.is_running = False
            self.time_display.configure(text="00:00:00")
            if getattr(self, '_has_started', False):
                messagebox.showinfo("Ειδοποίηση", "Ο χρονομετρητής έληξε!")
            return
        self._has_started = True
        hours, remainder = divmod(self.elapsed_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.time_display.configure(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        self.elapsed_seconds -= 1
        self._after_id = self.parent.after(1000, self.update_timer)

    def reset_timer(self):
        # Ακύρωση προηγούμενου timer αν υπάρχει
        if hasattr(self, '_after_id') and self._after_id is not None:
            try:
                self.parent.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None
        # Επαναφορά στην αρχική διάρκεια (αν υπάρχει), αλλιώς μηδενισμός
        if hasattr(self, 'initial_seconds') and self.initial_seconds > 0:
            self.elapsed_seconds = self.initial_seconds
            hours = self.initial_seconds // 3600
            minutes = (self.initial_seconds % 3600) // 60
            seconds = self.initial_seconds % 60
            self.time_display.configure(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            self.hours_input.delete(0, "end")
            self.hours_input.insert(0, f"{hours:02d}")
            self.minutes_input.delete(0, "end")
            self.minutes_input.insert(0, f"{minutes:02d}")
            self.seconds_input.delete(0, "end")
            self.seconds_input.insert(0, f"{seconds:02d}")
        else:
            self.elapsed_seconds = 0
            self.time_display.configure(text="00:00:00")
            self.hours_input.delete(0, "end")
            self.hours_input.insert(0, "00")
            self.minutes_input.delete(0, "end")
            self.minutes_input.insert(0, "00")
            self.seconds_input.delete(0, "end")
            self.seconds_input.insert(0, "00")
        self._has_started = False
        self.is_running = True
        self.pause_button.configure(text="Παύση", command=self.pause_timer)
        self.update_timer()
