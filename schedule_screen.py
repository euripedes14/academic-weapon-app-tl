import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkcalendar import Calendar
import datetime
from error_control import ErrorControl

# ctk.set_default_color_theme("themes/breeze.json")

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

class AddEventDialog(ctk.CTkToplevel):
    def __init__(self, parent, date, on_save):
        super().__init__(parent)
        self.title("Προσθήκη Υποχρέωσης")
        self.geometry("400x300")  # Αυξημένο ύψος και πλάτος για να φαίνονται όλα τα περιεχόμενα
        self.resizable(False, False)
        self.on_save = on_save
        self.date = date
        ctk.CTkLabel(self, text=f"Ημερομηνία: {date}", font=("Arial", 12)).pack(pady=(10, 5))
        ctk.CTkLabel(self, text="Όνομα Εργασίας", font=("Arial", 12)).pack(pady=(5, 2))
        self.name_entry = ctk.CTkEntry(self, width=250)
        self.name_entry.pack(pady=2)
        ctk.CTkLabel(self, text="Ώρα (π.χ. 14:00)", font=("Arial", 12)).pack(pady=(10, 2))
        self.time_entry = ctk.CTkEntry(self, width=120)
        self.time_entry.pack(pady=2)
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=25)
        ctk.CTkButton(btn_frame, text="Αποθήκευση", command=self.save).pack(side="left", padx=15)
        ctk.CTkButton(btn_frame, text="Ακύρωση", command=self.cancel).pack(side="left", padx=15)
        self.grab_set()
        self.wait_window()
    def save(self):
        name = self.name_entry.get()
        time = self.time_entry.get()
        if not name or not time:
            CTkMessagebox(title="Σφάλμα", message="Συμπλήρωσε όλα τα πεδία.", icon="warning")
            return
        self.on_save(self.date, name, time)
        self.destroy()
    def cancel(self):
        self.destroy()

