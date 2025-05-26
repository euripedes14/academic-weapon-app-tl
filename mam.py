# mam.py - 
# Nutrition Screen Classes description:
#
# ScrollableFrame:
#   Provides a scrollable area using a CTkFrame, CTkCanvas, and CTkScrollbar.
#   Used as a container for all nutrition-related UI so content can be scrolled if it overflows.
#
# NutritionMenu:
#   The main entry point for the nutrition screen.
#   Displays the "Που θα φας σήμερα;" message and two buttons ("Εστία", "Αλλού").
#   Handles navigation between the dining hall (EstiaMenu) and alternative food options (AllouMenu).
#   Uses ScrollableFrame to allow scrolling of content.
#
# EstiaMenu:
#   Displays the dining hall ("Εστία") section.
#   Loads and displays the weekly PDF menu from the university website using PyMuPDF and PIL.
#   (Optionally) Can display a hardcoded or parsed menu for each day.
#   Runs PDF loading in a separate thread to keep the UI responsive.
#
# AllouMenu:
#   Displays the "Αλλού" (other food options) section.
#   Shows a map (using MapSearch) where users can search for food places.
#   Displays a loading message while the map is being initialized.
#   Runs map loading in a separate thread to keep the UI responsive.
#
# open_nutrition:
#   Entry point function to launch the NutritionMenu in a given parent frame.


import os
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import fitz  # PyMuPDF
from map_search import MapSearch
import threading

ctk.set_default_color_theme("themes/breeze.json")
ctk.set_appearance_mode("light")

# class ScrollableFrame:
#     def __init__(self, parent):
#         self.main_frame = ctk.CTkFrame(parent, fg_color="#f2f2f2", corner_radius=10)
#         parent.update_idletasks()
#         self.main_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER, relwidth=0.8, relheight=0.8)

#         self.canvas = ctk.CTkCanvas(self.main_frame, bg="#f2f2f2", highlightthickness=0)
#         self.scrollbar = ctk.CTkScrollbar(self.main_frame, orientation="vertical", command=self.canvas.yview)
#         self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color="#f2f2f2")

#         self.scrollable_frame.bind(
#             "<Configure>",
#             lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
#         )

#         self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n")
#         self.canvas.configure(yscrollcommand=self.scrollbar.set)

#         self.canvas.pack(side="left", fill="both", expand=True)
#         self.scrollbar.pack(side="right", fill="y")

#         self.canvas.bind_all("<MouseWheel>", lambda event: self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

#     def get_canvas_and_frame(self):
#         return self.canvas, self.scrollable_frame

class NutritionMenu:
  
    def __init__(self, parent):
        for widget in parent.winfo_children():
            widget.destroy()
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        # Title
        title = ctk.CTkLabel(self.parent, text="Που θα φας σήμερα;", font=("Arial", 20, "bold"), text_color="#000000")
        title.pack(pady=(20, 10))

        # Tabview for Estia/Allou (like spendings)
        self.tabview = ctk.CTkTabview(self.parent, width=900, height=650, corner_radius=15)
        self.tabview.pack(pady=10, padx=20, fill="both", expand=True)

        estia_tab = self.tabview.add("Εστία")
        allou_tab = self.tabview.add("Αλλού")

        # Fill Estia tab
        EstiaMenu(estia_tab)
        # Fill Allou tab
        AllouMenu(allou_tab)

        # self.estia_section = ctk.CTkFrame(self.scrollable_frame, fg_color="#f2f2f2")
        # self.estia_section.pack(fill=ctk.BOTH, expand=True, pady=20)
        #threading.Thread(target=EstiaMenu, args=(self.estia_section,)).start()

        # self.allou_section = ctk.CTkFrame(self.scrollable_frame, fg_color="#f2f2f2")
        # self.allou_section.pack(fill=ctk.BOTH, expand=True, pady=20)
        #threading.Thread(target=AllouMenu, args=(self.allou_section,)).start()

