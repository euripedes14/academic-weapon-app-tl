import os
import json
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import fitz  # PyMuPDF
from map_search import MapSearch
import threading

# Εφαρμογή breeze theme σε όλα τα CTk widgets
# ctk.set_default_color_theme("themes/breeze.json")

MENU = {
    "Δευτέρα": ["Κοτόπουλο με ρύζι", "Σαλάτα", "Γιαούρτι"],
    "Τρίτη": ["Μακαρόνια με κιμά", "Τυρί φέτα", "Φρούτο"],
    "Τετάρτη": ["Φασολάκια", "Ψωμί", "Μήλο"],
    "Πέμπτη": ["Μπιφτέκια", "Πατάτες φούρνου", "Γιαούρτι"],
    "Παρασκευή": ["Ψάρι", "Χόρτα", "Πορτοκάλι"],
    "Σάββατο": ["Γεμιστά", "Φέτα", "Φρούτο"],
    "Κυριακή": ["Κοτόπουλο με πατάτες", "Σαλάτα", "Γλυκό"]
}

def create_scrollable_frame(nutrition_frame):
    main_frame = ctk.CTkFrame(nutrition_frame, fg_color="#f2f2f2", corner_radius=10)
    nutrition_frame.update_idletasks()
    main_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER, relwidth=0.8, relheight=0.8)

    canvas = ctk.CTkCanvas(main_frame, bg="#f2f2f2", highlightthickness=0)
    scrollbar = ctk.CTkScrollbar(main_frame, orientation="vertical", command=canvas.yview)
    scrollable_frame = ctk.CTkFrame(canvas, fg_color="#f2f2f2")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

    return canvas, scrollable_frame

class NutritionScreen:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.day_var = ctk.StringVar(value="Δευτέρα")
        self.create_ui()

    def create_ui(self):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        # Κεντρικό πλαίσιο
        container = ctk.CTkFrame(self.parent_frame, corner_radius=15)
        container.pack(fill="both", expand=True, padx=40, pady=40)

        # Τίτλος
        title = ctk.CTkLabel(container, text="Μενού Εστίας", font=("Arial", 28, "bold"))
        title.pack(pady=(10, 20))

        # Fun fact ή inspirational quote
        funfact = ctk.CTkLabel(
            container,
            text="🍏 \"Η σωστή διατροφή είναι το μυστικό της ενέργειας!\"",
            font=("Arial", 16, "italic")
        )
        funfact.pack(pady=(0, 20))

        # Επιλογή ημέρας
        day_frame = ctk.CTkFrame(container)
        day_frame.pack(pady=10)
        ctk.CTkLabel(day_frame, text="Επιλέξτε ημέρα:", font=("Arial", 15)).pack(side="left", padx=5)
        day_menu = ctk.CTkComboBox(
            day_frame, variable=self.day_var, values=list(MENU.keys()), width=150, font=("Arial", 14), command=self.update_menu
        )
        day_menu.pack(side="left", padx=5)

        # Πλαίσιο εμφάνισης μενού
        self.menu_frame = ctk.CTkFrame(container, corner_radius=10)
        self.menu_frame.pack(fill="both", expand=True, pady=25, padx=20)
        self.menu_labels = []
        self.update_menu(self.day_var.get())

        # Σχόλια/feedback
        feedback_label = ctk.CTkLabel(container, text="Έχεις σχόλια για το μενού;", font=("Arial", 14))
        feedback_label.pack(pady=(20, 5))
        self.feedback_entry = ctk.CTkEntry(container, placeholder_text="Γράψε εδώ το σχόλιό σου...", width=350)
        self.feedback_entry.pack(pady=5)
        submit_btn = ctk.CTkButton(container, text="Υποβολή", command=self.submit_feedback, width=120)
        submit_btn.pack(pady=(5, 15))

    def update_menu(self, day):
        # Καθαρισμός προηγούμενων labels
        for label in self.menu_labels:
            label.destroy()
        self.menu_labels.clear()

        menu_items = MENU.get(day, [])
        if not menu_items:
            lbl = ctk.CTkLabel(self.menu_frame, text="Δεν υπάρχει διαθέσιμο μενού.", font=("Arial", 16))
            lbl.pack(pady=10)
            self.menu_labels.append(lbl)
        else:
            for item in menu_items:
                lbl = ctk.CTkLabel(self.menu_frame, text=f"• {item}", font=("Arial", 18))
                lbl.pack(anchor="w", padx=20, pady=8)
                self.menu_labels.append(lbl)

    def submit_feedback(self):
        feedback = self.feedback_entry.get()
        if feedback.strip():
            ctk.CTkMessagebox(title="Ευχαριστούμε!", message="Το σχόλιό σου καταχωρήθηκε.")
            self.feedback_entry.delete(0, "end")
        else:
            ctk.CTkMessagebox(title="Προσοχή", message="Παρακαλώ γράψε ένα σχόλιο πριν την υποβολή.")

