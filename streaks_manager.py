import json
import os

STREAKS_FILE = "streaks.json"

def get_streak(username):
    if not os.path.exists(STREAKS_FILE):
        return 0
    with open(STREAKS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get(username, 0)

def set_streak(username, value):
    if os.path.exists(STREAKS_FILE):
        with open(STREAKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}
    data[username] = value
    with open(STREAKS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def increment_streak(username):
    streak = get_streak(username) + 1
    set_streak(username, streak)
    return streak

def reset_streak(username):
    set_streak(username, 0)
    return 0