class ScheduleScreen(ctk.CTkFrame):
    def __init__(self, parent, username=None):
        super().__init__(parent, fg_color="#f2f2f2", corner_radius=10)
        self.pack(fill="both", expand=True)
        self.username = username
        self.events = []
        self.load_events_from_file()
        self.columnconfigure(0, weight=1, uniform="group1")
        self.columnconfigure(1, weight=2, uniform="group1")
        self.columnconfigure(2, weight=1, uniform="group1")
        self.rowconfigure(0, weight=1)
        # Αριστερή στήλη: μη ολοκληρωμένες
        self.left_frame = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=10)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=20)
        ctk.CTkLabel(self.left_frame, text="Μη ολοκληρωμένες Εργασίες", font=("Arial", 14, "bold"), text_color="#000000").pack(anchor='n', pady=10)
        self.left_list = ctk.CTkScrollableFrame(self.left_frame, height=300)
        self.left_list.pack(fill="both", expand=True, padx=10, pady=10)
        # Κεντρικό ημερολόγιο
        self.calendar_frame = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=10)
        self.calendar_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 5), pady=20)
        ctk.CTkLabel(self.calendar_frame, text="Ημερολόγιο", font=("Arial", 14, "bold"), text_color="#000000").pack(anchor='n', pady=10)
        self.cal = Calendar(self.calendar_frame, selectmode='day', year=datetime.datetime.now().year,
                            month=datetime.datetime.now().month, day=datetime.datetime.now().day)
        self.cal.pack(fill="both", expand=True, padx=40, pady=40, ipadx=80, ipady=80)
        self.cal.bind("<<CalendarSelected>>", self.on_date_click)
        # Δεξιά στήλη: ολοκληρωμένες
        self.right_frame = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=10)
        self.right_frame.grid(row=0, column=2, sticky="nsew", padx=(5, 10), pady=20)
        ctk.CTkLabel(self.right_frame, text="Ολοκληρωμένες Εργασίες", font=("Arial", 14, "bold"), text_color="#000000").pack(anchor='n', pady=10)
        self.right_list = ctk.CTkScrollableFrame(self.right_frame, height=300)
        self.right_list.pack(fill="both", expand=True, padx=10, pady=(10,0))
        # Κουμπί καθαρισμού κάτω από τη scrollable λίστα
        self.clear_done_btn = ctk.CTkButton(self.right_frame, text="Καθαρισμός", fg_color="#faa2a2", hover_color="#f88379", command=self.clear_done_events)
        self.clear_done_btn.pack(side="bottom", pady=(10, 10))
        self.update_event_lists()

    def on_date_click(self, event):
        selected_date = self.cal.get_date()
        AddEventDialog(self, selected_date, self.add_event_from_dialog)

    def add_event_from_dialog(self, date, name, time):
        if not ErrorControl.is_time_slot_available(date, time):
            CTkMessagebox(title="Σύγκρουση Ώρας", message="Υπάρχει ήδη υποχρέωση για αυτή την ημερομηνία και ώρα.", icon="warning")
            return
        self.events.append((date, name, time, "undone"))
        self.save_events_to_file()
        self.update_event_lists()

    def update_event_lists(self):
        today = datetime.datetime.now().date()
        undone = []
        done = []
        for event in self.events:
            if len(event) == 4:
                date_str, event_name, event_hour, status = event
            else:
                date_str, event_name, event_hour = event
                status = "undone"
            for fmt in ("%d/%m/%Y", "%m/%d/%y"):
                try:
                    event_date = datetime.datetime.strptime(date_str.strip(), fmt).date()
                    break
                except ValueError:
                    continue
            else:
                continue
            if status == "done":
                done.append((date_str, event_name, event_hour, status))
            else:
                undone.append((date_str, event_name, event_hour, status))
        for widget in self.left_list.winfo_children():
            widget.destroy()
        for widget in self.right_list.winfo_children():
            widget.destroy()
        for event in undone:
            self.add_event_widget(self.left_list, event, completed=False)
        for event in done:
            self.add_event_widget(self.right_list, event, completed=True)

    def add_event_widget(self, parent, event, completed=False):
        date_str, event_name, event_hour, status = event
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=2)
        if not completed:
            var = ctk.BooleanVar(value=False)
            cb = ctk.CTkCheckBox(frame, variable=var, text="", command=lambda: self.mark_event_done(event))
            cb.pack(side="left")
            ctk.CTkLabel(frame, text=f"{date_str} | {event_name} | {event_hour}", anchor="w").pack(side="left", fill="x", expand=True, padx=5)
        else:
            ctk.CTkLabel(frame, text=f"{date_str} | {event_name} | {event_hour}", anchor="w", text_color="#888888", font=("Arial", 10, "overstrike")).pack(side="left", fill="x", expand=True, padx=5)

    def mark_event_done(self, event):
        # Ενημέρωση λίστας και αρχείου
        updated = []
        for e in self.events:
            if e[:3] == event[:3]:
                updated.append((e[0], e[1], e[2], "done"))
            else:
                updated.append(e)
        self.events = updated
        self.save_events_to_file()
        self.update_event_lists()

    def clear_done_events(self):
        answer = CTkMessagebox(title="Επιβεβαίωση", message="Θέλεις σίγουρα να διαγράψεις όλες τις ολοκληρωμένες εργασίες;", icon="question", option_1="Ναι", option_2="Όχι").get()
        if answer == "Ναι":
            self.events = [e for e in self.events if not (len(e) == 4 and e[3] == "done")]
            self.save_events_to_file()
            self.update_event_lists()

    def save_events_to_file(self):
        filename = f"events_{self.username}.txt" if self.username else "events.txt"
        with open(filename, "w", encoding="utf-8") as f:
            for e in self.events:
                f.write("|".join([e[0], e[1], e[2], e[3]]) + "\n")

    def load_events_from_file(self):
        self.events = []
        try:
            filename = f"events_{self.username}.txt" if self.username else "events.txt"
            with open(filename, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) == 4:
                        self.events.append(tuple(parts))
                    elif len(parts) == 3:
                        self.events.append((*parts, "undone"))
        except FileNotFoundError:
            pass

def save_event_to_file(date, event_name, event_hour, username=None):
    filename = f"events_{username}.txt" if username else "events.txt"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{date}|{event_name}|{event_hour}\n")

def open_schedule(parent_frame, username=None):
    for widget in parent_frame.winfo_children():
        widget.destroy()
    ScheduleScreen(parent_frame, username=username)
