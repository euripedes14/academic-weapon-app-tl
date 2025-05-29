# Ρόλος:
# Αποτελεί το data provider για το εβδομαδιαίο μενού της εστίας και σχετική λογική. 
# Παρέχει πληροφορίες για τα γεύματα κάθε ημέρας, το τρέχον ή επόμενο γεύμα, 
# και την κατάσταση λειτουργίας της εστίας.

# Μέθοδοι:
# __init__(self)
# Αρχικοποιεί το αντικείμενο με το εβδομαδιαίο μενού (self.current_menu), 
# τα χρονικά διαστήματα των γευμάτων (self.meal_times) και τις ημέρες της εβδομάδας (self.days).
# get_current_or_next_meal(self, now=None)

# Επιστρέφει το τρέχον ή το επόμενο γεύμα με βάση την ώρα και την ημέρα.
# Αν δεν είναι ώρα γεύματος, επιστρέφει το επόμενο γεύμα της ημέρας ή το πρωινό της επόμενης ημέρας.
# get_estia_status(self, now=None)
# Επιστρέφει αν η εστία είναι ανοιχτή ή πότε θα ανοίξει ξανά, με βάση την τρέχουσα ώρα.
# get_menu_for_day(self, day)
# Επιστρέφει το πλήρες μενού για μια συγκεκριμένη ημέρα (π.χ. "monday").
# get_meal(self, day, meal)
# Επιστρέφει το μενού για συγκεκριμένο γεύμα (π.χ. "lunch") μιας ημέρας.

# Διασύνδεση με άλλα αρχεία
# homescreenscreen.py
# Η κλάση HomeScreenScreen δημιουργεί instance της Menu για να εμφανίσει το τρέχον 
# ή επόμενο γεύμα και την κατάσταση της εστίας στην αρχική οθόνη.

# homescreen.py
# Μέσω της HomeScreenScreen, το μενού της εστίας εμφανίζεται στην αρχική οθόνη.
# Άλλα modules
# Οποιοδήποτε module χρειάζεται πληροφορίες για το μενού της εστίας ή την κατάστασή της μπορεί να χρησιμοποιήσει την κλάση Menu.
# Συνοπτικά:
# Η κλάση Menu είναι μια pure logic/data class που παρέχει δεδομένα και υπηρεσίες σχετικά με το μενού της εστίας.
# Δεν έχει εξαρτήσεις από UI και μπορεί να χρησιμοποιηθεί από οποιοδήποτε σημείο της εφαρμογής που χρειάζεται 
# πληροφορίες για τα γεύματα ή την κατάσταση της εστίας.

from datetime import datetime, time, timedelta

