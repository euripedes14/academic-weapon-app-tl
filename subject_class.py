
class Subject:

    def __init__(self, subjectName, professorNames, hoursStudied, courseCode):
        
        self.name = subjectName
        self.professors = professorNames
        self.hours = hoursStudied
        #self.emails = teacherEmail
        self.code = courseCode


subject1 = Subject("Τεχνολογία Λογισμικού",
                   ["Μιχάλης Ξένος", "Ιωάννης Βασιλόπουλος", "Αριστείδης Ηλίας"],
                   10,
                   "CEID1030")

subject2 = Subject("Προηγμένοι Μικροεπεξεργαστές",
                   ["Νικόλαος Σκλάβος"],
                   5,
                   "CEID1157")

subject3 = Subject("Εργαστήριο Προηγμένοι Μικροεπεξεργαστές",
                   ["Μαριλένα Δούναβη"],
                   20,
                   "CEID1088")

subject4 = Subject("test subject with an extroardinarily long name to test text wrapping i suppose",
                   ["Μαριλένα Δούναβη"],
                   0,
                   "CEID1088")

test_subject_array = [subject1, subject2, subject3, subject4]