
# This module contains the core logic for scheduling study sessions using Google OR-Tools.
# Λογική Ενσωμάτωσης OR-Tools για Προγραμματισμό Μελέτης
# Η βασική ιδέα είναι να χρησιμοποιήσουμε το εργαλείο Google OR-Tools και το Constraint
# Programming (CP-SAT Solver) για να δημιουργήσουμε ένα βέλτιστο πρόγραμμα μελέτης, λαμβάνοντας υπόψη:
# Τις ώρες μελέτης που απαιτούνται για κάθε μάθημα (study_hours)
# Τη διαθεσιμότητα του χρήστη (ημέρες και ώρες που μπορεί να μελετήσει)
# Τις προτιμήσεις του χρήστη (μέγιστη διάρκεια συνεδρίας, στόχοι, αποφυγή back-to-back sessions κ.λπ.)

# Βήματα Λογικής:
# Κατασκευή Χρονικών Διαστημάτων (Time Slots):
# Για κάθε ημέρα και χρονικό διάστημα διαθεσιμότητας του χρήστη, δημιουργούμε ένα slot (π.χ. "Δευτέρα 18:00-20:00").
# Κάθε slot μπορεί να αντιστοιχηθεί σε μία συνεδρία μελέτης.

# Μετατροπή Ωρών Μελέτης σε Συνεδρίες:
# Για κάθε μάθημα, υπολογίζουμε πόσες συνεδρίες χρειάζονται (π.χ. 30 ώρες μελέτης / 2 ώρες ανά συνεδρία = 15 συνεδρίες).

# Μεταβλητές Απόφασης:
# Ορίζουμε δυαδικές μεταβλητές (0/1) για κάθε συνδυασμό μαθήματος και slot:
# session_vars[(μάθημα, slot)] = 1 αν το μάθημα τοποθετηθεί σε αυτό το slot.

# Περιορισμοί (Constraints):
# Κάθε slot να έχει το πολύ ένα μάθημα (όχι επικαλύψεις).
# Ο συνολικός αριθμός συνεδριών ανά μάθημα να μην υπερβαίνει τις απαιτούμενες συνεδρίες.
# (Προαιρετικά) Αποφυγή back-to-back sessions για το ίδιο μάθημα.
# (Προαιρετικά) Κατανομή συνεδριών σε όλο το εξάμηνο.

# Στόχος (Objective):
# Να μεγιστοποιηθεί ο συνολικός αριθμός συνεδριών που τοποθετούνται στο πρόγραμμα 
# (ώστε να καλυφθούν όσο το δυνατόν περισσότερες ώρες μελέτης).

# Επίλυση και Εξαγωγή Προγράμματος:
# Ο αλγόριθμος επιστρέφει για κάθε slot το μάθημα που έχει τοποθετηθεί, δημιουργώντας έτσι ένα εξατομικευμένο πρόγραμμα μελέτης.

# Η παραπάνω λογική έχει ήδη υλοποιηθεί σε μεγάλο βαθμό στην κλάση StudyScheduler. Η πλήρης ενσωμάτωση 
# με το UI και τα πραγματικά δεδομένα του χρήστη απαιτεί περαιτέρω integration, το οποίο δεν προλάβαμε να ολοκληρώσουμε

# StudyScheduler: Αλγόριθμος Προγραμματισμού Μελέτης με χρήση Google OR-Tools

from ortools.sat.python import cp_model
import math
import json

# Φόρτωση προτιμήσεων χρήστη από αρχείο JSON
with open("user_preferences.json", "r", encoding="utf-8") as f:
    user_preferences = json.load(f)

# Ποσοστά κάλυψης στόχων μελέτης ανά προτίμηση
GOAL_PERCENTAGE = {
    "Get a pass": 0.5,
    "Ace my exams": 1.0,
    "Understand material": 0.7,
    "Keep up with assignments": 0.65
}

def get_goal_percentage(goal):
    """Επιστρέφει το αντίστοιχο ποσοστό χρόνου μελέτης βάσει του στόχου"""
    return GOAL_PERCENTAGE.get(goal, 1.0)

