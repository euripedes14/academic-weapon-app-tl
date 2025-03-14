import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from tkcalendar import Calendar
import datetime

events = []
cal = None

def on_date_click(event):
    selected_date = cal.get_date()
    event_name = simpledialog.askstring("Προσθήκη Υποχρέωσης", f"Προσθήκη υποχρέωσης για {selected_date}:")
    event_hour = simpledialog.askstring("Προσθήκη Ώρας", "Εισάγετε την ώρα της υποχρέωσης (π.χ. 14:00):")
    if event_name and event_hour:
        events.append((selected_date, event_name, event_hour))
        messagebox.showinfo("Υποχρέωση Προστέθηκε", f"Υποχρέωση '{event_name}' προστέθηκε για {selected_date} στις {event_hour}.")
        update_event_lists()

def update_event_lists():
    today = datetime.datetime.now().date()
    past_events = [event for event in events if datetime.datetime.strptime(event[0], "%m/%d/%y").date() < today]
    upcoming_events = [event for event in events if datetime.datetime.strptime(event[0], "%m/%d/%y").date() >= today]

    for item in past_events_tree.get_children():
        past_events_tree.delete(item)
    for item in upcoming_events_tree.get_children():
        upcoming_events_tree.delete(item)

    for event in past_events:
        past_events_tree.insert("", "end", values=(event[0], event[1], event[2]))
    for event in upcoming_events:
        upcoming_events_tree.insert("", "end", values=(event[0], event[1], event[2]))

def open_schedule(schedule_frame):
    global cal, past_events_tree, upcoming_events_tree

    # Clear the frame
    for widget in schedule_frame.winfo_children():
        widget.destroy()

    # Δημιουργία frame για το ημερολόγιο
    calendar_frame = tk.Frame(schedule_frame)
    calendar_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.6, relheight=0.6)

    # Δημιουργία frame για παρελθόντα γεγονότα
    past_events_frame = tk.Frame(schedule_frame)
    past_events_frame.place(relx=0.1, rely=0.5, anchor=tk.CENTER, relwidth=0.2, relheight=0.6)
    tk.Label(past_events_frame, text="DONE", font=("Arial", 12)).pack(anchor='w')

    # Δημιουργία frame για μελλοντικά γεγονότα
    upcoming_events_frame = tk.Frame(schedule_frame)
    upcoming_events_frame.place(relx=0.9, rely=0.5, anchor=tk.CENTER, relwidth=0.2, relheight=0.6)
    tk.Label(upcoming_events_frame, text="TO DO", font=("Arial", 12)).pack(anchor='w')

    # Προσθήκη ημερολογίου
    cal = Calendar(calendar_frame, selectmode='day', year=datetime.datetime.now().year, 
                   month=datetime.datetime.now().month, day=datetime.datetime.now().day)
    cal.pack(fill=tk.BOTH, expand=True)
    cal.bind("<<CalendarSelected>>", on_date_click)

    # Create Treeview for past events
    past_events_tree = ttk.Treeview(past_events_frame, columns=("Date", "Event", "Time"), show="headings")
    past_events_tree.heading("Date", text="Date")
    past_events_tree.heading("Event", text="Event")
    past_events_tree.heading("Time", text="Time")
    past_events_tree.pack(fill=tk.BOTH, expand=True)

    # Create Treeview for upcoming events
    upcoming_events_tree = ttk.Treeview(upcoming_events_frame, columns=("Date", "Event", "Time"), show="headings")
    upcoming_events_tree.heading("Date", text="Date")
    upcoming_events_tree.heading("Event", text="Event")
    upcoming_events_tree.heading("Time", text="Time")
    upcoming_events_tree.pack(fill=tk.BOTH, expand=True)

    calendar_frame.pack(pady=20, fill=tk.BOTH, expand=True)
    past_events_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    upcoming_events_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    schedule_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.7, relheight=0.7)