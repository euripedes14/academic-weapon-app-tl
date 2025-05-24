import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkcalendar import Calendar
import datetime
from error_control import ErrorControl

ctk.set_default_color_theme("themes/breeze.json")

# Custom CTk input dialog
class CTkInputDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, prompt):
        super().__init__(parent)
        self.title(title)
        self.geometry("350x150")
        self.resizable(False, False)
        self.value = None

        ctk.CTkLabel(self, text=prompt, font=("Arial", 12)).pack(pady=(20, 10))
        self.entry = ctk.CTkEntry(self, width=250)
        self.entry.pack(pady=5)
        self.entry.focus()

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="OK", command=self.on_ok).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Cancel", command=self.on_cancel).pack(side="left", padx=10)

        self.bind("<Return>", lambda event: self.on_ok())
        self.bind("<Escape>", lambda event: self.on_cancel())

        self.grab_set()
        self.wait_window()

    def on_ok(self):
        self.value = self.entry.get()
        self.destroy()

    def on_cancel(self):
        self.value = None
        self.destroy()

class ScheduleScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#f2f2f2", corner_radius=10)
        self.pack(fill="both", expand=True)
        self.events = []

        # Use grid for precise sizing
        self.columnconfigure(0, weight=1, uniform="group1")
        self.columnconfigure(1, weight=2, uniform="group1")  # Calendar gets double space
        self.columnconfigure(2, weight=1, uniform="group1")
        self.rowconfigure(0, weight=1)

        # Past events (DONE)
        self.past_events_frame = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=10)
        self.past_events_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=20)
        ctk.CTkLabel(self.past_events_frame, text="Ολοκληρωμένες Εργασίες", font=("Arial", 14, "bold"), text_color="#000000").pack(anchor='n', pady=10)
        self.past_events_list = ctk.CTkScrollableFrame(self.past_events_frame, height=300)
        self.past_events_list.pack(fill="both", expand=True, padx=10, pady=10)

        # Calendar (center, larger)
        self.calendar_frame = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=10)
        self.calendar_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 5), pady=20)
        ctk.CTkLabel(self.calendar_frame, text="Ημερολόγιο", font=("Arial", 14, "bold"), text_color="#000000").pack(anchor='n', pady=10)

        self.cal = Calendar(self.calendar_frame, selectmode='day', year=datetime.datetime.now().year,
                            month=datetime.datetime.now().month, day=datetime.datetime.now().day)
        self.cal.pack(fill="both", expand=True, padx=40, pady=40, ipadx=80, ipady=80)
        self.cal.bind("<<CalendarSelected>>", self.on_date_click)

        # Upcoming events (TO DO)
        self.upcoming_events_frame = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=10)
        self.upcoming_events_frame.grid(row=0, column=2, sticky="nsew", padx=(5, 10), pady=20)
        ctk.CTkLabel(self.upcoming_events_frame, text="Μη ολοκληρωμένες Εργασίες", font=("Arial", 14, "bold"), text_color="#000000").pack(anchor='n', pady=10)
        self.upcoming_events_list = ctk.CTkScrollableFrame(self.upcoming_events_frame, height=300)
        self.upcoming_events_list.pack(fill="both", expand=True, padx=10, pady=10)

        self.update_event_lists()

    def on_date_click(self, event):
        selected_date = self.cal.get_date()
        event_name = CTkInputDialog(self, "Προσθήκη Υποχρέωσης", f"Προσθήκη υποχρέωσης για {selected_date}:").value
        if not event_name:
            return
        event_hour = CTkInputDialog(self, "Προσθήκη Ώρας", "Εισάγετε την ώρα της υποχρέωσης (π.χ. 14:00):").value
        if not event_hour:
            return
        
        if not ErrorControl.is_time_slot_available(selected_date, event_hour):
            CTkMessagebox(title="Σύγκρουση Ώρας", message="Υπάρχει ήδη υποχρέωση για αυτή την ημερομηνία και ώρα.", icon="warning")
            return
        
        self.events.append((selected_date, event_name, event_hour))
        save_event_to_file(selected_date, event_name, event_hour)
        CTkMessagebox(title="Υποχρέωση Προστέθηκε", message=f"Υποχρέωση '{event_name}' προστέθηκε για {selected_date} στις {event_hour}.", icon="check")
        self.update_event_lists()

    def update_event_lists(self):        
        today = datetime.datetime.now().date()
        past_events = [event for event in self.events if datetime.datetime.strptime(event[0], "%m/%d/%y").date() < today]
        upcoming_events = [event for event in self.events if datetime.datetime.strptime(event[0], "%m/%d/%y").date() >= today]

        # Clear old widgets
        for widget in self.past_events_list.winfo_children():
            widget.destroy()
        for widget in self.upcoming_events_list.winfo_children():
            widget.destroy()

        for event in past_events:
            ctk.CTkLabel(self.past_events_list, text=f"{event[0]} | {event[1]} | {event[2]}", anchor="w").pack(fill="x", padx=5, pady=2)
        for event in upcoming_events:
            ctk.CTkLabel(self.upcoming_events_list, text=f"{event[0]} | {event[1]} | {event[2]}", anchor="w").pack(fill="x", padx=5, pady=2)

def save_event_to_file(date, event_name, event_hour):
    with open("events.txt", "a", encoding="utf-8") as f:
        f.write(f"{date}|{event_name}|{event_hour}\n")

def open_schedule(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()
    ScheduleScreen(parent_frame)