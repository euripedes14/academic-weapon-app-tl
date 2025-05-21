import customtkinter as ctk
from login_signup_basescreen import BaseScreen
from CTkMessagebox import CTkMessagebox
from database_drop import create_database, create_tables, check_user_credentials

# Εφαρμογή breeze theme σε όλα τα CTk widgets
ctk.set_default_color_theme("themes/breeze.json")
ctk.set_appearance_mode("light")


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
        conn = create_database() # Ensure the database is created
        create_tables(conn) # Ensure the tables are created
        # Check user credentials
        if check_user_credentials(conn, username, password):
            self.root.destroy()
            from navigation import main_app
            main_app()
        else:
            CTkMessagebox(title="Login Failed", message="Invalid username or password.")
        conn.close()

    def open_signup(self):
        self.main_frame.destroy()
        from signup_screen import SignUpScreen
        SignUpScreen(self.root)

def login_app():
    """Launch the Login screen."""
    root = ctk.CTk()
    ctk.set_default_color_theme("themes/breeze.json")
    ctk.set_appearance_mode("light")
    root.state("zoomed")  # <-- Προσθήκη για full screen
    app = LoginScreen(root)
    root.mainloop()

if __name__ == "__main__":
    login_app()