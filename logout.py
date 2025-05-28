import sys
import os
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk

def logout_and_login(root=None):
    # Δημιουργεί ανεξάρτητο pop-up για επιβεβαίωση logout
    temp_root = None
    if root is None:
        temp_root = ctk.CTk()
        temp_root.withdraw()
        parent = temp_root
    else:
        parent = root
    answer = CTkMessagebox(
        master=parent,
        title="Αποσύνδεση",
        message="Είστε σίγουροι ότι θέλετε να αποσυνδεθείτε;\nWe will be sad to see you go :c",
        icon="question",
        option_1="Ναι",
        option_2="Όχι"
    ).get()
    if temp_root:
        temp_root.destroy()
    if answer == "Ναι":
        if root:
            root.withdraw()
            from login import login_app
            login_app(parent=root)
        else:
            from login import login_app
            login_app()
