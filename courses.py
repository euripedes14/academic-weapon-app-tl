import customtkinter as ctk
from tkinter import messagebox
from subject_class import *
import openpyxl
import os

# Εφαρμογή breeze theme σε όλα τα CTk widgets
ctk.set_default_color_theme("themes/breeze.json")

def load_semesters_from_excel():
    """Φορτώνει τα εξάμηνα και τα μαθήματα από το Excel."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(base_dir, "ceid_courses.xlsx")
    wb = openpyxl.load_workbook(excel_path)
    sheet = wb.active
    data = {}

    for row in sheet.iter_rows(min_row=2, values_only=True):
        course_id = row[0]
        course_name = row[1]
        department = row[2]
        semester = row[3]
        ects = row[4]
        professor = row[5]
        study_hours = row[6]
        day = row[7]
        start_time = row[8]
        end_time = row[9]

        all_subjects.append(Subject(course_id, course_name, department, semester, ects, [professor], day, start_time, end_time, study_hours))

        if not semester or not course_name:
            continue
        if semester in data:
            data[semester].append(course_name)
        else:
            data[semester] = [course_name]
    return data

semesters_data = load_semesters_from_excel()
selected_courses = []

def save_courses():
    """Αποθηκεύει μόνο τα τσεκαρισμένα μαθήματα."""
    chosen = [course for course, var in selected_courses if var.get()]
    for chosen_course in chosen:
        for subject in all_subjects:
            if subject.course_name == chosen_course:
                chosen_subjects.append(subject)
    messagebox.showinfo("Αποθήκευση", f"Αποθηκεύτηκαν {len(chosen)} μαθήματα.\n\n{', '.join(chosen)}")
    return chosen

def toggle_courses(sem, course_frame, toggle_button):
    """Εμφάνιση/απόκρυψη λίστας μαθημάτων σε ένα εξάμηνο."""
    if course_frame.winfo_ismapped():
        course_frame.pack_forget()
        toggle_button.configure(text=f"+ Semester {sem}")
    else:
        course_frame.pack(fill="x", padx=30)
        toggle_button.configure(text=f"- Semester {sem}")

def open_courses_screen(parent_frame, app_root=None):
    for widget in parent_frame.winfo_children():
        widget.destroy()

    ctk.set_appearance_mode("light")

    container = ctk.CTkFrame(parent_frame)
    container.pack(fill="both", expand=True)

    # Title
    title = ctk.CTkLabel(container, text="Εισαγωγή Μαθημάτων", font=("Arial", 16, "bold"))
    title.pack(pady=20)

    # Tab buttons
    tab_frame = ctk.CTkFrame(container)
    tab_frame.pack(fill="x", pady=10)

    courses_tab_button = ctk.CTkButton(
        tab_frame, text="Μαθήματα", command=lambda: show_courses_tab(content_frame), width=100
    )
    courses_tab_button.pack(side="left", padx=5)

    settings_tab_button = ctk.CTkButton(
        tab_frame, text="Ρυθμίσεις", command=lambda: show_settings_tab(content_frame), width=100
    )
    settings_tab_button.pack(side="left", padx=5)

    # Content frame for tabs
    content_frame = ctk.CTkFrame(container)
    content_frame.pack(fill="both", expand=True, pady=10, padx=10)

    # Show the default tab (Courses)
    show_courses_tab(content_frame)

def show_courses_tab(content_frame):
    """Display the Courses tab."""
    for widget in content_frame.winfo_children():
        widget.destroy()

    semester_list_frame = ctk.CTkFrame(content_frame)
    semester_list_frame.pack(fill="x", pady=10)

    global selected_courses
    selected_courses = []

    for sem, courses in semesters_data.items():
        sem_header = ctk.CTkFrame(semester_list_frame)
        sem_header.pack(fill="x", padx=10, pady=5)

        toggle_button = ctk.CTkButton(
            sem_header, text=f"+ Semester {sem}", command=None
        )
        toggle_button.pack(fill="x")

        course_frame = ctk.CTkFrame(sem_header)

        for course in courses:
            var = ctk.BooleanVar()
            cb = ctk.CTkCheckBox(course_frame, text=course, variable=var)
            cb.pack(anchor="w", padx=20)
            selected_courses.append((course, var))

        toggle_button.configure(command=lambda s=sem, f=course_frame, b=toggle_button: toggle_courses(s, f, b))

    save_button = ctk.CTkButton(content_frame, text="Αποθήκευση", command=save_courses, width=20)
    save_button.pack(pady=20)

def open_calendar_popup(parent, availability_var):
    """Open a calendar-like popup for selecting available study times."""
    popup = ctk.CTkToplevel(parent)
    popup.title("Επιλογή Διαθεσιμότητας")
    popup.geometry("300x400")
    popup.grab_set()

    instructions = ctk.CTkLabel(popup, text="Επιλέξτε τις διαθέσιμες ώρες με κλικ:", font=("Arial", 12))
    instructions.pack(pady=10)

    selected_slots = set()
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    hours = range(8, 21)

    grid_frame = ctk.CTkFrame(popup)
    grid_frame.pack(pady=10)

    # Headers
    for col, day in enumerate(days):
        ctk.CTkLabel(grid_frame, text=day, font=("Arial", 10, "bold")).grid(row=0, column=col + 1, padx=5, pady=5)
    for row, hour in enumerate(hours):
        ctk.CTkLabel(grid_frame, text=f"{hour}:00", font=("Arial", 10)).grid(row=row + 1, column=0, padx=5, pady=5)

    # Buttons
    slot_buttons = {}
    def toggle_slot(day, hour):
        slot = f"{day} {hour}:00-{hour + 1}:00"
        btn = slot_buttons[(day, hour)]
        if slot in selected_slots:
            selected_slots.remove(slot)
            btn.configure(fg_color=None)
        else:
            selected_slots.add(slot)
            btn.configure(fg_color="#90caf9")

    for row, hour in enumerate(hours):
        for col, day in enumerate(days):
            btn = ctk.CTkButton(
                grid_frame, text="", width=25, height=15,
                command=lambda d=day, h=hour: toggle_slot(d, h)
            )
            btn.grid(row=row + 1, column=col + 1, padx=2, pady=2)
            slot_buttons[(day, hour)] = btn

    def save_slots():
        availability_var.set(", ".join(sorted(selected_slots)))
        popup.destroy()

    save_button = ctk.CTkButton(popup, text="Αποθήκευση", command=save_slots)
    save_button.pack(pady=10)

def show_settings_tab(content_frame):
    """Display the Settings tab."""
    for widget in content_frame.winfo_children():
        widget.destroy()

    settings_frame = ctk.CTkFrame(content_frame, corner_radius=10)
    settings_frame.pack(fill="x", pady=20, padx=20)

    settings_title = ctk.CTkLabel(settings_frame, text="Ρυθμίσεις", font=("Arial", 14, "bold"))
    settings_title.pack(pady=10)

    availability_label = ctk.CTkLabel(settings_frame, text="Διαθεσιμότητα Εβδομάδας:")
    availability_label.pack(anchor="w", padx=10, pady=5)

    availability_var = ctk.StringVar()
    availability_entry = ctk.CTkEntry(settings_frame, textvariable=availability_var, state="readonly", placeholder_text="Click to select times")
    availability_entry.pack(fill="x", padx=10, pady=5)

    availability_button = ctk.CTkButton(settings_frame, text="Επιλογή Διαθεσιμότητας", command=lambda: open_calendar_popup(settings_frame, availability_var))
    availability_button.pack(pady=5)

    session_length_label = ctk.CTkLabel(settings_frame, text="Μέγιστη Διάρκεια Συνεδρίας (λεπτά):")
    session_length_label.pack(anchor="w", padx=10, pady=5)

    session_length_entry = ctk.CTkEntry(settings_frame, placeholder_text="e.g., 120")
    session_length_entry.pack(fill="x", padx=10, pady=5)

    preferences_label = ctk.CTkLabel(settings_frame, text="Προτιμήσεις Χρήστη:")
    preferences_label.pack(anchor="w", padx=10, pady=5)

    no_back_to_back_var = ctk.BooleanVar()
    no_back_to_back_checkbox = ctk.CTkCheckBox(settings_frame, text="Όχι το ίδιο μάθημα συνεχόμενα", variable=no_back_to_back_var)
    no_back_to_back_checkbox.pack(anchor="w", padx=10, pady=5)

    pomodoropref_var = ctk.BooleanVar()
    pomodoropref_checkbox = ctk.CTkCheckBox(settings_frame, text="Χρονόμετρο Pomodoro", variable=pomodoropref_var)
    pomodoropref_checkbox.pack(anchor="w", padx=10, pady=5)

    timerpref_var = ctk.BooleanVar()
    timerpref_checkbox = ctk.CTkCheckBox(settings_frame, text="Απλό χρονόμετρο", variable=timerpref_var)
    timerpref_checkbox.pack(anchor="w", padx=10, pady=5)

    save_settings_button = ctk.CTkButton(
    settings_frame,
    text="Αποθήκευση Ρυθμίσεων",
    command=lambda: save_settings(
        availability_var.get(),
        session_length_entry.get(),
        no_back_to_back_var.get(),
        pomodoropref_var.get(),
        timerpref_var.get()
    )
)
    save_settings_button.pack(pady=10)

# def save_settings(availability, session_length, no_back_to_back):
#     """Αποθηκεύει τις ρυθμίσεις του χρήστη."""
#     messagebox.showinfo("Ρυθμίσεις", f"Οι ρυθμίσεις αποθηκεύτηκαν:\n\nΔιαθεσιμότητα: {availability}\nΜέγιστη Διάρκεια: {session_length} λεπτά\nΌχι το ίδιο μάθημα συνεχόμενα: {'Ναι' if no_back_to_back else 'Όχι'}")
def save_settings(availability, session_length, no_back_to_back, pomodoro_pref, timer_pref):
    # Save to a file (overwrite each time)
    with open("user_timer_pref.txt", "w") as f:
        if pomodoro_pref:
            f.write("pomodoro")
        elif timer_pref:
            f.write("stopwatch")
        else:
            f.write("none")
    messagebox.showinfo("Ρυθμίσεις", f"Οι ρυθμίσεις αποθηκεύτηκαν:\n\nΔιαθεσιμότητα: {availability}\nΜέγιστη Διάρκεια: {session_length} λεπτά\nΌχι το ίδιο μάθημα συνεχόμενα: {'Ναι' if no_back_to_back else 'Όχι'}")

