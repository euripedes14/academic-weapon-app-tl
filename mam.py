import os
import tkinter as tk
import fitz  # PyMuPDF
from PIL import Image, ImageTk
import requests
from io import BytesIO
from tkinter import messagebox
import gmplot

def open_nutrition(nutrition_frame):
    # Clear the frame
    for widget in nutrition_frame.winfo_children():
        widget.destroy()

    #main frame to contain all other frames and widgets
    main_frame = tk.Frame(nutrition_frame, bg="#f2f2f2")
    nutrition_frame.update_idletasks()  
    width = int(nutrition_frame.winfo_width() * 0.6)
    height = int(nutrition_frame.winfo_height() * 0.6)
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=width, height=height)

    #create a canvas and a scrollbar
    canvas = tk.Canvas(main_frame, bg="#f2f2f2")
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f2f2f2")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    #frame for the water tracker
    water_frame = tk.Frame(scrollable_frame, bg="#f2f2f2")
    water_frame.pack(side=tk.TOP, anchor=tk.CENTER)
    tk.Label(water_frame, text="Water Tracker", font=("Arial", 16, "bold"), fg="#005f5f", bg="#f2f2f2").pack(pady=10, anchor=tk.CENTER)
    tk.Label(water_frame, text="Drink 8 glasses of water a day!", font=("Arial", 12), fg="#006666", bg="#f2f2f2", anchor=tk.CENTER).pack(pady=5, anchor=tk.CENTER)
    water_button = tk.Button(water_frame, text="I drank a glass of water", command=lambda: messagebox.showinfo("Water Tracker", "Good job! Keep it up!"),
                             font=("Arial", 12, "bold"), fg="#ffffff", bg="#4CAF50", relief="flat", padx=20, pady=10, anchor=tk.CENTER)
    water_button.pack(pady=5, anchor=tk.CENTER)

    #frame for the PDF menu
    pdf_frame = tk.Frame(scrollable_frame, bg="#f2f2f2")
    pdf_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10, anchor=tk.CENTER)
    pdf_header = tk.Label(pdf_frame, text="Φαγητό της εστίας", font=("Arial", 18, "bold"), bg="#f2f2f2", anchor=tk.CENTER)
    pdf_header.pack(pady=10, anchor=tk.CENTER)

    # PDF URL
    pdf_url = "https://www.upatras.gr/wp-content/uploads/2024/12/%CE%A0%CE%A1%CE%9F%CE%93%CE%A1%CE%91%CE%9C%CE%9C%CE%91-%CE%A3%CE%99%CE%A4%CE%99%CE%A3%CE%97%CE%A3-%CE%99%CE%91%CE%9D%CE%9F%CE%A5%CE%91%CE%A1%CE%99%CE%9F%CE%A3-2025_compressed.pdf"

    #Download the PDF from the web
    response = requests.get(pdf_url)
    pdf_data = BytesIO(response.content)  # Convert the downloaded PDF to a BytesIO object psiloaxreiasto alla tha doume 
    doc = fitz.open(stream=pdf_data, filetype="pdf")

    # AFTO THELEI FTIAXIMO
    page = doc.load_page(0)
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img = ImageTk.PhotoImage(img)
    pdf_label = tk.Label(pdf_frame, image=img, bg="#f2f2f2", anchor=tk.CENTER)
    pdf_label.image = img  # Keep a reference to avoid garbage collection
    pdf_label.pack(anchor=tk.CENTER, pady=10)


#ALLI ORA ACTUAL API
  # Generate a static map image using gmplot
    # gmap = gmplot.GoogleMapPlotter(38.246639, 21.734573, 13)  # Coordinates for Patras, Greece
    # gmap.apikey = "epomeno version tr vrm"  #Google Maps API key
    # gmap.draw("map.html")

    # # Load the generated map image
    # with open("map.html", "r") as file:
    #     map_html = file.read()

    # # Display the map in a label
    # map_label = tk.Label(map_frame, text=map_html, font=("Arial", 14), bg="#f2f2f2", anchor=tk.CENTER)
    # map_label.pack(anchor=tk.CENTER, pady=10)
    # Frame for the map
    map_frame = tk.Frame(scrollable_frame, bg="#f2f2f2")
    map_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, anchor=tk.CENTER)
    map_header = tk.Label(map_frame, text="Αν θέλεις να φας κάτι άλλο μπορείς να το βρεις εδώ!", font=("Arial", 18, "bold"), bg="#f2f2f2", anchor=tk.CENTER)
    map_header.pack(pady=10, anchor=tk.CENTER)

# Load the map image
    map_file_path = "map_to_be_replaced.png"
    if os.path.exists(map_file_path):
        map_image = Image.open(map_file_path)
        map_photo = ImageTk.PhotoImage(map_image)

        # Display the map in a label
        map_label = tk.Label(map_frame, image=map_photo, bg="#f2f2f2", anchor=tk.CENTER)
        map_label.image = map_photo  # Keep a reference to avoid garbage collection
        map_label.pack(anchor=tk.CENTER, pady=10)
    else:
        tk.Label(map_frame, text="Map image not found.", font=("Arial", 14), bg="#f2f2f2", anchor=tk.CENTER).pack(anchor=tk.CENTER, pady=10)