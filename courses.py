# Κλάση: CourseManager
# Ρόλος:
# Διαχειρίζεται τη φόρτωση, αποθήκευση και ανάκτηση μαθημάτων, καθώς και την εξαγωγή δεδομένων για το πρόγραμμα μελέτης.

# Μέθοδοι:
# __init__(self, username=None)
# Αρχικοποιεί το αντικείμενο, φορτώνει τα μαθήματα από το Excel, αποθηκεύει το όνομα χρήστη και το path του αρχείου μαθημάτων.
# load_semesters_from_excel(self)
# Φορτώνει τα μαθήματα ανά εξάμηνο από το αρχείο ceid_courses.xlsx. Επιστρέφει dictionary με εξάμηνα ως keys και λίστες μαθημάτων ως values.
# save_courses(self)
# Αποθηκεύει τα επιλεγμένα μαθήματα του χρήστη στο αρχείο user_subjects.json (keyed by username). Εμφανίζει μήνυμα επιβεβαίωσης με CTkMessagebox.
# load_chosen_subjects(self)
# Επιστρέφει τη λίστα μαθημάτων που έχει αποθηκεύσει ο χρήστης (από το user_subjects.json).
# get_selected_subjects_with_hours(self)
# Επιστρέφει λίστα από dictionaries με τα επιλεγμένα μαθήματα, τις ώρες μελέτης, εβδομάδες εξαμήνου και πληροφορίες περιόδου. Χρησιμοποιείται για να περαστούν τα δεδομένα στον αλγόριθμο προγραμματισμού μελέτης.

# Κλάση: CourseUI
# Υλοποιεί το γραφικό περιβάλλον για την επιλογή μαθημάτων και τις ρυθμίσεις μελέτης.

# Μέθοδοι:
# __init__(self, parent_frame, app_root=None, username=None)
# Αρχικοποιεί το UI, δημιουργεί instance του CourseManager, καλεί το setup_ui.
# setup_ui(self)
# Δημιουργεί το βασικό UI: τίτλο, tabs ("Μαθήματα", "Ρυθμίσεις") και το περιεχόμενο.
# show_courses_tab(self, content_frame)
# Εμφανίζει τη λίστα εξαμήνων και μαθημάτων με checkboxes για επιλογή. Κουμπί αποθήκευσης καλεί το save_courses του CourseManager.
# toggle_courses(sem, course_frame, toggle_button)
# Εναλλάσσει το άνοιγμα/κλείσιμο της λίστας μαθημάτων κάθε εξαμήνου.
# show_settings_tab(self, content_frame)
# Εμφανίζει το UI για τις ρυθμίσεις μελέτης (διαθεσιμότητα, τύπος χρονομέτρου, στόχοι, υπενθυμίσεις, ημερήσιος στόχος κ.λπ.). Κουμπί αποθήκευσης καλεί το save_settings.
# get_availability_dict(self)
# Επιστρέφει dictionary με τη διαθεσιμότητα του χρήστη ανά ημέρα και χρονικό διάστημα.
# save_settings(self, ...)
# Αποθηκεύει όλες τις ρυθμίσεις μελέτης του χρήστη στο αρχείο user_preferences.json (keyed by username). Εμφανίζει μήνυμα επιβεβαίωσης με CTkMessagebox.
# Διασύνδεση με άλλα αρχεία
# ceid_courses.xlsx
# Περιέχει τα μαθήματα και τα εξάμηνα. Το διαβάζει η μέθοδος load_semesters_from_excel.
# user_subjects.json
# Αποθηκεύει τα επιλεγμένα μαθήματα κάθε χρήστη. Το διαβάζουν/γράφουν οι μέθοδοι save_courses και load_chosen_subjects.
# user_preferences.json
# Αποθηκεύει τις ρυθμίσεις μελέτης κάθε χρήστη. Το διαβάζει/γράφει η μέθοδος save_settings.
# CTkMessagebox
# Εμφανίζει μηνύματα επιβεβαίωσης ή σφάλματος στο χρήστη.
# CTkInputDialog (από schedule_screen.py)
# Χρησιμοποιείται για να ζητήσει νέα τιμή αν ο χρήστης βάλει μη έγκυρο ημερήσιο στόχο μελέτης.
# CourseManager
# Τα δεδομένα που επιστρέφει η μέθοδος get_selected_subjects_with_hours χρησιμοποιούνται από τον αλγόριθμο προγραμματισμού μελέτης (core_logic.py).

