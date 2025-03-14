import tkinter as tk
from tkinter import messagebox, simpledialog
from tkcalendar import Calendar
import datetime

events = []

def open_courses():
    messagebox.showinfo("Εισαγωγή Μαθημάτων", "Μεταφορά στην οθόνη εισαγωγής μαθημάτων.")

def open_schedule():
    messagebox.showinfo("Τι έχει το πρόγραμμα?", "Μεταφορά στην οθόνη διαχείρισης προγράμματος.")
    # Show the calendar frame
    calendar_frame.pack(pady=20, fill=tk.BOTH, expand=True)
    past_events_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    upcoming_events_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

def open_nutrition():
    messagebox.showinfo("Τι θα φάμε σήμερα?", "Μεταφορά στην οθόνη διατροφής & προτάσεων φαγητού.")

def open_notifications():
    messagebox.showinfo("Ειδοποιήσεις & Streaks", "Μεταφορά στην οθόνη ειδοποιήσεων.")

def open_settings():
    messagebox.showinfo("Ρυθμίσεις", "Μεταφορά στις ρυθμίσεις εφαρμογής.")

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

    for widget in past_events_frame.winfo_children():
        if widget.cget("text") != "          DONE":
            widget.destroy()
    for widget in upcoming_events_frame.winfo_children():
        if widget.cget("text") != "          TO DO":
            widget.destroy()

    for event in past_events:
        tk.Label(past_events_frame, text=f"{event[0]}: {event[1]} at {event[2]}").pack(anchor='w')
    for event in upcoming_events:
        tk.Label(upcoming_events_frame, text=f"{event[0]}: {event[1]} at {event[2]}").pack(anchor='w')

# Δημιουργία του κύριου παραθύρου
root = tk.Tk()
root.title("Academic Weapon - Αρχική Οθόνη")
root.state("zoomed")

# Δημιουργία μενού στο πάνω μέρος
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Προσθήκη επιλογών στο μενού
menu_bar.add_command(label="Εισαγωγή Μαθημάτων", command=open_courses)
menu_bar.add_command(label="Τι έχει το πρόγραμμα?", command=open_schedule)
menu_bar.add_command(label="Τι θα φάμε σήμερα?", command=open_nutrition)
menu_bar.add_command(label="Ειδοποιήσεις & Streaks", command=open_notifications)
menu_bar.add_command(label="Ρυθμίσεις", command=open_settings)

# Προσθήκη τίτλου
label = tk.Label(root, text="Καλώς ήρθατε στο SmartStudy", font=("Arial", 14))
label.pack(pady=20)

# Δημιουργία frame για το ημερολόγιο
calendar_frame = tk.Frame(root)
calendar_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.6, relheight=0.6)

# Δημιουργία frame για παρελθόντα γεγονότα
past_events_frame = tk.Frame(root)
past_events_frame.place(relx=0.1, rely=0.5, anchor=tk.CENTER, relwidth=0.2, relheight=0.6)
tk.Label(past_events_frame, text="          DONE", font=("Arial", 12)).pack(anchor='w')

# Δημιουργία frame για μελλοντικά γεγονότα
upcoming_events_frame = tk.Frame(root)
upcoming_events_frame.place(relx=0.9, rely=0.5, anchor=tk.CENTER, relwidth=0.2, relheight=0.6)
tk.Label(upcoming_events_frame, text="          TO DO", font=("Arial", 12)).pack(anchor='w')

# Προσθήκη ημερολογίου
cal = Calendar(calendar_frame, selectmode='day', year=datetime.datetime.now().year, 
               month=datetime.datetime.now().month, day=datetime.datetime.now().day)
cal.pack(fill=tk.BOTH, expand=True)
cal.bind("<<CalendarSelected>>", on_date_click)

# Εκκίνηση εφαρμογής
root.mainloop()