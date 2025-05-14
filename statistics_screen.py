import customtkinter as ctk
from subject_class import *

subject_array = chosen_subjects

class StatisticsClass:
    def __init__(self, parent_frame):
        self.parent = parent_frame

        # Κύριο πλαίσιο με λευκό φόντο
        self.main_frame = ctk.CTkFrame(self.parent, corner_radius=10, fg_color="#ffffff")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Πλαίσιο πλοήγησης με λευκό φόντο
        self.categories_frame = ctk.CTkFrame(self.main_frame, width=200, corner_radius=10, fg_color="#f9f9f9")
        self.categories_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Προσθήκη κουμπιών για τις κατηγορίες

        self.add_category_button("Συνολικές Ώρες Μελέτης", self.show_total)

        counter = 0
        for subject in subject_array:
            self.add_category_button(subject.course_name, self.show_subject,  counter)
            counter += 1
        

        # Περιεχόμενο με λευκό φόντο
        self.content_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color="#ffffff")
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)


    def add_category_button(self, text, command, *Args):
        
        # A dictionary to keep track of buttons for highlighting logic
        if not hasattr(self, "category_buttons"):
            self.category_buttons = []

        def wrapped_command():
            for btn in self.category_buttons:
                btn.configure(fg_color="#e0e0e0")  # Reset other buttons
            button.configure(fg_color="#cccccc")  # Highlight pressed button
            command(*Args)  # Execute the passed command

        button = ctk.CTkButton(
            self.categories_frame,
            text=text,
            command=wrapped_command,
            width=250,
            fg_color="#e0e0e0",  # Light gray background for button
            hover_color="#d1d1d1",  # Hover effect
            corner_radius=5,
            text_color="#000000"  # Black text
        )
        button._text_label.configure(wraplength=150)
        button.pack(pady=10)
        self.category_buttons.append(button)  # Add button to tracking list


    def show_subject(self, array_id):
        self.clear_content_frame()
        
        # show subject name

        subject_name_label = ctk.CTkLabel(self.content_frame,
                                      text = "Όνομα Μαθήματος: " + subject_array[array_id].course_name,
                                      text_color = "#000000",
                                      font=('Arial', 30))
        

        subject_name_label.pack(anchor = "w", pady = 5)

        # show subject department
        subject_department_label = ctk.CTkLabel(self.content_frame,
                                      text = "Σχολή Μαθήματος: " + subject_array[array_id].department,
                                      text_color = "#000000",
                                      font=('Arial', 20))
        

        subject_department_label.pack(anchor = "w", pady = 5)

        # show subject code

        subject_code_label = ctk.CTkLabel(self.content_frame,
                                      text = "Κωδικός Μαθήματος: " + subject_array[array_id].course_id,
                                      text_color = "#000000",
                                      font=('Arial', 15))
        

        subject_code_label.pack(anchor = "w", pady = 5)

        # show subject ects

        subject_ects_label = ctk.CTkLabel(self.content_frame,
                                      text = "ECTS Μαθήματος: " + str(subject_array[array_id].ects),
                                      text_color = "#000000",
                                      font=('Arial', 15))
        

        subject_ects_label.pack(anchor = "w", pady = 5)

        # show teacher(s) name

        if len(subject_array[array_id].professor) == 1:
            professor_label = ctk.CTkLabel(self.content_frame,
                                           text = "Όνομα Καθηγητή: " + subject_array[array_id].professor[0],
                                           text_color = "#000000",
                                           font=('Arial', 20))
            
            professor_label.pack(anchor = "w", pady = 5)
        
        else:
            
            teacher_title_label = ctk.CTkLabel(self.content_frame,
                                               text = "Ονόματα Καθηγητών: ",
                                               text_color = "#000000",
                                               font=('Arial', 20))
            
            teacher_title_label.pack(anchor = "w", pady = 5)

            for teacherName in subject_array[array_id].professor:

                professor_label = ctk.CTkLabel(self.content_frame,
                                               text = teacherName,
                                               text_color = "#000000",
                                               font=('Arial', 20))
                
                professor_label.pack(anchor = "w", pady = 5, padx=50,)
                

        # show hours studied

        hours_label = ctk.CTkLabel(self.content_frame,
                                   text = "Ώρες Μελέτης: " + str(subject_array[array_id].study_hours),
                                   text_color = "#000000",
                                   font=('Arial', 20))
        
        hours_label.pack(anchor = "w", pady = 5)

    def show_total(self):
        
        self.clear_content_frame()

        total_study_hours = 0

        for subject in subject_array:
            total_study_hours += subject.study_hours
        
        
        hours_label = ctk.CTkLabel(self.content_frame,
                                   text = "Συνολικές Ώρες Μελέτης: " + str(total_study_hours),
                                   text_color = "#000000",
                                   font=('Arial', 30))
        
        hours_label.pack(anchor = "w", pady = 5)

        indiv_label = ctk.CTkLabel(self.content_frame,
                                   text = "\nΞεχωριστά ώρες μελέτης ανά μάθημα: ",
                                   text_color = "#000000",
                                   font=('Arial', 25))
        
        indiv_label.pack(anchor = "w", pady = 5)

        for subject in subject_array:
            indiv_subject_hours = ctk.CTkLabel(self.content_frame,
                                               text = str(subject.course_name) + ": " + str(subject.study_hours),
                                               text_color = "#000000",
                                               font=('Arial', 20))
            
            indiv_subject_hours.pack(anchor = "w", pady = 5)

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("800x600")  # Ορισμός μεγέθους του κύριου παραθύρου
    root.title("Στατιστικά")

    app = StatisticsClass(root)  # Παράμετρος "root" στο γονικό πλαίσιο
    root.mainloop()
