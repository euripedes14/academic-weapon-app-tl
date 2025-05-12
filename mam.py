import os
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import fitz  # PyMuPDF
from map_search import MapSearch
import threading

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

def open_nutrition(nutrition_frame):
    for widget in nutrition_frame.winfo_children():
        widget.destroy()

    canvas, scrollable_frame = create_scrollable_frame(nutrition_frame)

    square_frame = ctk.CTkFrame(scrollable_frame, fg_color="#ffffff", width=300, height=200, corner_radius=10)
    square_frame.pack(pady=20)
    square_frame.pack_propagate(False)

    message_label = ctk.CTkLabel(square_frame, text="Που θα φας σήμερα?", font=("Arial", 14), text_color="#000000")
    message_label.pack(pady=20)

    button_frame = ctk.CTkFrame(square_frame, fg_color="#ffffff")
    button_frame.pack(pady=10)

    estia_button = ctk.CTkButton(
        button_frame,
        text="Εστία",
        fg_color="#e0e0e0",
        hover_color="#bdbdbd",
        text_color="#000000",
        command=lambda: scroll_to_section(canvas, scrollable_frame, "estia")
    )
    estia_button.pack(side=ctk.LEFT, padx=20)

    allou_button = ctk.CTkButton(
        button_frame,
        text="Αλλού",
        fg_color="#e0e0e0",
        hover_color="#bdbdbd",
        text_color="#000000",
        command=lambda: scroll_to_section(canvas, scrollable_frame, "allou")
    )
    allou_button.pack(side=ctk.RIGHT, padx=20)

    estia_section = ctk.CTkFrame(scrollable_frame, fg_color="#f2f2f2")
    estia_section.pack(fill=ctk.BOTH, expand=True, pady=20)
    threading.Thread(target=show_estia, args=(estia_section,)).start()

    allou_section = ctk.CTkFrame(scrollable_frame, fg_color="#f2f2f2")
    allou_section.pack(fill=ctk.BOTH, expand=True, pady=20)
    threading.Thread(target=show_allou, args=(allou_section,)).start()

def scroll_to_section(canvas, scrollable_frame, section):
    if section == "estia":
        canvas.yview_moveto(scrollable_frame.winfo_children()[1].winfo_y() / scrollable_frame.winfo_height())
    elif section == "allou":
        canvas.yview_moveto(scrollable_frame.winfo_children()[2].winfo_y() / scrollable_frame.winfo_height())

def show_estia(parent_frame):
    square_frame = ctk.CTkFrame(parent_frame, fg_color="#f2f2f2", width=900, height=600, corner_radius=10)
    square_frame.pack(pady=20)
    square_frame.pack_propagate(False)

    pdf_header = ctk.CTkLabel(square_frame, text="Φαγητό της εστίας", font=("Arial", 18, "bold"), text_color="#000000")
    pdf_header.pack(pady=10)

    pdf_url = "https://www.upatras.gr/wp-content/uploads/2024/12/%CE%A0%CE%A1%CE%9F%CE%93%CE%A1%CE%91%CE%9C%CE%9C%CE%91-%CE%A3%CE%99%CE%A4%CE%99%CE%A3%CE%97%CE%A3-%CE%99%CE%91%CE%9D%CE%9F%CE%A5%CE%91%CE%A1%CE%99%CE%9F%CE%A3-2025_compressed.pdf"

    def load_pdf():
        try:
            response = requests.get(pdf_url)
            pdf_data = BytesIO(response.content)
            doc = fitz.open(stream=pdf_data, filetype="pdf")

            page = doc.load_page(0)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img = ImageTk.PhotoImage(img)

            parent_frame.after(0, lambda: display_pdf(img))
        except Exception as e:
            parent_frame.after(0, lambda: messagebox.showerror("Error", f"Failed to load PDF: {e}"))

    def display_pdf(img):
        if square_frame.winfo_exists():
            pdf_label = ctk.CTkLabel(square_frame, image=img, text="", bg_color="#f2f2f2")
            pdf_label.image = img
            pdf_label.pack(pady=10)

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