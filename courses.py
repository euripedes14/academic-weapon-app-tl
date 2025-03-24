import tkinter as tk
from tkinter import messagebox, ttk

# Course data will be stored in entries instead of a separate list
course_entries = []
row_count = 6  # Start with 6 rows initially

def save_courses():
    """Save the courses entered in the entry fields"""
    saved_courses = []
    for row in range(len(course_entries)):
        course_name = course_entries[row][0].get().strip()
        if course_name:  # Only save rows with a course name
            professor = course_entries[row][1].get().strip()
            code = course_entries[row][2].get().strip()
            try:
                ects = int(course_entries[row][3].get()) if course_entries[row][3].get() else 0
            except ValueError:
                messagebox.showerror("Σφάλμα", f"Τα ECTS στη γραμμή {row+1} πρέπει να είναι αριθμός!")
                return
            saved_courses.append((course_name, professor, code, ects))
    
    messagebox.showinfo("Αποθήκευση", f"Αποθηκεύτηκαν {len(saved_courses)} μαθήματα.")
    return saved_courses

def add_row():
    """Add a new row to the table"""
    global row_count
    row = row_count
    row_entries = []
    
    for col, width in enumerate(col_widths):
        entry = tk.Entry(table_frame, width=width)
        entry.grid(row=row+1, column=col, padx=5, pady=5, sticky='we')
        row_entries.append(entry)
        
    course_entries.append(row_entries)
    row_count += 1
    
    # Scroll to the bottom to show the new row if many rows exist
    table_frame.update_idletasks()
    if parent_canvas:
        parent_canvas.yview_moveto(1.0)

def open_courses_screen(parent_frame, home_screen):
    global course_entries, row_count, table_frame, col_widths, parent_canvas
    
    course_entries = []
    row_count = 6  # Reset to initial 6 rows
    parent_canvas = None
    
    for widget in parent_frame.winfo_children():
        widget.destroy()

    container = tk.Frame(parent_frame, bg="#f2f2f2")
    container.pack(fill=tk.BOTH, expand=True)

    # Title at the top
    label = tk.Label(container, text="Εισαγωγή Μαθημάτων", font=("Arial", 14))
    label.pack(pady=20)

    # Main content frame - centered horizontally
    main_content = tk.Frame(container, bg="#f2f2f2")
    main_content.pack(expand=True, fill=tk.BOTH)
    
    # Create a frame to hold both table and buttons, centered vertically
    centered_content = tk.Frame(main_content, bg="#f2f2f2")
    centered_content.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    # Table frame with fixed width, placed at top of the centered content
    table_container = tk.Frame(centered_content, bg="#f2f2f2")
    table_container.pack(pady=(0, 10))
    
    # Headers
    headers = ["Μάθημα", "Καθηγητής", "Κωδικός", "ECTS"]
    col_widths = [30, 25, 12, 6]
    
    table_frame = tk.Frame(table_container, bg="#f2f2f2")
    table_frame.pack()
    
    for col, header in enumerate(headers):
        tk.Label(table_frame, text=header, font=("Arial", 10, "bold")).grid(
            row=0, column=col, padx=5, pady=5, sticky='w')
    
    # Create 6 editable rows
    for row in range(6):
        row_entries = []
        for col, width in enumerate(col_widths):
            entry = tk.Entry(table_frame, width=width)
            entry.grid(row=row+1, column=col, padx=5, pady=5, sticky='we')
            row_entries.append(entry)
        course_entries.append(row_entries)

    # Button frame, centered below the table
    button_frame = tk.Frame(centered_content, bg="#f2f2f2")
    button_frame.pack(pady=10)
    
    save_button = tk.Button(button_frame, text="Αποθήκευση", command=save_courses, width=15)
    save_button.pack(side=tk.LEFT, padx=5)
    
    add_row_button = tk.Button(button_frame, text="Προσθήκη Γραμμής", command=add_row, width=15)
    add_row_button.pack(side=tk.LEFT, padx=5)