import customtkinter as ctk
import json
import os
from datetime import datetime

# Εφαρμογή του breeze theme σε όλα τα στοιχεία
ctk.set_default_color_theme("themes/breeze.json")


class SettingsMenuApp:
    def __init__(self, parent_frame, username=None):
        self.parent = parent_frame
        self.username = username

        # Κύριο πλαίσιο
        self.main_frame = ctk.CTkFrame(self.parent, corner_radius=10)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Πλαίσιο πλοήγησης
        self.categories_frame = ctk.CTkFrame(self.main_frame, width=200, corner_radius=10)
        self.categories_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Προσθήκη κουμπιών για τις κατηγορίες
        self.add_category_button("Προφίλ", self.show_profile_settings)
        self.add_category_button("Λογαριασμός", self.show_account_settings)
        self.add_category_button("Σχετικά", self.show_about_settings)

        # Περιεχόμενο
        self.content_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.settings_file = "settings.json"
        self.log_file = "settings_log.txt"
        self.settings_data = self.load_settings()
        self.current_category = None
        if self.username is None:
            # Αν δεν δοθεί username, χρησιμοποίησε το πρώτο διαθέσιμο (για δοκιμή)
            if self.settings_data:
                self.username = list(self.settings_data.keys())[0]
            else:
                self.username = "default"
        if self.username not in self.settings_data:
            self.settings_data[self.username] = {}

        # Εφαρμογή θέματος κατά την εκκίνηση, αν υπάρχει αποθηκευμένη επιλογή
        appearance_settings = self.get_user_settings().get("appearance", {})
        theme = appearance_settings.get("theme", "Λευκό")
        if theme == "Λευκό":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_settings(self):
        with open(self.settings_file, "w", encoding="utf-8") as f:
            json.dump(self.settings_data, f, ensure_ascii=False, indent=2)

    def get_user_settings(self):
        return self.settings_data.get(self.username, {})

    def set_user_settings(self, category, changes):
        if self.username not in self.settings_data:
            self.settings_data[self.username] = {}
        self.settings_data[self.username][category] = changes

    def show_profile_settings(self):
        self.clear_content_frame()
        self.current_category = "profile"
        user_settings = self.get_user_settings().get("profile", {})
        # Username Setting
        username_label = ctk.CTkLabel(self.content_frame, text="Όνομα χρήστη:")
        username_label.pack(anchor="w", pady=5)
        self.username_entry = ctk.CTkEntry(
            self.content_frame,
            width=300,
            placeholder_text="Τρέχον Όνομα Χρήστη"
        )
        self.username_entry.pack(pady=5)
        if user_settings.get("username"):
            self.username_entry.insert(0, user_settings["username"])
        # Pronouns Setting
        pronouns_label = ctk.CTkLabel(self.content_frame, text="Αντωνυμίες:")
        pronouns_label.pack(anchor="w", pady=5)
        self.pronouns_dropdown = ctk.CTkOptionMenu(
            self.content_frame,
            values=["αυτός/αυτού", "αυτή/αυτής", "αυτοί/αυτών"]
        )
        pronouns = user_settings.get("pronouns")
        if pronouns:
            self.pronouns_dropdown.set(pronouns)
        else:
            self.pronouns_dropdown.set("Διάλεξε αντωνυμίες")
        self.pronouns_dropdown.pack(pady=5)
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
        self.current_category = "account"
        user_settings = self.get_user_settings().get("account", {})
        # Αλλαγή email
        email_label = ctk.CTkLabel(self.content_frame, text="Αλλαγή Email:")
        email_label.pack(anchor="w", pady=5)
        self.email_entry = ctk.CTkEntry(self.content_frame, width=300, placeholder_text="Νέο Email")
        self.email_entry.pack(pady=5)
        if user_settings.get("email"):
            self.email_entry.insert(0, user_settings["email"])
        # Αλλαγή κωδικού
        password_label = ctk.CTkLabel(self.content_frame, text="Νέος Κωδικός:")
        password_label.pack(anchor="w", pady=5)
        self.password_entry = ctk.CTkEntry(self.content_frame, width=300, placeholder_text="Νέος Κωδικός", show="*")
        self.password_entry.pack(pady=5)
        # Τρέχων κωδικός
        current_password_label = ctk.CTkLabel(self.content_frame, text="Τρέχων Κωδικός:")
        current_password_label.pack(anchor="w", pady=5)
        self.current_password_entry = ctk.CTkEntry(self.content_frame, width=300, placeholder_text="Τρέχων Κωδικός", show="*")
        self.current_password_entry.pack(pady=5)
        # Κουμπιά Αποθήκευσης και Ακύρωσης
        button_frame = ctk.CTkFrame(self.content_frame)
        button_frame.pack(pady=20)
        save_button = ctk.CTkButton(button_frame, text="Αποθήκευση Αλλαγών", command=self.save_changes)
        save_button.pack(side="left", padx=10)
        cancel_button = ctk.CTkButton(button_frame, text="Ακύρωση", command=self.cancel_changes)
        cancel_button.pack(side="left", padx=10)

    def show_about_settings(self):
        self.clear_content_frame()
        self.current_category = "about"
        # Πληροφορίες Εφαρμογής
        about_title = ctk.CTkLabel(self.content_frame, text="Σχετικά με την Εφαρμογή", font=("Arial", 16, "bold"))
        about_title.pack(pady=(10, 5))
        about_text = ctk.CTkLabel(
            self.content_frame,
            text="LockIN \nΈκδοση 1.0.0\n\nΑυτή η εφαρμογή δημιουργήθηκε στα πλαίσια του μαθήματος \nΤεχνολογία Λογισμικού \nγια να βοηθήσει τους φοιτητές \nνα οργανώσουν το ακαδημαϊκό τους πρόγραμμα.\n\n Δημιουργήθηκε από την ομάδα:\nΚακαλής Βασίλειος, 1080444\nΛειβαδίτης Ιωάννης, 1093417\nΜπαλάση Δήμητρα, 1093440\nΠαπουτσή Αγγελική Ειρήνη, 1093473\nΠοτός Βασίλειος, 1097439\n\n Μπορείτε να δείτε την αναλυτική ανάπτυξη της εφαρμογής \nστο αποθετήριο μας στο GitHub:\nhttps://github.com/euripedes14/academic-weapon-app-tl\n",
            justify="center",
        )
        about_text.pack(pady=5)

    def save_changes(self):
        if self.current_category == "profile":
            old_username = self.username
            username = self.username_entry.get()
            pronouns = self.pronouns_dropdown.get()
            changes = {}
            if username:
                changes["username"] = username
            if pronouns and pronouns != "Διάλεξε αντωνυμίες":
                changes["pronouns"] = pronouns
            # Αν αλλάζει το username, μετέφερε τα δεδομένα και ενημέρωσε όλα τα δεδομένα του χρήστη
            if username and username != old_username:
                if username in self.settings_data:
                    self.show_success_message("Το username υπάρχει ήδη!")
                    return
                # Μεταφορά όλων των δεδομένων του χρήστη στο νέο username
                self.settings_data[username] = self.settings_data.pop(old_username)
                # Ενημέρωση του username σε όλα τα categories
                for category in self.settings_data[username]:
                    if isinstance(self.settings_data[username][category], dict):
                        self.settings_data[username][category]["username"] = username
                self.username = username
            self.set_user_settings("profile", changes)
            self.log_change(f"profile ({self.username})", changes)
            self.save_settings()
            self.clear_content_frame()
            self.show_success_message("Οι αλλαγές αποθηκεύτηκαν.")
        elif self.current_category == "account":
            email = self.email_entry.get()
            password = self.password_entry.get()
            current_password = self.current_password_entry.get()
            user_settings = self.get_user_settings().get("account", {})
            real_password = user_settings.get("password")
            if not real_password or not current_password or current_password != real_password:
                from CTkMessagebox import CTkMessagebox
                CTkMessagebox(title="Αποτυχία", message="Λάθος κωδικός.", icon="cancel")
                return
            changes = {}
            if email:
                changes["email"] = email
            if password:
                changes["password"] = password
            else:
                changes["password"] = real_password
            self.set_user_settings("account", changes)
            self.log_change(f"account ({self.username})", changes)
            self.save_settings()
            self.clear_content_frame()
            self.show_success_message("Οι αλλαγές αποθηκεύτηκαν.")
        # ΑΦΑΙΡΕΣΗ: Δεν προσθέτουμε κατηγορία 'Εμφάνιση' ούτε σχετικές μεθόδους

    def show_success_message(self, message):
        success_label = ctk.CTkLabel(self.content_frame, text=message, text_color="green")
        success_label.pack(pady=20)
        # Ασφαλής απόκρυψη του label μετά από 2 δευτερόλεπτα
        def safe_destroy():
            try:
                success_label.destroy()
            except Exception:
                pass
        self.parent.after(2000, safe_destroy)

    def cancel_changes(self):
        # Επαναφόρτωση των ρυθμίσεων της τρέχουσας κατηγορίας
        if self.current_category == "profile":
            self.show_profile_settings()
        elif self.current_category == "account":
            self.show_account_settings()
        # ΑΦΑΙΡΕΣΗ: Δεν χρειάζεται επαναφόρτωση για την κατηγορία 'Εμφάνιση'

    def show_log(self):
        self.clear_content_frame()
        log_text = ""
        if os.path.exists(self.log_file):
            with open(self.log_file, "r", encoding="utf-8") as f:
                log_text = f.read()
        log_label = ctk.CTkLabel(self.content_frame, text="Ιστορικό Επιλογών", font=("Arial", 14, "bold"))
        log_label.pack(pady=(10, 5))
        log_box = ctk.CTkTextbox(self.content_frame, width=600, height=400)
        log_box.insert("1.0", log_text)
        log_box.configure(state="disabled")
        log_box.pack(pady=5)

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
        self.category_buttons.append(button)
        # Προσθήκη κουμπιού για το log αν δεν υπάρχει ήδη
        if text == "Σχετικά" and not hasattr(self, "log_button_added"):
            self.log_button_added = True
            log_button = ctk.CTkButton(
                self.categories_frame,
                text="Ιστορικό",
                command=self.show_log,
                width=180,
                corner_radius=5
            )
            log_button.pack(pady=10)
            self.category_buttons.append(log_button)

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_about_settings(self):
        self.clear_content_frame()
        self.current_category = "about"
        # Πληροφορίες Εφαρμογής
        about_title = ctk.CTkLabel(self.content_frame, text="Σχετικά με την Εφαρμογή", font=("Arial", 16, "bold"))
        about_title.pack(pady=(10, 5))
        about_text = ctk.CTkLabel(
            self.content_frame,
            text="LockIN \nΈκδοση 1.0.0\n\nΑυτή η εφαρμογή δημιουργήθηκε στα πλαίσια του μαθήματος \nΤεχνολογία Λογισμικού \nγια να βοηθήσει τους φοιτητές \nνα οργανώσουν το ακαδημαϊκό τους πρόγραμμα.\n\n Δημιουργήθηκε από την ομάδα:\nΚακαλής Βασίλειος, 1080444\nΛειβαδίτης Ιωάννης, 1093417\nΜπαλάση Δήμητρα, 1093440\nΠαπουτσή Αγγελική Ειρήνη, 1093473\nΠοτός Βασίλειος, 1097439\n\n Μπορείτε να δείτε την αναλυτική ανάπτυξη της εφαρμογής \nστο αποθετήριο μας στο GitHub:\nhttps://github.com/euripedes14/academic-weapon-app-tl\n",
            justify="center",
        )
        about_text.pack(pady=5)

    def log_change(self, category, changes):
        """Καταγράφει τις αλλαγές ρυθμίσεων σε αρχείο log."""
        log_entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Χρήστης: {self.username}, Κατηγορία: {category}, Αλλαγές: {changes}\n"
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception:
            pass

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("800x600")  # Ορισμός μεγέθους του κύριου παραθύρου
    root.title("Μενού Ρυθμίσεων")

    app = SettingsMenuApp(root)  # Παράμετρος "root" στο γονικό πλαίσιο
    root.mainloop()