import customtkinter as ctk


class BaseScreen:
    def __init__(self, root, title):
        self.root = root
        self.root.title(title)
        self.root.geometry("800x600")
        self.root.resizable(False, False)  # Disable resizing
        ctk.set_appearance_mode("light")  # Set light or dark mode
        ctk.set_default_color_theme("blue")  # Set the color theme

        self.create_widgets()

    def create_widgets(self):
        # Main frame for the screen
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=10, fg_color="#ffffff")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5, relheight=0.6)

        # Grid layout for labels and entries
        self.main_frame.grid_columnconfigure(0, weight=1)  # Left padding
        self.main_frame.grid_columnconfigure(1, weight=3)  # Label and entry
        self.main_frame.grid_columnconfigure(2, weight=1)  # Right padding

        # Title label
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=("Arial", 24, "bold"),
            text_color="#000000"
        )
        self.title_label.grid(row=0, column=0, columnspan=3, pady=20)

        # Username label and entry
        username_label = ctk.CTkLabel(
            self.main_frame,
            text="Username:",
            font=("Arial", 14),
            text_color="#000000"
        )
        username_label.grid(row=1, column=1, padx=10, pady=10, sticky="e")
        self.username_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Enter your username",
            width=300,
            fg_color="#f5f5f5",
            text_color="#000000"
        )
        self.username_entry.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        # Password label and entry
        password_label = ctk.CTkLabel(
            self.main_frame,
            text="Password:",
            font=("Arial", 14),
            text_color="#000000"
        )
        password_label.grid(row=2, column=1, padx=10, pady=10, sticky="e")
        self.password_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Enter your password",
            show="*",
            width=300,
            fg_color="#f5f5f5",
            text_color="#000000"
        )
        self.password_entry.grid(row=2, column=2, padx=10, pady=10, sticky="w")