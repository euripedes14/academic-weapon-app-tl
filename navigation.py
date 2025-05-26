import customtkinter as ctk
from login import LoginScreen
from signup_screen import SignUpScreen
from homescreen import HomeScreen


def main_app(username=None):
    """Launch the Home screen with user context."""
    root = ctk.CTk()
    try:
        root.state("zoomed")  # Try to maximize (works on most Windows)
    except Exception:
        pass
    # Fallback: set geometry to screen size (taskbar remains visible)
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")  
    
    app = HomeScreen(root, username=username)
    root.mainloop()