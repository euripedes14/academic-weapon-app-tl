import tkinter as tk
from tkinter import messagebox

def open_courses():
    messagebox.showinfo("Εισαγωγή Μαθημάτων", "Μεταφορά στην οθόνη εισαγωγής μαθημάτων.")

def open_schedule():
    messagebox.showinfo("Τι έχει το πρόγραμμα?", "Μεταφορά στην οθόνη διαχείρισης προγράμματος.")

def open_nutrition():
    messagebox.showinfo("Τι θα φάμε σήμερα?", "Μεταφορά στην οθόνη διατροφής & προτάσεων φαγητού.")

def open_notifications():
    messagebox.showinfo("Ειδοποιήσεις & Streaks", "Μεταφορά στην οθόνη ειδοποιήσεων.")

def open_settings():
    messagebox.showinfo("Ρυθμίσεις", "Μεταφορά στις ρυθμίσεις εφαρμογής.")

# Δημιουργία του κύριου παραθύρου
root = tk.Tk()
root.title("SmartStudy - Αρχική Οθόνη")
root.geometry("400x400")

# Προσθήκη τίτλου
label = tk.Label(root, text="Καλώς ήρθατε στο SmartStudy", font=("Arial", 14))
label.pack(pady=20)

# Κουμπιά πλοήγησης
buttons = [
    ("Εισαγωγή Μαθημάτων", open_courses),
    ("Τι έχει το πρόγραμμα?", open_schedule),
    ("Τι θα φάμε σήμερα?", open_nutrition),
    ("Ειδοποιήσεις & Streaks", open_notifications),
    ("Ρυθμίσεις", open_settings)
]

for text, command in buttons:
    button = tk.Button(root, text=text, command=command, width=30, height=2)
    button.pack(pady=5)

# Εκκίνηση εφαρμογής
root.mainloop()
