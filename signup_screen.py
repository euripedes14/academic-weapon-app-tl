from login_signup_basescreen import BaseScreen
from tkinter import messagebox
import customtkinter as ctk


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
        # Add your sign-up logic here
        messagebox.showinfo("Success", "Account created successfully!")
        self.open_login()

    def open_login(self):
        self.root.destroy()
        from login import login_app  # Import here to avoid circular import
        login_app()

def signup_app():
    """Launch the Sign-Up screen."""
    root = ctk.CTk()
    app = SignUpScreen(root)
    root.mainloop()