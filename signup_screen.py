import tkinter as tk

class SignUpScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign Up")
        self.root.geometry("300x300")

        self.create_widgets()

    def create_widgets(self):
        # Username label and entry
        username_label = tk.Label(self.root, text="Username")
        username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        # Password label and entry
        password_label = tk.Label(self.root, text="Password")
        password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        # Confirm Password label and entry
        confirm_password_label = tk.Label(self.root, text="Confirm Password")
        confirm_password_label.pack(pady=5)
        self.confirm_password_entry = tk.Entry(self.root, show="*")
        self.confirm_password_entry.pack(pady=5)

        # Sign-up button
        signup_button = tk.Button(self.root, text="Sign Up", command=self.signup)
        signup_button.pack(pady=20)

#Afto apla kanei click ki anoigei to login screen
    def signup(self):
        self.root.destroy()
        login_app()

def login_app():
    from login import LoginScreen  # Import here to avoid circular import
    root = tk.Tk()
    app = LoginScreen(root)
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = SignUpScreen(root)
    root.mainloop()