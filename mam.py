import os
import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import fitz  # PyMuPDF
from geopy.geocoders import Nominatim
import tkintermapview
import json
from map_search import fetch_nearby_food_places, generate_map, search_location

def create_scrollable_frame(nutrition_frame):
    # Main frame to contain all other frames and widgets
    main_frame = tk.Frame(nutrition_frame, bg="#f2f2f2")
    nutrition_frame.update_idletasks()
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.8, relheight=0.8)

    # Create a canvas and a scrollbar
    canvas = tk.Canvas(main_frame, bg="#f2f2f2")
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f2f2f2")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Enable mouse scrolling
    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

    return canvas, scrollable_frame

def open_nutrition(nutrition_frame):
    # Clear the frame
    for widget in nutrition_frame.winfo_children():
        widget.destroy()

    canvas, scrollable_frame = create_scrollable_frame(nutrition_frame)

    # Create a square frame for the message and buttons
    square_frame = tk.Frame(scrollable_frame, bg="#f2f2f2", width=300, height=200, relief=tk.RIDGE, bd=2)
    square_frame.pack(pady=20)
    square_frame.pack_propagate(False)  # Prevent the frame from resizing to fit its content

    # Display the message and buttons inside the square frame
    message_label = tk.Label(square_frame, text="Που θα φας σήμερα?", font=("Arial", 14))
    message_label.pack(pady=20)

    button_frame = tk.Frame(square_frame, bg="#f2f2f2")
    button_frame.pack(pady=10)

    estia_button = tk.Button(button_frame, text="Εστία", command=lambda: scroll_to_section(canvas, scrollable_frame, "estia"))
    estia_button.pack(side=tk.LEFT, padx=20)

    allou_button = tk.Button(button_frame, text="Αλλού", command=lambda: scroll_to_section(canvas, scrollable_frame, "allou"))
    allou_button.pack(side=tk.RIGHT, padx=20)

    # Create sections for estia and allou
    estia_section = tk.Frame(scrollable_frame, bg="#f2f2f2")
    estia_section.pack(fill=tk.BOTH, expand=True, pady=20)
    show_estia(estia_section)

    allou_section = tk.Frame(scrollable_frame, bg="#f2f2f2")
    allou_section.pack(fill=tk.BOTH, expand=True, pady=20)
    show_allou(allou_section)

def scroll_to_section(canvas, scrollable_frame, section):
    if section == "estia":
        canvas.yview_moveto(scrollable_frame.winfo_children()[1].winfo_y() / scrollable_frame.winfo_height())
    elif section == "allou":
        canvas.yview_moveto(scrollable_frame.winfo_children()[2].winfo_y() / scrollable_frame.winfo_height())

def show_estia(parent_frame):
    # Create a square frame for the PDF display
    square_frame = tk.Frame(parent_frame, bg="#f2f2f2", width=900, height=600, relief=tk.RIDGE, bd=2)
    square_frame.pack(pady=20)
    square_frame.pack_propagate(False)  # Prevent the frame from resizing to fit its content

    pdf_header = tk.Label(square_frame, text="Φαγητό της εστίας", font=("Arial", 18, "bold"), bg="#f2f2f2", anchor=tk.CENTER)
    pdf_header.pack(pady=10, anchor=tk.CENTER)

    # PDF URL
    pdf_url = "https://www.upatras.gr/wp-content/uploads/2024/12/%CE%A0%CE%A1%CE%9F%CE%93%CE%A1%CE%91%CE%9C%CE%9C%CE%91-%CE%A3%CE%99%CE%A4%CE%99%CE%A3%CE%97%CE%A3-%CE%99%CE%91%CE%9D%CE%9F%CE%A5%CE%91%CE%A1%CE%99%CE%9F%CE%A3-2025_compressed.pdf"

    # Download the PDF from the web
    response = requests.get(pdf_url)
    pdf_data = BytesIO(response.content)
    doc = fitz.open(stream=pdf_data, filetype="pdf")

    # Display the first page of the PDF
    page = doc.load_page(0)
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img = ImageTk.PhotoImage(img)
    pdf_label = tk.Label(square_frame, image=img, bg="#f2f2f2", anchor=tk.CENTER)
    pdf_label.image = img  # Keep a reference to avoid garbage collection 
    pdf_label.pack(anchor=tk.CENTER, pady=10)

def show_allou(parent_frame):
    # Frame for the map and search bar
    map_frame = tk.Frame(parent_frame, bg="#f2f2f2", width=900, height=600, relief=tk.RIDGE, bd=2)
    map_frame.pack(pady=20)
    map_frame.pack_propagate(False)  # Prevent the frame from resizing to fit its content

    map_header = tk.Label(map_frame, text="Αν θέλεις να φας κάτι άλλο μπορείς να το βρεις εδώ!", font=("Arial", 18, "bold"), bg="#f2f2f2", anchor=tk.CENTER)
    map_header.pack(pady=10, anchor=tk.CENTER)

    # Frame to contain the search bar and map
    search_map_frame = tk.Frame(map_frame, bg="#f2f2f2")
    search_map_frame.pack(fill="both", expand=True)

    # Search bar
    search_frame = tk.Frame(search_map_frame, bg="#f2f2f2")
    search_frame.pack(pady=10)
    search_entry = tk.Entry(search_frame, width=50)
    search_entry.pack(side=tk.LEFT, padx=10)
    search_button = tk.Button(search_frame, text="Search", command=lambda: search_location(map_placeholder, search_entry.get(), search_entry.get()))
    search_button.pack(side=tk.LEFT)

    # Placeholder for the map
    map_placeholder = tk.Frame(search_map_frame, bg="#f2f2f2", width=800, height=500, relief=tk.RIDGE, bd=2)
    map_placeholder.pack(fill="both", expand=True)
    map_placeholder.pack_propagate(False)  # Prevent the frame from resizing to fit its content

    # Generate and display the map
    location = "Patras, Greece"  # Default location
    generate_map(map_placeholder, location)