import customtkinter as ctk
from login import LoginScreen
from signup_screen import SignUpScreen
from homescreen import HomeScreen


def main_app():
    """Launch the Home screen."""
    root = ctk.CTk()
    root.state("zoomed")  # Full screen on Windows
    app = HomeScreen(root)
    root.mainloop()