# Το courses.py παρέχει τόσο το UI όσο και τη λογική για αποθήκευση/φόρτωση δεδομένων, 
# και διασυνδέεται με τα αρχεία δεδομένων και τα υπόλοιπα modules της εφαρμογής.

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import os
import openpyxl
from schedule_screen import CTkInputDialog
from datetime import date
import json

#We took it from here https://www.upatras.gr/stay-tuned/academic-calendar/
# SEMESTER_PERIODS = {
#     "odd": {
#         "start": date(2025, 9, 29),
#         "end": date(2026, 1, 9),
#         "exam_start": date(2026, 1, 19),
#         "exam_end": date(2026, 2, 6),
#     },
#     "even": {
#         "start": date(2026, 2, 16),
#         "end": date(2026, 5, 29),
#         "exam_start": date(2026, 6, 8),
#         "exam_end": date(2026, 6, 26),
#     }
# }
#For testing we will example dates

SEMESTER_PERIODS = {
    "odd": {
        "start": date(2025, 3, 1),      # started in the past
        "end": date(2025, 6, 1),        # ends soon (good for testing "current" semester)
        "exam_start": date(2025, 6, 10),
        "exam_end": date(2025, 6, 20),
    },
    "even": {
        "start": date(2025, 9, 15),     # starts in the future
        "end": date(2026, 1, 15),
        "exam_start": date(2026, 1, 20),
        "exam_end": date(2026, 2, 5),
    }
}

