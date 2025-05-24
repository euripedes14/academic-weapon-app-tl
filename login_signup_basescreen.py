import customtkinter as ctk

# Εφαρμογή breeze theme σε όλα τα CTk widgets
# ctk.set_default_color_theme("themes/breeze.json")
# ctk.set_appearance_mode("light")

class BaseScreen:
    def __init__(self, root, title):
        self.root = root
        self.root.title(title)
        self.root.state("zoomed")  # Full screen on Windows
        self.root.resizable(True, True)  # Enable resizing

        self.create_widgets()

    def create_widgets(self):
        # Main frame for the screen (χωρίς fg_color για να πάρει το breeze theme)
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=10)
        # Make the frame bigger (e.g., 70% width, 75% height)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.7, relheight=0.75)

        # Grid layout for labels and entries
        self.main_frame.grid_columnconfigure(0, weight=2)  # More left padding
        self.main_frame.grid_columnconfigure(1, weight=3)  # Label and entry
        self.main_frame.grid_columnconfigure(2, weight=5)  # More right padding

        # Center the rows vertically by adding empty rows with weight
        self.main_frame.grid_rowconfigure(0, weight=2)  # Top padding
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_rowconfigure(3, weight=2)  # Bottom padding

        # Title label
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=("Arial", 24, "bold")
        )
        self.title_label.grid(row=1, column=0, columnspan=3, pady=20, sticky="n")

        # Username label and entry
        username_label = ctk.CTkLabel(
            self.main_frame,
            text="Username:",
            font=("Arial", 14)
        )
        username_label.grid(row=2, column=1, padx=10, pady=10, sticky="e")
        self.username_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Enter your username",
            width=300
        )
        self.username_entry.grid(row=2, column=2, padx=10, pady=10, sticky="w")

        # Password label and entry
        password_label = ctk.CTkLabel(
            self.main_frame,
            text="Password:",
            font=("Arial", 14)
        )
        password_label.grid(row=3, column=1, padx=10, pady=10, sticky="e")
        self.password_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Enter your password",
            show="*",
            width=300
        )
        self.password_entry.grid(row=3, column=2, padx=10, pady=10, sticky="w")
        # Main frame for the screen (χωρίς fg_color για να πάρει το breeze theme)
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.7, relheight=0.75)

        # Grid layout for labels and entries
        self.main_frame.grid_columnconfigure(0, weight=1)  # Left padding
        self.main_frame.grid_columnconfigure(1, weight=3)  # Label and entry
        self.main_frame.grid_columnconfigure(2, weight=5)  # Right padding

        # Title label
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=("Arial", 24, "bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=3, pady=20)

        # Username label and entry
        username_label = ctk.CTkLabel(
            self.main_frame,
            text="Username:",
            font=("Arial", 14)
        )
        username_label.grid(row=1, column=1, padx=10, pady=10, sticky="e")
        self.username_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Enter your username",
            width=300
        )
        self.username_entry.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        # Password label and entry
        password_label = ctk.CTkLabel(
            self.main_frame,
            text="Password:",
            font=("Arial", 14)
        )
        password_label.grid(row=2, column=1, padx=10, pady=10, sticky="e")
        self.password_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Enter your password",
            show="*",
            width=300
        )
        self.password_entry.grid(row=2, column=2, padx=10, pady=10, sticky="w")
