import customtkinter as ctk

def open_study_screen(parent_frame, username=None):
    for widget in parent_frame.winfo_children():
        widget.destroy()
    # Εμφάνιση Pomodoro και ZoneIn GUIs για μελέτη
    import zonein
    import pomodoro
    # Δημιουργία πλαισίου για μελέτη
    study_frame = ctk.CTkFrame(parent_frame)
    study_frame.pack(fill="both", expand=True)
    # Εμφάνιση ZoneIn (π.χ. αριστερά)
    zonein_frame = ctk.CTkFrame(study_frame)
    zonein_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)
    zonein.ZoneInScreen(zonein_frame, username=username)