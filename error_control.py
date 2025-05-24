class ErrorControl:
    @staticmethod
    def is_time_slot_available(date, hour, events_file="events.txt"):
        try:
            with open(events_file, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) == 3:
                        existing_date, _, existing_hour = [p.strip() for p in parts]
                        if existing_date == date and existing_hour == hour:
                            return False
        except FileNotFoundError:
            pass
        return True