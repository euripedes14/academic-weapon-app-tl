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
    def __init__(self):
        self.selected_courses = []
        self.semesters_data = self.load_semesters_from_excel()

    def load_semesters_from_excel(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        excel_path = os.path.join(base_dir, "ceid_courses.xlsx")
        wb = openpyxl.load_workbook(excel_path)
        sheet = wb.active
        data = {}
        self.course_hours = {}
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
        with open("chosen_subjects.txt", "w", encoding="utf-8") as f:
            for course in chosen:
                f.write(course + "\n")
        CTkMessagebox(
            title="Αποθήκευση",
            message=f"Αποθηκεύτηκαν {len(chosen)} μαθήματα.\n\n{', '.join(chosen)}",
            icon="check"
        )
        return chosen

    @staticmethod
    def load_chosen_subjects():
        try:
            with open("chosen_subjects.txt", "r", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
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
    def __init__(self, parent_frame, app_root=None):
        self.manager = CourseManager()
        self.parent_frame = parent_frame
        self.app_root = app_root
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
        semester_list_frame = ctk.CTkFrame(content_frame, bg_color="#ffffff")
        semester_list_frame.pack(fill="x", pady=10)
        self.manager.selected_courses = []
        for sem, courses in self.manager.semesters_data.items():
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
        SettingsManager.show_settings_tab(content_frame)

class AvailabilityCalendar:
    """Handles the calendar popup for selecting available study times."""
    @staticmethod
    def open_calendar_popup(parent, availability_var):
        popup = ctk.CTkToplevel(parent)
        popup.title("Επιλογή Διαθεσιμότητας")
        popup.geometry("400x400")
        popup.grab_set()
        instructions = ctk.CTkLabel(popup, text="Επιλέξτε τις διαθέσιμες ώρες με κλικ:", font=("Arial", 12))
        instructions.pack(pady=10)
        selected_slots = set()
        def toggle_slot(day, hour, button):
            slot = f"{day} {hour}:00-{hour + 1}:00"
            if slot in selected_slots:
                selected_slots.remove(slot)
                button.configure(fg_color="white", text_color="black")
            else:
                selected_slots.add(slot)
                button.configure(fg_color="#90caf9", text_color="black")
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        hours = range(8, 21)
        grid_frame = ctk.CTkFrame(popup)
        grid_frame.pack(pady=10)
        for col, day in enumerate(days):
            ctk.CTkLabel(grid_frame, text=day, font=("Arial", 10, "bold")).grid(row=0, column=col + 1, padx=5, pady=5)
        for row, hour in enumerate(hours):
            ctk.CTkLabel(grid_frame, text=f"{hour}:00", font=("Arial", 10)).grid(row=row + 1, column=0, padx=5, pady=5)
        for row, hour in enumerate(hours):
            for col, day in enumerate(days):
                btn = ctk.CTkButton(
                    grid_frame, text="", width=30, height=20, fg_color="white", text_color="black"
                )
                btn.grid(row=row + 1, column=col + 1, padx=2, pady=2)
                btn.configure(command=lambda d=day, h=hour, b=btn: toggle_slot(d, h, b))
        def save_slots():
            availability_var.set(", ".join(sorted(selected_slots)))
            popup.destroy()
        save_button = ctk.CTkButton(popup, text="Αποθήκευση", command=save_slots, fg_color="lightgreen", text_color="black")
        save_button.pack(pady=10)

class SettingsManager:
    """Handles saving and displaying user settings."""
    @staticmethod
    def show_settings_tab(content_frame):
        for widget in content_frame.winfo_children():
            widget.destroy()
        settings_frame = ctk.CTkFrame(content_frame, bg_color="#f9f9f9", corner_radius=10)
        settings_frame.pack(fill="x", pady=20, padx=20)
        settings_title = ctk.CTkLabel(settings_frame, text="Ρυθμίσεις", font=("Arial", 14, "bold"), text_color="#000000")
        settings_title.pack(pady=10)

        # Availability
        availability_label = ctk.CTkLabel(settings_frame, text="Διαθεσιμότητα Εβδομάδας:", text_color="#000000")
        availability_label.pack(anchor="w", padx=10, pady=5)
        availability_var = ctk.StringVar()
        availability_entry = ctk.CTkEntry(settings_frame, textvariable=availability_var, state="readonly", placeholder_text="Click to select times")
        availability_entry.pack(fill="x", padx=10, pady=5)
        availability_button = ctk.CTkButton(settings_frame, text="Επιλογή Διαθεσιμότητας", command=lambda: AvailabilityCalendar.open_calendar_popup(settings_frame, availability_var), fg_color="#e0e0e0", text_color="#000000", hover_color="#d6d6d6")
        availability_button.pack(pady=5)

        # Timer preference
        timer_label = ctk.CTkLabel(settings_frame, text="Προτίμηση Χρονομέτρου:", text_color="#000000")
        timer_label.pack(anchor="w", padx=10, pady=5)
        timer_pref_var = ctk.StringVar(value="stopwatch")
        timer_options = ["stopwatch", "pomodoro"]
        timer_menu = ctk.CTkComboBox(settings_frame, values=timer_options, variable=timer_pref_var)
        timer_menu.pack(fill="x", padx=10, pady=5)

        # Preferred study time
        study_time_label = ctk.CTkLabel(settings_frame, text="Προτιμώμενη Ώρα Μελέτης:", text_color="#000000")
        study_time_label.pack(anchor="w", padx=10, pady=5)
        study_time_var = ctk.StringVar(value="Afternoon")
        study_time_options = ["Morning", "Afternoon", "Evening", "Night"]
        study_time_menu = ctk.CTkComboBox(settings_frame, values=study_time_options, variable=study_time_var)
        study_time_menu.pack(fill="x", padx=10, pady=5)

        # Study goal
        goal_label = ctk.CTkLabel(settings_frame, text="Στόχος Μελέτης:", text_color="#000000")
        goal_label.pack(anchor="w", padx=10, pady=5)
        goal_var = ctk.StringVar(value="Get a pass")
        goal_options = ["Get a pass", "Ace my exams", "Understand material", "Keep up with assignments"]
        goal_menu = ctk.CTkComboBox(settings_frame, values=goal_options, variable=goal_var)
        goal_menu.pack(fill="x", padx=10, pady=5)

        # Notification preference
        notif_label = ctk.CTkLabel(settings_frame, text="Υπενθυμίσεις:", text_color="#000000")
        notif_label.pack(anchor="w", padx=10, pady=5)
        notif_var = ctk.BooleanVar(value=True)
        notif_checkbox = ctk.CTkCheckBox(settings_frame, text="Ενεργοποίηση Υπενθυμίσεων", variable=notif_var, bg_color="#f9f9f9")
        notif_checkbox.pack(anchor="w", padx=10, pady=5)

        # Daily study target
        daily_target_label = ctk.CTkLabel(settings_frame, text="Ημερήσιος Στόχος Μελέτης (λεπτά):", text_color="#000000")
        daily_target_label.pack(anchor="w", padx=10, pady=5)
        daily_target_var = ctk.StringVar()
        daily_target_entry = ctk.CTkEntry(settings_frame, textvariable=daily_target_var, placeholder_text="π.χ. 90")
        daily_target_entry.pack(fill="x", padx=10, pady=5)

        # No back-to-back
        preferences_label = ctk.CTkLabel(settings_frame, text="Προτιμήσεις Χρήστη:", text_color="#000000")
        preferences_label.pack(anchor="w", padx=10, pady=5)
        no_back_to_back_var = ctk.BooleanVar()
        no_back_to_back_checkbox = ctk.CTkCheckBox(settings_frame, text="Όχι το ίδιο μάθημα συνεχόμενα", variable=no_back_to_back_var, bg_color="#f9f9f9")
        no_back_to_back_checkbox.pack(anchor="w", padx=10, pady=5)

        # Save button
        save_settings_button = ctk.CTkButton(
            settings_frame,
            text="Αποθήκευση Ρυθμίσεων",
            command=lambda: SettingsManager.save_settings(
                availability_var.get(),
                timer_pref_var.get(),
                study_time_var.get(),
                goal_var.get(),
                notif_var.get(),
                daily_target_var.get(),
                no_back_to_back_var.get()
            ),
            fg_color="#e0e0e0", text_color="#000000", hover_color="#d6d6d6"
        )
        save_settings_button.pack(pady=10)


    @staticmethod
    def save_settings(availability, timer_pref, study_time, goal, notif, daily_target, no_back_to_back):
            # Defensive programming for daily_target using CTkInputDialog
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

            # Save all preferences in a single JSON file
            preferences = {
                "availability": availability,
                "timer_pref": timer_pref,
                "study_time": study_time,
                "goal": goal,
                "notifications": notif,
                "daily_target": daily_target_int,
                "no_back_to_back": no_back_to_back
            }
            with open("user_preferences.json", "w", encoding="utf-8") as f:
                json.dump(preferences, f, ensure_ascii=False, indent=2)

            CTkMessagebox(
                title="Ρυθμίσεις",
                message=(
                    f"Οι ρυθμίσεις αποθηκεύτηκαν:\n\n"
                    f"Διαθεσιμότητα: {availability}\n"
                    f"Χρονομέτρηση: {timer_pref}\n"
                    f"Ώρα Μελέτης: {study_time}\n"
                    f"Στόχος: {goal}\n"
                    f"Υπενθυμίσεις: {'Ναι' if notif else 'Όχι'}\n"
                    f"Ημερήσιος στόχος: {daily_target_int} λεπτά\n"
                    f"Όχι το ίδιο μάθημα συνεχόμενα: {'Ναι' if no_back_to_back else 'Όχι'}"
                ),
                icon="check"
            )
   # @staticmethod
    # def save_settings(availability, timer_pref, study_time, goal, notif, daily_target, no_back_to_back):
    #     # Defensive programming for daily_target using CTkInputDialog
    #     while True:
    #         try:
    #             daily_target_int = int(daily_target)
    #             if daily_target_int <= 0:
    #                 raise ValueError
    #             break
    #         except Exception:
    #             input_dialog = CTkInputDialog(
    #                 None,
    #                 "Λανθασμένη τιμή",
    #                 "Παρακαλώ εισάγετε έναν θετικό αριθμό για τον ημερήσιο στόχο μελέτης (λεπτά):"
    #             )
    #             daily_target = input_dialog.value
    #             if daily_target is None or daily_target == "":
    #                 CTkMessagebox(title="Ακύρωση", message="Η αποθήκευση ρυθμίσεων ακυρώθηκε.", icon="warning")
    #                 return

    #     # Save to a file for persistence
    #     with open("user_timer_pref.txt", "w", encoding="utf-8") as f:
    #         f.write(f"{timer_pref}\n")
    #     with open("user_preferences.txt", "w", encoding="utf-8") as f:
    #         f.write(f"availability={availability}\n")
    #         f.write(f"timer_pref={timer_pref}\n")
    #         f.write(f"study_time={study_time}\n")
    #         f.write(f"goal={goal}\n")
    #         f.write(f"notifications={'on' if notif else 'off'}\n")
    #         f.write(f"daily_target={daily_target_int}\n")
    #         f.write(f"no_back_to_back={'yes' if no_back_to_back else 'no'}\n")
    #     CTkMessagebox(
    #         title="Ρυθμίσεις",
    #         message=(
    #             f"Οι ρυθμίσεις αποθηκεύτηκαν:\n\n"
    #             f"Διαθεσιμότητα: {availability}\n"
    #             f"Χρονομέτρηση: {timer_pref}\n"
    #             f"Ώρα Μελέτης: {study_time}\n"
    #             f"Στόχος: {goal}\n"
    #             f"Υπενθυμίσεις: {'Ναι' if notif else 'Όχι'}\n"
    #             f"Ημερήσιος στόχος: {daily_target_int} λεπτά\n"
    #             f"Όχι το ίδιο μάθημα συνεχόμενα: {'Ναι' if no_back_to_back else 'Όχι'}"
    #         ),
    #         icon="check"
    #     )
  