def open_nutrition(nutrition_frame):
    for widget in nutrition_frame.winfo_children():
        widget.destroy()

    # Breeze theme χρώματα
    theme_fg = "#B4D9E7"  # light mode
    theme_fg_dark = "#1E3A46"  # dark mode

    # Ερώτηση και κουμπιά επιλογής στο πάνω μέρος
    top_frame = ctk.CTkFrame(nutrition_frame, fg_color=theme_fg)
    top_frame.pack(pady=(30, 10))

    message_label = ctk.CTkLabel(top_frame, text="Που θα φας σήμερα?", font=("Arial", 18, "bold"), text_color="#000000")
    message_label.pack(pady=10)

    button_frame = ctk.CTkFrame(top_frame, fg_color=theme_fg)
    button_frame.pack(pady=5)

    # Κάτω μέρος για το δυναμικό περιεχόμενο
    content_frame = ctk.CTkFrame(nutrition_frame, fg_color=theme_fg)
    content_frame.pack(fill=ctk.BOTH, expand=True, padx=40, pady=20)

    def show_choice(choice):
        # Καθαρίζει το κάτω μέρος και εμφανίζει το περιεχόμενο της επιλογής
        for widget in content_frame.winfo_children():
            widget.destroy()
        # Κουμπί επιστροφής
        back_btn = ctk.CTkButton(content_frame, text="Πίσω", fg_color="#e0e0e0", hover_color="#bdbdbd", text_color="#000000", command=reset_to_question)
        back_btn.pack(pady=(0, 10))
        # Περιεχόμενο ανά επιλογή
        if choice == "estia":
            show_estia(content_frame)
        elif choice == "allou":
            show_allou(content_frame)

    def reset_to_question():
        for widget in content_frame.winfo_children():
            widget.destroy()

    estia_button = ctk.CTkButton(
        button_frame,
        text="Εστία",
        fg_color="#e0e0e0",
        hover_color="#bdbdbd",
        text_color="#000000",
        command=lambda: show_choice("estia")
    )
    estia_button.pack(side=ctk.LEFT, padx=20)

    allou_button = ctk.CTkButton(
        button_frame,
        text="Αλλού",
        fg_color="#e0e0e0",
        hover_color="#bdbdbd",
        text_color="#000000",
        command=lambda: show_choice("allou")
    )
    allou_button.pack(side=ctk.RIGHT, padx=20)

