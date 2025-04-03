import customtkinter as ctk


class SettingsMenuApp:
    def __init__(self, parent_frame):
        self.parent = parent_frame

        # Κύριο πλαίσιο με λευκό φόντο
        self.main_frame = ctk.CTkFrame(self.parent, corner_radius=10, fg_color="#ffffff")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Πλαίσιο πλοήγησης με λευκό φόντο
        self.categories_frame = ctk.CTkFrame(self.main_frame, width=200, corner_radius=10, fg_color="#f9f9f9")
        self.categories_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Προσθήκη κουμπιών για τις κατηγορίες
        self.add_category_button("Προφίλ", self.show_profile_settings)
        self.add_category_button("Λογαριασμός", self.show_account_settings)
        self.add_category_button("Απόρρητο", self.show_privacy_settings)
        self.add_category_button("Σχετικά", self.show_about_settings)

        # Περιεχόμενο με λευκό φόντο
        self.content_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color="#ffffff")
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def add_category_button(self, text, command):
        # A dictionary to keep track of buttons for highlighting logic
        if not hasattr(self, "category_buttons"):
            self.category_buttons = []

        def wrapped_command():
            for btn in self.category_buttons:
                btn.configure(fg_color="#e0e0e0")  # Reset other buttons
            button.configure(fg_color="#cccccc")  # Highlight pressed button
            command()  # Execute the passed command

        button = ctk.CTkButton(
            self.categories_frame,
            text=text,
            command=wrapped_command,
            width=180,
            fg_color="#e0e0e0",  # Light gray background for button
            hover_color="#d1d1d1",  # Hover effect
            corner_radius=5,
            text_color="#000000"  # Black text
        )
        button.pack(pady=10)
        self.category_buttons.append(button)  # Add button to tracking list

    def show_profile_settings(self):
        self.clear_content_frame()

        # Username Setting
        username_label = ctk.CTkLabel(self.content_frame, text="Όνομα χρήστη:", text_color="#000000")
        username_label.pack(anchor="w", pady=5)
        username_entry = ctk.CTkEntry(
            self.content_frame,
            width=300,
            placeholder_text="Τρέχον Όνομα Χρήστη",
            fg_color="#f5f5f5",  # Slightly darker light background for better visibility
            text_color="#000000"  # Black text
        )
        username_entry.pack(pady=5)

        # Profile Picture Setting
        image_label = ctk.CTkLabel(self.content_frame, text="Φωτογραφία Προφίλ:", text_color="#000000")
        image_label.pack(anchor="w", pady=5)
        change_image_button = ctk.CTkButton(
            self.content_frame,
            text="Αλλαγή Φωτογραφίας",
            width=150,
            fg_color="#f0f0f0",  # Very light gray for the button for better visibility
            hover_color="#e5e5e5",  # Light hover effect
            text_color="#000000"  # Black text for contrast
        )
        change_image_button.pack(pady=5)

        # Pronouns Setting
        pronouns_label = ctk.CTkLabel(self.content_frame, text="Αντωνυμίες:", text_color="#000000")
        pronouns_label.pack(anchor="w", pady=5)
        pronouns_dropdown = ctk.CTkOptionMenu(
            self.content_frame,
            values=["αυτός/αυτού", "αυτή/αυτής", "αυτοί/αυτών"],
            fg_color="#ffffff",  # Pure white for the dropdown button for consistency
            button_color="#f0f0f0",  # Light button color to match the profile picture button
            button_hover_color="#e8e8e8",  # Hover effect slightly darker
            dropdown_fg_color="#f9f9f9",  # Light background for dropdown list
            dropdown_hover_color="#f1f1f1",  # Lighter hover effect for list items
            dropdown_text_color="#000000",  # Black text for readability
            text_color="#000000"  # Dropdown button text color
        )
        pronouns_dropdown.set("Διάλεξε αντωνυμίες")  # Placeholder message
        pronouns_dropdown.pack(pady=5)

        # Save and Cancel Buttons
        button_frame = ctk.CTkFrame(self.content_frame, fg_color="#ffffff")  # White background for the frame
        button_frame.pack(pady=20)
        save_button = ctk.CTkButton(
            button_frame,
            text="Αποθήκευση Αλλαγών",
            fg_color="#b2f2bb",  # Light green save button
            hover_color="#9ae6a1",  # Slightly darker hover for save button
            text_color="#000000",  # Black text
            command=self.save_changes
        )
        save_button.pack(side="left", padx=10)
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Ακύρωση",
            fg_color="#faa2a2",  # Light red cancel button
            hover_color="#f88379",  # Slightly darker hover for cancel button
            text_color="#000000",  # Black text
            command=self.cancel_changes
        )
        cancel_button.pack(side="left", padx=10)

    def show_account_settings(self):
        self.clear_content_frame()

        # Αλλαγή email
        email_label = ctk.CTkLabel(self.content_frame, text="Αλλαγή Email:", text_color="#000000")
        email_label.pack(anchor="w", pady=5)
        email_entry = ctk.CTkEntry(self.content_frame, width=300, placeholder_text="Νέο Email", fg_color="#f9f9f9",
                                   text_color="#000000")
        email_entry.pack(pady=5)

        # Αλλαγή κωδικού
        password_label = ctk.CTkLabel(self.content_frame, text="Νέος Κωδικός:", text_color="#000000")
        password_label.pack(anchor="w", pady=5)
        password_entry = ctk.CTkEntry(self.content_frame, width=300, placeholder_text="Νέος Κωδικός", show="*",
                                      fg_color="#f9f9f9", text_color="#000000")
        password_entry.pack(pady=5)

        # Τρέχων κωδικός
        current_password_label = ctk.CTkLabel(self.content_frame, text="Τρέχων Κωδικός:", text_color="#000000")
        current_password_label.pack(anchor="w", pady=5)
        current_password_entry = ctk.CTkEntry(self.content_frame, width=300, placeholder_text="Τρέχων Κωδικός",
                                              show="*", fg_color="#f9f9f9", text_color="#000000")
        current_password_entry.pack(pady=5)

        # Κουμπιά Αποθήκευσης και Ακύρωσης
        button_frame = ctk.CTkFrame(self.content_frame, fg_color="#ffffff")
        button_frame.pack(pady=20)
        save_button = ctk.CTkButton(button_frame, text="Αποθήκευση Αλλαγών", fg_color="#b2f2bb", text_color="#000000",
                                    command=self.save_changes)
        save_button.pack(side="left", padx=10)
        cancel_button = ctk.CTkButton(button_frame, text="Ακύρωση", fg_color="#faa2a2", text_color="#000000",
                                      command=self.cancel_changes)
        cancel_button.pack(side="left", padx=10)

    def show_privacy_settings(self):
        self.clear_content_frame()

        # Ενεργοποίηση τοποθεσίας
        location_label = ctk.CTkLabel(self.content_frame, text="Επιτρέψτε Πρόσβαση Τοποθεσίας:", text_color="#000000")
        location_label.pack(anchor="w", pady=5)
        location_toggle = ctk.CTkSwitch(self.content_frame, text="", onvalue=True, offvalue=False, fg_color="#e0e0e0",
                                        button_color="#b2f2bb")
        location_toggle.pack(pady=5)

    def show_about_settings(self):
        self.clear_content_frame()

        # Πληροφορίες Εφαρμογής
        about_label = ctk.CTkLabel(
            self.content_frame,
            text="Σχετικά με την Εφαρμογή",
            text_color="#000000",
            font=("Arial", 24)
        )
        about_label.pack(pady=20)

        description_label = ctk.CTkLabel(
            self.content_frame,
            text="LockIN: Σύμμαχος των Φοιτητών.\nΈκδοση 0.1\nΠρογραμματιστές: Η ομάδα σας",
            text_color="#555555"
        )
        description_label.pack(pady=5)

    def save_changes(self):
        print("Οι αλλαγές αποθηκεύτηκαν!")  # Υλοποίηση placeholder

    def cancel_changes(self):
        print("Οι αλλαγές ακυρώθηκαν!")  # Υλοποίηση placeholder

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("800x600")  # Ορισμός μεγέθους του κύριου παραθύρου
    root.title("Μενού Ρυθμίσεων")

    app = SettingsMenuApp(root)  # Παράμετρος "root" στο γονικό πλαίσιο
    root.mainloop()