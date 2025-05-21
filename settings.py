import customtkinter as ctk

# Εφαρμογή του breeze theme σε όλα τα στοιχεία
ctk.set_default_color_theme("themes/breeze.json")


class SettingsMenuApp:
    def __init__(self, parent_frame):
        self.parent = parent_frame

        # Κύριο πλαίσιο
        self.main_frame = ctk.CTkFrame(self.parent, corner_radius=10)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Πλαίσιο πλοήγησης
        self.categories_frame = ctk.CTkFrame(self.main_frame, width=200, corner_radius=10)
        self.categories_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Προσθήκη κουμπιών για τις κατηγορίες
        self.add_category_button("Προφίλ", self.show_profile_settings)
        self.add_category_button("Λογαριασμός", self.show_account_settings)
        self.add_category_button("Απόρρητο", self.show_privacy_settings)
        self.add_category_button("Σχετικά", self.show_about_settings)

        # Περιεχόμενο
        self.content_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def add_category_button(self, text, command):
        # A dictionary to keep track of buttons for highlighting logic
        if not hasattr(self, "category_buttons"):
            self.category_buttons = []

        def wrapped_command():
            command()

        button = ctk.CTkButton(
            self.categories_frame,
            text=text,
            command=wrapped_command,
            width=180,
            corner_radius=5
        )
        button.pack(pady=10)
        self.category_buttons.append(button)  # Add button to tracking list

    def show_profile_settings(self):
        self.clear_content_frame()

        # Username Setting
        username_label = ctk.CTkLabel(self.content_frame, text="Όνομα χρήστη:")
        username_label.pack(anchor="w", pady=5)
        username_entry = ctk.CTkEntry(
            self.content_frame,
            width=300,
            placeholder_text="Τρέχον Όνομα Χρήστη"
        )
        username_entry.pack(pady=5)

        # Profile Picture Setting
        image_label = ctk.CTkLabel(self.content_frame, text="Φωτογραφία Προφίλ:")
        image_label.pack(anchor="w", pady=5)
        change_image_button = ctk.CTkButton(
            self.content_frame,
            text="Αλλαγή Φωτογραφίας",
            width=150
        )
        change_image_button.pack(pady=5)

        # Pronouns Setting
        pronouns_label = ctk.CTkLabel(self.content_frame, text="Αντωνυμίες:")
        pronouns_label.pack(anchor="w", pady=5)
        pronouns_dropdown = ctk.CTkOptionMenu(
            self.content_frame,
            values=["αυτός/αυτού", "αυτή/αυτής", "αυτοί/αυτών"]
        )
        pronouns_dropdown.set("Διάλεξε αντωνυμίες")  # Placeholder message
        pronouns_dropdown.pack(pady=5)

        # Save and Cancel Buttons
        button_frame = ctk.CTkFrame(self.content_frame)
        button_frame.pack(pady=20)
        save_button = ctk.CTkButton(
            button_frame,
            text="Αποθήκευση Αλλαγών",
            command=self.save_changes
        )
        save_button.pack(side="left", padx=10)
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Ακύρωση",
            command=self.cancel_changes
        )
        cancel_button.pack(side="left", padx=10)

    def show_account_settings(self):
        self.clear_content_frame()

        # Αλλαγή email
        email_label = ctk.CTkLabel(self.content_frame, text="Αλλαγή Email:")
        email_label.pack(anchor="w", pady=5)
        email_entry = ctk.CTkEntry(self.content_frame, width=300, placeholder_text="Νέο Email")
        email_entry.pack(pady=5)

        # Αλλαγή κωδικού
        password_label = ctk.CTkLabel(self.content_frame, text="Νέος Κωδικός:")
        password_label.pack(anchor="w", pady=5)
        password_entry = ctk.CTkEntry(self.content_frame, width=300, placeholder_text="Νέος Κωδικός", show="*")
        password_entry.pack(pady=5)

        # Τρέχων κωδικός
        current_password_label = ctk.CTkLabel(self.content_frame, text="Τρέχων Κωδικός:")
        current_password_label.pack(anchor="w", pady=5)
        current_password_entry = ctk.CTkEntry(self.content_frame, width=300, placeholder_text="Τρέχων Κωδικός", show="*")
        current_password_entry.pack(pady=5)

        # Κουμπιά Αποθήκευσης και Ακύρωσης
        button_frame = ctk.CTkFrame(self.content_frame)
        button_frame.pack(pady=20)
        save_button = ctk.CTkButton(button_frame, text="Αποθήκευση Αλλαγών", command=self.save_changes)
        save_button.pack(side="left", padx=10)
        cancel_button = ctk.CTkButton(button_frame, text="Ακύρωση", command=self.cancel_changes)
        cancel_button.pack(side="left", padx=10)

    def show_privacy_settings(self):
        self.clear_content_frame()

        # Ενεργοποίηση τοποθεσίας
        location_label = ctk.CTkLabel(self.content_frame, text="Επιτρέψτε Πρόσβαση Τοποθεσίας:")
        location_label.pack(anchor="w", pady=5)
        location_toggle = ctk.CTkSwitch(self.content_frame, text="", onvalue=True, offvalue=False)
        location_toggle.pack(pady=5)

    def show_about_settings(self):
        self.clear_content_frame()
        # Πληροφορίες Εφαρμογής

    def save_changes(self):
        pass

    def cancel_changes(self):
        pass

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("800x600")  # Ορισμός μεγέθους του κύριου παραθύρου
    root.title("Μενού Ρυθμίσεων")

    app = SettingsMenuApp(root)  # Παράμετρος "root" στο γονικό πλαίσιο
    root.mainloop()