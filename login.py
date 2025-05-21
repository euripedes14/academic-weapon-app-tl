from login_signup_basescreen import BaseScreen
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from database_drop import create_database, create_tables, check_user_credentials


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
            fg_color="#e0e0e0",  # Light grey
            hover_color="#bdbdbd",  # Slightly darker grey
            text_color="#000000",
            command=self.login
        )
        login_button.grid(row=3, column=1, columnspan=2, pady=20)

        # Sign-up button
        signup_button = ctk.CTkButton(
            self.main_frame,
            text="Sign Up",
            width=150,
            fg_color="#e0e0e0",  # Light grey
            hover_color="#bdbdbd",  # Slightly darker grey
            text_color="#000000",
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
            # Show error message (using CTkMessageBox or a label)
            CTkMessagebox(title="Login Failed", message="Invalid username or password.")
        conn.close()

    def open_signup(self):
        self.main_frame.destroy()
        from signup_screen import SignUpScreen
        SignUpScreen(self.root)


def login_app():
    """Launch the Login screen."""
    root = ctk.CTk()
    app = LoginScreen(root)
    root.mainloop()

if __name__ == "__main__":
    login_app()