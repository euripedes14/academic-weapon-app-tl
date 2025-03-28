import tkinter as tk
from homescreen import HomeScreen

class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x250")

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

        # Login button
        login_button = tk.Button(self.root, text="Login", command=self.login)
        login_button.pack(pady=10)

        # Sign-up button
        signup_button = tk.Button(self.root, text="Sign Up", command=self.open_signup)
        signup_button.pack(pady=10)

#Afta apla kanoun click ki anoigoun to homescreen tr
    def login(self):
        self.root.destroy()
        main_app()

    def open_signup(self):
        self.root.destroy()
        signup_app()

def main_app():
    root = tk.Tk()
    app = HomeScreen(root)
    root.mainloop()

def signup_app():
    from signup_screen import SignUpScreen  # Import here to avoid circular import
    root = tk.Tk()
    app = SignUpScreen(root)
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginScreen(root)
    root.mainloop()