def show_estia(parent_frame):
    # Zoom state
    if not hasattr(parent_frame, '_zoom_level'):
        parent_frame._zoom_level = 1.0
    if not hasattr(parent_frame, '_pan_offset'):
        parent_frame._pan_offset = None

    square_frame = ctk.CTkFrame(parent_frame, fg_color="#B4D9E7", width=900, height=600, corner_radius=10)
    square_frame.pack(pady=20)
    square_frame.pack_propagate(False)

    # Zoom controls
    zoom_frame = ctk.CTkFrame(square_frame, fg_color="#B4D9E7")
    zoom_frame.pack(pady=(10, 0))
    ctk.CTkLabel(zoom_frame, text="Zoom:", font=("Arial", 14, "bold"), text_color="#000000").pack(side="left", padx=5)
    def set_zoom(delta):
        parent_frame._zoom_level = max(0.5, min(2.5, parent_frame._zoom_level + delta))
        parent_frame._pan_offset = None  # Reset pan on zoom
        load_pdf()  # Πρέπει να ξαναφορτώσει το pdf με νέο zoom
    ctk.CTkButton(zoom_frame, text="-", width=30, command=lambda: set_zoom(-0.2)).pack(side="left", padx=2)
    ctk.CTkButton(zoom_frame, text="+", width=30, command=lambda: set_zoom(0.2)).pack(side="left", padx=2)

    pdf_header = ctk.CTkLabel(square_frame, text="Φαγητό της εστίας", font=("Arial", 18, "bold"), text_color="#000000")
    pdf_header.pack(pady=10)

    # Canvas για εμφάνιση και drag
    canvas = ctk.CTkCanvas(square_frame, width=800, height=500, bg="#B4D9E7", highlightthickness=0)
    canvas.pack(pady=10)

    pdf_url = "https://www.upatras.gr/wp-content/uploads/2024/12/%CE%A0%CE%A1%CE%9F%CE%93%CE%A1%CE%91%CE%9C%CE%9C%CE%91-%CE%A3%CE%99%CE%A4%CE%99%CE%A3%CE%97%CE%A3-%CE%99%CE%91%CE%9D%CE%9F%CE%A5%CE%91%CE%A1%CE%99%CE%9F%CE%A3-2025_compressed.pdf"
    parent_frame._pdf_img = None
    parent_frame._canvas_img_id = None

    def render_pdf():
        canvas.delete("all")
        if parent_frame._pdf_img:
            if parent_frame._pan_offset is None:
                # Center image on first render or zoom
                parent_frame._pan_offset = [canvas.winfo_width()//2, canvas.winfo_height()//2]
            x, y = parent_frame._pan_offset
            parent_frame._canvas_img_id = canvas.create_image(x, y, anchor="center", image=parent_frame._pdf_img)

    def load_pdf():
        try:
            response = requests.get(pdf_url)
            pdf_data = BytesIO(response.content)
            doc = fitz.open(stream=pdf_data, filetype="pdf")
            page = doc.load_page(0)
            zoom = parent_frame._zoom_level
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            parent_frame._pdf_img = ImageTk.PhotoImage(img)
            parent_frame._pan_offset = None  # Center on new image
            parent_frame.after(0, render_pdf)
        except Exception as e:
            parent_frame.after(0, lambda: messagebox.showerror("Error", f"Failed to load PDF: {e}"))

    # Drag logic
    drag_data = {"x": 0, "y": 0, "dragging": False}
    def on_press(event):
        drag_data["x"] = event.x
        drag_data["y"] = event.y
        drag_data["dragging"] = True
    def on_release(event):
        drag_data["dragging"] = False
    def on_motion(event):
        if drag_data["dragging"] and parent_frame._pdf_img:
            dx = event.x - drag_data["x"]
            dy = event.y - drag_data["y"]
            if parent_frame._pan_offset is not None:
                parent_frame._pan_offset[0] += dx
                parent_frame._pan_offset[1] += dy
                drag_data["x"] = event.x
                drag_data["y"] = event.y
                render_pdf()
    canvas.bind("<ButtonPress-1>", on_press)
    canvas.bind("<ButtonRelease-1>", on_release)
    canvas.bind("<B1-Motion>", on_motion)

    threading.Thread(target=load_pdf).start()

def show_allou(parent_frame):
    map_frame = ctk.CTkFrame(parent_frame, fg_color="#f2f2f2", width=900, height=600, corner_radius=10)
    map_frame.pack(pady=20)
    map_frame.pack_propagate(False)

    map_header = ctk.CTkLabel(
        map_frame,
        text="Αν θέλεις να φας κάτι άλλο μπορείς να το βρεις εδώ!",
        font=("Arial", 18, "bold"),
        text_color="#000000"
    )
    map_header.pack(pady=10)

    # Initialize the map with Patras, Greece
    map_search = MapSearch(map_frame)

    # Add a search bar
    search_frame = ctk.CTkFrame(map_frame, fg_color="#f2f2f2")
    search_frame.pack(pady=10)
    search_entry = ctk.CTkEntry(search_frame, width=50, fg_color="#ffffff", text_color="#000000")
    search_entry.pack(side=ctk.LEFT, padx=10)
    search_button = ctk.CTkButton(
        search_frame,
        text="Search",
        fg_color="#e0e0e0",
        hover_color="#bdbdbd",
        text_color="#000000",
        command=lambda: map_search.search_location(search_entry.get())
    )
    search_button.pack(side=ctk.LEFT)
