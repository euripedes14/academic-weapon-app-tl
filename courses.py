import customtkinter as ctk
from tkinter import messagebox
import openpyxl
import os  # Import os for handling file paths
import tkinter as tk  # Import tkinter for the calendar popup

def load_semesters_from_excel():
    """Φορτώνει τα εξάμηνα και τα μαθήματα από το Excel."""
    # Get the directory of the current Python file
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Build the path to the Excel file
    excel_path = os.path.join(base_dir, "ceid_courses.xlsx")

    # Load the workbook
    wb = openpyxl.load_workbook(excel_path)
    sheet = wb.active
    data = {}
    for row in sheet.iter_rows(min_row=2, values_only=True):
        sem = row[3]  # Semester is in column D (index 3)
        course_name = row[1]  # Course name is in column B (index 1)
        if not sem or not course_name:
            continue
        if sem in data:
            data[sem].append(course_name)
        else:
            data[sem] = [course_name]
    return data

# Sample semester/course data
semesters_data = load_semesters_from_excel()

# Global list to store selected courses (course name + BooleanVar)
selected_courses = []

def save_courses():
    """Αποθηκεύει μόνο τα τσεκαρισμένα μαθήματα."""
    chosen = [course for course, var in selected_courses if var.get()]
    messagebox.showinfo("Αποθήκευση", f"Αποθηκεύτηκαν {len(chosen)} μαθήματα.\n\n{', '.join(chosen)}")
    return chosen

def toggle_courses(sem, course_frame, toggle_button):
    """Εμφάνιση/απόκρυψη λίστας μαθημάτων σε ένα εξάμηνο."""
    if course_frame.winfo_ismapped():
        course_frame.pack_forget()
        toggle_button.configure(text=f"+ Semester {sem}")  # Use `configure` instead of `config`
    else:
        course_frame.pack(fill="x", padx=30)
        toggle_button.configure(text=f"- Semester {sem}")  # Use `configure` instead of `config`

def open_courses_screen(parent_frame, app_root=None):
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Set light theme
    ctk.set_appearance_mode("light")

    container = ctk.CTkFrame(parent_frame, bg_color="#ffffff")  # Light background color
    container.pack(fill="both", expand=True)

    # Title
    title = ctk.CTkLabel(container, text="Εισαγωγή Μαθημάτων", font=("Arial", 16, "bold"), text_color="#000000")
    title.pack(pady=20)

    # Tab buttons
    tab_frame = ctk.CTkFrame(container, bg_color="#ffffff")
    tab_frame.pack(fill="x", pady=10)

    courses_tab_button = ctk.CTkButton(
        tab_frame, text="Μαθήματα", command=lambda: show_courses_tab(content_frame),
        fg_color="#e0e0e0", text_color="#000000", hover_color="#d6d6d6", width=100
    )
    courses_tab_button.pack(side="left", padx=5)

    settings_tab_button = ctk.CTkButton(
        tab_frame, text="Ρυθμίσεις", command=lambda: show_settings_tab(content_frame),
        fg_color="#e0e0e0", text_color="#000000", hover_color="#d6d6d6", width=100
    )
    settings_tab_button.pack(side="left", padx=5)

    # Content frame for tabs
    content_frame = ctk.CTkFrame(container, bg_color="#ffffff")
    content_frame.pack(fill="both", expand=True, pady=10, padx=10)

    # Show the default tab (Courses)
    show_courses_tab(content_frame)

def show_courses_tab(content_frame):
    """Display the Courses tab."""
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Semester list
    semester_list_frame = ctk.CTkFrame(content_frame, bg_color="#ffffff")
    semester_list_frame.pack(fill="x", pady=10)

    global selected_courses
    selected_courses = []

    for sem, courses in semesters_data.items():
        sem_header = ctk.CTkFrame(semester_list_frame, bg_color="#ffffff")
        sem_header.pack(fill="x", padx=10, pady=5)

        toggle_button = ctk.CTkButton(
            sem_header, text=f"+ Semester {sem}",
            command=None, fg_color="#e0e0e0", text_color="#000000", hover_color="#d6d6d6"
        )
        toggle_button.pack(fill="x")

        course_frame = ctk.CTkFrame(sem_header, bg_color="#ffffff")

        for course in courses:
            var = ctk.BooleanVar()
            cb = ctk.CTkCheckBox(course_frame, text=course, variable=var)  # Removed bg_color
            cb.pack(anchor="w", padx=20)
            selected_courses.append((course, var))

        # Assign toggle behavior
        toggle_button.configure(command=lambda s=sem, f=course_frame, b=toggle_button: toggle_courses(s, f, b))

    # Save button
    save_button = ctk.CTkButton(content_frame, text="Αποθήκευση", command=save_courses, width=20, fg_color="#e0e0e0", text_color="#000000", hover_color="#d6d6d6")
    save_button.pack(pady=20)