class Menu:
    def __init__(self):
        self.current_menu = {
            "monday": {
                "breakfast": "Γάλα, καφές, τσάι, άρτος, βούτυρο, μαρμελάδα, τυρόπιτα, χυμός",
                "lunch": {
                    "first_course": "Λαχανόρυζο",
                    "main_courses": [
                        "Σουφλέ με πέννες",
                        "Μακαρόνια με σάλτσα λαχανικών, τυρί τριμμένο"
                    ],
                    "salad": "Μαρούλι με κρεμμύδια φρέσκα, ρόκα, λόλα, λάχανο άσπρο, κόκκινο, καρότο",
                    "dessert": "Φρούτο 2 επιλογές, Αναψυκτικό"
                },
                "dinner": {
                    "first_course": "Μινεστρόνε",
                    "main_courses": [
                        "Γιουβέτσι λαχανικών",
                        "Σουτζουκάκια κοκκινιστά με ριζότο"
                    ],
                    "salad": "Μαρούλι με κρεμμύδια φρέσκα, ρόκα-λόλα, λάχανο άσπρο, κόκκινο, καρότο",
                    "dessert": "Φρούτο 2 επιλογές, Κομπόστα"
                }
            },
            "tuesday": {
                "breakfast": "Γάλα, καφές, τσάι, άρτος, βούτυρο, πραλίνα, ντόνατς, χυμός",
                "lunch": {
                    "first_course": "Κοτόσουπα",
                    "main_courses": [
                        "Κοτόπουλο κοκκινιστό με ριζότο",
                        "Χοιρινό εξοχικό με πατάτες τηγανιτές"
                    ],
                    "salad": "Μαρούλι, ρόκα, λόλα, κρουτόν, λάχανο άσπρο, κόκκινο, πολίτικη, καλαμπόκι, μουστάρδα",
                    "dessert": "Φρούτο 2 επιλογές, Τζατζίκι"
                },
                "dinner": {
                    "first_course": "Σούπα ζυμαρικών",
                    "main_courses": [
                        "Κασερόπιτα με πατάτες φούρνου",
                        "Σπετσοφάι"
                    ],
                    "salad": "Μαρούλι με κρεμμύδια φρέσκα, ρόκα, λάχανο άσπρο, κόκκινο, καρότο",
                    "dessert": "Φρούτο 2 επιλογές, Γιαούρτι"
                }
            },
            "wednesday": {
                "breakfast": "Γάλα, καφές, τσάι, άρτος, βούτυρο, μέλι, κέικ, χυμός",
                "lunch": {
                    "first_course": "Ψαρόσουπα",
                    "main_courses": [
                        "Χταπόδι κοκκινιστό με μακαρονάκι κοφτό",
                        "Βακαλάος αλά σπετσιώτα και πανέ με πατάτες φούρνου"
                    ],
                    "salad": "Μπρόκολο ή κουνουπίδι βραστό-καρότο, μαρούλι με κρεμμύδια φρέσκα, ρόκα, λόλα, λάχανο άσπρο, κόκκινο",
                    "dessert": "Φρούτο 2 επιλογές, Τυρί Φέτα-Γλυκό"
                },
                "dinner": {
                    "first_course": "Τοματόσουπα",
                    "main_courses": [
                        "Στραπατσάδα με τυρί, πατάτες τηγανιτές",
                        "Βολιώτικο ριζότο"
                    ],
                    "salad": "Μαρούλι με κρεμμύδια φρέσκα, ρόκα, λάχανο άσπρο, κόκκινο, καρότο",
                    "dessert": "Φρούτο 2 επιλογές, Τυρί Φέτα"
                }
            },
            "thursday": {
                "breakfast": "Γάλα, καφές, τσάι, άρτος, βούτυρο, μαρμελάδα, σφολιάτα, χυμός",
                "lunch": {
                    "first_course": "Σούπα λαχανικών",
                    "main_courses": [
                        "Κοτόπουλο με σως μουστάρδας-φιογκάκια",
                        "Χοιρινή μπριζόλα ψητή με ριζότο"
                    ],
                    "salad": "Μαρούλι, ρόκα, λόλα, κρουτόν, λάχανο άσπρο, κόκκινο, πολίτικη, καλαμπόκι, μουστάρδα",
                    "dessert": "Φρούτο 2 επιλογές, Τυρί φέτα"
                },
                "dinner": {
                    "first_course": "Κους κους με μανιτάρια",
                    "main_courses": [
                        "Αρακάς λαδερός με πατάτες",
                        "Μακαρόνια με κιμά, τυρί τριμμένο"
                    ],
                    "salad": "Ντομάτα, πιπεριά, κρεμμύδι, λάχανο άσπρο, κόκκινο, καρότο",
                    "dessert": "Φρούτο 2 επιλογές, Ζελέ"
                }
            },
            "friday": {
                "breakfast": "Γάλα, καφές, τσάι, άρτος, βούτυρο, μέλι, αυγό, χυμός",
                "lunch": {
                    "first_course": "Κοφτό μακαρονάκι με σάλτσα",
                    "main_courses": [
                        "Φακές σούπα",
                        "Γίγαντες πλακί"
                    ],
                    "salad": "Ταραμοσαλάτα, ελιές, μαρούλι με κρεμμύδια φρέσκα, ρόκα-λόλα, λάχανο άσπρο, κόκκινο, καρότο, παντζάρια",
                    "dessert": "Φρούτο 2 επιλογές"
                },
                "dinner": {
                    "first_course": "Πουρές με μπέικον",
                    "main_courses": [
                        "Ταλιατέλες με σάλτσα ντομάτας, τυρί τριμμένο",
                        "Μελιτζάνες φούρνου με τυριά και πατάτες τηγανιτές"
                    ],
                    "salad": "Μαρούλι με κρεμμύδια φρέσκα, ρόκα-λόλα, λάχανο άσπρο, κόκκινο, καρότο",
                    "dessert": "Φρούτο 2 επιλογές, Τυρί φέτα"
                }
            },
            "saturday": {
                "breakfast": "Γάλα, καφές, τσάι, άρτος, βούτυρο, μαρμελάδα, ζαμπόν, τυρί, χυμός",
                "lunch": {
                    "first_course": "Σούπα του Σεφ",
                    "main_courses": [
                        "Παστίτσιο",
                        "Κοτόπουλο ψητό με λαζανάκι"
                    ],
                    "salad": "Μαρούλι με κρεμμύδια φρέσκα, ρόκα, λάχανο άσπρο, κόκκινο, καρότο",
                    "dessert": "Φρούτο 2 επιλογές"
                },
                "dinner": {
                    "first_course": "Κριθαρότο λαχανικών",
                    "main_courses": [
                        "Σπανακόρυζο",
                        "Πίτσα special (τυρί, ζαμπόν-μπέικον, πιπέρια ή μαργαρίτα, πατάτες τηγανιτές)"
                    ],
                    "salad": "Μαρούλι με κρεμμύδια φρέσκα, ρόκα, λάχανο άσπρο, κόκκινο, καρότο",
                    "dessert": "Φρούτο 2 επιλογές"
                }
            },
            "sunday": {
                "breakfast": "Γάλα, καφές, τσάι, άρτος, βούτυρο, μαρμελάδα, ζαμπόν, τυρί, χυμός",
                "lunch": {
                    "first_course": "Κρεατόσουπα",
                    "main_courses": [
                        "Μοσχάρι γιουβέτσι",
                        "Χοιρινό αλά μπότσαρη με ριζότο"
                    ],
                    "salad": "Μαρούλι με κρεμμύδια φρέσκα, ρόκα, λάχανο άσπρο, κόκκινο, καρότο",
                    "dessert": "Φρούτο 2 επιλογές, Τυρί φέτα"
                },
                "dinner": {
                    "first_course": "Χορτόσουπα",
                    "main_courses": [
                        "Φασολάκια λαδερά με πατάτες",
                        "Τριβελάκι καρμπονάρα, τυρί τριμμένο"
                    ],
                    "salad": "Ντομάτα, πιπεριά, κρεμμύδι, λάχανο άσπρο, κόκκινο, καρότο",
                    "dessert": "Φρούτο 2 επιλογές, Τυρί φέτα"
                }
            }
        }
        self.meal_times = [
            ("breakfast", time(7, 30), time(9, 0)),
            ("lunch", time(12, 0), time(16, 0)),
            ("dinner", time(19, 0), time(21, 0)),
        ]
        self.days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    def get_current_or_next_meal(self, now=None):
        if now is None:
            now = datetime.now()
        today = now.strftime("%A").lower()
        current_time = now.time()

        # Find current meal
        for meal, start, end in self.meal_times:
            if start <= current_time <= end:
                return today, meal, self.current_menu[today][meal]

        # If not in any meal time, find the next meal today or tomorrow
        for meal, start, _ in self.meal_times:
            if current_time < start:
                return today, meal, self.current_menu[today][meal]

        # If after dinner, show tomorrow's breakfast
        tomorrow = (now.weekday() + 1) % 7
        next_day = self.days[tomorrow]
        return next_day, "breakfast", self.current_menu[next_day]["breakfast"]

    def get_estia_status(self, now=None):
        if now is None:
            now = datetime.now()
        current_time = now.time()

        # Check if currently open
        for meal, start, end in self.meal_times:
            if start <= current_time <= end:
                return "Εστία ανοιχτή"

        # Find next opening time today
        for meal, start, _ in self.meal_times:
            if current_time < start:
                next_open = datetime.combine(now.date(), start)
                delta = next_open - now
                hours, remainder = divmod(delta.seconds, 3600)
                minutes = remainder // 60
                if hours > 0:
                    return f"Η εστία ανοίγει σε {hours} ώρες και {minutes} λεπτά"
                else:
                    return f"Η εστία ανοίγει σε {minutes} λεπτά"

        # If after last meal, show tomorrow's breakfast opening
        tomorrow = now + timedelta(days=1)
        next_open = datetime.combine(tomorrow.date(), self.meal_times[0][1])
        delta = next_open - now
        hours, remainder = divmod(delta.seconds + delta.days * 86400, 3600)
        minutes = (remainder // 60)
        if hours > 0:
            return f"Η εστία ανοίγει σε {hours} ώρες και {minutes} λεπτά"
        else:
            return f"Η εστία ανοίγει σε {minutes} λεπτά"

    def get_menu_for_day(self, day):
        """Return the full menu for a given day (e.g. 'monday')."""
        return self.current_menu.get(day.lower())

    def get_meal(self, day, meal):
        """Return the menu for a specific meal on a given day."""
        return self.current_menu.get(day.lower(), {}).get(meal)