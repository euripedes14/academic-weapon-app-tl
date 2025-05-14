from login_signup_basescreen import BaseScreen
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from database import create_database, create_tables, insert_user


# Example for signup_screen.py


class SignUpScreen(BaseScreen):
    def __init__(self, root):
        super().__init__(root, "Sign Up")
        self.title_label.configure(text="Create an Account")
        self.add_confirm_password()
        self.add_buttons()

    def add_confirm_password(self):
        # Confirm Password label and entry
        confirm_password_label = ctk.CTkLabel(
            self.main_frame,
            text="Confirm Password:",
            font=("Arial", 14),
            text_color="#000000"
        )
        confirm_password_label.grid(row=3, column=1, padx=10, pady=10, sticky="e")
        self.confirm_password_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Confirm your password",
            show="*",
            width=300,
            fg_color="#f5f5f5",
            text_color="#000000"
        )
        self.confirm_password_entry.grid(row=3, column=2, padx=10, pady=10, sticky="w")

    def add_buttons(self):
        # Sign-up button
        signup_button = ctk.CTkButton(
            self.main_frame,
            text="Create Account",
            width=150,
            fg_color="#e0e0e0",  # Light grey
            hover_color="#bdbdbd",  # Slightly darker grey
            text_color="#000000",
            command=self.signup
        )
        signup_button.grid(row=4, column=1, columnspan=2, pady=20)

        # Back to Login button
        back_button = ctk.CTkButton(
            self.main_frame,
            text="Back to Login",
            width=150,
            fg_color="#e0e0e0",  # Light grey
            hover_color="#bdbdbd",  # Slightly darker grey
            text_color="#000000",
            command=self.open_login
        )
        back_button.grid(row=5, column=1, columnspan=2, pady=10)

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        email = getattr(self, 'email_entry', None)
        email = email.get() if email else None
        pronouns = getattr(self, 'pronouns_entry', None)
        pronouns = pronouns.get() if pronouns else None

        if not username or not password:
            CTkMessagebox(title="Sign Up Failed", message="Username and password are required.", icon="cancel")
            return

        if password != confirm_password:
            CTkMessagebox(title="Sign Up Failed", message="Passwords do not match.", icon="cancel")
            return

        conn = create_database()
        create_tables(conn)
        try:
            insert_user(conn, username, password, email, pronouns)
            CTkMessagebox(title="Sign Up Success", message="Account created successfully!", icon="check")
            self.open_login()
        except Exception as e:
            CTkMessagebox(title="Sign Up Failed", message=f"Error: {e}", icon="cancel")
        finally:
            conn.close()

    def open_login(self):
        self.main_frame.destroy()  # Destroy only the frame, not the root
        from login import LoginScreen
        LoginScreen(self.root)

def signup_app():
    """Launch the Sign-Up screen."""
    root = ctk.CTk()
    app = SignUpScreen(root)
    root.mainloop()