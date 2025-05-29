# Κλάση: LoginScreen
# Ρόλος: Υλοποιεί τη φόρμα σύνδεσης του χρήστη στην εφαρμογή.
# Κληρονομεί από:
# BaseScreen (από το login_signup_basescreen.py), που παρέχει βασική δομή για οθόνες authentication.
# Μέθοδοι:
# __init__(self, root)
# Αρχικοποιεί την οθόνη σύνδεσης, ορίζει τίτλο και καλεί τη self.add_buttons() για να προσθέσει τα κουμπιά.
# add_buttons(self)
# Προσθέτει δύο κουμπιά:
# "Login" (συνδέει με τη μέθοδο self.login)
# "Sign Up" (συνδέει με τη μέθοδο self.open_signup)
# login(self)
# Παίρνει τα στοιχεία από τα πεδία username/password, ελέγχει αν υπάρχουν στο settings.json και αν ο κωδικός είναι σωστός.
# Αν όλα είναι σωστά, καλεί το main_app από το navigation.py και περνά το username.
# Αν όχι, εμφανίζει μήνυμα λάθους με CTkMessagebox.
# open_signup(self)
# Καταστρέφει το frame και ανοίγει την οθόνη εγγραφής (SignUpScreen από signup_screen.py).
# Συνάρτηση:
# login_app(parent=None)
# Εκκινεί την οθόνη σύνδεσης είτε ως νέο παράθυρο είτε ως κύριο παράθυρο της εφαρμογής.


import customtkinter as ctk
from login_signup_basescreen import BaseScreen
from CTkMessagebox import CTkMessagebox
import os
import json

class LoginScreen(BaseScreen):
    def __init__(self, root):
        super().__init__(root, "Login")
        self.title_label.configure(text="Welcome to LockIN")
        self.add_buttons()

    def add_buttons(self):
        # Login button
        login_button = ctk.CTkButton(
            self.main_frame,
            text="Login",
            width=150,
            command=self.login
        )
        login_button.grid(row=3, column=1, columnspan=2, pady=20)

        # Sign-up button
        signup_button = ctk.CTkButton(
            self.main_frame,
            text="Sign Up",
            width=150,
            command=self.open_signup
        )
        signup_button.grid(row=4, column=1, columnspan=2, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Έλεγχος ύπαρξης και password στο settings.json
        settings_file = "settings.json"
        user_exists = False
        password_ok = False
        if os.path.exists(settings_file):
            with open(settings_file, "r", encoding="utf-8") as f:
                settings_data = json.load(f)
            if username in settings_data:
                user_exists = True
                user_account = settings_data[username].get("account", {})
                if user_account.get("password") == password:
                    password_ok = True
        if not user_exists:
            CTkMessagebox(title="Login Failed", message="Το username δεν υπάρχει.")
            return
        if not password_ok:
            CTkMessagebox(title="Login Failed", message="Λάθος κωδικός.")
            return
        self.root.destroy()
        from navigation import main_app
        main_app(username=username)

    def open_signup(self):
        self.main_frame.destroy()
        from signup_screen import SignUpScreen
        SignUpScreen(self.root)

def login_app(parent=None):
    if parent is not None:
        # Δημιουργία login ως Toplevel πάνω στο υπάρχον root
        login_window = ctk.CTkToplevel(parent)
        login_window.title("Login")
        login_window.state("zoomed")
        from login import LoginScreen
        LoginScreen(login_window)
        login_window.grab_set()
        login_window.focus_force()
    else:
        root = ctk.CTk()
        ctk.set_default_color_theme("themes/breeze.json")
        ctk.set_appearance_mode("light")
        root.state("zoomed")
        from login import LoginScreen
        LoginScreen(root)
        root.mainloop()

if __name__ == "__main__":
    login_app()