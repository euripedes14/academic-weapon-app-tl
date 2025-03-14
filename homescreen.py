import tkinter as tk
from tkinter import messagebox
from schedule_screen import open_schedule  # Import the open_schedule function
from mam import open_nutrition  # Import the open_nutrition function

def open_courses():
    messagebox.showinfo("Εισαγωγή Μαθημάτων", "Μεταφορά στην οθόνη εισαγωγής μαθημάτων.")

def open_notifications():
    messagebox.showinfo("Ειδοποιήσεις & Streaks", "Μεταφορά στην οθόνη ειδοποιήσεων.")

def open_settings():
    messagebox.showinfo("Ρυθμίσεις", "Μεταφορά στις ρυθμίσεις εφαρμογής.")

def hide_all_frames():
    schedule_frame.pack_forget()
    nutrition_frame.pack_forget()

def show_nutrition():
    hide_all_frames()
    nutrition_frame.pack(fill=tk.BOTH, expand=True)
    open_nutrition(nutrition_frame)

def show_schedule():
    hide_all_frames()
    schedule_frame.pack(fill=tk.BOTH, expand=True)
    open_schedule(schedule_frame)

# Δημιουργία του κύριου παραθύρου
root = tk.Tk()
root.title("LockIN - Αρχική Οθόνη")
root.state("zoomed")

# Δημιουργία μενού στο πάνω μέρος
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Προσθήκη επιλογών στο μενού
menu_bar.add_command(label="Εισαγωγή Μαθημάτων", command=open_courses)
menu_bar.add_command(label="Τι έχει το πρόγραμμα?", command=show_schedule)
menu_bar.add_command(label="Τι θα φάμε σήμερα?", command=show_nutrition)
menu_bar.add_command(label="Ειδοποιήσεις & Streaks", command=open_notifications)
menu_bar.add_command(label="Ρυθμίσεις", command=open_settings)

# Προσθήκη τίτλου
label = tk.Label(root, text="Καλώς ήρθατε στο LockIN", font=("Arial", 14))
label.pack(pady=20)

# Δημιουργία frame για το πρόγραμμα
schedule_frame = tk.Frame(root, bg="#f2f2f2")

# Δημιουργία frame για το πρόγραμμα σίτισης και την παρακολούθηση της κατανάλωσης νερού
nutrition_frame = tk.Frame(root, bg="#f2f2f2")

# Εκκίνηση εφαρμογής
root.mainloop()