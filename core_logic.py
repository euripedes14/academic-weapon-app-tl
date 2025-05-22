
# This module contains the core logic for scheduling study sessions using Google OR-Tools.
from ortools.sat.python import cp_model
import math

class StudyScheduler:
    def __init__(self, subjects, user_availability, preferences):
        """
        subjects: list of dicts, each with at least 'course_name', 'study_hours', 'semester_weeks'
        user_availability: dict, e.g. {'Monday': ['18:00-20:00', ...], ...}
        preferences: dict, e.g. {'max_session_length': 2, ...}
        """
        self.subjects = subjects
        self.user_availability = user_availability
        self.preferences = preferences
        self.model = cp_model.CpModel()
        self.slots = []
        self.slot_map = {}
        self.session_vars = {}

    def build_time_slots(self):
        for day, times in self.user_availability.items():
            for t in times:
                start, end = t.split('-')
                # You can split into 1-hour slots, or whatever granularity you want
                self.slots.append((day, t))
                self.slot_map[(day, t)] = len(self.slots) - 1

    def create_variables(self):
        for subj_idx, subj in enumerate(self.subjects):
            for slot_idx, slot in enumerate(self.slots):
                self.session_vars[(subj_idx, slot_idx)] = self.model.NewBoolVar(f"{subj['course_name']}_{slot}")

    def add_constraints(self):
        # No overlapping: only one subject per slot
        for slot_idx in range(len(self.slots)):
            self.model.Add(
                sum(self.session_vars[(subj_idx, slot_idx)] for subj_idx in range(len(self.subjects))) <= 1
            )

        # Instead of requiring all hours, maximize scheduled sessions (soft constraint)
        self.total_sessions = []
        for subj_idx, subj in enumerate(self.subjects):
            total_slots_needed = math.ceil(subj['study_hours'] / self.preferences['max_session_length'])
            subj_sessions = [self.session_vars[(subj_idx, slot_idx)] for slot_idx in range(len(self.slots))]
            # You can require at least 1 session if you want, or just maximize
            # self.model.Add(sum(subj_sessions) >= min(1, total_slots_needed))
            self.total_sessions.extend(subj_sessions)
            # Optionally, you can add a soft lower bound:
            # self.model.Add(sum(subj_sessions) <= total_slots_needed)
            # But do NOT require >= total_slots_needed, so the solver can always find something

    def solve(self):
        self.build_time_slots()
        self.create_variables()
        self.add_constraints()

        # Maximize the total number of scheduled sessions
        self.model.Maximize(sum(self.total_sessions))

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
            return []  # Return empty list if nothing can be scheduled

# Example usage:
if __name__ == "__main__":
    subjects = [
        {'course_name': 'Math', 'study_hours': 45, 'semester_weeks': 15},
        {'course_name': 'Physics', 'study_hours': 30, 'semester_weeks': 15}
    ]
    user_availability = {
        'Monday': ['18:00-20:00'],
        'Wednesday': ['16:00-18:00', '18:00-20:00'],
        'Friday': ['18:00-20:00']
    }
    preferences = {'max_session_length': 2}
    scheduler = StudyScheduler(subjects, user_availability, preferences)
    schedule = scheduler.solve()
    print(schedule)