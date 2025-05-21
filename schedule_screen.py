import customtkinter as ctk
from tkinter import simpledialog, messagebox, ttk
from tkcalendar import Calendar
import datetime

ctk.set_default_color_theme("themes/breeze.json")


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
        ctk.CTkLabel(self.past_events_frame, text="DONE", font=("Arial", 14, "bold"), text_color="#000000").pack(anchor='n', pady=10)
        self.past_events_tree = ttk.Treeview(self.past_events_frame, columns=("Date", "Event", "Time"), show="headings", height=10)
        self.past_events_tree.heading("Date", text="Date")
        self.past_events_tree.heading("Event", text="Event")
        self.past_events_tree.heading("Time", text="Time")
        self.past_events_tree.pack(fill="both", expand=True, padx=10, pady=10)

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
        ctk.CTkLabel(self.upcoming_events_frame, text="TO DO", font=("Arial", 14, "bold"), text_color="#000000").pack(anchor='n', pady=10)
        self.upcoming_events_tree = ttk.Treeview(self.upcoming_events_frame, columns=("Date", "Event", "Time"), show="headings", height=10)
        self.upcoming_events_tree.heading("Date", text="Date")
        self.upcoming_events_tree.heading("Event", text="Event")
        self.upcoming_events_tree.heading("Time", text="Time")
        self.upcoming_events_tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.update_event_lists()

    def on_date_click(self, event):
        selected_date = self.cal.get_date()
        event_name = simpledialog.askstring("Προσθήκη Υποχρέωσης", f"Προσθήκη υποχρέωσης για {selected_date}:")
        event_hour = simpledialog.askstring("Προσθήκη Ώρας", "Εισάγετε την ώρα της υποχρέωσης (π.χ. 14:00):")
        if event_name and event_hour:
            self.events.append((selected_date, event_name, event_hour))
            save_event_to_file(selected_date, event_name, event_hour)
            messagebox.showinfo("Υποχρέωση Προστέθηκε", f"Υποχρέωση '{event_name}' προστέθηκε για {selected_date} στις {event_hour}.")
            self.update_event_lists()

    def update_event_lists(self):
        today = datetime.datetime.now().date()
        past_events = [event for event in self.events if datetime.datetime.strptime(event[0], "%m/%d/%y").date() < today]
        upcoming_events = [event for event in self.events if datetime.datetime.strptime(event[0], "%m/%d/%y").date() >= today]

        for item in self.past_events_tree.get_children():
            self.past_events_tree.delete(item)
        for item in self.upcoming_events_tree.get_children():
            self.upcoming_events_tree.delete(item)

        for event in past_events:
            self.past_events_tree.insert("", "end", values=(event[0], event[1], event[2]))
        for event in upcoming_events:
            self.upcoming_events_tree.insert("", "end", values=(event[0], event[1], event[2]))

def save_event_to_file(date, event_name, event_hour):
    with open("events.txt", "a", encoding="utf-8") as f:
        f.write(f"{date}|{event_name}|{event_hour}\n")

def open_schedule(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()
    ScheduleScreen(parent_frame)