def open_calendar_popup(parent, availability_var):
    """Open a calendar-like popup for selecting available study times."""
    popup = tk.Toplevel(parent)
    popup.title("Επιλογή Διαθεσιμότητας")
    popup.geometry("400x400")
    popup.grab_set()  # Make the popup modal

    # Instructions
    instructions = tk.Label(popup, text="Επιλέξτε τις διαθέσιμες ώρες με κλικ:", font=("Arial", 12))
    instructions.pack(pady=10)

    # Time slots grid
    selected_slots = set()  # Store selected time slots

    def toggle_slot(day, hour, button):
        """Toggle the selection of a time slot."""
        slot = f"{day} {hour}:00-{hour + 1}:00"
        if slot in selected_slots:
            selected_slots.remove(slot)
            button.config(bg="white", relief="raised")
        else:
            selected_slots.add(slot)
            button.config(bg="lightblue", relief="sunken")

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    hours = range(8, 21)  # 8:00 to 20:00

    grid_frame = tk.Frame(popup)
    grid_frame.pack(pady=10)

    # Create grid headers
    for col, day in enumerate(days):
        tk.Label(grid_frame, text=day, font=("Arial", 10, "bold")).grid(row=0, column=col + 1, padx=5, pady=5)
    for row, hour in enumerate(hours):
        tk.Label(grid_frame, text=f"{hour}:00", font=("Arial", 10)).grid(row=row + 1, column=0, padx=5, pady=5)

    # Create grid buttons
    for row, hour in enumerate(hours):
        for col, day in enumerate(days):
            button = tk.Button(grid_frame, text="", width=5, height=2, bg="white")
            button.grid(row=row + 1, column=col + 1, padx=2, pady=2)
            # Properly bind the button to the toggle_slot function
            button.config(command=lambda d=day, h=hour, b=button: toggle_slot(d, h, b))

    # Save button
    def save_slots():
        availability_var.set(", ".join(sorted(selected_slots)))
        popup.destroy()

    save_button = tk.Button(popup, text="Αποθήκευση", command=save_slots, bg="lightgreen", font=("Arial", 12))
    save_button.pack(pady=10)

def show_settings_tab(content_frame):
    """Display the Settings tab."""
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Settings Section
    settings_frame = ctk.CTkFrame(content_frame, bg_color="#f9f9f9", corner_radius=10)
    settings_frame.pack(fill="x", pady=20, padx=20)

    settings_title = ctk.CTkLabel(settings_frame, text="Ρυθμίσεις", font=("Arial", 14, "bold"), text_color="#000000")
    settings_title.pack(pady=10)

    # Weekly Availability
    availability_label = ctk.CTkLabel(settings_frame, text="Διαθεσιμότητα Εβδομάδας:", text_color="#000000")
    availability_label.pack(anchor="w", padx=10, pady=5)

    availability_var = tk.StringVar()
    availability_entry = ctk.CTkEntry(settings_frame, textvariable=availability_var, state="readonly", placeholder_text="Click to select times")
    availability_entry.pack(fill="x", padx=10, pady=5)

    availability_button = ctk.CTkButton(settings_frame, text="Επιλογή Διαθεσιμότητας", command=lambda: open_calendar_popup(settings_frame, availability_var), fg_color="#e0e0e0", text_color="#000000", hover_color="#d6d6d6")
    availability_button.pack(pady=5)

    # Max Session Length
    session_length_label = ctk.CTkLabel(settings_frame, text="Μέγιστη Διάρκεια Συνεδρίας (λεπτά):", text_color="#000000")
    session_length_label.pack(anchor="w", padx=10, pady=5)

    session_length_entry = ctk.CTkEntry(settings_frame, placeholder_text="e.g., 120")
    session_length_entry.pack(fill="x", padx=10, pady=5)

    # User Preferences
    preferences_label = ctk.CTkLabel(settings_frame, text="Προτιμήσεις Χρήστη:", text_color="#000000")
    preferences_label.pack(anchor="w", padx=10, pady=5)

    no_back_to_back_var = ctk.BooleanVar()
    no_back_to_back_checkbox = ctk.CTkCheckBox(settings_frame, text="Όχι το ίδιο μάθημα συνεχόμενα", variable=no_back_to_back_var, bg_color="#f9f9f9")
    no_back_to_back_checkbox.pack(anchor="w", padx=10, pady=5)

    # Save Settings Button
    save_settings_button = ctk.CTkButton(settings_frame, text="Αποθήκευση Ρυθμίσεων", command=lambda: save_settings(availability_var.get(), session_length_entry.get(), no_back_to_back_var.get()), fg_color="#e0e0e0", text_color="#000000", hover_color="#d6d6d6")
    save_settings_button.pack(pady=10)

def save_settings(availability, session_length, no_back_to_back):
    """Αποθηκεύει τις ρυθμίσεις του χρήστη."""
    messagebox.showinfo("Ρυθμίσεις", f"Οι ρυθμίσεις αποθηκεύτηκαν:\n\nΔιαθεσιμότητα: {availability}\nΜέγιστη Διάρκεια: {session_length} λεπτά\nΌχι το ίδιο μάθημα συνεχόμενα: {'Ναι' if no_back_to_back else 'Όχι'}")
