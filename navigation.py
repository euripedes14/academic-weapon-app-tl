import customtkinter as ctk
from login import LoginScreen
from signup_screen import SignUpScreen
from homescreen import HomeScreen


def main_app(username=None):
    """Launch the Home screen with user context."""
    root = ctk.CTk()
    root.state("zoomed")  # Full screen on Windows
    app = HomeScreen(root, username=username)
    root.mainloop()