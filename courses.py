import customtkinter as ctk
from tkinter import messagebox
import openpyxl

def load_semesters_from_excel():
    """Φορτώνει τα εξάμηνα και τα μαθήματα από το Excel."""
    wb = openpyxl.load_workbook("c:\\Users\\yanni\\Documents\\MEGAsync\\CEID\\8th sem - Erasmus\\TL_project\\academic-weapon-app-tl\\ceid_courses.xlsx")
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

    # Main content frame
    main_content = ctk.CTkFrame(container, bg_color="#ffffff")
    main_content.pack(fill="both", expand=True)

    # Semester list
    semester_list_frame = ctk.CTkFrame(main_content, bg_color="#ffffff")
    semester_list_frame.pack(fill="x", pady=10)

    global selected_courses
    selected_courses = []

    for sem, courses in semesters_data.items():
        sem_header = ctk.CTkFrame(semester_list_frame, bg_color="#ffffff")
        sem_header.pack(fill="x", padx=10, pady=5)

        toggle_button = ctk.CTkButton(
            sem_header, text=f"+ Semester {sem}",  # Add "Semester" next to the number
            command=None, fg_color="#e0e0e0", text_color="#000000", hover_color="#d6d6d6"
        )
        toggle_button.pack(fill="x")

        course_frame = ctk.CTkFrame(sem_header, bg_color="#ffffff")

        for course in courses:
            var = ctk.BooleanVar()
            cb = ctk.CTkCheckBox(course_frame, text=course, variable=var, bg_color="#ffffff")  # Removed `text_color`
            cb.pack(anchor="w", padx=20)
            selected_courses.append((course, var))

        # Assign toggle behavior
        toggle_button.configure(command=lambda s=sem, f=course_frame, b=toggle_button: toggle_courses(s, f, b))

    # Save button
    save_button = ctk.CTkButton(main_content, text="Αποθήκευση", command=save_courses, width=20, fg_color="#e0e0e0", text_color="#000000", hover_color="#d6d6d6")
    save_button.pack(pady=20)
