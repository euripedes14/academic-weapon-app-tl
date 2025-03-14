import tkinter as tk
import fitz  # PyMuPDF
from PIL import Image, ImageTk
import requests
from io import BytesIO
from tkinter import messagebox

def open_nutrition(nutrition_frame):
    # Clear the frame
    for widget in nutrition_frame.winfo_children():
        widget.destroy()

    # Create a frame for the water tracker
    water_frame = tk.Frame(nutrition_frame, bg="#ffffff", bd=2, relief="flat")
    water_frame.pack(side=tk.TOP, anchor='ne', padx=10, pady=10)

    # Display the water tracker
    tk.Label(water_frame, text="Water Tracker", font=("Arial", 16, "bold"), fg="#005f5f", bg="#ffffff").pack(pady=20)
    tk.Label(water_frame, text="Drink 8 glasses of water a day!", font=("Arial", 12), fg="#006666", bg="#ffffff").pack(pady=10)

    # Button for tracking water intake
    water_button = tk.Button(water_frame, text="I drank a glass of water", command=lambda: messagebox.showinfo("Water Tracker", "Good job! Keep it up!"),
                             font=("Arial", 12, "bold"), fg="#ffffff", bg="#4CAF50", relief="flat", padx=20, pady=10)
    water_button.pack(pady=10)

    # Create a frame for the PDF menu
    pdf_frame = tk.Frame(nutrition_frame, bg="#ffffff", bd=2, relief="flat")
    pdf_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Add header above the PDF menu
    pdf_header = tk.Label(pdf_frame, text="Φαγητό της εστίας", font=("Arial", 18, "bold"), bg="#ffffff")
    pdf_header.pack(pady=10)

    # PDF URL
    pdf_url = "https://www.upatras.gr/wp-content/uploads/2024/12/%CE%A0%CE%A1%CE%9F%CE%93%CE%A1%CE%91%CE%9C%CE%9C%CE%91-%CE%A3%CE%99%CE%A4%CE%99%CE%A3%CE%97%CE%A3-%CE%99%CE%91%CE%9D%CE%9F%CE%A5%CE%91%CE%A1%CE%99%CE%9F%CE%A3-2025_compressed.pdf"

    # Download the PDF from the web
    response = requests.get(pdf_url)
    pdf_data = BytesIO(response.content)  # Convert the downloaded PDF to a BytesIO object

    # Open the PDF with PyMuPDF
    doc = fitz.open(stream=pdf_data, filetype="pdf")

    # Render the first page of the PDF
    page = doc.load_page(0)
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img = ImageTk.PhotoImage(img)

    # Display the PDF page in a label
    pdf_label = tk.Label(pdf_frame, image=img, bg="#ffffff")
    pdf_label.image = img  # Keep a reference to avoid garbage collection
    pdf_label.pack(fill=tk.BOTH, expand=True)

    # Create a frame for the map
    map_frame = tk.Frame(nutrition_frame, bg="#ffffff", bd=2, relief="flat")
    map_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Add header above the map
    map_header = tk.Label(map_frame, text="Αν θέλεις να φας κάτι άλλο μπορείς να το βρεις εδώ!", font=("Arial", 18, "bold"), bg="#ffffff")
    map_header.pack(pady=10)

    # Placeholder for Google Maps API
    map_label = tk.Label(map_frame, text="Google Maps API Placeholder", font=("Arial", 14), bg="#ffffff")
    map_label.pack(fill=tk.BOTH, expand=True)