class CourseManager:
    """Handles loading, saving, and toggling courses."""
    def __init__(self, username=None):
        self.selected_courses = []
        self.semesters_data = self.load_semesters_from_excel()
        self.username = username
        self.subjects_file = "user_subjects.json"

    def load_semesters_from_excel(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        excel_path = os.path.join(base_dir, "ceid_courses.xlsx")
        try:
            wb = openpyxl.load_workbook(excel_path)
            sheet = wb.active
        except Exception as e:
            CTkMessagebox(title="Σφάλμα", message=f"Αποτυχία φόρτωσης αρχείου Excel:\n{e}", icon="cancel")
            return {}
        data = {}
        self.course_hours = {}
        if sheet is None:
            CTkMessagebox(title="Σφάλμα", message="Το φύλλο εργασίας Excel δεν βρέθηκε.", icon="cancel")
            return {}
        for row in sheet.iter_rows(min_row=2, values_only=True):
            sem = row[3]
            course_name = row[1]
            study_hours = row[6]
            if not sem or not course_name:
                continue
            if sem in data:
                data[sem].append(course_name)
            else:
                data[sem] = [course_name]
        return data

    def save_courses(self):
        chosen = [course for course, var in self.selected_courses if var.get()]
        data = {}
        if os.path.exists(self.subjects_file):
            with open(self.subjects_file, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except Exception:
                    data = {}
        key = self.username if self.username else "default"
        data[key] = chosen
        with open(self.subjects_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        CTkMessagebox(
            title="Αποθήκευση",
            message=f"Αποθηκεύτηκαν {len(chosen)} μαθήματα.\n\n{', '.join(chosen)}",
            icon="check"
        )
        return chosen

    def load_chosen_subjects(self):
        key = self.username if self.username else "default"
        if os.path.exists(self.subjects_file):
            with open(self.subjects_file, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    return data.get(key, [])
                except Exception:
                    return []
        else:
            return []
        
    def get_selected_subjects_with_hours(self):
        """
        Returns a list of dicts: [{'course_name': ..., 'study_hours': ..., 'semester_weeks': ..., 'period': {...}}, ...]
        for all selected courses.
        """
        chosen = [course for course, var in self.selected_courses if var.get()]
        subjects = []
        for course in chosen:
            hours = self.course_hours.get(course, 30)  # Default to 30 if not found
            # Find semester for this course
            semester = None
            for sem, courses in self.semesters_data.items():
                if course in courses:
                    semester = sem
                    break
            # Determine if odd or even semester
            if semester is not None:
                try:
                    sem_num = int(semester)
                    sem_type = "odd" if sem_num % 2 == 1 else "even"
                except Exception:
                    sem_type = "odd"  # fallback
            else:
                sem_type = "odd"
            # Calculate weeks
            period = SEMESTER_PERIODS[sem_type]
            semester_weeks = (period["end"] - period["start"]).days // 7
            subjects.append({
                'course_name': course,
                'study_hours': hours,
                'semester_weeks': semester_weeks,
                'period': period,
                'semester_type': sem_type,
                'semester': semester
            })
        return subjects

class CourseUI:
    """Handles the UI for course selection and tab switching."""
    def __init__(self, parent_frame, app_root=None, username=None):
        self.manager = CourseManager(username=username)
        self.parent_frame = parent_frame
        self.app_root = app_root
        self.username = username
        self.setup_ui()

    def setup_ui(self):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        ctk.set_appearance_mode("light")
        container = ctk.CTkFrame(self.parent_frame, bg_color="#ffffff")
        container.pack(fill="both", expand=True)
        title = ctk.CTkLabel(container, text="Εισαγωγή Μαθημάτων", font=("Arial", 16, "bold"), text_color="#000000")
        title.pack(pady=20)
        tab_frame = ctk.CTkFrame(container, bg_color="#ffffff")
        tab_frame.pack(fill="x", pady=10)
        courses_tab_button = ctk.CTkButton(
            tab_frame, text="Μαθήματα", command=lambda: self.show_courses_tab(content_frame),
            fg_color="#e0e0e0", text_color="#000000", hover_color="#d6d6d6", width=100
        )
        courses_tab_button.pack(side="left", padx=5)
        settings_tab_button = ctk.CTkButton(
            tab_frame, text="Ρυθμίσεις", command=lambda: self.show_settings_tab(content_frame),
            fg_color="#e0e0e0", text_color="#000000", hover_color="#d6d6d6", width=100
        )
        settings_tab_button.pack(side="left", padx=5)
        content_frame = ctk.CTkFrame(container, bg_color="#ffffff")
        content_frame.pack(fill="both", expand=True, pady=10, padx=10)
        self.show_courses_tab(content_frame)

    def show_courses_tab(self, content_frame):
        for widget in content_frame.winfo_children():
            widget.destroy()
        # Κάνε scrollable το πλαίσιο λίστας εξαμήνων/μαθημάτων
        scrollable_semester_list = ctk.CTkScrollableFrame(content_frame, bg_color="#ffffff")
        scrollable_semester_list.pack(fill="both", expand=True, pady=10)
        self.manager.selected_courses = []
        for sem, courses in self.manager.semesters_data.items():
            sem_header = ctk.CTkFrame(scrollable_semester_list, bg_color="#ffffff")
            sem_header.pack(fill="x", padx=10, pady=5)
            toggle_button = ctk.CTkButton(
                sem_header, text=f"+ Semester {sem}",
                command=None, fg_color="#e0e0e0", text_color="#000000", hover_color="#d6d6d6"
            )
            toggle_button.pack(fill="x")
            course_frame = ctk.CTkFrame(sem_header, bg_color="#ffffff")
            for course in courses:
                var = ctk.BooleanVar()
                cb = ctk.CTkCheckBox(course_frame, text=course, variable=var)
                cb.pack(anchor="w", padx=20)
                self.manager.selected_courses.append((course, var))
            toggle_button.configure(command=lambda s=sem, f=course_frame, b=toggle_button: self.toggle_courses(s, f, b))
        save_button = ctk.CTkButton(content_frame, text="Αποθήκευση", command=self.manager.save_courses, width=20, fg_color="#e0e0e0", text_color="#000000", hover_color="#d6d6d6")
        save_button.pack(pady=20)


    @staticmethod
    def toggle_courses(sem, course_frame, toggle_button):
        if course_frame.winfo_ismapped():
            course_frame.pack_forget()
            toggle_button.configure(text=f"+ Semester {sem}")
        else:
            course_frame.pack(fill="x", padx=30)
            toggle_button.configure(text=f"- Semester {sem}")

    def show_settings_tab(self, content_frame):
        for widget in content_frame.winfo_children():
            widget.destroy()
        # Εμφάνιση όλων των ρυθμίσεων σε scrollable πλαίσιο
        scrollable_settings = ctk.CTkScrollableFrame(content_frame, bg_color="#ffffff")
        scrollable_settings.pack(fill="both", expand=True, pady=10)
        settings_frame = ctk.CTkFrame(scrollable_settings, bg_color="#f9f9f9", corner_radius=10)
        settings_frame.pack(fill="x", pady=20, padx=20)
        settings_title = ctk.CTkLabel(settings_frame, text="Ρυθμίσεις", font=("Arial", 14, "bold"), text_color="#000000")
        settings_title.pack(pady=10)
        import os
        import json
        if self.username:
            pref_path = f"user_preferences_{self.username}.json"
        else:
            pref_path = "user_preferences_default.json"
        # --- Load user preferences if exist ---
        user_prefs = {}
        username = self.username if self.username else "default"
        pref_path = "user_preferences.json"
        if os.path.exists(pref_path):
            try:
                with open(pref_path, "r", encoding="utf-8") as f:
                    all_prefs = json.load(f)
                    # Ensure username is str and not accidentally int
                    user_prefs = all_prefs.get(str(username), {})
            except Exception:
                user_prefs = {}
        # --- Availability UI with time dropdowns ---
        from datetime import time
        def time_options(start=0, end=24):
            # Returns list of HH:MM strings from start to end (step 30min)
            opts = []
            for h in range(start, end):
                opts.append(f"{h:02d}:00")
                opts.append(f"{h:02d}:30")
            opts.append(f"{end:02d}:00")
            return opts
        days = ["Δευτέρα", "Τρίτη", "Τετάρτη", "Πέμπτη", "Παρασκευή", "Σάββατο", "Κυριακή"]
        self.availability_vars = {}
        for day in days:
            frame = ctk.CTkFrame(settings_frame)
            frame.pack(fill="x", padx=10, pady=2)
            ctk.CTkLabel(frame, text=day, width=80).pack(side="left")
            slots = []
            prev_end_idx = 0
            for i in range(3):
                start_var = ctk.StringVar()
                end_var = ctk.StringVar()
                start_menu = ctk.CTkComboBox(frame, values=time_options(), variable=start_var, width=70)
                end_menu = ctk.CTkComboBox(frame, values=time_options(), variable=end_var, width=70)
                start_menu.pack(side="left", padx=2)
                ctk.CTkLabel(frame, text="-").pack(side="left")
                end_menu.pack(side="left", padx=2)
                def update_end_menu(event=None, s_var=start_var, e_menu=end_menu):
                    val = s_var.get()
                    if val:
                        idx = time_options().index(val)
                        e_menu.configure(values=time_options(idx+1))
                        # Reset end if out of range
                        if e_menu.get() and time_options(idx+1).index(e_menu.get()) < 0:
                            e_menu.set("")
                start_menu.bind("<<ComboboxSelected>>", update_end_menu)
                # For next slot, update start options based on previous end
                if i > 0:
                    def update_start_menu(event=None, prev_e_var=slots[i-1][1], s_menu=start_menu):
                        val = prev_e_var.get()
                        if val:
                            idx = time_options().index(val)
                            s_menu.configure(values=time_options(idx+1))
                            if s_menu.get() and time_options(idx+1).index(s_menu.get()) < 0:
                                s_menu.set("")
                    slots[i-1][1].trace_add('write', update_start_menu)
                slots.append((start_var, end_var))
            self.availability_vars[day] = slots
            # Fill from user_prefs if available
            if user_prefs.get("availability", {}).get(day):
                for idx, time_range in enumerate(user_prefs["availability"][day]):
                    if idx < 3:
                        try:
                            start, end = time_range.split("-")
                            slots[idx][0].set(start.strip())
                            slots[idx][1].set(end.strip())
                        except Exception:
                            pass
        # --- Timer preference ---
        timer_label = ctk.CTkLabel(settings_frame, text="Επιλογή Χρονομέτρου:", text_color="#000000")
        timer_label.pack(anchor="w", padx=10, pady=5)
        timer_type_var = ctk.StringVar(value=user_prefs.get("timer_type", "stopwatch"))
        timer_minutes_var = ctk.StringVar(value=str(user_prefs.get("timer_minutes", 25)))
        pomodoro_sessions_var = ctk.StringVar(value=str(user_prefs.get("pomodoro_sessions", 4)))
        timer_frame = ctk.CTkFrame(settings_frame)
        timer_frame.pack(fill="x", padx=10, pady=2)
        def on_timer_type_change(*_):
            if timer_type_var.get() == "stopwatch":
                timer_minutes_entry.configure(state="normal")
                pomodoro_sessions_entry.configure(state="disabled")
            else:
                timer_minutes_entry.configure(state="disabled")
                pomodoro_sessions_entry.configure(state="normal")
        ctk.CTkRadioButton(timer_frame, text="Κανονικό Χρονόμετρο", variable=timer_type_var, value="stopwatch", command=on_timer_type_change).pack(side="left", padx=5)
        timer_minutes_entry = ctk.CTkEntry(timer_frame, textvariable=timer_minutes_var, width=60, placeholder_text="Λεπτά")
        timer_minutes_entry.pack(side="left", padx=5)
        ctk.CTkRadioButton(timer_frame, text="Pomodoro", variable=timer_type_var, value="pomodoro", command=on_timer_type_change).pack(side="left", padx=5)
        pomodoro_sessions_entry = ctk.CTkEntry(timer_frame, textvariable=pomodoro_sessions_var, width=60, placeholder_text="Sessions")
        pomodoro_sessions_entry.pack(side="left", padx=5)
        # Set initial state
        on_timer_type_change()
        # --- Other settings (unchanged, but loaded/saved per user) ---
        study_time_var = ctk.StringVar(value=user_prefs.get("study_time", "Afternoon"))
        study_time_label = ctk.CTkLabel(settings_frame, text="Προτιμώμενη Ώρα Μελέτης:", text_color="#000000")
        study_time_label.pack(anchor="w", padx=10, pady=5)
        study_time_options = ["Morning", "Afternoon", "Evening", "Night"]
        study_time_menu = ctk.CTkComboBox(settings_frame, values=study_time_options, variable=study_time_var)
        study_time_menu.pack(fill="x", padx=10, pady=5)
        goal_var = ctk.StringVar(value=user_prefs.get("goal", "Get a pass"))
        goal_label = ctk.CTkLabel(settings_frame, text="Στόχος Μελέτης:", text_color="#000000")
        goal_label.pack(anchor="w", padx=10, pady=5)
        goal_options = ["Get a pass", "Ace my exams", "Understand material", "Keep up with assignments"]
        goal_menu = ctk.CTkComboBox(settings_frame, values=goal_options, variable=goal_var)
        goal_menu.pack(fill="x", padx=10, pady=5)
        notif_var = ctk.BooleanVar(value=user_prefs.get("notifications", True))
        notif_label = ctk.CTkLabel(settings_frame, text="Υπενθυμίσεις:", text_color="#000000")
        notif_label.pack(anchor="w", padx=10, pady=5)
        notif_checkbox = ctk.CTkCheckBox(settings_frame, text="Ενεργοποίηση Υπενθυμίσεων", variable=notif_var, bg_color="#f9f9f9")
        notif_checkbox.pack(anchor="w", padx=10, pady=5)
        daily_target_var = ctk.StringVar(value=str(user_prefs.get("daily_target", 90)))
        daily_target_label = ctk.CTkLabel(settings_frame, text="Ημερήσιος Στόχος Μελέτης (λεπτά):", text_color="#000000")
        daily_target_label.pack(anchor="w", padx=10, pady=5)
        daily_target_entry = ctk.CTkEntry(settings_frame, textvariable=daily_target_var, placeholder_text="π.χ. 90")
        daily_target_entry.pack(fill="x", padx=10, pady=5)
        no_back_to_back_var = ctk.BooleanVar(value=user_prefs.get("no_back_to_back", False))
        preferences_label = ctk.CTkLabel(settings_frame, text="Προτιμήσεις Χρήστη:", text_color="#000000")
        preferences_label.pack(anchor="w", padx=10, pady=5)
        no_back_to_back_checkbox = ctk.CTkCheckBox(settings_frame, text="Όχι το ίδιο μάθημα συνεχόμενα", variable=no_back_to_back_var, bg_color="#f9f9f9")
        no_back_to_back_checkbox.pack(anchor="w", padx=10, pady=5)
        # Save button
        save_settings_button = ctk.CTkButton(
            settings_frame,
            text="Αποθήκευση Ρυθμίσεων",
            command=lambda: self.save_settings(
                self.get_availability_dict(),
                timer_type_var.get(),
                timer_minutes_var.get(),
                pomodoro_sessions_var.get(),
                study_time_var.get(),
                goal_var.get(),
                notif_var.get(),
                daily_target_var.get(),
                no_back_to_back_var.get()
            ),
            fg_color="#e0e0e0", text_color="#000000", hover_color="#d6d6d6"
        )
        save_settings_button.pack(pady=10)
    def get_availability_dict(self):
        result = {}
        for day, slots in self.availability_vars.items():
            times = []
            for start_var, end_var in slots:
                start = start_var.get().strip()
                end = end_var.get().strip()
                if start and end:
                    times.append(f"{start}-{end}")
            if times:
                result[day] = times
        return result

    def save_settings(self, availability, timer_type, timer_minutes, pomodoro_sessions, study_time, goal, notif, daily_target, no_back_to_back):
        # Save all settings for all users in one file, keyed by username
        pref_path = "user_preferences.json"
        all_prefs = {}
        if os.path.exists(pref_path):
            try:
                with open(pref_path, "r", encoding="utf-8") as f:
                    all_prefs = json.load(f)
            except Exception:
                all_prefs = {}
        username = self.username if self.username else "default"
        # Validate daily_target
        while True:
            try:
                daily_target_int = int(daily_target)
                if daily_target_int <= 0:
                    raise ValueError
                break
            except Exception:
                input_dialog = CTkInputDialog(
                    None,
                    "Λανθασμένη τιμή",
                    "Παρακαλώ εισάγετε έναν θετικό αριθμό για τον ημερήσιο στόχο μελέτης (λεπτά):"
                )
                daily_target = input_dialog.value
                if daily_target is None or daily_target == "":
                    CTkMessagebox(title="Ακύρωση", message="Η αποθήκευση ρυθμίσεων ακυρώθηκε.", icon="warning")
                    return
        # Validate timer_minutes and pomodoro_sessions
        try:
            timer_minutes_int = int(timer_minutes)
        except Exception:
            timer_minutes_int = 25
        try:
            pomodoro_sessions_int = int(pomodoro_sessions)
        except Exception:
            pomodoro_sessions_int = 4
        preferences = {
            "availability": availability,
            "timer_type": timer_type,
            "timer_minutes": timer_minutes_int,
            "pomodoro_sessions": pomodoro_sessions_int,
            "study_time": study_time,
            "goal": goal,
            "notifications": notif,
            "daily_target": daily_target_int,
            "no_back_to_back": no_back_to_back
        }
        # Καθαρισμός παλιού format (αν υπάρχει) ώστε να υπάρχουν μόνο keys με usernames
        # Αν βρεθούν keys που δεν είναι usernames, τα αγνοούμε
        all_prefs = {k: v for k, v in all_prefs.items() if isinstance(v, dict)}
        all_prefs[username] = preferences
        with open(pref_path, "w", encoding="utf-8") as f:
            json.dump(all_prefs, f, ensure_ascii=False, indent=2)
        CTkMessagebox(
            title="Ρυθμίσεις",
            message=(
                f"Οι ρυθμίσεις αποθηκεύτηκαν!\n\n"
                f"Διαθεσιμότητα: {availability}\n"
                f"Χρονομέτρηση: {timer_type} ({timer_minutes_int} λεπτά ή {pomodoro_sessions_int} sessions)\n"
                f"Ώρα Μελέτης: {study_time}\n"
                f"Στόχος: {goal}\n"
                f"Υπενθυμίσεις: {'Ναι' if notif else 'Όχι'}\n"
                f"Ημερήσιος στόχος: {daily_target_int} λεπτά\n"
                f"Όχι το ίδιο μάθημα συνεχόμενα: {'Ναι' if no_back_to_back else 'Όχι'}"
            ),
            icon="check"
        )