class EstiaMenu:
    def __init__(self, parent_frame):
        self.square_frame = ctk.CTkFrame(parent_frame, width=900, height=600, corner_radius=10)
        self.square_frame.pack(pady=20, padx=20, anchor="center", expand=True)
        self.square_frame.pack_propagate(False)

        pdf_header = ctk.CTkLabel(self.square_frame, text="Φαγητό της εστίας", font=("Arial", 18, "bold"), text_color="#000000")
        pdf_header.pack(pady=10)

        self.pdf_url = "https://www.upatras.gr/wp-content/uploads/2025/04/%CE%A0%CE%A1%CE%9F%CE%93%CE%A1%CE%91%CE%9C%CE%9C%CE%91-%CE%A3%CE%99%CE%A4%CE%99%CE%A3%CE%97%CE%A3_%CE%9C%CE%91%CE%99%CE%9F%CE%A3_-2025_compressed.pdf"
        self.doc = None
        self.current_page = 0
        self.tk_img = None
        self.pdf_label = None

        # Navigation buttons
        nav_frame = ctk.CTkFrame(self.square_frame)
        nav_frame.pack(pady=(0, 10))
        self.prev_btn = ctk.CTkButton(nav_frame, text="<< Προηγούμενη", command=self.prev_page, state="disabled")
        self.prev_btn.pack(side="left", padx=5)
        self.page_label = ctk.CTkLabel(nav_frame, text="Σελίδα 1")
        self.page_label.pack(side="left", padx=5)
        self.next_btn = ctk.CTkButton(nav_frame, text="Επόμενη >>", command=self.next_page, state="disabled")
        self.next_btn.pack(side="left", padx=5)

        threading.Thread(target=self.load_pdf).start()

    def load_pdf(self):
        try:
            response = requests.get(self.pdf_url)
            pdf_data = BytesIO(response.content)
            doc = fitz.open(stream=pdf_data, filetype="pdf")
            self.doc = doc
            self.current_page = 0
            self.square_frame.after(0, self.show_page)
        except Exception as e:
            self.square_frame.after(0, lambda: messagebox.showerror("Error", f"Failed to load PDF: {e}"))

    def show_page(self):
        if not self.doc:
            return
        page = self.doc.load_page(self.current_page)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        self.tk_img = ImageTk.PhotoImage(img)
        if self.pdf_label is None:
            self.pdf_label = ctk.CTkLabel(self.square_frame, image=self.tk_img, text="")
            self.pdf_label.pack(pady=10)
        else:
            self.pdf_label.configure(image=self.tk_img)
            self.pdf_label.image = self.tk_img  # Keep reference

        # Update navigation
        self.page_label.configure(text=f"Σελίδα {self.current_page + 1} από {self.doc.page_count}")
        self.prev_btn.configure(state="normal" if self.current_page > 0 else "disabled")
        self.next_btn.configure(state="normal" if self.current_page < self.doc.page_count - 1 else "disabled")

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page()

    def next_page(self):
        if self.doc and self.current_page < self.doc.page_count - 1:
            self.current_page += 1
            self.show_page()

class AllouMenu:
    def __init__(self, parent_frame):
        self.map_frame = ctk.CTkFrame(parent_frame, width=900, height=600, corner_radius=10)
        self.map_frame.pack(pady=20, padx=20, anchor="center", expand=True)
        self.map_frame.pack_propagate(False)

        map_header = ctk.CTkLabel(
            self.map_frame,
            text="Αν θέλεις να δεις τι άλλες επιλογές έχεις για φαγητό, μπορείς να ψάξεις εδώ!",
            font=("Arial", 18, "bold"),
            text_color="#000000"
        )
        map_header.pack(pady=10)

        # Loading label
        loading_label = ctk.CTkLabel(self.map_frame, text="Φόρτωση χάρτη...", font=("Arial", 14), text_color="#888888")
        loading_label.pack(pady=20)

        def load_map():
            # Only the map search logic runs in the thread
            def on_map_ready():
                loading_label.destroy()
                search_frame = ctk.CTkFrame(self.map_frame)
                search_frame.pack(pady=10)
                search_entry = ctk.CTkEntry(search_frame, width=50)
                search_entry.pack(side=ctk.LEFT, padx=10)
                search_button = ctk.CTkButton(
                    search_frame,
                    text="Search",
                    command=lambda: map_search.search_location(search_entry.get())
                )
                search_button.pack(side=ctk.LEFT)
            map_search = MapSearch(self.map_frame)
            self.map_frame.after(0, on_map_ready)

        threading.Thread(target=load_map).start()

# Entry point for the nutrition screen
def open_nutrition(nutrition_frame):
    NutritionMenu(nutrition_frame)