class StudyScheduler:
    def __init__(self, subjects, user_availability, preferences):
        """
        subjects: λίστα με λεξικά τύπου {'course_name', 'study_hours', 'semester_weeks'}
        user_availability: διαθεσιμότητα χρήστη ανά ημέρα {'Monday': ['18:00-20:00', ...]}
        preferences: προτιμήσεις χρήστη (π.χ. {'max_session_length': 2})
        """
        self.subjects = subjects
        self.user_availability = user_availability
        self.preferences = preferences
        self.model = cp_model.CpModel()
        self.slots = []          # Λίστα διαθέσιμων slots (π.χ. ('Monday', '18:00-20:00'))
        self.slot_map = {}       # Χάρτης από slot -> index
        self.session_vars = {}   # Δυαδικές μεταβλητές για κάθε μάθημα και slot
        self.total_sessions = [] # Όλες οι μεταβλητές προς μεγιστοποίηση

    def build_time_slots(self):
        """Δημιουργεί slots βάσει της διαθεσιμότητας χρήστη ή προσθέτει default slot αν λείπουν δεδομένα"""
        if not self.user_availability:
            self.slots.append(('Monday', '18:00-20:00'))
            self.slot_map[('Monday', '18:00-20:00')] = 0
        else:
            for day, times in self.user_availability.items():
                if not times:
                    self.slots.append((day, '18:00-20:00'))
                    self.slot_map[(day, '18:00-20:00')] = len(self.slots) - 1
                else:
                    for t in times:
                        self.slots.append((day, t))
                        self.slot_map[(day, t)] = len(self.slots) - 1
        # Αν δεν δημιουργήθηκαν slots (π.χ. κενή είσοδος), προστίθεται default slot
        if not self.slots:
            self.slots.append(('Monday', '18:00-20:00'))
            self.slot_map[('Monday', '18:00-20:00')] = 0

    def create_variables(self):
        """Δημιουργεί τις δυαδικές μεταβλητές απόφασης για κάθε μάθημα-slot"""
        if not self.subjects:
            self.subjects = [{'course_name': 'Dummy', 'study_hours': 2, 'semester_weeks': 1}]
        for subj_idx, subj in enumerate(self.subjects):
            for slot_idx, slot in enumerate(self.slots):
                self.session_vars[(subj_idx, slot_idx)] = self.model.NewBoolVar(f"{subj['course_name']}_{slot}")

    def add_constraints(self):
        """Προσθέτει περιορισμούς για αποφυγή επικαλύψεων και υπερπρογραμματισμού"""
        # Κάθε slot επιτρέπεται να περιέχει το πολύ ένα μάθημα
        for slot_idx in range(len(self.slots)):
            self.model.Add(
                sum(self.session_vars[(subj_idx, slot_idx)] for subj_idx in range(len(self.subjects))) <= 1
            )

        # Περιορισμοί για κάθε μάθημα: μέγιστος αριθμός συνεδριών
        for subj_idx, subj in enumerate(self.subjects):
            study_hours = subj.get('study_hours', 2)
            max_len = self.preferences.get('max_session_length', 2)
            if max_len <= 0:
                max_len = 1
            total_slots_needed = max(1, math.ceil(study_hours / max_len))

            subj_sessions = [self.session_vars[(subj_idx, slot_idx)] for slot_idx in range(len(self.slots))]
            self.total_sessions.extend(subj_sessions)
            self.model.Add(sum(subj_sessions) <= total_slots_needed)

        # (Προαιρετικό): Αποφυγή back-to-back sessions (δεν υλοποιείται ακόμη)

    def solve(self):
        """Εκτελεί τον αλγόριθμο και επιστρέφει το προτεινόμενο πρόγραμμα μελέτης"""
        self.build_time_slots()
        self.create_variables()
        self.add_constraints()

        if not self.total_sessions:
            return []

        self.model.Maximize(sum(self.total_sessions))  # Στόχος: τοποθέτηση όσο περισσότερων sessions γίνεται
        solver = cp_model.CpSolver()
        status = solver.Solve(self.model)

        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            schedule = []
            for subj_idx, subj in enumerate(self.subjects):
                for slot_idx, slot in enumerate(self.slots):
                    if solver.Value(self.session_vars[(subj_idx, slot_idx)]):
                        schedule.append({
                            'subject': subj['course_name'],
                            'day': slot[0],
                            'time': slot[1]
                        })
            return schedule
        else:
            # Επιστροφή default προγράμματος αν δεν βρεθεί λύση
            return [{
                'subject': self.subjects[0]['course_name'],
                'day': self.slots[0][0],
                'time': self.slots[0][1]
            }]
